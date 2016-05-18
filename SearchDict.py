#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import re
import urllib

class SearchDict(object):
    def __init__(self, query_list):
        self.query_list = query_list
        self.base_url = 'http://dict-co.iciba.com/api/dictionary.php?'

    def get_translated_list(self):
        self.translated_list = []

        for query in self.query_list:
            url_arg = {
                'type': 'json',
                'key':  'INSERT YOUR KEY',
                'w': query.encode('utf-8')
            }
            api_url = self.base_url + urllib.urlencode(url_arg)
            content = urllib.urlopen(api_url).read()
            data = json.loads(content)

            for part in data['symbols'][0]['parts']:
                for mean in part['means']:
                    translated_word = mean.encode('utf-8')
                    self.translated_list.append([translated_word])
        return self.translated_list


    def get_pure_translation(self):
        self.pure_translation = []
        for j in range(len(self.translated_list)):
            target = self.translated_list[j][0]
            remove_marks = re.compile("\s+|【.*?】+|\[.*?\]+|（.*?）+|[\.0-9]+|[a-zA-Z0-9]").sub('',target)
            generate_tokens = re.split(u'[\uff1b\uff0c\n]',remove_marks.decode("utf8"))
            self.pure_translation.append(generate_tokens)
        return self.pure_translation


if __name__ == '__main__':
    print 'What do you want to translate:'
    query_list = [j.strip() for j in raw_input('> ').split(' ')]
    print '\n'

    translator = SearchDict(query_list)
    translated_list = translator.get_translated_list()

    print 'Result:'
    for i in range(len(translated_list)):
        print '\t' + translated_list[i][0]

    print 'Improved Results:'
    pure_translation = translator.get_pure_translation()
    for j in range(len(pure_translation)):
        for k in range(len(pure_translation[j])):
            print '\t' + pure_translation[j][k]
