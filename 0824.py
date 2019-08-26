#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket,datetime
import urllib.request
import csv
import sys
from http import cookiejar
# socket.setdefaulttimeout(20)
class Connect(object):
    def __init__(self):
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)
        self.baseurl="https://api.kreditq.id/orderapi/v1/loan-order/get-repayment-list"
        self.headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Referer": "https://pubs.kreditq.id/KreditQ/index.html",
        "Sec-Fetch-Mode": "cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }
    def get_token(self):
        login = 'https://api.kreditq.id/orderapi/v1/order-user/login'
        passf = {
            "name": "doni",
            "password": "1234567"
        }
        passd = json.dumps(passf).encode('utf8')
        request = urllib.request.Request(url=login, method='POST',
                 headers=self.headers,data=passd)
        print(request.full_url)
        print(request.data,request.get_method())
        response = urllib.request.urlopen(request)
        # print(data)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb)
        tokens=content['data']['accessToken']
        response.close()
        print(tokens)
        return tokens

    def totale(self,token):
        dataformat = {
            "number": 0,
            "size": 10
        }
        self.headers['token'] = token
        data1 = json.dumps(dataformat)
        data3 = data1.encode('utf8')
        print(data1)
        request = urllib.request.Request(url=self.baseurl, method='POST',
                                         headers=self.headers,data=data3)
        print(request.full_url)
        print(request.data,request.get_method())
        response = urllib.request.urlopen(request)
        # print(data)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb)
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
        request = urllib.request.Request(url=self.baseurl, method='POST',
                                         headers=self.headers,data=data3)
        print(request.full_url)
        print(request.data,request.get_method())
        response = urllib.request.urlopen(request)
        # print(data)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb)
        print(type(contentb))
        # print(content['data'])
        # print(content['totalElements'])
        # content = json.loads(contentb, strict=False)
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
                        head = ['工单id', '借款类型', '用户姓名', 'KTP身份证号','手机号', '应还金额','放款时间', '计划还款日', '还款时间', '实还金额','还款状态','逾期天数','逾期金额','借款金额','借款期限','当前期限'
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
    filename='userinfo' + now.strftime(format)
    with open(filename, 'w') as f:
        head = ['工单id', '借款类型', '用户姓名', 'KTP身份证号','手机号', '应还金额','放款时间', '计划还款日', '还款时间', '实还金额','还款状态','逾期天数','逾期金额','借款金额','借款期限','当前期限'
                ]
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    basereq = Connect()
    number = 0
    token=basereq.get_token()
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
    # userdataf = {}
    # userdataf['mobile'] = sys.argv[1]
    # userdataf['password'] = sys.argv[2]
    # basereq.loginaction(userdataf)
    # # basereq.headers['Cookie'] = sys.argv[1]
    # baseinfo = basereq.reqbase(0, 10)
    # offset = baseinfo['offset'] + 10
    # totalCount = baseinfo['totalCount']
    # contact_list = baseinfo['list']
    # basereq.userInfo(contact_list,filename)
    # while offset <= totalCount:
    #     baseinfo = basereq.reqbase(offset, 10)
    #     contact_list = baseinfo['list']
    #     basereq.userInfo(contact_list,filename)
    #     offset = offset + 10
