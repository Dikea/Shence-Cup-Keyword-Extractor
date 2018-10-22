# ShenceCup.extract_keywords

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
