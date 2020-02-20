# 链家全站房源爬虫-[成都链家](https://cd.lianjia.com/ershoufang/)
## 大家好，我是W
项目介绍：本项目将使用**模块化的方法**打造一个**爬虫框架**，并**实现链家全站房源的爬虫**。爬虫的目标是每一套房源的关键信息全部采集下来（**包括：小区名称，所在区域，总价，单价，房屋户型，所在楼层，建筑面积，户型结构，套内面积，建筑类型，房屋朝向，建筑结构，装修情况，梯户比例，配备电梯，产权年限，挂牌时间，交易权属，上次交易，房屋用途，房屋年限，产权所属，抵押信息，房本备件**），并将数据存储在csv格式文件上。

项目流程：**项目分析、网站分析、模块设计、代码实现、数据采集**。

项目时间：2020年2月19日

## 项目分析
经过上面的项目介绍我们知道我们要做一个爬虫框架，实际上爬虫本身的内容是很少的一部分，也并不是这次的重点。

### 框架部分分析

既然要做一个简单地爬虫框架，那么他就应该包含以下部分：**日志输出模块、持久化模块、页面下载模块、页面解析模块和最后的爬虫主体逻辑模块**。

简单的说一下理由：

1. **日志输出模块**：用于输出我们爬虫的工作日志，对日常的维护有很大的帮助。有人可能会质疑我们不是有控制台吗？为什么要输出成文件？因为在实际的开发过程中，一个爬虫往往要运行很久，并且会输出很多的log，而我们不可能去一行行的翻控制台。再说云服务器上也没有控制台可以翻，这时需要维护的时候只能翻log，所以说这时一个必须的模块。
2. **持久化模块**：顾名思义就是讲数据进行持久化的模块，本次输出目标是CSV文件，所以持久化模块也是输出到CSV的，若有其他需求可以自行更改。
3. **页面下载模块**：爬虫程序说到底是模拟人的操作去对数据进行提取，而提取的基础是目标页面被我们下载到本地最后进行解析。
4. **页面解析模块**：当页面被下载到本地之后，我们需要通过自己的代码将数据从HTML代码中解析出来，所以将其拆成一个模块。
5. **爬虫主体逻辑模块**：这个模块能够控制我们的爬虫运行的逻辑，也是我们将框架套入其他项目中需要考虑最多的模块。 

所以总的来说搭建一个简单地爬虫框架，就是要将爬虫中负责不同功能的代码抽出来单独做成一个模块，使得在使用的时候达到重复利用的效果，也让程序更符合低耦合高聚合的理念，让开发程序变得像搭积木一样缺什么插什么这样简单。

### 爬虫部分分析

这个链家的爬虫需要爬取的主要是详情页里面的信息，所以前期一切准备都是为了获取到详情页的HTML代码，最后将其进行解析。

同时，经过框架分析我们发现当框架搭建好之后我们的需要改动的地方只有页面解析模块和爬虫主体逻辑模块，因为不同的页面需要不同的解析逻辑，爬虫的主体逻辑也需要适当的变化。


## 网站分析

