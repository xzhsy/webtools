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
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "149.129.222.131:9999",
            "Pragma": "no-cache",
            "Referer": "http://149.129.222.131:9999/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "X-ADMIN- TOKEN": "eyJsb2NhbGUiOiJ6aF9DTiIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiI2MDAwNCIsImV4cCI6MTU2Nzk0NDYzMn0.1X85QY0gwtpSH8K08RwFAK5LVS-nvReAU5zONhHiQiyDCd9v5sWcc6SHR34hIqkxKYiz07QzGyEdf01kE1_yxg"
        }
        #自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)


        #全部客户
        #http://149.129.222.131:9999/api/api/customer/load-customers?offset=0&limit=10
        #定义请求连接
        self.baseurl='http://149.129.222.131:9999/api/api/collection/my?'
        self.userUrl='http://149.129.222.131:9999/api/api/review/personalInfo?'
        self.loadUrl='http://149.129.222.131:9999/api/api/collection/collection-loan-detail?'
        #验证码连接
        self.catpch='http://149.129.222.131:9999/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        self.login = 'http://149.129.222.131:9999/api/auth/login'

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
        itemlist=[]
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
        for i in content['item']:
            itemlist.append(i['contractNo'])
        infodic['list'] = itemlist
        return infodic
    def reqUserinfo(self,contractNo):
        dataformat = {
            "contractNo": contractNo
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl=self.userUrl+data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)
        userdic={}
        # print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        userdic['姓名'] = content['fullName']
        userdic['手机号'] = content['mobile']
        userdic['贷款编号'] = content['loanAppId']
        return  userdic
    def reqLaninfo(self,contractNo):
        dataformat = {
            "contractNo": contractNo
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl=self.loadUrl+data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)
        userdic={}
        # print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        userdic['应还款日期'] = content['dueDate']
        userdic['还款时间'] = content['depositTime']
        userdic['逾期天数'] = content['overdueDays']
        return userdic

    def userInfo(self,contactList,filename):
        userinfo = []
        contact_list = contactList
        faillist=[]
        while len(contactList) != 0 or len(faillist) !=0:
            try:
                if len(contact_list) == 0:
                    contact_list = faillist
                for i in contact_list:
                    # print(i)
                    baseuser = basereq.reqUserinfo(i)
                    baseuser2 = basereq.reqLaninfo(i)
                    baseuser.update(baseuser2)
                    userinfo.append(baseuser)
                    if i in faillist:
                        faillist.remove(i)
                    if i in contact_list:
                        contact_list.remove(i)
            except ConnectionResetError as e:
                faillist.append(i)
                print(e)
            except socket.timeout as e:
                faillist.append(i)
                print(e)
            except Exception as e:
                faillist.append(i)
                print(e)
        # print(offset, userinfo)
        with open(filename, 'a',newline='') as f:
            head = ['姓名', '手机号', '贷款编号','应还款日期','还款时间','逾期天数','期限'
                    ]
            writer = csv.DictWriter(f, head)
            for item in userinfo:
                writer.writerow(item)
            f.close()

if __name__ == '__main__':
    now = datetime.datetime.now()
    format = "%Y-%m-%d-%H-%M-%S"

    basereq = Connect()
    # userdataf = {
    #     "mobile": "018",
    #     "password": "123456"
    # }
    userdataf = {}
    if len(sys.argv) >= 2:
        userdataf['mobile'] = sys.argv[1]
        userdataf['password'] = sys.argv[2]
    else:
        userdataf['mobile'] = input('输入用户名： ')
        userdataf['password'] = input('输入密码： ')
    basereq.loginaction(userdataf)
    filename=userdataf['mobile']+ '-' + now.strftime(format) + '.csv'
    with open(filename, 'w') as f:
        head = ['姓名', '手机号', '贷款编号', '应还款日期', '还款时间', '逾期天数', '期限'
                ]
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    # basereq.headers['Cookie'] = sys.argv[1]
    args=['PROCESSED','PROCESS_FAILED']
    for i in args:
        baseinfo = basereq.reqbase(0, 10,i)
        offset = baseinfo['offset'] + 10
        totalCount = baseinfo['totalCount']
        contact_list = baseinfo['list']
        basereq.userInfo(contact_list,filename)
        while offset <= totalCount:
            baseinfo = basereq.reqbase(offset, 10,i)
            contact_list = baseinfo['list']
            basereq.userInfo(contact_list,filename)
            offset = offset + 100
