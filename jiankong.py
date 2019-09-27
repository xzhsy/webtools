import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pymysql
import psutil
import os
import time


def mail(name, description, disk_send_info, cpu_send_info, mem_send_info):
    sender = 'mail_address'
    password = 'mail_password'
    reciver = 'xxx.xx@xx.com,xxx@xx.com'  # 可设置多人，用逗号分隔
    subject = 'xxx(监控项目名称):%s警告' % name + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    msg = MIMEMultipart('mixed')  # 初始化  注意：标题和正文不能分别初始化
    msg['From'] = sender
    msg['To'] = reciver
    msg['Subject'] = subject
    msg.attach(MIMEText(str(description), 'plain', 'utf-8'))
    msg.attach(MIMEText(str(disk_send_info), 'plain', 'utf-8'))  # 添加正式，MIMEText切记不能忘记
    msg.attach(MIMEText(str(cpu_send_info), 'plain', 'utf-8'))
    msg.attach(MIMEText(str(mem_send_info), 'plain', 'utf-8'))

    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.set_debuglevel(1)
    smtp.login(sender, password)
    smtp.sendmail(sender, reciver.split(','), msg.as_string())
    print('%s 发送成功' % subject)
    smtp.quit()


# 获得硬盘的信息
def disk_info(disk_find):
    # disk =  psutil.disk_partitions()
    # for i in disk:
    #     disk_partition = i.device       #所有硬盘盘符
    #     disk_use = psutil.disk_usage(disk_partition)
    #     disk_utilization = disk_use.percent
    disk_use = psutil.disk_usage(disk_find)
    disk_utilization = str(disk_use.percent)
    disk_total = '%sG' % (round(disk_use.total / 1024 / 1024 / 1024, 2))
    disk_used = '%sG' % (round(disk_use.used / 1024 / 1024 / 1024, 2))
    disk_free = '%sG' % (round(disk_use.free / 1024 / 1024 / 1024, 2))
    disk_msg = {'总量': disk_total,
                '已使用': disk_used,
                '空闲': disk_free,
                '使用率': disk_utilization + '%'
                }
    return disk_msg


def cpu_info():
    cpu_idle = str(os.popen("top -n 1 | sed -n '3p' | awk '{print $8}'").read()).strip()
    cpu_used = str(100 - float(cpu_idle)) + '%'
    cpu_msg = {'已使用': cpu_used,
               '剩余': str(cpu_idle) + '%'}
    return cpu_idle, cpu_msg


def memory_info():
    mem_free = str(os.popen("top -n 1 | sed -n '4p' | awk '{print $8}'").read()).strip()
    mem_buff = str(os.popen("top -n 1 | sed -n '4p' | awk '{print $10}'").read()).strip()
    mem_cached = str(os.popen("top -n 1 | sed -n '5p' | awk '{print $9}'").read()).strip()
    mem_total = round(int(str(os.popen("top -n 1 | sed -n '4p' | awk '{print $4}'").read()).strip()) / 1024 / 1024, 0)
    mem_free_total = round((int(mem_free) + int(mem_buff) + int(mem_cached)) / 1024 / 1024, 0)
    mem_free_ratio = str(round(int(mem_free_total) * 100 / int(mem_total), 2))
    mem_msg = {
        '总量': str(mem_total) + 'G',
        '已使用': str(mem_total - mem_free_total) + 'G',
        '剩余': mem_free_ratio + '%'
    }
    return mem_free_ratio, mem_msg


def mysql_monitor(user, password, host, port):
    try:
        conn = pymysql.connect(host=host, port=port, user=user, passwd=password)
    except:
        return '主人，数据库无法正常连接了，请尽快处理！！！'
    conn.close()


def docker_monitor():


# disk_find = str(os.popen("df -hT | grep /data |awk 'NR==1{print}' | awk '{print $1}'").read()).strip()#读取第一行
disk_find = '/data'
while True:
    disk_info_msg = disk_info(disk_find)
    cpu_tup = cpu_info()
    cpu_idle = cpu_tup[0]
    cpu_msg = cpu_tup[1]
    mem_tup = memory_info()
    mem_free_ratio = mem_tup[0]
    mem_msg = mem_tup[1]
    mysql_info = mysql_monitor('xxx(user)', 'xxxx(password)', '192.168.1.230', 3306)
    localtime = time.localtime()
    if str(localtime[3]) == '11':
        name = '正常'
        description = '主人，我乖乖的努力工作了一天哟，犒赏犒赏！！！'
        disk_send_info = '硬盘：' + str(disk_info_msg)
        cpu_send_info = 'CPU:' + str(cpu_msg)
        mem_send_info = '内存：' + str(mem_msg)
        print(disk_send_info)
        mail(name, description, disk_send_info, cpu_send_info, mem_send_info)
    if mysql_info:
        name = '数据库'
        description = mysql_info
        disk_send_info = '硬盘：' + str(disk_info_msg)
        cpu_send_info = 'CPU:' + str(cpu_msg)
        mem_send_info = '内存：' + str(mem_msg)
        mail(name, description, disk_send_info, cpu_send_info, mem_send_info)
    if int(float(disk_info_msg['使用率'][0:-1])) >= 80:
        os.popen('docker stop default-vidio')
        name = '硬盘'
        description = '主人，我吃胀了，请给我健胃消食片！！！！'
        disk_send_info = '硬盘：' + str(disk_info_msg)
        cpu_send_info = 'CPU:' + str(cpu_msg)
        mem_send_info = '内存：' + str(mem_msg)
        mail(name, description, disk_send_info, cpu_send_info, mem_send_info)
    # 小数后面是.0,先转浮点数在转整数
    if int(float(cpu_idle)) <= 20:
        name = 'CPU'
        description = '主人，我大脑不够用了，快救救我！！！！'
        disk_send_info = '硬盘：' + str(disk_info_msg)
        cpu_send_info = 'CPU:' + str(cpu_msg)
        mem_send_info = '内存：' + str(mem_msg)
        mail(name, description, disk_send_info, cpu_send_info, mem_send_info)
    if int(float(mem_free_ratio)) <= 20:
        name = '内存'
        description = '主人，我血液不畅通，快疏通疏通！！！！'
        disk_send_info = '硬盘：' + str(disk_info_msg)
        cpu_send_info = 'CPU:' + str(cpu_msg)
        mem_send_info = '内存：' + str(mem_msg)
        mail(name, description, disk_send_info, cpu_send_info, mem_send_info)
    time.sleep(3600)