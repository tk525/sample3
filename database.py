import psycopg2
import config


def connect(ip, once_neg_percent):
    """ Connect to the PostgreSQL database server """
    ip = ip.pop() #list解除
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
