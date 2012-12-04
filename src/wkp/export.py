# -*- coding: utf-8 -*-

import os

import pyfpdf
import random

class ExporterTargetInvalidException(Exception):
    pass

class ExporterTargetExistsException(Exception):
    pass

class PDFExporter:
    def __init__(self, article, target, overwrite = False):
        self.article = article
        self.target = target
        self.random = random.Random()
        self.pdf = pyfpdf.FPDF(format = 'A5', orientation = 'L')
        
        self.article.downloadImages(overwrite = False)
        print('Generating PDF contents...')
        
        self._selectSentences()
        self._createTitlePage()
        self._createContentPages()
    
    def _selectSentences(self, topSentenceCount = 10, randomSentenceCount = 10):
        max = len(self.article.sentences)
        self.sentenceSelection = list()
        
        # Add top 10 sentences to selection
        self.sentenceSelection.extend(self.article.sentences[0 : (max -1 if max < topSentenceCount else topSentenceCount)])
        # Add random 10 sentences to selection
        for _ in range(randomSentenceCount):
            self.sentenceSelection.append(self.random.choice(self.article.sentences[len(self.sentenceSelection):]))
    
    def _createTitlePage(self):
        self.pdf.add_page()
        
        self.pdf.set_font('Arial', size = 24)
        
        if len(self.article.storedImages) > 0:
            self.pdf.image(self.article.storedImages[0], x = 10, y = 10, h = 30)
            self.pdf.cell(45, 30)
        
        self.pdf.multi_cell(135, 10, txt = self.article.title)
        self.pdf.ln(20)
        self.pdf.set_font('Arial', size = 16)
        self.pdf.multi_cell(180, 10, txt = self.random.choice(self.article.sentences).original)
        
    def _createContentPages(self):
        self.pdf.set_margins(25, 15, 25)
        self.pdf.set_font('Arial', size = 16)
        
        sentenceList = self.sentenceSelection[:]
        
        while len(sentenceList) > 0:
            self.pdf.add_page()
            self.pdf.ln(10)
            
            for _ in range(3 if len(sentenceList) > 3 else len(sentenceList)):
                sentence = sentenceList.pop(self.random.randint(0, len(sentenceList) - 1))
                self.pdf.multi_cell(160, 6, txt = sentence.original)
                self.pdf.ln(10)
    
    def write(self, overwrite = False):
        print('Writing PDF file...')
        
        if os.path.isdir(self.target):
            raise ExporterTargetInvalidException('Defined target is a directory.')
        if os.path.isfile(self.target) and not overwrite:
            raise ExporterTargetExistsException('Defined target exists.')
        if os.path.isfile(self.target) and overwrite:
            os.remove(self.target)
        
        self.pdf.output(self.target)
        