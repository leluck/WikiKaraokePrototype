#!/usr/bin/python
# -*- coding: utf-8 -*-

import wkp.parser

def launch():
    example = 'http://de.wikipedia.org/wiki/Lama_(Kamel)'
    
    parser = wkp.parser.ArticleParser(example)
    article = parser.getArticle()
    
    for s in article.sentences:
        print('%8.2f - %s' % (s.impact, s.original))
    
if __name__ == '__main__':
    launch()