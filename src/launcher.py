#!/usr/bin/python
# -*- coding: utf-8 -*-

import wkp.parser

def launch():
    example = 'http://de.wikipedia.org/wiki/Lama_(Kamel)'
    
    parser = wkp.parser.ArticleParser(example)
    article = parser.getArticle()
    
    for (sentence, weight) in sorted(article.sentenceWeights, key = lambda s: s[1], reverse = True):
        print('%6.2f: %s' % (weight, sentence))
    
if __name__ == '__main__':
    launch()