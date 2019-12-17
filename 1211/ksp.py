#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket, datetime
import urllib.request
import csv
import sys
from http import cookiejar
import threading
from multiprocessing import Process

socket.setdefaulttimeout(20)


class Connect(object):
    def __init__(self):
        # 自定义请求方法，获取cookie https://adminweb.manage.finkredit-ksp.com/
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)
        self.headers = {
            "Host": "adminweb.manage.finkredit-ksp.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept": " */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://adminweb.manage.finkredit-ksp.com/",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        # 定义请求连接
        #应还款url
        self.dueurl = 'http://adminweb.manage.finkredit-ksp.com/api/api/review/loanAppManagement?'
        self.userurl = 'http://adminweb.manage.finkredit-ksp.com/api/api/review/applyHistory?'

        # 验证码连接
        self.catpch = 'https://adminweb.manage.finkredit-ksp.com/api/auth/captcha?width=120&height=50&serialId=8zfSz6LD'
        self.login = 'https://adminweb.manage.finkredit-ksp.com/api/auth/login'


    def loginaction(self, userdataf):
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


    def loaninfo(self, offset, limit,startdate,enddate):
        dataf = {
            "issueSuccessTimeFrom": startdate,
            "issueSuccessTimeTo": enddate,
            "offset": offset,
            "limit": limit
        }
        data = urllib.parse.urlencode(dataf)
        url = self.dueurl + data
        request = urllib.request.Request(url=url, method='GET')
        print(request.get_full_url())
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        totalcount = content['paginator']['totalCount']
        infodic = {}
        infodic['totalcount'] = totalcount
        infodic['list'] = content['item']
        return infodic

    def personinfo(self,contractNo):
        dataf = {
            "contractNo":contractNo
        }
        data = urllib.parse.urlencode(dataf)
        url = self.userurl + data
        request = urllib.request.Request(url=url, method='GET')
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        personinfo = {}
        personlist = []
        if isinstance(content,list):
            for i in content:
                personinfo['历史贷款编号'] = i['id']
                personinfo['历史申请时间'] = i['applyTime']
                personinfo['历史手机号'] = i['mobile']
                personinfo['历史期限'] = i['period']
                personinfo['历史状态'] = i['status']['value']
                personinfo['历史逾期天数'] = i['overdueDays']
                personlist.append(personinfo)
        elif isinstance(content,dict) and  content:
            personinfo['历史贷款编号'] = content['id']
            personinfo['历史申请时间'] = content['applyTime']
            personinfo['历史手机号'] = content['mobile']
            personinfo['历史期限'] = content['period']
            personinfo['历史状态'] = content['status']['value']
            personinfo['历史逾期天数'] = content['overdueDays']
            personlist.append(personinfo)
        else:
            personinfo['历史贷款编号'] = ''
            personinfo['历史申请时间'] = ''
            personinfo['历史手机号'] = ''
            personinfo['历史期限'] = ''
            personinfo['历史状态'] = ''
            personinfo['历史逾期天数'] = ''
            personlist.append(personinfo)
        return personlist

    def loanaction(self, offset, limit, filename,startdate,enddate):
        faillist = []
        loanlist = []
        try:
            print(offset)
            baseinfo = basereq.loaninfo(offset, limit,startdate,enddate)
            for i in baseinfo['list']:
                loandic = {}
                perlist = []
                loandic['贷款编号'] = i['loanAppId']
                loandic['用户姓名'] = i['realName']
                loandic['用户等级'] = i['customerGrade']
                loandic['手机号'] = i['mobile']
                loandic['成功放款时间'] = i['issueSuccessTime']
                loandic['期限'] = i['duration']
                loandic['申请状态'] = i['loanAppStatus']['value']
                contractNo=i['contractNo']
                perlist = basereq.personinfo(contractNo)
                for perdic in perlist:
                    perdic.update(loandic)
                    loanlist.append(perdic)
        except Exception as e:
            faillist.append(offset)
            print(e)
        with open(filename, 'a', newline='') as f:
            head = ['贷款编号', '用户姓名', '用户等级','手机号','成功放款时间', '期限','申请状态','历史贷款编号','历史申请时间','历史手机号','历史期限','历史状态','历史逾期天数']
            writer = csv.DictWriter(f, head)
            for item in loanlist:
                writer.writerow(item)
            f.close()
        print(faillist)


    def action(self, limit,file,startdate,enddate):
        now = datetime.datetime.now()
        format = "%Y-%m-%d-%H-%M-%S"
        filename = file + 'loan' + now.strftime(format) + '.csv'
        head = ['贷款编号', '用户姓名', '用户等级','手机号','成功放款时间', '期限','申请状态','历史贷款编号','历史申请时间','历史手机号','历史期限','历史状态','历史逾期天数']
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, head)
            writer.writeheader()

        offset = 0
        baseinfo = basereq.loaninfo(offset, 10,startdate,enddate)
        # print(baseinfo)
        totalCount = baseinfo['totalcount']
        threadlist = []
        while offset <= totalCount:
            print('offset:', offset)
            t = threading.Thread(target=basereq.loanaction, args=(offset, limit, filename,startdate,enddate,))
            offset = offset + limit
            threadlist.append(t)
        n = 0
        i = ''
        for i in threadlist:
            i.setDaemon(True)
            i.start()
            if n > 3:
                i.join()
                n = 0
            n = n + 1
        i.join()


if __name__ == '__main__':
    basereq = Connect()
    userdataf = {}
    if len(sys.argv) >= 2:
        userdataf['mobile'] = sys.argv[1]
        userdataf['password'] = sys.argv[2]
    else:
        userdataf['mobile'] = input('输入用户名： ')
        userdataf['password'] = input('输入密码： ')
    basereq.loginaction(userdataf)
    startdate = input('输入开始时间:')
    enddate = input('输入查询结束时间:')
    # basereq.action(200)
    file=userdataf['mobile']
    basereq.action(40,file,startdate,enddate)


