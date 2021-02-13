import datetime
import numpy as np

import database, l1_login

def l3_user_show():

    ip = l1_login.get_ip().pop()
    # database.l3_create_user_show_all(user_name, birth, mail, tel, credit_card, ip)
    datas = np.array(database.l3_create_user_show_all(ip))

    return datas

def l3_cuser(user_name, birth, mail, tel, credit_card):

    ip = l1_login.get_ip().pop()
    database.l3_create_user_insert(user_name, birth, mail, tel, credit_card, ip)



    #＋日記/メンタルヘルス、心理カウンセラーからのメモを暗号化

    ip = l1_login.get_ip().pop()

    database.l2_dairy_update(ip)
    database.l3_mc_update(ip)
