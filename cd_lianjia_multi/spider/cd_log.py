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
