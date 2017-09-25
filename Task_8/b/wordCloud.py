import requests
import jieba
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
from datetime import datetime
from config import *
from os import path

d = path.dirname('./a/')
d2 = path.dirname('./b/')

GetMobile_URL = URL + '/index.php/indexCx/getMobileo' #获取数据的接口
Mobile_URL = URL + '/index.php/indexCx/mlist/mobile/' #获取手机号的接口
KeyWork_URL = URL + '/index.php/indexCx/setKeyWordList/' #提交词频的统计结果的对应于手机号的接口

def content(mobile):
    url = Mobile_URL + mobile
    datas = requests.get(url).json()
    message = ''
    for data in datas:
        msg = datas[data]['msgContent']
        if '\n' in msg:
            index = msg.find(':')
            message = message + msg[index:]
        else:
            message = message + msg
    return message

def word_freq(text):
    words = jieba.cut(text, cut_all=False)
    keywords = {}
    for word in words:
        if word in keywords:
            keywords[word] += 1
        else:
            keywords[word] = 1

    # 排序并只保留中文
    word_cloud = dict()
    for key in keywords:
        if u'\u4e00' <= key <= u'\u9fa5' and len(key)>2:
            word_cloud[key] = keywords[key]
        else:
            pass
    return word_cloud

def word_mask(CN_freq, mobile):
    image = Image.open(path.join(d2, 'rocket.png'))
    graph = np.array(image)

    # 生成云图
    wc = WordCloud(font_path='font.ttf',background_color='white',
	               max_words=2000,mask=graph)
    wc.generate_from_frequencies(CN_freq)
    # image_color = ImageColorGenerator(graph)

    # 保存云图
    wc.to_file(path.join(d,'%s.png' % mobile))
    # wc.to_file('./a', '%s.png' % mobile)

    # 显示图片
    # plt.imshow(wc)
    # plt.imshow(wc.recolor(color_func=image_color))
    # plt.axis("off")  # 关闭图像坐标系
    # plt.show()

def main():
    datas = requests.get(GetMobile_URL).json()
    total = len(datas)
    count = 0
    countNO = 0
    for data in datas:
        count += 1
        mobile = data['mobile']
        text = content(mobile)
        CN_freq = word_freq(text)

        # log
        now = datetime.now()
        logtime = now.strftime('%Y-%m-%d %H:%M:%S')

        if len(CN_freq) == 0:
            log = '%s - logger - INFO - %s' % (logtime, 'NoChatRecord')
            # print(log)
        else:
            countNO += 1
            # word_cloud = word_mask(CN_freq, mobile)
            word_mask(CN_freq, mobile)
            log = '%s - logger - INFO - NO.%d WordCloud' % (logtime, countNO)
            # print(log)
        with open('wordCloud.log', mode='a') as f:
            if count == total:
                f.write(log)
                f.write('\n')
                f.write('#' * len(log))
                print(log)
            else:
                f.write(log)
                print(log)
            f.write('\n')

if __name__ == '__main__':
    main()
