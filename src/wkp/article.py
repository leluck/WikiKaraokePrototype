# -*- coding: utf-8 -*-

import re
import bs4

import wkp.word
import wkp.sentence
import lovelysystems.stemmer as stemmer

class Article:
    def __init__(self, title, content, images):
        self.title = title
        self.content = content
        self.images = images
        
        self._fetchText()
        
        self.words = dict()
        self.sentences = list()
        
        self._analyze()
    
    def __str__(self):
        return self.title
    
    def _fetchText(self):
        self.text = ''
        for element in self.content:
            if not isinstance(element, bs4.element.NavigableString):
                for child in element.find_all('p'):
                    self.text += '%s ' % (child.get_text(strip = False))
        
        pattern = re.compile(r'\[\d+\]')
        self.text = re.sub(pattern, '', self.text) # Strip literature references
    
    def _analyze(self):
        # Scan for all words and count their stem's occurences
        for word in self.text.split():
            stem = stemmer.stem(word)
            try:
                newWord = wkp.word.Word(word)
                self.words[newWord.stem] = newWord
            except wkp.word.WordAlreadyExistsException:
                if stem in self.words.keys():
                    self.words[stem].increment()
                pass
            except wkp.word.WordTooShortException:
                pass
        
        # Weight words (normalization by max occurence)
        topWord = max(self.words.values(), key = lambda w: w.count)
        for word in self.words.values():
            word.calculateImpact(normalization = topWord.count, scaling = 1000)
        
        # Scan for all sentences and calculate sum of their contained words
        pattern = re.compile(r'[^\s\d]{2,}[.!?:]\s|$')
        position = 0
        match = pattern.search(self.text)
        while match is not None and position < len(self.text):
            endPos = match.end()
            sentence = wkp.sentence.Sentence(self.text[position:position + match.end()].strip())
            sentence.calculateImpact(self.words)
            self.sentences.append(sentence)
            match = pattern.search(self.text[position + endPos:])
            position += endPos
        
        self.sentences = sorted(self.sentences, reverse = True)