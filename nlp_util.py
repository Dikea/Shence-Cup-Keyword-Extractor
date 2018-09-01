#-*- coding: utf-8 -*-


import codecs
import jieba
from pyhanlp import *
import config


class NlpUtil(object):


    # Add customer words.
    with codecs.open(config.customer_words_path, "r", "utf-8") as rfd:
        customer_words = rfd.read().splitlines()
    jieba.initialize()
    CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary")
    for w in customer_words:
        jieba.add_word(w, freq = 1000000)
        CustomDictionary.add(w)
    print ("Load customer dict done.")
    

    @classmethod
    def word_tokenize(cls, text, use_jieba=True):
        if use_jieba:
            tokens = jieba.lcut(text)
        else:
            tokens = [term.word for term in HanLP.segment(text)]
        return tokens

if __name__ == "__main__":
    print " ".join((NlpUtil.word_tokenize(u"你说爸爸去哪儿呢")))
