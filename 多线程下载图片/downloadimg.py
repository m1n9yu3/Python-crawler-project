# coding = utf-8
# Authon : m1n9yu3
# time : 2020.10.28
"""
https://www.doutula.com/photo/list/?page=页数
"""

import requests
import re
from lxml import etree
import threading
import time
from queue import *



def askurl(url):
    """ 网页访问: 访问失败返回 空字符"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.content
    return ""


def getimage(html, q_img):
    """ 通过 html 提取图片url,名称, 访问url,下载图片,并使用刚才的名称保存到本地"""
    text = etree.HTML(html)
    s = text.xpath(
        "//div[@class='page-content text-center']//img[@class!='gif']")
    for i in s:
        img_url = i.get('data-original')
        img_name = i.get('alt')
        # print(img_name, img_url)  #打印测试数据
        q_img.put((img_url, img_name))


def saveimg(img_name, img_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"}
    r = requests.get(img_url, headers=headers)
    # 判断是否访问成功
    if r.status_code == 200:
        img_name = re.sub("[|?~]", "", img_name)
        filename = './img/' + img_name + '.' + str(img_url).split(".")[-1]
        with open(filename, mode="wb") as f:
            f.write(r.content)


def spider(url, q_img):
    getimage(askurl(url), q_img)


class MultitGetHtml(threading.Thread):

    def __init__(self, q, q_img):
        super().__init__()
        self.q = q
        self.q_img = q_img

    def run(self):
        while not self.q.empty():
            url = self.q.get()
            try:
                spider(url, self.q_img)
            except:
                print("错误:", url)


class MultitDownloadImg(threading.Thread):

    def __init__(self, q_img):
        super().__init__()
        self.q_img = q_img

    def run(self):
        while not self.q_img.empty():
            url, name = self.q_img.get()
            try:
                saveimg(img_name=name, img_url=url)
            except:
                print("错误:", url)


def MultitThread():
    """ 多线程异步爬取 """
    q = Queue()
    q_img = Queue()
    thread_count = 20  # 启用的线程数量,数量越多,爬取越快,但是容易把网站搞死
    threads = []
    for i in range(1, 100):
        url = "https://www.doutula.com/photo/list/?page=%d" % i
        q.put(url)
    for i in range(thread_count):
        threads.append(MultitGetHtml(q, q_img))
    for i in threads:
        i.start()
    # 初始化队列的时间
    time.sleep(10)
    # 多线程下载图片
    threads = []
    for i in range(thread_count):
        threads.append(MultitDownloadImg(q_img))
    for i in threads:
        i.start()
    print("执行结束")


def SingleThread():
    """ 单线程爬取 """
    for i in range(1, 2):
        url = "https://www.doutula.com/photo/list/?page=%d" % i
        s = askurl(url)
        # print(s)
        getimage(s)


def main():
    # SingleThread()
    MultitThread()


if __name__ == '__main__':
    main()
