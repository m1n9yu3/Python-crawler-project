# coding = utf-8
"""
https://rapiddns.io/subdomain/baidu.com?page=1#result
https://rapiddns.io/subdomain/搜索内容?page=页数#result
"""

import requests
from lxml import etree
import threading
import queue
import sys


class get_url(threading.Thread):
    def __init__(self, Q, searchname):
        threading.Thread.__init__(self)
        self.q = Q
        self.contect = searchname

    def run(self):
        """访问 url """
        while not self.q.empty():
            url = self.q.get()
            try:
                self.parse_html(url)
            except Exception:
                pass

    def parse_html(self, url):
        """ 页面解析"""
        # print(contect)
        html = requests.get(url=url).text
        pa = etree.HTML(html)
        l = []
        for i in pa.xpath("//a[@target='_blank']//text()"):
            if (self.contect in i) and (i != self.contect):
                # if isok(i):
                print(i)
                l.append(i)
        return l

def isok(url):
    """ 判断网页是否可以访问"""
    return requests.get(url).status_code == 200

def main(searchname: str):
    """ 主函数 """
    # 创建线程队列
    threQ = queue.Queue()
    thread_count = 20
    threads = []
    # 查看有效数据
    for i in range(1, 150):
        url = "https://rapiddns.io/subdomain/%s?page=%d#result" % (searchname, i)
        threQ.put(url)
    for i in range(thread_count):
        threads.append(get_url(threQ, searchname))
    for i in threads:
        i.start()
    # 暂停线程
    for i in threads:
        i.join()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("请输入想要查询的关键字!!!")
        sys.exit(-1)
    else:
        main(sys.argv[1])

"""
python3 main.py  要查询的关键字  > 重定向文本
"""
