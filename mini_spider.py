#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: mini_spider.py
Author: baidu(baidu@baidu.com)
Date: 2015/08/16 10:47:21
"""

import sys
import getopt
import logging

from lib import log

VERSION="MiniSpider version 1.0"

def usage(ret):
    print '%s \nUsage:  python mini_spider.py -c spider.conf' % VERSION
    sys.exit(ret)

def main():
    log.init_log('./log/spider')
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hvc:")
    except getopt.GetoptError as err:
        logging.error(str(err))
        usage(1)
    for opt,arg in opts:
        if opt == "-v":
            print VERSION
        elif opt == "-h":
            usage(0)
        elif opt == "-c":
            conf = arg
        else:
            logging.error("unrecognized option")
            usage(1)
        


if __name__ == "__main__" :
    main()