本次我们要做的就是成都地区的链家二手房全部房源的爬取 - [成都链家](https://cd.lianjia.com/ershoufang/)

### 分析列表页

	https://cd.lianjia.com/ershoufang/
我们发现链家的链接还是比较简洁的，只有一个cd和ershoufang是变量，也就是说我们把cd改成其他城市就可以进入其他城市的列表页了。

那么我们随便点几个页面试试：

1. 首先拉到页面的最底部，试着翻页来查看URL的变化
	
		https://cd.lianjia.com/ershoufang/pg2/
		# 很容易发现后面多了个pg2 多点几页 确实是这个逻辑

2. 点击链家的不同区域，查看URL变化
		
		https://cd.lianjia.com/ershoufang/jinjiang/
		https://cd.lianjia.com/ershoufang/tianfuxinqu/
		# 不同的区，只需要在ershoufang后面加上小区对应的名字就可以了

3. 点击一个区下面的不同小区试试
		
		https://cd.lianjia.com/ershoufang/hangkonggang/
		https://cd.lianjia.com/ershoufang/jiulonghu1/
		# 原来不同大区下的小区也是和2一样的逻辑

4. 对不同的区翻页试试
	
		https://cd.lianjia.com/ershoufang/jinjiang/pg3/
		# 又是在后面加pg页码

5. F12查看一下详情页的URL在哪

		选择器选中小区链家查看
		发现列表页里直接藏有详情页的URL，那就太简单了，直接解析HTML就可以了

到此我们对列表页的研究也差不多了，总结起来就是在不同的区后加页码实现翻页，在ershoufang/后加区名选区。


### 分析详情页

1. 点击进入详情页

		进入详情页发现我们需要的信息全都在里面，只是有的散落在不同的地方，而有的排列整齐在一起。

2. 从列表页分别选择车位、别墅和普通住宅查看


	
		分别点击进入我们会发现，别墅和车位的基本属性信息明显少于普通住宅。

		这时给我们解析详情页带来了不同的思路，是分类别分别解析，还是一起解析然后处理数据，这时值得注意的点。
在知道了信息的位置后，网站分析部分就差不多了。


## 模块设计和代码实现

### 日志输出模块

	import logging
	import datetime


	class MyLog():
    """
    日志输出用于调试
    """

    def __init__(self, name, filepath):
        """初始化属性"""
        # 初始化日志
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 每日生成一个新文件
        filepath = (filepath + "/" + str(datetime.date.today()) + "log.txt")
        self.fh = logging.FileHandler(filepath)
        self.fh.setLevel(logging.DEBUG)

        # 初始化格式器
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def getMyLogger(self):
        return self.logger

这个模块主要用于日志输出，这个模块直接复制就能用也不多解释了，要改就改一改路径和格式化器也可以。

### 持久化模块

	import csv
	from spider import cd_log

	class DataSaver():
    """持久化模块"""

    def __init__(self):
        # 实例化一个log对象 用于日志输出
        self.log = cd_log.MyLog('DataSaver', 'logs')
        # 保存路径
        self.filename = "../doc/origin_data/cd_lianjia-wuhouqu.csv"
        # 在init中写csv表头
        with open(self.filename, 'w', encoding='utf-8', newline='') as f:
            # 根据我们要采集的数据按顺序写好表头列表
            data = [
                "id", "小区名称", "所在区域", "总价", "单价",
                "房屋户型", "所在楼层", "建筑面积", "户型结构",
                "套内面积", "建筑类型", "房屋朝向", "建筑结构",
                "装修情况", "梯户比例", "配备电梯", "产权年限",
                "挂牌时间", "交易权属", "上次交易", "房屋用途",
                "房屋年限", "产权所属", "抵押信息", "房本备件",
            ]
            writer = csv.writer(f, dialect='excel')
            writer.writerow(data)

    def save_csv(self, detail_data):
        """
        保存详情页的信息
        :param detail_data:list类型 存放每一详情页的信息
        :return:None
        """
        # 判空
        if detail_data is None:
            self.log.logger.error('[详情页数据保存失败 数据为空]')
            print('[详情页数据保存失败 数据为空]')
            return

        with open(self.filename, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(detail_data)

        self.log.logger.info("[详情页数据保存成功]")
        print("[详情页数据保存成功]")

如果熟悉scrapy的人可能会觉得这个模块跟scrapy的pipeline差不多，只需要将路径配置好，写好自己的pipeline函数，也就是上面的save_csv就差不多了，但是显然pipeline有统一的对象传入，格式控制的更好，所以需要改进的话可以考虑改进这些。

### 页面下载模块
	
	import random

	import requests

	from spider import cd_log


	class HtmlDownloader():
    """网页下载器"""

    def __init__(self):
        self.log = cd_log.MyLog("HtmlDownloader", "logs")
        self.USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5;",
            "Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)",
            "Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        ]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            "Accept-Encoding": "gzip, deflate, br",
            'Accept-Language': 'zh-CN,zh;q=0.9',
            "Cache-Control": "max-age=0",
            "User-Agent": random.choice(self.USER_AGENTS),
            "Referer": "https://cd.lianjia.com/ershoufang/",
        }

    def download(self, url):
        if url is None:
            self.log.logger.error('[网页下载器 url为空]')
            return None

        response = requests.get(url=url, headers=self.headers)
        if response.status_code != 200:
            self.log.logger.error('[网页下载器 请求失败{}]'.format(response.status_code))
            return None

        self.log.logger.info('[网页下载器 请求成功]')
        print('[网页下载器 请求成功]')
        return response.text

在这个页面下载器模块，我们只需要定义一个download函数，而这个函数中对**URL进行判断**，对**请求进行判断**就可以了，接下来就是简单地将网页download下来后返回给主调函数就可以，可以说是很方便的。

同时，**init函数**中的变量可以自己设置，需要**设置随机UA和IP的可以在这里添加进来**。

当然，如果到后期对这个框架不满意，还可以将其中的UA、headers、IP都抽出来做成配置文件，这就越来越像scrapy框架了。


### 页面解析模块

到了页面解析模块，就跟整个框架的关系变小了，因为这里主要写的是我们的页面解析逻辑，但是他同样作为框架必不可少的一部分存在于框架之中，我们看有什么功能是可以抽出来的。


	from lxml import etree=
	from spider import cd_log
	
	class HtmlParser():
    """解析模块"""

    def __init__(self):
        self.log = cd_log.MyLog('HtmlParser', 'logs')

    def get_detail_urls(self, html_str):
        """
        负责将列表页中存在的详情页解析出来
        :param html_str:列表页HTML
        :return:列表页URL的集合
        """
        if html_str is None:
            self.log.logger.error('[解析列表页错误 列表页为空]')
            print('[解析列表页错误 列表页为空]')
            return
        # 使用集合set可以去重 可迭代
        # 使用xpath解析//ul[@class='sellListContent']/li/a/@href
        tree = etree.HTML(html_str)
        detail_url_set = set(tree.xpath("//ul[@class='sellListContent']/li/a/@href"))
        if detail_url_set is None:
            self.log.logger.error('[xpath解析失败 详情页URL集合为空]')
            return None

        self.log.logger.error('[详情页URL解析成功]')
        return detail_url_set

    def xpath_validating(self, detail_name, xpath_res, detail_data):
        """
        xpath出错处理
        :param detail_name:详情信息名字
        :param xpath_res: xpath结果
        :param detail_data: 返回列表
        :return: None
        """
        if xpath_res is None:
            self.log.logger.error('[解析详情页出错 {} 找不到]'.format(detail_name))
            detail_obj = 'null'
        else:
            self.log.logger.info('[解析{}成功]'.format(detail_name))
            detail_obj = xpath_res
        detail_data.append(detail_obj)

    def get_detail_data(self, detail_str, id):
        if detail_str is None:
            self.log.logger.error('[解析详情页失败 详情页为空]')
            print('[解析详情页失败 详情页为空]')
            return

        detail_data = []  # 最后要返回的数据列表
        detail_data.append(id)

        tree = etree.HTML(detail_str)
        self.xpath_validating('community_name', tree.xpath("//div[@class='communityName']/a/text()")[0], detail_data)
        self.xpath_validating('area', tree.xpath("//div[@class='areaName']//a/text()")[0], detail_data)
        self.xpath_validating('total_price', tree.xpath("//div[@class='price ']/span[@class='total']/text()"), detail_data)
        self.xpath_validating('price', tree.xpath("//div[@class='unitPrice']/span[@class='unitPriceValue']/text()"), detail_data)
        introContent_list = tree.xpath("//div[@class='introContent']//ul/li/text()")
        self.xpath_validating('house_fwhx', introContent_list[0], detail_data)
        self.xpath_validating('house_szlc', introContent_list[1], detail_data)
        self.xpath_validating('house_jjmj', introContent_list[2], detail_data)
        self.xpath_validating('house_hxjg', introContent_list[3], detail_data)
        self.xpath_validating('house_tnmj', introContent_list[4], detail_data)
        self.xpath_validating('house_jjlx', introContent_list[5], detail_data)
        self.xpath_validating('house_fwcx', introContent_list[6], detail_data)
        self.xpath_validating('house_jjjg', introContent_list[7], detail_data)
        self.xpath_validating('house_zxqk', introContent_list[8], detail_data)
        self.xpath_validating('house_thbl', introContent_list[9], detail_data)
        self.xpath_validating('house_pbdt', introContent_list[10], detail_data)
        self.xpath_validating('house_cqnx', introContent_list[11], detail_data)
        transaction_list = tree.xpath("//div[@class='transaction']//ul/li/span/text()")
        self.xpath_validating('house_gpsj', transaction_list[1], detail_data)
        self.xpath_validating('house_jyqs', transaction_list[3], detail_data)
        self.xpath_validating('house_scjy', transaction_list[5], detail_data)
        self.xpath_validating('house_fwyt', transaction_list[7], detail_data)
        self.xpath_validating('house_fwnx', transaction_list[9], detail_data)
        self.xpath_validating('house_cqss', transaction_list[11].strip(), detail_data)
        self.xpath_validating('house_dyxx', transaction_list[13].strip(), detail_data)
        self.xpath_validating('house_fbbj', transaction_list[15], detail_data)

        self.log.logger.info('[3.3 详情页数据解析完成]')
        print('[3.3 详情页数据解析完成]')
        return detail_data


看到这个模块大家可以知道，主要就是两个分别解析列表页和详情页信息的函数，还有一个验证xpath是否能够获取对象的方法。除此之外并没有什么值得我们过分推敲的。

通过传入的HTML代码，然后使用自己有关的css、xpath知识就可以把页面中的对象解析出来，最终将对象返回。


### 爬虫主体逻辑模块

接下来要做爬虫的主体逻辑了，首先我们要明确起始地址是什么，列表页的URL从何处而来，爬取的范围有多少。

起始地址是什么：通过前面的网页分析我们可以知道，**每一个城市对应一个二手房URL**，然后**针对不同的区就会在URL后添加区名**，所以我们的**起始地址完全可以设置为不同的区的URL**。

列表页的URL从何处来：**列表页的URL就是不同的区的URL，在改区的URL下添加pg就可以翻页**。

爬取的范围有多少：针对这个，我们完全**可以使用列表页的页数作为一个区爬取的范围。**当然，如果想要爬取的更细致（因为有的区房源过多，而分页只给我们分了一百页，也就是说超过3000的房源3000套过后的信息我们是无法通过大区翻页获得），就**可以使用区中区的分类方法，进而爬取更细致的列表页**。


这也是这个框架比较弱的一个缺点了，所需要的爬取范围需要我们手工指定。
	
	import random
	import time
	
	from spider import cd_log
	from spider.data_saver import DataSaver
	from spider.html_downloader import HtmlDownloader
	from spider.html_parser import HtmlParser
	from spider.url_manager import UrlManager
	
	
	class lianjia_spider:

    def __init__(self):
        self.log = cd_log.MyLog('lianjia_spider', 'logs')
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.um = UrlManager()
        self.saver = DataSaver()

    def run(self):
        """
            爬虫入口函数
        :return:
        """
        # 成都武侯区
        areas = {
            'caojinlijiao': 22, 'chuanda': 9, 'chuanyin': 14, 'cuqiao': 16, 'dongshengzhen': 41, 'gaopeng': 2,
            'gaoshengqiao': 9,
            'guangfuqiao': 5, 'hangkonggang': 92, 'hongpailou': 20, 'huaxi': 12, 'huochenanzhan': 10, 'lidu': 19,
            'longwan': 9,
            'shuangnan': 22, 'tongzilin': 17, 'waishuangnan': 26, 'wudahuayuan': 37, 'wuhouci': 2, 'wuhoulijiao': 21,
            'xinshuangnan': 16, 'yulin': 11, 'zongbei': 19,
        }

        id = 1
        stop = 1

        # 2.抓取二手房详情页连接，放入URL队列中等待请求
        for area, pg_num in areas.items():
            # 2.1 遍历列表长度，得到详情页URL队列
            for num in range(1, pg_num + 1):
                # 2.1.1 拼接列表页地址
                page_url = "https://cd.lianjia.com/ershoufang/{}/{}/".format(area, 'pg' + str(num))
                self.log.logger.info('[拼接列表页{}成功]'.format(page_url))
                print('[拼接列表页{}成功]'.format(page_url))
                # 2.1.2 启动下载器下载列表页
                try:
                    html_str = self.downloader.download(page_url)
                except Exception as e:
                    self.log.logger.error('[2.1.2 请求页面异常] {}'.format(repr(e)))
                    time.sleep(60 * 30)
                else:
                    # 2.2.1 每请求成功一次列表页，就要解析一次详情页地址
                    try:
                        html_url_list = self.parser.get_detail_urls(html_str)
                    except Exception as e:
                        self.log.logger.error('[2.2.1 解析详情页地址异常] {}'.format(repr(e)))
                    else:
                        self.um.add_waiting_urls(html_url_list)
                        # 每次请求休眠 [1.2,1.4,1.6,1.8,2.0]秒
                        time.sleep(random.choice([1.2, 1.4, 1.6, 1.8, 2.0]))

            print('[随机睡眠]')
            time.sleep(60 * 8)  # 解析完一个大区的地址后就睡眠8分钟 也可以随机睡眠
            print('[苏醒]')
            # 3 解析详情页
            print('[需要解析{}个详情页]'.format(self.um.get_url_set_size()))

            while self.um.has_new_url():
                # 3.1 获取详情页地址
                detail_url = self.um.get_new_url()
                if detail_url is not None:
                    self.log.logger.info('[准备请求地址{}]'.format(detail_url))
                    print('[准备请求地址{}]'.format(detail_url))
                else:
                    self.log.logger.error('[获取详情页地址失败]')
                    print('[获取详情页地址失败]')
                    continue

                # 3.2 下载器下载详情页
                try:
                    detail_str = self.downloader.download(detail_url)
                except Exception as e:
                    print(repr(e))
                    self.log.logger.error("[下载详情页异常] {}".format(repr(e)))
                    self.um.add_waiting_url(detail_url)
                    print('[沉睡20分钟]')
                    time.sleep(60 * 20)
                    print('[苏醒]')
                    continue
               
                # 3.3 解析数据
                try:
                    detail_data = self.parser.get_detail_data(detail_str, id)
                    print(detail_data)
                except Exception as e:
                    print(repr(e))
                    self.log.logger.error('[解析数据异常] {}'.format(repr(e)))
                    continue
                # 3.4 保存数据
                try:
                    self.saver.save_csv(detail_data)
                except Exception as e:
                    self.log.logger.error('[3.4 保存数据出错 {}]'.format(repr(e)))
                    continue

                print('[ID]', id)
                id += 1
                stop += 1
                time.sleep(random.choice([0.5, 1, 1.6, 2, 1.8]))
                if stop == 2500: # 每解析2500条数据睡眠20分钟
                    time.sleep(60 * 20)
                    stop = 1

	
	if __name__ == '__main__':
	    cd = lianjia_spider()
	    cd.run()

我来讲解一下这个模块的逻辑，首先我们会在run方法里定义一个areas字典，改字典就是我们要拼接列表页的范围，也是列表页的来源。
在拼接列表页的过程中同时将列表页下载下来，放入列表页队列里，等待进一步的解析。
经过for循环将字典拼接出来一个区后，会进行8分钟的休眠。

等待休眠结束就会对列表页进行解析，将详情页URL放入队列，从详情页URL中取出URL进行下载，对下载下来的详情页解析出item，交由持久化模块保存。

整体的逻辑很简单，需要注意的是在不同的阶段需要设置相应的睡眠时间，防止目标网站检测。


## 数据采集

数据采集的成果



我们会发现车库和别墅的数据有异样，看来还要进行进一步的处理，但是大家放心，这些数据并不会因此而作废。


## 总结
其实做一个简单地复用爬虫框架其实不难，重点是要把握住爬虫框架的几个部分，将通用的模块抽出来就可以做成一个简单地框架，当然要做成scrapy这样的爬虫框架还是需要很严密的逻辑的。