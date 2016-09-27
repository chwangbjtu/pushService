#!/usr/bin/python
# -*- coding:utf-8 -*-  

import re
import urllib2

import constant

class UrlToId:
    '''
    '''
    
    __56 = "56.com"
    __youku = "youku.com"
    __ku6 = "ku6.com"
    __tudou = "tudou.com"


    def __init__(self):
        '''
        '''
        self.__tudou_content_regax = re.compile(r'[\w\W]*itemData\s*=\s*\{([\w\W]*?)\}[\w\W]*')
        self.__tudou_regax = re.compile(r'[\w\W]*iid\s*[:=]\s*(.*).*')
        self.__youku_regax = re.compile(r'.*/v_show/id_(.*).html.*')		
        self.__ku6_regax = re.compile(r'.*\/(.*).html.*')
        self.__56_regax1 = re.compile(r'.*_vid-(.*)\.html.*')
        self.__56_regax2 = re.compile(r'.*\/v_(.*).html')

        self.__handler = {}
        self.__handler[self.__56] = self.__56id
        self.__handler[self.__youku] = self.__youkuid
        self.__handler[self.__ku6] = self.__ku6id
        self.__handler[self.__tudou] = self.__tudouid


    def __getwebtype(self, urltype):
        if urltype == self.__56:
            return '56'
        elif urltype == self.__youku:
            return 'yk'
        elif urltype == self.__ku6:
            return 'k6'
        elif urltype == self.__tudou:
            return 'td'
        else:
            return ''

    def urlgetid(self, url):
        ''' get the urltype from url
        '''
        (flag, urltype) = self.__judgeurl(url)
        if flag == constant.NOT_EXISTS:
            return (constant.NOT_EXISTS, "", "")
        handler = self.__handler[urltype]
        (flag, id) = handler(url)
        urlwebtype = self.__getwebtype(urltype)
        if urlwebtype == '':
            flag = constant.NOT_EXISTS
        return (flag, urlwebtype, id)

    def __judgeurl(self, url):
        '''judge url  (youku, 56, tudou, ku6 or the other) 
        '''
        for key in self.__handler:
            if url.find(key) != -1:
                return (constant.SUCCESS, key)
        return (constant.NOT_EXISTS, "")

    def __youkuid(self, url):
        '''
        '''
        pattern = "http://v.youku.com/"
        ret = re.match(pattern, url)
        if not ret:
           return (constant.STARTURLERROR, "")
        pattern = ".*/v_show/id_.*"
        ret = re.match(pattern, url)
        if not ret:
           return (constant.ERRORPARAM, "") 
        return self.__regurematch(url, self.__youku_regax)

    def __56id(self, url):
        '''
        '''
        pattern = "http://www.56.com/"
        ret = re.match(pattern, url)
        if not ret:
           return (constant.STARTURLERROR, "")
 
        (flag, id) = self.__regurematch(url, self.__56_regax1)
        if flag == constant.FAIL:
            return  self.__regurematch(url, self.__56_regax2)
        else:
            return (flag, id)


    def __ku6id(self, url):
        '''
        '''
        pattern = "http://v.ku6.com/"
        ret = re.match(pattern, url)
        if not ret:
           return (constant.STARTURLERROR, "")
        return self.__regurematch(url, self.__ku6_regax)


    def __tudouid(self, url):
        '''
        '''
        pattern = "http://www.tudou.com/"
        ret = re.match(pattern, url)
        if not ret:
           return (constant.STARTURLERROR, "")
        (flag, resp) = self.__urlgethtml(url)
        if flag == constant.FAIL:
            return(constant.WEBGETINVALID, "")
        (flag, content) = self.__regurematch(resp, self.__tudou_content_regax)
        if flag == constant.FAIL:
            return (constant.FAIL, "")
        return self.__regurematch(content, self.__tudou_regax)
        
    def __urlgethtml(self, url):
        '''
        '''
        try:
            resp = urllib2.urlopen(url)
            urlcontent = resp.read()			
        except urllib2.URLError:
            return (constant.FAIL, "")
        return (constant.SUCCESS, urlcontent)


    def __regurematch(self, resp, regax):
        content = ""
        flag = constant.SUCCESS
        contentinfo = regax.match(resp)
        if contentinfo == None:
            flag = constant.FAIL
        else:
            content = contentinfo.group(1)
        return(flag, content)


def __test():
    urltoid = UrlToId()


    print 'http://www.56.com/w31/play_album-aid-10899049_vid-ODY5NzAxMTU.html', urltoid.urlgetid("http://www.56.com/w31/play_album-aid-10899049_vid-ODY5NzAxMTU.html")
    print 'http://www.56.com/u80/v_ODY5MTcwNTM.html',  urltoid.urlgetid("http://www.56.com/u80/v_ODY5MTcwNTM.html")
    print 'http://v.youku.com/v_show/id_XNTE1Nzk2NjEy.html', urltoid.urlgetid("http://v.youku.com/v_show/id_XNTE1Nzk2NjEy.html")
    print 'http://v.ku6.com/special/show_6581706/tQrtBRLUxj29KGPM5Sln1A...html', urltoid.urlgetid("http://v.ku6.com/special/show_6581706/tQrtBRLUxj29KGPM5Sln1A...html")
    print 'http://www.tudou.com/programs/view/Pe3XdGdM7jM/?fr=rec2',  urltoid.urlgetid("http://www.tudou.com/programs/view/Pe3XdGdM7jM/?fr=rec2")
    print 'http://www.tudou.com/programs/view/rK9BjW2h6aU/?fr=rec2', urltoid.urlgetid("http://www.tudou.com/programs/view/rK9BjW2h6aU/?fr=rec2")
    print 'http://www.tudou.com/programs/view/sdfsfsfs', urltoid.urlgetid("http://www.tudou.com/programs/view/sdfsfsfs")
    #print urltoid.urlgetid("http://www.aiqiyi.com")
    

if __name__ == "__main__":
   __test() 
