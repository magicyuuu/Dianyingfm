# -*- coding: utf-8 -*-
__author__ = 'yushiwei'
import unittest
from magicyu.dianyingfm import movie

class testMovie(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):

        pass

    def testInNoneOutEmpty(self):
        result = movie.search("")
        self.assertTrue(result == [])

    def testInHaliboteOut15(self):
        result = movie.search("哈利波特")
        self.assertTrue(result is not None)
        self.assertTrue(len(result) is 17, "数量错误")

    def testInSomeOut2(self):
        self.assertTrue(len(movie.search("匆匆那年")) is 2, "返回数量有误")

    def testInSomeOut20(self):
        self.assertTrue(len(movie.search("H")) is 20, "返回数量有误")

    def testRightData(self):
        results = movie.search("纸牌屋")
        find = False
        name = u'纸牌屋 第一季 TV'
        for result in results:
            if result['name'] == name and result['time'] == 2013:
                find = True
                self.assertTrue(result['douban'] == 9.1)
                self.assertTrue(result['imdb'] == 9.1)
                self.assertTrue(result['types'] == [u'剧情'])
                self.assertTrue(result['actors'] == [u'凯文·史派西', u'罗宾·怀特', u'凯特·玛拉'])
        self.assertTrue(find, u"没有找到: " + name)

    def testInUrlOutMagnet(self):
        results = movie.movieDetail('http://dianying.fm/movie/the-godfather/')
        self.assertTrue(results is not None)
        self.assertTrue(len(results) > 10)

        find = False
        for result in results:
            if result.name == u'教父三部曲1080p@圣城南宫 MKV 60.0 GB':
                find = True
                self.assertTrue(result.video == 'MKV')
                self.assertTrue(result.size == '60.0 GB')
                print result.seed
                self.assertTrue(result.seed == 14)
                self.assertTrue(result.magnet.find(u'magnet:?x') > -1)
                self.assertTrue(result.update == '2012-09-05')
        self.assertTrue(find)
