import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
#import matplotlib.pyplot as plt
from datetime import date, time, datetime, timedelta
import requests


API = 'http://192.168.0.210'

API_Data = API + '/index.php/indexCx/getMobileo' #获取数据的接口
API_Mobile = API + '/index.php/indexCx/mlist/mobile/' #获取手机号的接口
API_KeyWork = API + '/index.php/indexCx/setKeyWordList/' #提交词频的统计结果的对应于手机号的接口

# 整合全部的聊天记录
def content(mobile):
	url = API_Mobile + mobile
	datas = requests.get(url).json()
	message = ''
	for data in datas:
		msg = datas[data]['msgContent']
		if '\n' in msg:
			index = msg.find(':')
			message = message + msg[index:]
		else:
			message = message + msg
	# print(message)
	return message

# 统计聊天记录词频
def word_freq(text):
	words = jieba.cut(text,cut_all=False) # 精确模式
	keywords = {}
	for word in words:
	    if word in keywords:
	        keywords[word] += 1
	    else:
	        keywords[word] = 1
	# print(type(keywords))
	# print(keywords)

	# 排序且只保留中文word
	word_cloud = dict()
	for key in keywords:
	    if  u'\u4e00' <= key <= u'\u9fa5' and len(key)>2:
	        word_cloud[key] = keywords[key]
	    else:
	        pass
	# print(word_cloud)
	return word_cloud

def word_mask(CN_freq, mobile):
	# 初始化底图
	image = Image.open('rocket.png')
	graph = np.array(image)

	# stopwords = set(STOPWORDS)


	# 生成云图
	wc = WordCloud(font_path='font.ttf',background_color='white',
	               max_words=2000,mask=graph)
	wc.generate_from_frequencies(CN_freq)
	image_color = ImageColorGenerator(graph)

	# 保存云图
	wc.to_file('%s.png' %mobile)

	# 显示图片
	# plt.imshow(wc)
	# plt.imshow(wc.recolor(color_func=image_color))
	# plt.axis("off")  # 关闭图像坐标系
	# plt.show()

def main():
    try:
        datas = requests.get(API_Data).json()
        # print(datas)
        # 提取全部的手机号码
        count = 0
        for data in datas:
            mobile = data['mobile']
            # print(mobile)
            text = content(mobile)
            # print(text)
            CN_freq = word_freq(text)
            # print(CN_freq,len(CN_freq))
            if len(CN_freq) == 0:
                print(mobile + '：暂无有效的聊天记录')
                pass
            else:
                count = count + 1
                word_cloud = word_mask(CN_freq, mobile)
                print(mobile + '：第%d词云已生成' %count)
        print('词云任务完成')
    except:
        print('wordcloud error')

if __name__ == '__main__':
    main()
