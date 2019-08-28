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
            "Referer": "http://149.129.222.131:9999/",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "X-ADMIN- TOKEN": "eyJsb2NhbGUiOiJ6aF9DTiIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiJZaW5nIiwiZXhwIjoxNTY2ODgyMzg1fQ.pYVtcUzyqwvom9OPdJXK9eu_PBiyKgRMcKI-oHWf3UaPx89-87fyJXWhQCZvZUwfNCZlxlLduU8sZYog9pUHRg"
        }

        # 自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)
        # self.headers = {
        #     "Host": " adminweb.adminrichboxbox.com",
        #     "User-Agent": " Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
        #     "Accept": " */*",
        #     "Accept-Language": " en-US,en;q=0.5",
        #     "Accept-Encoding": " gzip, deflate, br",
        #     "Referer": " https://adminweb.adminrichboxbox.com/",
        #     "X-ADMIN-TOKEN": " eyJsb2NhbGUiOiJpbl9JRCIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiIwMTQiLCJleHAiOjE1NjY0NDkyMzR9.i_OePk7yGoOsc_q_oYrgMeUc2yp-3Ir46E0JV20sbjk3ZATe0AvWUOKxlkQTo03bJ66PqACcQ9M_7aseeHS4Hg",
        #     "Connection": " keep-alive",
        #     "Pragma": " no-cache",
        #     "Cache-Control": " no-cache"
        # }
        # 定义请求连接
        # self.baseurl = 'http://149.129.222.131:9999/api/api/customer/load-customers?'
        # self.userUrl = 'http://149.129.222.131:9999/api/api/customer/load-personal-info?'
        # self.basicUrl = 'http://149.129.222.131:9999/api/api/customer/load-basic-info?'
        # self.realpayUrl = 'http://149.129.222.131:9999/api/api/finance/customer/deposit-history?'
        # self.loadUrl = 'http://149.129.222.131:9999/api/api/finance/customer/issue-history?'
        self.payurl = 'http://149.129.222.131:9999/api/api/finance/deposit?'
        self.loanurl = 'http://149.129.222.131:9999/api/api/finance/loanIssue?'

        # 验证码连接
        self.catpch = 'http://149.129.222.131:9999/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        self.login = 'http://149.129.222.131:9999/api/auth/login'
        # self.baseurl='https://adminweb.adminrichboxbox.com/api/api/collection/my?'
        # self.userUrl='https://adminweb.adminrichboxbox.com/api/api/review/personalInfo?'
        # self.loadUrl='https://adminweb.adminrichboxbox.com/api/api/collection/collection-loan-detail?'
        # #验证码连接
        # self.catpch='https://adminweb.adminrichboxbox.com/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        # self.login = 'https://adminweb.adminrichboxbox.com/api/auth/login'

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
            "limit": limit,
            "startTime": "2019-07-01",
            "endTime": "2019-09-01"
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

    def payinfo(self, offset, limit):
        dataf = {
            "offset": offset,
            "limit": limit,
            "startTime": "2019-07-01",
            "endTime": "2019-09-01"
        }
        data = urllib.parse.urlencode(dataf)
        url = self.payurl + data
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

    def loanaction(self, offset, limit, filename):
        faillist = 0
        loanlist = []
        try:
            print(offset)
            baseinfo = basereq.loaninfo(offset, limit)
            for i in baseinfo['list']:
                loandic = {}
                loandic['用户编号'] = i['customerId']
                loandic['放款编号'] = i['issueAmount']
                loandic['贷款编号'] = i['loanAppId']
                loandic['贷款状态'] = i['loanStatus']['value']
                loandic['用户姓名'] = i['realName']
                loandic['手机'] = i['mobile']
                loandic['放款状态'] = i['loanIssueStatus']['value']
                loandic['放款金额'] = i['issueAmount']
                loandic['支付公司流水号'] = i['outTransactionId']
                loandic['放款渠道'] = i['disbursementMethod']
                loandic['银行卡号'] = i['bankcardNo']
                loandic['客户银行卡分行名称'] = i['bankCode']
                loandic['已验证的银行卡用户名'] = i['verifyAccountHolderName']
                loandic['银行名'] = i['bankcardAccountNo']
                loandic['银行卡验证状态'] = i['verifyStatus']['value']
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

    def payaction(self, offset, limit, filename):
        faillist = 0
        paylist = []
        try:
            baseinfo2 = basereq.payinfo(offset, limit)
            for i in baseinfo2['list']:
                paydic = {}
                paydic['用户编号'] = i['customerId']
                paydic['还款编号'] = i['orderNo']
                paydic['贷款编号'] = i['loanAppId']
                paydic['用户姓名'] = i['realName']
                paydic['手机'] = i['mobile']
                paydic['交易状态'] = i['depositStatus']['value']
                paydic['还款码(VA)'] = i['paymentCode']
                paydic['还款金额'] = i['depositAmount']
                paydic['实收金额'] = i['arrivedAmount']
                paydic['清算金额'] = i['clearedAmount']
                paydic['支付公司流水号'] = i['outTransactionId']
                paydic['支付渠道'] = i['depositChannel']
                paydic['还款渠道'] = i['source']
                paydic['还款码操作员'] = i['operator']
                paydic['还款方式'] = i['depositMethod']
                paydic['创建时间'] = i['createTime']
                paydic['还款到账时间'] = i['reachedTime']
                paylist.append(paydic)
        except Exception as e:
            print(e)
        with open(filename, 'a', newline='') as f:
            head = ['用户编号', '还款编号', '贷款编号', '用户姓名', '手机', '交易状态', '还款码(VA)', '还款金额', '实收金额', '清算金额', '支付公司流水号', '支付渠道',
                    '还款渠道', '还款码操作员', '还款方式', '创建时间', '还款到账时间']
            writer = csv.DictWriter(f, head)
            for item in paylist:
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
        baseinfo = basereq.payinfo(offset, 10)
        # print(baseinfo)
        totalCount = baseinfo['totalcount']
        threadlist = []
        while offset <= totalCount:
            print('offset:', offset)
            # Connect.loanaction(offset, limit, totalCount, filename)
            t = threading.Thread(target=basereq.payaction, args=(offset, limit, filename,))
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
