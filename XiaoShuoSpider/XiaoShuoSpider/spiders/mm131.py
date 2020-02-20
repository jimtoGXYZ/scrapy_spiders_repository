# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from XiaoShuoSpider.items import MM131SpiderItem


class Mm131Spider(CrawlSpider):
    '''
        使用crawlspider貌似无法实现相册翻页，或者是url队列太过于庞大所以一直在爬第一页
        事实证明是能爬到同一个相册的翻页效果但是由于爬取全站的图片导致相册url队列太长
        相册翻页需要很久才能翻到 所以需要等待
        尝试使用scrapyspider手动实现页面爬取
    '''
    name = 'mm131'
    allowed_domains = ['www.mm131.net']
    start_urls = ['https://www.mm131.net/xinggan/']

    rules = (
        Rule(LinkExtractor(allow=r'.+/xinggan/(.+).html'), callback='parse_page', follow=True),
        # Rule(LinkExtractor(allow=r'/d{3,}_./d{1,}.html'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        '''
            use imagePipeline to download pictures which is offer by scrapy-framework
            1.to get titles of each albums
            2.to ge mini-pic's url of each albums
            3.to make an item and yield to imagepipeline
        '''

        title = response.xpath("//div[@class='content']/h5/text()").get()
        url = response.xpath("//div[@class='content-pic']/a/img/@src").get()
        # with open('xx.html','w') as f:
        #     f.write(response.text)
        print('[response page]', title, url ,response.request.headers)
        # image_urls必须接受list对象 所以需要将xpath返回对象改成list
        url_list = []
        url_list.append(url)
        yield MM131SpiderItem(title=title, image_urls=url_list)
