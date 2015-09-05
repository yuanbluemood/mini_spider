#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: lib/opt_parser.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/09/04 20:05:42
"""
import sys
import getopt

VERSION_INFO="MiniSpider version 1.0 ! "

def usage(msg):
    """
    print help info;then exit.
    """
    print '%s   \nUsage:  python mini_spider.py [-c filename] [-h] [-v]' % msg
    sys.exit(0)

def opt_parser(args):
    """Parser opt from command line.
    Print usage info if needed and return the config filename.
    Args supported is "[-h]:help [-v]:version [-c filename]:configfile"
    Args:
        args: e.g. sys.argv 
    Returns:
        help info if opt is not '-c filename';config filename if '-c filename'
    Raises:
        GetoptError: An exception of getopt module .
    """
    if len(args) == 1:
        usage("Must give one option.")
    try:
        opts,args=getopt.getopt(args[1:],"hvc:")
    except getopt.GetoptError as err:
        usage(err)
    for opt,arg in opts:
        if opt == "-v":
            usage(VERSION_INFO)
        elif opt == "-h":
            usage("")
        elif opt == "-c":
            return arg
        else:
            usage("")
