# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql

from scrapy_db_practice import settings


class MysqlPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, db=settings.MYSQL_DB,
                                       user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        print(item['job_name'], item['campany_name'], item['campany_size'], item['salary'], item['work_place'],
              item['update_time'],
              item['hire_num'], item['edu_background'], item['experience_requirement'], item['campany_nature'],
              item['job_requirement'], item['campany_intro'], item['linkman'], item['phone'],
              item['email'], item['location'])

        sql = "insert into " + settings.MYSQL_TABLE + \
              "(job_name,campany_name,campany_size,salary,work_place,update_time,hire_num,edu_background,experience_requirement,campany_nature,job_requirement,campany_intro,linkman,phone,email,location) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            self.cursor.execute(sql, (
                item['job_name'], item['campany_name'], item['campany_size'], item['salary'], item['work_place'],
                item['update_time'],
                item['hire_num'], item['edu_background'], item['experience_requirement'], item['campany_nature'],
                item['job_requirement'], item['campany_intro'], item['linkman'], item['phone'],
                item['email'], item['location']))
            self.connect.commit()
        except Exception as e:
            print(e)
        return item


class MongoDBPipeline(object):

    def __init__(self, uri, db):
        self.mongo_uri = uri
        self.mongo_db = db
        self.mongo_collection = 'gxrc_tech'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(uri=crawler.settings.get('MONGO_URI'), db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = {
            'job_name': item['job_name'],
            'campany_name': item['campany_name'],
            'campany_size': item['campany_size'],
            'salary': item['salary'],
            'work_place': item['work_place'],
            'update_time': item['update_time'],
            'hire_num': item['hire_num'],
            'edu_background': item['edu_background'],
            'experience_requirement': item['experience_requirement'],
            'campany_nature': item['campany_nature'],
            'job_requirement': item['job_requirement'],
            'campany_intro': item['campany_intro'],
            'linkman': item['linkman'],
            'phone': item['phone'],
            'email': item['email'],
            'location': item['location'],
        }

        table = self.db[self.mongo_collection]
        table.insert_one(data)
        return item
