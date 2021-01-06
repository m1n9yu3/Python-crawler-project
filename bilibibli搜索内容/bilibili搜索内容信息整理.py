# !/usr/bin/python3
# coding = utf-8

import requests
import re
import bs4
from lxml import etree
import time
import pandas as pd
import xlsxwriter

"""
https://search.bilibili.com/all?keyword=内容&page=页数

爬取目标：  视频标题  视频链接  视频上传时间 视频播放量  视频时常 视频up主

"""


def parse_html(page_html):
    """页面解析"""
    data = []
    etr = etree.HTML(page_html.text)
    # print(page_html.text)
    soup = bs4.BeautifulSoup(page_html.text, "lxml")
    for i in soup.find_all('li', attrs={"class": "video-item matrix"}):
        info = []
        # print(i)
        # 标题解析
        info.append(i.find("a", attrs={"class": "title"})['title'])
        # 链接解析
        info.append(i.find("a", attrs={"class": "title"})['href'][2:].replace("?from=search", ""))
        # 播放数量
        # print(list(i.find("span", attrs={"class": "so-icon watch-num"}).strings)[0])
        info.append(i.find("span", attrs={"class": "so-icon watch-num"}).text.replace("\n", "").replace(" ", ""))
        # 视频时长
        info.append(i.find("span", attrs={"class": "so-imgTag_rb"}).text)
        # 弹幕数量
        info.append(i.find("span", attrs={"class": "so-icon hide"}).text.replace("\n", "").replace(" ", ""))
        # 上传时间
        info.append(i.find("span", attrs={"class": "so-icon time"}).text.replace("\n", "").replace(" ", ""))
        # up 主
        info.append(i.find("a", attrs={"class": "up-name"}).text)
        data.append(info)
        print(info)
    return data


def is_next(response):
    """判断是否有下一页"""
    return re.findall('<li class="page-item next">', response.text) != []


def save_data(data):
    """保存数据，  将数据保存到 excel 表格中"""
    pd.DataFrame(data, columns=['标题', '链接', '观看数量', '视频时长', '弹幕数量', '上传时间', 'up主姓名']).to_excel('bilibili.xlsx', index=False, engine='xlsxwriter')

def main():
    # connect = input("请输入搜索内容:")
    connect = 'python'
    data = []
    url = "https://search.bilibili.com/all?keyword=%s&page=%d"
    headers = {"User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    for i in range(1, 50):
        response = requests.get(url=url % (connect, i), headers=headers)
        data += parse_html(response)
        if not is_next(response):
            # 没有下一页按钮
            print("爬取结束,共爬取 %d 页内容" % i)
            break


    save_data(data)


if __name__ == '__main__':
    main()
