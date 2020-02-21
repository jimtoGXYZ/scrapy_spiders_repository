from queue import Queue

import requests
import time
import random
import threading

from spider.cd_log import MyLog
from spider.data_saver import DataSaver
from spider.html_downloader import HtmlDownloader
from spider.html_parser import HtmlParser


class lianjia_spider():

    def __init__(self):
        self.item_queue = Queue()
        self.list_page_url_queue = Queue()
        self.list_page_html_queue = Queue()
        self.detail_page_url_queue = Queue()
        self.log = MyLog('lianjia_spider', 'logs')
        self.saver = DataSaver()
        self.html_downloader = HtmlDownloader()
        self.parser = HtmlParser()

    def prepare_list_page(self, areas):
        """
        通过URL拼接将列表页的URL拼接出来,并将其装在list_page_queue里
        :param areas:所要拼接的区的字典
        :return:None
        """
        for area, page_num in areas.items():
            for page in range(1, page_num + 1):
                url = "https://cd.lianjia.com/ershoufang/{}/{}/".format(area, 'pg' + str(page))
                print("拼装URL {} 成功 列表页队列size={}".format(url, self.list_page_url_queue.qsize()))
                self.list_page_url_queue.put(url)

    def multi_thread_parse_list_page(self):
        """
        开启线程执行本函数
        这个函数负责调用下载函数去下载出列表页的html
        :return:None
        """
        print('[列表页下载器]', self.list_page_url_queue.empty())
        # 当列表页URL队列不为空时 可以下载网页
        while True:
            print("[列表页url队列大小：{}]".format(self.list_page_url_queue.qsize()))

            print('[下载列表页HTML线程]', threading.currentThread().name)

            lock = threading.Lock()  # 加锁
            lock.acquire()  # 获取锁 使得多个线程访问queue变为单线程操作

            # 20 分钟还是没有数据则线程销毁
            try:
                list_page_url = self.list_page_url_queue.get(timeout=60 * 20)
            except Exception as e:
                self.log.logger.error('[列表页URL队列等待超过20分钟 ，估计没有需要下载的列表页了 准备正常退出]')
                print('[列表页URL队列等待超过20分钟 ，估计没有需要下载的列表页了 准备正常退出]')
                return

            lock.release()  # 解锁 每个线程获取自己的url后去解析URL

            print("[爬虫 取出列表页URL {}]".format(list_page_url))
            html_str = self.html_downloader.download_html(list_page_url)

            lock.acquire()
            self.list_page_html_queue.put(html_str)
            lock.release()

            self.log.logger.info("[爬虫 列表页 {} HTML放入列表页HTML队列]".format(list_page_url))
            print("[爬虫 列表页 {} HTML放入列表页HTML队列]".format(list_page_url))

    def multi_thread_parse_detail_url(self):
        """
        开启多线程执行本函数
        这个函数负责调用解析函数去解析出列表页中的详情页URL，并将其放入详情页URL队列
        :return:None
        """
        print('[详情页解析器]', self.list_page_html_queue.empty())
        while True:

            lock = threading.Lock()  # 定义锁
            lock.acquire()  # 拿锁=加锁

            try:
                html_str = self.list_page_html_queue.get(timeout=60 * 20)
            except Exception as e:
                self.log.logger.error("[列表页HTML队列等待超过20分钟 估计没有HTML代码需要解析了 准备正常退出]")
                print('[列表页HTML队列等待超过20分钟 估计没有HTML代码需要解析了 准备正常退出]')
                return

            lock.release()  # 解锁

            detail_url_list = self.parser.parse_detail_url_list(html_str)
            if detail_url_list is None or len(detail_url_list) == 0:
                self.log.logger.error("[爬虫 详情页URL列表为空]")
                print("[爬虫 详情页URL列表为空]")
                return

            lock.acquire()
            self.add_to_detail_page_url_queue(detail_url_list)
            lock.release()

            print('[详情页URL队列大小为：{}]'.format(self.detail_page_url_queue.qsize()))

    def multi_thread_parse_detail_html(self):
        """
        开启多线程执行本函数
        这个函数负责从详情页URL队列里取出URL，并调用详情页解析器来解析出item，然后将item放入item队列
        :return:None
        """
        print('[详情页解析器]', self.detail_page_url_queue.empty())
        while True:
            # time.sleep(1)

            lock = threading.Lock()  # 开锁
            lock.acquire()

            try:
                print('[进入获取详情页URL的队列]')
                detail_url = self.detail_page_url_queue.get(timeout=60 * 20)
            except Exception as e:
                self.log.logger.error('[详情页URL队列等待超过20分钟 估计没有URL了 准备正常退出]')
                print('[详情页URL队列等待超过20分钟 估计没有URL了 准备正常退出]')
                return
            lock.release()  # 解锁
            item = self.parser.parse_detail_item(detail_url)

            lock.acquire()
            self.item_queue.put(item)
            lock.release()

    def multi_thread_save(self):
        """
        开启多线程执行本函数
        这个函数负责从item队列中取出item，并调用保存器保存item
        :return:None
        """
        print('[保存器]', self.item_queue.empty())
        while True:
            lock = threading.Lock()  # 拿锁
            lock.acquire()
            print('[item队列大小：{}]'.format(self.item_queue.qsize()))
            try:
                item = self.item_queue.get(timeout=60 * 20)
            except Exception as e:
                self.log.logger.error('[保存器已经等待超过20分钟 估计已经没有item需要保存 准备正常退出]')
                print('[保存器已经等待超过20分钟 估计已经没有item需要保存 准备正常退出]')
                return

            print(item)
            self.saver.save_item(item)
            lock.release()  # 开锁

    def run(self):
        areas = {
            'babaojie': 17, 'beisen': 19, 'caoshijie': 17, 'caotang': 10, 'funanxinqu': 29, 'guanghuapaoxiao': 16,
            'huanhuaxi': 5, 'huapaifang': 22,
            'jiaolonggang': 60, 'jinsha': 31, 'jinfu': 11, 'kuanzhaixiangzi': 5, 'renmingongyuan': 12, 'taishenglu': 14,
            'waiguanghua': 52,
            'waijinsha': 26, 'wanjiawan': 18, 'xinancaida': 17, 'youpindao': 9,
        }

        # 将列表页地址拼接出来放进队列里
        self.prepare_list_page(areas)

        # 开启线程下载列表页
        for i in range(1, 5):
            t = threading.Thread(target=self.multi_thread_parse_list_page, name='parse_list_page_{}'.format(i))
            t.start()

        print('[开启线程下载列表页 准备睡眠 让列表页队列有余量]')
        # time.sleep(60 * 5)
        # 开启线程解析列表页中详情页的URL
        for i in range(1, 5):
            t = threading.Thread(target=self.multi_thread_parse_detail_url, name='parse_detail_url_{}'.format(i))
            print('[开启解析详情页URL的线程]')
            t.start()

        print('[开启线程解析出详情页URL 准备睡眠 让详情页队列有余量]')
        # time.sleep(60 * 5)

        # 开启线程从详情页中解析出item
        for i in range(1, 6):
            t = threading.Thread(target=self.multi_thread_parse_detail_html, name='parse_detail_html_{}'.format(i))
            t.start()

        print('[开启线程下载并解析出item 准备睡眠 让item队列有余量]')
        # time.sleep(60 * 9)

        # 开启线程保存item
        for i in range(1, 3):
            t = threading.Thread(target=self.multi_thread_save, name='save_item_{}'.format(i))
            t.start()

    def add_to_detail_page_url_queue(self, detail_url_list):
        for url in detail_url_list:
            self.detail_page_url_queue.put(url)


if __name__ == '__main__':
    lianjia = lianjia_spider()
    lianjia.run()
