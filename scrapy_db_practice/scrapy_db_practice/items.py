# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDbPracticeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GXRCItem(scrapy.Item):
    job_name = scrapy.Field() #
    campany_name = scrapy.Field() #
    campany_size = scrapy.Field() #
    salary = scrapy.Field() #
    work_place = scrapy.Field() #
    update_time = scrapy.Field() #
    hire_num = scrapy.Field() #
    edu_background = scrapy.Field() #
    experience_requirement = scrapy.Field() #
    campany_nature = scrapy.Field() #
    job_requirement = scrapy.Field() #
    campany_intro = scrapy.Field() #
    linkman = scrapy.Field() #
    phone = scrapy.Field()
    email = scrapy.Field() #
    location = scrapy.Field() #
