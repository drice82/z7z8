#!/usr/bin/python3

import pymysql
import os
import sys
import time
import json
import subprocess
import signal
import hashlib
import base64

HOST = os.environ.get('MYSQL_HOST', 'mysqlserver.net')
PORT = int(os.environ.get('MYSQL_PORT', 3306))
USERNAME = os.environ.get('MYSQL_USERNAME', 'admin_ss1')
PASSWORD = os.environ.get('MYSQL_PWD', 'mysqlpassword')
DBNAME = os.environ.get('MYSQL_DBNAME', 'admin_ss1')
MUL = float(os.environ.get('SET_MUL', 1))
UPDATE_TIME = int(os.environ.get('UPDATE_TIME', 120))
ENABLED_SS = int(os.environ.get('ENABLED_SS', 0))

V2CTL_PATH = '/usr/bin/xray'
CONFIG_PATH = '/app/tmp_inbounds.json'
CTL_PORT = 10085
User_list = []
data = []

loop = True

def md5_base64_hex(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    # 十六进制数据字符串值
    md5_str = m.hexdigest()
    b64_str = base64.b64encode(md5_str.encode('utf-8'))
    return b64_str.decode('utf-8')

def update_traffic():
    for u_list in User_list:
        try:
            traffic_msg = get_traffic(u_list['email'])
            if traffic_msg !=0:
                tra_sql = 'UPDATE user SET d=d+' + str(int(traffic_msg[0]*MUL)) + ', u=u+' + str(int(traffic_msg[1]*MUL)) + ', t=' + str(traffic_msg[2]) + ' WHERE email=\'' + u_list['email'] + '\''
                exec_sql(tra_sql)
        except Exception as e:
            print('Traffic read error!')
            print(e)


def get_traffic(user_email):
    def traffic_get_msg(cmd):
        import re
        try:
            exec_cmd = subprocess.Popen(
                    (cmd),
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True)
            outs, errs = exec_cmd.communicate(timeout = 1)
        except subprocess.TimeoutExpired as e:
            exec_cmd.kill()
            return 0
        finally:
            exec_cmd.kill()
        allouts = (outs + errs).decode()
        error_str = 'failed to get'
        check_error = re.search(error_str, str(allouts))
        if check_error is not None:
            return 0
        else:
            try:
                traffic_values = json.loads(allouts)["stat"]["value"]
                return traffic_values
            except Exception as e:
                return 0

    cmd_downlink = V2CTL_PATH + ' api stats --server=127.0.0.1:' + str(
        CTL_PORT) + ' -name \"user>>>' + user_email + '>>>traffic>>>downlink\" -reset'
    cmd_uplink = V2CTL_PATH + ' api stats --server=127.0.0.1:' + str(
        CTL_PORT) + ' -name \"user>>>' + user_email + '>>>traffic>>>uplink\" -reset'
    d_data = int(traffic_get_msg(cmd_downlink))
    u_data = int(traffic_get_msg(cmd_uplink))
    if d_data == 0:
        return 0
    else:
        use_time = int(time.time())
        return d_data, u_data, use_time


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
    sql = "SELECT id, email, enable, uuid, passwd, port FROM user"
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


def sql_cov_json(userlist):
    #获取配置文件
    def get_config_json():
        with open(CONFIG_PATH, 'rb+') as f:
            json_dict = json.loads(f.read().decode('utf8'))
        return json_dict

    #生成新的clients字段
    def make_config_json():
        global User_list
        for user in userlist:
            if user['enable'] == 1:
                usrname_cfg = {}
                usrname_cfg['id'] = user['uuid']
                usrname_cfg['email'] = user['email']
                #usrname_cfg['level'] = 0
                usrname_cfg['password'] = user['passwd'] + str(user['port'])
                User_list.append(usrname_cfg)
            elif user['enable'] == 0:
                del_user = [i for i in User_list if i['id'] == user['uuid']]
                User_list = [m for m in User_list if m not in del_user]
        return User_list

    #在配置中更新clients字段
    def create_config_json():
        from copy import deepcopy
        c_dict = get_config_json()
        users1 = make_config_json()
        #update vless_ws
        users_tmp = deepcopy(users1)
        for i in users_tmp:
            del i['password']
        c_dict["inbounds"][3]["settings"].update({'clients':users_tmp})

        #update trojan
        users_tmp = deepcopy(users1)
        for i in users_tmp:
            del i['id']
        c_dict["inbounds"][1]["settings"].update({'clients':users_tmp})

        #update ss
        if ENABLED_SS == 1:
            users_tmp = deepcopy(users1)
            for i in users_tmp:
                del i['id']
                i['password'] = md5_base64_hex(i['password'])
            c_dict["inbounds"][4]["settings"].update({'clients':users_tmp})

        #update vmess
        users_tmp = deepcopy(users1)
        for i in users_tmp:
            #i['alterId'] = 16
            del i['password']
        c_dict["inbounds"][2]["settings"].update({'clients':users_tmp})

        #update vless_xtls
        users_tmp = deepcopy(users1)
        for i in users_tmp:
            i['flow'] = 'xtls-rprx-direct'
            del i['password']
        c_dict["inbounds"][0]["settings"].update({'clients':users_tmp})
        return c_dict

    #更新json并格式化
    def format_json():
        config_dict = create_config_json()
        config_str = json.dumps(
                config_dict, sort_keys=False, indent=4, separators=(',', ':'))
        with open(CONFIG_PATH, 'wb+') as f:
            f.write(config_str.encode('utf8'))
    #执行
    format_json()

def update_cfg(u_list):
    sql_cov_json(u_list)
    res=os.popen(V2CTL_PATH + ' api rmi --server=127.0.0.1:' + str(CTL_PORT) + ' "xtls" "vless" "vmess" "trojan" "shadowsocks"').read()
    #print("1" + res)
    res=os.popen(V2CTL_PATH + ' api adi --server=127.0.0.1:' + str(CTL_PORT) + ' /app/tmp_inbounds.json').read()
    #print("2" + res)
    if ENABLED_SS == 0:
        res=os.popen(V2CTL_PATH + ' api rmi --server=127.0.0.1:' + str(CTL_PORT) + ' "shadowsocks"').read()
        #print("3" + res)

def accept_cfg():
    user_config_temp = pull_user()
    if user_config_temp !='None':
        print(time.asctime(time.localtime(time.time())) + ' Update user list.')
        try:
            update_cfg(user_config_temp)
        except Exception as e:
            print(e)
            print('Update Error!')
    #else:
        #print('no update')

def receive_signal(signum, stack):
    global loop
    loop = False

signal.signal(signal.SIGTERM, receive_signal)
signal.signal(signal.SIGINT, receive_signal)

def main():
    print("V2cli is running")
    global loop
    while loop:
        #print(time.asctime(time.localtime(time.time())))
        try:
            update_traffic()
            accept_cfg()
        except Exception as e:
            print(e)
        update_time = UPDATE_TIME
        while loop and update_time>0:
            update_time -=1
            time.sleep(1)


if __name__ == "__main__":
    main()

