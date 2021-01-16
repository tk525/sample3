import psycopg2
import config
import numpy as np
import datetime



#l1_user 表示
def l1_user_show(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    #全て取得
    # sql_l1_select = "SELECT * FROM l1_user;"
    # 一部のみ取得
    sql = "SELECT * FROM l1_user where user_id = '%s';"%(ip,)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l1_user Database connection closed.')
 
    return show

#l1_userのipが一致する最終レコードを取得 表示
def l1_user_last_record(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT login_user_id, text_score, created_on, num_of_times_using_bad_word FROM l1_login JOIN l1_user ON l1_login.login_user_id=l1_user.user_id ORDER BY created_on DESC LIMIT 1;" #IDが一致したデータの最後に更新されたものを取得
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close()  
    print('l1_user_last_record Database connection closed.')
    return show

#l1_user 挿入
def l1_user_connect(ip, once_neg_percent, text):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        


        sql = "SELECT login_user_id, text_score, created_on, num_of_times_using_bad_word FROM l1_login JOIN l1_user ON l1_login.login_user_id=l1_user.user_id ORDER BY created_on DESC LIMIT 1;" #IDが一致したデータの最後に更新されたものを取得
        cur.execute(sql)

        #全て取得
        show = cur.fetchall()
        show = np.array(show)
        show = np.ravel(show)


        #l1_user データ挿入
        if type(show[len(show)-1]) == datetime.datetime: #最後のレコードの挿入されてるデータ型が日付であれば。つまり、初回であれば
            # 数字のみ
            # sql_l1_insert = "INSERT INTO l1_user (user_id, text) VALUES (0062, 111);"
            # 数字・文字入れれる
            # sql_l1_insert = "INSERT INTO l1_user (user_id, text) VALUES ('%s', '%s');"%('aaa','DSAD',)
            # 変数代入
            sql = "INSERT INTO l1_user (user_id, text_score, text) VALUES ('%s', '%s', '%s');"%(ip, once_neg_percent, text)

        elif type(show[len(show)-1]) == int:
            sql = "INSERT INTO l1_user (user_id, text_score, text, num_of_times_using_bad_word) VALUES ('%s', '%s', '%s', '%s');"%(ip, once_neg_percent, text, show[len(show)-1])

        cur.execute(sql)
        conn.commit() #挿入

       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l1_user_connect Database connection closed.')

def l1_user_connect_with_bw(ip, once_neg_percent, text, num_of_bw):
    """ Connect to the PostgreSQL database server """
    conn = None


    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        sql = "INSERT INTO l1_user (user_id, text_score, text, num_of_times_using_bad_word) VALUES ('%s', '%s', '%s', '%s');"%(ip, once_neg_percent, text, num_of_bw)
        cur.execute(sql)
        conn.commit() #挿入
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l1_user_connect Database connection closed.')






#l1_login 挿入
def l1_login_connect(ip):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        sql = "INSERT INTO l1_login (login_user_id) VALUES ('%s');"%(ip)

        cur.execute(sql)
        conn.commit() #挿入
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l1_login_connect Database connection closed.')

#l1_loginの最終レコードのみ 表示
def l1_login_show(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l1_login where login_user_id = '%s' ORDER BY id DESC LIMIT 1;"%(ip,) #IDが一致したデータの最後に更新されたものを取得
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l1_login_show Database connection closed.')
    return show





#l2_personality 挿入
def l2_personality(ip, record, personality_result):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        sql = "INSERT INTO l2_personality (personality_user_id, record, personality_result) VALUES ('%s', '%s', '%s');"%(ip, record, personality_result)

        cur.execute(sql)
        conn.commit() #挿入
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l2_personality Database connection closed.')

#l2_personalityの全てのレコードを取得 表示
def l2_personality_all_record():
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l2_personality;"
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l2_personality_all_record Database connection closed.') 
    return show 

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
    print('l2_personality Database connection closed.') 
    return show 



#l2_dairy 挿入
def l2_dairy(ip, mind, re_text):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        sql = "INSERT INTO l2_dairy (dairy_user_id, dairy_mind, dairy_text) VALUES ('%s', '%s', '%s');"%(ip, mind, re_text)

        cur.execute(sql)
        conn.commit() #挿入
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l2_dairy Database connection closed.')

#l2_dairy 表示
def l2_dairy_show(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l2_dairy where dairy_user_id = '%s';"%(ip,)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l2_dairy Database connection closed.') 
    return show 



#l2_endg 挿入or更新
def l2_endg(ip, end_goal, end_goal_tasks):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        """DBに同じIPアドレスがある場合はend_goal_tasksのみを更新させるために、
        ipアドレスでDB内を検索し、もしあればend_goal_tasksのみ更新。
        無くて、l2_endg.pyからend_goal_tasksを受け取っていればor受け取ってなければの分岐を作成
        """
        sql = "SELECT * FROM l2_endg where endg_user_id = '%s';"%(ip,)
        cur.execute(sql)
        show = cur.fetchall()

        if not show: #ipアドレスでDB内を検索して、無い場合

            if end_goal_tasks == 'empty': #l2_endg.pyからend_goal_tasksを受け取ってなければ
                sql = "INSERT INTO l2_endg (endg_user_id, end_goal) VALUES ('%s', '%s');"%(ip, end_goal)
            else: #l2_endg.pyからend_goal_tasksを受け取っていれば
                sql = "INSERT INTO l2_endg (endg_user_id, end_goal, end_goal_tasks) VALUES ('%s', '%s', '%s');"%(ip, end_goal, end_goal_tasks)

        else: #end_goal_tasksのみ更新
            sql = "UPDATE l2_endg set end_goal_tasks = (select REPLACE (end_goal_tasks, '', '%s'));"%(end_goal_tasks,)

        cur.execute(sql)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l2_endg Database connection closed.')

#l2_endg 表示
def l2_endg_show(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l2_endg where endg_user_id = '%s';"%(ip,)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l2_endg Database connection closed.') 
    return show 





#l3_dairy ID一致・最終更新されたものを表示
def l3_dairy(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    #IDが一致したデータの最後に更新されたものを取得
    sql = "SELECT * FROM l1_login where login_user_id = '%s' ORDER BY id DESC LIMIT 1;"%(ip,)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close()
    print('l3_dairy(仮) Database connection closed.')  
    return show



#l3_bbs_txt 全て表示
def l3_bbs_txt(ip):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l3_bullentin_board_text where bbs_txt_user_id = '%s';"%(ip,)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_txt 指定した日付表示
def l3_bbs_txt_show_date(date):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l3_bullentin_board_text WHERE bbs_txt_created_on::text LIKE '{}%';".format(date)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_txt 指定したid表示
def l3_bbs_txt_show_id(id):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l3_bullentin_board_text where id = '%s';"%(id,)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 


def l3_bbs_txt_insert(ip, text):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        sql = "INSERT INTO l3_bullentin_board_text (bbs_txt_user_id, bbs_txt_text) VALUES ('%s', '%s');"%(ip, text)
        cur.execute(sql)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('suspended_and_baned Database connection closed.')



#l3_bbs_act 指定した日付のアクション表示
def l3_bbs_act_show_date(date):
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor() 

    sql = "SELECT * FROM l3_bullentin_board_act WHERE bbs_act_created_on::text LIKE '{}%';".format(date)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 




#垢BAN / 3日間のsuspended 挿入
def suspended_and_baned(ip, level):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()        

        sql = "INSERT INTO suspended_and_baned (sb_user_id, sb_level) VALUES ('%s', '%s');"%(ip, level)
        cur.execute(sql)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('suspended_and_baned Database connection closed.')

#垢BAN / 3日間のsuspended 表示
def suspended_and_baned_show(ip):
    """ Connect to the PostgreSQL database server """
    conn = None

    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()        

    sql = "SELECT * FROM suspended_and_baned WHERE sb_user_id = '%s';"%(ip,)
    cur.execute(sql)

    #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close()
    print('suspended_and_baned Database connection closed.')
    return show

#垢BAN / 3日間のsuspended 削除
def suspended_and_baned_delete(ip):
    """ Connect to the PostgreSQL database server """
    conn = None

    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()        

    sql = "delete from suspended_and_baned where sb_user_id = '%s';"%(ip,)
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()
    print('suspended_and_baned Database connection closed.')
