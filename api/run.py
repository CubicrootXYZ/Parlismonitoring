# -*- coding: utf-8 -*-
import redis, configparser, falcon, os, logging, pytz, datetime, json
from includes import mysql
from sqlescapy import sqlescape
from falcon import uri

r = redis.Redis(host="redis")
#print(conn.set('hello', 'world'))
#print(conn.get('hello'))

# reading config
config = configparser.ConfigParser()
config.readfp(open('config.ini'))
dbhost = config.get('database', 'host')
dbdatabase = config.get('database', 'database')
dbuser = config.get('database', 'user')
dbpassword = config.get('database', 'password')
logging_level_console = config.get('logging', 'level_console')
logging_level_file = config.get('logging', 'level_file')
logging_file = config.get('logging', 'filepath')
logging_active = config.get('logging', 'active')
prefix = config.get('database', 'prefix')
caching_minutes = config.get('caching', 'minutes')
caching_hours = config.get('caching', 'hours')
# setup logger
try: 
    logger = logging.getLogger('PARLISMONITORING-API')

    ch = logging.StreamHandler()
    if logging_level_console == 0:
        ch.setLevel(logging.DEBUG)
    elif logging_level_console == 1:
        ch.setLevel(logging.WARNING)
    elif logging_level_console == 2:
        ch.setLevel(logging.ERROR)

    log = logging.FileHandler(logging_file)
    if logging_level_console == 0:
        log.setLevel(logging.DEBUG)
    elif logging_level_console == 1:
        log.setLevel(logging.WARNING)
    elif logging_level_console == 2:
        log.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.setFormatter(formatter)
    logger.addHandler(ch)
    if logging_active == 1:    
        logger.addHandler(log)
    logger.debug("--------------------------------- START --------------------------------")
    logger.debug("Successfuly setup the logger.")
    local = pytz.timezone("Europe/Berlin")
except Exception as e:
    print("Not able to initialize Logger: ", e)
    exit()
# setup db
conDatabase = mysql.Database(dbhost, dbdatabase, dbuser, dbpassword, logger)

class GetWordClouds():
    def __init__(self, days=183):
        self.days = days

    def on_get(self, req, resp):
        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        data = {"status": "success", "data": {}}

        redisCache = r.get("wordclouds")

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                res = conDatabase.execute("SELECT COUNT(word_id) AS counter, author, word FROM "+prefix+"files_keywords INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords.word_id = "+prefix+"keywords.id) INNER JOIN "+prefix+"files ON ("+prefix+"files_keywords.file_id = "+prefix+"files.id) INNER JOIN "+prefix+"authors_files ON ("+prefix+"files.id = "+prefix+"authors_files.file_id) INNER JOIN "+prefix+"authors ON ("+prefix+"authors_files.author_id = "+prefix+"authors.id) WHERE "+prefix+"files_keywords.date > '"+critical_date.strftime("%Y-%m-%d")+"' GROUP BY "+prefix+"authors.author, "+prefix+"keywords.word ORDER BY counter")
                
                for entry in res:

                    if entry['author'] in word_list:
                        word_list[entry['author']].update({entry['word'] : entry['counter']}) #TODO: does not work
                    else:
                        word_list[entry['author']] = {entry['word'] : entry['counter']}

                data['data'] = word_list

                r.setex("wordclouds", datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data["data"] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data)

        conDatabase.close()

class GetWordCloud():
    def __init__(self, days=183):
        self.days = days

    def on_get(self, req, resp):
        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        data = {"status": "success", "data": {}}

        redisCache = r.get("wordcloud")

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                res = conDatabase.execute("SELECT COUNT(word_id) AS counter, word FROM "+prefix+"files_keywords INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords.word_id = "+prefix+"keywords.id) INNER JOIN "+prefix+"files ON ("+prefix+"files_keywords.file_id = "+prefix+"files.id) INNER JOIN "+prefix+"authors_files ON ("+prefix+"files.id = "+prefix+"authors_files.file_id) INNER JOIN "+prefix+"authors ON ("+prefix+"authors_files.author_id = "+prefix+"authors.id) WHERE "+prefix+"files_keywords.date > '"+critical_date.strftime("%Y-%m-%d")+"' GROUP BY "+prefix+"keywords.word ORDER BY COUNT(word_id) DESC LIMIT 40")
            

                data['data'] = res

                r.setex("wordcloud", datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data["data"] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data)

        conDatabase.close()

