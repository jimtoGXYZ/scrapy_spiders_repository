from lxml import etree

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
