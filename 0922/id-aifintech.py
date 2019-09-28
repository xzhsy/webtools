#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket,datetime
import urllib.request
import csv
import sys
from http import cookiejar
socket.setdefaulttimeout(20)

class Connect(object):
    def __init__(self,cookie):
        self.headers = {
            "authority": " lmt-man.id-aifintech.cc",
            "method": " POST",
            "path": " /cs/collection/getTotalList?flag=member",
            "scheme": " https",
            "accept": " application/json, text/javascript, */*; q=0.01",
            "accept-encoding": " gzip, deflate, br",
            "accept-language": " zh-CN,zh;q=0.9",
            "cache-control": " no-cache",
            "content-length": " 14",
            "content-type": " application/x-www-form-urlencoded; charset=UTF-8",
            "origin": " https://lmt-man.id-aifintech.cc",
            "pragma": " no-cache",
            "referer": " https://lmt-man.id-aifintech.cc/cs/common/frame/index?jspname=pages/csm/addressList/collectionCollector_query",
            "sec-fetch-mode": " cors",
            "sec-fetch-site": " same-origin",
            "user-agent": " Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "x-requested-with": " XMLHttpRequest"
        }
        self.cookie=cookie
        #自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        #定义请求连接
        self.baseurl='https://lmt-man.id-aifintech.cc/cs/collection/getTotalList?flag=member'
        #登陆连接
        self.before='https://lmt-man.id-aifintech.cc/cs/login'
        self.login = 'https://lmt-man.id-aifintech.cc/cs/j_spring_security_check'

    def loginaction(self,userdataf):
        try:
            before = urllib.request.Request(self.before)
            beforeponse = self.opener.open(before)
            userdata = urllib.parse.urlencode(userdataf).encode(encoding='UTF8')
            login = urllib.request.Request(self.login, method='POST', data=userdata, headers=self.headers)
            response = self.opener.open(login)
            response.close()

        except Exception as e:
            print("登陆失败：", e)
            exit(1)

    def reqbase(self,page,limit):
        limit=limit
        dataformat = {
            "page": page,
            "rows": limit
        }
        self.headers['Cookie'] = "lang=zh; JSESSIONID=" + self.cookie + "; INST_ORG=bj_qianbang"
        data = urllib.parse.urlencode(dataformat).encode(encoding='UTF8')
        baseurl=self.baseurl
        request = urllib.request.Request(url=baseurl, method='POST',data=data,
                                         headers=self.headers)
        userinfo=[]
        infodic={}
        print(request.full_url)
        # response = self.opener.open(request)
        response = urllib.request.urlopen(request)
        print(data)
        contentb = str(response.read(), encoding='utf-8').strip("'")
        # print(contentb)
        content = json.loads(contentb, strict=False)
        response.close()
        infodic['totalCount'] = content['total']
        for i in  content['rows']:
            midinfo = {}
            midinfo['入催时间'] = i['createTime']
            midinfo['客户名称'] = i['chname']
            midinfo['手机号码'] = i['mobile']
            if 'outDate' in i:
                midinfo['出崔时间'] = i['outDate']
            else:
                midinfo['出崔时间'] =''
            midinfo['应还日期'] = i['dueDate']
            midinfo['最大逾期天数'] = i['hisMaxOverdueDays']
            midinfo['业务状态'] = i['states']
            midinfo['身份证号'] = i['idNumber']
            userinfo.append(midinfo)
        with open(filename, 'a',newline='') as f:
            #贷款编号、任务状态、应还款日、还款时间、用户姓名、手机、申请状态、逾期天数
            head = ['客户名称', '手机号码', '入催时间', '出崔时间', '应还日期', '最大逾期天数', '身份证号', '业务状态'
                    ]
            writer = csv.DictWriter(f, head)
            for item in userinfo:
                writer.writerow(item)
            f.close()
        return infodic

if __name__ == '__main__':
    now = datetime.datetime.now()
    format = "%Y-%m-%d-%H-%M-%S"
    cookie=sys.argv[3]
    basereq = Connect(cookie)
    userdataf = {}
    if len(sys.argv) >= 2:
        userdataf['j_username'] = sys.argv[1]
        userdataf['j_password'] = sys.argv[2]
    else:
        userdataf['j_username'] = input('输入用户名： ')
        userdataf['j_password'] = input('输入密码： ')
    basereq.loginaction(userdataf)
    filename=userdataf['j_username']+ '-' + now.strftime(format) + '.csv'
    with open(filename, 'w') as f:
        head = ['客户名称', '手机号码', '入催时间', '出崔时间', '应还日期', '最大逾期天数', '身份证号', '业务状态'
                ]
        ##客户名称、入催时间、出崔时间、身份证号、手机号码、应还日期、最大逾期天数、业务状态
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    # basereq.headers['Cookie'] = sys.argv[1]
    baseinfo = basereq.reqbase(1, 50)
    totalCount = baseinfo['totalCount']
    page=2
    limit=50
    pages=round(totalCount/limit)
    while page <= pages:
        baseinfo = basereq.reqbase(page, limit)
        page = page + 1
