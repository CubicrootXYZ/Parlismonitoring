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
    def __init__(self, config, tagger=False, scraper=False, prepare_db=False):
        self.config = config
        if prepare_db and not self._prepare_database():
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


class Timer:

    def start(self, scraper=True, tagger=True):
        if not self._load_config():
            return

        Runner(self.config, False, False, True) # init the database first, not multithread compatible2

        if tagger:
            threading.Thread(target=self.tagger, args=[self.config]).start()
        if scraper:
            time.sleep(10)
            threading.Thread(target=self.scraper, args=[self.config]).start()

        log.error("Threading stopped. Exiting.")

    def tagger(self, config):
        log.info("Tagger started.")
        while True:
            Runner(config, True, False)
            time.sleep(10*60)
        log.error("Tagger exited.")

    def scraper(self, config):
        log.info("Scraper started.")
        while True:
            Runner(config, False, True)
            time.sleep(8+60*60 + randint(0, 240))
        log.error("Scraper exited")

    def _load_config(self):
        reader = configparser.ConfigParser()
        f = open('config.ini')
        reader.read_file(f)
        f.close()
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


if __name__ == '__main__':
    t = Timer()
    t.start(True, True)
