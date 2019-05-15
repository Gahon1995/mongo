from mongoengine import *
from db.mongodb import BaseDB
from utils.consts import Region


class User(BaseDB):
    meta = {
        'index_background': True,
        'indexes': [
            'uid',
            'name',
        ]
    }
    uid = IntField(required=True, unique=True)
    name = StringField(required=True, unique=True)
    pwd = StringField(required=True)
    gender = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    dept = StringField(required=True)
    grade = StringField(required=True)
    language = StringField(required=True)
    region = StringField(required=True)
    role = StringField(required=True)
    preferTags = StringField(required=True)
    obtainedCredits = IntField(default=0)

    # 尝试利用objectid来获取创建时间
    # timestamp = DateTimeField(default=datetime.now)

    @property
    def create_time(self):
        # 创建时间
        return self.get_create_time()

    @classmethod
    def register(cls, name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                 obtainedCredits: int):
        self = cls()
        self.name = name
        self.pwd = pwd
        self.gender = gender
        self.email = email
        self.phone = phone
        self.dept = dept
        self.grade = grade
        self.language = language
        self.region = region
        self.role = role
        self.preferTags = preferTags
        self.obtainedCredits = obtainedCredits

        _id = User.get_id('uid')

        if region == Region.bj:
            self.uid = _id if _id % 2 == 0 else _id + 1
        elif region == Region.hk:
            self.uid = _id if _id % 2 == 1 else _id + 1

        return self

    def update(self, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
               obtainedCredits: int):
        self.pwd = pwd
        self.gender = gender
        self.email = email
        self.phone = phone
        self.dept = dept
        self.grade = grade
        self.language = language
        self.region = region
        self.role = role
        self.preferTags = preferTags
        self.obtainedCredits = obtainedCredits
        self.save()