class GetWordByDay():
    def __init__(self, days=183):
        self.days = days

    def on_get(self, req, resp, word):
        word = uri.decode(word)
        print(word)
        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        data = {"status": "success", "data": {}}

        redisCache = r.get("wordbyday_"+word)

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                res = conDatabase.execute("SELECT COUNT(word_id), date FROM "+prefix+"files_keywords INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords.word_id = "+prefix+"keywords.id) WHERE "+prefix+"files_keywords.date > '"+critical_date.strftime("%Y-%m-%d")+"' AND "+prefix+"keywords.word LIKE '"+sqlescape(word)+"%' GROUP BY "+prefix+"files_keywords.date ORDER BY date")
                res2 = conDatabase.execute("SELECT COUNT(word_id), date FROM "+prefix+"files_keywords_content INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords_content.word_id = "+prefix+"keywords.id) WHERE "+prefix+"files_keywords_content.date > '"+critical_date.strftime("%Y-%m-%d")+"' AND "+prefix+"keywords.word LIKE '"+sqlescape(word)+"%' GROUP BY "+prefix+"files_keywords_content.date ORDER BY date")
                

                for entry in res:

                    word_list[entry['date'].strftime("%Y-%m-%d")] = entry['COUNT(word_id)']

                for entry in res2:
                    if (entry['date'].strftime("%Y-%m-%d") in word_list):
                        word_list[entry['date'].strftime("%Y-%m-%d")] += entry['COUNT(word_id)']
                    else: 
                        word_list[entry['date'].strftime("%Y-%m-%d")] = entry['COUNT(word_id)']

                data['data'] = word_list


                r.setex("wordbyday_"+word, datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data["data"] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data)
        conDatabase.close()

class GetWordByDayAndAuthor():
    def __init__(self, days=365):
        self.days = days

    def on_get(self, req, resp, word):
        word = uri.decode(word)
        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        data = {"status": "success", "data": {}}

        redisCache = r.get("wordbydayandauthor_"+word)

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                res = conDatabase.execute("SELECT COUNT(word_id), "+prefix+"files_keywords.date, "+prefix+"authors.author FROM "+prefix+"files_keywords INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords.word_id = "+prefix+"keywords.id) INNER JOIN "+prefix+"files ON ("+prefix+"files_keywords.file_id = "+prefix+"files.id) INNER JOIN "+prefix+"authors_files ON ("+prefix+"files.id = "+prefix+"authors_files.file_id) INNER JOIN "+prefix+"authors ON ("+prefix+"authors_files.author_id = "+prefix+"authors.id) WHERE "+prefix+"files_keywords.date > '"+critical_date.strftime("%Y-%m-%d")+"' AND "+prefix+"keywords.word LIKE '"+sqlescape(word)+"%' GROUP BY "+prefix+"files_keywords.date, "+prefix+"authors.author ORDER BY "+prefix+"files_keywords.date")
                res2 = conDatabase.execute("SELECT COUNT(word_id), "+prefix+"files_keywords_content.date, "+prefix+"authors.author FROM "+prefix+"files_keywords_content INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords_content.word_id = "+prefix+"keywords.id) INNER JOIN "+prefix+"files ON ("+prefix+"files_keywords_content.file_id = "+prefix+"files.id) INNER JOIN "+prefix+"authors_files ON ("+prefix+"files.id = "+prefix+"authors_files.file_id) INNER JOIN "+prefix+"authors ON ("+prefix+"authors_files.author_id = "+prefix+"authors.id) WHERE "+prefix+"files_keywords_content.date > '"+critical_date.strftime("%Y-%m-%d")+"' AND "+prefix+"keywords.word LIKE '"+sqlescape(word)+"%' GROUP BY "+prefix+"files_keywords_content.date, "+prefix+"authors.author ORDER BY "+prefix+"files_keywords_content.date")
                
                for entry in res:

                    if entry['author'] in word_list:
                        word_list[entry['author']].update({entry['date'].strftime("%Y-%m-%d") : entry['COUNT(word_id)']})

                    else:
                        word_list[entry['author']] = {entry['date'].strftime("%Y-%m-%d") : entry['COUNT(word_id)']}

                for entry in res2:
                    if entry['author'] in word_list:
                        if entry['date'].strftime("%Y-%m-%d") in word_list[entry['author']]:
                            word_list[entry['author']][entry['date'].strftime("%Y-%m-%d")] += entry['COUNT(word_id)']
                        else: 
                            word_list[entry['author']].update({entry['date'].strftime("%Y-%m-%d") : entry['COUNT(word_id)']})

                    else:
                        word_list[entry['author']] = {entry['date'].strftime("%Y-%m-%d") : entry['COUNT(word_id)']}

           
                data['data'] = word_list


                r.setex("wordbydayandauthor_"+word, datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data["data"] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data)
        conDatabase.close()

