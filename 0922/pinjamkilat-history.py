#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket,datetime
import urllib.request
import csv
import sys
from http import cookiejar
import threading


socket.setdefaulttimeout(20)

class Connect(object):
    def __init__(self):
        self.headers = {
            "Host": "adminweb.pinjamkilat.co.id",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://adminweb.pinjamkilat.co.id/collection/my",
            "origin": "https://adminweb.pinjamkilat.co.id",
            "Connection": "keep-alive"
        }
        #自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        #定义请求 历史案件：https://adminweb.pinjamkilat.co.id/api/api/review/loanAppAssignedHistory?offset=0&limit=10
        self.baseurl='https://adminweb.pinjamkilat.co.id/api/api/review/loanAppAssignedHistory?'
        self.loadUrl='https://adminweb.pinjamkilat.co.id/api/api/review/applyHistory?'
        #验证码连接
        self.catpch='https://adminweb.pinjamkilat.co.id/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        self.login = 'https://adminweb.pinjamkilat.co.id/api/auth/login'

    def loginaction(self,userdataf):
        caprep = urllib.request.Request(self.catpch)
        capponse = self.opener.open(caprep)
        print(self.catpch)
        SecretCode = input('输入验证码： ')
        capponse.close()
        userdataf['answer'] = SecretCode
        try:
            userdata = urllib.parse.urlencode(userdataf).encode(encoding='UTF8')
            login = urllib.request.Request(self.login, method='POST', data=userdata, headers=self.headers)
            response = self.opener.open(login)
            response.close()
        except Exception as e:
            print('登陆失败，原因：',e)
            exit(1)

    def reqbase(self,nexta,limit):
        offset=nexta
        limit=limit
        dataformat = {
            "offset": offset,
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
        userinfo = []
        infodic['totalCount'] = content['paginator']['totalCount']
        infodic['offset'] = content['paginator']['offset']
        for i in  content['item']:
            midinfo = {}
            midinfo['贷款编号'] = i['loanAppId']
            midinfo['用户姓名'] = i['realName']
            midinfo['手机号1'] = i['mobile']
            midinfo['申请时间'] = i['contractTime']
            midinfo['申请状态'] = i['loanAppStatus']['value']
            midinfo['contractNo'] = i['contractNo']
            userinfo.append(midinfo)

        infodic['list']=userinfo
        return infodic


    def reqUserinfo(self,para):
        contractNo = para['contractNo']
        dataformat = {
            "contractNo": contractNo
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl=self.loadUrl+data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)

        # print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        userlist=[]
        for i in content:
            userdic = {}
            userdic['子手机号'] = i['mobile']
            userdic['子贷款编号'] = i['id']
            userdic['子申请时间'] = i['applyTime']
            userdic['证件号码'] = i['credentialNo']
            userdic['贷款类型'] = i['loanType']['value']
            userdic['期限'] = i['period']
            userdic['状态'] = i['period']
            userdic['子贷款状态'] = i['subStatus']
            userdic['逾期天数'] = i['overdueDays']
            userdic.update(para)
            userlist.append(userdic)
        return  userlist


    def useraction(self,contactList,filename):
        contact_list = contactList
        for i in contact_list:
            baseuser = basereq.reqUserinfo(i)
            with open(filename, 'a', newline='') as f:
                head = ['贷款编号', '用户姓名', '手机号1', '申请时间', '申请状态', '子手机号', '子贷款编号', '子申请时间', '证件号码', '贷款类型', '期限',
                        '状态', '子贷款状态', '逾期天数',
                        'contractNo']
                writer = csv.DictWriter(f, head)
                for item in baseuser:
                    writer.writerow(item)
                f.close()


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
    filename=userdataf['mobile']+ '-' + now.strftime(format) + '.csv'
    with open(filename, 'w') as f:
        head = ['贷款编号', '用户姓名', '手机号1', '申请时间', '申请状态', '子手机号', '子贷款编号', '子申请时间', '证件号码', '贷款类型', '期限', '状态', '子贷款状态',
                '逾期天数','contractNo'
                ]
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    # basereq.headers['Cookie'] = sys.argv[1]
    baseinfo = basereq.reqbase(0, 10)
    offset = 0
    totalCount = baseinfo['totalCount']
    contact_list = baseinfo['list']
    basereq.useraction(contact_list,filename)

    threadlist = []
    while offset <= totalCount:
        # basereq.userInfo(contact_list, filename)
        baseinfo = basereq.reqbase(offset, 100)
        contact_list = baseinfo['list']
        # basereq.useraction(contact_list, filename)
        t = threading.Thread(target=basereq.useraction, args=(contact_list, filename,))
        offset = offset + 100
        threadlist.append(t)

    n = 0
    for m in threadlist:
        m.setDaemon(True)
        m.start()
        if n > 10:
            m.join()
            n = 0
            time.sleep(3)
        n = n + 1
    m.join()