#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket,datetime
import urllib.request
import csv
import sys
from http import cookiejar
import threading
from multiprocessing import Process

socket.setdefaulttimeout(20)

class Connect(object):
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "adminweb.kreditselulera.com",
            "Pragma": "no-cache",
            "Referer": "http://adminweb.kreditselulera.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }
        #自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        #定义请求连接获取用户编码 customerId
        self.baseurl='http://adminweb.kreditselulera.com/api/api/customer/load-customers?'
        #获取用户个人信息
        self.perUrl='http://adminweb.kreditselulera.com/api/api/customer/load-personal-info?'
        # 获取用户基础信息
        self.userUrl='http://adminweb.kreditselulera.com/api/api/customer/load-basic-info?'
        # 放款信息
        self.loanurl='http://adminweb.kreditselulera.com/api/api/finance/loanIssue?'
        # 还款信息
        self.deposurl='http://adminweb.kreditselulera.com/api/api/finance/deposit?'
        #验证码连接
        self.catpch='http://adminweb.kreditselulera.com/api/auth/captcha?width=120&height=50&serialId=svysoP6G'
        self.login = 'http://adminweb.kreditselulera.com/api/auth/login'

    def loginaction(self,userdataf):
        caprep = urllib.request.Request(self.catpch)
        capponse = self.opener.open(caprep)
        print(self.catpch)
        SecretCode = input('输入验证码： ')
        capponse.close()
        userdataf['answer'] = SecretCode
        userdata = urllib.parse.urlencode(userdataf).encode(encoding='UTF8')
        login = urllib.request.Request(self.login, method='POST', data=userdata, headers=self.headers)
        response = self.opener.open(login)
        response.close()


    def reqdepoinfo(self, offset, limit, filename):
        dataformat = {
            # "depositStatus": 'CLEARED',
            "offset": offset,
            "limit": limit
            # "startTime":"2019-09-01",
            # "endTime": "2019-10-01"
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl = self.deposurl + data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)

        print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        # 放款编号、贷款编号，贷款状态、用户名、手机、创建时间
        totalcount = content['paginator']['totalCount']
        a = {}
        a['totalcount'] = totalcount
        depolist = []
        for i in content['item']:
            depodic = {}
            depodic['还款编号'] = i['orderNo']
            depodic['贷款编号'] = i['loanAppId']
            depodic['还款到账时间'] = i['reachedTime']
            depodic['交易状态'] = 'CLEARED'
            depodic['用户姓名'] = i['realName']
            depodic['手机号'] = i['mobile']
            depodic['创建时间'] = i['createTime']
            depodic['用户编号'] = i['customerId']
            depolist.append(depodic)

        with open(filename, 'a', newline='') as f:
            head = ['用户编号', '用户姓名', '手机号', '还款编号','贷款编号', '交易状态', '创建时间', '还款到账时间'
                    ]
            writer = csv.DictWriter(f, head)
            for item in depolist:
                writer.writerow(item)
            f.close()
        return a

    def depoaction(self, filename, limit):
        filename1 = filename + 'depo.csv'
        with open(filename1, 'w') as f:
            # 贷款编号、用户姓名、手机、交易状态、创建时间、还款到账时间
            head = ['用户编号', '用户姓名', '手机号', '还款编号','贷款编号', '交易状态', '创建时间', '还款到账时间'
                    ]
            writer = csv.DictWriter(f, head)
            writer.writeheader()
        # basereq.headers['Cookie'] = sys.argv[1]
        baseinfo = basereq.reqdepoinfo(0, 10, filename1)
        offset = 10
        totalCount = baseinfo['totalcount']
        threadlist = []
        while offset <= totalCount:
            # basereq.userInfo(contact_list, filename)
            t = threading.Thread(target=basereq.reqdepoinfo, args=(offset, limit, filename1,))
            offset = offset + limit
            threadlist.append(t)

        n = 0
        for i in threadlist:
            i.setDaemon(True)
            i.start()
            if n > 10:
                i.join()
                n = 0
            n = n + 1
        i.join()



if __name__ == '__main__':
    now = datetime.datetime.now()
    format = "%Y-%m-%d-%H-%M-%S"

    basereq = Connect()
    userdataf = {}
    if len(sys.argv) >= 2:
        userdataf['mobile'] = sys.argv[1]
        userdataf['password'] = sys.argv[2]
    else:
        userdataf['mobile'] = input('输入用户名： ')
        userdataf['password'] = input('输入密码： ')
    basereq.loginaction(userdataf)
    filename=userdataf['mobile']+  now.strftime(format)
    basereq.depoaction(filename, 200)

