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
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "adminweb.adminrichboxbox.com",
            "Pragma": "no-cache",
            "Referer": "https://adminweb.adminrichboxbox.com/",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "X-ADMIN- TOKEN": "eyJsb2NhbGUiOiJ6aF9DTiIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiJZaW5nIiwiZXhwIjoxNTY2ODgyMzg1fQ.pYVtcUzyqwvom9OPdJXK9eu_PBiyKgRMcKI-oHWf3UaPx89-87fyJXWhQCZvZUwfNCZlxlLduU8sZYog9pUHRg"
        }

        # 自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        # 定义请求连接
        self.loanurl = 'https://adminweb.adminrichboxbox.com/api/api/collection/my?'
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
        print(login.get_full_url())
        response = self.opener.open(login)
        response.close()


    def loaninfo(self, offset, limit,Status):
        dataf = {
            "offset": offset,
            "limit": limit,
            "collectionTaskStatus": Status
            # "startTime": "2019-07-01",
            # "endTime": "2019-09-01"
        }
        data = urllib.parse.urlencode(dataf)
        url = self.loanurl + data
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


    def loanaction(self, offset, limit, filename,Status):
        faillist = 0
        loanlist = []
        try:
            print(offset)
            baseinfo = basereq.loaninfo(offset, limit,Status)
            for i in baseinfo['list']:
                loandic = {}
                loandic['贷款编号'] = i['loanAppId']
                loandic['用户姓名'] = i['realName']
                loandic['手机'] = i['mobile']
                loandic['应还款日期'] = i['dueDate']
                loandic['还款日期'] = i['depositTime']
                loandic['逾期天数'] = i['overdueDays']
                loanlist.append(loandic)
        except Exception as e:
            faillist = offset
            print(e)
        with open(filename, 'a', newline='') as f:
            head = [ '贷款编号', '用户姓名', '手机', '应还款日期', '还款日期', '逾期天数']
            writer = csv.DictWriter(f, head)
            for item in loanlist:
                writer.writerow(item)
            f.close()


    def action(self, limit,file,Status):
        now = datetime.datetime.now()
        format = "%Y-%m-%d-%H-%M-%S"
        filename = file + now.strftime(format) + '.csv'
        with open(filename, 'w') as f:
            head = [ '贷款编号', '用户姓名', '手机', '应还款日期', '还款日期', '逾期天数']
            writer = csv.DictWriter(f, head)
            writer.writeheader()


        offset = 0
        baseinfo = basereq.loaninfo(offset, 10,Status)
        # print(baseinfo)
        totalCount = baseinfo['totalcount']
        threadlist = []
        while offset <= totalCount:
            print('offset:', offset)
            # Connect.loanaction(offset, limit, totalCount, filename)
            # t = threading.Thread(target=basereq.loanaction, args=(offset, limit, filename,Status,))
            # t = Process(target=basereq.payaction, args=(offset, limit, filename,))
            basereq.loanaction(offset, limit, filename,Status)
            offset = offset + limit
        #     threadlist.append(t)
        # n = 0
        # for i in threadlist:
        #     i.setDaemon(True)
        #     i.start()
        #     if n > 10:
        #         i.join()
        #         n = 0
        #     n = n + 1
        # i.join()

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
    file1=userdataf['mobile']+"success"
    # t1=Process(target=basereq.action,args=(200,file,'PROCESSED',))
    file2 = userdataf['mobile'] + "failed"
    basereq.action(200,file1,'PROCESSED')
    basereq.action(200, file2, 'PROCESS_FAILED')
    # t2 = Process(target=basereq.action, args=(200, file1, 'PROCESS_FAILED',))
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()