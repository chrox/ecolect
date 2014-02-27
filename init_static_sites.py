#!/usr/bin/python 

import redis

r_server = redis.Redis("localhost")
r_server.delete("ecolect_sites:static")
with open("data/static_sites.txt") as sites:
    urls = sites.read().splitlines()
    for url in urls:
        r_server.sadd("ecolect_sites:static", url)

