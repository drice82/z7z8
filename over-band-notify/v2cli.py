#!/usr/bin/python3

import pymysql
#import os
#import sys
import time
#import json
#import subprocess
import signal

HOST = '192.168.99.199'
PORT = 3306
USERNAME = 'root'
PASSWORD = ' '
DBNAME = 'admin_ss1'
MUL = 1
UPDATE_TIME = 10

User_list = []
data = []

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

def pull_user():
    from copy import deepcopy
    global data
    sql = "SELECT id, email, enable, uuid FROM user"
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
        data_id = [x['uuid'] for x in data]
        data_cache_id = [y['uuid'] for y in data_cache]
        id_change = [z for z in data_id if z not in data_cache_id]
        data_delete =[]
        for n1 in data:
            for n2 in id_change:
                if n1['uuid'] == n2:
                    n1['enable'] = 0
                    data_delete.append(n1)
        data_all = data_change + data_delete
        data = deepcopy(data_cache)
    return data_all



def receive_signal(signum, stack):
    global loop
    loop = False

signal.signal(signal.SIGTERM, receive_signal)
signal.signal(signal.SIGINT, receive_signal)

def main():
    global loop
    pull_user()
    while loop:
        #print(time.asctime(time.localtime(time.time())))
        try:
#            accept_cfg()
            user1=pull_user()
            print(user1)
        except Exception as e:
            print(e)
        update_time = UPDATE_TIME
        while loop and update_time>0:
            update_time -=1
            time.sleep(1)


if __name__ == "__main__":
    main()
