import bleach, database, l1_login


# ip = l1_login.get_ip().pop()
# x = database.l1_user_last_record(ip)

x = bleach.clean('anko')
print(x)
#SQL攻撃対策

# sql = "SELECT * FROM l1_user where user_id = %s;"
# para = (ip,)