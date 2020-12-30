import psycopg2
import config

#l1_user 表示
def l1_user_show(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    #全て取得
    # sql_l1_select = "SELECT * FROM l1_user;"
    # 一部のみ取得
    sql_l1_select = "SELECT * FROM l1_user where user_id = '%s';"%(ip,)
    cur.execute(sql_l1_select)

     #全て取得
    l1_show = cur.fetchall()

    cur.close()
    conn.close()  
    return l1_show

#l1_user 挿入
def l1_user_connect(ip, once_neg_percent, text):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        #l1_user データ挿入
    # 数字のみ
        # sql_l1_insert = "INSERT INTO l1_user (user_id, text) VALUES (0062, 111);"
    # 数字・文字入れれる
        # sql_l1_insert = "INSERT INTO l1_user (user_id, text) VALUES ('%s', '%s');"%('aaa','DSAD',)
    # 変数代入
        sql_l1_insert = "INSERT INTO l1_user (user_id, text_score, text) VALUES ('%s', '%s', '%s');"%(ip, once_neg_percent, text)

        cur.execute(
            sql_l1_insert
        )
        conn.commit() #挿入

        # cur.fetchall()
        # x = cur.fetchall()
        # print(x)

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



#l1_login 挿入
def l1_login_connect(ip):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        sql_l1_login_insert = "INSERT INTO l1_login (user_id) VALUES ('%s');"%(ip)

        cur.execute(
            sql_l1_login_insert
        )
        conn.commit() #挿入
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

#l1_loginの最終レコードのみ 表示
def l1_login_show(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql_l2_select = "SELECT * FROM l1_login where login_user_id = '%s' ORDER BY id DESC LIMIT 1;"%(ip,) #IDが一致したデータの最後に更新されたものを取得
    cur.execute(sql_l2_select)

     #全て取得
    l1_show = cur.fetchall()

    cur.close()
    conn.close()  
    return l1_show



#l1_userのipが一致する最終レコードを取得 表示
def l1_user_last_record(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT login_user_id, text_score, created_on FROM l1_login JOIN l1_user ON l1_login.login_user_id=l1_user.user_id ORDER BY created_on DESC LIMIT 1;" #IDが一致したデータの最後に更新されたものを取得
    cur.execute(sql)

     #全て取得
    l1_show = cur.fetchall()

    cur.close()
    conn.close()  
    return l1_show





#l2_personality 挿入
def l2_personality(ip, record, personality_result):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        sql = "INSERT INTO l2_personality (personality_user_id, record, personality_result) VALUES ('%s', '%s', '%s');"%(ip, record, personality_result)

        cur.execute(
            sql
        )
        conn.commit() #挿入
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

#l2_personalityの最終レコードを取得 表示
def l2_personality_last_record(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l2_personality where personality_user_id = '%s' ORDER BY id DESC LIMIT 1;"%(ip,) #IDが一致したデータの最後に更新されたものを取得
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close()  
    return show 




