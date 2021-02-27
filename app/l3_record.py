import numpy as np

import l1_login, database



def l3_record():
    ip = l1_login.get_ip().pop()

    paid_member_result = database.l3_create_user_show_ip(ip)

    return paid_member_result
