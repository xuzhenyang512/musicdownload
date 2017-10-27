#-*-coding:utf-8
#from Tkinter import *
import os
import urllib
import urllib2
import Tkinter
import requests
from __init__ import *


def downLoadFromURL(dest_dir, url):
    try:
        urllib.urlretrieve(url, dest_dir)
        return OK
    except:
        my_println('\tError retrieving the URL:', url)
        return ERROR


def readfile(filename):
    readlines = []
    if os.path.exists(filename):
        file = open(filename, 'r')
        readlines = file.readlines()
        file.close()
    downloadlist = []
    for line in readlines:
        downloadlist.append(json_format(
            line.replace('\n', '').replace('\r', '')))
    return downloadlist


def line():
    str = ""
    for i in range(LINE_WIDTH):
        str += "-"
    return str


def array_print(array, callback):
    index = 1
    my_println(line())
    for e in array:
        callback(index, e)
        my_println(line())
        index += 1


def my_print(*argv):
    str = ""
    for a in argv:
        print a


def my_println(*argv):
    str = ""
    for a in argv:
        print a.encode(g_encode),
    print ""


def kg_print(s1, s2, s3):
    global g_encode
    my_println("{}| {} {}".format("{0: ^6}".format(s1), "{0: <16}".format(
        s2), s3.replace('\n', '').replace('\r', '')[0:50]))


def json_format(name, code="", other=""):
    obj = {}
    obj["name"] = name
    obj["code"] = code
    obj["other"] = other
    return obj


def json_print(index, obj):
    kg_print(index, obj["name"], obj["other"])


def printlistinfo(list):
    array_print(list, json_print)


def getpage(url):
    for i in range(5):
        r = requests.get(url)
        if r.status_code == 200:
            return r.content
        else:
            my_println("requests error :", r.status_code, url)
    return ""

    # return urllib2.urlopen(url).read();
