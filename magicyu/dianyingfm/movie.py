# -*- coding: utf-8 -*-
__author__ = 'yushiwei'

import urllib
import urllib2
import os
import sys
import json
import logging
import printer
from pyquery import PyQuery
from collections import namedtuple

BASE_URL = 'http://dianying.fm'

SEARCH_URL = BASE_URL + "/waterfall/key_%s?page=%d"

SEARCH_MAX_SIZE = 20

# 网络请求最大时延
TIMEOUT = 5

MOVIE_ICON = ''

LOG = logging.getLogger("movie")

#
# @{key} string
#
def search(key):
    if key == '' or key == None:
        return []

    result = []
    needBreak = False
    for i in range(1, 10):
        responseData = urllib2.urlopen(urllib2.Request(
            url=SEARCH_URL % (urllib.quote(key), i))
        )
        if responseData.getcode() != 200:
            LOG.error("wrong url:", responseData.geturl())
            return []

        jsonResult = json.loads(responseData.read())
        blocks = PyQuery(jsonResult['html']).items('.x-movie-detail')
        for block in blocks:
            result.append(__parseMovieInfo(block))
            if len(result) >= 20:
                needBreak = True
                break
        if jsonResult['more'] is False or needBreak:
            break
    return result


def __parseMovieInfo(block):
    # 八个属性
    name, time, img, url, douban, imdb, types, actors = None, None, None, None, None, None, None, None

    nameTag = block('.muted').parent().text()
    name = nameTag[0: -6].strip()
    time = int(nameTag[len(name) + 2:-1])

    img = block('img').attr('src')
    url = BASE_URL + block('a:first').attr('href')

    baseInfo = block.items('.x-item-name')
    for info in baseInfo:
        txt = info.parent().text()
        if txt.find(u'评分') > -1:
            sp = txt[4:].split(" ")
            if len(sp) >= 1:
                douban = float(sp[0])
            if len(sp) >= 2:
                imdb = float(sp[1])
        elif txt.find(u'类型') > -1:
            types = txt[4:].split(" / ", 3)
        elif txt.find(u'主演') > -1:
            actors = txt[4:].split(" / ", 3)
    return {
        'name': name,
        'time': time,
        'img': img,
        'url': url,
        'douban': douban,
        'imdb': imdb,
        'types': types,
        'actors': actors
    }


MovieData = namedtuple('MovieData', ['name', 'size', 'video', 'magnet', 'update', 'seed'])


def movieDetail(movieUrl):
    if movieUrl is None or movieUrl == '':
        return []
    try:
        response = urllib2.urlopen(url=movieUrl, timeout=5)
    except urllib2.URLError as e:
        LOG.error(e)
        return []
    if response.getcode() != 200:
        return []

    results = []
    resources = PyQuery(response.read()).items('.resources')
    for resource in resources:
        sizeTag = resource.find('span.muted')
        size = sizeTag.text()
        video = sizeTag.prev().text()
        name = sizeTag.parent().text()

        magnetTag = resource.find('a.btn.btn-mini.x-tooltip')
        magnet = magnetTag.attr('href')

        # 上传时间: 2011-02-09, 种子数: 84 <br> 右键复制磁力链接
        seedInfo = magnetTag.attr('title')
        update, seed = None, None

        betweenResult = __between(seedInfo, u'上传时间: ', u', 种子')
        if betweenResult[0]:
            update = betweenResult[1]
        betweenResult = __between(seedInfo, u'种子数: ', u' <br>')
        if betweenResult[0]:
            seed = int(betweenResult[1])

        results.append(MovieData(
            name=name,
            size=size,
            video=video,
            magnet=magnet,
            update=update,
            seed=seed
        ))
    for r in results:
        print r
    return results

def __between(str, start, end):
    startIndex = str.find(start)
    if startIndex > -1:
        endIndex = str.find(end)
        if endIndex > -1:
            return (True, str[startIndex + len(start):endIndex])
    return (False, None)


def showSearch(results):
    p = printer.Printer()
    for r in results:
        title = r['name']
        subtitle = '%s年 Douban:%s IMDB:%s 类型:%s 主演:%s' % (
            r['time'],
            r['douban'],
            r['imdb'],
            ','.join(r['types']),
            '/'.join(r['actors'])
        )
        arg = r['url']
        p.add_item(title=title, subtitle=subtitle, arg=arg, valid=True, icon=MOVIE_ICON)
    p.end()


def showDetail(results):
    p = printer.Printer()
    for r in results:
        title = r.name
        subtitle = '格式:%s 时间:%s 种子:%d 大小:%s' % (
            r.video,
            r.time,
            r.seed,
            r.size
        )
        arg = r.magnet
        p.add_item(title=title, subtitle=subtitle, arg=arg, valid=True, icon=MOVIE_ICON)
    p.end()
    pass
