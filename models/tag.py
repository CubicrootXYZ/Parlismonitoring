from pony import orm
from pony.orm import *
from .models import db
from datetime import datetime


class Tag(db.Entity):
    STATUS_START = "started"
    STATUS_FINISHED = "finished"
    STATUS_ERROR = "failed"

    id = PrimaryKey(int, auto=True)
    start = Required(datetime)
    end = Optional(datetime)
    status = Required(str)
    processed_files = Optional(int)
