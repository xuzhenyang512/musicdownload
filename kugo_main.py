#-*-coding:utf-8
from __init__ import *
from kugo_base import *
from MyHTMLParser import *
import json


def printranklist(params={}):
    global g_ranks
    printlistinfo(g_ranks)


def printmusicinfo(params={}):
    global g_music
    printlistinfo(g_music)


def printplist(params={}):
    global g_specials
    printlistinfo(g_specials)


def printdownlist(params={}):
    global g_downlist
    if len(g_downlist) == 0:
        g_downlist = readfile("list")
    printlistinfo(g_downlist)


def foreach_ids(ids, list, fun):
    for id in ids:
        index = int(id)
        if index < 1 or index > len(list):
            continue
        fun(list[index - 1])


def _search(keyword, page=1, dl="N"):
    #my_println(keyword)
    json_dic1 = json.loads(getpage(URLS["search"].format(keyword, page)))
    global g_music
    for item in json_dic1["data"]["lists"]:
        g_music.append(json_format(item["SongName"],
                                   item["FileHash"], item["SingerName"]))
        if dl.upper() == "Y":
            download(item["FileHash"])


def _search_first(keyword, dl="N"):
    #my_println(keyword)
    json_dic1 = json.loads(getpage(URLS["search"].format(keyword, "1")))
    if len(json_dic1["data"]["lists"]) > 0:
        global g_music
        item = json_dic1["data"]["lists"][0]
        g_music.append(json_format(item["SongName"],
                                   item["FileHash"], item["SingerName"]))
        if dl.upper() == "Y":
            download(item["FileHash"])


def search(params):
    keyword = params["k"]
    ids = params["i"]
    global g_music
    g_music = []
    if keyword != "":
        _search(keyword, params["p"], params["d"])
    else:
        filename = params["f"]
        global g_downlist
        if filename != "":
            g_downlist = readfile(filename)
        if len(g_downlist) == 0:
            g_downlist = readfile("list")
        if len(ids) == 0:
            for e in g_downlist:
                _search(e["name"], params["p"], params["d"])
        else:
            foreach_ids(ids, g_downlist, lambda e: _search(
                e['name'], params["p"], params["d"]))
    printlistinfo(g_music)


def search_first(params):
    keyword = params["k"]
    ids = params["i"]
    global g_music
    g_music = []
    if keyword != "":
        _search_first(keyword, params["d"])
    else:
        filename = params["f"]
        global g_downlist
        if filename != "":
            g_downlist = readfile(filename)
        if len(g_downlist) == 0:
            g_downlist = readfile("list")
        if len(ids) == 0:
            for e in g_downlist:
                _search_first(e["name"], params["d"])
        else:
            foreach_ids(ids, g_downlist, lambda e: _search_first(
                e['name'], params["d"]))
    printlistinfo(g_music)


def _download(hash):
    json_dic1 = json.loads(getpage(URLS["download"].format(hash)))
    file_name = json_dic1["data"]["song_name"] + ".mp3"
    dest_dir = os.path.join(g_downloadpath, file_name)
    url = json_dic1["data"]["play_url"]
    my_println("download:", json_dic1["data"]["song_name"],
               json_dic1["data"]["audio_name"], json_dic1["data"]["author_name"])
    downLoadFromURL(dest_dir, url)


def download(params):
    index = params["i"]
    global g_music
    ids = params["i"]
    if len(ids) == 0:
        for e in g_music:
            _download(e["code"])
    else:
        foreach_ids(ids, g_music, lambda e: _download(e["code"]))


def ranklist(params={}):
    json_dic1 = json.loads(getpage(URLS["ranklist"]))
    global g_ranks
    g_ranks = []
    for rank in json_dic1["rank"]["list"]:
        g_ranks.append(json_format(
            rank["rankname"],  rank["rankid"], rank["intro"]))
    printlistinfo(g_ranks)


def _rankinfo(rankid, page=1, dl="N"):
    hp = MyHTMLParser()
    hp.feed(getpage(URLS["rank"].format(page, rankid)))
    hp.close()
    global_features = []
    for data in hp.datas:
        if data.find("global") != -1:
            s_i = data.find("global.features = [") + len("global.features = ")
            e_i = data.find("}];", s_i) + 2
            gloglobal_featuresbal = json.loads(data[s_i: e_i])
    global g_music
    for song in gloglobal_featuresbal:
        g_music.append(json_format(song["FileName"], song["Hash"]))
        if (dl.upper() == "Y"):
            download(song["Hash"])


def rankinfo(params):
    #my_println("tranklistinfo", params)
    global g_ranks
    global g_music
    g_music = []
    ids = params["i"]
    if len(ids) == 0:
        for e in g_ranks:
            _rankinfo(e["code"], params["p"], params["d"])
    else:
        foreach_ids(ids, g_ranks, lambda e: _rankinfo(
            e["code"], params["p"], params["d"]))
    printlistinfo(g_music)


def plist(params):
    json_dic1 = json.loads(getpage(URLS["plist"].format(params["p"])))
    global g_specials
    g_specials = []
    for p in json_dic1["plist"]["list"]["info"]:
        g_specials.append(json_format(
            p["specialname"], p["specialid"], p["intro"]))
    printlistinfo(g_specials)


def _plistinfo(specialid, dl):
    hp = MyHTMLParser()
    hp.feed(getpage(URLS["plistinfo"].format(specialid)))
    hp.close()
    plist = []
    for data in hp.datas:
        if data.find("var data=[{") != -1:
            s_i = data.find("var data=") + len("var data=")
            e_i = data.rfind("}],") + 2
            plist = json.loads(data[s_i: e_i])
    global g_music
    for p in plist:
        g_music.append(json_format(p["songname"], p["HASH"], p["singername"]))
        if (dl.upper() == "Y"):
            download(p["HASH"])


def plistinfo(params={}):
    global g_music
    global g_specials
    g_music = []
    ids = params["i"]
    if len(ids) == 0:
        for special in g_specials:
            _plistinfo(special["code"], params["d"])
    else:
        foreach_ids(ids, g_specials, lambda e: _plistinfo(
            e["code"], params["d"]))
    printlistinfo(g_music)


def exit(params={}):
    return EXIT


def help(params={}):
    for h in g_helps:
        my_println(h.replace("\n", '').replace("\r", ""))
