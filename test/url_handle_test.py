#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: url_handle_test.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/09/04 21:37:24
"""
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib import url_handle
from lib import gl_value
from lib import log

class TestUrlHandle(unittest.TestCase):
    """test module url_handle
    """
    def setUp(self):
        self.url = "http://pycm.baidu.com:8081"
        self.out_dir = "output_here"
        self.url_content = \
"""<!DOCTYPE html>
<html>
    <head>
        <meta charset=utf8>
        <title>Crawl Me</title>
    </head>
    <body>
        <ul>
            <li><a href=page1.html>page 1</a></li>
            <li><a href="page2.html">page 2</a></li>
            <li><a href='page3.html'>page 3</a></li>
            <li><a href='mirror/index.html'>mirror</a></li>
            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
        </ul>
    </body>
</html>

"""
        gl_value.URL_LIST_FILE = "./urls"
        gl_value.OUTPUT_DIRECTORY = "../output"
        gl_value.MAX_DEPTH = float(8)
        gl_value.CRAWL_INTERVA = 0.1
        gl_value.CRAWL_TIMEOUT = float(1)
        gl_value.THREAD_COUNT = 12
        gl_value.TARGET_URL = ".*.(gif|png|jpg|bmp)$"
        log.init_log('%s/test.log' % gl_value.OUTPUT_DIRECTORY)

    def tearDown(self):
        try:
            if os.path.exists(self.out_dir):
                os.system("rm -r %s" % self.out_dir)
        except IOError as msg:
            print "Clear conf_file fail. Message: %s" % msg

    def test_init_outdir(self):
        """test init outdir"""
        gl_value.OUTPUT_DIRECTORY = self.out_dir
        url_handle.UrlHandle(self.url)
        self.assertTrue(os.path.exists('output_here'))

    def test_get_content(self):
        """test get content of url if not match reg"""
        gl_value.OUTPUT_DIRECTORY = self.out_dir
        content = url_handle.UrlHandle(self.url).get_content()
        self.assertEqual(content,self.url_content)

        """test saving img when match reg """
        self.url = 'http://img1.money.126.net/chart/hk/time/210x140/HSI.png'
        content = url_handle.UrlHandle(self.url).get_content()
        self.assertTrue(os.path.exists('output_here/http:__img1.money.126.net_chart_hk_time_210x140_HSI.png'))

    def test_parse_url(self):
        """test url list return"""
        url_handler = url_handle.UrlHandle(self.url)
        content = url_handler.get_content()
        url_links = url_handler.parse_url(content)
        pre_links = [u'http://pycm.baidu.com:8081/mirror/index.html', u'http://pycm.baidu.com:8081/page2.html', u'http://pycm.baidu.com:8081/page1.html', u'http://pycm.baidu.com:8081/page3.html']
        self.assertEqual(url_links,pre_links)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUrlHandle)
    unittest.TextTestRunner(verbosity=2).run(suite)
