import configparser, os, datetime, smtplib, ssl
from orator import DatabaseManager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Notifier():
    """class for handling the notifications
    """
    def __init__(self):
        """reads config and sets up database connection
        """
        h,d,u,p = self.readSettings()
        self.connectDb(h, d, u, p)

    def readSettings(self):
        """reads config

        Returns:
            string: hostname
            string: database
            string: user
            string: password
        """
        try:
            config = configparser.ConfigParser()
            config.readfp(open('config.ini'))
            host = config.get('database', 'host')
            database = config.get('database', 'database')
            user = config.get('database', 'user')
            password = config.get('database', 'password')
            self.prefix = config.get('database', 'prefix')
            self.key_t = config.get('search', 'title_keywords')
            self.key_c = config.get('search', 'content_keywords')
            self.laws = config.get("search", 'laws')
            self.days = config.get("search", "intervall_days")
            return host, database, user, password
        except Exception as e:
            print(f"Error while loading config: {e}")
            return False, False, False, False

    def connectDb(self, host, db, user, pwd):
        """establishs the database connection

        Args:
            host (string): database host
            db (string): database name
            user (string): database user
            pwd (string): database password
        """
        config = {
            'mysql': {
                'driver': 'mysql',
                'host': host,
                'database': db,
                'user': user,
                'password': pwd,
                'prefix': ''
            }
        }
        try:
            self.db = DatabaseManager(config)
        except Exception as e:
            print(f"Error while executing {e}")

    def run(self):
        """run this to run the whole notifier

        Returns:
            boolean: False if there was an error
        """
        edge_date = datetime.datetime.now()-datetime.timedelta(days=int(self.days))
        id_t = []
        id_c = []
        id_l = []
        files = []

        #collect keyword ids
        try:
            if len(self.key_c) > 1:
                id_c = self.db.table(self.prefix+"keywords").join(self.prefix+"files_keywords_content", self.prefix+"keywords.id", "=", self.prefix+"files_keywords_content.word_id").where_in("word", self.key_c.split(",")).where(self.prefix+"files_keywords_content.date", ">=", edge_date.strftime("%Y-%m-%d")).lists("file_id")
            if len(self.key_t) > 1:
                id_t = self.db.table(self.prefix+"keywords").join(self.prefix+"files_keywords", self.prefix+"keywords.id", "=", self.prefix+"files_keywords.word_id").where_in("word", self.key_t.split(",")).where(self.prefix+"files_keywords.date", ">=", edge_date.strftime("%Y-%m-%d")).lists("file_id")
            if int(self.laws) is 1:
                id_l = self.db.table(self.prefix+"files").where_in("type", ["Gesetzesbeschluss", "Gesetzentwurf"]).where("time", ">=", edge_date.strftime("%Y-%m-%d 00:00:00")).lists("id")

            file_ids = list(set(list(id_t)+list(id_c)+list(id_l)))

            files = self.db.table(self.prefix+"files").where_in("id", file_ids).get()
        except Exception as e:
            print(f"Error while getting data from database: {e}")
            return False

        self.notify(files)

    def notify(self, files):
        """handles notifcation, you can change this function to other notification providers, it does not need any external ressources than the config file 

        Args:
            files (list): list of dicts of all files to notify
        """
        try:
            config = configparser.ConfigParser()
            config.readfp(open('config.ini'))
            mailto = config.get("mail", "mailto")
            host = config.get("mail", "host")
            user = config.get("mail", "user")
            pwd = config.get("mail", "password")
            port = config.get("mail", "port")
        except Exception as e:
            print(f"Error while reading config: {e}")
            return False

        laws = ""
        misc = ""

        for file in files:
            if file["type"] in ["Gesetzesbeschluss", "Gesetzentwurf"]:
                laws+=f"<a href='{file['link']}'><b>{file['title']}</b></a> ({file['number']}) from {file['date']}<br>"
            else:
                misc+=f"<a href='{file['link']}'><b>{file['title']}</b></a> ({file['number']}, {file['type']}) from {file['date']}<br>"

        text = "New update from PARLISmonitoring for the last "+self.days+" days.<br><br>New laws:<br><br>"+laws+"<br>Miscellaneous<br><br>"+misc

        message = MIMEMultipart("alternative")
        message["Subject"] = "PARLISmonitoring update"
        message["From"] = user
        message["To"] = mailto
        message.attach(MIMEText(text, "html"))

        try:
            c = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=c) as server:
                server.login(user, pwd)
                server.sendmail(
                    user, mailto, message.as_string()
                )
        except Exception as e:
            print(f"Error while sending mail: {e}")
            return False

        return True





n = Notifier()
n.run()

