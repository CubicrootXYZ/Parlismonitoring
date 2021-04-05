from pony import orm
from pony.orm import *
from .models import db
from datetime import datetime


class File(db.Entity):
    title = Required(LongStr)
    title_short = Optional(str)
    title_word_count = Optional(int)
    number = Required(str)
    publish_date = Required(datetime)
    type = Required(str)
    author = Required(str)
    file_size = Optional(int, size=64)
    word_count = Optional(int)
    insert_date = Required(datetime)
    link = Required(str)
    pages = Optional(int)
