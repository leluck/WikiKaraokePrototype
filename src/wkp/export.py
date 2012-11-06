# -*- coding: utf-8 -*-

import os

import pyfpdf

class ExporterTargetInvalidException(Exception):
    pass

class ExporterTargetExistsException(Exception):
    pass

class PDFExporter:
    def __init__(self, article, target, overwrite = False):
        self.article = article
        self.target = target
        self.pdf = pyfpdf.FPDF(format = 'A5', orientation = 'L')
        
        self.article.downloadImages(overwrite = True)
        print('Generating PDF contents...')
        self._createTitlePage()
        
    def _createTitlePage(self):
        self.pdf.add_page()
        
        self.pdf.set_font('Arial', size = 24)
        
        if len(self.article.storedImages) > 0:
            self.pdf.image(self.article.storedImages[0], x = 10, y = 10, w = 30)
            self.pdf.cell(50, 50)
        
        self.pdf.cell(50, 20, txt = self.article.title, align = 'C')
    
    def write(self, overwrite = False):
        print('Writing PDF file...')
        
        if os.path.isdir(self.target):
            raise ExporterTargetInvalidException('Defined target is a directory.')
        if os.path.isfile(self.target) and not overwrite:
            raise ExporterTargetExistsException('Defined target exists.')
        if os.path.isfile(self.target) and overwrite:
            os.remove(self.target)
        
        self.pdf.output(self.target)
        