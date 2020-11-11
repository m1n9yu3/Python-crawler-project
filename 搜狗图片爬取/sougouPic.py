# coding = utf-8

"""
https://pic.sogou.com/napi/pc/searchList?mode=1&start=%d&xml_len=%d&query=%s % (起始地址,长度,搜索内容)
最大长度为 100
"""


import  requests
import re
import queue
import threading
import os

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"}
contect = ''

def parse_html(d,que):
    for i in d["data"]["items"]:
        localfilename = i['title']
        localfilename = re.sub("[\.,゜\*】 ()<>/\|:\*?]","",localfilename)
        localfilename += i['type']
        if "." not in localfilename:
            localfilename += ".png"
        print("图片名称:%s\t 本地名称文件: %s" % (i['title'], localfilename))
        que.put([localfilename, i['picUrl']])
        # try:
        #     saveImage(localfilename,picurl=i['picUrl'])
        # except:
        #     print("访问错误 url: ",i['picUrl'])




class GetImage(threading.Thread):
    def __init__(self,q,contect):
        threading.Thread.__init__(self)
        self.q = q
        self.contect = contect

    def run(self) -> None:
        while not self.q.empty():
            data = self.q.get()
            try:
                self.saveImage(data[0],data[1])
            except:
                print("访问错误 url:",data[1])

    def saveImage(self,filename, picurl):
        """ 保存图片到本地"""
        imgdata = requests.get(url=picurl, headers=headers, timeout=15)
        if imgdata.status_code != 200 or imgdata.content == None:
            return
        with open("./%s/"% (self.contect) + filename, mode="wb") as f:
            f.write(imgdata.content)
            f.close()

def mkdir_():
    if not os.path.exists("./%s/" % (contect)):
        # 文件夹不存在
        os.mkdir(os.getcwd() + "/%s/" % (contect))
    else:
        print("文件夹存在")


def main():
    global contect
    contect = input("请输入想要搜索的内容:")
    try:
        mkdir_()
    except:
        print("文件夹创建失败")
    q_obj = queue.Queue()
    threads = []
    thread_count = 20
    for i in range(1,1000,100):
        d = requests.get("https://pic.sogou.com/napi/pc/searchList?mode=1&start=%d&xml_len=100&query=%s" % (i,contect) ,headers=headers).json()
        parse_html(d,q_obj)
    for i in range(thread_count):
        threads.append(GetImage(q_obj,contect))
    for i in threads:
        i.start()
    for i in threads:
        i.join()


if __name__ == '__main__':
    main()

