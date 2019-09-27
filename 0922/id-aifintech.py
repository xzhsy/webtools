#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket,datetime
import urllib.request
import csv
import sys
from http import cookiejar
socket.setdefaulttimeout(20)

class Connect(object):
    def __init__(self):
        self.headers = {
            "Host": " adminweb.adminrichboxbox.com",
            "User-Agent": " Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "*/*",
            "Accept-Language": " zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": " gzip, deflate, br",
            "Referer": "https://adminweb.adminrichboxbox.com/collection/my",
            "x-admin-token": " eyJsb2NhbGUiOiJ6aF9DTiIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiIwMDkiLCJleHAiOjE1NjkwNDI3MDh9.B9Q6ZGi8b05eYJBwSLNWW19q70zTpeizKLe8c3B_xsHi6RO1GEAfbvyBAfYybU4Z30irzlbjYsW002AO4Q9ScA",
            "origin": " https://adminweb.adminrichboxbox.com",
            "Connection": "keep-alive"
        }
        #自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        #定义请求连接
        self.baseurl='https://lmt-man.id-aifintech.cc/cs/collection/getTotalList?flag=member'
        self.userUrl='https://adminweb.adminrichboxbox.com/api/api/review/personalInfo?'
        self.loadUrl='https://adminweb.adminrichboxbox.com/api/api/collection/collection-loan-detail?'
        #登陆连接
        self.login = 'https://lmt-man.id-aifintech.cc/cs/j_spring_security_check'

    def loginaction(self,userdataf):
        userdata = urllib.parse.urlencode(userdataf).encode(encoding='UTF8')
        login = urllib.request.Request(self.login, method='POST', data=userdata, headers=self.headers)
        response = self.opener.open(login)
        response.close()

    def reqbase(self,nexta,limit,status):
        offset=nexta
        limit=limit
        dataformat = {
            "offset": offset,
            "collectionTaskStatus": status,
            "limit": limit
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl=self.baseurl+data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)
        userinfo=[]
        infodic={}
        print(request.full_url)
        response = self.opener.open(request)
        # print(data)
        contentb = str(response.read(), encoding='utf-8')
        # print(contentb)
        content = json.loads(contentb, strict=False)
        response.close()
        infodic['totalCount'] = content['paginator']['totalCount']
        infodic['offset'] = content['paginator']['offset']
        for i in  content['item']:
            midinfo = {}
            midinfo['入催时间'] = i['createTime']
            midinfo['客户名称'] = i['chname']
            midinfo['手机号码'] = i['mobile']
            midinfo['出崔时间'] = i['outDate']
            midinfo['应还日期'] = i['dueDate']
            midinfo['最大逾期天数'] = i['hisMaxOverdueDays']
            midinfo['任务状态'] = i['collectionTaskStatus']['value']
            midinfo['身份证号'] = i['idNumber']
            userinfo.append(midinfo)
        with open(filename, 'a',newline='') as f:
            #贷款编号、任务状态、应还款日、还款时间、用户姓名、手机、申请状态、逾期天数
            head = ['客户名称', '手机号码', '入催时间', '出崔时间', '应还日期', '最大逾期天数', '身份证号', '业务状态'
                    ]
            writer = csv.DictWriter(f, head)
            for item in userinfo:
                writer.writerow(item)
            f.close()
        return infodic

if __name__ == '__main__':
    now = datetime.datetime.now()
    format = "%Y-%m-%d-%H-%M-%S"

    basereq = Connect()
    userdataf = {}
    if len(sys.argv) >= 2:
        userdataf['j_username'] = sys.argv[1]
        userdataf['j_password'] = sys.argv[2]
    else:
        userdataf['j_username'] = input('输入用户名： ')
        userdataf['j_password'] = input('输入密码： ')
    basereq.loginaction(userdataf)
    filename=userdataf['mobile']+ '-' + now.strftime(format) + '.csv'
    with open(filename, 'w') as f:
        head = ['客户名称', '手机号码', '入催时间', '出崔时间', '应还日期', '最大逾期天数', '身份证号', '业务状态'
                ]
        ##客户名称、入催时间、出崔时间、身份证号、手机号码、应还日期、最大逾期天数、业务状态
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    # basereq.headers['Cookie'] = sys.argv[1]
    args=['PROCESSED','PROCESS_FAILED','CANCELED']
    for i in args:
        baseinfo = basereq.reqbase(0, 10,i)
        offset = baseinfo['offset'] + 10
        totalCount = baseinfo['totalCount']
        while offset <= totalCount:
            baseinfo = basereq.reqbase(offset, 100,i)
            offset = offset + 100
