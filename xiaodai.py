#!/bin/bash/env python
#
import urllib, json, time, socket
import urllib.request
import random

proxy_list=[]
proxy_d = {}
# proxy_list = [{'http': '111.231.90.122:8888'}, {'http': '117.191.11.109:80'}, {'http': '117.191.11.77:8080'}, {'http': '117.191.11.111:8080'}, {'http': '117.191.11.108:8080'}, {'http': '117.191.11.110:8080'}, {'http': '47.102.216.176:3128'}, {'http': '117.191.11.111:80'}, {'http': '117.191.11.77:80'}, {'http': '117.191.11.110:80'}, {'http': '117.191.11.74:8080'}, {'http': '117.191.11.72:8080'}, {'http': '117.191.11.107:80'}, {'http': '117.191.11.102:8080'}, {'http': '117.191.11.74:80'}, {'http': '117.191.11.102:80'}, {'http': '117.191.11.72:80'}, {'http': '117.191.11.107:8080'}, {'http': '117.191.11.105:8080'}, {'http': '121.40.162.239:808'}, {'http': '212.64.51.13:8888'}, {'http': '117.191.11.103:80'}, {'http': '117.191.11.79:80'}, {'http': '202.85.52.151:80'}, {'http': '62.234.188.160:80'}, {'http': '117.191.11.103:8080'}, {'http': '117.191.11.79:8080'}, {'http': '117.191.11.101:80'}, {'http': '120.210.219.73:80'}, {'http': '36.25.243.50:80'},  {'http': '183.146.213.198:80'}]
with open('ip.txt','r') as f:
    for i in f.readlines():
        proxy_d['http'] = i
        proxy_list.append(proxy_d)
f.close()
# 随机选择一个代理
proxy = random.choice(proxy_list)
# 使用选择的代理构建代理处理器对象
httpproxy_handler = urllib.request.ProxyHandler(proxy)
opener = urllib.request.build_opener(httpproxy_handler)
socket.setdefaulttimeout(5)
headers = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Cookie":"login=true; __guid=49543221.3851771190890170000.1565660474348.4082; _sm_au_d=1; shiro.sesssion=833c233f-ed3e-4854-bc23-1fdbdf8330e2;",
"Host":"bung.talu-tech.com",
"Pragma":"no-cache",
"Referer":"http://bung.talu-tech.com/console/login.do",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}

dataformat = {
"statrtTime":'',
"endTime":'',
"createdName": '',
"realName": '',
"phone":'',
"idCard": '',
}
fail=[]
data = urllib.parse.urlencode(dataformat).encode('utf-8')
# print(data)
request = urllib.request.Request(url='http://bung.talu-tech.com/console/user/home/1/findWhitelist.do', method='POST',
                                 headers=headers, data=data)
response = urllib.request.urlopen(request)
# print(data)
contentb=str(response.read(),encoding='utf-8')
print(contentb)
content = json.loads(contentb,strict=False)
response.close()
# print(content)
dic = content['data']
counts = dic['lastPageIndex']
time.sleep(1)

def req(count):
    # 随机选择一个代理
    proxy = random.choice(proxy_list)
    # 使用选择的代理构建代理处理器对象
    httpproxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(httpproxy_handler)
    dataformat['reqPageNum']=count
    data = urllib.parse.urlencode(dataformat).encode('utf-8')
    request = urllib.request.Request(url='http://bung.talu-tech.com/console/user/home/1/findWhitelist.do',
                                     method='POST',
                                     headers=headers, data=data)
    try:
        print(count)
        response = opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb)
        response.close()
        dic = content['data']
        counts = dic['lastPageIndex']
        resultlist = dic['list']
        return resultlist
    except ConnectionResetError as e:
        fail.append(count)
        print(e)
        # time.sleep(30)
        a=[]
        return  a
    except socket.timeout as e:
        fail.append(count)
        print(e)
        a=[]
        return  a
    except Exception as e:
        fail.append(count)
        print(e)
        a=[]
        return  a

for i in range(570,counts):
    alist=req(i)
    with open('result.txt','a') as f:
        for i in alist:
            f.write(i['phone']+'\n')
    f.close()

    
while fail:
    for i in fail:
        fail.remove(i)
        alist = req(i)
        with open('result.txt', 'a') as f:
            for i in alist:
                f.write(i['phone'] + '\n')
        f.close()
        time.sleep(3)
print(fail)
