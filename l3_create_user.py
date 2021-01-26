import datetime
import numpy as np

import database, l1_login


user_name = "Olivia"
birth = datetime.datetime(1990, 5, 25).strftime("%Y/%m/%d")
mail = '@gmail.com'
tel = '111222333'
credit_card = 'E100000'

database.l3_create_user_insert(user_name, birth, mail, tel, credit_card)




#＋日記/メンタルヘルス、心理カウンセラーからのメモを暗号化

ip = l1_login.get_ip().pop()

database.l2_dairy_update(ip)
database.l3_mc_update(ip)
