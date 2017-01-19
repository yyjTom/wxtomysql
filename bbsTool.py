from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import json
import re
import urllib.request
import urllib
import pymysql
from collections import deque
from bs4 import BeautifulSoup
import time
import random
import wxlist
import wxtosql
import threading
import webbrowser
import os
def downicon():
    temp=os.path.exists("egj.ico")
    if(temp==False):
        print("aa")
        url="http://60.205.150.155/bbstool/egj.ico"
        urlop=urllib.request.urlopen(url)
        date=urlop.read()
        f = open("egj.ico",'wb')  
        f.write(date)  
        f.close()  
        print('Pic Saved!')   

def btnljdis():
    btnlj.state(['disabled'])
    btnlj.update_idletasks()
    
def loginstate(statestr):
    state["text"]=statestr
    state.update_idletasks()
    
def autostate(statestr):
    stateauto["text"]=statestr
    stateauto.update_idletasks()
    
def ljstate(statestr):
    statelj["text"]=statestr
    statelj.update_idletasks()
 
def systime():
    print("获取网络时间")
    try:
        urltime="http://admin.egjegj.com/util/api/getTime/"
        urlop = urllib.request.urlopen(urltime)
        date = urlop.read().decode("utf-8")
        date = date.replace("\"", "")
        date = date.replace("\n", "")
        print("获取网络时间成功："+date)
        statestr="获取网络时间成功："+date
        global sysdata
        sysdata=date
        loginstate(statestr)
    except: 
        date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()) )
        print("获取网络时间失败，获取本地时间:",date)
        statestr="获取网络时间失败，获取本地时间:"+date
        global sysdata
        sysdata=date
        loginstate(statestr)
def version(num):
    url="http://admin.egjegj.com/handyService/api/getOtherVersion"
    urlop = urllib.request.urlopen(url)
    json_str = urlop.read().decode("utf-8")
    data = json.loads(json_str)
    print(data)
    value=data['version']['version']
    msg=data['version']['desc']
    print(value)
    if(num!=value):
        ans=messagebox.askyesno(title='新版本提醒', message = "发现e管家灌水工具有新版本，是否更新\n更新提醒：\n"+msg)
        if(ans):
            url=data['version']['path']            
            webbrowser.open_new(url)
            #os.exit()            
            sys.exit()

def get_screen_size(window):  
    return window.winfo_screenwidth(),window.winfo_screenheight()
  
def get_window_size(window):  
    return window.winfo_reqwidth(),window.winfo_reqheight()  
  
def center_window(root, width, height):  
    screenwidth = root.winfo_screenwidth()  
    screenheight = root.winfo_screenheight()  
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)  
    print(size)  
    root.geometry(size)
def sysclose(*e):
    print("exit")
    sys.exit()

#root.deiconify() 显示窗体
#root.withdraw()  隐藏窗体
#name.grid_forget() 删除组件
def reg():   
    n=name.get()
    p=password.get()
    if(n and p):       
        
        t1 = threading.Thread(target=loginstate("正在登陆..............................................................."))
        t1.start()
        url="http://wuye.egjegj.com/index.php/Api/Public/login?username="+n+"&password="+p
        urlop = urllib.request.urlopen(url)
        json_str = urlop.read().decode("utf-8")
        data = json.loads(json_str)
        print(data)
        value=data['operateSuccess']
        if(value):
            t1 = threading.Thread(target=loginstate("登陆成功，等待跳转"))
            t1.start()
            global userid
            global loginName
            global nickName
            global cid
            cid=data['user']['communityId']
            userid=data['user']['id']
            loginName=data['user']['loginName']
            nickName=data['user']['nickName']
            print("id:"+userid+loginName+nickName)
            loginWin.withdraw()
            choiceWin.deiconify()            
        else:
            state["text"]="用户名或密码错误"
    else:
        state["text"]="请输入用户名或密码"
    
def auto():
    autoWin.deiconify()
    print("id:"+userid+loginName+nickName)
 
def lj():
    ljWin.deiconify()
    print("id:"+userid+loginName+nickName)
    
def quitlj():
    btnlj.state(['!disabled'])
    ljWin.withdraw()
    print("id:"+userid+loginName+nickName)
 
def quitauto():
    btnauto.state(['!disabled'])
    autoWin.withdraw()
    print("id:"+userid+loginName+nickName)
    
def cmdlj():
    btnlj.state(['disabled'])
    
    ljstate("开始抓取")

    styletype=ljstyle.get()
    plate=ljplate.get()   
   
    conn=pymysql.connect(host='rds5ty3k88i163pqs7y7.mysql.rds.aliyuncs.com',user='lcht',passwd='lcht2015_yyj',db='egjbbs',port=3306,charset='utf8')
    cur=conn.cursor()#获取一个游标
    print(cur)
    
   
    ljstate("分析url中...")
    url=urltext.get("0.0", "end");
    print()
    sql=wxtosql.wxtosql(url,userid,loginName,styletype,plate,sysdata,nickName,cid);
    if(sql.find('error')==-1):
        cur.execute(sql)
        conn.commit()
        ljstate("操作成功")
    else:
        ljstate(sql)
    conn.commit()
    cur.close()#关闭游标
    conn.close()#释放数据库资源    
    print("成功") # 把末尾的'\n'删掉
    
