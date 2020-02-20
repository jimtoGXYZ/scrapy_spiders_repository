import pandas as pd

# 读取csv文件
house_df = pd.read_csv("..\\doc\\processed_data\\cd_lianjia-v3_ed.csv", low_memory=False)
# 命名id只跑到37995 但是行数却达到67887
# 按照所有列进行去重比对，只有存在所有列全部一致的才去重
house_df.drop_duplicates(
    subset=['小区名称', '所在区域', '总价', '房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况', '梯户比例',
            '配备电梯', '产权年限', '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '产权所属', '抵押信息', '房本备件', ], inplace=True,
    keep="first")
id_list = []
id_index = house_df["id"]
print(len(id_index))
for i in range(len(id_index)):
    id_list.append(i)
house_df.loc[:, ('id')] = id_list  # 对所有元素的id重新赋值
print(house_df)

house_df.to_csv('..\\doc\\processed_data\\cd_lianjia-v3_ed_nodump.csv', header=True, index=False)  # 将去重后的文件存储
