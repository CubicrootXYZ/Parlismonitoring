import os
import collections
import time
from pony.orm import *
from includes import logger, rnntagger, parser
from error import resource_error
from models import File, Scrape, db, FileKeywordContent, FileKeyword, Keyword, Tag
from datetime import datetime, timedelta

log = logger.Logger("debug")


class Tagger:

    def __init__(self):
        with db_session:
            last_tag = Tag.select(status="started").order_by(
                desc(Tag.start)).first()
            if last_tag is not None and last_tag.start > (datetime.now() - timedelta(days=2)):
                log.info("Tagger already running - skipping.")
                return

            tag_ = Tag(start=datetime.now(), status="started")
        if self.run():
            with db_session:
                tag = Tag.select(status="started").order_by(
                    desc(Tag.start)).first()
                if tag is not None:
                    tag.end = datetime.now()
                    tag.status = "finished"

    @db_session
    def run(self, i=1):
        log.info("Starting tag process.")
        files = File.select(title_word_count=None,
                            word_count=None).order_by(File.publish_date)
        rnn = rnntagger.RnnTagger("german")

        log.debug(f"Found {len(files)} files to tag.")
        for file in files:
            log.debug(f"Tagging file {i}")
            file_start = time.time()

            link = file.link

            if file.insert_date < datetime.now() - timedelta(days=365):
                continue

            if not link.startswith('http://') and not link.startswith('https://'):
                log.info(f"Invalid link given. Skipping. {link}")
                continue

            try:
                p = parser.Parser(link)
                text = p.get_text()
                size = int(p.get_size())
                pages = int(p.get_pages())
            except Exception as e:
                log.info(e)
                continue

            log.debug(f"Size: {size}")

            # roughly 40 seconds
            keywords_content = []
            try:
                log.info(f"Start tagging in {len(text) +1} steps.")
                for t in text:
                    keywords_content += rnn.tag(t)
                    log.debug("Next step.")
                keywords_title = rnn.tag(file.title)
            except rnntagger.TaggerError as e:
                log.info(f"Skipping. Tagging failed with: {e}")
                continue

            log.debug("Sorting keywords")
            keywords_content_sorted = self.sort(keywords_content)
            keywords_title_sorted = self.sort(keywords_title)

            log.debug(
                f"Found {len(keywords_content)} words. Start inserting them.")
            tot_words = 0
            for word, tags in keywords_content_sorted.items():
                for tag, word_count in tags.items():
                    k_id = self._get_keyword_id(word, tag)
                    if k_id is -1:
                        continue
                    FileKeywordContent(
                        file_id=file.id, keyword_id=k_id, word_count=word_count)
                    tot_words += word_count

            tot_title = 0
            log.debug(
                f"Found {len(keywords_title)} words. Start inserting them.")
            for word, tags in keywords_title_sorted.items():
                for tag, word_count in tags.items():

                    k_id = self._get_keyword_id(word, tag)
                    if k_id is -1:
                        continue
                    f = FileKeyword(file_id=file.id,
                                    keyword_id=k_id, word_count=word_count)
                    tot_title += word_count

            file.file_size = size
            file.word_count = tot_words
            file.title_word_count = tot_title
            file.pages = pages
            file.commit()
            log.debug(f"File DUR: {time.time()-file_start}")
            i += 1

            if i == 5:
                log.debug("Flushing session to avoid data loss.")
                self.run(i)

        log.info("Finished tagging. Nothing left to do.")
        return True

    def _get_type(self, tag):
        type = "unknown"

        if tag.startswith('NN'):
            type = "noun"
        elif tag.startswith('ART'):
            type = 'article'
        elif tag.startswith("$"):
            type = "punctuation"
        elif tag.startswith("ADJ"):
            type = "adjective"
        elif tag.startswith("NE"):
            type = "proper name"
        elif tag.startswith("V"):
            type = "verb"

        return type

    def _get_keyword_id(self, word, type_):
        keyword = Keyword.select(word=word, type=type_).first()

        if keyword is None:
            try:
                keyword = Keyword(created=datetime.now(), word=word, type=type_)
                keyword.flush()
            except Exception as e:
                print(f"Failed to insert keyword {keyword} with error: {e}")
                return -1

        return keyword.id

    def sort(self, sentences):
        ret = {}

        for sentence in sentences:
            for word in sentence:
                if "root" not in word:
                    continue

                word['root'] = word['root'].split("<")[0].split(
                    "(")[0].split(">")[0]  # clean word

                if len(word['root']) < 1 or word['root'] is None or (len(word['root']) > 1 and word['root'][0] in ["(", "/", ")", "{", "}", "<", ">"]) or len(word['root']) > 100:
                    continue
                type_ = self._get_type(word['tag'])
                if word['root'] in ret:
                    if type_ in ret[word['root']]:
                        ret[word['root']][type_] += 1
                    else:
                        ret[word['root']][type_] = 1
                else:
                    ret[word['root']] = {}
                    ret[word['root']][type_] = 1
        return ret
