from pony import orm
from pony.orm import *
from .models import db
from datetime import datetime


class Keyword(db.Entity):
    created = Required(datetime)
    word = Required(str)
    type = Optional(str)
    comment = Optional(str)
