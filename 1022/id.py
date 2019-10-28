#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket,datetime
import urllib.request
import csv
import sys

import requests
from http import cookiejar
socket.setdefaulttimeout(20)


headers = {
    "authority": "lmt-man.id-aifintech.cc",
    "method": "POST",
    "path": "/cs/collection/getTotalList?flag=member",
    "scheme": "https",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-length": "14",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://lmt-man.id-aifintech.cc",
    "pragma": "no-cache",
    "referer": "https://lmt-man.id-aifintech.cc/cs/common/frame/index?jspname=pages/csm/addressList/collectionCollector_query",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

#定义请求连接
baseurl='https://lmt-man.id-aifintech.cc/cs/collection/getTotalList?flag=member'
#登陆连接
before='https://lmt-man.id-aifintech.cc/cs/login'
login = 'https://lmt-man.id-aifintech.cc/cs/j_spring_security_check'

Con_session = requests.session()

userdataf={}
userdataf['j_username'] = input('输入用户名： ')
userdataf['j_password'] = input('输入密码： ')

cookie_object = cookiejar.CookieJar()

userdata = urllib.parse.urlencode(userdataf).encode(encoding='UTF8')

res = Con_session.post(login, data=userdata, headers=headers)
print(f"isLoginStatus = {res.status_code}")


dataformat = {
    "page": 1,
    "rows": 10
}

data = urllib.parse.urlencode(dataformat).encode(encoding='UTF8')

request = Con_session.post(url=baseurl, method='POST', data=data)
print(request.status_code)
