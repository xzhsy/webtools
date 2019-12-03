# encoding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import math
import csv
import datetime
# 启动chrome浏览器

firfox_options = webdriver.FirefoxOptions()
firfox_options.headless=True
driver = webdriver.Firefox(options=firfox_options)
#driver = webdriver.Firefox()
# 进登陆首页
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
def login():
    username = driver.find_element_by_xpath('//*[@type="text"]')
    username.clear()
    # 将xxxxxxxxxx换成qq邮箱账户type="password
    username.send_keys('doni')
    # 输入密码：将1111111111替换为自己的邮箱密码
    driver.find_element_by_xpath('//*[@type="password"]').send_keys('1234567')
    # 点击登陆
    driver.find_element_by_xpath('//*[@type="button"]').click()
    time.sleep(3)

def filres():
    driver.find_element_by_xpath('//*[@class="ivu-icon ivu-icon-md-arrow-dropdown"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@class="custom-content-con"]/div[2]/div/div/a').click()
    time.sleep(1)
    #选择语言
    driver.find_element_by_xpath('//*[@class="custom-content-con"]/div[2]/div/div[2]/ul/li[1]').click()
    time.sleep(1)
    #还款查询
    driver.find_element_by_xpath('//*[@class="side-menu-wrapper"]/ul/li[2]/span').click()
    time.sleep(1)
    #添加赛选条件
    
    d=driver.find_elements_by_xpath('//*[@placeholder="Select date"]')
    if d:
       driver.find_element_by_xpath('//*[@placeholder="Select date"]').click()
    d1=driver.find_elements_by_xpath('//*[@placeholder="选择日期"]')
    if d1:
       driver.find_element_by_xpath('//*[@placeholder="选择日期"]').click()
    time.sleep(1)
    # 'class="ivu-picker-panel-content ivu-picker-panel-content-left"'
    #span 确定具体日期 20+2 =20号
    #本月头一周，日期需往前反一页
    driver.find_element_by_xpath('//*[@class="ivu-picker-panel-content ivu-picker-panel-content-left"]/div[1]/span[2]').click()
    time.sleep(1)
    # 开始时间'class="ivu-picker-panel-content ivu-picker-panel-content-left"]/dev[2]/span[22]'
    driver.find_element_by_xpath('//*[@class="ivu-picker-panel-content ivu-picker-panel-content-left"]/div[2]/span[20]').click()
    time.sleep(1)
    #结束时间
    driver.find_element_by_xpath('//*[@class="ivu-picker-panel-content ivu-picker-panel-content-right"]/div[2]/span[3]').click()
    time.sleep(1)
    #确认
    driver.find_element_by_xpath('//*[@class="ivu-picker-confirm"]/button[3]/span').click()
    time.sleep(1)
    #查询
    driver.find_element_by_xpath('//*[@class="search-inline search-mar ivu-btn ivu-btn-primary ivu-btn-small"]/span').click()
    time.sleep(1)
#催收查询
# driver.find_element_by_xpath('//*[@class="ivu-menu-submenu"]/div/span').click()
# time.sleep(1)
#pdl
#driver.find_element_by_xpath('//*[@class="ivu-menu-submenu ivu-menu-opened"]/ul/li[1]').click()
#fenqi
# driver.find_element_by_xpath('//*[@class="ivu-menu-submenu ivu-menu-opened"]/ul/li[2]').click()
# time.sleep(1)
login()
filres()
total=driver.find_element_by_xpath('//*[@class="ivu-page-total"]')
print(total.text)
c=int(total.text.split(' ')[1])
count=math.floor(c/100)
driver.find_element_by_xpath('//*[@class="ivu-select ivu-select-single ivu-select-small"]/div/div/span').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@class="ivu-select ivu-select-visible ivu-select-single ivu-select-small"]/div[2]/ul[2]/li[6]').click()
ctext=driver.page_source
with open('a.txt','w') as f:
    f.write(ctext)
f.close()
now = datetime.datetime.now()
format = "%Y-%m-%d-%H-%M-%S"
# filename = 'doni-pdl-'+now.strftime(format)+'.csv'
filename = 'doni-' + now.strftime(format) + '.csv'
def savefile(afile):
    with open(filename, 'a') as f:
        head = [
                ]
        writer = csv.writer(f, dialect='excel')
        writer.writerow(head)
    f.close()
    with open(afile, 'r', encoding='utf-8') as f:
        content = f.read()
    f.close()
    restxt = BeautifulSoup(content,'html.parser')
    for lines in restxt.find_all('tr',class_="ivu-table-row"):
        lineslist = []
        for line in lines.find_all('span'):
            lineslist.append(line.string)
        # print(lineslist)
        with open(filename,'a' ,newline='') as f:
            csv_writer =csv.writer(f)
            csv_writer.writerow(lineslist)
        f.close()
savefile('a.txt')
i=1
while i <= count:
    print(i)
    try:
        driver.find_element_by_xpath('//*[@class="ivu-page-next"]' ).click()
        res=driver.page_source
        with open('a.txt','w') as f:
            f.write(res)
        f.close()
        time.sleep(3)
        savefile('a.txt')
    except Exception as e:
        login()
        filres()
        driver.find_element_by_xpath('//*[@class="ivu-select ivu-select-single ivu-select-small"]/div/div/span').click()
        time.sleep(1)
        driver.find_element_by_xpath(
            '//*[@class="ivu-select ivu-select-visible ivu-select-single ivu-select-small"]/div[2]/ul[2]/li[6]').click()
        n=0
        while n < i:
            try:
                driver.find_element_by_xpath('//*[@class="ivu-page-next"]').click()
            except Exception as e:
                break
            n = n + 1
    i = i + 1

# driver.quit()



