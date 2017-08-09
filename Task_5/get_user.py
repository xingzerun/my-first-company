from pymongo import MongoClient
from datetime import datetime
from requests import post

MONGO_URL = 'mongodb://0.0.0.0:27017/'
MONGO_DB = 'chatLog'
MONGO_Collections = 'usercontacts'

# 存储地址
URL = 'http://0.0.0.0/IndexCx/setFriendCounts/'

# Making a Connection with MongoClient
client = MongoClient(MONGO_URL)

# Getting a Database
db = client[MONGO_DB]

# Getting a Collection
collection = db[MONGO_Collections]

# 遍历 chatLog -> usercontacts
for usercontact in collection.find():
    # print(usercontact)
    userPhone = usercontact['userPhone']
    # print('userPhone:%d' % userPhone)

    userContacts = usercontact['userContacts']
    num = len(userContacts)
    # print('userContacts:%d' % num)

    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d')
    # print(strnow)

    d = {
        'mobile':userPhone,
        'da':strnow,
        'num':num,
    }

    r = post(URL, data=d)
    print(userPhone,':',r.content)
