#!/bin/bash/env python
#
import urllib, json, time, socket
import urllib.request
import random

socket.setdefaulttimeout(3)
proxy_list = []

with open('F:\ipproxy\代理IP.txt', 'r') as f:
    for i in f.readlines():
        proxy_d = {}
        proxy_d['http']=i
        # 随机选择一个代理
        # proxy = random.choice(proxy_list)
        # 使用选择的代理构建代理处理器对象
        httpproxy_handler = urllib.request.ProxyHandler(proxy_d)
        opener = urllib.request.build_opener(httpproxy_handler)

        requset= urllib.request.Request('http://bung.talu-tech.com/console/login.do')
        try:
            response = opener.open(requset)
            with open('ip.txt', 'a') as f:
                f.writelines(i)
                f.close()
            proxy_list.append(proxy_d)
            # print(proxy_list)
        except Exception as e:
            print(e)
    f.close()
print(proxy_list)
