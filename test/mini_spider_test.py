#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: mini_spider_test.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/08/30 22:13:34
"""
import os
import re
import sys
import unittest

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import mini_spider
import logging
import Queue
import threading
import time

from lib import log
from lib import conf_parser
from lib import opt_parser
from lib import gl_value
from lib import url_info
from lib import url_handle

class TestMiniSpider(unittest.TestCase):
    """
    Spider class of mini_spider.py test cases
    """
    def setUp(self):
        """
        Before run test, init gloable varibles.
        """
        self.lock = threading.Lock()
        self.url_queue = Queue.Queue()
        self.crawed_urls = set()
        gl_value.URL_LIST_FILE = "./urls"
        gl_value.OUTPUT_DIRECTORY = "./output_here"
        gl_value.MAX_DEPTH = float(8)
        gl_value.CRAWL_INTERVA = 0.1
        gl_value.CRAWL_TIMEOUT = float(1)
        gl_value.THREAD_COUNT = 12
        gl_value.TARGET_URL = ".*.(gif|png|jpg|bmp)$"
        log.init_log('%s/test.log' % gl_value.OUTPUT_DIRECTORY)
        
    def tearDown(self):
        if os.path.exists(gl_value.OUTPUT_DIRECTORY):
            os.system("rm -r %s" % gl_value.OUTPUT_DIRECTORY)
        

    def test_url_queue(self):
        """test url queue when crawed start_url"""
        start_url = 'http://pycm.baidu.com:8081'
        url = url_info.Url(start_url)
        spider = url_handle.UrlHandle(start_url)
        content = spider.get_content()
        if content is not None:
            urls = spider.parse_url(content)
            self.lock.acquire()
            for i in urls:
                add_url = url_info.Url(i,url.depth+1)
                self.url_queue.put(add_url)
            self.assertEqual(4,self.url_queue.qsize())
            self.assertEqual(1,self.url_queue.get().depth)
        self.lock.release()

    def test_thread_work(self):
        """test spider work thread with given start_url"""
        start_url = 'http://pycm.baidu.com:8081'
        url = url_info.Url(start_url)
        self.url_queue.put(url)
        thread = mini_spider.SpiderThread(self.url_queue,self.lock,self.crawed_urls)
        thread.start()
        thread.join()
        self.assertTrue(os.path.exists('output_here/http:__pycm.baidu.com:8081_3_image.jpg'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMiniSpider)
    unittest.TextTestRunner(verbosity=2).run(suite)
