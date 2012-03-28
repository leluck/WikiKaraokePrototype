
import re

class Article:
    def __init__(self, title, content, images):
        self.title = title
        self.content = content
        self.images = images
        self.ignore = ['Der', 'Die', 'Das', 'Da']
        
        self.wordIndex = None
        self.wordUniques = None
        self.wordWeights = None
        self.sentenceIndex = None
        self.sentenceWeights = None
        
        self._createWordIndex()
        self._weightWords()
        self._createSentenceIndex()
        self._weightSentences()
    
    def __str__(self):
        return self.title
    
    def _createWordIndex(self):
        self.wordIndex = []
        self.wordUniques = []
        tempWordIndex = []
        
        badChars = '.,:;?!()[]'
        for (_, title, text) in self.content:
            tempWordIndex.extend([v.strip(badChars) for v in title.split()])
            tempWordIndex.extend([v.strip(badChars) for v in text.split()])
        for word in tempWordIndex:
            if word.istitle() and word not in self.ignore and len(word) > 2:
                self.wordIndex.append(word)
                if word not in self.wordUniques:
                    self.wordUniques.append(word)
    
    def _createSentenceIndex(self):
        self.sentenceIndex = dict()
        pattern = re.compile(r'[^\s\d]+[.!?:]\s|$')
        for (_, title, text) in self.content:
            absolutePosition = 0
            match = pattern.search(text)
            while match is not None and absolutePosition < len(text):
                sentenceLength = match.end()
                if title not in self.sentenceIndex:
                    self.sentenceIndex[title] = []
                self.sentenceIndex[title].append(text[absolutePosition:absolutePosition + sentenceLength].strip())
                match = pattern.search(text[absolutePosition + sentenceLength:])
                absolutePosition += sentenceLength
    
    def _weightWords(self):
        max = ('', 0.0)
        self.wordWeights = dict()
        for unique in self.wordUniques:
            for word in self.wordIndex:
                if word.find(unique) != -1:
                    if unique in self.wordWeights:
                        self.wordWeights[unique] += 1
                    else:
                        self.wordWeights[unique] = 1
                    if self.wordWeights[unique] > max[1]:
                        max = (unique, self.wordWeights[unique])
        for unique in self.wordWeights:
            self.wordWeights[unique] = (self.wordWeights[unique] * 1000.0) / max[1]
            
    
    def _weightSentences(self):
        self.sentenceWeights = []
        for section in self.sentenceIndex:
            for sentence in self.sentenceIndex[section]:
                sentenceWeight = 0.0
                for word in self.wordUniques:
                    if sentence.find(word) != -1:
                        sentenceWeight += self.wordWeights[word]
                if len(sentence.split()) > 2:
                    sentenceWeight /= float(len(sentence.split()))
                    self.sentenceWeights.append((sentence, sentenceWeight))
            
                
            
            
            
            