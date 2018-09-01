#-*- coding: utf-8 -*-


import time
import codecs
from collections import Counter
import config
from pyhanlp import *
from nlp_util import NlpUtil
from rule_util import RuleUtil
from tfidf_model import TfidfModel


DEBUG = True


def debug_print(text):
    if DEBUG:
        if isinstance(text, str):
            print (text.encode("utf-8"))
        else:
            print (text)


class KeywordsModel(object):

    def __init__(self, raw_corpus):
        self.id2keywords = {}
        self.keywords_set = set()
        self._read_train_docs()
        self.tfidf_inst = TfidfModel(raw_corpus)
        

    def _read_train_docs(self):
        with codecs.open(config.train_docs, "r", "utf-8") as rfd:
            for line in rfd:
                idx, keywords = line.strip().split("\t")
                keywords = keywords.split(",")
                self.keywords_set.update(keywords)
                self.id2keywords[idx] = keywords


    def _vote_for_best(self, multi_keywords):
        count = Counter()
        for keywords in multi_keywords:
            for w in multi_keywords:
                if len(w) < 2: 
                    continue
                count[w] += 1
        ret_keywords = [w for w, c in 
            count.items().sort(key=lambda x: x[1], reverse=True)]
        return ret_keywords
                

    def extract_keywords(self, idx, title, content):
        debug_print("\n\nidx=%s, title=%s" % (idx, title))
        if idx in self.id2keywords:
            debug_print("train_answer: " + " ".join(self.id2keywords[idx]))

        ret_keywords = []
        title = RuleUtil.process_text(title) 
        content = RuleUtil.process_text(content)
        quotes = NlpUtil.extract_quotes((title + content).replace(" ", ""))
        names = NlpUtil.name_recognize(title.replace(" ", "")) 

        debug_print("quotes:" + " ".join(quotes))
        debug_print("names:" + " ".join(names))

        ret_keywords = RuleUtil.add_to_keywords(title, 
            ret_keywords, quotes, once_flag=True)
        debug_print("ret_keywords: " + " ".join(ret_keywords))

        title, ret_keywords = RuleUtil.recognize_foreign_names(
            title, names, ret_keywords)

        ret_keywords = RuleUtil.add_to_keywords(title,
            ret_keywords, names, once_flag=False)
        debug_print("ret_keywords: " + " ".join(ret_keywords))

        tfidf_keywords = self.tfidf_inst.get_keywords(title, content)
        debug_print("tfidf_keywords: " + " ".join(tfidf_keywords))
        for token in tfidf_keywords:
            if token not in ret_keywords:
                ret_keywords.append(token)

        if len(ret_keywords) < 2:
            ret_keywords += title.split()

        debug_print("Final_ret_keywords: " + " ".join(ret_keywords))
        return ret_keywords[:2]


def main():
    s_time = time.time()

    with codecs.open(config.tokenized_all_docs, "r", "utf-8") as rfd, \
        codecs.open(config.result_path, "w", "utf-8") as wfd:
        cnt = 0
        wfd.write("id,label1,label2\n")
        docs = [s.replace("\n", "").split("\t", 2) 
            for s in rfd.read().split("&&&&")][:-1]
        print ("TotalDocNumber=%d" % len(docs))
        raw_corpus = [title.split() + content.split() for _, title, content in docs]

        model = KeywordsModel(raw_corpus)
        for idx, title, content in docs:
            cnt += 1
            if cnt % 1000 == 0:
                print ("cnt=%d" % cnt)
            keywords = model.extract_keywords(idx, title, content)
            answer = idx + "," + ",".join(keywords)
            if len(keywords) == 1:
                answer += ","
            wfd.write(answer + "\n")
                
    e_time = time.time()
    print ("RunTime=%.2f seconds." % (e_time - s_time))


if __name__ == "__main__":
    main()
