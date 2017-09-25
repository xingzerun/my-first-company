import requests
import jieba
import json
import jieba.analyse
from requests.exceptions import RequestException
from config import *
from datetime import datetime
import json

# URL = 'http://0.0.0.0'
GetMobile_URL = URL + '/index.php/indexCx/getMobileo' #获取数据的接口
Mobile_URL = URL + '/index.php/indexCx/mlist/mobile/' #获取手机号的接口
KeyWork_URL = URL + '/index.php/indexCx/setKeyWordList/' #提交词频的统计结果的对应于手机号的接口


#获取某一个网页
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#合并某一个手机号的全部聊天内容
def content_one_message(html):
    datas = json.loads(html)
    s = ''
    for v in datas:
        msg = datas[v]['msgContent']
        if '\n' in msg:
            index = msg.find(':')
            s = s + msg[index:]
        else:
            s = s + msg
    return s

#解析某一个手机号的聊天内容
def parse_one_message(message):
    jieba.add_word('邦盈网络')
    # 统计词频
    words = jieba.cut(message,cut_all=False) # 精确模式
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    # print(word_freq)

    # 排序且只保留中文word
    freq_word = []
    for word,freq in word_freq.items():
        if word >= u'\u4e00' and word <= u'\u9fa5' and len(word)>2:
            freq_word.append((word,freq))
    freq_word.sort(key=lambda x:x[1],reverse=True)

    # 汇总前二十名的词频
    ls = ''
    for word,freq in freq_word[:14]:
        ls = ls + word + '=' + str(freq) + '|'

    ls = ls[:-1]
    return ls

def main():
    # 如果一开始就获取时间是程序开始的时间
    # now = datetime.now()
    # logtime = now.strftime('%Y-%m-%d %H:%M:%S')

    count = 0

    response = requests.get(GetMobile_URL)
    html_0 = response.text # 获取手机号码网页
    datas = json.loads(html_0)
    for data in datas:
        count+=1
        # print(count)
        for v in data.values():  # v为遍历过程输出的某一个手机号
            url = Mobile_URL + v # 单个手机号的所有信息 #获取手机号的接口
            # print(url)
            html_1 = get_one_page(url) # 获取网页内容
            # print(html_1)
            message = content_one_message(html_1) # 获取网页内全部聊天内容
            # print(message)
            word_freq = parse_one_message(message) # 获取聊天内容中词频前20位的词及个数，字符串形式
            # print(word_freq) # 这样的输出：腾讯=6|新闻=6|张林苍=6|重刑犯=5|越狱=5
            url = KeyWork_URL #提交词频的统计结果的对应于手机号的接口
            # mobile = int(v)
            d = {
                'mobile': v,
                'list': word_freq,
            }
            # 响应
            r = requests.post(url, data=d)
            print(d)

            status = json.loads(r.content)
            now = datetime.now()
            logtime = now.strftime('%Y-%m-%d %H:%M:%S')
            log = '%s - logger - INFO - %s : %s' % (logtime, v, status)
            with open('wordCount.log', mode='a') as f:
                if count == len(datas):
                    print(log)
                    f.write(log)
                    f.write('\n')
                    print('#' * len(log))
                    f.write('#' * len(log))
                else:
                    print(log)
                    f.write(log)
                f.write('\n')

if __name__ == '__main__':
    main()
