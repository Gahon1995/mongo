from mongoengine import Document


class BaseDB(Document):
    meta = {
        'abstract': True,
    }

    def __str__(self):
        return self.to_json()

    @classmethod
    def find(cls, **kwargs):
        return cls.objects(**kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        return cls.objects(**kwargs).first()

    @classmethod
    def insert(cls, data):
        return cls.from_json(data).save()

    # @classmethod
    # def update(cls, filters, data):
    #     return cls.objects(filters)

    @classmethod
    def delete(cls, **kwargs):
        return cls.objects(**kwargs).delete()
