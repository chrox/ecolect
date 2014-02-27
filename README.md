介绍
=======

Ecolect是应用Scrapy爬虫框架编写的环评信息收集程序，可根据提供的种子链接地址抓取网站的环评公式信息。


安装
==============

程序依赖以下程序库：
* scrapy
* redis/redispy
* mongodb/pymongo

运行
==============

启动redis和mongodb数据库服务后，
在ecolect根目录下运行：
```
    ./init_static_sites.py
    ./init_start_urls.py
```
初始化种子链接地址。

运行：
```
    scrapy crawl ecolect_posts
```
即可启动一个爬虫进程。可同时启动多个爬虫进程，提高程序并发性能。

增量抓取
==============

环评信息发布网站的内容实时更新，增量抓取可以在尽量短的时间内收集最新发布的信息。

获得数据
==============

Ecolect收集的环评公告信息可通过Scrapy的Pipline存储到Mongodb或者其他数据库中。
