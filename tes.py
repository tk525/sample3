import database, l1_login

ip = l1_login.get_ip().pop()
x = database.l1_user_show(ip)
print(x)