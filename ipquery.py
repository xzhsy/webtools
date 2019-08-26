#!/usr/bin/python
# -*- coding:UTF-8 -*-
from  urllib import request
import sys
import json

class queryIP(object):
    def __init__(self,iptext):
        self.__iptext = iptext
        self.url0 = 'http://ip-api.com/json/'
        self.url1 = 'http://whois.pconline.com.cn/ipJson.jsp?ip=%s&json=true'
        self.url2 = 'http://ip.taobao.com/service/getIpInfo.php?ip='
        self.header = {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2a1pre) Gecko/20090428 Firefox/3.6a1pre"}

    def queryIP(self):
        a=1
        with open(self.__iptext,'r') as f:
            for ii in f.readlines():
                i = ii.strip('\n')
                try:
                    url = self.url0 + i +"?lang=zh-CN"
                    req = request.Request(url,method='GET',headers=self.header)
                    resp = request.urlopen(req).read()
                    city = json.loads(resp)['city']
                    country = json.loads(resp)['country']
                    print("count：%s，ip：%s，city：%s，country: %s" % (a,i,city,country))
                except Exception as e:
                    print(url)
                    print(e)

                if city == None:
                    try:
                        url = self.url1 % i.strip('\n')
                        # print(url)
                        req = request.Request(url,method='GET',headers=self.header)
                        resp = request.urlopen(req).read().decode('GBK')
                        resp=json.loads(resp)
                        city = resp['city']
                        country = resp['country']
                        print("count：%s，ip：%s，city：%s，country: %s" % (a, i, city, country))
                    except Exception as e:
                        print(url)
                        print(e)

                if city == None:
                    try:
                        url = self.url2 + i
                        print(url)
                        req = request.Request(url,method='GET',headers=self.header)
                        resp = request.urlopen(req).read()
                        city = json.loads(resp)['data']['city']
                        country = json.loads(resp)['data']['country']
                        print("count：%s，ip：%s，city：%s，country: %s" % (a, i, city, country))
                        # print(resp)
                    except Exception as e:
                        print(url)
                        print(e)
                a=a+1


if __name__ == "__main__":
    a= queryIP('ip.txt')
    a.queryIP()