# Scrapy settings for ecolect project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ecolect'

SPIDER_MODULES = ['ecolect.spiders']
NEWSPIDER_MODULE = 'ecolect.spiders'

CONCURRENT_REQUESTS = 100
LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 15
REDIRECT_ENABLED = False
AJAXCRAWL_ENABLED = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ecolect (+http://www.yourdomain.com)'

SCHEDULER = "rediscrapy.scheduler.Scheduler"
SCHEDULER_PERSIST = True
#SCHEDULER_QUEUE_CLASS = "rediscrapy.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "rediscrapy.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "rediscrapy.queue.SpiderStack"

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'ecolect_items'
MONGODB_UNIQUE_KEY = 'url'

ITEM_PIPELINES = {
    'ecolect.pipelines.EcolectPipeline': 100,
    'rediscrapy.pipelines.RedisPipeline': 300,
    'scrapy_mongodb.MongoDBPipeline': 500,
}

EXTENSIONS = {
    'scrapy.contrib.corestats.CoreStats': 500,
    'scrapy.webservice.WebService': 500,
}
