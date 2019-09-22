import urllib.request
import urllib
from bs4 import BeautifulSoup
import re
import csv
import datetime
import threading
from multiprocessing import Process
import request


pid = r'<tr data-key="\d{6}"'
page = r'<li class="last"><a .*?data-page="\d.*?"'


class Pqcontent(object):
    def __init__(self):
        self.header = {
            "content-encoding": "gzip",
            "content-type": "text/html; charset=UTF-8",
            "date": "Tue, 10 Sep 2019 14:57:48 GMT",
            "expires": "Thu, 19 Nov 1981 08:52:00 GMT",
            "server": "Tengine",
            "set-cookie": "_identity=d9aff5936640a05b0410cfb55b02712f9b096950bd14ccfe8bb6b7e826cb6365a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A17%3A%22%5B189%2Cnull%2C604800%5D%22%3B%7D; expires=Tue, 17-Sep-2019 14:57:48 GMT; Max-Age=604800; path=/; HttpOnly",
            "status": "200",
            "vary": "Accept-Encoding",
            "x-powered-by": "PHP/7.1.20",
            ":authority": "uangrupiah-op.iposecure.com",
            ":method": "GET",
            ":path": "/detail/addr?id=422361",
            ":scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "cookie": "_csrf=fa95ed6664252811865ad3848fffd9be82e7ff5af67fcaa39ef8b9ee9dc82a68a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22%85%AD%22%7B%82%B5%1D%16M%7B%03%16%C4%3F%0C%B0+%A2%81y%9C%F0Ddy%CD%F8%A7C%AA%F8%B1%22%3B%7D; PHPSESSID=2nhpplni7jtnr5vb3ppenulp1s; _identity=d9aff5936640a05b0410cfb55b02712f9b096950bd14ccfe8bb6b7e826cb6365a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A17%3A%22%5B189%2Cnull%2C604800%5D%22%3B%7D",
            "pragma": "no-cache",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-reqss": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }

        self.baseurl = 'https://uangrupiah-op.iposecure.com/customer/index?CustomerSearch%5Bphone_no%5D=&CustomerSearch%5Bname%5D=&CustomerSearch%5Bcard_number%5D=&CustomerSearch%5Bcustomer_va%5D=&CustomerSearch%5Bstatus%5D=-1&CustomerSearch%5Bis_black%5D=&CustomerSearch%5Bis_stop_loan%5D=&_pjax=%23pjax-customer&page='
        self.userurl = 'https://uangrupiah-op.iposecure.com/detail/addr?id=422361'

        self.csvbase=['用户编号','操作','序号','当前使用APP Name','客户手机号','客户名','身份证号码','认证总状态','审核员','是否黑名单','是否暂停贷款','注册日期','认证通过日期','贷款次数','催款次数']
        self.csvinfo=['序号','客户手机号','客户名','手机号','联系人姓名','是否紧急联系人','关系']



    def reqbase(self,pg,file):
        basedic = {}
        url = self.baseurl + str(pg)
        reqs = request.GET(url,headers=self.header,verify = False) ## 替换为ssl证书位置
        content = reqs.text
        format = BeautifulSoup(content, "html.parser")
        pages = re.finditer(page, content)
        for ii in pages:
            # print(ii.group())
            pa = ii.group().split('=')[-1].strip('"')
            print(pa)
            basedic['pages'] = pa

        uids = re.finditer(pid, content)
        uidlist = []
        for i in uids:
            # print(i.group().split('=')[-1].strip('"'))
            uid = i.group().split('=')[-1].strip('"')
            uidlist.append(uid)

        basedic['list'] = uidlist
        with open(file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for i in format.table.tbody.find_all('tr'):
                print(i)
                uid = i.attrs['data-key']
                csl = []
                csl.append(uid)
                for cell in i.findAll(['td', 'th']):
                    csl.append(cell.get_text())
                writer.writerow(csl)

            f.close()

        return basedic


    def baseaction(self):
        now = datetime.datetime.now()
        format = "%Y-%m-%d-%H-%M-%S"
        file = now.strftime(format)
        filename = 'base' + file
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer=csv.writer(f)
            writer.writerow(self.csvbase)
        infodic = basereq.reqbase(0, filename)
        pages = infodic['pages']
        page=0
        threadlist = []
        while page <= pages:
            basereq.reqbase(page,filename)
            t = threading.Thread(target=basereq.reqbase,args=(page,filename,))
            threadlist.append(t)
            page = page + 1

        for the in threadlist:
            the.setDaemon(True)
            the.start()
            if n > 3:
                the.join()
                n = 0
            n = n + 1
        the.join()


if __name__== '__main__':
    # now = datetime.datetime.now()
    # format = "%Y-%m-%d-%H-%M-%S"
    # file=now.strftime(format)

    basereq = Pqcontent()
    basereq.baseaction()