class GetWordByMonth():
    def __init__(self, days=183):
        self.days = days

    def on_get(self, req, resp, word):
        word = uri.decode(word)
        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        data = {"status": "success", "data": {}}

        redisCache = r.get("wordbymonth_"+word)

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                res = conDatabase.execute("SELECT COUNT(word_id), DATE_FORMAT("+prefix+"files_keywords.date, '%m.%Y') AS date FROM "+prefix+"files_keywords INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords.word_id = "+prefix+"keywords.id) WHERE "+prefix+"files_keywords.date > '"+critical_date.strftime("%Y-%m-%d")+"' AND "+prefix+"keywords.word LIKE '"+sqlescape(word)+"%' GROUP BY DATE_FORMAT("+prefix+"files_keywords.date, '%m.%Y') ORDER BY DATE_FORMAT("+prefix+"files_keywords.date, '%m.%Y')")
                res2 = conDatabase.execute("SELECT COUNT(word_id), DATE_FORMAT("+prefix+"files_keywords_content.date, '%m.%Y') AS date FROM "+prefix+"files_keywords_content INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords_content.word_id = "+prefix+"keywords.id) WHERE "+prefix+"files_keywords_content.date > '"+critical_date.strftime("%Y-%m-%d")+"' AND "+prefix+"keywords.word LIKE '"+sqlescape(word)+"%' GROUP BY DATE_FORMAT("+prefix+"files_keywords_content.date, '%m.%Y') ORDER BY DATE_FORMAT("+prefix+"files_keywords_content.date, '%m.%Y')")
                

                for entry in res:

                    word_list[entry['date']] = entry['COUNT(word_id)']

                for entry in res2:
                    if (entry['date'] in word_list):
                        word_list[entry['date']] += entry['COUNT(word_id)']
                    else: 
                        word_list[entry['date']] = entry['COUNT(word_id)']
           
                data['data'] = word_list


                r.setex("wordbymonth_"+word, datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data["data"] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data) 
        conDatabase.close()

class GetWordByMonthAndAuthor():
    def __init__(self, days=183):
        self.days = days

    def on_get(self, req, resp, word):
        word = uri.decode(word)
        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        data = {"status": "success", "data": {}}

        redisCache = r.get("wordbymonthandauthor_"+word)

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                res = conDatabase.execute("SELECT COUNT(word_id), DATE_FORMAT("+prefix+"files_keywords.date, '%m.%Y') AS date, "+prefix+"authors.author AS author FROM "+prefix+"files_keywords INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords.word_id = "+prefix+"keywords.id) INNER JOIN "+prefix+"files ON ("+prefix+"files_keywords.file_id = "+prefix+"files.id) INNER JOIN "+prefix+"authors_files ON ("+prefix+"files.id = "+prefix+"authors_files.file_id) INNER JOIN "+prefix+"authors ON ("+prefix+"authors_files.author_id = "+prefix+"authors.id) WHERE "+prefix+"files_keywords.date > '"+critical_date.strftime("%Y-%m-%d")+"' AND "+prefix+"keywords.word LIKE '"+sqlescape(word)+"%' GROUP BY DATE_FORMAT("+prefix+"files_keywords.date, '%m.%Y'), "+prefix+"authors.author ORDER BY DATE_FORMAT("+prefix+"files_keywords.date, '%m.%Y')")
                res2 = conDatabase.execute("SELECT COUNT(word_id), DATE_FORMAT("+prefix+"files_keywords_content.date, '%m.%Y') AS date, "+prefix+"authors.author AS author FROM "+prefix+"files_keywords_content INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords_content.word_id = "+prefix+"keywords.id) INNER JOIN "+prefix+"files ON ("+prefix+"files_keywords_content.file_id = "+prefix+"files.id) INNER JOIN "+prefix+"authors_files ON ("+prefix+"files.id = "+prefix+"authors_files.file_id) INNER JOIN "+prefix+"authors ON ("+prefix+"authors_files.author_id = "+prefix+"authors.id) WHERE "+prefix+"files_keywords_content.date > '"+critical_date.strftime("%Y-%m-%d")+"' AND "+prefix+"keywords.word LIKE '"+sqlescape(word)+"%' GROUP BY DATE_FORMAT("+prefix+"files_keywords_content.date, '%m.%Y'), "+prefix+"authors.author ORDER BY DATE_FORMAT("+prefix+"files_keywords_content.date, '%m.%Y')")
                

                for entry in res:

                    if entry['author'] in word_list:
                        word_list[entry['author']].update({entry['date'] : entry['COUNT(word_id)']})

                    else:
                        word_list[entry['author']] = {entry['date'] : entry['COUNT(word_id)']}

                for entry in res2:
                    if entry['author'] in word_list:
                        if entry['date'] in word_list[entry['author']]:
                            word_list[entry['author']][entry['date']] += entry['COUNT(word_id)']
                        else: 
                            word_list[entry['author']].update({entry['date'] : entry['COUNT(word_id)']})

                    else:
                        word_list[entry['author']] = {entry['date'] : entry['COUNT(word_id)']}

                data['data'] = word_list


                r.setex("wordbymonthandauthor_"+word, datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data["data"] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data) 
        conDatabase.close()

