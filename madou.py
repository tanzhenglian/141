import random
import requests
import json
import time
from lxml import etree, html

prc_password = "123456"  # prc密码
rpc_url = "http://192.168.1.14:6800/jsonrpc"  # 改成自己的aria2 rpc链接
dir = '/downloads'  # 下载地址，末尾不需要 /

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.56',
}


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
    res = session.post(url=rpc_url, data=json.dumps(req), verify=False)
    print(res.text)
    if "error" in res:
        print("Aria2c replied with an error:", res["error"])


def get_video_info(video_url):
    res = session.get(url=video_url, headers=headers)
    data_html = etree.HTML(res.text)
    # print(data_html)
    magnet = data_html.xpath("//div[@class = 'entry-content u-text-format u-clearfix']//p/a[@rel='follow']/@href")
    if len(magnet):
        magnet = str(magnet[0])
        # print(magnet)
        exec_rpc(magnet)



def main():
    # 设置重连次数
    requests.adapters.DEFAULT_RETRIES = 5
    global session
    session = requests.Session()
    session.keep_alive = False  # 关闭多余连接
    # 倒序167页到1,如需正序换成 for i in range(1,168):
    for i in range(168,0,-1):
        print(i)
        url = "https://madouqu.com/page/"+ str(i)
        res = session.get(url=url, headers=headers).text
        data_html = etree.HTML(res)
        video_urls = data_html.xpath(
            "//div[@class = 'entry-media']//div[@class = 'placeholder']//a[@target='_blank']/@href")
        # 循环请求详情页，得到下载地址
        print(video_urls)
        for video_url in video_urls:
            get_video_info(video_url)


# 开始执行主程序
if __name__ == '__main__':
    main()
