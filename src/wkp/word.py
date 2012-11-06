# -*- coding: utf-8 -*-

import lovelysystems.stemmer as stemmer

class WordAlreadyExistsException(Exception):
    pass

class WordTooShortException(Exception):
    pass

class Word:
    all = set()
    
    def __init__(self, word):
        self.original = word.lower()
        
        self.stem = stemmer.stem(word)
        
        if self.stem in self.all:
            raise WordAlreadyExistsException
        if len(self.stem) < 4:
            raise WordTooShortException
        self.all.add(self.stem)
        
        self.count = 1.0
        self.impact = 0.0
    
    def __lt__(self, other):
        if self.count < other.count:
            return True
        return False
    
    def __eq__(self, other):
        if self.count == other.count:
            return True
        return False
    
    def increment(self):
        self.count = self.count + 1.0
    
    def calculateImpact(self, normalization = 1.0, scaling = 1.0):
        self.impact = (float(self.count) * float(scaling)) / float(normalization)