#!/usr/bin/python 

import redis

r_server = redis.Redis("localhost")
r_server.delete("ecolect:start_urls")
urls = r_server.smembers("ecolect_sites:static")
for url in urls:
    r_server.lpush("ecolect:start_urls", url)

