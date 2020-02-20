# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from XiaoShuoSpider.items import XiaoshuospiderItem


class SjzzSpider(CrawlSpider):
    name = 'SJZZ'
    allowed_domains = ['www.ihuiai.com', 'www.ihuiai.com/60/60497/']
    start_urls = ['http://www.ihuiai.com/60/60497/']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.ihuiai.com/60/60497/(.+)\.html'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        title = response.xpath("//div[@class='bookname']/h1/text()").get()
        content = response.xpath("//div[@id='content']/text()").extract()
        content = [x.strip() for x in content]
        content_str = ""
        for i in content:
            content_str += i
        content_str = [content_str]
        yield XiaoshuospiderItem(title=title, content=content_str)
