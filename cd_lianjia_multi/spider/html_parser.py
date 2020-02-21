from lxml import etree

from spider.cd_log import MyLog
from spider.html_downloader import HtmlDownloader


class HtmlParser:

    def __init__(self):
        self.downloader = HtmlDownloader()
        self.log = MyLog('HtmlParser', 'logs')
        self.id = 1  # 因为多线程的进入id值可能会重复，需要通过pandas处理

    def parse_detail_url_list(self, html_str):
        """
        负责从列表页的HTML中解析出详情页的URL列表
        :param html_str:
        :return: detail_url_list : list
        """
        if html_str is None or html_str == '':
            self.log.logger.error("[列表页解析器 列表页为空]")
            print("[列表页解析器 列表页为空]")
            return None

        tree = etree.HTML(html_str)
        detail_url_set = set(tree.xpath("//ul[@class='sellListContent']/li/a/@href"))
        if detail_url_set is None:
            self.log.logger.error('[列表页解析器 详情页URL集合为空]')
            return None

        self.log.logger.info('[列表页解析器 详情页URL列表解析成功]')
        return list(detail_url_set)

    def parse_detail_item(self, detail_url):
        """
        负责调用详情页下载器下载详情页HTML，并将HTML解析出item
        :param detail_url:详情页的URL
        :return:item
        """
        if detail_url == '' or detail_url == None:
            self.log.logger.error('[详情页解析器 详情页URL为空 无法解析]')
            print('[详情页解析器 详情页URL为空 无法解析]')
            return

        html_str = self.downloader.download_html(detail_url)
        tree = etree.HTML(html_str)
        transaction_list = tree.xpath("//div[@class='transaction']//ul/li/span/text()")

        item = ['null' for i in range(25)]
        item[0] = 1  # id列固定1 后期用pandas重新排

        communityName = tree.xpath("//div[@class='communityName']/a/text()")[0]
        areaName = tree.xpath("//div[@class='areaName']/span/a/text()")[0]
        price = tree.xpath("//span[@class='total']/text()")[0]
        unitPrice = tree.xpath("//div[@class='unitPrice']/span/text()")[0]
        item[1] = communityName
        item[2] = areaName
        item[3] = price
        item[4] = unitPrice

        content = tree.xpath("//div[@class='base']/div[@class='content']//li/text()")
        if transaction_list[7] == '车库':
            # 按照车库类型解析
            self.parse_car(content, item)

        elif transaction_list[7] == '别墅':
            # 按照别墅类型解析
            self.parse_big_house(content, item)
        else:
            # 按照其他类型解析
            self.parse_nomal(content, item)

        item[17] = transaction_list[1].strip()  # 挂牌时间
        item[18] = transaction_list[3].strip()  # 交易权属
        item[19] = transaction_list[5].strip()  # 上次交易
        item[20] = transaction_list[7].strip()  # 房屋用途
        item[21] = transaction_list[9].strip()  # 房屋年限
        item[22] = transaction_list[11].strip()  # 产权所属
        item[23] = transaction_list[13].strip()  # 抵押信息
        item[24] = transaction_list[15].strip()  # 房本备件


        return item


    def parse_car(self, content, item):
        """
        车库的基本属性只有三个 分别解析出来对应位置放入
        :param tree:
        :param item:item列表
        :return:None
        """
        item[6] = content[0]  # 所在楼层
        item[7] = content[1]  # 建筑面积
        item[11] = content[2]  # 房屋朝向

    def parse_big_house(self, content, item):
        """
        别墅有9个基本属性 但是位置不对 需要手工对应
        :param content:
        :param item:
        :return:
        """
        item[5] = content[0]  # 房屋户型
        item[6] = content[1]  # 所在楼层
        item[7] = content[2]  # 建筑面积
        item[9] = content[3]  # 套内面积
        item[11] = content[4]  # 房屋朝向
        item[12] = content[5]  # 建筑结构
        item[13] = content[6]  # 装修情况
        item[10] = content[7]  # 建筑类型
        item[16] = content[8]  # 产权年限

    def parse_nomal(self, content, item):
        """
        普通住在和商业办公类位置都一样 只是商业办公类多了几个 且并不需要
        :param content:
        :param item:
        :return:
        """
        item[5] = content[0]  # 房屋户型
        item[6] = content[1]  # 所在楼层
        item[7] = content[2]  # 建筑面积
        item[8] = content[3]  # 户型结构
        item[9] = content[4]  # 套内面积
        item[10] = content[5]  # 建筑类型
        item[11] = content[6]  # 房屋朝向
        item[12] = content[7]  # 建筑结构
        item[13] = content[8]  # 装修情况
        item[14] = content[9]  # 梯户比例
        item[15] = content[10]  # 配备电梯
        item[16] = content[11]  # 产权年限
