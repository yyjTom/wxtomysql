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

def wxtosql(url,userid,userName,styletype,plate,date,nickName,cid):
    print("正在抓取---->"+url)
    urlop = urllib.request.urlopen(url)
    data = urlop.read().decode("utf-8")
    soup = BeautifulSoup(data,"html.parser")
    #去掉代码中的script和style
    [s.extract() for s in soup(['script','style'])]
    #去掉img标签中的style\data-w标签
    for s in soup.find_all('img'):
        del s['data-w']
        del s['style']
        del s['width']
    for s in soup.find_all('iframe'):
        if(s.get('src')):
            s['data-src']=s['src']
            del s['src']
        del s['data-w']
        del s['style']
        del s['width']
        del s['height']
    title= soup.title.get_text();
    #html代码中id为js_content是内容部分
    content = soup.select('div[id="js_content"]')[0]
    desc=content.get_text()[:100]
    desc = desc.replace("\n", "")
    desc = desc.replace(" ", "")
    desc = desc.replace("'", "")
    desc=desc.replace(u'\xa0', u' ')
    #将content中data-src去掉，并格式化输出
    try:
        content=unescape(content.prettify(formatter=None),2)
    except:
        print("error 002")
        sql="error 002"
        return sql
    #content=unescape(content,2)
    content = content.replace("\n", "")
    content = content.replace("<p></p>", "")
     #将content中src的图片地址重新处理到图床
    linkre = re.compile('width=\"100%\" src=\"(.+?)\"')
    reslist=linkre.findall(content)
    path=""
    count=0
    for x in reslist:
        print(x)
        if(x.find('iframe')!=-1):
            print("no...")
            newurl=x
            newurl = newurl.replace("&width", "&aaa")
            newurl = newurl.replace("&height", "&aaa")
            newurl = newurl.replace("preview", "player")
            content=content.replace(x,newurl)               
            continue
        print("yes...")        
        random.seed()
        name=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+str(random.randint(1000,9999))
        if(x.find('gif')!=-1):
            name=name+".gif"
        else:
            name=name+".jpg"
        print(name)
        imgurl="http://121.43.230.60/publicApi/qiniuUpimg.php?name="+name+"&img="+x;
        urlop = urllib.request.urlopen(imgurl)
        data = urlop.read().decode("utf-8")
        if(data.find('error')==-1):
            newurl="http://oivtcly0a.bkt.clouddn.com/"+name
            content=content.replace(x,newurl)
            if(styletype!="0" and count>=1 and count<=4):
                imgurl="http://admin.egjegj.com/LT/uploads/tp/urlimg.php?name="+name+"&img="+newurl;
                try:
                    urlop = urllib.request.urlopen(imgurl)
                    data = urlop.read().decode("utf-8")
                    if(data.find('error')==-1):
                        path=path+"uploads/Tp/"+name+","
                        print(path)
                except:
                    print("error")
            count=count+1;
        else:        
            print("error")
    path=path[:-1]
    print(path)
    print("图文输入为："+styletype)
    
    if(len(path)==0 or styletype=="0"):
        print("aaaaaaaaaaaaaaaaaaaaaaaaa")
        stype="1"
    elif(styletype !="1" and styletype !="2" and styletype !="3" and styletype !="0" ):        
        stype=str(random.randint(1,3))
        print("bbbbbbbbbbb"+stype)
    else:
        stype=styletype
    print("图文模式为："+stype)
    try:
        url="http://60.205.150.155/bbstool/img/"+plate+".jpg"
        urlop=urllib.request.urlopen(url)
        content=content+'<img width=\"100%\" src=\"'+url+'\"></img>'
    except:
        print("no image")
    sql="INSERT INTO `egj_sendcard`(communityId,plateId,title,cardContent,date,`desc`,userId,nickName,userName,disable,pageView,path,path_thu,tag,stick,good,contribute,showCommunity,inte,styleType,platform) VALUES ("+cid+","+plate+",'"+title+"','"+content+"','"+date+"','"+desc+"',"+userid+",'"+nickName+"','"+userName+"',0,1,'"+path+"','"+path+"',0,0,0,1,0,0,"+stype+",1)"
    #print(sql)
    return sql

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
