#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: lib/conf_parser.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/09/04 20:01:13
"""
import os
import logging
import ConfigParser

from lib import gl_value

def conf_parser(conf_file):
    """Parse the conf file 
    Call gl_value to init global variable.Then cover it.
    Call ConfigParser.ConfigParser to read config info, set global variables.
    Args:
        conf_file: A file with all config info for spider work.
    Returns:
        The status of parser result.
    Raises:
        ValueError: an exception of configParser
    """
    if not os.path.exists(conf_file):
        logging.error("Config file %s do not exist!" % conf_file)
        return -1
    config = ConfigParser.ConfigParser()
    config.read(conf_file)

    try:
        gl_value.URL_LIST_FILE = config.get('spider','url_list_file')
        gl_value.OUTPUT_DIRECTORY = config.get('spider','output_directory')
        gl_value.MAX_DEPTH = float(config.get('spider','max_depth'))
        gl_value.CRAWL_INTERVAL = float(config.get('spider','crawl_interval'))
        gl_value.CRAWL_TIMEOUT = float(config.get('spider','crawl_timeout'))
        gl_value.TARGET_URL = config.get('spider','target_url')
        gl_value.THREAD_COUNT = int(config.get('spider','thread_count'))
        logging.info("Read global values from %s successfully" % conf_file)
        return 0
    except ValueError as err:
        logging.error("Read global value error, Error message: %s ", err)
        return -1
