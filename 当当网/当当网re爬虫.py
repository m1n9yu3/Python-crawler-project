# coding = utf-8

"""
当当网 爬虫任务
商品名称 商品链接 价格 作者 出版日期 出版社 评分 评论数 商家
数据保存到 excel 文档中


url: http://search.dangdang.com/?key=python%C5%C0%B3%E6&act=input&page_index=页数
最高到 99 页

"""
import requests
import re
import os




def ack_url(url):
    """ 访问网页 返回页面信息"""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    response = requests.get(url=url, headers=headers)
    return response.text

def mkdir_():
    if not os.path.exists("./img/"):
        os.mkdir("./img/")



def parse_html(html):
    """ 解析页面信息, 顺便保存商品图片"""
    info = []
    l = re.findall("<a title=(.*)</li>", html)
    for i in l:
        single_info = []
        # 商品标题
        tilte = re.findall('"(.*)"  ddclick=', i)
        tilte[0] = tilte[0].replace(",", "")
        single_info += tilte
        # 商品链接
        single_info += re.findall('href="(.*)"  target="_blank" >', i)
        # 商品价格
        pairs = re.findall('search_now_price">(.*?)</span>', i)
        pairs[0] = pairs[0].replace("&yen;", "￥")
        single_info += pairs
        # 作者
        authon = re.findall("name='itemlist-author' dd_name='单品作者' title='.*?'>(.*?)</a>", i)
        authons = ''
        if len(authon) > 1:
            for auth in authon:
                authons += auth + '/'
            single_info += [authons]
        elif len(authon) == 1:
            single_info += authon
        else:
            single_info += ['无']
        # 出版日期
        press_time = re.findall('<p class="search_book_author"><span>.*?</span><span >(.*?)</span>', i)
        if len(press_time) == 0:
            single_info += ['None']
        else:
            single_info += press_time
        # 出版社
        press = re.findall("name='P_cbs' dd_name='单品出版社' title='.*?'>(.*?)</a>", i)
        if len(press) == 0:
            single_info += ['无']
        else:
            single_info += press
        # 评分
        single_info += re.findall('<span style="width: (.*);"></span>', i)
        # 评分有一个转换
        # 评价数
        single_info += re.findall('class="search_comment_num" ddclick=".*?">(.*?)</a>', i)
        # 店铺
        shop = re.findall('name="itemlist-shop-name" dd_name="单品店铺" target="_blank" title=".*?">(.*?)</a>', i)
        if len(shop) == 0:
            single_info += ['自营']
        else:
            single_info += shop
        info.append(single_info)

    return info



def save2excel(info):
    """ 保存数据到 excel"""
    if not os.path.exists("1.csv"):
        os.remove("1.csv")

    with open("1.csv", mode="w") as f:
        f.write("商品名称,商品链接,价格,作者,出版日期,出版社,评分,评论数,商家\n")
        for i in info:
            s = ",".join(i) + "\n"
            f.write(s)

def main():
    url = "http://search.dangdang.com/?key=python爬虫&act=input&page_index=%d"
    info = []
    for i in range(1, 100):
        h = ack_url(url % i)
        info += parse_html(h)
        print("第{}页，爬取完成".format(i))
    save2excel(info)


if __name__ == '__main__':
    main()
