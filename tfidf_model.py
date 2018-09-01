#-*- coding: utf-8 -*-


import codecs
from gensim import corpora, models
import config


class TfidfModel(object):

    def __init__(self, raw_corpus):
        self.dictionary = corpora.Dictionary(raw_corpus)
        corpus = [self.dictionary.doc2bow(s) for s in raw_corpus]
        self.model = models.tfidfmodel.TfidfModel(corpus, normalize=False)
        print ("Build tfidf model done.")


    def get_keywords(self, title, content):
        t_tokens = title.split()
        c_tokens = content.split()
        tokens = t_tokens + c_tokens 
        bow = self.dictionary.doc2bow(tokens)
        tfidf = self.model[bow]
        keywords = [(self.dictionary[idx], value) for idx, value in tfidf]
        keywords.sort(key=lambda x: x[1], reverse=True)
        keywords = [w for w, v in keywords if len(w) >= 2 and w in t_tokens]
        return keywords


if __name__ == "__main__":
    tfidf_inst = TfidfModel(config.tokenized_all_docs)
    for word, value in tfidf_inst.get_keywords(u"林志玲 不错 呀"):
        print ("%s, %s" % (word, value))
