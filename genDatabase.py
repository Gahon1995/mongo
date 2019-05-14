from random import random
from service.user_service import UserService
from service.article_service import ArticleService
from service.read_service import ReadService

from utils.consts import Region, Gender, Category, DBMS

# USERS_NUM = 10000
# ARTICLES_NUM = 200000
# READS_NUM = 1000000

USERS_NUM = 100
ARTICLES_NUM = 200
READS_NUM = 1000

uid_region = {}
aid_lang = {}


# Beijing:60%   Hong Kong:40%
# en:20%    zh:80%
# 20 depts
# 3 roles
# 50 tags
# 0~99 credits

def gen_an_user(i):
    timeBegin = 1506328859000
    user = {}
    user["timestamp"] = str(timeBegin + i)
    user["uid"] = str(i)
    user["name"] = "user%d" % i if i != 0 else "admin"
    user["pwd"] = "password" if i != 0 else "admin"
    user["gender"] = Gender.male if random() > 0.33 else Gender.female
    user["email"] = "email%d" % i
    user["phone"] = "phone%d" % i
    user["dept"] = "dept%d" % int(random() * 20)
    user["grade"] = "grade%d" % int(random() * 4 + 1)
    user["language"] = "en" if random() > 0.8 else "zh"
    user["region"] = Region.bj if random() > 0.4 else Region.hk
    user["role"] = "role%d" % int(random() * 3)
    user["preferTags"] = "tags%d" % int(random() * 50)
    user["obtainedCredits"] = str(int(random() * 100))

    uid_region[user["uid"]] = user["region"]
    return user


# science:45%   technology:55%
# en:50%    zh:50%
# 50 tags
# 2000 authors
def gen_an_article(i):
    timeBegin = 1506000000000
    article = {}
    article["timestamp"] = str(timeBegin + i)
    article["aid"] = str(i)
    article["title"] = "title%d" % i
    article["category"] = Category.science if random() > 0.55 else Category.technology
    article["abstract"] = "abstract of article %d" % i
    article["articleTags"] = "tags%d" % int(random() * 50)
    article["authors"] = "author%d" % int(random() * 2000)
    article["language"] = "en" if random() > 0.5 else "zh"
    article["text"] = "text %d's location on hdfs" % i
    article["image"] = "image %d's location on hdfs" % i
    article["video"] = "video %d's location on hdfs" % i

    aid_lang[article["aid"]] = article["language"]
    return article


# user in Beijing read/agree/comment/share an english article with the probability 0.6/0.2/0.2/0.1
# user in Hong Kong read/agree/comment/share an Chinese article with the probability 0.8/0.2/0.2/0.1
p = {}
p["Beijing" + "en"] = [0.6, 0.2, 0.2, 0.1]
p["Beijing" + "zh"] = [1, 0.3, 0.3, 0.2]
p["Hong Kong" + "en"] = [1, 0.3, 0.3, 0.2]
p["Hong Kong" + "zh"] = [0.8, 0.2, 0.2, 0.1]


def gen_an_read(i):
    timeBegin = 1506332297000
    read = {}
    read["timestamp"] = str(timeBegin + i * 10000)
    read["uid"] = str(int(random() * USERS_NUM))
    read["aid"] = str(int(random() * ARTICLES_NUM))

    region = uid_region[read["uid"]]
    lang = aid_lang[read["aid"]]
    ps = p[region + lang]

    if (random() > ps[0]):
        # read["readOrNot"] = "0";
        return gen_an_read(i)
    else:
        read["readOrNot"] = "1"
        read["readTimeLength"] = str(int(random() * 100))
        read["readSequence"] = str(int(random() * 4))
        read["agreeOrNot"] = "1" if random() < ps[1] else "0"
        read["commentOrNot"] = "1" if random() < ps[2] else "0"
        read["shareOrNot"] = "1" if random() < ps[3] else "0"
        read["commentDetail"] = "comments to this article: (" + read["uid"] + "," + read["aid"] + ")"
    return read


def print_bar(now, total):
    print('\rprocess:\t {now} / {total}  {rate}%'.format(now=now + 1, total=total,
                                                         rate=round((now + 1) / total * 100, 2)), end='')
    if now == total:
        print()


def gen_users():
    from model.user import User
    User.delete_by()
    for i in range(USERS_NUM):
        # print_bar(i, USERS_NUM)
        data = gen_an_user(i)
        if data['region'] == Region.bj:
            db_alias = DBMS.DBMS1
        else:
            db_alias = DBMS.DBMS2
        UserService.register(data['name'], data['pwd'], data['gender'], data['email'], data['phone'], data['dept'],
                             data['grade'], data['language'], data['region'], data['role'], data['preferTags'],
                             int(data['obtainedCredits']), db_alias=db_alias)


def gen_articles():
    from model.article import Article
    Article.delete_by()
    for i in range(ARTICLES_NUM):
        # print_bar(i, ARTICLES_NUM)
        data = gen_an_article(i)
        ArticleService.add_an_article(title=data['title'], authors=data['authors'], category=data['category'],
                                      abstract=data['abstract'], articleTags=data['articleTags'],
                                      language=data['language'], text=data['text'], image=data['image'],
                                      video=data['video'])


def gen_reads():
    from model.read import Read
    from model.be_read import BeRead
    Read.delete_by()
    BeRead.delete_by()
    for i in range(READS_NUM):
        # print_bar(i, READS_NUM)
        data = gen_an_read(i)

        article = ArticleService.get_an_article(title='title' + data['aid'])

        name = 'user' + data['uid'] if data['uid'] != '0' else 'admin'
        user = UserService.get_user_by_name(name=name)

        db_alias = DBMS.DBMS1 if user.region == Region.bj else DBMS.DBMS2

        new_read = Read()
        new_read.aid = article
        new_read.uid = user
        new_read.readOrNot = int(data['readOrNot'])
        new_read.readTimeLength = int(data['readTimeLength'])
        new_read.readSequence = int(data['readSequence'])
        new_read.commentOrNot = int(data['commentOrNot'])
        new_read.commentDetail = data['commentDetail']
        new_read.agreeOrNot = int(data['agreeOrNot'])
        new_read.shareOrNot = int(data['shareOrNot'])
        ReadService.save_read(new_read)
        del new_read


def main():
    # from mongoengine import connect
    # host = '127.0.0.1'
    # connect('mongo-new', host=host, port=27017)
    from main import init
    init()

    print('\n导入user数据...')
    gen_users()

    print('\n导入article数据...')
    gen_articles()

    print('\n导入read数据...')
    gen_reads()


if __name__ == '__main__':
    main()
