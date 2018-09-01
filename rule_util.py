#-*- coding: utf-8 -*-



class RuleUtil(object):

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
            for i in range(names_len):
                for j in range(names_len):
                    new_name = names[i] + "·" + names[j]
                    if new_name in raw_title:
                        debug_print("new_name: " + new_name)
                        break
            keywords.append(new_name)
            if i == names_len:
                return
            new_tokens = [new_name]
            for token in title:
                if token not in new_name:
                    new_tokens.append(token)
            new_title = " ".join(new_tokens)
            print("new_title: %s" % new_title).encode("utf-8")
            return new_title, keywords
        else:
            return title, keywords
