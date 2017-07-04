from requests import post
from pymongo import MongoClient

client = MongoClient(API) #需要数据库地址
db = client['chatLog']
users = db['usercontacts']

for user in users.find():
    userPhone = user['userPhone']
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

    url = API_mobile #提交性别统计的接口
    r = post(url, data=d)
    print(userPhone,':',r.content)
