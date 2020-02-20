# 拉勾网Ajax爬虫 [https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB](https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB")

## 大家好，我是W
项目介绍：本项目为使用requests库实现Ajax的爬虫项目。**项目目标**是将指定关键词下的所有搜索结果的全部信息爬取下来（**包括：职位详情页url，公司全名，公司缩写名，公司规模，行业领域，金融阶段，公司标签，第一标签，第二标签，第三标签，技能标签，职位标签，行业标签，发布时间，城市，地区，薪水，工龄，工作性质，教育背景，职位优势，职位要求**）。本项目流程为：项目分析、网站分析、ajax分析、代码实现、数据提取、数据存储。

## 网站分析
1. 打开拉勾网查看基本信息  [https://www.lagou.com/](https://www.lagou.com/ "https://www.lagou.com/")
2. 点击搜索框搜索爬虫相关职位，可以观察到url为 

	[https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=](https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput= "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=")
	
	显然？后面的参数是无效的，删除回车查看搜索结果（爬虫中文被自动转码）

	[https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB](https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB")

	所以我们请求的URL完全可以使用短的这个版本（非要用长的也ok）

3. 到网页底部试着翻页，**发现URL并没有变化**，可以猜测是**通过ajax进行数据刷新**的，到此我们通过网站分析确定了网站的数据传送方式是ajax，所以**确定了接下来的工作不是请求页面并解析数据**，**而是通过查找拉勾网的ajax请求地址传递参数处理返回来的json字符串**。


## Ajax分析
1. ajax数据的查找
	1. 通过F12同时刷新查看返回来的文件，**一个个的查找数据**。当然查找的**效率太低**了，而且**很多都是没用的图片，js之类的文件**，所以大家使用这个方法**可以着重看文件名有json的文件**。

	2. 通过**勾选选项卡中的XHR**，这意味着**只看json文件**，但是**这种方法会忽略掉很多json文件**，**因为筛的不好**。
	3. **通过```ctrl+F```打开搜索框**，**搜索Ajax|ajax|json 的关键词**，这样很大几率能找到携带页面信息的文件。


	4. 若还是没有找到，可以**尝试复制页面的特定关键词**（即职位特殊信息等等），按照方法3搜索。
	
	以上四种方法基本上能解决ajax数据文件查找问题。
2. 最终我们通过方法2，3，4都找到了文件```positionAjax.json?needAddtionalResult=false```，接下来就需要对请求这个文件的方法进行分析
	1. **点击文件**查看请求响应的**详情**，可以看到**general**下有
	
		**```Request URL: https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false```**
		
		很明显我们**要请求的ajax文件的URL就是这个**

	2. 同时可以看到**第二行**有
	
		**```Request Method: POST```**

		所以我们的请求方式**需要用POST提交**

	3. 在**request headers**下我们可以看到**accept**
	
		**```Accept: application/json, text/javascript, */*; q=0.01```**
		
		所以我们需要添加这一行在headers里，用于接收json文件，若是大家不放心可以多往headers里添加一些参数
	
	4. 现在的网站都有一个**reference**参数来控制我们的请求从何处来，以排除一些粗糙的爬虫（连reference都没有带之类的），所以为了不返工，我们也把reference记下来
		
		**```Referer: https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB```**
	
	5. 在headers里我们可以看到**有一大片的Cookies**，这点很重要，拉勾网**很可能通过生成带有时间戳的cookie来做反爬虫**，不信的话我们可以写一个简单的py文件请求一下，不带cookie返回的是什么
			
			我已经做了，返回的是 {"status":false,"msg":"您操作太频繁,请稍后再访问","clientIp":"你的IP","state":2402}

			Cookie: user_trace_token=20200203223937-2f5bf3e1-7acf-4bb5-929b-bded281e09d4; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221700b7e1b9320f-06c7274cd78945-b383f66-1327104-1700b7e1b94236%22%2C%22%24device_id%22%3A%221700b7e1b9320f-06c7274cd78945-b383f66-1327104-1700b7e1b94236%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A...........

	6. 将**详情卡拉到最下方**，我们可以看到一个**Form Data**，其中有3个参数
		
			first: true # 显然first是用来指定是否是第一页的，是则为true，否则为false
			pn: 1 # pn应该对应的是页码 我们可以多翻几页试试看这个参数会不会变
			kd: 爬虫 # 显然使我们的请求关键字
		所以我们在构造请求的时候需要**用表单请求把这几个参数传上去**
	

自此，我们ajax部分的分析就结束了，其中包括**ajax文件如何查找**，**如何分析ajax请求**，**如何伪造ajax请求**。


## 代码实现
这一part应该是各位同学最喜闻乐见的了，这回我用一个py文件重头到尾的写一下爬虫的流程（主要是scrapy的HTTPFormRequest用不了T.T）

1. 先搭一个框架

		class lagou:

		    def __init__(self):
		        pass
		
		    def run(self):
		        pass


		if __name__ == '__main__':
		    la = lagou()
		    la.run()


2. 在init方法里写上之前分析的header、ajax_url、表单请求参数params

	    def __init__(self):
	        self.headers = {
	            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
	            "Referer": "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB",
	            "Accept": "application/json, text/javascript, */*; q=0.01",
	        }
	        self.ajax_url = 'https://www.lagou.com/jobs/positionAjax.json'
	        self.params = {
	            "first": "true",
	            "pn": 0, # 这两个参数要用代码来改，接下来会说明
	            "kd": "爬虫",
	        }

3. 编写一个负责请求并返回json字符串的函数
	
		def get_json_str(self):
	        response = requests.post(url=self.ajax_url, headers=self.headers, data=self.params) # 在请求中我们没有添加cookie，返回来的result见上
	        json_str = json.loads(response.text)
	        return json_str

4. 经过步骤3，我们知道必须搞来cookie，所以写一个负责请求cookie的函数
	
		def get_cookies(self):
	        cookie_url = "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB" # 请求的地址就是reference
	        session = requests.Session()
	        session.get(url=cookie_url, headers=self.headers)
	        return session.cookies

5. 这时改一个步骤3的函数

	    def get_page_html(self, request_url):
	        response = requests.get(url=request_url, headers=self.headers, cookies=self.get_cookies())
	        print(response.status_code)
	        return response.text
		这回改了正确的params就不会再出错了，但是我们需要实现数据的解析、翻页和存储
		

6. 实现数据解析
	1. 返回来的数据格式（别复制，我把大部分删除了，为了节省文章篇幅）
		
			{'success': True, 'msg': None, 'code': 0, 'content': {'showId': 'fd5d528e1da544a4b5b4ec09e0ad964b', 'hrInfoMap': None, 'pageNo': 1, 'positionResult': {'resultSize': 15, 'result': [{'positionId': 6789054, 'positionName': '爬虫', 'companyId': 348784, 'companyFullName': '杭州知衣科技有限公司', 'companyShortName': '知衣科技', 'companyLogo': 'i/image2/M01/AC/0E/CgoB5lvvmFmAH5P5AAA5-5rnZGE002.png', 'companySize': '50-150人', 'industryField': '移动互联网,电商', 'financeStage': 'A轮', 'companyLabelList': , '大数据+AI'], 'firstType': '开发|测试|运维类', 'secondType': '后端开发', 'thirdType': 'Python', 'skillLables': ['Python', 'python爬虫'], 'positionLabadeDescription': None, 'promotionScoreExplain': None, 'isHotHire': 0, 'count': 0, 'aggregatePositionIds': [], 'famousCompany': True}], 'locationInfo': {'city': None, 'district': None, 'businessZone': None, 'isAllhotBusinessZone': False, 'locationCode': None, 'queryByGisCode': False}, 'queryAnalysisInfo': {'positionName': '爬虫', 'companyName': None, 'industryName': None, 'usefulCompany': False, 'jobNature': None}, 'strategyProperty': {'name': 'dm-csearch-experimentalPositionStrategy', 'id': 0}, 'hotLabels': None, 'hiTags': None, 'industryField': None, 'companySize': None, 'positionName': None, 'totalCount': 189, 'categoryTypeAndName': {'3': '爬虫'}}, 'pageSize': 15}, 'resubmitToken': None, 'requestId': None}

	
		别慌，一大堆数据看起来很乱，但是我们copy到json.cn或者json在线解析工具就会发现其中的结构

			{
				'success': True,
				'msg': None,
				'code': 0,
				'content': {
					'showId': 'fd5d528e1da544a4b5b4ec09e0ad964b',
					'hrInfoMap': None,
					'pageNo': 1,
					'positionResult': {15个职位信息....},
					'pageSize': 15
				},
				'resubmitToken': None,
				'requestId': None
			}
		
		
		其中，在positionResult里还有一个字段```'totalCount': 189,```，显然是搜索结果的职位个数，这个信息可以让我们计算出总页数（因为每页固定15个职位）

	2. 解析每个职位的字典/json
		
			json_str["content"]['positionResult']['result'] # 每个职位的信息
		到这一步我们的爬虫基本上就结束了，因为剩下的就是将字典信息读出来，然后交由MongoDB插入就可以了，但是我们的职位要求存在于详情页中，所以还没完！需要找到json串与详情页URL的关系（因为我们知道整个页面都是json串构造出来的，所以详情页URL也一定在里面）
	3. 查找详情页URL
		
		我们继续按照前面分析ajax的方法分析详情页。
		
		打开详情页 ```https://www.lagou.com/jobs/5960364.html?show=b2cb4a384ec3454f9a93b4c0500d6348``` ，显然后面的show没用，直接删掉。
		
		得到```https://www.lagou.com/jobs/5960364.html```，显然jobs/(\+d).html数字串就是定位串，所以复制5960364到json文件中查找，果然找到```positionId```对应的就是它。
		
		给大家留个小坑，构造URL，然后用xpath解析出来详情（之所以是小坑，那肯定有坑，大家可以想想拉钩需要添加的什么东西在Ajax分析2.5里[太明显了]）

		不会xpath提取的可以学习一下这篇 [https://www.cnblogs.com/xufengnian/p/10788195.html](https://www.cnblogs.com/xufengnian/p/10788195.html "https://www.cnblogs.com/xufengnian/p/10788195.html")

		不会mongodb存储的可以学习一下这篇 [https://blog.csdn.net/qq_26776745/article/details/79560615](https://blog.csdn.net/qq_26776745/article/details/79560615 "https://blog.csdn.net/qq_26776745/article/details/79560615")


7. 计算总页数
	
		def set_page_count(self):
	        json_str = self.get_json_str()
	        if json_str['success']:
	            job_count = json_str['content']['positionResult']['totalCount']
	            self.page_count = job_count / 15 if job_count % 15 == 0 else int(job_count / 15) + 1  # 下取整
	            print('[共{}页]'.format(self.page_count))
		
8. 实现翻页

		def set_request_params(self):
	        if self.params['pn'] < self.page_count:
	            self.params['pn'] += 1
	            if self.params['pn'] != 1:
	                self.params['first'] = 'false'

9. MongoDB存储


		# mongoDB __init__里写
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client['python_scrapy']
        self.collection = self.db['lagou']

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
		


## 完整代码

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


## 总结

本次的Ajax爬虫就到此结束了，回想起刚开始面对ajax的手足无措现在是不是感觉更得心应手。确实ajax好像很吓人，但是只要了解到json文件的搜索，查找规律后，其实对数据的处理部分倒反比不同的页面爬虫更加简单。同时，在爬不同的网站的时候需要注意各个网站的反爬策略，总结起来总会有收获的。