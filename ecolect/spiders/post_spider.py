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

class PostSpider(RedisMixin, CrawlSpider):
    name = "post_spider"
    redis_key = 'ecolect:start_urls'
    start_urls = []

    rules = [
        Rule(SgmlLinkExtractor(), callback = 'parse', follow = False),
    ]

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def __init__(self):
        self.title_keywords = ("(工程|项目)", "第?(一|二|三|首)(次|号)", "(公示|公告)")
        self.line_seps = re.compile('\n|。|；')
        self.head_seps = re.compile('_|( - )|\n|。|；|(>>)')
        self.project_name_exp = re.compile(".*?(关于)?(.*?(项目|工程))")
        self.field_regexps = {
            "project_name": {
                'extract': [
                        (re.compile(".*项目名称：(.*?项目)"), 0),
                    ],
                'hintextract': [
                        (re.compile(".*名称：(.*?项目)"), 0),
                    ],
                'hinting': [
                        re.compile(".*(建设)?.*项目.*"),
                    ],
                },
            "project_address": {
                'extract': [
                        (re.compile(".*(建设|工程)地(点|址)(：)?(.*)"), 3),
                        (re.compile(".*项目位于(.*?)\s.*"), 0),
                        (re.compile(".*项目位于(.*)"), 0),
                        (re.compile(".*(在|于)(.*?路)建"), 1),
                    ],
                'hintextract': [
                        (re.compile(".*地(点|址)(：)?(.*)"), 2),
                        (re.compile(".*(位于|立足)(.*)"), 1),
                    ],
                'hinting': [
                        re.compile(".*(建设)?.*项目.*"),
                    ],
                },
            "project_investment": {
                'extract': [
                        (re.compile(".*投资(.*?)元"), 0),
                        (re.compile(".*投资为(.*?)元"), 0),
                        (re.compile(".*投资(.*)"), 0),
                    ],
                },
            "builder_name": {
                'extract': [
                        (re.compile(".*建设单位(名称)?：(.*?)\s.*"), 1),
                        (re.compile(".*建设单位(名称)?：(.*)"), 1),
                        (re.compile(".*项目业主：(.*)"), 0),
                    ],
                'hintextract': [
                        (re.compile(".*单位(名称)?：(.*?)\s.*"), 1),
                        (re.compile(".*单位(名称)?：(.*)"), 1),
                        (re.compile(".*：(.*?(公司|队|局|厅|部))"), 0),
                        (re.compile("(\s|　)*(.*?(公司|队|局|厅|部))"), 1),
                    ],
                'hinting': [
                        re.compile(".*建设.*单位.*"),
                    ],
                },
            "builder_address": {
                'extract': [
                        (re.compile(".*建设单位(地址|所在地)：(.*?)\s.*"), 2),
                        (re.compile(".*建设单位(地址|所在地)：(.*)"), 2),
                    ],
                'hintextract': [
                        (re.compile(".*(地址|所在地)：(.*?)\s.*"), 1),
                        (re.compile(".*(地址|所在地)：(.*)"), 1),
                    ],
                'hinting': [
                        re.compile(".*建设.*单位.*"),
                    ],
                },
            "eia_name": {
                'extract': [
                        (re.compile(".*(环评|评价|受理).*(机构|单位).?(名称)?：(.*?)\s.*"), 3),
                        (re.compile(".*(环评|评价|受理).*(机构|单位).?(名称)?：(.*)"), 3),
                    ],
                'hintextract': [
                        (re.compile(".*(机构|单位).?(名称)?：(.*?)\s.*"), 2),
                        (re.compile(".*(机构|单位).?(名称)?：(.*)"), 2),
                        (re.compile("(\s|　)*(.*?(院|公司))"), 1),
                    ],
                'hinting': [
                        re.compile(".*环.*评.*(单位|机构).*"),
                        re.compile(".*(评价|反馈|意见).*(机构|单位).*"),
                    ],
                },
            "eia_address": {
                'extract': [
                        (re.compile(".*环.*评.*单位(地址|所在地)：(.*?)\s.*"), 1),
                        (re.compile(".*环.*评.*单位(地址|所在地)：(.*)"), 1),
                    ],
                'hintextract': [
                        (re.compile(".*(地址|所在地)：(.*?)\s.*"), 1),
                        (re.compile(".*(地址|所在地)：(.*)"), 1),
                    ],
                'hinting': [
                        re.compile(".*环.*评.*(单位|机构).*"),
                        re.compile(".*(评价|反馈|意见).*(机构|单位).*"),
                    ],
                },
            "start_date": {
                'extract': [
                        (re.compile(".*(\d\d\d\d(-|/|\.|年)\d\d?(-|/|\.|月)\d\d?(日)?).*"), 0),
                    ],
                },
            "lapse_time": {
                'extract': [
                        (re.compile(".*?起((一|二|三|四|五|六|七|八|九|十|两|\d)+)日.*"), 0),
                        (re.compile(".*?((一|二|三|四|五|六|七|八|九|十|两|\d)+)个?工作日.*"), 0),
                    ],
                },
            "pollutions": {
                'appending': [
                        (re.compile(".*(废气|气体|燃料|火力|化工|天然气|气).*"), u"废气"),
                        (re.compile(".*(废水|化工|纺织|水).*"), u"废水"),
                        (re.compile(".*(废渣|矿|炉|渣|工程).*"), u"废渣"),
                        (re.compile(".*(噪声|铁路|公路|桥梁|机场|声).*"), u"噪声"),
                        (re.compile(".*(粉尘|建材|水泥|炉|尘).*"), u"粉尘"),
                        (re.compile(".*(废.*剂|废.*油|废.*矿|废.*物|废旧)?.*(回收|再生|再利用).*"), u"危废"),
                        (re.compile(".*辐射.*"), u"辐射"),
                    ],
                },
        }
        self.hintings = {}
        self.date_regexp = re.compile(".*([\d零一二三四五六七八九]{4})(-|/|\.|年)([\d零一二三四五六七八九]{1,2})(-|/|\.|月)([\d零一二三四五六七八九]{1,2})(日)?.*")

    def parse(self, response):
        sel = Selector(response)
        item = PostItem()

        # fill page url
        item['url'] = response.url
        # extract page title
        def match_title(title):
            if title is None: return False
            for keyword in self.title_keywords:
                regex = re.compile(".*%s.*" %keyword)
                if not regex.match(title):
                    return False
            return True
        for tag in ("h1", "h2", "h3", "h4", "title", "strong", "b", "p", "span"):
            for heads in sel.xpath("//%s/text()" %tag).extract():
                #for head in heads.strip().encode('utf-8').split(" - "):
                for head in filter(None, self.head_seps.split(heads.encode('utf-8'))):
                    if match_title(head):
                        item['title'] = head.strip()
                        break
        # clean page content
        html = sel.xpath("//html").extract()
        if html:
            content = Document(html[0]).summary()
            item['page_content'] = content.encode('utf-8')
            #print item['page_content']
        if item.get('title') is None:
            print "title not found in this page"
            return
        if item.get('page_content') is None:
            print "content not found in this page"
            return

        #text = HtmlTool.text(html[0]).encode('utf-8')
        text = HtmlTool.text(content).encode('utf-8')
        lines = filter(None, self.line_seps.split(text))
        # try to extract project name from title
        res = self.project_name_exp.match(item['title'])
        if res:
            item["project_name"] = res.groups()[1]
        # project pollutions
        item["pollutions"] = {}
        # extract other fields from page content
        post_lapse_time = None
        self.hinting_results = {}
        # dates occuring in page content
        self.dates = []
        for line in lines:
            def extract_field(field):
                exps = self.field_regexps[field].get("extract", [])
                for exp in exps:
                    result = exp[0].match(line)
                    if result:
                        try:
                            return result.groups()[exp[1]]
                        except:
                            pass
            def hintextract_field(field):
                if field in self.hintings:
                    exps = self.field_regexps[field].get("hintextract", [])
                    for exp in exps:
                        result = exp[0].match(line)
                        if result:
                            try:
                                return result.groups()[exp[1]]
                            except:
                                pass
            def set_field(field):
                def set_extract_field(field):
                    extract_res = extract_field(field)
                    if extract_res:
                        item[field] = extract_res
                        self.hinting_results[field] = False
                        return True
                def set_hintextract_field(field):
                    hintextract_res = hintextract_field(field)
                    if hintextract_res:
                        item[field] = hintextract_res
                        self.hinting_results[field] = True
                        return True
                if not item.get(field):
                    if set_extract_field(field):
                        return True
                    else:
                        return set_hintextract_field(field)
                elif self.hinting_results.get(field):
                    set_extract_field(field)
                    return True
                else:
                    return True
            def append_field(field):
                exps = self.field_regexps[field].get("appending", [])
                for exp in exps:
                    if exp[0].match(line):
                        item[field][exp[1].encode('utf-8')] = 1
            def hinting_fields(fields):
                for field in fields:
                    exps = self.field_regexps[field].get("hinting", [])
                    for exp in exps:
                        if exp.match(line):
                            self.hintings = {}
                            for field in fields:
                                self.hintings[field] = True
                            break

            # set hinting field
            hinting_fields(["project_address"])
            hinting_fields(["builder_name", "builder_address"])
            hinting_fields(["eia_name", "eia_address"])
            # set item fields
            if set_field("project_name"):
                set_field("project_address")
            set_field("project_investment")
            if set_field("builder_name"):
                set_field("builder_address")
            #print self.hintings
            if set_field("eia_name"):
                set_field("eia_address")
            if set_field("start_date"):
                res = self.date_regexp.match(line)
                if res:
                    digits = res.groups()
                    try:
                        self.dates.append(WorkDay(Digit(digits[0]), Digit(digits[2]), Digit(digits[4])))
                    except:
                        pass
            # append fields
            append_field("pollutions")
            # extract fields
            if post_lapse_time is None:
                lapse = extract_field("lapse_time")
                if lapse:
                    post_lapse_time = Digit(lapse)

        # sort all dates occuring in content
        # and the first date must be start date of this project
        # if there is no explicit lapse time we can use the last date as end date of this project
        self.dates = sorted(self.dates)
        if self.dates:
            item["post_start_date"] = str(self.dates[0] + 0)
        if self.dates and post_lapse_time:
            item["post_end_date"] = str(self.dates[0].within(post_lapse_time))
        elif len(self.dates) > 1:
            item["post_end_date"] = str(self.dates[-1] + 0)
        if item.get("project_investment"):
            investment = Digit(item["project_investment"])
            item["project_investment"] = investment if investment > 0 else None
        print "网页标题：", item.get('title')
        print "网页链接：", item.get('url')
        print "项目名称：", item.get("project_name")
        print "项目地址：", item.get("project_address")
        print "项目投资：", item.get("project_investment")
        print "污染类型：", "、".join(item.get("pollutions").keys())
        print "建设单位：", item.get("builder_name")
        print "单位地址：", item.get("builder_address")
        print "环评单位：", item.get("eia_name")
        print "单位地址：", item.get("eia_address")
        print "公告时间：", item.get("post_start_date"), "-", item.get("post_end_date")
        item["page_content"] = None
        yield item

