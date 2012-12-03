# -*- coding: utf-8 -*-

import os
import re

from urllib import FancyURLopener

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
        self.storedImages = list()
        
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
        print('Analyzing article...')
        
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
        
    def downloadImages(self, overwrite = False):
        print('Downloading article images...')
        
        targetdir = '../tmp'
        if not os.path.isdir(targetdir):
            os.mkdir(targetdir)
        
        imagecount = 0
        for url in self.images:
            imagecount += 1
            parts = url.split('/')
            if 'thumb' in parts:
                # Remove mid-string 'thumb' and last part, as they refer to the resized 
                # version of a wikipedia image
                parts.remove('thumb')
                parts.remove(parts[-1])
                url = '/'.join(parts)
            
            safename = ''.join([c for c in self.title.lower() if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
            filename = '%s_%03d.%s' % (safename.replace(' ', '-'), imagecount, parts[-1].split('.')[-1])
            fullpath = os.path.join(targetdir, filename)
            
            self.storedImages.append(fullpath)
            if os.path.isfile(fullpath):
                if overwrite:
                    os.remove(fullpath)
                else:
                    continue
            
            opener = ImageDownloader()
            opener.retrieve(url, fullpath)

class ImageDownloader(FancyURLopener):
    version = '(Linux; U; Android 2.2.1; de-DE) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'