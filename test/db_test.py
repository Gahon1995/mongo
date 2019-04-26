import json
from mongoengine import connect
from model.User import User
from model.Article import Article

connect('test', host='192.168.109.128', port=27017)


# data = '{"timestamp": "1506328859000", "uid": "2", "name": "user2", "gender": "male", "email": "email0", "phone": "phone0", "dept": "dept17", "grade": "grade4", "language": "zh", "region": "Beijing", "role": "role1", "preferTags": "tags39", "obtainedCredits": "79"}'
#
# # user = User().from_json(data)
# # user.save()
#
# User.insert(data)

# User.delete_by()

# for u in User.find():
#     print(u.name)

arti = {"timestamp": "1506000000000", "aid": "0", "title": "title0", "category": "technology", "abstract": "abstract of article 0", "articleTags": "tags33", "authors": "author376", "language": "zh", "text": "text 0's location on hdfs", "image": "image 0's location on hdfs", "video": "video 0's location on hdfs"}

Article.insert(json.dumps(arti))

for a in Article.find_all():
    print(a)