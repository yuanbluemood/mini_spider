#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: conf_parser_test.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/09/04 21:37:24
"""
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib import conf_parser
from lib import gl_value

class TestConfParser(unittest.TestCase):
    """test conf_parser
    """
    def setUp(self):
        self.conf_file = "spider.conf"
        conf_file_content = \
"""
[spider]
url_list_file: ./urls ; 种子文件路径
output_directory: ../output ; 抓取结果存储目录
max_depth: 8 ; 最大抓取深度(种子为0级)
crawl_interval: 0.1 ; 抓取间隔. 单位: 秒
crawl_timeout: 1 ; 抓取超时. 单位: 秒
target_url: .*.(gif|png|jpg|bmp)$ ; 需要存储的目标网页URL pattern(正则表达式)
thread_count: 12 ; 抓取线程数
"""
        try:
            with open(self.conf_file, "w") as f:
                f.write(conf_file_content)
        except IOError as msg:
            print "Open conf_file to write fail. Message: %s" % msg

    def tearDown(self):
        try:
            if os.path.exists(self.conf_file):
                os.remove(self.conf_file)
        except IOError as msg:
            print "Clear conf_file fail. Message: %s" % msg

    def test_parser(self):
        """test parser
        """
        try:
            conf = conf_parser.conf_parser(self.conf_file)

            self.assertEqual("./urls", gl_value.URL_LIST_FILE)
            self.assertEqual("../output", gl_value.OUTPUT_DIRECTORY) 
            self.assertEqual(float(8), gl_value.MAX_DEPTH)
            self.assertEqual(0.1, gl_value.CRAWL_INTERVAL)
            self.assertEqual(float(1), gl_value.CRAWL_TIMEOUT)
            self.assertEqual(12, gl_value.THREAD_COUNT)
            self.assertEqual(".*.(gif|png|jpg|bmp)$", gl_value.TARGET_URL)

        except ValueError as msg:
            print "Try to read conf fail. Message: %s" %msg

if __name__ == "__main__":
    unittest.main()
