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
            "Host": "149.129.222.131:9999",
            "Pragma": "no-cache",
            "Referer": "http://149.129.222.131:9999/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "X-ADMIN- TOKEN": "eyJsb2NhbGUiOiJ6aF9DTiIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiI2MDAwNCIsImV4cCI6MTU2Nzk0NDYzMn0.1X85QY0gwtpSH8K08RwFAK5LVS-nvReAU5zONhHiQiyDCd9v5sWcc6SHR34hIqkxKYiz07QzGyEdf01kE1_yxg"
        }
        #自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        #定义请求连接获取用户编码 customerId
        self.baseurl='http://149.129.222.131:9999/api/api/customer/load-customers?'
        #获取用户个人信息
        self.perUrl='http://149.129.222.131:9999/api/api/customer/load-personal-info?'
        # 获取用户基础信息
        self.userUrl='http://149.129.222.131:9999/api/api/customer/load-basic-info?'
        # 放款信息
        self.loanurl='http://149.129.222.131:9999/api/api/finance/loanIssue?'
        # 还款信息
        self.deposurl='http://149.129.222.131:9999/api/api/finance/deposit?'
        #验证码连接
        self.catpch='http://149.129.222.131:9999/api/auth/captcha?width=120&height=50&serialId=svysoP6G'
        self.login = 'http://149.129.222.131:9999/api/auth/login'

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

    # 放款时间
    def reqLaninfo(self, status,offset,limit,filename):
        dataformat = {
            "loanStatus": status,
            "offset": offset,
            "limit": limit,
            "startTime": "2019-08-31",
            "endTime": "2019-10-01"
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl = self.loanurl + data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)

        print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        # 放款编号、贷款编号，贷款状态、用户名、手机、创建时间
        totalcount = content['paginator']['totalCount']
        a={}
        a['totalcount'] = totalcount
        loanlist = []
        for i in content['item']:
            loandic = {}
            loandic['放款编号'] = i['orderNo']
            loandic['贷款编号'] = i['loanAppId']
            loandic['贷款状态'] = status
            loandic['用户姓名'] = i['realName']
            loandic['手机号'] = i['mobile']
            loandic['创建时间'] = i['createTime']
            loandic['用户编号'] = i['customerId']
            loanlist.append(loandic)

        with open(filename, 'a', newline='') as f:
            head = ['用户编号', '用户姓名', '手机号', '放款编号', '贷款编号', '贷款状态', '创建时间'
                    ]
            writer = csv.DictWriter(f, head)
            for item in loanlist:
                writer.writerow(item)
            f.close()
        return a


    def loanaction(self,filename,limit):
        filename1 = filename + 'loan.csv'
        with open(filename1, 'w') as f:
            #放款编号、贷款编号，贷款状态、用户名、手机、创建时间
            head = ['用户编号', '用户姓名', '手机号', '放款编号','贷款编号','贷款状态','创建时间'
                    ]
            writer = csv.DictWriter(f, head)
            writer.writeheader()
        # basereq.headers['Cookie'] = sys.argv[1]
        paras=['PAID_OFF','OVERDUE']
        for i in paras:
            baseinfo = basereq.reqLaninfo(i,0, 10,filename1)
            offset = 10
            totalCount = baseinfo['totalcount']
            threadlist = []
            while offset <= totalCount:
                # basereq.userInfo(contact_list, filename)
                t = threading.Thread(target=basereq.reqLaninfo,args=(i,offset, limit,filename1,))
                offset = offset + limit
                threadlist.append(t)

            n = 0
            for m in threadlist:
                m.setDaemon(True)
                m.start()
                if n > 10:
                    m.join()
                    n = 0
                n = n + 1
            m.join()





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
    basereq.loanaction(filename, 200)

