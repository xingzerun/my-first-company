from selenium import webdriver
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time
import pymongo
from config import *
import urllib
import chardet
from urllib import parse

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

#获取百度索引页源代码
def get_page_index(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text,'lxml')
            return soup
        return None
    except RequestException:
        print('请求索引页出错')
        return None

# 提取搜索页结果的url
def findURL(html):
    try:
        list = []
        for i in html.find_all(class_ = 'result'):
            list.append(i.h3.a['href'])
        return list
    except RequestException:
        print('url请求出错')
        return None

#解析索引页每一个索引
def parse_page_index(url):
    try:
        response = urllib.request.urlopen(url).read()
        encoding = chardet.detect(response)['encoding']
        if encoding == 'utf-8' or encoding == 'UTF-8':
            res = requests.get(url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text,'lxml')
            title = soup.title.string
            return title
        elif encoding == 'gb2312' or encoding == 'GB2312':
            res = requests.get(url)
            res.encoding = 'gb2312'
            soup = BeautifulSoup(res.text,'lxml')
            title = soup.title.string
            return title
        else:
            return None
    except:
        parse_page_index(url)

def save_to_CONTENT_TITLE(result):
    try:
        if db[CONTENT_TITLE].insert(result):
            print('存储到CONTENT_TITLE成功',result)
    except:
        print('存储到CONTENT_TITLE失败',result)

def main():
    # browser = webdriver.Chrome()
    # keyword = parse.quote_plus("游戏") #将关键词编码
    keyword = "游戏"
    start = time.time()
    for i in range(0,3):
        url = "http://www.baidu.com/s?wd="+keyword+"&pn=" + str(i*10)
        print(url)
        html = get_page_index(url)
        indexURL = findURL(html)
        for i in range(0,len(indexURL)):
            # print(i,indexURL[i])
            title = parse_page_index(indexURL[i])
            product = {
                # '_id': i,  # 某一页的某一个网页链接的序号
                "tag_id": 1,  # 关键词序列
                "tag_info": keyword,

                # "content_title_id": i,  # 与content_title的id相关联

                "title": title,  # 某一页的某一个网页链接的标题
                "域名": indexURL[i],  # 某一页的某一个网页链接
                # "count": "100",  # 某一页的某一个网页链接中注册人数，int
                # "sy_count": "50",  # 某一页的某一个网页链接中数据库中剩余没有尝试是否注册的手机号
            }
            # print(product)
            save_to_CONTENT_TITLE(product)
        # browser.implicitly_wait(10)
        time.sleep(1)

if __name__ == '__main__':
    main()