def cmdauto():
    btnauto.state(['disabled'])
    autostate("开始抓取")
    styletype=autostyle.get()
    plate=autoplate.get()
    keywords=autokey.get()
    num=int(autonum.get())
    page=num/10
    conn=pymysql.connect(host='rds5ty3k88i163pqs7y7.mysql.rds.aliyuncs.com',user='lcht',passwd='lcht2015_yyj',db='egjbbs',port=3306,charset='utf8')
    cur=conn.cursor()#获取一个游标
    print(cur)
    queue=wxlist.listwx(keywords,page)
    autostate("获取列表完成")
    autostate("分析列表中...")
    count=1;
    while queue:
        url=queue.popleft();      
        sql=wxtosql.wxtosql(url,userid,loginName,styletype,plate,sysdata,nickName,cid);
        if(len(sql)>0):
            cur.execute(sql)
            conn.commit()
            autostate("成功插入%s条"%(count))
            count=count+1;
    conn.commit()
    cur.close()#关闭游标
    conn.close()#释放数据库资源
    autostate("操作成功")
    print("成功") # 把末尾的'\n'删掉
global loginName
global userid
global nickName
global sysdata
global cid
sysdata=date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
sversion = threading.Thread(target=version("2.3"))
sversion.start()
stime = threading.Thread(target=systime)
stime.start()
downicon()
#登陆窗口创建
loginWin=Tk()
loginWin.title("e管家灌水工具")
loginWin.iconbitmap('egj.ico')
center_window(loginWin,260,170)
#loginWin.geometry('600x600')
Label(loginWin,text="在此输入您选择发布信息的用户名和密码").grid(row=0,columnspan=2,padx=10,pady=5)
Label(loginWin,text="账号：").grid(row=1,sticky=E)
name=Entry(loginWin)
name.grid(row=1,column=1,sticky=E,padx=10,pady=5)

Label(loginWin,text="密码：").grid(row=2,sticky=E)
password=Entry(loginWin)
password['show']="*"
password.grid(row=2,column=1,sticky=E,padx=10,pady=5)
Button(loginWin, text="确定", command = reg).grid(row=4,columnspan=2,padx=10,pady=5)
#底部状态显示栏
state=Label(loginWin,text="")
state.grid(row=5,columnspan=2,sticky=W)
loginWin.protocol("WM_DELETE_WINDOW", sysclose)


#链接抓取窗口
ljWin=Tk()
ljWin.title("链接抓取")
ljWin.iconbitmap('egj.ico')
ljWin.overrideredirect(True)
center_window(ljWin,500,400) # 是x 不是*

Label(ljWin, text="请在搜狗搜索中，搜索您的微信文章，链接为：http://weiloginWin.sogou.com/").pack()
Label(ljWin, text="请要输入连接").pack()
urltext=Text(ljWin,height=5,width=50)
urltext.pack()

Label(ljWin, text="请要输入要灌水的版块id：").pack()
ljplate = Entry(ljWin,text="")
ljplate.pack()

Label(ljWin, text="请选择发布图文类型").pack()
Label(ljWin, text="输入0：无图模式，输入1：标准魔术，输入2：右图模式",foreground="red").pack()
Label(ljWin, text="输入3：单图模式，输入其他值将随机随机",foreground="red").pack()
ljstyle = Entry(ljWin,text="随机")
ljstyle.pack()

Label(ljWin, text=" ").pack()
btnlj=Button(ljWin, text="确定", width=10,command = cmdlj)
btnlj.pack()
Button(ljWin, text="关闭", width=10,command = quitlj).pack()
statelj=Label(ljWin,text="")
statelj.pack()




#自动抓取窗口
autoWin=Tk()
autoWin.title("自动抓取")
autoWin.iconbitmap('egj.ico')
autoWin.overrideredirect(True)
center_window(autoWin,500,400) 

Label(autoWin, text="请要输入要查找的关键词：").pack()
autokey=Entry(autoWin,text="")
autokey.pack()

Label(autoWin, text="请要输入要搜集多少条目（10的倍数）：").pack()
autonum = Entry(autoWin,text="")
autonum.pack()

Label(autoWin, text="请要输入要灌水的版块id：").pack()
autoplate = Entry(autoWin,text="")
autoplate.pack()

Label(autoWin, text="请选择发布图文类型").pack()
Label(autoWin, text="输入0：无图模式，输入1：标准魔术，输入2：右图模式",foreground="red").pack()
Label(autoWin, text="输入3：单图模式，输入其他值将随机随机",foreground="red").pack()
autostyle = Entry(autoWin,text="随机")
autostyle.pack()

btnauto=Button(autoWin, text="确定", width=10,command = cmdauto)
btnauto.pack()
Button(autoWin, text="关闭", width=10,command = quitauto).pack()
stateauto=Label(autoWin,text="")
stateauto.pack()


#选择模式窗口
choiceWin=Tk()
choiceWin.iconbitmap('egj.ico')
choiceWin.title("选择模式")
center_window(choiceWin,280,100)
Button(choiceWin, text="自动抓取",width=10,command = auto).grid(row=0,column=0,padx=30,pady=30)
Button(choiceWin, text="链接抓取",width=10,command = lj).grid(row=0,column=1,padx=30,pady=30)
choiceWin.protocol("WM_DELETE_WINDOW", sysclose)
#隐藏除登陆外的所有窗口
ljWin.withdraw()
autoWin.withdraw()
choiceWin.withdraw()
loginWin.mainloop()

