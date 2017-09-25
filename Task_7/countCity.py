# -*- coding：utf-8 -*-
from pymongo import MongoClient
from requests import post
from config import *
from datetime import datetime
import json

City_URL = URL + '/index.php/indexCx/setCityList/'
# MONGO_URL = 'mongodb://192.168.0.210:27017/'
MONGO_DB = 'chatLog'
MONGO_Collections = 'usercontacts'

client = MongoClient(MONGO_URL)  # 数据库地址
db = client[MONGO_DB]
users = db[MONGO_Collections]

countCollection = users.count()
# print(countCollection)
count = 0
for user in users.find():  # 遍历usercontacts文档，每次输出一个用户
    count += 1
    try:
        userPhone = int(user['userPhone'])  # 提取用户手机号
        userContacts = user['userContacts']  # 提取userContacts中的信息，然后解析
        contactCity = []
        try:
            for i in range(len(userContacts)):  # 遍历userContacts中全部的值
                if 'contactProvince' in userContacts[i].keys():  # 判断userContacts[x]中是否有'contactProvince'键
                    x = userContacts[i]['contactProvince']
                    # 判断是否为中文
                    if (x >= u'\u4e00' and x <= u'\u9fa5'):  # 去除''的情况
                        contactCity.append(x)
                    # 判断是否为英文
                    elif (x >= u'\u0041' and x <= u'\u005a') or (x >= u'\u0061' and x <= u'\u007a'):
                        contactCity.append('南海诸岛')
                    else:
                        pass
        except:
            pass

        # print(contactCity)
        countList = []
        countStr = ''
        countCity = set(contactCity)  # 统计城市的数量，并构造适合的响应格式
        for i in countCity:
            countList.append("%s=%d" % (i, contactCity.count(i)))  # 构造 城市=数量 的列表
        countStr = '|'.join(countList)

        d = {
            'mobile': userPhone,
            'list': countStr
        }
        url = City_URL  # 城市数量统计的接口
        # 响应
        r = post(url, data=d)
        # print(d)

        status = json.loads(r.content)
        now = datetime.now()
        logtime = now.strftime('%Y-%m-%d %H:%M:%S')
        log = '%s - logger - INFO - %s : %s' % (logtime, userPhone, status)
        # print(count)
        with open('countCity.log', mode='a') as f:
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
        with open('countCity.log', mode='a') as f:
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
