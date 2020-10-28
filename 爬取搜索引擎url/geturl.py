# coding = utf-8

"""
爬取 url 链接
"""

import threading
import re
import bs4
import requests
from queue import *
import sys

# 全局变量存储 所有的 url
urllist = []


class bingget(threading.Thread):
    def __init__(self, Threq):
        threading.Thread.__init__(self)
        self.q = Threq

    def run(self):
        while not self.q.empty():
            url = self.q.get()
            try:
                self.speider(url)
            except:
                print("访问错误:%s" % url)

    def speider(self, url):
        global urllist
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"}
        respone = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(respone.content, 'lxml')
        urls = soup.find_all(name="a", attrs={'class': None, "target": "_blank"})
        for i in urls:
            url_t = requests.get(headers=headers, url=i['href'])
            if url_t.status_code == 200:
                if url_t.url in urllist:
                    continue
                print(url_t.url)
                urllist.append(url_t.url)


class googleget(threading.Thread):
    def __init__(self, Threq):
        threading.Thread.__init__(self)
        self.q = Threq

    def run(self):
        while not self.q.empty():
            url = self.q.get()
            try:
                self.speider(url)
            except:
                print("访问错误:%s" % url)

    def speider(self, url):
        global urllist
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"}
        respone = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(respone.content, 'lxml')
        urls = soup.find_all(name="a", attrs={'class': None, "onmousedown": re.compile(("."))})
        for i in urls:
            # print(i['href'])
            url_t = requests.get(headers=headers, url=i['href'])
            if url_t.status_code == 200:
                if url_t.url in urllist:
                    continue
                print(url_t.url)
                urllist.append(url_t.url)


filename = ''


class baiduget(threading.Thread):

    def __init__(self, queueobj):
        """ 初始化 """
        threading.Thread.__init__(self)
        self.queueobj = queueobj

    def run(self):
        """ 开始爬取 """
        while not self.queueobj.empty():
            url = self.queueobj.get()
            try:
                self.spider(url)
            except Exception:
                pass

    def spider(self, url):
        global urllist
        """ url爬取 """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"}
        html = requests.get(headers=headers, url=url)
        if html.status_code == 200:
            soup = bs4.BeautifulSoup(html.content, 'lxml')
            urls = soup.find_all(name="a", attrs={'class': None, 'data-click': re.compile(('.'))})
            for i in urls:
                r_url = requests.get(url=i['href'], headers=headers, timeout=3)
                if r_url.status_code == 200:
                    if r_url.url in urllist:
                        continue
                    print(r_url.url)
                    urllist.append(r_url.url)
                    # self.save2txt(r_url.url)

    def save2txt(self, text):
        """ 保存文件 """
        f = open(filename, mode="a")
        f.write(text)
        f.close()


# bing 爬虫模板
"""
https://cn.bing.com/search?q=内容&first=页数
# 100 页 为最高
"""


def bingsearch(content):
    """ bing 搜索 """
    print("开始bing爬取")
    threQ = Queue()
    thread_count = 20
    threads = []
    for i in range(1, 1000, 10):
        url = "https://cn.bing.com/search?q=%s&first=%d" % (content, i)
        threQ.put(url)
    for i in range(thread_count):
        threads.append(bingget(threQ))
    for i in threads:
        i.start()


# google 爬虫模板
'''
https://www.google.com/search?q=内容&start=页数
400 条信息为最高
'''


def googlesearch(content):
    """ google 搜索 """
    print("开始谷歌爬取")
    threQ = Queue()
    thread_count = 20
    threads = []
    for i in range(1, 400, 10):
        url = "https://www.google.com/search?q=%s&start=%d" % (content, i)
        threQ.put(url)
    for i in range(thread_count):
        threads.append(googleget(threQ))
    for i in threads:
        i.start()


# 百度模板
'''
'https://www.baidu.com/s?wd=%s&pn=%s'
单次最高 750 条数据
'''


def baidusearch(keywords):
    """ baidu 爬取"""
    print("开始百度爬取")
    queueobj = Queue()
    thread_count = 20
    threads = []
    # 放入队列
    for i in range(0, 750, 10):
        queueobj.put('https://www.baidu.com/s?wd=%s&pn=%s' % (keywords, str(i)))
    # 线程对象
    for i in range(thread_count):
        threads.append(baiduget(queueobj))
    # 线程启动
    for i in threads:
        i.start()


def test():
    # url = "https://cn.bing.com/search?q=%s&first=%d" % ("mingyue", 1)
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"}
    # html = requests.get(url, headers=headers)
    # soup = bs4.BeautifulSoup(html.text, "lxml")
    # print(html.text)
    pass


def main(context):
    bingsearch(context)
    baidusearch(context)
    googlesearch(context)
    save2text()


def save2text():
    while True :
        if len(urllist) != 0:
            break
    f = open("urllist.txt", mode="w+")
    for i in urllist:
        f.write(i)
    f.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("请输入想要查询的关键字!!!")
        sys.exit(-1)
    else:
        main(sys.argv[1])
