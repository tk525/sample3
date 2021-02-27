import os
import sys
sys.path.append('../')

import datetime
import numpy as np
import random, string

from app import database, l1_login

def user_check():

    ip = l1_login.get_ip().pop()
    result = database.l3_create_user_show_ip(ip)
    return result

def l3_user_show():

    ip = l1_login.get_ip().pop()
    # database.l3_create_user_show_all(user_name, birth, mail, tel, credit_card, ip)
    datas = np.array(database.l3_create_user_show_all(ip))

    return datas

def l3_cuser(user_name, birth, mail, tel, credit_card):

    ip = l1_login.get_ip().pop()

    rmname_pre = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
    rmname = ''.join(rmname_pre)

    database.l3_create_user_insert(user_name, birth, mail, tel, credit_card, ip, rmname)

    #＋日記/メンタルヘルス、心理カウンセラーからのメモを暗号化

    ip = l1_login.get_ip().pop()

    database.l2_dairy_update(ip)
    database.l3_mc_update(ip)

def cuser_update(lists):

    ip = l1_login.get_ip().pop()

    rmname_pre = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
    rmname = ''.join(rmname_pre)

    id_num = database.l3_create_user_show_idnum(ip)
    database.l3_uc_update(lists, id_num, rmname)