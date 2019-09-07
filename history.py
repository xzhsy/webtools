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
        # 自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)
        self.headers = {
            "Host": " adminweb.adminrichboxbox.com",
            "User-Agent": " Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept": " */*",
            "Accept-Language": " en-US,en;q=0.5",
            "Accept-Encoding": " gzip, deflate, br",
            "Referer": " https://adminweb.adminrichboxbox.com/",
            "X-ADMIN-TOKEN": "eyJsb2NhbGUiOiJ6aF9DTiIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiIwMTUiLCJleHAiOjE1Njc5NDI2NzJ9.D45Is5C8Uwm4JzKCG9ux0TUiC9t1Hm_mgfFcPsnXHavH3h64wBipmU63ZqJBpUxafiOVsZVWoz1MgFmAhNcmog",
            "Connection": " keep-alive",
            "Pragma": " no-cache",
            "Cache-Control": " no-cache"
        }
        # 定义请求连接
        self.overdueurl = 'https://adminweb.adminrichboxbox.com/api/api/review/loanAppAssignedHistory?'

        # 验证码连接
        self.catpch = 'https://adminweb.adminrichboxbox.com/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        self.login = 'https://adminweb.adminrichboxbox.com/api/auth/login'


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



    def overdueinfo(self, offset, limit):
        dataf = {
            "offset": offset,
            "limit": limit
        }
        data = urllib.parse.urlencode(dataf)
        url = self.overdueurl + data
        request = urllib.request.Request(url=url, method='GET')
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        totalcount = content['paginator']['totalCount']
        infodic = {}
        infodic['totalcount'] = totalcount
        infodic['list'] = content['item']
        return infodic


    def overdueaction(self, offset, limit, filename):
        faillist = []
        overduelist = []
        try:
            print(offset)
            baseinfo = basereq.overdueinfo(offset, limit)
            for i in baseinfo['list']:
                overdue = {}
                overdue['贷款编号'] = i['loanAppId']
                overdue['用户姓名'] = i['realName']
                overdue['手机号'] = i['mobile']
                overdue['放款时间'] = i['issueDate']
                overdue['还款时间'] = i['dueDate']
                overdue['逾期天数'] = i['overdueDays']
                overduelist.append(overdue)
        except Exception as e:
            faillist.append(offset)
            print(e)
        with open(filename, 'a', newline='') as f:
            head = ['用户编号', '贷款编号', '用户姓名', '手机号', '放款时间', '还款时间', '逾期天数']
            writer = csv.DictWriter(f, head)
            for item in overduelist:
                writer.writerow(item)
            f.close()
        print(faillist)

    def dueaction(self, limit,file):
        now = datetime.datetime.now()
        format = "%Y-%m-%d-%H-%M-%S"
        filename2 = file + now.strftime(format) + '.csv'
        head2 = ['用户编号', '贷款编号', '用户姓名', '手机号', '放款时间', '还款时间', '逾期天数']
        with open(filename2, 'w') as f:
            writer = csv.DictWriter(f, head2)
            writer.writeheader()
        offset = 0
        baseinfo = basereq.overdueinfo(offset, 10)
        # print(baseinfo)
        totalCount = baseinfo['totalcount']
        threadlist = []
        while offset <= totalCount:
            print('offset:', offset)
            t = threading.Thread(target=basereq.overdueaction, args=(offset, limit, filename2,))
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
    basereq = Connect()
    userdataf = {}
    if len(sys.argv) >= 2:
        userdataf['mobile'] = sys.argv[1]
        userdataf['password'] = sys.argv[2]
    else:
        userdataf['mobile'] = input('输入用户名： ')
        userdataf['password'] = input('输入密码： ')
    basereq.loginaction(userdataf)
    # basereq.action(200)
    t1 = Process(target=basereq.action,args=(200,))
    t1.start()
    t1.join()


