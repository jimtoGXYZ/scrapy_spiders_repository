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
