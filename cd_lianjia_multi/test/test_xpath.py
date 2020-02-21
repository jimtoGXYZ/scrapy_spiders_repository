import requests
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "Accept-Encoding": "gzip, deflate, br",
    'Accept-Language': 'zh-CN,zh;q=0.9',
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Referer": "https://cd.lianjia.com/ershoufang/",
}

response = requests.get(url="https://cd.lianjia.com/ershoufang/106102258795.html", headers=headers)

if response.status_code == 200:
    html_str = response.text
    tree = etree.HTML(html_str)
    transaction_list = tree.xpath("//div[@class='transaction']//ul/li/span/text()")
    content = tree.xpath("//div[@class='content']//li/text()")
    # print(content[2] if content[2].replace(' ', '') != '' or content[2].strip() != None else 'null')
    # print(content)
    # print(transaction_list[7])
    item = ['null' for i in range(25)]

    communityName = tree.xpath("//div[@class='communityName']/a/text()")[0]
    areaName = tree.xpath("//div[@class='areaName']/span/a/text()")[0]
    price = tree.xpath("//span[@class='total']/text()")[0]
    unitPrice = tree.xpath("//div[@class='unitPrice']/span/text()")[0]
    # item.append(communityName, areaName, price, unitPrice)
    # print(communityName, areaName, price, unitPrice)
    item[1] = communityName

    print(item)