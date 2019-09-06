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
            "Host": "149.129.222.131:9999",
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
        try:
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
        except Exception as e:
            print("登陆失败：", e)

    def loaninfo(self, offset, limit):
        dataf = {
            "offset": offset,
            "limit": limit
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


    def loanaction(self, offset, limit, filename):
        faillist = 0
        loanlist = []
        try:
            print(offset)
            baseinfo = basereq.loaninfo(offset, limit)
            for i in baseinfo['list']:
                loandic = {}
                loandic['贷款编号'] = i['loanAppId']
                loandic['用户姓名'] = i['realName']
                loandic['手机'] = i['mobile']
                loandic['还款时间'] = i['dueDate']
                loandic['支付公司流水号'] = i['outTransactionId']
                loandic['放款渠道'] = i['disbursementMethod']
                loandic['创建时间'] = i['createTime']
                loanlist.append(loandic)
        except Exception as e:
            faillist = offset
            print(e)
        with open(filename, 'a', newline='') as f:
            head = ['用户编号', '放款编号', '贷款编号', '贷款状态', '用户姓名', '手机', '放款状态', '放款金额', '支付公司流水号', '放款渠道', '银行卡号',
                    '客户银行卡分行名称', '已验证的银行卡用户名', '银行名', '银行卡验证状态', '创建时间']
            writer = csv.DictWriter(f, head)
            for item in loanlist:
                writer.writerow(item)
            f.close()

    # def action(self, limit):
    #     now = datetime.datetime.now()
    #     format = "%Y-%m-%d-%H-%M-%S"
    #     filename = 'loan' + now.strftime(format) + '.csv'
    #     with open(filename, 'w') as f:
    #         head = ['用户编号', '放款编号', '贷款编号', '贷款状态', '用户姓名', '手机', '放款状态', '放款金额', '支付公司流水号', '放款渠道', '银行卡号',
    #                 '客户银行卡分行名称', '已验证的银行卡用户名', '银行名', '银行卡验证状态', '创建时间']
    #         writer = csv.DictWriter(f, head)
    #         writer.writeheader()
    #
    #
    #     offset = 0
    #     baseinfo = basereq.loaninfo(offset, 10)
    #     # print(baseinfo)
    #     totalCount = baseinfo['totalcount']
    #     threadlist = []
    #     while offset <= totalCount:
    #         print('offset:', offset)
    #         # Connect.loanaction(offset, limit, totalCount, filename)
    #         t = threading.Thread(target=basereq.loanaction, args=(offset, limit, filename,))
    #         # basereq.loanaction(offset, limit, filename)
    #         offset = offset + limit
    #         threadlist.append(t)
    #     n = 0
    #     for i in threadlist:
    #         i.setDaemon(True)
    #         i.start()
    #         if n <= 10:
    #             i.join()
    #             n = 0
    #         n = n + 1
    def action(self, limit):
        now = datetime.datetime.now()
        format = "%Y-%m-%d-%H-%M-%S"
        filename = 'pay' + now.strftime(format) + '.csv'
        with open(filename, 'w') as f:
            head = ['用户编号', '还款编号', '贷款编号', '用户姓名', '手机', '交易状态', '还款码(VA)', '还款金额', '实收金额', '清算金额', '支付公司流水号', '支付渠道',
                    '还款渠道', '还款码操作员', '还款方式', '创建时间', '还款到账时间']
            writer = csv.DictWriter(f, head)
            writer.writeheader()


        offset = 0
        baseinfo = basereq.loaninfo(offset, 10)
        # print(baseinfo)
        totalCount = baseinfo['totalcount']
        threadlist = []
        while offset <= totalCount:
            print('offset:', offset)
            # Connect.loanaction(offset, limit, totalCount, filename)
            t = threading.Thread(target=basereq.loanaction, args=(offset, limit, filename,))
            # t = Process(target=basereq.payaction, args=(offset, limit, filename,))
            # basereq.loanaction(offset, limit, filename)
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
    basereq.action(200)
    # threadlist = []
    #
    # for i in [2, 3, 4, 5]:
    #     t = threading.Thread(target=basereq.action, args=(i, 10,))
    #     # t = Process(target=basereq.action, args=(i, 10,))
    #     threadlist.append(t)
    # for i in threadlist:
    #     i.setDaemon(True)
    #     i.start()
    # i.join()
