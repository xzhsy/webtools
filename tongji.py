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
        # self.headers = {
        #     "Accept": "*/*",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "zh-CN,zh;q=0.9",
        #     "Cache-Control": "no-cache",
        #     "Connection": "keep-alive",
        #     "Host": "149.129.222.131:9999",
        #     "Pragma": "no-cache",
        #     "Referer": "http://149.129.222.131:9999/",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        #     "X-ADMIN- TOKEN": "eyJsb2NhbGUiOiJ6aF9DTiIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiI2MDAwNCIsImV4cCI6MTU2NjM3MDI2NH0.Lk5fXi639BaDMXF_b36dgxMGQnLOAnQhQSawx7V11M4Bzn5RitfeS2AJTkcT1e6_Y8m4bYdDpWJx8CgTh0t-xA"
        # }
        #自定义请求方法，获取cookie
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
            "X-ADMIN-TOKEN": " eyJsb2NhbGUiOiJpbl9JRCIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiIwMTQiLCJleHAiOjE1NjY0NDkyMzR9.i_OePk7yGoOsc_q_oYrgMeUc2yp-3Ir46E0JV20sbjk3ZATe0AvWUOKxlkQTo03bJ66PqACcQ9M_7aseeHS4Hg",
            "Connection": " keep-alive",
            "Pragma": " no-cache",
            "Cache-Control": " no-cache"
        }
        #定义请求连接
        self.baseurl='https://adminweb.adminrichboxbox.com/api/api/collection/my?'
        self.userUrl='https://adminweb.adminrichboxbox.com/api/api/review/personalInfo?'
        self.loadUrl='https://adminweb.adminrichboxbox.com/api/api/collection/collection-loan-detail?'
        #验证码连接
        self.catpch='https://adminweb.adminrichboxbox.com/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        self.login = 'https://adminweb.adminrichboxbox.com/api/auth/login'

    def loginaction(self,userdataf):
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
            print(e)

    def reqbase(self,nexta,limit):
        offset=nexta
        limit=limit
        dataformat = {
            "offset": offset,
            "collectionTaskStatus": "PROCESSED",
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
        userdic['用户编号'] = content['customerId']
        userdic['身份证号'] = content['credentialNo']
        userdic['用户等级'] = content['customerGrade']
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
        userdic['应还金额'] = content['dueAmount']
        userdic['放款时间'] = content['issueDate']
        userdic['还款时间'] = content['dueDate']
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
            head = ['姓名', '手机号', '用户编号', '用户等级','身份证号', '贷款编号','应还金额','放款时间','还款时间','逾期天数'
                    ]
            writer = csv.DictWriter(f, head)
            for item in userinfo:
                writer.writerow(item)
            f.close()

if __name__ == '__main__':
    now = datetime.datetime.now()
    format = "%Y-%m-%d-%H-%M-%S"
    filename='userinfo' + now.strftime(format)
    with open(filename, 'w') as f:
        head = ['姓名', '手机号', '用户编号', '用户等级','身份证号', '贷款编号','应还金额', '放款时间', '还款时间', '逾期天数'
                ]
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    basereq = Connect()
    # userdataf = {
    #     "mobile": "018",
    #     "password": "123456"
    # }
    userdataf = {}
    userdataf['mobile'] = sys.argv[1]
    userdataf['password'] = sys.argv[2]
    basereq.loginaction(userdataf)
    # basereq.headers['Cookie'] = sys.argv[1]
    baseinfo = basereq.reqbase(0, 10)
    offset = baseinfo['offset'] + 10
    totalCount = baseinfo['totalCount']
    contact_list = baseinfo['list']
    basereq.userInfo(contact_list,filename)
    while offset <= totalCount:
        baseinfo = basereq.reqbase(offset, 10)
        contact_list = baseinfo['list']
        basereq.userInfo(contact_list,filename)
        offset = offset + 10
