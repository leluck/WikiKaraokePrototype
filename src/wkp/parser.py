import xml.dom.minidom
import urllib2

import wkp.article

class ArticleParser:
    def __init__(self, url):
        self.url = url
        self._parse()
    
    def _findElementByAttribute(self, nodelist, attribute, value):
        for node in nodelist:
            if node.nodeType != node.TEXT_NODE:
                if node.getAttribute(attribute) == value:
                    return node
        return None
    
    def _fetchImageAddresses(self, baseNode):
        imgList = []
        images = baseNode.getElementsByTagName('img')
        if len(images) > 0:
            for i in images:
                if i.getAttribute('height') and int(i.getAttribute('height')) > 100 \
                or i.getAttribute('width') and int(i.getAttribute('width')) > 100:
                    imgList.append('http:%s' % (str(i.getAttribute('src'))))
        return imgList
    
    def _getParagraphText(self, node):
        text = ''
        for child in node.childNodes:
            if child.nodeType == child.TEXT_NODE:
                text += str(child.data)
            else:
                text += self._getParagraphText(child)
        return text.encode('utf-8').strip()
    
    def _fetchContent(self, baseNode):
        currentType = 'h1'
        currentName = self.title
        contentList = []
        for n in baseNode.childNodes:
            if n.nodeType != n.ELEMENT_NODE:
                continue
            if n.tagName == 'p':
                contentList.append((currentType, currentName, self._getParagraphText(n)))
            elif n.tagName == 'h2':
                currentType = 'h2'
                for span in n.getElementsByTagName('span'):
                    if span.getAttribute('class') == 'mw-headline':
                        currentName = str(span.firstChild.data).encode('utf-8')
            elif n.tagName == 'h3':
                currentType = 'h3'
                for span in n.getElementsByTagName('span'):
                    if span.getAttribute('class') == 'mw-headline':
                        currentName = str(span.firstChild.data).encode('utf-8')
        return contentList
            
    def _parse(self):
        req = urllib2.Request(self.url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0')
        
        root = xml.dom.minidom.parseString(urllib2.urlopen(req).read().encode('utf-8'))
        content = self._findElementByAttribute(root.getElementsByTagName('div'), 'id', 'mw-content-text')
        if content == None:
            content = self._findElementByAttribute(root.getElementsByTagName('div'), 'class', 'mw-content-ltr')
        
        self.title = str(root.getElementsByTagName('h1')[0].getElementsByTagName('span')[0].firstChild.data).encode('utf-8')
        self.images = self._fetchImageAddresses(content)
        self.content = self._fetchContent(content)
        
    def getArticle(self):
        return wkp.article.Article(self.title, self.content, self.images)