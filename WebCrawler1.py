import urllib2
import re

class JokeCrawler:
    def __init__(self):
        self.page_index = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.enable = False
        self.stories = []

    def getNewPage(self, page_index):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(page_index)
            request = urllib2.Request(url, headers= self.headers)
            response = urllib2.urlopen(request)
            page_html = response.read().decode('utf-8')
            return page_html
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print "Failed to get page, error message: ", e.reason
                return None

    def getPageItems(self, pageIndex):
        page_html = self.getNewPage(pageIndex)
        if not page_html:
            return None
        pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?"content">(.*?)</div>.*?number">(.*?)</.*?number">(.*?)</.',re.S)
        items = re.findall(pattern, page_html)
        pageStories = []
        for item in items:
            haveImage = re.search('img', item[2])
            if not haveImage:
                replace_br = re.compile('<br/>')
                text = re.sub(replace_br,"\n",item[1])
                pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[3].strip()])
        return pageStories

    def preLoadPage(self):
        if self.enable:
            if len(self.stories) < 2:
                page_items = self.getPageItems(self.page_index)
                if page_items:
                    self.stories.extend(page_items)
                    self.page_index += 1

    def getOneStory(self):
        input = raw_input()
        self.preLoadPage()
        if input == 'Q':
            self.enable = False
            return
        print len(self.stories[0])
        print "publisher: %s\tlikes: %s\tcomment: %s \n%s" % (self.stories[0][0], self.stories[0][2], self.stories[0][3], self.stories[0][1])
        del self.stories[0]

    def main(self):
        print 'Press Enter for new message'
        self.enable = True
        self.preLoadPage()
        while self.enable:
            if len(self.stories) > 0:
                self.getOneStory()

crawler = JokeCrawler()
crawler.main()