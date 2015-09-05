#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: lib/url_info.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/08/16 17:55:36
"""

class Url:
    """A Url object with url_link and depth.
    Attributs:
        url: A pure url link.
        depth: A number to identify how deep when spider a url.
    """
    def __init__(self,url,depth=0):
        """Inits url variables"""
        self.url = url
        self.depth = depth
