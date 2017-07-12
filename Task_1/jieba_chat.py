# 遗憾，没有用到所接触过的NumPy，pandas。感觉本程序是可以通过它们来处理数据，可能会更加的简洁
import requests
import jieba
import json
import jieba.analyse
from requests.exceptions import RequestException

API = 'http://0.0.0.0'

API_Data = API + '/index.php/indexCx/getMobileo' #获取数据的接口
API_Mobile = API + '/index.php/indexCx/mlist/mobile/' #获取手机号的接口
API_KeyWork = API + '/index.php/indexCx/setKeyWordList/' #提交词频的统计结果的对应于手机号的接口

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
    #print('datas',datas)
    #print (type(datas))
    s = ''
    for v in datas:
        #print ("12313",v)
        # 此处datas应该位dict类型，但是却无法使用datas.values(),感觉可能是dict中嵌套了list（一定要再回头来改改）
        # print (type(datas[v]['msgContent']))
        s = s + datas[v]['msgContent']
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

# 本打算用于通过遍历手机号返回到数据库，然而本人实现不了
# def get_one_mobile(html):
#     datas = json.loads(html)
#     for data in datas:
#         for v in data.values():
#             # print(v)
#             return v

def main():
    response = requests.get(API_Data) #获取数据的接口
    # mobile_html = get_one_page(mobileURL) # 获取手机号码网页
    # mobile = get_one_mobile(mobile_html) # 获取某一个手机号码
    # print(mobile)
    html_0 = response.text # 获取手机号码网页
    datas = json.loads(html_0)
    for data in datas:
        for v in data.values():  # v为遍历过程输出的某一个手机号 
            url = API_Mobile + v # 单个手机号的所有信息 #获取手机号的接口
            # print(url)
            html_1 = get_one_page(url) # 获取网页内容
            # print(html_1)
            message = content_one_message(html_1) # 获取网页内全部聊天内容
            word_freq = parse_one_message(message) # 获取聊天内容中词频前20位的词及个数，字符串形式
            # print(word_freq) # 这样的输出：腾讯=6|新闻=6|张林苍=6|重刑犯=5|越狱=5
            url = API_KeyWork #提交词频的统计结果的对应于手机号的接口
            d = {
                'list': word_freq,
                'mobile': v
            }
            r = requests.post(url, data=d)
            print(v ,':', r.content)   # 手机号：返回结果


if __name__ == '__main__':
    main()
