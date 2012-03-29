import re
import bs4

class Article:
    def __init__(self, title, content, images):
        self.title = title
        self.content = content
        self.images = images
        
        self._fetchText()
        
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
    
    def _fetchText(self):
        self.text = ''
        for element in self.content:
            if not isinstance(element, bs4.element.NavigableString):
                for child in element.find_all('p'):
                    self.text += '%s ' % (child.get_text(strip = False))
        
        pattern = re.compile(r'\[\d+\]')
        self.text = re.sub(pattern, '', self.text) # Strip literature references
    
    def _createWordIndex(self):
        self.wordIndex = []
        self.wordUniques = []
            
        badChars = '.,:;?!()[]'
        for word in self.text.split():
            if (word.istitle() and len(word) > 2) or len(word) > 5:
                self.wordIndex.append(word.strip(badChars))
        
        for word in self.wordIndex:
            if word not in self.wordUniques:
                self.wordUniques.append(word)
    
    def _createSentenceIndex(self):
        self.sentenceIndex = []
        
        pattern = re.compile(r'[^\s\d]{2,}[.!?:]\s|$')
        position = 0
        match = pattern.search(self.text)
        while match is not None and position < len(self.text):
            sentenceLength = match.end()
            self.sentenceIndex.append(self.text[position:position + sentenceLength].strip())
            match = pattern.search(self.text[position + sentenceLength:])
            position += sentenceLength
    
    def _weightWords(self):
        max = ('', 0.0)
        self.wordWeights = dict()
        for unique in self.wordUniques:
            for word in self.wordIndex:
                if word.find(unique) != -1:
                    if unique in self.wordWeights:
                        self.wordWeights[unique] += 1.0
                    else:
                        self.wordWeights[unique] = 1.0
                    if self.wordWeights[unique] > max[1]:
                        max = (unique, self.wordWeights[unique])
        for unique in self.wordWeights:
            self.wordWeights[unique] = (self.wordWeights[unique] * 1000.0) / max[1]
    
    def _weightSentences(self):
        self.sentenceWeights = []
        for sentence in self.sentenceIndex:
            weight = 0.0
            for word in self.wordUniques:
                if sentence.find(word) != -1:
                    weight += self.wordWeights[word]
            if len(sentence.split()) > 2:
                weight /= float(len(sentence.split()))
                self.sentenceWeights.append((sentence, weight))
            
                
            
            
            
            