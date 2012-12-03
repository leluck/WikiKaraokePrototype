#!/usr/bin/python
# -*- coding: utf-8 -*-

import wkp.retriever
import wkp.export

def launch():
    example = 'http://de.wikipedia.org/wiki/Lama_(Kamel)'
    
    receiver = wkp.retriever.ArticleRetriever(example)
    article = receiver.getArticle()
    exporter = wkp.export.PDFExporter(article, 'testoutput.pdf')
    exporter.write(overwrite = True)
    
    #for s in article.sentences:
    #    print('%8.2f - %s' % (s.impact, s.original))
    
if __name__ == '__main__':
    launch()