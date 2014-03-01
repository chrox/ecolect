介绍
=======

Ecolect是应用Scrapy爬虫框架编写的环评信息收集程序，可根据提供的种子链接地址抓取网站的环评公示信息。


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
即可启动一个爬虫进程。


并发
==============

不同爬虫进程之间可共用一个种子链接列表和请求队列（存储在Redis数据库中），
使用`parallel`可同时启动多个爬虫进程，提高程序并发性能:
```
    parallel bash -c "scrapy crawl ecolect_posts &" -- {0..3}
```


增量抓取
==============

增量抓取可以在尽量短的时间内收集最新发布的信息。通过Redis数据库持久化Scrapy的过滤器和请求队列，Ecolect甚至可以在异常退出后，重新恢复到上次运行的抓取进度。


获得数据
==============

Ecolect收集的环评公告信息可通过Scrapy的Pipline存储到Mongodb或者其他数据库中。


第三方函数库
==============

本程序使用了许多第三方函数库，比如：
* scrapy_redis (过滤器和请求队列的持久化，实现并发和增量抓取)
* scrapy_mongodb （存储抓取的文档）
* scrapyjs （抓取Javascript生成的页面）
* readability （Html页面正文内容提取）
* htmltool （Html页面文本分行）
* digit （汉语数字到阿拉伯数字的转换）


截图
==============

[![使用1000个种子链接的运行状态：](https://github.com/chrox/ecolect/wiki/screenshots/ecolect_posts_25k_screenshot.png)](https://github.com/chrox/ecolect/wiki/screenshots/ecolect_posts_25k_screenshot.png)
