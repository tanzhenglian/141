import random
import requests
import json
import time
import datetime
import arrow
from lxml import etree

prc_password = "123456"  # prc密码
rpc_url = "http://192.168.1.14:6800/jsonrpc"  # 改成自己的aria2 rpc链接
dir = '/downloads'  # 下载地址，末尾不需要 /


def exec_rpc(magnet):
    req = {
        "jsonrpc": "2.0",
        "id": "magnet",
        "method": "aria2.addUri",
        "params": [
            f"token:{prc_password}",
            [magnet],
            {
                "bt-stop-timeout": str(60),
                "max-concurrent-downloads": str(16),
                "listen-port": "6881",
                "dir": dir,
            },
        ],
    }
    res = requests.post(url=rpc_url, data=json.dumps(req), verify=False)
    print(res.text)
    if "error" in res:
        print("Aria2c replied with an error:", res["error"])

def isLeapYear(years):
    '''
    通过判断闰年，获取年份years下一年的总天数
    :param years: 年份，int
    :return:days_sum，一年的总天数
    '''
    # 断言：年份不为整数时，抛出异常。
    assert isinstance(years, int), "请输入整数年，如 2018"

    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
        # print(years, "是闰年")
        days_sum = 366
        return days_sum
    else:
        # print(years, '不是闰年')
        days_sum = 365
        return days_sum


def getAllDayPerYear(years):
    '''
    获取一年的所有日期
    :param years:年份
    :return:全部日期列表
    '''
    start_date = '%s-1-1' % years
    a = 0
    all_date_list = []
    days_sum = isLeapYear(int(years))
    print()
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)
    # print(all_date_list)
    return all_date_list

def main():
    # url = "https://www.141jav.com/date/2021/12/04"

    # url = "https://www.141ppv.com/date/2021/12/01"

    # url = "https://www.141jav.com/date/" + \
    #       time.strftime('%Y/%m/%d', time.localtime())

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.56',
    }

    all_date_list = getAllDayPerYear("2021")

    for date in all_date_list:
        diff=int(int(time.mktime(time.strptime(date, '%Y-%m-%d')))-int(time.mktime(time.strptime('2021-04-22', '%Y-%m-%d'))))
        if(diff>=0):
            url = "https://www.141jav.com/date/" + \
                  datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y/%m/%d')
            res = requests.get(url=url, headers=headers, verify=False).text
            dateHtml = etree.HTML(res)
            magnets = dateHtml.xpath(
                "//div[@class = 'card mb-3']//a[@title='Magnet torrent']/@href")

            for magnet in magnets:
                magnet = str(magnet)
                exec_rpc(magnet)
            # 暂停一下
            time.sleep(random.randint(5, 10))

# 开始执行主程序
if __name__ == '__main__':
    main()