import re
import urllib.request
import urllib
import pymysql
from collections import deque
from bs4 import BeautifulSoup
import time
import sys
import getpass
#python默认的递归深度是很有限的，再次定义更大递归深度
sys.setrecursionlimit(1000000) #例如这里设置为一百万

global state
state=0

#字符串替代函数,1对应url，2对应html
def unescape(s,strtype):
    if strtype==1:        
        #s = s.replace("&lt;", "<")
        #s = s.replace("&gt;", ">")
        # this has to be last:
        s = s.replace("&amp;", "&")
    elif strtype==2:
        s = s.replace("data-src", "width=\"100%\" src")
        s = s.replace("'", "")
    elif strtype==3:       
        s = s.replace("\"", "")
    return s

#获取搜狗微信中索引连接
#query:关键字，page:查找的页数（1页10条索引）
def listwx(query,page):
    global state
    #已队列形式存储访问的链接    
    queue = deque()
    #存储已经访问到的链接
    visited = set()
    #搜狗微信的根地址
    url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&p=42341200&dp=1"
    url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&dp=1"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    #按照页数循环遍历
    count=1;
    
    while (count <= page):
       # print("防止被禁止，等待中。。。")
       #time.sleep(1)
       
        
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


print("获取网络时间")
try:
    urltime="http://admin.egjegj.com/util/api/getTime/"
    urlop = urllib.request.urlopen(urltime)
    date = unescape(urlop.read().decode("utf-8"),3)    
    print("获取网络时间成功："+date)
except:
    print(e)
    sys.exit(0)   
    date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()) )
    print("获取网络时间失败，获取本地时间:",date)

print("请输入此脚本密钥");
key=getpass.getpass()
#key="lcht%2016"
while key!="lcht%2016":
    print("密码不正确请重新输入");
    key=getpass.getpass()
      
keywords = input("请要输入要查找的关键词：");
print ("你要查找的关键词是: ",keywords)
num = int(input("请要输入要搜集多少条目（10的倍数）："));
print ("你要查找的条数为: ",num)
page=num/10
queue=listwx(keywords,page)





conn=pymysql.connect(host='localhost',user='root',passwd='root',db='stblog',port=3306,charset='utf8')
cur=conn.cursor()#获取一个游标
print(cur)

while queue:
    url=queue.popleft();
    #print("防止被禁止，等待中。。。")
    #time.sleep(1)
    print("正在抓取---->"+url)
    urlop = urllib.request.urlopen(url)
    data = urlop.read().decode("utf-8")
    soup = BeautifulSoup(data,"html.parser")
    #去掉代码中的script和style
    [s.extract() for s in soup(['script','style'])]
    
    title= soup.title.get_text();
    #html代码中id为js_content是内容部分
    content = soup.select('div[id="js_content"]')[0]
    #将content中data-src去掉，并格式化输出
    content=unescape(content.prettify(formatter=None),2)

    sql="INSERT INTO `egj_sendcard`(communityId,plateId,title,cardContent,date,userId,nickName,userName,disable,pageView,tag,stick,good,contribute,showCommunity,inte) VALUES (2,173,'"+title+"','"+content+"','"+date+"',8349,'版主','18002160216',0,1,0,0,0,1,0,0)"
    #print(sql)‘
    cur.execute(sql)
    conn.commit()

conn.commit()
cur.close()#关闭游标
conn.close()#释放数据库资源
print("成功") # 把末尾的'\n'删掉

key = input("输入回车关闭");
