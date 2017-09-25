from requests import post
from pymongo import MongoClient
from config import *
from datetime import datetime
import json

Sex_URL = URL + '/index.php/indexCx/setSixList/'
# MONGO_URL = 'mongodb://0.0.0.0:27017/'
MONGO_DB = 'chatLog'
MONGO_Collections = 'usercontacts'

client = MongoClient(MONGO_URL) #需要数据库地址
db = client[MONGO_DB]
users = db[MONGO_Collections]

countCollection = users.count()
# print(countCollection)
count = 0
for user in users.find():
    count += 1
    try:
        userPhone = int(user['userPhone'])
        userContacts = user['userContacts']
        contactSex = []
        try:
            for i in range(len(userContacts)):
                if 'contactSex' in userContacts[i].keys():
                    x = userContacts[i]['contactSex']
                    if x == 0:
                        x = '未知'
                    elif x == 1:
                        x = '男'
                    elif x == 2:
                        x = '女'
                    else:
                        pass
                    contactSex.append(x)
                else:
                    pass
        except:
            pass

        countList = []
        countStr = ''
        countSex = set(contactSex)
        for i in countSex:
            countList.append("%s=%d" % (i, contactSex.count(i)))
        countStr = '|'.join(countList)

        d = {
            'mobile': userPhone,
            'list': countStr
        }
        url = Sex_URL #性别统计的接口
        # 响应
        r = post(url, data=d)
        print(d)

        status = json.loads(r.content)
        now = datetime.now()
        logtime = now.strftime('%Y-%m-%d %H:%M:%S')
        log = '%s - logger - INFO - %s : %s' % (logtime, userPhone, status)

        # print(count)
        with open('countSex.log', mode='a') as f:
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
        with open('countSex.log', mode='a') as f:
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
