import psycopg2
import config

#Level1_user 表示
def l1_ai_show(ip):
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



#Level1_user 挿入
def l1_ai_connect(ip, once_neg_percent):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        #l1_user dprappデータベースの中身表示
        sql_l1_select = "SELECT * FROM l1_user;"

        #l1_user データ挿入
    # 数字のみ
        # sql_l1_insert = "INSERT INTO l1_user (user_id, text) VALUES (0062, 111);"
    # 数字・文字入れれる
        # sql_l1_insert = "INSERT INTO l1_user (user_id, text) VALUES ('%s', '%s');"%('aaa','DSAD',)
    # 変数代入
        sql_l1_insert = "INSERT INTO l1_user (user_id, text) VALUES ('%s', '%s');"%(ip, once_neg_percent,)

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



#Level1_login 挿入
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

#Level1_user 表示
def l1_login_show(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql_l1_select = "SELECT * FROM l1_login where user_id = '%s' ORDER BY id DESC LIMIT 1;"%(ip,) #IDが一致したデータの最後に更新されたものを取得
    cur.execute(sql_l1_select)

     #全て取得
    l1_show = cur.fetchall()

    cur.close()
    conn.close()  
    return l1_show

