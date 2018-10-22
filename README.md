# ShenceCup.extract_keywords

[神策杯](http://www.dcjingsai.com/common/cmpt/%E2%80%9C%E7%A5%9E%E7%AD%96%E6%9D%AF%E2%80%9D2018%E9%AB%98%E6%A0%A1%E7%AE%97%E6%B3%95%E5%A4%A7%E5%B8%88%E8%B5%9B_%E8%B5%9B%E4%BD%93%E4%B8%8E%E6%95%B0%E6%8D%AE.html)第五名解决方案

## 1. 运行环境和依赖
```python2.7```
依赖Python包:```pandas numpy pyhanlp jieba gensim```

## 2. 数据清洗说明
从训练数据进行新词发现，合成自定义词典，利用jieba进行分词
运行程序： ```./process.sh```

## 3. 主程序运行
提取语料关键词
```python extract_keywords.py > o &```
关键词分析结果会在目录下result.csv文件中。


## 解题思路：
通过对训练语料训练分析，发现书名号内的引用内容，和人名等信息最容易作为关键词，所以使用pyhanlp包来进行命名实体识别，识别人名。另外，使用textrank提取文本摘要，使用tfidf来对关键词进行排序。优先级策略为：书名号内容 > 人名 > 在训练语料中出现过的关键词 > textrank + tfidf 权重排序。模型没有使用外部语料。
