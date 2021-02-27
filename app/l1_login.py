import os
import sys
sys.path.append('../')

import netifaces as ni
import psutil
import socket
import datetime

from app import database



#ipアドレス取得
def get_ip() -> list:
    if os.name == "nt":
        # Windows
        return socket.gethostbyname_ex(socket.gethostname())[2]
        pass
    else:
        # それ以外
        result = []
        address_list = psutil.net_if_addrs()
        for nic in address_list.keys():
            ni.ifaddresses(nic)
            try:
                ip = ni.ifaddresses(nic)[ni.AF_INET][0]['addr']
                if ip not in ["127.0.0.1"]:
                    result.append(ip)
            except KeyError as err:
                pass
        return result



ip = get_ip().pop()
try:
    l1_login_last_record = database.l1_login_show(ip)
except:
    l1_login_last_record = ''


if len(l1_login_last_record) == 0:

    database.l1_login_connect(ip)

else:
    
    l1_login_last_record = l1_login_last_record.pop()

    #すでにログインしているかどうか判定
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    l1_login_last_time = l1_login_last_record[2].strftime('%Y-%m-%d')

    if time != l1_login_last_time:
        # IPアドレス+ログインタイム挿入
        database.l1_login_connect(ip)


    #IPアドレスが一致したデータの最終更新されたもので、ログインポイント付与判定
    login_point_judge = 'ログインポイント付与' if l1_login_last_record[0] % 3 == 0 else '' #計算
    print(login_point_judge)
