# 这片笔记主要是由于做爬虫时遇到了，解析不同网页遇到不同的编码格式，特写的笔记，供以后参考
import urllib.request
import re
import chardet
import urllib

urls = [
'http://www.baidu.com/s?wd=%E6%B8%B8%E6%88%8F&pn=0',
'http://www.baidu.com/link?url=39DnFEGNdmqQy0uQhm-RCmyhJr8hEN5k_OQylHYH9WK',
'http://www.baidu.com/link?url=lfJfl30YBE5J-17DW8Ikus-JV2OFMJPWuvHbv_r6hmu'
]

for i in urls:
    response = urllib.request.urlopen(i).read()
    enconding_dict = chardet.detect(response)
    print(enconding_dict)
    web_encoding = enconding_dict['encoding']
    print(web_encoding)


# 已经学会如何查看网页的编码格式了，但是对于读取的网页内容是否可以判断还不知是否可行，更不会了
if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
    html = response
else:
    html = response.decode('gbk','ignore').encode('utf-8')
# print(html)
