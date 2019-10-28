# encoding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import math
# 启动chrome浏览器
driver = webdriver.Firefox()
# 进入qq邮箱登陆首页
driver.get("https://pubs.kreditq.id/KreditQ/index.html#/login")
time.sleep(1)

# 窗口最大化
driver.maximize_window()
# 切换到登陆frame（!!!!!!!!必须先切换!!!!!!!!）
# driver.switch_to.frame('login_frame')
# driver.find_element_by_xpath("//*[@id='switcher_plogin']").click()
# time.sleep(3)
#########登陆
# 输入用户名
# username = driver.find_element_by_xpath("//*[@id='u']")
username = driver.find_element_by_xpath('//*[@type="text"]')
username.clear()
# 将xxxxxxxxxx换成qq邮箱账户type="password
username.send_keys('doni')
# 输入密码：将1111111111替换为自己的邮箱密码
driver.find_element_by_xpath('//*[@type="password"]').send_keys('1234567')
# 点击登陆
driver.find_element_by_xpath('//*[@type="button"]').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@class="ivu-icon ivu-icon-md-arrow-dropdown"]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@class="custom-content-con"]/div[2]/div/div/a').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@class="custom-content-con"]/div[2]/div/div[2]/ul/li[1]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@class="ivu-menu-submenu"]/div/span').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@class="ivu-menu-submenu ivu-menu-opened"]/ul/li[1]').click()
time.sleep(1)
total=driver.find_element_by_xpath('//*[@class="ivu-page-total"]')
print(total.text)
c=int(total.text.split(' ')[1])
count=math.floor(c/100)
driver.find_element_by_xpath('//*[@class="ivu-select ivu-select-single ivu-select-small"]/div/div/span').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@class="ivu-select ivu-select-visible ivu-select-single ivu-select-small"]/div[2]/ul[2]/li[6]').click()
ctext=driver.page_source
content=BeautifulSoup(ctext,"html.parser")

with open('a.txt','a') as f:
    f.write(ctext)
f.close()

i=1
while i <= count:
    driver.find_element_by_xpath('//*[@class="ivu-page-next"]' ).click()
    res=driver.page_source
    restxt= BeautifulSoup(res,"html.parser")
    with open('a.txt','a') as f:
        f.write(res)
    f.close()
    time.sleep(3)
    i = i + 1
# driver.quit()