class GetFilesByMonth():
    def __init__(self, days=183):
        self.days = days    

    def on_get(self, req, resp):
        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        data = {"status": "success", "data": {}}

        redisCache = r.get("filesbymonth")

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                res = conDatabase.execute("SELECT COUNT(id), DATE_FORMAT(date, '%m.%Y') AS date FROM "+prefix+"files WHERE "+prefix+"files.date > '"+critical_date.strftime("%Y-%m-%d")+"' GROUP BY DATE_FORMAT("+prefix+"files.date, '%m.%Y') ORDER BY DATE_FORMAT("+prefix+"files.date, '%m.%Y')")
                
                for entry in res:

                    word_list[str(entry['date'])] = entry['COUNT(id)']
           
                data['data'] = word_list


                r.setex("filesbymonth", datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data["data"] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data) 
        conDatabase.close()

class GetSearchFiles():
    def __init__(self, days=183):
        self.days = days    

    def on_get(self, req, resp):
        data = {"status": "failure", "data": {}}

        try:
            searchstring = sqlescape(req.params['searchstring'])  
            data = {"status": "success", "data": {}}      
        except:
            searchstring = False
            logger.info("No search string delivered")
        try:
            filenumber = sqlescape(req.params['filenumber'])
            data = {"status": "success", "data": {}}     
            if len(filenumber) < 1:
                filenumber = False 
        except:
            filenumber = False
            logger.info("No filenumber delivered")
        try:
            author = sqlescape(req.params['author'])     
            data = {"status": "success", "data": {}}   
            if len(author) < 1:
                author = False  
        except:
            author = False
            logger.info("No author delivered")
        try:
            type_ = sqlescape(req.params['type'])     
            data = {"status": "success", "data": {}}  
            if len(type_) < 1:
                type_ = False    
        except:
            type_ = False
            logger.info("No type delivered")
        try:
            date_begin_ = req.params['date_begin']   
            date_begin = datetime.datetime.strptime(date_begin_, "%Y-%m-%d")  
            data = {"status": "success", "data": {}}   
            if len(date_begin) < 1:
                date_begin = False 
        except:
            date_begin = False
            date_begin_ = False
            logger.info("No date delivered")
        try:
            date_end_ = req.params['date_end']   
            date_end = datetime.datetime.strptime(date_end_, "%Y-%m-%d")    
            data = {"status": "success", "data": {}}    
            if len(date_end) < 1:
                date_end = False  
        except:
            date_end = False
            date_end_ = False
            logger.info("No date delivered")

        

        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

        redisCache = r.get("searchfiles_searchstring-"+str(searchstring)+"_filenumber-"+str(filenumber)+"_type-"+str(type_)+"_datebegin-"+str(date_begin_)+"_dateend"+str(date_end_)+"_author"+str(author).replace(" ", ""))

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                
                query = "SELECT "+prefix+"files.number AS number, DATE_FORMAT(any_value("+prefix+"files.date), '%d-%m-%Y') AS date, any_value("+prefix+"files.link) AS link, any_value("+prefix+"files.title) AS title, any_value("+prefix+"files.type) AS type, GROUP_CONCAT(DISTINCT "+prefix+"authors.author) AS author FROM "+prefix+"files INNER JOIN "+prefix+"authors_files ON ("+prefix+"files.id = "+prefix+"authors_files.file_id) INNER JOIN "+prefix+"authors ON ("+prefix+"authors_files.author_id = "+prefix+"authors.id) WHERE "+prefix+"files.id > 0 "
                
                if (searchstring != False):
                    query += " AND "+prefix+"files.title LIKE '%"+str(searchstring)+"%' " 
                
                if (filenumber != False):
                    query += "AND "+prefix+"files.number LIKE '%"+str(filenumber)+"%' "

                if (type_ != False):
                    query += "AND "+prefix+"files.type LIKE '%"+str(type_)+"%' "

                if (author != False):
                    query += "AND "+prefix+"authors.author LIKE '%"+str(author)+"%' "

                if (date_begin != False and date_begin > critical_date):
                    query += "AND "+prefix+"files.date >= '"+date_begin.strftime("%Y-%m-%d")+"' "
                else:
                    "AND "+prefix+"files.date > '"+critical_date.strftime("%Y-%m-%d")+"' "

                if (date_end != False and date_end > critical_date):
                    query += "AND "+prefix+"files.date <= '"+date_end.strftime("%Y-%m-%d")+"' "
                
                query += "GROUP BY "+prefix+"files.number ORDER BY DATE_FORMAT(any_value(date), '%d-%m-%Y') DESC LIMIT 500"

                res = conDatabase.execute(query)
           
                data['data'] = res


                r.setex("searchfiles_searchstring-"+str(searchstring)+"_filenumber-"+str(filenumber)+"_type-"+str(type_)+"_datebegin-"+str(date_begin_)+"_dateend"+str(date_end_)+"_author"+str(author).replace(" ", ""), datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data['data'] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data) 
        conDatabase.close()

