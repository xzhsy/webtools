#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket, datetime
import urllib.request
import csv
import sys
from http import cookiejar
socket.setdefaulttimeout(20)


class Connect(object):
    def __init__(self, cookie):
        self.headers = {
            "authority": "lmt-man.id-aifintech.cc",
            "method": "POST",
            "path": "/cs/collection/getOperatedFinishList",
            "scheme": "https",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://lmt-man.id-aifintech.cc",
            "pragma": "no-cache",
            "referer": "https://lmt-man.id-aifintech.cc/cs/common/frame/index?jspname=pages/csm/collection/operateFinish",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": " same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        self.cookie = cookie
        # 自定义请求方法，获取cookie
        cookie_object = cookiejar.CookieJar()
        hanler = urllib.request.HTTPCookieProcessor(cookie_object)
        self.opener = urllib.request.build_opener(hanler)

        # 定义请求连接，还款查询
        self.baseurl = 'https://lmt-man.id-aifintech.cc/cs/collection/getOperatedFinishList'
        # 登陆连接
        self.before = 'https://lmt-man.id-aifintech.cc/cs/login'
        self.login = 'https://lmt-man.id-aifintech.cc/cs/j_spring_security_check'

    def loginaction(self, userdataf):
        try:
            userdata = urllib.parse.urlencode(userdataf).encode(encoding='UTF8')
            login = urllib.request.Request(self.login, method='POST', data=userdata, headers=self.headers)
            response = self.opener.open(login)
            response.close()

        except Exception as e:
            print("登陆失败：", e)
            exit(1)

    def reqbase(self, page, limit):
        limit=limit
        dataformat = {
            "chname": '',
            "mobile": '',
            "collector": '',
            "overdueLevel": '',
            "dayInte": '',
            "overduyDays": '',
            "expectedRepayDate": "2019-11-15,2019-12-03",
            "realRepayDate": '',
            "page": page,
            "rows": limit,
        }
        self.headers['Cookie'] = "lang=zh; JSESSIONID=" + self.cookie + "; INST_ORG=bj_qianbang"
        data = urllib.parse.urlencode(dataformat).encode(encoding='UTF8')
        baseurl = self.baseurl
        request = urllib.request.Request(url=baseurl, method='POST',data=data,headers=self.headers)
        userinfo = []
        infodic = {}
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
            midinfo["客户姓名"] = i["chname"]
            midinfo["手机号码"] = i["mobile"]
            midinfo["到账金额"] = i["arriveAmount"]
            midinfo["逾期总金额"] = i["dayinte"]
            midinfo["逾期天数"] = i["overdueDays"]
            midinfo["逾期费用"] = i["realAmount"]
            midinfo["逾期等级"] = i["overdueLevel"]
            midinfo["放款日期"] = i["contractdate"]
            midinfo["应还日期"] = i["startpaydate"]
            midinfo["实际还款时间"] = i["outDate"]
            midinfo["身份证号码"] = i["idnumber"]
            userinfo.append(midinfo)
        with open(filename, 'a',newline='') as f:
            # 贷款编号、任务状态、应还款日、还款时间、用户姓名、手机、申请状态、逾期天数
            head = ['客户姓名', '手机号码', '到账金额', '逾期总金额', '逾期天数', '逾期费用', '逾期等级', '放款日期','应还日期', '实际还款时间', '身份证号码'
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
    # basereq.loginaction(userdataf)
    filename=userdataf['j_username']+ '-re-' + now.strftime(format) + '.csv'
    with open(filename, 'w') as f:
        head = ['客户姓名', '手机号码', '到账金额', '逾期总金额', '逾期天数', '逾期费用', '逾期等级', '放款日期', '应还日期', '实际还款时间', '身份证号码'
                ]
        ##客户名称、入催时间、出崔时间、身份证号、手机号码、应还日期、最大逾期天数、业务状态
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    # basereq.headers['Cookie'] = sys.argv[1]
    baseinfo = basereq.reqbase(1, 50)
    totalCount = baseinfo['totalCount']
    page = 2
    limit = 50
    pages=round(totalCount/limit)
    print(pages)
    while page <= pages:
        baseinfo = basereq.reqbase(page, limit)
        page = page + 1
