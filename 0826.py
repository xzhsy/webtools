#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket,datetime
import urllib.request
import csv
import sys
from http import cookiejar
import  threading

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

        #自定义请求方法，获取cookie
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
        #定义请求连接
        self.baseurl='http://149.129.222.131:9999/api/api/customer/load-customers?'
        self.userUrl='http://149.129.222.131:9999/api/api/customer/load-personal-info?'
        self.basicUrl='http://149.129.222.131:9999/api/api/customer/load-basic-info?'
        self.realpayUrl='http://149.129.222.131:9999/api/api/finance/customer/deposit-history?'
        self.loadUrl='http://149.129.222.131:9999/api/api/finance/customer/issue-history?'
        #验证码连接
        self.catpch='http://149.129.222.131:9999/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        self.login = 'http://149.129.222.131:9999/api/auth/login'
        # self.baseurl='https://adminweb.adminrichboxbox.com/api/api/collection/my?'
        # self.userUrl='https://adminweb.adminrichboxbox.com/api/api/review/personalInfo?'
        # self.loadUrl='https://adminweb.adminrichboxbox.com/api/api/collection/collection-loan-detail?'
        # #验证码连接
        # self.catpch='https://adminweb.adminrichboxbox.com/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
        # self.login = 'https://adminweb.adminrichboxbox.com/api/auth/login'

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
            print("登陆失败：",e)

    def reqbase(self,nexta,limit,status):
        offset=nexta
        limit=limit
        dataformat = {
            "customerGradeId": status,
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
        infodic['totalCount'] = content['paginator']['totalCount']
        infodic['offset'] = content['paginator']['offset']
        for i in content['item']:
            itemlist.append(i['customerId'])
        infodic['list'] = itemlist
        return infodic

    def reqUserinfo(self,contractNo):
        dataformat = {
            "customerId": contractNo
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl=self.userUrl+data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)
        userdic={}
        print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        if contentb:
            content = json.loads(contentb, strict=False)
            response.close()
        # userdic['姓名'] = content['fullName']
        # userdic['手机号'] = content['mobile']
        # userdic['用户编号'] = content['customerId']
            userdic['身份证号'] = content['credentialNo']
        else:
            userdic['身份证号'] = ''
            # userdic['注册时间'] = content['credentialNo']
        # userdic['用户等级'] = content['customerGrade']
        # userdic['贷款编号'] = content['loanAppId']
        return  userdic
    def reqBaseinfo(self,contractNo):
        dataformat = {
            "customerId": contractNo
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl=self.basicUrl+data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)
        userdic={}
        print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        userdic['姓名'] = content['realName']
        userdic['手机号'] = content['mobile']
        userdic['用户编号'] = content['customerId']
        userdic['注册时间'] = content['registerTime']
        # userdic['用户等级'] = content['customerGrade']
        # userdic['贷款编号'] = content['loanAppId']
        return  userdic

    def reqLaninfo(self,contractNo):
        dataformat = {
            "customerId": contractNo
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl=self.loadUrl+data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)
        loanlist = []
        userdic={}
        print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        if contentb:
            content = json.loads(contentb, strict=False)
            response.close()
            for i in content:
                userdic['放款-贷款金额'] = i['issueAmount']
                userdic['放款-贷款编号'] = i['loanAppId']
                userdic['银行卡状态'] = i['verifyStatus']['value']
                loanlist.append(userdic)
        else:
            userdic['放款-贷款金额'] = ''
            userdic['放款-贷款编号'] = ''
            userdic['银行卡状态'] = ''
            loanlist.append(userdic)
        return loanlist

    def repayinfo(self,contractNo):
        dataformat = {
            "customerId": contractNo
        }
        data = urllib.parse.urlencode(dataformat)
        baseurl=self.realpayUrl+data
        request = urllib.request.Request(url=baseurl, method='GET',
                                         headers=self.headers)
        repaylist = []
        userdic={}
        print(request.full_url)
        response = self.opener.open(request)
        contentb = str(response.read(), encoding='utf-8')
        if contentb:
            content = json.loads(contentb, strict=False)
            response.close()
            for i in content:
                userdic['还款-贷款金额'] = i['depositAmount']
                userdic['还款-贷款编号'] = i['loanAppId']
                userdic['还款金额'] = i['depositAmount']
                repaylist.append(userdic)
        else:
            userdic['还款-贷款金额'] = ''
            userdic['还款-贷款编号'] = ''
            userdic['还款金额'] = ''
            repaylist.append(userdic)
        return repaylist

    def userInfo(self,contactList,filename,filename2,stats):
        userinfo = []
        relpay = []
        loanlist = []
        contact_list = contactList
        faillist=[]
        while len(contactList) != 0 or len(faillist) !=0:
            try:
                if len(contact_list) == 0:
                    contact_list = faillist
                for i in contact_list:
                    # print(i)
                    baseuser = basereq.reqUserinfo(i)
                    baseuser2 = basereq.reqBaseinfo(i)
                    baseuser.update(baseuser2)
                    paydic = {}
                    paydic['用户等级'] = stats
                    paydic.update(baseuser)
                    loandic= {}
                    loandic['用户等级'] = stats
                    loandic.update(baseuser)
                    relpayinfo = basereq.repayinfo(i)
                    loaninfo = basereq.reqLaninfo(i)
                    for pay in relpayinfo:
                        paydic.update(pay)
                        relpay.append(paydic)
                    for loan in loaninfo:
                        loandic.update(loan)
                        loanlist.append(loandic)
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
            head = ['用户等级','姓名', '手机号', '用户编号', '注册时间','身份证号', '放款-贷款编号','放款-贷款金额','银行卡状态']
            writer = csv.DictWriter(f, head)
            for item in loanlist:
                writer.writerow(item)
            f.close()
        with open(filename2, 'a',newline='') as f:
            head = ['用户等级','姓名', '手机号', '用户编号', '注册时间','身份证号', '还款-贷款编号','还款-贷款金额','还款金额']
            writer = csv.DictWriter(f, head)
            for item in relpay:
                writer.writerow(item)
            f.close()


    def action(self,stats,limit):
        now = datetime.datetime.now()
        format = "%Y-%m-%d-%H-%M-%S"
        filename = 'loan' + now.strftime(format) + '.csv'
        with open(filename, 'w') as f:
            head = ['用户等级','姓名', '手机号', '用户编号', '注册时间', '身份证号', '放款-贷款编号', '放款-贷款金额', '银行卡状态']
            writer = csv.DictWriter(f, head)
            writer.writeheader()
        filename2 = 'repay' + now.strftime(format) + '.csv'
        with open(filename2, 'w') as f:
            head = ['用户等级','姓名', '手机号', '用户编号', '注册时间', '身份证号', '还款-贷款编号', '还款-贷款金额', '还款金额']
            writer = csv.DictWriter(f, head)
            writer.writeheader()
        # basereq.headers['Cookie'] = sys.argv[1]
        baseinfo = basereq.reqbase(0, 10, stats)
        print(baseinfo)
        offset = baseinfo['offset'] + limit
        totalCount = baseinfo['totalCount']
        totalCount = 30
        contact_list = baseinfo['list']
        basereq.userInfo(contact_list, filename, filename2,stats)
        while offset <= totalCount:
            baseinfo = basereq.reqbase(offset, limit, stats)
            contact_list = baseinfo['list']
            basereq.userInfo(contact_list, filename, filename2,stats)
            offset = offset + limit


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
    threadlist = []
    # basereq.action(1,10)
    for i in [2,3,4,5,1]:
        t = threading.Thread(target=basereq.action, args=(i,10, ))
        threadlist.append(t)
    for i in threadlist:
        i.setDaemon(True)
        i.start()
    i.join()
