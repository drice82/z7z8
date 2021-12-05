#!/usr/bin/python3
import requests
import pymysql
import time
import json
import math

# DB Setting
HOST = 'da.domain.net'
PORT = 3306
USERNAME = 'username'
PASSWORD = 'password'
DBNAME = 'dbname'

# Cost Setting, Monthly, Quarterly, Half Year, Annually
M_FEE = 16.8
Q_FEE = 48
H_FEE = 88
A_FEE = 168


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


def update_user(port, days):
    sql = "SELECT expire_time FROM user WHERE port = " + str(port)
    tmp = exec_sql(sql)
    expire_time = tmp[0]['expire_time']
    if expire_time > time.time():
        expire_time = expire_time + days * 86400
    else:
        expire_time = time.time() + days * 86400
    sql = "UPDATE user SET expire_time =" + str(expire_time) + ", enable = 1 WHERE port = " + str(port)
    exec_sql(sql)
    print ("user:", port, "added", days, "days")

def check_order():
    sql = "SELECT * FROM trc20 WHERE succ = 0 AND time_stamp > " + str(int(time.time())-2500)
    tmp = exec_sql(sql)
    for i in tmp:
        if check_payment(i['address'], int(i['time_stamp']), float(i['usdt'])):
            days = 0
            if math.isclose(i['cny'], M_FEE, rel_tol=1e-5) : days = 30
            if math.isclose(i['cny'], Q_FEE, rel_tol=1e-5) : days = 90
            if math.isclose(i['cny'], H_FEE, rel_tol=1e-5) : days = 180
            if math.isclose(i['cny'], A_FEE, rel_tol=1e-5) : days = 360
            update_user(i['port'], days)
            sql = "UPDATE trc20 SET succ = 1 WHERE id =" + str(i['id'])
            exec_sql(sql)

def check_payment(to_address, block_ts, usdt):
    block_ts = block_ts * 1000
    usdt = int(usdt * 1000000)
    r=requests.get("https://apilist.tronscan.org/api/token_trc20/transfers?tokens=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t&relatedAddress=" + to_address + "&start_timestamp=" + str(block_ts), timeout=30)
    data = r.json()['token_transfers']
    for i in data:
        if int(i['quant']) == usdt and i['confirmed'] == True: 
            return True

def main():
    check_order()

if __name__ == "__main__":
    main()
