import urllib.request
import urllib
from http import cookiejar
import sys,json,ssl
import os,time,multiprocessing

ssl._create_default_https_context = ssl._create_unverified_context
cookie_object= cookiejar.CookieJar()
hanler = urllib.request.HTTPCookieProcessor(cookie_object)
opener = urllib.request.build_opener(hanler)

captcha='http://149.129.222.131:9999/api/auth/captcha?width=120&height=50&serialId=KY1uqphQ'
login='http://149.129.222.131:9999/api/auth/login'

baseurl='http://149.129.222.131:9999/api/api/collection/my?'
formdata = {
    "mobile": 60004,
    "password": "zxyl123"
}

dataformat = {
    "offset": 0,
    "collectionTaskStatus": "PROCESSED",
    "limit": 20
}
basedata = urllib.parse.urlencode(dataformat).encode(encoding='UTF8')

headers = {
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "149.129.222.131:9999",
    "Pragma": "no-cache",
    "Referer": "http://149.129.222.131:9999/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}

caprep = urllib.request.Request(captcha)
capponse = opener.open(caprep)
print(captcha)
SecretCode = input('输入验证码： ')
print(SecretCode)
formdata['answer']=str(SecretCode)
data = urllib.parse.urlencode(formdata).encode(encoding='UTF8')
print(data)
login = urllib.request.Request(login,method='POST',data=data,headers=headers)

response = opener.open(login)
response.close()

basereq = urllib.request.Request(baseurl,data=basedata,headers=headers,method='GET')

baserespon = opener.open(basereq)
contentb = str(baserespon.read(), encoding='utf-8')
content = json.loads(contentb, strict=False)
response.close()
print(content)
# print("查看 response 的返回类型：",type(response))
# print("查看反应地址信息: ",response)
# print("查看头部信息1(http header)：\n",response.info())
# print("查看头部信息2(http header)：\n",response.getheaders())
# print("输出头部属性信息：",response.getheader("Server"))
# print("查看响应状态信息1(http status)：\n",response.status)
# print("查看响应状态信息2(http status)：\n",response.getcode())
# print("查看响应 url 地址：\n",response.geturl())
# for item in cookie_object:
#     print(item)
#     print("name="+item.name)
#     print("value="+item.value)
