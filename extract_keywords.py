#-*- coding: utf-8 -*-


import codecs
import config
from pyhanlp import *


class KeywordsModel(object):

    def __init__(self):
        self.id2keywords = {}
        self.keywords_set = set()
        self._read_train_docs()
        

    def _read_train_docs(self):
        with codecs.open(config.train_docs, "r", "utf-8") as rfd:
            for line in rfd:
                idx, keywords = line.strip().split("\t")
                keywords = keywords.split(",")
                self.keywords_set.update(keywords)
                self.id2keywords[idx] = keywords


    def extract_keywords(self, idx, title, content):
        if idx in self.id2keywords:
            return [idx] + self.id2keywords[idx][:2]
        keywords = list(HanLP.extractKeyword(title + " " + content, 2))
        return [idx] + keywords


if __name__ == "__main__":
    with codecs.open(config.all_docs, "r", "utf-8") as rfd, \
        codecs.open(config.result_path, "w", "utf-8") as wfd:
        cnt = 0
        model = KeywordsModel()
        rfd.readline()
        wfd.write("id,label1,label2\n")
        for line in rfd:
            cnt += 1
            if cnt % 1000 == 0:
                print ("cnt=%d" % cnt)
            idx, title, content = line.strip().split("\t", 2)
            keywords = model.extract_keywords(idx, title, content)
            wfd.write(",".join(keywords) + "\n")
