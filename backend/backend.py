# python 3.7.3
from pony import orm
from models.models import db
from includes import logger
from scraper import Scraper
from tagger import Tagger
import configparser, time
import threading
from random import randint

log = logger.Logger("debug")


class Runner:
    def __init__(self, tagger=False, scraper=False):
        if not self._load_config():
            return
        if not self._prepare_database():
            return

        if scraper:
            sc = Scraper(self.config['parlis']['url'])
            sc.run()
        if tagger:
            ta = Tagger()
            ta.run()

    def _prepare_database(self):
        log.debug("Setting up database")
        if self.config['settings']['debug'] == 1:
            orm.set_sql_debug(True)

        try:
            db.bind(provider='mysql',
                    user=self.config['database']['user'],
                    password=self.config['database']['password'],
                    host=self.config['database']['host'],
                    database=self.config['database']['database'])

            db.generate_mapping(create_tables=True)
        except Exception as e:
            log.error(f"Error while setting up database: {e}")
            return False
        return True

    def _load_config(self):
        reader = configparser.ConfigParser()
        reader.read_file(open('config.ini'))
        log.debug("Reading config")

        required_config = {
            'database': [
                'host',
                'database',
                'user',
                'password',
                'prefix'
            ],
            'parlis': [
                'url'
            ],
            'settings': [
                'debug'
            ]
        }

        self.config = {}

        for topic, settings in required_config.items():
            if topic not in self.config.keys():
                self.config[topic] = {}
            for setting in settings:
                try:
                    self.config[topic][setting] = reader.get(topic, setting)
                except:
                    log.error(f"Missing key {setting} in {topic}")
                    return False
        log.debug("Finished reading config")
        return True


class Timer:

    def start(self, scraper=True, tagger=True):
        if tagger:
            threading.Thread(target=self.tagger).start()
        if scraper:
            threading.Thread(target=self.scraper).start()

        log.error("Threading stopped. Exiting.")

    def tagger(self):
        log.info("Tagger started.")
        while True:
            Runner(True, False)
            time.sleep(10*60)
        log.error("Tagger exited.")

    def scraper(self):
        log.info("Scraper started.")
        while True:
            Runner(False, True)
            time.sleep(8+60*60 + randint(0, 240))
        log.error("Scraper exited")


if __name__ == '__main__':
    t = Timer()
    t.start(True, True)
