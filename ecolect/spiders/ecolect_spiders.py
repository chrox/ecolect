#!/usr/sbin/python
# -*- coding: utf-8 -*-
from urlparse import urljoin
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from rediscrapy.spiders import RedisMixin

from post_spider import PostSpider
from approval_spider import ApprovalSpider

class EcolectSpider(RedisMixin, CrawlSpider):
    #name = 'ecolect_redis'
    #redis_key = 'ecolect:start_urls'
    title_len = 15

    rules = [
        Rule(SgmlLinkExtractor(), callback = 'parse', follow = False),
    ]
    
    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//a')
        for link in links:
            url = link.xpath('@href').extract()
            title = link.xpath('text()').extract()
            if url and title and len(title[0]) > self.title_len:
                yield Request(urljoin(response.url, url[0]), callback=self.ecolect_parse)
        for label in (u'下一页', u'下页'):
            next_page = sel.xpath(u'//a[contains(text(), "%s")]/@href' % label).extract()
            if next_page:
                yield Request(url = urljoin(response.url, next_page[0]), callback=self.parse, dont_filter=False)
    
    def ecolect_parse(self, response):
        pass

class EcolectPost(EcolectSpider):
    name = 'ecolect_posts'
    redis_key = 'ecolect:start_urls'
    spider = PostSpider()

    def ecolect_parse(self, response):
        return self.spider.parse(response)

class EcolectApproval(EcolectSpider):
    name = 'ecolect_approvals'
    redis_key = 'ecolect:start_urls'
    spider = ApprovalSpider()

    def ecolect_parse(self, response):
        return self.spider.parse(response)

