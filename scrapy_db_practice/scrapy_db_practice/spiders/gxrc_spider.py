# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_db_practice.items import GXRCItem


class GxrcSpiderSpider(CrawlSpider):
    name = 'gxrc_spider'
    allowed_domains = ['gxrc.com']
    start_urls = ['https://s.gxrc.com/sJob?posType=5480&workProperty=-1&workAge=1&page=1&pageSize=20']

    rules = (
        # CrawlSpider扫描到的所有详情页都会进入请求队列 同时设置callback为parse_item，对其进行数据提取 ，follow为False，详情页下有其他职位并不符合我们的搜索规则
        Rule(LinkExtractor(allow=r'https://www.gxrc.com/jobDetail/(.+)'), callback='parse_item', follow=True),
        # 编写翻页规则 posType为搜索大类 workProperty为工作性质 workAge为工作年限 pageSize=(\d){1,2}表示1~2位数字均可 page=(\d){1,3}
        # follow=True 即遇见导航栏还存在下一页就翻页 没有callback表示不需要对列表页处理，只需要请求回来交由core分析提取上一个规则的详情页即可
        Rule(LinkExtractor(
            allow=r'https://s.gxrc.com/sJob?posType=5480&workProperty=-1&workAge=1&pageSize=(\d){1,2}&page=(\d){1,3}'),
            follow=True),
    )

    def parse_item(self, response):
        job_name = response.xpath("//*[@class='header']//div[@class='pos-wrap clearfix']/h1/text()").get()
        salary = response.xpath(
            "//*[@class='header']//div[@class='pos-wrap clearfix']/div[@class='salary']/text()").get().strip()
        detail = response.xpath("//*[@class='base-info fl']/p/text()").extract()  # 返回一个list 通过下标选择
        edu_background = detail[1]
        experience_requirement = detail[2]
        hire_num = detail[3]
        campany_name = response.xpath("//div[@class='ent-name']/a/text()").get()
        entDetails = response.xpath("//div[@id='entDetails']/p/span/text()").extract()
        work_place = entDetails[3]
        campany_size = entDetails[1]
        campany_nature = entDetails[0]
        update_time = response.xpath("//span[@class='w3']/label/text()").get().strip()
        job_requirement = response.xpath("//pre[@id='examineSensitiveWordsContent']/text()").get()
        campany_intro = response.xpath("//pre[@id='examineSensitiveWordsContent2']/text()").get()

        contact_info = response.xpath("//div[@class='contact-info-con con']/p/label")
        linkman = contact_info[0].xpath("./text()").get()
        email = contact_info[2].xpath("./text()").get()  # 没有回自动返回None
        location = contact_info[3].xpath("./text()").get()

        # print(job_name, campany_name, campany_intro, salary, job_requirement)

        yield GXRCItem(job_name=job_name, campany_name=campany_name, campany_size=campany_size, salary=salary,
                       work_place=work_place, update_time=update_time, hire_num=hire_num, edu_background=edu_background,
                       experience_requirement=experience_requirement, campany_nature=campany_nature,
                       job_requirement=job_requirement, campany_intro=campany_intro, linkman=linkman, phone=None,
                       email=email, location=location)
