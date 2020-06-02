import urllib.request

url = 'https://www.yiren91.com/se/zhenshizipai/'

proxy_support = urllib.request.ProxyHandler({'http':'95.217.130.87:3128'})
opener = urllib.request.build_opener(proxy_support)
opener.addheaders = [('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')]
urllib.request.install_opener(opener)

response = urllib.request.urlopen(url)

html = response.read().decode('utf-8')
print(html)