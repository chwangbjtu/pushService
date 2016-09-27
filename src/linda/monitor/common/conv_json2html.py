# -*- coding:utf-8 -*-
import json
import tornado.template

def generate_html(json_data, html_template):
    
    loader = tornado.template.Loader("./common")
    cont = loader.load(html_template).generate(table = json_data)
    
    return cont

if __name__ == '__main__':
    html_template = 'mail_template.html'
    json_data = {'title': u'test', 'date': '192.168.1.1', \
                'header': [u'频道', u'优酷', u'爱奇艺', u'youtube'], \
                'row': [[u'资讯', u'102l', u'0', u'200'], [u'体育', u'22', u'120', u'300']]}
    print json_data
    cont = generate_html(json_data, html_template)
    print cont
