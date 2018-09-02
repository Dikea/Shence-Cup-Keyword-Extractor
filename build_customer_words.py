#-*- coding: utf-8 -*-


import os
import re
import codecs
import config


# Read train docs.
customer_words_set = set()
with codecs.open(config.train_docs, "r", "utf-8") as rfd:
    for line in rfd:
        idx, keywords = line.strip().split("\t")
        keywords = keywords.split(",")
        customer_words_set.update(keywords)


# Read N-gram.
for i in range(3, 4):
    file_name = os.path.join("conf", "result.%dgram" % i)
    with codecs.open(file_name, "r", "utf-8") as rfd:
        for line in rfd:
            info = line.strip().split(",")
            word, _, _, cnt = info
            customer_words_set.add(word)


# Read name-entity extracted form text.
entity_pattern = re.compile(ur"《(.*?)》") 
with codecs.open(config.all_docs, "r", "utf-8") as rfd:
    data = rfd.read().split("&&&&")[:-1]
    for line in data:
        entities = entity_pattern.findall(line)
        customer_words_set.update(entities)


with codecs.open(config.customer_words_path, "w", "utf-8") as wfd:
    for word in customer_words_set:
        if len(word) > 1:
            wfd.write("%s\n" % word)
