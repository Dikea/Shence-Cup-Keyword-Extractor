#-*- coding: utf-8 -*-


import re


quote_pattern = re.compile(ur"《(.*?)》")


class RuleUtil(object):

    @classmethod
    def process_text(cls, text):
        if not (u"《" in text and u"》" in text):
            return text

        new_tokens = []
        uniq_s = ""
        for s in quote_pattern.findall(text):
            s = s.replace(" ", "")
            new_tokens.append(u"《" + " " + s + " " + u"》")
            uniq_s += s + u"《" + u"》"
        for token in text.split():
            if token not in uniq_s:
                new_tokens.append(token)
        new_text = " ".join(new_tokens)
        print ("new_text: %s" % new_text).encode("utf-8")

        return new_text 


    @classmethod
    def add_to_keywords(cls, title, keywords, words_set, once_flag=False):
        for token in title.split():
            if token in words_set and token not in keywords:
                keywords.append(token)
                if once_flag:
                    return keywords
        """
        keywords_str = "".join(keywords)
        for token in words_set:
            if token not in keywords_str:
                keywords.append(token)
                if once_flag:
                    break
        """
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
