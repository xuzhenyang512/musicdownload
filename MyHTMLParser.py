#-*-coding:utf-8
from __init__ import *
from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.a_t = False
        self.datas = []

    def handle_starttag(self, tag, attrs):
        if str(tag).startswith("script"):
            self.a_t = True
        # for attr in attrs:
        #    print "属性值：" + attr

    def handle_data(self, data):
        if self.a_t is True:
            self.datas.append(data)
            # print "得到的数据: " + data
    # 处理结束标签，比如</xx>或者<……/>

    def handle_endtag(self, tag):
        self.a_t = False
        # print "结束一个标签:" + tag