#-*- coding: utf-8 -*-


import re


quote_pattern = re.compile(ur"《(.*?)》")


class RuleUtil(object):

    @classmethod
    def process_text(cls, text):
        if not (u"《" in text and u"》" in text):
            return text

        for s in quote_pattern.findall(text):
            text = text.replace(s, " " + s.replace(" ", "") + " ")
        print ("new_text: %s" % text).encode("utf-8")

        return text 


    @classmethod
    def add_to_keywords(cls, title, keywords, words_set, once_flag=False):
        for token in title.split():
            if token in words_set and token not in keywords:
                keywords.append(token)
                if once_flag:
                    return keywords
        return keywords


    @classmethod
    def recognize_foreign_names(cls, title, names, keywords):
        raw_title = title.replace(" ", "")
        tokens = title.split()
        if "·" in tokens and len(names) >= 2:
            names_len = len(names)
            new_name = ""
            for i in range(names_len):
                if new_name:
                    break
                for j in range(names_len):
                    name = names[i] + "·" + names[j]
                    if name in raw_title:
                        new_name = name
                        print("new_name: " + new_name)
                        break
            if new_name:
                keywords.append(new_name)
                new_tokens = [new_name]
                for token in title.split():
                    if token not in new_name:
                        new_tokens.append(token)
                new_title = " ".join(new_tokens)
                print("new_title: %s" % new_title).encode("utf-8")
                return new_title, keywords
        return title, keywords


if __name__ == "__main__":
    print RuleUtil.process_text(u"《 你 好 · 呀 》")
