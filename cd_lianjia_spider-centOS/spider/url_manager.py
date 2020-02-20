class UrlManager():
    """core模块，用于管理所有待请求的详情页的URL"""

    def __init__(self):
        self.waiting_urls = set()
        self.processed_urls = set()

    def get_url_set_size(self):
        return len(self.waiting_urls)

    def add_waiting_url(self, url):
        """向集合中添加一条url"""
        if url is not None and url not in self.processed_urls:
            self.waiting_urls.add(url)
        else:
            return None

    def add_waiting_urls(self, url_set):
        """向集合中批量添加url"""
        if url_set is not None and len(url_set) != 0:
            for url in url_set:
                self.waiting_urls.add(url)
        else:
            return None

    def get_new_url(self):
        """从集合中获取一个未请求过的URL"""
        if self.waiting_urls is not None and len(self.waiting_urls) != 0:
            url = self.waiting_urls.pop()
            self.processed_urls.add(url)
            return url
        else:
            return None

    def has_new_url(self):
        """判断是否还有未请求的URL"""
        return self.waiting_urls is not None and len(self.waiting_urls) != 0
