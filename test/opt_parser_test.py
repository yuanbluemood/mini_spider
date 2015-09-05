#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: opt_parser_test.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/09/04 21:37:24
"""
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib import opt_parser

class TestOptParser(unittest.TestCase):
    """test command option Parser
    """
    def setUp(self):
        self.sys_argv = ['mini_spider.py', '-c', 'spider.conf']

    def tearDown(self):
        pass

    def test_opt_parser(self):
        """test opt parser
        """
        conf = opt_parser.opt_parser(self.sys_argv)
        self.assertEqual("spider.conf", conf)

if __name__ == "__main__":
    unittest.main()
