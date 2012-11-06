#!/usr/bin/python
# -*- coding: utf-8 -*-

import wkp.parser
import wkp.export

def launch():
    example = 'http://de.wikipedia.org/wiki/Lama_(Kamel)'
    
    parser = wkp.parser.ArticleParser(example)
    article = parser.getArticle()
    export = wkp.export.PDFExporter(article, 'testoutput.pdf')
    export.write(overwrite = True)
    
    #for s in article.sentences:
    #    print('%8.2f - %s' % (s.impact, s.original))
    
if __name__ == '__main__':
    launch()