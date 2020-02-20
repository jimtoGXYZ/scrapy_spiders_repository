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
        # 1.定义每个区需要爬取的列表页长度
        # areas = {'qionglai': 1, 'jinjiang': 100, 'qingyang': 100, 'wuhou': 100, 'chenghua': 100, 'jinniu': 100,
        #          'tianfuxinqu': 100,
        #          'gaoxinxi1': 77, 'shuangliu': 100, 'wenjiang': 100, 'pidou': 100, 'longquanyi': 100, 'xindou': 100,
        #          'tianfuxinqunanqu': 8, 'qingbaijiang': 92, 'doujiangyan': 100, 'pengzhou': 33, 'jianyang': 64,
        #          'xinjin': 50, 'jintang': 42,
        #          'chongzhou1': 3, 'dayi': 1, 'pujiang': 1,
        #          }

        # 成都锦江区
        # areas = {
        #     'chuanshi': 11, 'dongdalu': 8, 'dongguangxiaoqu': 7, 'donghu': 17, 'dongkezhan': 8, 'hejiangting': 26,
        #     'hongxinglu': 9,
        #     'jingjusi': 8, 'jinrongcheng': 35, 'jiuyanqiao': 17, 'langudi': 10, 'lianhua2': 9, 'liulichang': 11,
        #     'panchenggang': 18, 'sanguantang': 9, 'sanshengxiang': 51,
        #     'shahebao': 16, 'shuinianhe': 8, 'yanshikou': 19, 'zhuojincheng': 31,
        # }

        # 成都青羊区
        # areas = {
        #     'babaojie': 17, 'beisen': 19, 'caoshijie': 17, 'caotang': 10, 'funanxinqu': 29, 'guanghuapaoxiao': 16,
        #     'huanhuaxi': 5, 'huapaifang': 22,
        #     'jiaolonggang': 60, 'jinsha': 31, 'jinfu': 11, 'kuanzhaixiangzi': 5, 'renmingongyuan': 12, 'taishenglu': 14,
        #     'waiguanghua': 52,
        #     'waijinsha': 26, 'wanjiawan': 18, 'xinancaida': 17, 'youpindao': 9,
        #
        # }

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
            time.sleep(60 * 8)  # 解析完所有详情页地址后睡眠20分钟
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
                # else:
                # 3.3 解析数据
                try:
                    detail_data = self.parser.get_detail_data(detail_str, id)
                    print(detail_data)
                except Exception as e:
                    print(repr(e))
                    self.log.logger.error('[解析数据异常] {}'.format(repr(e)))
                    continue
                # 3.4 保存数据
                # else:
                try:
                    self.saver.save_csv(detail_data)
                except Exception as e:
                    self.log.logger.error('[3.4 保存数据出错 {}]'.format(repr(e)))
                    continue

                print('[ID]', id)
                id += 1
                stop += 1
                time.sleep(random.choice([0.5, 1, 1.6, 2, 1.8]))
                if stop == 2500:
                    time.sleep(60 * 20)
                    stop = 1


if __name__ == '__main__':
    cd = lianjia_spider()
    cd.run()
