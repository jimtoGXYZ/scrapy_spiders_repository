import csv

from spider import cd_log


class DataSaver():
    """持久化模块"""

    def __init__(self):
        self.log = cd_log.MyLog('DataSaver', 'logs')
        self.filename = "../doc/origin_data/cd_lianjia-qingyangqu4.csv"
        with open(self.filename, 'w', encoding='utf-8', newline='') as f:
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

    def save_item(self, detail_data):
        if detail_data is None:
            self.log.logger.error('[保存器 数据为空保存失败]')
            print('[保存器 数据为空保存失败]')
            return

        with open(self.filename, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(detail_data)

        self.log.logger.info("[保存器 详情页数据保存成功]")
        print("[保存器 详情页数据保存成功]")
