#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: mini_spider.py
Author: liuchangfu(liuchangfu@baidu.com)
Date: 2015/08/16 10:47:21
"""

import os
import sys
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

class SpiderThread(threading.Thread):
    """Spider's main working thread.

    SpiderThread object will get one url from url_queue each time.
    Then call url_handle.UrlHandle to get_content ,save imgs, parse links.
    After crawed this url ,put it to crawed_urls set.

    Attributes:
        url_queue: A queue to put urls to crawl.
        lock: A thread lock for global variable r/w.
        crawed_urls: A set for crawled urls in case of dulplicate crawl.
    """
    def __init__(self,url_queue,lock,crawed_urls):
        """Init attributes of SpiderThread"""
        super(SpiderThread, self).__init__()
        self.url_queue = url_queue
        self.lock = lock
        self.crawed_urls = crawed_urls

    def run(self):
        """run method of SpiderThread"""
        while True:
            self.lock.acquire()
            if not self.url_queue.empty():
                url = self.url_queue.get()
                self.lock.release()
                if url.depth >= gl_value.MAX_DEPTH:
                    logging.info("Url %s has reach max depth %s" ,url.url, gl_value.MAX_DEPTH)
                    self.url_queue.task_done()
                    continue
                elif url.url in self.crawed_urls:
                    logging.info("Url %s has crawed" ,url.url)
                    self.url_queue.task_done()
                    continue
    
                """get_content(save if match reg)£¬parse_links(need depth+1)"""
                spider = url_handle.UrlHandle(url.url)
                content = spider.get_content()
                if content is not None:
                    urls = spider.parse_url(content)
                    self.lock.acquire()
                    for i in urls:
                        add_url = url_info.Url(i,url.depth+1)
                        self.url_queue.put(add_url)
                    self.lock.release() 
    
                logging.info("Url %s has crawed,current depth:%s" % (url.url,url.depth))

                self.lock.acquire()
                self.crawed_urls.add(url.url)
                self.lock.release()

                time.sleep(gl_value.CRAWL_INTERVAL)
                self.url_queue.task_done()
            else:
                self.lock.release()
                logging.info("Url queue now is empty,thread quit!" )
                break

def main():
    """main func:
    parse sys.argv firstly,and read conf to set global variable.
    start threads by conf to spider,then stop thread when over.
    """
    log.init_log('./log/spider') 

    conf = opt_parser.opt_parser(sys.argv)

    """init global variables"""
    try:
        conf_parser.conf_parser(conf)
    except UnboundLocalError as msg:
        logging.error("Read conf fail. Message: %s" % msg)
        return

    """init queue by url file"""
    lock = threading.Lock()
    url_queue = Queue.Queue()
    crawed_urls = set()
    try:
        fp = open(gl_value.URL_LIST_FILE)
    except IOError as msg:
        logging.error("Open url file %s fail. Message: %s" % (gl_value.URL_LIST_FILE,msg))
        return
    for start_point in fp.readlines():
        if not start_point.startswith('http'):
            break
        start_url = url_info.Url(start_point.strip('/\n\r'))
        url_queue.put(start_url)

    threads = []
    """start thread"""
    for i in xrange(gl_value.THREAD_COUNT):
        thread = SpiderThread(url_queue,lock,crawed_urls)
        threads.append(thread)
        time.sleep(1)
        thread.start()
        logging.info("Staring spider thread...")

    """stop thread"""
    for thread in threads:
        thread.join()
    logging.info("Spider work is done!")
    print "Spider work is done!"

if __name__ == "__main__" :
    main()
