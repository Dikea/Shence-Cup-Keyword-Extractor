#-*- coding: utf-8 -*-


import sys
import codecs


def discover_new_words(title, content):
    words_set = set()
    t_len, c_len = len(title), len(content)
    print title
    print content
    for step in range(3, 7):
        for i in range(t_len):
            if i + step > t_len:
                continue
            word = title[i : i + step]
            if word in content:
                words_set.add(word)
                print word
    return words_set



if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    new_words_set = set()
    with codecs.open(input_file, "r", "utf-8") as rfd:
        rfd.readline()
        for line in rfd:
            idx, title, content = line.strip().split("\t", 2)
            new_words = discover_new_words(title, content)
            new_words_set.update(new_words)

    with codecs.open(output_file, "r", "utf-8") as wfd:
        for w in new_words_set:
            wfd.write("%s\n" % w)
