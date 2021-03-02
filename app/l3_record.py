import os
import sys
sys.path.append('../')

import numpy as np

from app import l1_login, database



def l3_record():

    paid_member_result = database.l3_create_user_show_ip()

    return paid_member_result
