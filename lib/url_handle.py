#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: lib/url_handle.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/08/16 10:47:21
"""

import os
import logging
import re
import urllib
import urllib2
import urlparse
import time

import chardet
from bs4 import BeautifulSoup

from lib import gl_value

class UrlHandle:
    """Handle url to get,save,parselinks.
    Attributes:
        crawl_timeout: The timeout when open a url.
        out_dir: The output directory for url save.
        target_url: The reg match for crawl target.
        url: The url to handle.
    """
    def __init__(self,url):
        """Inits UrlHandle with global variables"""
        self.crawl_timeout = gl_value.CRAWL_TIMEOUT
        self.init_outdir()
        self.target_url = re.compile(gl_value.TARGET_URL)
        self.url = url

    def init_outdir(self):
        """check out_dir exsits,if not create one"""
        out_dir = os.path.join(os.getcwd(),gl_value.OUTPUT_DIRECTORY)
        if not os.path.isdir(out_dir):
            logging.error("Output dir don't exits %s ,create it" % gl_value.OUTPUT_DIRECTORY)
            try:
                os.mkdir(out_dir)
            except os.error as err:
                logging.error("Mkdir %s error,message is %s" % (out_dir,err))
            return -1
        self.out_dir = out_dir

    def get_content(self):
        """Check if match,then save by urlretrieve.
        returns:
            content: The html content after check match,or None.
        raises:
            URLError: An excption of urllib2,when call urlopen fail.
            UnicodeEncodeError: An excption when met encoding problem.
        """
        if self.target_url.match(self.url):
            try:
                save_name=os.path.join(self.out_dir, self.url.replace('/', '_'))
                urllib.urlretrieve(self.url,save_name)
                logging.info("Saving %s." % self.url)
            except IOError as err:
                logging.error("Saving %s error. Error message: %s." % (self.url,err))
            return None

        try:
            response = urllib2.urlopen(self.url, timeout=gl_value.CRAWL_TIMEOUT)
            content = response.read()
        except urllib2.URLError as err:
            logging.error("Open url %s error. Message: %s." % (self.url,err))
            return None
        except UnicodeEncodeError as err:
            logging.error("Open url %s error. Message: %s." % (self.url,err))
            return None
        except Exception,err:
            logging.error("Open url %s timeout.Message: %s" % (self.url,err))
            return None
            
        if response.getcode() != 200:
            time.sleep(gl_value.CRAWL_INTERVAL)
            return None
        if len(content) == 0:
            return None
        return content

    def parse_url(self, html):
        """Handle encoding and decode.Get all links in html.
        returns:
            page_links: A list object of url links ,or None.
        raises:
            UnicodeEncodeError: An excption when met encoding problem.
            TypeError: An exception when call BeautifulSoup to find links.
        """
        char_dict = chardet.detect(html)
        web_encoding = char_dict['encoding']
        if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
            content = html
        else:
            try:
                content = html.decode('GBK','ignore').encode('utf-8')
            except UnicodeDecodeError as err:
                logging.error("Decode html error. Message: %s.", err)
                return None

        page_links = []
        base_url = self.url.strip('/ ')
        try:
            urls = BeautifulSoup(content).findAll('a', href=True)
            imgs = BeautifulSoup(content).findAll('img', src=True)
        except TypeError as msg:
            logging.error("Type error. Message: %s" % msg)
            return page_links
        except UnicodeDecodeError as msg:
            logging.error("Unicode decode error. Message: %s" % msg)
            return page_links

        links_set = set()
        for link in urls:
            if not link['href'].startswith('javascript:'):
                links_set.add(link['href'])
        for link in imgs:
            links_set.add(link['src'])
        for link in links_set:
            if not link.startswith('http'):
                try:
                    page_links.append(urlparse.urljoin(base_url, link.strip('/')))
                except UnicodeDecodeError as msg:
                    logging.error('Url parse error.Message: %s'% msg)
            else:
                page_links.append(link.strip('/'))
        return page_links
