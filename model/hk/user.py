from mongoengine import *

from config import DBMS
from model.user import User


class HkUser(User):
    meta = {
        'db_alias': DBMS.DBMS2,
        'collection': 'user'
    }
