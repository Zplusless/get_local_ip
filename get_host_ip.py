'''
if ip of local computer changes, send new ip to the TARGET_EMAIL_ADRESS
'''

import socket
import os
import pickle
import datetime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


CONFIG = './config'         # config file path
SOME_IP = 'baidu.com'       # some website you can visit
EMAIL_ADRESS = 'email_address'  # your email
PASSWORD = 'password'           # your email password
SERVER = 'server_adress'        # your email server adress
TARGET_EMAIL_ADRESS = 'target_address'  # who will recieve the email 



def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((SOME_IP, 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def judge(ip, CONFIG = CONFIG):
    if os.path.exists(CONFIG):
        old_ip = ''
        with open(CONFIG, 'r', newline='') as file:
            old_ip = file.read()
        if old_ip == ip:
            print('ip没有改变，不需要发送')
            return False  # 不用发送
        else:
            with open(CONFIG, 'w') as file:
                file.write(ip)
            print('ip改变，已更新记录并发送邮件')
            return True
    else:
        with open(CONFIG, 'w') as file:
            file.write(ip)
        print('未找到记录，已发送邮件')
        return True

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_email(content, to_adress):

    from_addr = EMAIL_ADRESS
    password = PASSWORD
    to_addr = to_adress
    smtp_server = SERVER

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = MIMEText('hello, the ip is ' + content + '\n' + time_now, 'plain', 'utf-8')
    msg['From'] = _format_addr('服务器ip监控 <%s>' % from_addr)
    msg['To'] = _format_addr('edge <%s>' % to_addr)
    msg['Subject'] = Header('GPU服务器ip变动为：'+ content, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()




if __name__ == '__main__':
    ip = get_host_ip()
    if judge(ip = ip):
        send_email(ip, TARGET_EMAIL_ADRESS)
        print('邮件发送成功!!')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # else:
    #     print('ip not changed')

