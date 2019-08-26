#!/bin/bash/env python
# -*- coding:UTF-8 -*-
import urllib, json, time, socket
import urllib.request
import csv

socket.setdefaulttimeout(20)
class Connect(object):
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "JSESSIONID=tuir4nF9bVEa3n8I8QYiD1WcxnxbS5oXzv5RnmiQ; ADMINID=100001",
            "Host": "adminweb.kantongcerdik100.com",
            "Pragma": "no-cache",
            "Referer": "https://adminweb.kantongcerdik100.com/",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "X-ADMIN- TOKEN": "eyJsb2NhbGUiOiJpbl9JRCIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiIwODU3MTUzMjIwNzAiLCJleHAiOjE1NjU4MzA4MTR9.qGsdyOswqsKHqNIMkzh66kqPDVXJQjNdY9PN9UjjjRMqWsHE4MxLUXdTLPyUzwDuIc3Jk94gFjKdZ7bnsV2yFw"
        }

        self.baseurl='https://adminweb.kantongcerdik100.com/api/api/collection/current-loan?'
        self.userUrl='https://adminweb.kantongcerdik100.com/api/api/review/personalInfo?'
        self.loadUrl='https://adminweb.kantongcerdik100.com/api/api/collection/collection-loan-detail?'


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
        response = urllib.request.urlopen(request)
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
        response = urllib.request.urlopen(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        userdic['姓名'] = content['fullName']
        userdic['手机号'] = content['mobile']
        userdic['用户编号'] = content['customerId']
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
        response = urllib.request.urlopen(request)
        contentb = str(response.read(), encoding='utf-8')
        content = json.loads(contentb, strict=False)
        response.close()
        userdic['放款时间'] = content['issueDate']
        userdic['还款时间'] = content['dueDate']
        userdic['逾期天数'] = content['overdueDays']
        return userdic

    def userInfo(self,contactList):
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
        with open('userinfo.csv', 'a',newline='') as f:
            head = ['姓名', '手机号', '用户编号', '用户等级', '贷款编号','放款时间','还款时间','逾期天数'
                    ]
            writer = csv.DictWriter(f, head)
            for item in userinfo:
                writer.writerow(item)
            f.close()

if __name__ == '__main__':
    with open('userinfo.csv', 'w') as f:
        head = ['姓名', '手机号', '用户编号', '用户等级', '贷款编号', '放款时间', '还款时间', '逾期天数'
                ]
        writer = csv.DictWriter(f, head)
        writer.writeheader()
    basereq = Connect()
    baseinfo = basereq.reqbase(0, 200)
    offset = baseinfo['offset'] + 200
    totalCount = baseinfo['totalCount']
    contact_list = baseinfo['list']
    basereq.userInfo(contact_list)
    while offset <= totalCount:
        baseinfo = basereq.reqbase(offset, 200)
        contact_list = baseinfo['list']
        basereq.userInfo(contact_list)
        offset = offset + 200
