import requests
from pony.orm import *
from includes import logger
from error import resource_error
from models import File, Scrape, db, FileKeywordContent, FileKeyword, Keyword
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

log = logger.Logger("debug")


class Scraper:
    def __init__(self, url):
        log.debug("Setting up Scraper")
        self.url = url
        self.offset = 0

    def run(self, files=0):
        if self.offset > 150:
            with db_session:
                this_scrape = Scrape.select(status="started").order_by(desc(Scrape.start)).first()
                if this_scrape is not None:
                    this_scrape.status = "finished"
                    this_scrape.end = datetime.now()
                    this_scrape.processed_files = files
                log.info("To far back in time. Stopping.")
            return

        try:
            page = self.get_page()
        except resource_error.ResourceError as e:
            log.error(e)
            return

        with db_session:
            try:
                last_scrape = Scrape.select(status="finished").order_by(desc(Scrape.start)).first
                runtil_date = last_scrape.end - timedelta(days=1)
            except:
                last_scrape = None
                runtil_date = datetime.now() - timedelta(days=30)

            if self.offset is 0:
                this_scrape = Scrape(start=datetime.now(), status="started")

        for entry in page.split('<hr class="col-xs-12 divider divider-small">'):
            log.debug(f"Next file ({files}) ...")
            try:
                with db_session:
                    soup = BeautifulSoup(entry, 'html.parser')
                    title = soup.a.get_text()

                    if len(title) > 160:
                        short_title = title[:157] + "..."
                    else:
                        short_title = title

                    # end of page or invalid title
                    if "Weitere Dokumente anzeigen" in title or len(title) < 5:
                        log.debug("EOF or title invalid. Skipping.")
                        continue

                    try:
                        info = soup.find_all('li')
                        publish_date = datetime.strptime(info[1].getText().replace("Datum: ", "", 1), "%d.%m.%Y")
                        number = info[0].getText()
                        type = info[2].getText().replace("Art: ", "", 1)
                        author = info[3].getText().replace("Urheber: ", "", 1)
                        link = 'https://www.landtag-bw.de'+soup.a.get('href') # TODO move base url to config
                        insert_date = datetime.now()
                    except Exception as e:
                        log.info(f"Could not parse file. Skipping. {e}")
                        continue

                    if publish_date < runtil_date:
                        log.info("Reach end of last scrape, finished.")
                        this_scrape = Scrape.select(status="started").order_by(desc(Scrape.start)).first()
                        if this_scrape is not None:
                            this_scrape.status = "finished"
                            this_scrape.end = datetime.now()
                            this_scrape.processed_files = files
                            this_scrape.flush()
                        return

                    # check if file already exists
                    file_ = File.select(title=title, number=number).first()
                    if file_ is not None:
                        # TODO update file in database
                        log.info(f"Already having file \"{title}\" in database. Skipping.")
                        continue

                    file = File(title=title, title_short=short_title, number=number, publish_date=publish_date,
                                type=type, author=author, insert_date=insert_date,
                                link=link)
                    files += 1
            except Exception as e:
                log.error(f"Fatal error, file might not be saved: {e}")

        log.debug("EOF. Getting next page.")
        self.offset += 30
        self.run(files=files)

    def get_page(self):
        log.debug("Getting page")
        try:
            res = requests.get(self.url + str(self.offset)).text
            return res
        except Exception as e:
            log.debug(f"Can not get page: {e}")
            raise resource_error.ResourceError(f"Can not fetch {self.url}")
