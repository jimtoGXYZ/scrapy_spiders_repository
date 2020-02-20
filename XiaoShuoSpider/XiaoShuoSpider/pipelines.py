# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.images import ImagesPipeline

from XiaoShuoSpider import settings


class XiaoshuospiderPipeline(object):
    def process_item(self, item, spider):
        print(item['title'])
        print(item['content'])


class MMSpiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        request_objs = super(MMSpiderPipeline, self).get_media_requests(item, info)
        for obj in request_objs:
            obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(MMSpiderPipeline, self).file_path(request, response, info) # 就不需要调用父类的file_path获取uuid定义的path
        title = request.item.get("title")
        # 本来相片的path是由ImagesPipeline的file_path生成uuid生成的 现在用相册名(页码数)自己定义imagepath
        path = title + ".jpg"
        print('[文件名] '+path)
        image_store = settings.IMAGES_STORE

        # 取消文件夹定义 让其放再image下
        # category_path = os.path.join(image_store, title)
        # if not os.path.exists(category_path):
        #     os.mkdir(category_path)

        # 取消full文件夹 直接放再image文件夹下
        image_path = path.replace("full/", "")
        image_path = os.path.join(image_store, path)
        return image_path


class WXappSpiderPipeline(object):

    def __init__(self):
        self.f = open('wxapp.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.f, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        # print(item['title'], item['time'], item['author'], item['content'])
        self.exporter.export_item(item)
        return item

    def close_spider(self):
        self.f.close()
