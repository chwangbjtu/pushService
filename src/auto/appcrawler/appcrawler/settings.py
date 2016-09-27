# -*- coding: utf-8 -*-

# Scrapy settings for appcrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'appcrawler'

SPIDER_MODULES = ['appcrawler.spiders']
NEWSPIDER_MODULE = 'appcrawler.spiders'


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 0.1
CONCURRENT_ITEMS = 400
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 256
CONCURRENT_REQUESTS_PER_IP = 32
DEPTH_LIMIT = 0
DEPTH_PRIORITY = 0
DNSCACHE_ENABLED = True


ITEM_PIPELINES = {
    'appcrawler.pipelines.MysqlStorePipeline': 100,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware' : 100,
    
}

LOG_LEVEL = 'INFO'
