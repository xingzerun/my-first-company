from pymongo import MongoClient
from datetime import datetime
from requests import post
from config import *
import json

# MONGO_URL = 'mongodb://192.168.0.210:27017/'
MONGO_DB = 'chatLog'
MONGO_Collections = 'usercontacts'
# 返回数据接口
Friends_URL = URL + '/IndexCx/setFriendCounts/'

# Making a Connection with MongoClient
client = MongoClient(MONGO_URL)

# Getting a Database
db = client[MONGO_DB]

# Getting a Collection
collection = db[MONGO_Collections]

countCollection = collection.count()
# print(countCollection)
count = 0

# 遍历 chatLog -> usercontacts
for usercontact in collection.find():
    count += 1
    try:
        # print(usercontact)
        userPhone = int(usercontact['userPhone'])
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

        # 响应
        r = post(Friends_URL, data=d)
        # print(d)

        status = json.loads(r.content)
        logtime = now.strftime('%Y-%m-%d %H:%M:%S')
        log = '%s - logger - INFO - %s : %s' % (logtime, userPhone, status)
        # print(count)
        with open('countFriends.log', mode='a') as f:
            if count == countCollection:
                print(log)
                f.write(log)
                f.write('\n')
                print('#' * len(log))
                f.write('#' * len(log))
            else:
                print(log)
                f.write(log)
            f.write('\n')
    except:
        now = datetime.now()
        strnow = now.strftime('%Y-%m-%d')
        logtime = now.strftime('%Y-%m-%d %H:%M:%S')
        log = '%s - logger - INFO - %s' % (logtime, 'error')
        with open('countFriends.log', mode='a') as f:
            if count == countCollection:
                print(log)
                f.write(log)
                f.write('\n')
                print('#' * len(log))
                f.write('#' * len(log))
            else:
                print(log)
                f.write(log)
                f.write('\n')

