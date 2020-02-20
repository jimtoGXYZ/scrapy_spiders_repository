# --coding:UTF-8--


import csv

file_path = '..\\doc\\origin_data\\cd_lianjia-v3.csv'
to_path = '..\\doc\\processed_data\\cd_lianjia-v3_ed.csv'

with open(file_path, encoding='utf-8') as f:
    reader = csv.reader(f)
    content = [line for line in reader]

# print(content)  # [[], [],]

with open(to_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for line in content:
        line = [i.strip() for i in line]  # 处理空串问题
        line = [i.replace("['", "").replace("']", "") for i in line]  # 处理总价和单价的['']
        if line[0] == 'id':
            writer.writerow(line)
            continue

        if line[3] == '' or line[3] == '[]':
            continue

        if '别墅' in line:
            newline = line[:]
            # 别墅数据异常 7建筑面积,8户型结构,9套内面积 中间差一个户型结构
            for i in range(13, 7, -1):  # 给户型结构挪位置
                line[i + 1] = line[i]
            line[8] = 'null'  # 户型结构放入
            # 套内面积", "建筑类型", "房屋朝向" 少一个建筑类型
            for i in range(15, 9, -1):
                line[i + 1] = line[i]
            line[10] = 'null'
            # 梯户比例,配备电梯,产权年限 两者中间差一个配备电梯
            line[16] = line[15]
            line[15] = 'null'

        if '车库' in line:  # 将数据挪位置 然后空位置赋null
            line[11] = line[7]
            line[7] = line[6]
            line[6] = line[5]
            line[5] = 'null'
            line2 = []
            for i in line:
                line2.append(i if i != '' else 'null')
            line = line2
            del line2

        try:

            # 除去面积单位 不用循环 效率低
            if line[7] != 'null' and line[7] != '暂无数据':
                line[7] = line[7].replace('㎡', '')
            if line[9] != 'null' and line[9] != '暂无数据':
                line[9] = line[9].replace('㎡', '')

            writer.writerow(line)
        except Exception as e:
            print(repr(e))
            print('[写入数据失败]', line[0])

        print(line)
