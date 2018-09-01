#-*- coding: utf-8 -*-


import re
import codecs
import jieba
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
    name_segment = HanLP.newSegment().enableNameRecognize(True)
    

    @classmethod
    def word_tokenize(cls, text, use_jieba=True):
        if use_jieba:
            tokens = jieba.lcut(text)
        else:
            tokens = [term.word for term in HanLP.segment(text)]
        return tokens


    @classmethod
    def name_recognize(cls, text):
        term_list = cls.name_segment.seg(text)
        names = [t.word for t in list(term_list) if str(t.nature) == "nr"]
        return set(names)


    @classmethod
    def extract_quotes(cls, text):
        quotes = quote_pattern.findall(text)
        return set(quotes)


if __name__ == "__main__":
    print " ".join((NlpUtil.word_tokenize(u"你说爸爸去哪儿呢", False)))
    print " ".join(NlpUtil.name_recognize(u"杨超越出演那年花开月正圆"))
