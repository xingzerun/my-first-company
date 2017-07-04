from pymongo import MongoClient
from requests import post

client = MongoClient(API_mongoDB) #数据库地址
db = client['chatLog']
users = db['usercontacts']

for user in users.find():  # 遍历usercontacts文档，每次输出一个用户
    userPhone = user['userPhone']  #提取用户手机号
    userContacts = user['userContacts'] #提取userContacts中的信息，然后解析
    contactCity = []
    try:
	    for i in range(len(userContacts)):  # 遍历userContacts中全部的值
	        if 'contactCity' in userContacts[i].keys():  # 判断userContacts[x]中是否有'contactCity'键
	            x = userContacts[i]['contactCity']
	            if x != '': # 去除''的情况
	                contactCity.append(x)
	            else:
	                pass
	        else:
	            pass
    except:
        pass

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

    url = API_City #城市数量统计的接口
    r = post(url,data=d)
    print(userPhone, ':', r.content)
