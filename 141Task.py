import requests
import json
import time
from lxml import etree

prc_password="123456" #prc密码
rpc_url = "http://192.168.1.14:6800/jsonrpc"  #改成自己的aria2 rpc链接
dir='/downloads'     #下载地址，末尾不需要 /

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
    res=requests.post(url=rpc_url, data=json.dumps(req), verify=False)
    print(res.text)
    if "error" in res:
        print("Aria2c replied with an error:", res["error"])

def main():
    url = "https://www.141jav.com/date/" + \
          time.strftime('%Y/%m/%d', time.localtime())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.56',
    }
    res = requests.get(url=url, headers=headers).text

    dateHtml = etree.HTML(res)
    magnets = dateHtml.xpath(
        "//div[@class = 'card mb-3']//a[@title='Magnet torrent']/@href")
    for magnet in magnets:
        magnet = str(magnet)
        exec_rpc(magnet)

# 开始执行主程序
if __name__ == '__main__':
    main()