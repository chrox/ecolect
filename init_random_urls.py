#!/usr/bin/python 

import redis

server = redis.Redis("localhost")
server.delete("ecolect:start_urls")
server.lpush("ecolect:start_urls", server.srandmember("ecolect_sites:static"))

