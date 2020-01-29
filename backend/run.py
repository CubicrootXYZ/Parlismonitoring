# ALWAYS generate a new Connection for each thread when mutlithreading. Else the connection.insert_id() might brake

from bs4 import BeautifulSoup
import requests, PyPDF2
from io import BytesIO
import spacy, configparser, logging, pytz, os, time, datetime, random
from includes import mysql

try:
    os.chdir("D:\github_repos\landtags-parlis-monitoring\\backend")
except: 
    os.chdir("/mnt/d/github_repos/landtags-parlis-monitoring")

class parlisScrape():

    def __init__(self):
        self.state = self.loadConfig()   #also sets up db connection
    

        self.nlp = spacy.load("de_core_news_sm")
       

    def scrape(self):
        self.logger.info("---- Start scraping ---- ")
        if not self.state:
            self.logger.error("Can not start scraping, Setup seems wrong.")
            return False

        file = {}        
        page = self.getPage(self.url)

        if (page == False):
            self.logger.error("Can not get page from %s", url)
            return False

        #get each file from the page
        for entry in page.split('<hr class="col-xs-12 divider divider-small">'):
            file_info = True

            soup = BeautifulSoup(entry, 'html.parser')

            file['title'] = soup.a.get_text()
            self.logger.debug("Got document with title: %s", file['title'])

            # stop at the end of the page
            if "Weitere Dokumente anzeigen" in file['title'] or len(file['title']) < 2:
                self.logger.debug("---- Reached end of scraped page ----")
                break
            
            file['keywords'] = self.getKeywords(file['title'])            

            info = soup.find_all('li') 
            try:
                date = info[1].getText().replace("Datum: ", "", 1).split(".")
                file['number'] = info[0].getText()
                file['date'] = date[2]+"-"+date[1]+"-"+date[0]
                file['type'] = info[2].getText().replace("Art: ", "", 1)
                file['author'] = info[3].getText().replace("Urheber: ", "", 1)
                file['link'] = 'https://www.landtag-bw.de'+soup.a.get('href')
            except:
                self.logger.warning("File information not available.")
                file_info = False
                
            # only go on if the file exists and we got all the data needed
            if file_info and not self.exists(file):        
                # analyze the pdf file 
                self.logger.debug("Extract keywords from PDF")           
                try:
                    file_ = requests.get(file['link']).content
                    file_mem = BytesIO(file_)
                    file_read = PyPDF2.PdfFileReader(file_mem)
                    number_of_pages = file_read.getNumPages()
                    file_content = ''
                    i = 0
                    while (i < number_of_pages):
                        page = file_read.getPage(i)
                        file_content += ' '+page.extractText().replace("_", " ").replace(".", " ").replace(",", " ").replace("0", " ").replace("1", " ").replace("2", " ").replace("3", " ").replace("4", " ").replace("5", " ").replace("6", " ").replace("7", " ").replace("8", " ").replace("9", " ")
                        i += 1

                    file['keywords_content'] = self.getKeywords(file_content)
                except Exception as e: 
                    self.logger.info("Not able of catching PDF file: %s", e)

                # insert all keywords into the database
                file['keywords_id'] = self.insertKeywords(file['keywords'])           
                file['keywords_content_id'] = self.insertKeywords(file['keywords_content'])      
                file['authors_id'] = self.insertAuthors(file['author'].replace(" ", "").split(','))

                # insert file in database 
                if file['keywords_id'] != False and file['keywords_content_id'] != False:
                    self.insert(file)                

    def exists(self, file):
        res = self.conDatabase.selectFrom(self.prefix+'files', 'COUNT(*)', 'title = "'+file['title']+'" AND number = "'+file['number']+'"')

        if res == False:
            return False

        if res[0]['COUNT(*)'] > 0:
            self.logger.debug("File %s exists already!", file['title'])
            return True
        self.logger.debug("File %s does not exists in database.", file['title'])
        return False

    def insert(self, file):
        
        res = self.conDatabase.insertInto(self.prefix+"files", [['title', file['title']], ['number', file['number']], ['date', file['date']], ['type',file['type']], ['link', file['link']]])

        if res == False:
            return False

        file['id'] = self.conDatabase.selectFrom(self.prefix+'files', '*', 'title = "'+file['title']+'" AND number = "'+file['number']+'"')[0]['id']
        
        #file['id'] = self.conDatabase.lastId()

        for id in file['keywords_id']:
            if not self.conDatabase.insertInto(self.prefix+'files_keywords', [['word_id', id], ['file_id', file['id']], ['date', file['date']]]):
                self.logger.warning("Can not insert keyword.")

        for id in file['keywords_content_id']:
            if not self.conDatabase.insertInto(self.prefix+'files_keywords_content', [['word_id', id], ['file_id', file['id']], ['date', file['date']]]):
                self.logger.warning("Can not insert keyword.")

        for id in file['authors_id']:
            if not self.conDatabase.insertInto(self.prefix+'authors_files', [['author_id', id], ['file_id', file['id']]]):
                self.logger.warning("Can not insert author.")

        self.logger.debug("Inserted everything into the database")
        return True

    def getPage(self, url):
        try:
            res = requests.get(url).text
            return res
        except Exception as e:
            self.logger.error("Can not get Page: %s", e)
            return False

    # lemmatizes the given text and returns all nouns
    def getKeywords(self, text):
        doc = self.nlp(text)
        keywords=[]
        for token in doc:
            if token.pos_ == "NOUN":
                if token.lemma_ not in keywords and len(token.lemma_) > 2:
                    keywords.append(token.lemma_.replace(" ", ""))

        return keywords

    def insertAuthors(self, authors):
        authors_text = ''
        authors_list = []
        for author in authors:
            authors_text += '"'+author+'",'

        authors_text = authors_text[:-1]

        res = self.conDatabase.execute("SELECT * FROM "+self.prefix+"authors WHERE author IN ("+authors_text+")")

        if res == False:
            self.logger.warning("Can not get authors")
            return False

        for entry in res:
            if entry['author'] in authors:
                authors_list.append(entry['id'])
                authors.remove(entry['author'])
        
        for author in authors:
            res = self.conDatabase.insertInto(self.prefix+'authors', [['author', author]])
            if res == False:
                self.logger.warning("Can not insert auhtors")
                return False
            authors_list.append(self.conDatabase.execute("SELECT * FROM "+self.prefix+"authors WHERE author = '"+author+"'")[0]['id'])

        return authors_list
        


    # checks which keywords are already in the database and adds all the other ones
    def insertKeywords(self, keywords):
        trigger = False
        words_list = []
        words = ''
        for word in keywords: 
            words += '"'+word+'",'

        words = words[:-1]

        res = self.conDatabase.execute("SELECT * FROM "+self.prefix+"keywords WHERE word IN ("+words+")")
        if res == False:
            self.logger.warning("Can not get keywords")
            return False

        for entry in res:
            if entry['word'] in keywords:
                words_list.append(entry['id'])
                keywords.remove(entry['word'])


        for word in keywords:
            res = self.conDatabase.insertInto(self.prefix+'keywords', [['word', word]])
            if res == False:
                self.logger.warning("Can not insert keywords")
                return False
            words_list.append(self.conDatabase.execute("SELECT * FROM "+self.prefix+"keywords WHERE word = '"+word+"'")[0]['id'])

        return words_list

    def loadConfig(self):
        config = configparser.ConfigParser()
        config.readfp(open('config.ini'))
        host = config.get('database', 'host')
        database = config.get('database', 'database')
        user = config.get('database', 'user')
        password = config.get('database', 'password')
        logging_level_console = config.get('logging', 'level_console')
        logging_level_file = config.get('logging', 'level_file')
        logfile = config.get('logging', 'filepath')
        log = config.get('logging', 'active')
        self.prefix = config.get('database', 'prefix')
        self.url = config.get('parlis', 'url')

        if not self.setupLogger(log, logging_level_console, logging_level_file, logfile):
            return False

        self.logger.debug("Setup database.")

        if self.setupDatabase(host, database, user, password):
            return True

        return False

    def setupDatabase(self, host, database, username, password):
        self.conDatabase = mysql.Database(host, database, username, password, self.logger)

        if self.conDatabase.connect():
            try:
                self.conDatabase.createTable(self.prefix+"files", ['title VARCHAR(1000)', 'number VARCHAR(100)', 'date DATE', 'type VARCHAR(100)', 'link VARCHAR(500)'])
                self.conDatabase.createTable(self.prefix+"keywords", ['word VARCHAR(100)'])
                self.conDatabase.createTable(self.prefix+"files_keywords", ['word_id INT', 'file_id INT', 'date DATE'])
                self.conDatabase.createTable(self.prefix+"files_keywords_content", ['word_id INT', 'file_id INT', 'date DATE'])
                self.conDatabase.createTable(self.prefix+"authors", ['author VARCHAR(100)'])
                self.conDatabase.createTable(self.prefix+"authors_files", ['author_id INT', 'file_id INT'])
            except Exception as e:
                self.logger.error("Could not create Tables: %s", e)
                return False
            self.logger.debug("Succesfuly connected to database.")
            return True
        else:
            self.logger.error("Could not connec to to Database.")
            return False
        return True

    def __del__(self):
        self.logger.debug("Close everything. Good bye.")
        self.conDatabase.close()

    def setupLogger(self, active, level_console, level_file, file):
        try: 
            self.logger = logging.getLogger('PARLISMONITORING')

            self.ch = logging.StreamHandler()
            if level_console == 0:
                self.ch.setLevel(logging.DEBUG)
            elif level_console == 1:
                self.ch.setLevel(logging.WARNING)
            elif level_console == 2:
                self.ch.setLevel(logging.ERROR)
        
            self.log = logging.FileHandler(file)
            if level_console == 0:
                self.log.setLevel(logging.DEBUG)
            elif level_console == 1:
                self.log.setLevel(logging.WARNING)
            elif level_console == 2:
                self.log.setLevel(logging.ERROR)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.ch.setFormatter(formatter)
            self.log.setFormatter(formatter)
            self.logger.addHandler(self.ch)
            if active == 1:    
                self.logger.addHandler(self.log)
            self.logger.debug("--------------------------------- START --------------------------------")
            self.logger.debug("Successfuly setup the logger.")
            self.local = pytz.timezone("Europe/Berlin")
            return True
        except Exception as e:
            print("Not able to initialize Logger: ", e)
            return False


class Timer():

    def __init__(self):
        self.next_scrapetime = datetime.datetime.now()
        self.loop()

    def loop(self):
        while True:
            if datetime.datetime.now() >= self.next_scrapetime:
                run = parlisScrape()
                run.scrape()

                self.next_scrapetime = self.nextScrape()

            time.sleep(180)

    def nextScrape(self):
        if datetime.datetime.now().weekday() == 6:
            return datetime.datetime.now()+datetime.timedelta(hours=30-int(datetime.datetime.now().strftime("%H")), minutes=random.randint(1,44))           
        elif (int(datetime.datetime.now().strftime("%H")) >= 16):
            return datetime.datetime.now()+datetime.timedelta(hours=30-int(datetime.datetime.now().strftime("%H")), minutes=random.randint(1,44))
        elif (int(datetime.datetime.now().strftime("%H")) <= 6):
            return datetime.datetime.now()+datetime.timedelta(hours=6-int(datetime.datetime.now().strftime("%H")), minutes=random.randint(1,44))
        else:
            return datetime.datetime.now()+datetime.timedelta(hours=random.randint(1,2), minutes=random.randint(1,44))


start = Timer()

