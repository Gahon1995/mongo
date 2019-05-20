from mongoengine import *

from config import DBMS
from model.user import User


class BjUser(User):
    meta = {
        'db_alias': DBMS.DBMS1,
        'collection': 'user'
    }
