#!/usr/bin/python3

import pymysql
import time
import signal

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

HOST = '172.17.0.1'
PORT = 3306
USERNAME = 'admin_ss1'
PASSWORD = ''
DBNAME = 'admin_ss1'
UPDATE_TIME = 300
data = []

FROM_ADDR = ""
MAIL_USR = ""
MAIL_PWD = ""
SMTP_SERVER = ""

loop = True

#读取数据库连接
def exec_sql(sql):
    import pymysql
    conn = pymysql.connect(
        host=HOST,
        user=USERNAME,
        passwd=PASSWORD,
        db=DBNAME,
        port=PORT,
        charset='utf8'
        )
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
        data = 'error'
    finally:
        conn.close()
    return data


def traffic_check(all_user):
    sql = "SELECT u, d, transfer_enable, id FROM user"
    tmp = exec_sql(sql)
    for i in tmp:
        if i['u'] + i['d'] > i['transfer_enable']:
            for n in all_user:
                if n['id'] == i['id']:
                    n['enable'] = 0


def get_change():
    from copy import deepcopy
    global data
    sql = "SELECT id, email, enable FROM user"
    data_cache = exec_sql(sql)
    if data_cache == 'error':
        return 'error'
    traffic_check(data_cache)
    if data_cache == data:
        return 'None'
    else:
        #检索变更
        data_change = [
            i for i in data_cache
            if i not in [m for m in data if m in data_cache]
        ]
        data = deepcopy(data_cache)
    return data_change


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

#根据域名选择发件服务器，暂时不用
def check_mail(m):
    import re
    if re.match(r'.*@163\.com', m):
        return True
    if re.match(r'.*@qq\.com', m):
        return True
    if re.match(r'.*@gmail\.com', m):
        return True
    if re.match(r'.*@icloud\.com', m):
        return True
    else:
        return False


def send_mail(to_addr):
    msg = MIMEText('您在的服务因[账户过期]或[流量超额]导致服务暂停，请登录网站 查看详情', 'plain', 'utf-8')
    msg['From'] = _format_addr('客户支持 <%s>' % FROM_ADDR)
    msg['To'] = _format_addr('用户 <%s>' % to_addr)
    msg['Subject'] = Header('服务暂停通知', 'utf-8').encode()

    server = smtplib.SMTP(SMTP_SERVER, 587)
#    server.set_debuglevel(0)
    server.ehlo()
    server.starttls()
    server.login(MAIL_USR, MAIL_PWD)
    server.sendmail(FROM_ADDR, [to_addr], msg.as_string())
    server.quit()


def receive_signal(signum, stack):
    global loop
    loop = False

signal.signal(signal.SIGTERM, receive_signal)
signal.signal(signal.SIGINT, receive_signal)

def main():
    global loop
    mail_list=[]
    get_change()
    print(time.asctime(time.localtime(time.time())) + ' start')
    while loop:
        try:
            changed=get_change()
            if changed != "None":
                mail_list = [ i for i in changed if i['enable']==0 ]
                for m in mail_list:
                    print(time.asctime(time.localtime(time.time())) + ' send to ' + m['email'])
                    send_mail(m['email'])
            
        except Exception as e:
            print(e)
        update_time = UPDATE_TIME
        while loop and update_time>0:
            update_time -=1
            time.sleep(1)


if __name__ == "__main__":
    main()
