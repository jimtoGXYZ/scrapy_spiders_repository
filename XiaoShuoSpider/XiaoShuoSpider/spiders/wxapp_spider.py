# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from XiaoShuoSpider.items import WXappSpiderItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://wxapp-union.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+-1.html'), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        title = response.xpath("//div[@class='h hm cl']/div/h1/text()").get()
        author = response.xpath("//div[@class='avatar_right cl']/div/p/a/text()").get()
        time = response.xpath("//div//p[@class='authors']/span/text()").get()
        content_list = response.xpath("//div[@class='content_middle cl']/div[@class='d']/table//td//p/text()").extract()
        content = ""
        for c in content_list:
            content += c.strip()

        yield WXappSpiderItem(title=title, author=author, time=time, content=content)
