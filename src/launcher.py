#!/usr/bin/python
# coding=utf-8

import wkp.parser

def launch():
    example = 'http://de.wikipedia.org/wiki/Bienen'
    
    parser = wkp.parser.ArticleParser(example)
    article = parser.getArticle()
    
    for s in sorted(article.sentenceWeights, key=lambda s: s[1], reverse=True):
        print(s[0])
        print(s[1])
    
if __name__ == '__main__':
    launch()