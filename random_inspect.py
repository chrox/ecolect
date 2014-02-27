#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sys
import redis
import json
import random 

decoder = json.JSONDecoder()
r_server = redis.Redis("localhost")
count = r_server.llen("ecolect_posts:items")
random.seed(int(sys.argv[-1]))
item_str = r_server.lindex("ecolect_posts:items", random.randint(0, count)) 
item = decoder.decode(item_str)

print "网页标题：", item.get('title')
print "网页链接：", item.get('url')
print "项目名称：", item.get("project_name")
print "项目地址：", item.get("project_address")
print "项目投资：", item.get("project_investment")
print "污染类型：", "、".join([pollution.encode('utf-8') for pollution in item.get("pollutions").keys()])
print "建设单位：", item.get("builder_name")
print "单位地址：", item.get("builder_address")
print "环评单位：", item.get("eia_name")
print "单位地址：", item.get("eia_address")
print "公告时间：", item.get("post_start_date"), "-", item.get("post_end_date")

r_server.delete("ecolect:start_urls")
r_server.lpush("ecolect:start_urls", item.get('url'))

