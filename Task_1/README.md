# Task One

* 聊天记录词频统计
* 接口中全部的手机号码统计

2017.7.24   
需求：公司项目逐渐完善，提出了展示词云效果的词频统计。  
计划：  
通过学习发现例子中使用了**基于TF-IDF算法的关键词抽取**，由此有以下思路：

* 延续老方法，通过jieba.cut()，用自己的笨方法，笨数据分析（嘿嘿），统计出词频，制作wordcloud
* 使用jieba.analyse

		jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
	* sentence 为待提取的文本
	* topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
	* withWeight 为是否一并返回关键词权重值，默认值为 False
	* allowPOS 仅包括指定词性的词，默认值为空，即不筛选
	
	jieba.analyse.TFIDF(idf_path=None) 新建 TFIDF 实例，idf_path 为 IDF 频率文件

* 刚刚看了一下amueller的demo，发现人家根本就没有用jieba（人家是老外。。。固定思维害死人。。。），写完这个去试试，不用jieba是啥子情况
	

## 词云:
WordCloud：https://amueller.github.io/word_cloud/index.html   
乔巴：http://mp.weixin.qq.com/s?__biz=MjM5NTgwMDE4NA==&mid=2653407094&idx=2&sn=7a544ffca9b6b79c6ea51e5dac6b7488&chksm=bd2192618a561b77d17c57484937d586290f87bf788385113327535f02a949d89099dd61a05b&mpshare=1&scene=23&srcid=0602oc3tDXzKPQMdf1vY4JXq#rd

## jieba中可能可以用来禁用词的方法
 jieba.analyse.ChineseAnalyzer有停用词的处理（https://github.com/fxsjy/jieba/issues/77）：https://github.com/fxsjy/jieba/blob/master/jieba/analyse/analyzer.py  
 ‘你是说stopwords？ 现在还没有提供接口，你可以先试一试效果’（https://github.com/fxsjy/jieba/issues/54）：https://github.com/fxsjy/jieba/blob/master/test/extract_tags.py
## stop_word demo
extract_tags：https://github.com/fxsjy/jieba/blob/master/test/extract_tags_stop_words.py

2017.7.28  
需求：把word_cloud和定时任务合并，做成一个文件  
总结：  
上次由于时间紧迫，提交的其实是提取关键词的词云，趁着这次机会又重新改为词频云了，完美~  
但是，stopword和字体颜色仍然不能随心所欲的更改，很烦！   
有几个模糊的计划：  

* 自己写一个文件，把stopwords一个一个的排除。
	* https://github.com/FantasRu/WordCloud/blob/master/main.py
	* https://github.com/fyuanfen/wordcloud/blob/master/word.py
* 该源码！？经过试验，修改作者https://github.com/xingzerun/word_cloud/blob/master/examples/masked.py中的

		-text = open(path.join(d, 'alice.txt')).read()  
		+text = open(path.join(d, 'alice.txt')，encoding='utf-8').read()
alice.txt中可以全为中文，并且也可以很好地制作词云

