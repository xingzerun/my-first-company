#百度注册接口
#只是最简单的通过接口可以成功的验证手机号有无注册。由于过于简单，很容易被识别并禁止

import requests
import json

url = 'https://passport.baidu.com/v2/?\
regphonecheck&token=92f62c492cdb16d85026bf3497ccc6d7&tpl=mn&apiver=v3&\
tt=1498797248673&phone={}&countrycode=&gid=9D4CE3F-EAA5-4B75-B160-4051120FF598&\
exchange=0&isexchangeable=1&callback=bd__cbs__8uwa5j'

def getmsg(phone):
    msg = requests.get(url.format(phone))
    msg.encoding = 'utf-8'
    html = msg.text.strip('bd__cbs__8uwa5j(').rstrip(')')
    jd = json.loads(html)
    return jd['errInfo']['msg']

phone = 18795985950
getmsg(phone)
