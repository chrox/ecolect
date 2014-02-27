#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from ecolect.items import PostItem
from rediscrapy.spiders import RedisMixin
from readability.readability import Document

from utils.digit import Digit
from utils.workday import WorkDay
from utils.htmltool import HtmlTool

class ApprovalSpider(RedisMixin, CrawlSpider):
    name = "approval_spider"
    redis_key = 'ecolect:start_urls'
    start_urls = []

    rules = [
        Rule(SgmlLinkExtractor(), callback = 'parse', follow = False),
    ]

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def __init__(self):
        pass

    def parse(self, response):
        pass

