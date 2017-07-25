import requests
import json
import jieba
import jieba.analyse

from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

from os import path

API = 'http://0.0.0.0'

API_Data = API + '/index.php/indexCx/getMobileo' #获取数据的接口
API_Mobile = API + '/index.php/indexCx/mlist/mobile/' #获取手机号的接口
API_KeyWork = API + '/index.php/indexCx/setKeyWordList/' #提交词频的统计结果的对应于手机号的接口

def read_content(content_path):
    respone = requests.get(content_path)
    datas = json.loads(respone.text)
    # print(datas)
    message = ''
    for m in datas:
        msg = datas[m]['msgContent']
        if '\n' in msg:
            index = msg.find(':')
            message = message + msg[index:]
        else:
            message = message + msg
    # print(content)
    return message

def make_cloud(keywords,mobile,count):
    d = path.dirname(__file__)
    # 初始化图片
    image = Image.open(path.join(d, "rocket.png"))
    graph = np.array(image)

    # 生成云图
    wc = WordCloud(font_path='font.ttf',background_color='white',
                   max_words=2000,mask=graph)
    wc.generate_from_frequencies(keywords)
    image_color = ImageColorGenerator(graph)

    # 保存云图
    wc.to_file(path.join('%d.png' % count))
    # wc.to_file(path.join('%s.png' % mobile))

    # 显示图片
    # plt.imshow(wc)
    # plt.imshow(wc.recolor(color_func=image_color))
    # plt.axis("off")  # 关闭图像坐标系
    # plt.show()

def main():
    response = requests.get(API_Data)
    mobile_html = response.text
    mobiles = json.loads(mobile_html)
    count = 0
    for mobile in mobiles:
        # print(mobile['mobile'])
        mobile = mobile['mobile']
        content_path = API_Mobile + mobile
        # print(content_path)
        message = read_content(content_path)
        try:
            if len(message) is 0:
                print(0, mobile, len(message))
                pass
            else:
                count+=1
                print(count, mobile, len(message))
                result = jieba.analyse.textrank(message, topK=1000, withWeight=True)

                # 生成关键词比重字典
                keywords = dict()
                for i in result:
                    keywords[i[0]] = i[1]
                # print(keywords)
                make_cloud(keywords, mobile, count)
        except:
            pass


if __name__ == '__main__':
    main()
