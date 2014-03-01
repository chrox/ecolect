#!/usr/sbin/python
# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
from scrapy import log
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
        self.renderjs = crawler.settings.get("RENDERJS", False)

    def parse(self, response):
        sel = Selector(response)

        for link in sel.xpath('//a'):
            url = link.xpath('@href').extract()
            title = link.xpath('text()').extract()
            if url and title and len(title[0]) > self.title_len:
                yield Request(urljoin(response.url, url[0]), callback=self.ecolect_parse)

        for label in (u'下一页', u'下页', u'后页', u'更多', 'Next', '>', '>>', u'→'):
            next_pages = sel.xpath(u'//a[contains(text(), "%s")]/@href' % label).extract()
            next_pages.extend(sel.xpath(u'//a[@title = "%s"]/@href' % label).extract())
            for next_page in next_pages:
                yield Request(url = urljoin(response.url, next_page), callback=self.parse)

        for script in sel.xpath('//script/text()').extract():
            script_re = re.compile('createPageHTML\((\d+),\s*(\d+),\s*"(.*)",\s*"(.*)"\).*')
            res = script_re.match(script)
            if res:
                params = res.groups()
                count, index, name, ext = int(params[0]), int(params[1]), params[2], params[3]
                if index < count:
                    cur_node = name + "_" + str(index) + "." + ext
                    new_node = name + "_" + str(index + 1) + "." + ext
                    base_url = response.url.replace(cur_node, "")
                    yield Request(url = urljoin(base_url, new_node), callback=self.parse)

        # no next page link? probably we could try to render this page first
        if self.renderjs and "renderjs" not in response.meta:
            response.meta["renderjs"] = 1
            yield Request(response.url, callback=self.parse, meta=response.meta)
    
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

