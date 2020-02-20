"""
    2020年2月17日15:44:53
    按照不同的小区进行分类并计算小区总价平均值
    使用plt进行数据展示

"""

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

from_path = "..\\doc\\processed_data\\cd_lianjia-v3_ed.csv"
to_path = "..\\doc\\pic\\area_mean_price.png"
# 读取数据 类型dataframe
df = pd.read_csv(from_path)
# 设置所在区域为大索引
df.set_index(['所在区域'], inplace=True)
# 根据所在区域做聚集操作
groupby_obj = df.groupby("所在区域")
# 根据所在区域算出总价的平均值
total_list = groupby_obj.mean()["总价"]
print(total_list)
# 取出索引作为标签
total_index_list = total_list.index
print(total_list, total_index_list)
# 设置刻度
y_ticks = range(len(total_index_list))
x_ticks = range(0, 260, 10)
# 打开画布
plt.figure(figsize=(20, 9), dpi=80)
# 设置柱子
plt.barh(y=y_ticks, width=total_list, height=0.2, color='orange')
# 设置y轴刻度
plt.yticks(ticks=y_ticks, labels=total_index_list)
# 设置x轴刻度
plt.xticks(ticks=x_ticks)

# 增加标签
plt.xlabel("区域平均价格(单位：万元)")
plt.ylabel("区域名称")
plt.title("成都2020年2月份各区平均房价一览图")

# 打开网格
plt.grid()
# 保存图片
plt.savefig(to_path)
# 展示图片
plt.show()
