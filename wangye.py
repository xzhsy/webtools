from bs4 import BeautifulSoup
import os,sys
import re
import csv

p = r'<tr data-key="\d{6}"'
page = r'<li class="last"><a .*?data-page="\d.*?"'
# pa = re.compile(p)

# print(os.getcwd())
filepath=os.path.join('F:\\小车','a.html')
with open(filepath,'r',encoding='utf-8') as f:
    content = f.read()
    f.close()

format = BeautifulSoup(content,"html.parser")
# print(format.table.tbody.tr.td.find_all('button')[1]['href'])
a = re.finditer(p,content)
b = re.finditer(page,content)
# for i in a:
#     print(i.group().split('=')[-1].strip('"'))
#
# for ii in b:
#     # print(ii.group())
#     pa = ii.group().split('=')[-1].strip('"')
#     print(pa)

baseurl = 'https://uangrupiah-op.iposecure.com/customer/index?CustomerSearch%5Bphone_no%5D=&CustomerSearch%5Bname%5D=&CustomerSearch%5Bcard_number%5D=&CustomerSearch%5Bcustomer_va%5D=&CustomerSearch%5Bstatus%5D=-1&CustomerSearch%5Bis_black%5D=&CustomerSearch%5Bis_stop_loan%5D=&_pjax=%23pjax-customer&page='
curl=baseurl + '0'
print(curl)
# # print(format.table.tr)
headl=['用户编号','操作','序号','当前使用APP Name','客户手机号','客户名','身份证号码','认证总状态','审核员','是否黑名单','是否暂停贷款','注册日期','认证通过日期','贷款次数','催款次数']
with open('cs.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headl)
    for i in format.table.tbody.find_all('tr'):
        print(i)
        print(i.attrs['data-key'])
        uid=i.attrs['data-key']
        csl = []
        csl.append(uid)
        for cell in i.findAll(['td','th']):
            csl.append(cell.get_text())
        writer.writerow(csl)

    f.close()
# print(format.table.tbody.tr.find_all('data-key'))
