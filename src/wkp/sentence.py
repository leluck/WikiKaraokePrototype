# -*- coding: utf-8 -*-

import lovelysystems.stemmer as stemmer

class Sentence:
    def __init__(self, sentence):
        self.original = sentence
        self.impact = 0.0

    def __lt__(self, other):
        if self.impact < other.impact:
            return True
        return False
    
    def __eq__(self, other):
        if self.impact == other.impact:
            return True
        return False
    
    def __len__(self):
        return len(self.original)
    
    def calculateImpact(self, knownWords):
        sum = 0.0
        wordcount = 0
        
        for word in self.original.split():
            wordcount += 1
            stem = stemmer.stem(word)
            if stem in knownWords.keys():
                sum += knownWords[stem].impact
        
        self.impact = sum / float(wordcount)