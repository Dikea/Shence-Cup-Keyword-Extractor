#-*- coding: utf-8 -*-


import sys
import codecs
from nlp_util import NlpUtil
import config


with codecs.open(config.all_docs, "r", "utf-8") as rfd, \
    codecs.open(config.tokenized_all_docs, "w", "utf-8") as wfd:
    data = rfd.read().split("&&&&")
    for line in data[:-1]:
        try:
            line = line.replace("\n", "")
            info = line.split("\t", 2)
            idx, title, content = info
            title = " ".join(NlpUtil.word_tokenize(title))
            content = " ".join(NlpUtil.word_tokenize(content))
            wfd.write("%s\t%s\t%s&&&&\n" % (idx, title, content))
        except Exception as e:
            print ("line=%s, errmsg=%s" % (line, e)).encode("utf-8")
