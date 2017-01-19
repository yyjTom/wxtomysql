import re
import urllib.request
import urllib
import pymysql
from collections import deque
from bs4 import BeautifulSoup
import time
import sys
import getpass
import random

#字符串替代函数,1对应url，2对应html
def unescape(s,strtype):
    if strtype==1:        
        #s = s.replace("&lt;", "<")
        #s = s.replace("&gt;", ">")
        # this has to be last:
        s = s.replace("&amp;", "&")
    elif strtype==2:
        s = s.replace("data-src", "width=\"100%\" src")
        s = s.replace("data-w", "aa")
        s = s.replace("'", "")
    elif strtype==3:       
        s = s.replace("\"", "")
        s = s.replace("\n", "")
    return s
#获取搜狗微信中索引连接
#query:关键字，page:查找的页数（1页10条索引）
def listwx(query,page):
    state=0
    #已队列形式存储访问的链接    
    queue = deque()
    #存储已经访问到的链接
    visited = set()
    #搜狗微信的根地址
   # url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&p=42341200&dp=1"
   # url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&dp=1"
    url ="http://weixin.sogou.com/weixin?usip=null&from=tool&ft=&tsn=1&et=&interation=null&type=2&wxid=&ie=utf8"    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    #按照页数循环遍历
    count=1;
    
    while (count <= page):
       # print("防止被禁止，等待中。。。")
       #time.sleep(1)
        url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&dp=1"
        
        values = {'page' : count,    
                 'query' : query}

        data = urllib.parse.urlencode(values)
        url=url+'&'+data

        headers = {'Cookie': 'CXID=D3404FABEEBE7CAAC342A938AF1926E4; SUID=836CA46F4E6C860A57AADED000022AA2; SUV=00CE353B6FA45EA257BD2B7285E0E720; IPLOC=CN1200; SUIR=1480588826; SNUID=379F93E6C9CF885FB9EA7900CADEC68D'}
        print(url)        
        req = urllib.request.Request(url,headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read().decode("utf-8")
##        print(data)
        
        # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
        linkre = re.compile('href=\"(http://mp.weixin.qq.com/s.+?)\"')
        if len(linkre.findall(data))<3:
           
            state=0
            while state!=1 and state!=2 and state!=3:
                print("此网页现在需要输入验证码，才能继续抓取！请用ie打开网址http://weixin.sogou.com/weixin?query=1，输入验证码")
                print("输完验证码请按1，跳过网页抓取直接开始分析请按2，取消此次工作输入请按3")            
                state = int(input("请输入："));
                print ("你输入的内容是: ",state)              
                    
        if state ==0:
            pass
        if state == 1:
            continue                
        elif state == 2:
            return queue
        elif state ==3:
            print ("程序退出")
            sys.exit(0)    

        for x in linkre.findall(data):
            y=unescape(x,1)
            if 'http' in y and y not in visited:
              visited |= {y}
              print('加入队列 --->  ' + y)      
              queue.append(y)        
        print("已经采集的页数：",count)
        count +=1
    return queue

