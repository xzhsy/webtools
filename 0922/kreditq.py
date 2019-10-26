#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket,datetime
import urllib.request
import csv
import requests
from http import cookiejar
# socket.setdefaulttimeout(20)
class Connect(object):
    def __init__(self):
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)
        self.baseurl="https://super.kreditq.id/orderapi/v1/loan-order/get-repayment-list"
        self.headers = {
            "Host": "super.kreditq.id",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://pubs.kreditq.id/KreditQ/index.html",
            "Content-Type": "application/json;charset=utf-8",
            "Content-Length": "36",
            "Origin": "https://pubs.kreditq.id",
            "Connection": "keep-alive", }
        self.opurl='https://super.kreditq.id/orderapi/v1/loan-order/get-repayment-list'
        self.opheader={
            "Host": "super.kreditq.id",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,token",
            "Origin": "https://pubs.kreditq.id",
            "Connection": "keep-alive"
        }
    def get_token(self):
        login = 'https://super.kreditq.id/orderapi/v1/order-user/login'
        passf = {
            "name": "doni",
            "password": "1234567"
        }
        passd = json.dumps(passf).encode('utf8')
        logreq=requests.options(url='https://super.kreditq.id/orderapi/v1/order-user/login',headers=self.opheader)
        print(logreq.status_code)
        reponse = requests.post(url=login,
                 headers=self.headers,data=passd)
        # print(reponse.text)
        print(reponse.status_code )
        content = json.loads(reponse.text)
        tokens=content['data']['accessToken']
        print(tokens)
        return tokens

    def totale(self,token):
        dataformat = {
            "number": 0,
            "size": 10,
            "endTime": "2019-10-10 23:59:59",
            "startTime":"2019-09-01 00:00:00"
        }
        self.headers['token'] = token
        data1 = json.dumps(dataformat)
        data3 = data1.encode('utf8')
        print(data1)
        logreq=requests.options(url='https://super.kreditq.id/orderapi/v1/order-user/login',headers=self.opheader)
        print(logreq.status_code)
        response = requests.post(url=self.baseurl,
                                         headers=self.headers,data=data3)
        print(response.status_code)
        print(response.text)
        content = json.loads(response.text)
        print(content)
        response.close()
        totalcount=content['data']['totalElements']
        print(totalcount)
        return totalcount

    def reqbase(self,number,token):
        dataformat = {
            "number": number,
            "size": 100
        }
        self.headers['token'] = token
        data1 = json.dumps(dataformat)
        data3 = data1.encode('utf8')
        print(data1)
        logreq=requests.options(url='https://super.kreditq.id/orderapi/v1/order-user/login',headers=self.opheader)
        print(logreq.status_code)
        response = requests.post(url=self.baseurl,
                                         headers=self.headers,data=data3)
        # print(data)
        print(response.text)
        print(response.status_code)
        content = json.loads(response.text)
        response.close()
        contact_list = content['data']['content']
        faillist=[]
        while len(contact_list) != 0 or len(faillist) !=0:
            try:
                if len(contact_list) == 0:
                    contact_list = faillist
                for i in contact_list:
                    userinfo = []
                    # print(i)
                    baseuser={}
                    baseuser['工单id'] = i['orderNo']
                    baseuser['借款类型'] = i['loanType']
                    baseuser['用户姓名'] = i['name']
                    baseuser['KTP身份证号'] = i['ktp']
                    baseuser['手机号'] = i['phone']
                    baseuser['应还金额'] = i['totalRepaymentAmount']
                    baseuser['放款时间'] = i['gmtCreate']
                    baseuser['计划还款日'] = i['repaymentDate']
                    baseuser['还款时间'] = i['realRepaymentDate']
                    baseuser['实还金额'] = i['realRepaymentAmount']
                    baseuser['还款状态'] = i['state']
                    baseuser['逾期天数'] = i['overdueDay']
                    baseuser['逾期金额'] = i['overdueFee']
                    baseuser['借款金额'] = i['balance']
                    baseuser['借款期限'] = i['period']
                    baseuser['当前期限'] = i['loanDay']
                    userinfo.append(baseuser)
                    if i in faillist:
                        faillist.remove(i)
                    if i in contact_list:
                        contact_list.remove(i)
                    with open(filename, 'a',newline='') as f:
                        head = ['工单id', '借款类型', '用户姓名', 'KTP身份证号',
'手机号', '应还金额','放款时间', '计划还款日', '还款时间', '实还金额','还款状态'
,'逾期天数','逾期金额','借款金额','借款期限','当前期限'
                                ]
                        writer = csv.DictWriter(f, head)
                        for item in userinfo:
                            writer.writerow(item)
                        f.close()
            except ConnectionResetError as e:
                faillist.append(i)
                print(e)
            except socket.timeout as e:
                faillist.append(i)
                print(e)
            except Exception as e:
                faillist.append(i)
                print(e)
            except TypeError as e:
                print(e)


if __name__ == '__main__':
    now = datetime.datetime.now()
    format = "%Y-%m-%d-%H-%M-%S"
    basereq = Connect()
    number = 0
    token=basereq.get_token()
    filename='doni-' + now.strftime(format) + '.csv'
    with open(filename, 'w') as f:
        head = ['工单id', '借款类型', '用户姓名', 'KTP身份证号','手机号', '应还金额','放款时间', '计划还款日', '还款时间', '实还金额','还款状态','逾期天数','逾期金额','借款金额','借款期限','当前期限'
                ]
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    total = basereq.totale(token)
    number2 = 0
    while number2 <= total:
        try:
            basereq.reqbase(number,token)
            number2 = number2 + 100
            number = number + 1
        except Exception as e:
            token=basereq.get_token()
            print(e)

