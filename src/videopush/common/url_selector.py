from random import randint

class UrlSelector(object):

    def __init__(self, urls, type=None):
        self.urls = urls
        self.last_url = None
        if type == 'rb':
            self.selector = getattr(self, 'round_robin_url')
        elif type == 'rd':
            self.selector = getattr(self, 'random_url')
        else:
            self.selector = getattr(self, 'random_url')

    def round_robin_url(self):
        num = len(self.urls)
        if num > 0:
            tgt = [i for i, item in enumerate(self.urls) if self.last_url == item]
            if tgt:
                index = (tgt[0] + 1) % num
                self.last_url = self.urls[index]
            else:
                self.last_url = self.urls[0]
            
            return self.last_url

    def random_url(self):
        num = len(self.urls)
        if num > 0:
            index = randint(0, num - 1)
            return self.urls[index]
    
    def get_url(self):
        return self.selector()
    
if __name__ == "__main__":
    url_selector = UrlSelector(['http://www.baidu.com', 'http://www.sina.com.cn', 'http://www.sohu.com', 'http://www.fun.tv'], type='rb')
    for x in xrange(10):
        url = url_selector.get_url()
        print url

    url_selector = UrlSelector(['http://www.qq.com'], type='rb')
    for x in xrange(10):
        url = url_selector.get_url()
        print url


