import urllib.request
import os
import re

def urlopen(url):
    req = urllib.request.Request(url)
    req.add_header('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')
    # headers = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     "accept-encoding": "gzip, deflate, br",
    #     "accept-language": "zh-CN,zh;q=0.9",
    #     "cache-control": "no-cache",
    #     "cookie": "__cfduid=d44a053e7973141f95f25c54fe8027a571591091286; UM_distinctid=172746e799d38c-0f2b99ac05601f-f7d1d38-144000-172746e799e82f; CNZZDATA2420152=cnzz_eid%3D1910612595-1591090601-%26ntime%3D1591090601; _ga=GA1.2.1522683829.1591091299; _gid=GA1.2.590864139.1591091299; _gat_gtag_UA_137975950_2=1",
    #     "pragma": "no-cache",
    #     "referer": "https://yiren91.com/",
    #     "upgrade-insecure-requests": 1,
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    # }

    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def get_page(url):
    html = urlopen(url).decode('utf-8')
    P = r'<li><a href="(/se/zhenshizipai/[+\d]+\.html)'
    pagesList = re.findall(P,html)
    # print(pagesList)
    # for each in pagesList:
    #     print(each)
    return pagesList

def find_imgs(url):
    # print(url)
    html = urlopen(url).decode('utf-8')
    p = r'<img id="aimg_[\d]+" src="([\d]+\.jpg)'
    img_addrs = re.findall(p,html)
    for i in img_addrs:
        print(i)
        img = urlopen(i)

        print(img)

def save_imgs(folder,img_addrs):
    pass


def download_mm(folder='ooxx',pages=10):
    if not os.path.exists('ooxx'):
        os.mkdir(folder)
    os.chdir(folder)

    url = 'https://yiren91.com/se/zhenshizipai/'
    # a = urlopen(url).decode("utf8","ignore")
    # print(a)
    pages = get_page(url)
    print(pages)
    for i in pages:
        pageurl = 'https://yiren91.com' + i
        find_imgs(pageurl)

if __name__ == '__main__':
    download_mm()