class GetSearchFilesExperimental():
    def __init__(self, days=183):
        self.days = days    

    def on_get(self, req, resp):
        data = {"status": "failure", "data": {}}

        try:
            searchstring = sqlescape(req.params['searchstring'])  
            data = {"status": "success", "data": {}}      
        except:
            searchstring = False
            logger.info("No search string delivered")
        try:
            filenumber = sqlescape(req.params['filenumber'])
            data = {"status": "success", "data": {}}     
            if len(filenumber) < 1:
                filenumber = False 
        except:
            filenumber = False
            logger.info("No filenumber delivered")
        try:
            author = sqlescape(req.params['author'])     
            data = {"status": "success", "data": {}}   
            if len(author) < 1:
                author = False  
        except:
            author = False
            logger.info("No author delivered")
        try:
            type_ = sqlescape(req.params['type'])     
            data = {"status": "success", "data": {}}  
            if len(type_) < 1:
                type_ = False    
        except:
            type_ = False
            logger.info("No type delivered")
        try:
            date_begin_ = req.params['date_begin']   
            date_begin = datetime.datetime.strptime(date_begin_, "%Y-%m-%d")  
            data = {"status": "success", "data": {}}   
            if len(date_begin) < 1:
                date_begin = False 
        except:
            date_begin = False
            date_begin_ = False
            logger.info("No date delivered")
        try:
            date_end_ = req.params['date_end']   
            date_end = datetime.datetime.strptime(date_end_, "%Y-%m-%d")    
            data = {"status": "success", "data": {}}    
            if len(date_end) < 1:
                date_end = False  
        except:
            date_end = False
            date_end_ = False
            logger.info("No date delivered")

        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

        

        redisCache = r.get("searchfilesexperimental_searchstring-"+str(searchstring)+"_filenumber-"+str(filenumber)+"_type-"+str(type_)+"_datebegin-"+str(date_begin_)+"_dateend"+str(date_end_)+"_author"+str(author).replace(" ", ""))

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                
                query = "SELECT any_value("+prefix+"files.number) AS number, DATE_FORMAT(any_value("+prefix+"files.date), '%d-%m-%Y') AS date, any_value("+prefix+"files.link) AS link, any_value("+prefix+"files.title) AS title, any_value("+prefix+"files.type) AS type, GROUP_CONCAT(DISTINCT "+prefix+"authors.author) AS author FROM "+prefix+"files INNER JOIN "+prefix+"authors_files ON ("+prefix+"files.id = "+prefix+"authors_files.file_id) INNER JOIN "+prefix+"authors ON ("+prefix+"authors_files.author_id = "+prefix+"authors.id) INNER JOIN "+prefix+"files_keywords_content ON ("+prefix+"files.id = "+prefix+"files_keywords_content.file_id) INNER JOIN "+prefix+"keywords ON ("+prefix+"files_keywords_content.word_id = "+prefix+"keywords.id) WHERE "+prefix+"files.id > 0 "
                
                if (searchstring != False):
                    query += " AND ("+prefix+"files.title LIKE '%"+str(searchstring)+"%' OR "+prefix+"keywords.word LIKE '"+str(searchstring)+"%')  " 
                
                if (filenumber != False):
                    query += "AND "+prefix+"files.number LIKE '%"+str(filenumber)+"%' "

                if (type_ != False):
                    query += "AND "+prefix+"files.type LIKE '%"+str(type_)+"%' "

                if (author != False):
                    query += "AND "+prefix+"authors.author LIKE '%"+str(author)+"%' "

                if (date_begin != False and date_begin > critical_date):
                    query += "AND "+prefix+"files.date >= '"+date_begin.strftime("%Y-%m-%d")+"' "
                else:
                    "AND "+prefix+"files.date > '"+critical_date.strftime("%Y-%m-%d")+"' "

                if (date_end != False and date_end > critical_date):
                    query += "AND "+prefix+"files.date <= '"+date_end.strftime("%Y-%m-%d")+"' "
                
                query += "GROUP BY "+prefix+"files.number ORDER BY any_value("+prefix+"files.date) DESC LIMIT 500"

                res = conDatabase.execute(query)
           
                data['data'] = res


                r.setex("searchfilesexperimental_searchstring-"+str(searchstring)+"_filenumber-"+str(filenumber)+"_type-"+str(type_)+"_datebegin-"+str(date_begin_)+"_dateend"+str(date_end_)+"_author"+str(author).replace(" ", ""), datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data['data'] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data) 
        conDatabase.close()

