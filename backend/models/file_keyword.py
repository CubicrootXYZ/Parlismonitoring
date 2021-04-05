from pony import orm
from pony.orm import *
from .models import db
from .file import File
from .keyword import Keyword


class FileKeywordContent(db.Entity):
    file_id = Required(int)
    keyword_id = Required(int)
    word_count = Required(int, sql_default=0)


class FileKeyword(db.Entity):
    file_id = Required(int)
    keyword_id = Required(int)
    word_count = Required(int, sql_default=0)