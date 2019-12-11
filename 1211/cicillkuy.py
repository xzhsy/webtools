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
            "Host": " adminweb.cicillkuy.com",
            "User-Agent": " Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "*/*",
            "Accept-Language": " zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": " gzip, deflate, br",
            "Referer": "https://adminweb.cicillkuy.com/collection/my",
            "origin": " https://adminweb.cicillkuy.com",
            "Connection": "keep-alive"
        }
        #自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        #定义请求连接
        #https://adminweb.cicillkuy.com/api/api/collection/my?collectionTaskStatus=CREATED&dueDateFrom=2019-11-15&dueDateTo=2019-12-11&offset=0&limit=10
        self.baseurl='https://adminweb.cicillkuy.com/api/api/collection/my?'
        self.userUrl='https://adminweb.cicillkuy.com/api/api/review/personalInfo?'
        self.loadUrl='https://adminweb.cicillkuy.com/api/api/collection/collection-loan-detail?'
        #验证码连接
        self.catpch='https://adminweb.cicillkuy.com/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        self.login = 'https://adminweb.cicillkuy.com/api/auth/login'

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

    def reqbase(self,nexta,limit,startstr,endstr):
        offset=nexta
        limit=limit
        dataformat = {
            "offset": offset,
            "dueDateFrom": startstr,
            "dueDateTo" : endstr,
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
            midinfo['贷款编号'] = i['loanAppId']
            midinfo['用户姓名'] = i['realName']
            midinfo['手机号'] = i['mobile']
            midinfo['还款时间'] = i['depositTime']
            midinfo['应还款日期'] = i['dueDate']
            midinfo['逾期天数'] = i['overdueDays']
            midinfo['任务状态'] = i['collectionTaskStatus']['value']
            midinfo['申请状态'] = i['loanAppStatus']['value']
            userinfo.append(midinfo)
        with open(filename, 'a',newline='') as f:
            #贷款编号、任务状态、应还款日、还款时间、用户姓名、手机、申请状态、逾期天数
            head = ['用户姓名', '手机号', '贷款编号','应还款日期','还款时间','逾期天数','任务状态','申请状态'
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
        userdataf['mobile'] = sys.argv[1]
        userdataf['password'] = sys.argv[2]
    else:
        userdataf['mobile'] = input('输入用户名： ')
        userdataf['password'] = input('输入密码： ')
    startstr = input('输入开始日期： ')
    endstr = input('输入结束日期： ')
    basereq.loginaction(userdataf)
    filename=userdataf['mobile']+ '-' + now.strftime(format) + '.csv'
    with open(filename, 'w') as f:
        head = ['姓名', '手机号', '贷款编号', '应还款日期', '还款时间', '逾期天数', '任务状态', '申请状态'
                ]
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    # basereq.headers['Cookie'] = sys.argv[1]

    baseinfo = basereq.reqbase(0, 10,startstr,endstr)
    offset = baseinfo['offset'] + 10
    totalCount = baseinfo['totalCount']
    while offset <= totalCount:
        baseinfo = basereq.reqbase(offset, 100,startstr,endstr)
        offset = offset + 100
