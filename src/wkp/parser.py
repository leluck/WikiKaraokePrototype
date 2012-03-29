import urllib2
from bs4 import BeautifulSoup

import wkp.article

class ArticleParser:
    def __init__(self, url):
        self.url = url
        self._parse()
            
    def _parse(self):
        req = urllib2.Request(self.url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 2.2.1; de-DE) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
        soup = BeautifulSoup(urllib2.urlopen(req).read().encode('utf-8'))
                
        self.content = soup.find(id = 'mw-content-text').parent.contents
        self.title = soup.find('h1').find('span').string
        self.images = []
        for img in soup.find_all('img'):
            if int(img.get('height')) > 100 and int(img.get('width')) > 100:
                self.images.append('http:%s' % (img.get('src')))
        
    def getArticle(self):
        return wkp.article.Article(self.title, self.content, self.images)