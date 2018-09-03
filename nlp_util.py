#-*- coding: utf-8 -*-


import re
import codecs
import jieba
import jieba.analyse
from gensim import summarization
from pyhanlp import *
import config


quote_pattern = re.compile(ur"《(.*?)》")


class NlpUtil(object):


    # Add customer words.
    with codecs.open(config.customer_words_path, "r", "utf-8") as rfd:
        customer_words = rfd.read().splitlines()
    jieba.initialize()
    CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary")
    for w in customer_words:
        jieba.add_word(w, freq = 1000000)
        #CustomDictionary.add(w)
    print ("Load customer dict done.")
    ch_name_segment = HanLP.newSegment().enableNameRecognize(True)
    ja_name_segment = HanLP.newSegment().enableJapaneseNameRecognize(True)
    fr_name_segment = HanLP.newSegment().enableTranslatedNameRecognize(True)
    text_rank_keywords = JClass("com.hankcs.hanlp.summary.TextRankKeyword")


    @classmethod
    def word_tokenize(cls, text, use_jieba=True):
        if use_jieba:
            tokens = jieba.lcut(text)
        else:
            tokens = [term.word for term in HanLP.segment(text)]
        return tokens


    @classmethod
    def name_recognize(cls, text):
        text = text.replace(" ", "")
        ch_names = [t.word for t in list(cls.ch_name_segment.seg(text)) if "nr" in str(t.nature)]
        fr_names = [t.word for t in list(cls.fr_name_segment.seg(text)) if "nr" in str(t.nature)]
        fr_names = [w for w in fr_names if u"·" in w]
        fr_str = "".join(fr_names)
        ch_names = [w for w in ch_names if w not in fr_str]
        names = list(set(ch_names + fr_names))
        return names


    @classmethod
    def extract_quotes(cls, text):
        quotes = quote_pattern.findall(text.replace(" ", ""))
        return list(set(quotes))


    @classmethod
    def text_rank(cls, title, content, size=5):
        print title, content
        #keywords = summarization.keywords(title + " " + content).split('\n')[:5] 
        keywords = HanLP.extractKeyword(title + " " + content, 5)
        keywords = [w for w in keywords if w in title and len(w) >= 2]
        #jieba.analyse.textrank(text, topK=5, 
        #    withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
        return keywords


if __name__ == "__main__":
    print " ".join((NlpUtil.word_tokenize(u"你说爸爸去哪儿呢", False)))
    print " ".join(NlpUtil.name_recognize(u"新亘结衣加盟迪士尼新片《丛林巡航》"))
