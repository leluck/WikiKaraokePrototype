#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('C:\\Program Files\\Python27\\lib\\site-packages\\PIL')
#TODO: permanently add PIL to sys.path, installation for win was broken
#      due to spaces in install path.

import wkp.parser
import wkp.export

def launch():
    example = 'http://de.wikipedia.org/wiki/Stechmücke'
    
    parser = wkp.parser.ArticleParser(example)
    article = parser.getArticle()
    export = wkp.export.PDFExporter(article, 'testoutput.pdf')
    export.write(overwrite = True)
    
    #for s in article.sentences:
    #    print('%8.2f - %s' % (s.impact, s.original))
    
if __name__ == '__main__':
    launch()