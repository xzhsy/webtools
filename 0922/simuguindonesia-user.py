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
            "Host": "adminweb.simuguindonesia.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://adminweb.simuguindonesia.com/collection/my",
            "origin": "https://adminweb.simuguindonesia.com",
            "Connection": "keep-alive"
        }
        #自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        #定义请求连接 全部客户
        self.baseurl='https://adminweb.simuguindonesia.com/api/api/customer/load-customers?'
        self.userurl='https://adminweb.simuguindonesia.com/api/api/customer/load-basic-info?'
        self.dueurl='https://adminweb.simuguindonesia.com/api/api/finance/customer/deposit-history?'
        self.loadUrl='https://adminweb.simuguindonesia.com/api/api/finance/customer/issue-history?'
        #验证码连接
        self.catpch='https://adminweb.simuguindonesia.com/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        self.login = 'https://adminweb.simuguindonesia.com/api/auth/login'

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

    # def reqbase(self,nexta,limit,status):
    def reqbase(self, nexta, limit):
        offset=nexta
        limit=limit
        dataformat = {
            "offset": offset,
            # "collectionTaskStatus": status,
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
        for i in  content['item']:
            midinfo = {}
            midinfo['用户编号'] = i['customerId']
            midinfo['用户姓名'] = i['realName']
            midinfo['手机号'] = i['mobile']
            midinfo['用户等级'] = i['customerGrade']
            midinfo['注册时间'] = i['registerTime']
            midinfo['状态'] = i['status']['value']
            userinfo.append(midinfo)
        infodic['list'] = userinfo
        return infodic

    def personinfo(self, customerId):
        dataf = {
            "customerId": customerId
        }
        data = urllib.parse.urlencode(dataf)
        url = self.userurl + data
        request = urllib.request.Request(url=url, method='GET')
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        personinfo = {}
        if content:
            personinfo['手机号2'] = content['mobile']
        else:
            personinfo['手机号2'] = ''
        return personinfo

    def dueinfo(self, customerId):
        dataf = {
            "customerId": customerId
        }
        data = urllib.parse.urlencode(dataf)
        url = self.dueurl + data
        request = urllib.request.Request(url=url, method='GET')
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        duelist = []
        if content:
            for i in content:
                dueinfo = {}
                dueinfo['还款-贷款编号'] = i['loanAppId']
                dueinfo['还款-交易状态'] = i['depositStatus']['value']
                dueinfo['还款-创建时间'] = i['createTime']
                duelist.append(dueinfo)
        else:
            dueinfo = {}
            dueinfo['还款-贷款编号'] = ''
            dueinfo['还款-交易状态'] = ''
            dueinfo['还款-创建时间'] = ''
            duelist.append(dueinfo)
        return duelist

    def loaninfo(self, customerId):
        dataf = {
            "customerId": customerId
        }
        data = urllib.parse.urlencode(dataf)
        url = self.loadUrl + data
        request = urllib.request.Request(url=url, method='GET')
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()

        loanlist = []
        if content:
            for i in content:
                loaninfo = {}
                loaninfo['放款-贷款编号'] = i['loanAppId']
                loaninfo['放款-创建时间'] = i['createTime']
                loanlist.append(loaninfo)
        else:
            loaninfo = {}
            loaninfo['放款-贷款编号'] = ''
            loaninfo['放款-创建时间'] = ''
            loanlist.append(loaninfo)
        return loanlist

    def dueaction(self,userlist,filename):
        try:
            for i in userlist:
                customerId = i['用户编号']
                mob = basereq.personinfo(customerId)
                i.update(mob)
                duelist = basereq.dueinfo(customerId)
                due = []
                for l in duelist:
                    i.update(l)
                    due.append(i)
                with open(filename, 'a',newline='') as f:
                    #贷款编号、任务状态、应还款日、还款时间、用户姓名、手机、申请状态、逾期天数
                    head = ['用户编号', '用户姓名', '手机号','用户等级','注册时间','状态','手机号2','还款-贷款编号','还款-交易状态','还款-创建时间'
                            ]
                    writer = csv.DictWriter(f, head)
                    for item in due:
                        writer.writerow(item)
                    f.close()
        except Exception as e:
            print(e)

    def loanaction(self,userlist,filename2):
        try:
            for l in userlist:
                customerId = l['用户编号']
                mob = basereq.personinfo(customerId)
                l.update(mob)
                loanlist = basereq.loaninfo(customerId)
                baselist = []
                for loa in loanlist:
                    l.update(loa)
                    baselist.append(l)
                with open(filename2, 'a',newline='') as f:
                    #贷款编号、任务状态、应还款日、还款时间、用户姓名、手机、申请状态、逾期天数
                    head = ['用户编号', '用户姓名', '手机号','用户等级','注册时间','状态','手机号2','放款-贷款编号','放款-创建时间'
                            ]
                    writer = csv.DictWriter(f, head)
                    for item in baselist:
                        writer.writerow(item)
                    f.close()
        except Exception as e:
            print(e)

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
    filename=userdataf['mobile']+ '-due' + now.strftime(format) + '.csv'
    with open(filename, 'w') as f:
        head = ['用户编号', '用户姓名', '手机号', '用户等级', '注册时间', '状态', '手机号2', '还款-贷款编号', '还款-交易状态', '还款-创建时间'
                ]
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    filename2=userdataf['mobile']+ '-loan' + now.strftime(format) + '.csv'
    # with open(filename2, 'w') as f:
    #     head = ['用户编号', '用户姓名', '手机号', '用户等级', '注册时间', '状态', '手机号2', '放款-贷款编号',
    #             '放款-创建时间'
    #             ]
    #     writer = csv.DictWriter(f, head)
    #     writer.writeheader()
    # basereq.headers['Cookie'] = sys.argv[1]
    baseinfo = basereq.reqbase(0, 10)
    offset =  0
    totalCount = baseinfo['totalCount']
    while offset <= totalCount:
        baseinfo = basereq.reqbase(offset, 100)
        userlist = baseinfo['list']
        basereq.dueaction(userlist,filename)
        # basereq.loanaction(userlist, filename2)
        offset = offset + 100
    # args=['PROCESSED','PROCESS_FAILED','CANCELED']
    # for i in args:
    #     baseinfo = basereq.reqbase(0, 10,i)
    #     offset = baseinfo['offset'] + 10
    #     totalCount = baseinfo['totalCount']
    #     while offset <= totalCount:
    #         baseinfo = basereq.reqbase(offset, 100,i)
    #         offset = offset + 100