class GetAuthors():
    def __init__(self, days=183):
        self.days = days    

    def on_get(self, req, resp):
        data = {"status": "success", "data": {}}

        word_list = {}
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

        redisCache = r.get("authors")

        if redisCache == None:
            if conDatabase.connect():
                critical_date = datetime.datetime.now()-datetime.timedelta(days=self.days)
                
                query = "SELECT "+prefix+"authors.author AS author FROM "+prefix+"authors"
            
                res = conDatabase.execute(query)
           
                data['data'] = res


                r.setex("authors", datetime.timedelta(minutes=int(caching_minutes), hours=int(caching_hours)), json.dumps(data['data']))
            else:
                data = {"status": "failure", "data": {"error_code": 1}}
                logger.error("No database connection available. #1")
                


        else: 
            data['data'] = json.loads(redisCache.decode('utf-8'))
        resp.body = json.dumps(data) 
        conDatabase.close()


api = falcon.API()
api.req_options.auto_parse_form_urlencoded=True
api.add_route('/wordclouds', GetWordClouds(days=183))
api.add_route('/wordcloud', GetWordCloud(days=183))
api.add_route('/wordbyday/{word}', GetWordByDay(days=365))
api.add_route('/wordbydayandauthor/{word}', GetWordByDayAndAuthor(days=365))
api.add_route('/wordbymonth/{word}', GetWordByMonth(days=1825))
api.add_route('/wordbymonthandauthor/{word}', GetWordByMonthAndAuthor(days=1825))
api.add_route('/filesbymonth', GetFilesByMonth(days=1825))
api.add_route('/searchfiles', GetSearchFiles(days=1825))
api.add_route('/searchfilesexperimental', GetSearchFilesExperimental(days=1825))
api.add_route('/authors', GetAuthors(days=18250))


#debugging
#run = GetWordByDay()
#print(run.on_get("", "", "berichten"))

