#本篇主要是因为第一次使用python连接MongoDB有很多不会的地方，
#特写这篇笔记用于以后的参考范例。

import pymongo
import random

MONGO_URL = 'localhost' #本地连接
MONGO_DB = 'test' #建立数据库
TAG_INFO = 'tag_info' #建立存储关键词的信息
CONTENT_TITLE = 'content_title' #建立存储百度搜索关键词的信息
CONTENT = 'content' #建立存储某一论坛中用户注册的手机号或email信息
# service_args = ['--load-images=false','--disk-cache=true']# 不加载图片，开启缓存

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def content_title(i,key,keyword):
    content_title ={
        '_id':i, #　某一页的某一个网页链接的序号
        "tag_id": key, # 关键词序列
        "tag_info": keyword,

        "content_title_id": i, # 与content_title的id相关联

        "title": 'dadasd',  # 某一页的某一个网页链接的标题
        "url": "http://www." + str(random.randint(100, 299)) + ".net", #某一页的某一个网页链接
        "count": "100", # 某一页的某一个网页链接中注册人数，int
        "sy_count": "50",  #某一页的某一个网页链接中数据库中剩余没有尝试是否注册的手机号
    }
    if db[CONTENT_TITLE].save(content_title):
        print(i,'存储到CONTENT_TITLE成功',end=',')
    else:
        print(i,'存储到CONTENT_TITLE失败',end=',')

def content(i):
    content = {
        '_id':i, #目前，如果我设置了_id，则循环会产生错误
        "content_title_id": i, # 与content_title的id相关联，理想情况是从1开始循环
        "phone": str(random.randint(18700000000,18799999998)),
        "email": str(random.randint(1000000000,1999999998)) + "@qq.com"

        "title": 'dadasd',  # 某一页的某一个网页链接的标题
    }
    if db[CONTENT].save(content):
        print('存储到CONTENT成功')
    else:
        print('存储到CONTENT失败')

def insert(key,keyword):
    print(keyword)
    for i in range(key,key+10):
        content_title(i, key, keyword)
        content(i)


def main():
    KEYWORD = ['游戏', #1
               '金融', #2
               '电影', #3
               '音乐' #4
               ]
    for keyword in KEYWORD:
        if keyword == '游戏':
            key = 1
            insert(key,keyword)
        elif keyword == '金融':
            key = 1000
            insert(key,keyword)
        elif keyword == '电影':
            key = 2000
            insert(key,keyword)
        elif keyword == '音乐':
            key = 3000
            insert(key,keyword)
        else:
            pass

if __name__ == '__main__':
    main()



