import json
import time

import pymongo
import requests
from lxml import etree


class lagou:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Referer": "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        }
        self.ajax_url = 'https://www.lagou.com/jobs/positionAjax.json'
        self.params = {
            "first": "true",
            "pn": 0,
            "kd": "爬虫",
        }
        self.page_count = 0

        # mongoDB
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client['python_scrapy']
        self.collection = self.db['lagou']

    def set_page_count(self):
        json_str = self.get_json_str()
        if json_str['success']:
            job_count = json_str['content']['positionResult']['totalCount']
            self.page_count = job_count / 15 if job_count % 15 == 0 else int(job_count / 15) + 1  # 下取整
            print('[共{}页]'.format(self.page_count))

    def get_json_str(self):
        response = requests.post(url=self.ajax_url, headers=self.headers, data=self.params, cookies=self.get_cookies())
        json_str = json.loads(response.text)
        return json_str

    def get_cookies(self):
        cookie_url = "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB"
        session = requests.Session()
        session.get(url=cookie_url, headers=self.headers)
        return session.cookies

    def set_request_params(self):
        if self.params['pn'] < self.page_count:
            self.params['pn'] += 1
            if self.params['pn'] != 1:
                self.params['first'] = 'false'

    def get_page_html(self, request_url):
        response = requests.get(url=request_url, headers=self.headers, cookies=self.get_cookies())
        print(response.status_code)
        return response.text

    def get_job_require(self, html):
        tree = etree.HTML(html)
        job_require_list = tree.xpath("//dd[@class='job_bt']/div[@class='job-detail']/p/text()")
        job_require = ""
        for i in job_require_list:
            job_require += i.strip()
        print(job_require)
        return job_require

    def save_in_mongo(self, job_json, job_require):
        job_details = {
            "positionId": job_json["positionId"],
            "companyFullName": job_json["companyFullName"],
            "companyShortName": job_json["companyShortName"],
            "companySize": job_json["companySize"],
            "industryField": job_json["industryField"],
            "financeStage": job_json["financeStage"],
            "companyLabelList": job_json["companyLabelList"],
            "firstType": job_json["firstType"],
            "secondType": job_json["secondType"],
            "thirdType": job_json["thirdType"],
            "skillLables": job_json["skillLables"],
            "positionLables": job_json["positionLables"],
            "industryLables": job_json["industryLables"],
            "createTime": job_json["createTime"],
            "city": job_json["city"],
            "district": job_json["district"],
            "salary": job_json["salary"],
            "workYear": job_json["workYear"],
            "jobNature": job_json["jobNature"],
            "education": job_json["education"],
            "positionAdvantage": job_json["positionAdvantage"],
            "job_require": job_require,
        }
        self.collection.insert_one(job_details)

    def run(self):
        self.set_page_count()  # 设置页码数

        for i in range(self.page_count):  # 遍历所有页
            time.sleep(2)
            self.set_request_params()  # 设置翻页参数
            json_str = self.get_json_str()  # 请求json数据
            print(json_str)
            print("第{}页".format(self.params['pn']))
            for j in json_str["content"]['positionResult']['result']:  # 遍历每一个职位
                time.sleep(1)
                html = self.get_page_html("https://www.lagou.com/jobs/{}.html".format(j['positionId']))
                job_require = self.get_job_require(html)
                self.save_in_mongo(j, job_require)

            # 保存到MongoDB


if __name__ == '__main__':
    la = lagou()
    la.run()
