# from bs4 import BeautifulSoup
# import os,sys
#
#
#
# print(os.getcwd())
# filepath=os.path.join('F:\\小车','a.html')
# with open(filepath,'r',encoding='utf-8') as f:
#     content = f.read()
#     f.close()
#
# format = BeautifulSoup(content,"html.parser")
#
# print(format.name)
# for i in format.attrs:
#     print(i)

from selenium import webdriver

# browser = webdriver.Chrome()
# browser.get('http://www.baidu.com/')
option = webdriver.ChromeOptions()
option.add_argument('user-data-dir=C:\\Users\\han20\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #设置成用户自己的数据目录
option.add_argument('disable-infobars')

driver = webdriver.Chrome(chrome_options=option)

#
# driver.maximize_window()
driver.get("https://mail.qq.com/cgi-bin/frame_html?sid=VtX1N0ixB9xdkA5T&r=40dca94c6fe1436a3d5aaa4bf3e0aef8")
print(driver.page_source)