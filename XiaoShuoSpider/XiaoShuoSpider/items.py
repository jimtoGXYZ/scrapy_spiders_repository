# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoshuospiderItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()

class MM131SpiderItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    iamges = scrapy.Field()


class WXappSpiderItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
