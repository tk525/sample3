import psycopg2
import os
import numpy as np
import datetime
from psycopg2.extras import DictCursor

DATABASE_URL = os.environ.get('DATABASE_URL')

#l1_user 表示
def l1_user_show(ip):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    #全て取得
    # sql_l1_select = "SELECT * FROM l1_user;"
    # 一部のみ取得
    # sql = "SELECT * FROM l1_user where user_id = '%s';"%(ip,)

    sql = "SELECT * FROM l1_user where user_id = %s;"
    para = (ip,)
    # sql = "SELECT * FROM l1_user where user_id = '%s';"%("'OR'A'='A")#全部引き出された

    cur.execute(
        sql,para
    )

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l1_user Database connection closed.')
 
    return show

#l1_userのipが一致する最終レコードを取得 表示
def l1_user_last_record(ip):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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
    
        print('ip_pd', pd.read_pickle("app/login.csv"))
        print('ip', ip)
        print('neg_percent', once_neg_percent)
        print('txt', text)

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        sql = "SELECT login_user_id, text_score, created_on, num_of_times_using_bad_word FROM l1_login JOIN l1_user ON l1_login.login_user_id=l1_user.user_id ORDER BY created_on DESC LIMIT 1;" #IDが一致したデータの最後に更新されたものを取得
        cur.execute(sql)

        #全て取得
        show = cur.fetchall()
        show = np.array(show)
        show = np.ravel(show)
        print('ここはDB', show)
        # ['192.168.3.3' '0.0' datetime.datetime(2021, 2, 22, 5, 59, 28, 848773), None] #4

        #l1_user データ挿入 バッドワード使用履歴の有無
        # if type(show[len(show)-1]) == datetime.datetime:
        if show[len(show)-1] == None or len(show) == 0: #最後のレコードの挿入されてるデータ型が日付であれば。つまり、初回であれば

            # sql = "INSERT INTO l1_user (user_id, text_score, text) VALUES ('%s', '%s', '%s');"%(ip, once_neg_percent, text)
            # SQL攻撃対策
            sql = "INSERT INTO l1_user (user_id, text_score, text) VALUES (%s, %s, %s);"
            para = (ip, once_neg_percent, text)

        # elif type(show[len(show)-1]) == int:
        elif show[len(show)-1] != None:
            # sql = "INSERT INTO l1_user (user_id, text_score, text, num_of_times_using_bad_word) VALUES ('%s', '%s', '%s', '%s');"%(ip, once_neg_percent, text, show[len(show)-1])
            #SQL攻撃対策 
            sql = "INSERT INTO l1_user (user_id, text_score, text, num_of_times_using_bad_word) VALUES (%s, %s, %s, %s);"
            para = (ip, once_neg_percent, text, show[len(show)-1])

        cur.execute(sql,para)
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
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "INSERT INTO l1_user (user_id, text_score, text, num_of_times_using_bad_word) VALUES ('%s', '%s', '%s', '%s');"%(ip, once_neg_percent, text, num_of_bw)
        #SQL攻撃対策
        sql = "INSERT INTO l1_user (user_id, text_score, text, num_of_times_using_bad_word) VALUES (%s, %s, %s, %s);"
        para = (ip, once_neg_percent, text, num_of_bw,)
        cur.execute(sql, para)
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
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "INSERT INTO l1_login (login_user_id) VALUES ('%s');"%(ip)
        #SQL攻撃対策
        sql = "INSERT INTO l1_login (login_user_id) VALUES (%s);"
        para = (ip,)

        cur.execute(sql, para)
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

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    # sql = "SELECT * FROM l1_login where login_user_id = '%s' ORDER BY id DESC LIMIT 1;"%(ip,) #IDが一致したデータの最後に更新されたものを取得
    #SQL攻撃対策
    sql = "SELECT * FROM l1_login where login_user_id = %s ORDER BY id DESC LIMIT 1;" #IDが一致したデータの最後に更新されたものを取得
    para = (ip,)
    cur.execute(sql, para)

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
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "INSERT INTO l2_personality (personality_user_id, record, personality_result) VALUES ('%s', '%s', '%s');"%(ip, record, personality_result)
        #SQL攻撃対策
        sql = "INSERT INTO l2_personality (personality_user_id, record, personality_result) VALUES (%s, %s, %s);"
        para = (ip, record, personality_result,)

        cur.execute(sql, para)
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

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    # sql = "SELECT * FROM l2_personality where personality_user_id = '%s' ORDER BY id DESC LIMIT 1;"%(ip,) #IDが一致したデータの最後に更新されたものを取得
    #SQL攻撃対策
    sql = "SELECT * FROM l2_personality where personality_user_id = %s ORDER BY id DESC LIMIT 1;" #IDが一致したデータの最後に更新されたものを取得
    para = (ip,)
    cur.execute(sql, para)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l2_personality Database connection closed.') 
    return show 





#l2_dairy 挿入
def l2_dairy(ip, mind, re_text, img):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "INSERT INTO l2_dairy (dairy_user_id, dairy_mind, dairy_text, img) VALUES ('%s', '%s', '%s', '%s');"%(ip, mind, re_text, img)
        #SQL攻撃対策
        sql = "INSERT INTO l2_dairy (dairy_user_id, dairy_mind, dairy_text, img) VALUES (%s, %s, %s, %s);"
        para = (ip, mind, re_text, img,)

        cur.execute(sql, para)
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

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor(cursor_factory=DictCursor) 

    # sql = "SELECT * FROM l2_dairy where dairy_user_id = '%s' ORDER BY dairy_created_on DESC;"%(ip,)
    #SQL攻撃対策
    sql = "SELECT * FROM l2_dairy where dairy_user_id = %s ORDER BY dairy_created_on DESC;"
    para = (ip,)
    cur.execute(sql,para)

     #全て取得
    show = cur.fetchall()
    print('でーたべえす', show)

    cur.close()
    conn.close() 
    print('l2_dairy Database connection closed.') 
    return show 

#l2_dairy 表示
def l2_dairy_show_text_encode(ip):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    # sql = "SELECT encode(dairy_text::bytea, 'escape') FROM l2_dairy where dairy_user_id = '%s' ORDER BY dairy_created_on DESC;"%(ip,)
    #SQL攻撃対策
    sql = "SELECT encode(dairy_text::bytea, 'escape') FROM l2_dairy where dairy_user_id = %s ORDER BY dairy_created_on DESC;"
    para = (ip,)
    cur.execute(sql, para)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l2_dairy Database connection closed.') 
    return show 

#l2_dairy 更新
def l2_dairy_update(ip):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "SELECT encode(pm_user_name::bytea, 'escape') FROM paid_members;"
        # sql = "SELECT dairy_text FROM l2_dairy WHERE dairy_user_id = '%s';"%(ip,)
        #SQL攻撃対策
        sql = "SELECT dairy_text FROM l2_dairy WHERE dairy_user_id = %s;"
        para = (ip,)
        cur.execute(sql, para)
        show = np.array(cur.fetchall())
        show = np.ravel(show)
        # print(show)

        #l3_mcのmemoだけ暗号化
        for text in show:
            sql = "UPDATE l2_dairy SET dairy_text = '{}'::bytea WHERE dairy_user_id ='{}';".format(text,ip)

        cur.execute(sql, para)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l2_dairy Database connection closed.')





#l2_endg 挿入or更新
def l2_endg(ip, end_goal, end_goal_tasks):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        """DBに同じIPアドレスがある場合はend_goal_tasksのみを更新させるために、
        ipアドレスでDB内を検索し、もしあればend_goal_tasksのみ更新。
        無くて、l2_endg.pyからend_goal_tasksを受け取っていればor受け取ってなければの分岐を作成
        """
        # sql = "SELECT * FROM l2_endg where endg_user_id = '%s';"%(ip,)
        #SQL攻撃対策
        sql = "SELECT * FROM l2_endg where endg_user_id = %s;"
        para = (ip,)
        cur.execute(sql, para)
        show = cur.fetchall()

        if not show: #ipアドレスでDB内を検索して、無い場合

            if end_goal_tasks == 'empty': #l2_endg.pyからend_goal_tasksを受け取ってなければ
                # sql = "INSERT INTO l2_endg (endg_user_id, end_goal) VALUES ('%s', '%s');"%(ip, end_goal)
                #SQL攻撃対策
                sql = "INSERT INTO l2_endg (endg_user_id, end_goal) VALUES (%s, %s);"
                para = (ip, end_goal,)
            else: #l2_endg.pyからend_goal_tasksを受け取っていれば
                # sql = "INSERT INTO l2_endg (endg_user_id, end_goal, end_goal_tasks) VALUES ('%s', '%s', '%s');"%(ip, end_goal, end_goal_tasks)
                #SQL攻撃対策
                sql = "INSERT INTO l2_endg (endg_user_id, end_goal, end_goal_tasks) VALUES (%s, %s, %s);"
                para = (ip, end_goal, end_goal_tasks,)

        else: 
            if end_goal == 'empty':#end_goal_tasksのみ更新
                # sql = "UPDATE l2_endg SET (end_goal_tasks) = ('%s');"%(end_goal_tasks,)
                #SQL攻撃対策
                sql = "UPDATE l2_endg SET (end_goal_tasks) = (%s);"
                para = (end_goal_tasks,)
            else:
                # sql = "UPDATE l2_endg SET (end_goal, end_goal_tasks) = ('%s', '%s');"%(end_goal, end_goal_tasks,)
                #SQL攻撃対策
                sql = "UPDATE l2_endg SET (end_goal, end_goal_tasks) = (%s, %s);"
                para = (end_goal, end_goal_tasks,)


        cur.execute(sql, para)
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

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    # sql = "SELECT * FROM l2_endg where endg_user_id = '%s';"%(ip,)
    #SQL攻撃対策
    sql = "SELECT * FROM l2_endg where endg_user_id = %s;"
    para = (ip,)
    cur.execute(sql, para)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l2_endg Database connection closed.') 
    return show 





#l3_dairy ID一致・最終更新されたものを表示
def l3_dairy(ip):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    #IDが一致したデータの最後に更新されたものを取得
    # sql = "SELECT * FROM l1_login where login_user_id = '%s' ORDER BY id DESC LIMIT 1;"%(ip,)
    #SQL攻撃対策
    sql = "SELECT * FROM l1_login where login_user_id = %s ORDER BY id DESC LIMIT 1;"
    para = (ip,)
    cur.execute(sql, para)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close()
    print('l3_dairy(仮) Database connection closed.')  
    return show





#l3_bbs_txt 全て表示
def l3_bbs_all_txt():

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    sql = "SELECT * FROM l3_bullentin_board_text ORDER BY id DESC;"
    cur.execute(sql)
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_txt 全て表示
def l3_bbs_txt(ip):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    # sql = "SELECT * FROM l3_bullentin_board_text where bbs_txt_user_id = '%s';"%(ip,)
    #SQL攻撃対策
    sql = "SELECT * FROM l3_bullentin_board_text where bbs_txt_user_id = %s;"
    para = (ip,)
    cur.execute(sql, para)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_txt 指定した日付表示
def l3_bbs_txt_show_date(date):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    # sql = "SELECT * FROM l3_bullentin_board_text WHERE bbs_txt_user_id = '%s';"%(id,)
    #SQL攻撃対策
    sql = "SELECT * FROM l3_bullentin_board_text WHERE bbs_txt_user_id = %s;"
    para = (id,)
    cur.execute(sql, para)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_txt 指定したid表示
def l3_bbs_txt_show_post_id(id):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    # sql = "SELECT * FROM l3_bullentin_board_text where id = '%s';"%(id,)
    #SQL攻撃対策
    sql = "SELECT * FROM l3_bullentin_board_text where id = %s;"
    para = (id,)
    cur.execute(sql, para)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_txt 挿入
def l3_bbs_txt_insert(ip, text):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "INSERT INTO l3_bullentin_board_text (bbs_txt_user_id, bbs_txt_text) VALUES ('%s', '%s');"%(ip, text)
        #SQL攻撃対策
        sql = "INSERT INTO l3_bullentin_board_text (bbs_txt_user_id, bbs_txt_text) VALUES (%s, %s);"
        para = (ip, text,)
        cur.execute(sql, para)
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

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    sql = "SELECT * FROM l3_bullentin_board_act WHERE bbs_act_created_on::text LIKE '{}%';".format(date)
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_act 表示
def l3_bbs_act_show_id(id):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    # sql = "SELECT * FROM l3_bullentin_board_act WHERE bbs_act_user_id = '%s';"%(id,)
    #SQL攻撃対策
    sql = "SELECT * FROM l3_bullentin_board_act WHERE bbs_act_user_id = %s;"
    para = (id,)
    cur.execute(sql, para)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_act 表示
def l3_bbs_act_show_all():

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor() 

    sql = "SELECT * FROM l3_bullentin_board_act;"
    cur.execute(sql)

     #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show 

#l3_bbs_act 挿入
def l3_bbs_act_insert(ip, act):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "INSERT INTO l3_bullentin_board_act (bbs_act_user_id, bbs_act) VALUES ('%s', '%s');"%(ip, act)
        #SQL攻撃対策
        sql = "INSERT INTO l3_bullentin_board_act (bbs_act_user_id, bbs_act) VALUES (%s, %s);"
        para = (ip, act)
        cur.execute(sql, para)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l3_bbs_act Database connection closed.')

#l3_bbs_act 挿入
def l3_bbs_act_delete(ip, act):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "DELETE FROM l3_bullentin_board_act WHERE bbs_act_user_id = '%s' AND bbs_act = '%s';"%(ip, act)
        #SQL攻撃対策
        sql = "DELETE FROM l3_bullentin_board_act WHERE bbs_act_user_id = %s AND bbs_act = %s;"
        para = (ip, act,)
        cur.execute(sql, para)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l3_bbs_act Database connection closed.')





#l3_mc 挿入
def l3_mc_insert(ip, memo):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "INSERT INTO l3_mc (mc_user_id, memo) VALUES ('%s', '%s');"%(ip, memo)
        #SQL攻撃対策
        sql = "INSERT INTO l3_mc (mc_user_id, memo) VALUES (%s, %s);"
        para = (ip, memo,)
        cur.execute(sql, para)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('l3_mher Database connection closed.')

#l3_mc 更新
# def l3_mc_update(ip):
#     """ Connect to the PostgreSQL database server """
#     conn = None

#     try:
    
#         conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#         cur = conn.cursor()        

#         # sql = "SELECT encode(pm_user_name::bytea, 'escape') FROM paid_members;"
#         # sql = "SELECT memo FROM l3_mc WHERE mc_user_id = '%s';"%(ip,)
#         #SQL攻撃対策
#         sql = "SELECT memo FROM l3_mc WHERE mc_user_id = %s;"
#         para = (ip,)
#         cur.execute(sql, para)
#         show = np.array(cur.fetchall())
#         show = np.ravel(show)

#         #l3_mcのmemoだけ暗号化
#         for text in show:
#             sql = "UPDATE l3_mc SET memo = '{}'::bytea WHERE mc_user_id ='{}';".format(text,ip)

#         cur.execute(sql)
#         conn.commit()

#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('l3_mc Database connection closed.')





#paid_mambers 名前 表示
def l3_create_user_show():
    """ Connect to the PostgreSQL database server """
    conn = None


    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()        

    sql = "SELECT encode(pm_user_name::bytea, 'escape') FROM paid_members;"
    # sql = "SELECT * FROM paid_members;"
    cur.execute(sql)
    show = cur.fetchall()

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show

#paid_mambers 名前 表示
def l3_create_user_show_all(ip):
    """ Connect to the PostgreSQL database server """
    conn = None


    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()        

    sql = "SELECT encode(pm_user_id::bytea, 'escape') FROM paid_members;"
    cur.execute(sql)
    show = cur.fetchall()

    if show == []:
        datas = ''

    else:
        for num, ips in enumerate(show):
            if ips[0] == ip:
                break
        num = num + 1 #配列は0からだけど、DBは1からなので

        sql = ["SELECT encode(pm_user_name::bytea, 'escape') FROM paid_members WHERE id = "+ str(num) +";",
            "SELECT encode(pm_birth::bytea, 'escape') FROM paid_members WHERE id = "+ str(num) +";",
            "SELECT encode(pm_mail::bytea, 'escape') FROM paid_members WHERE id = "+ str(num) +";",
            "SELECT encode(pm_tel::bytea, 'escape') FROM paid_members WHERE id = "+ str(num) +";",
            "SELECT encode(pm_credit_card::bytea, 'escape') FROM paid_members WHERE id = "+ str(num) +";",
            "SELECT pm_room_name FROM paid_members WHERE id = "+ str(num) +";"
        ]

        datas_pre = []
        for i in range(len(sql)):
            cur.execute(sql[i])
            data = cur.fetchall()
            datas_pre.append(data)
        datas_pre=np.array(datas_pre)
        datas=np.ravel(datas_pre)

    cur.close()
    conn.close() 
    print('paidmembers Database connection closed.') 
    return datas

#paid_mambers ipアドレス 表示
def l3_create_user_show_ip(ip):
    """ Connect to the PostgreSQL database server """
    conn = None


    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()        

    sql = "SELECT encode(pm_user_id::bytea, 'escape') FROM paid_members;"
    cur.execute(sql)
    shows = cur.fetchall()

    num = 1
    if len(shows) > 0:
        for show in shows:
            if show[0] == ip:
                show = 'OK'
            else:
                show = ''
            num = num + 1 #配列番号になる
    else:
        show = ''


    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return show

#paid_mambers ipアドレス 表示
def l3_create_user_show_idnum(ip):
    """ Connect to the PostgreSQL database server """
    conn = None


    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()        

    sql = "SELECT encode(pm_user_id::bytea, 'escape') FROM paid_members;"
    cur.execute(sql)
    shows = cur.fetchall()

    num = 1
    for show in shows:
        if show[0] == ip:
            show = 'OK'
            break
        else:
            show = ''
        num = num + 1 #配列番号になる

    cur.close()
    conn.close() 
    print('l3_bbs_txt Database connection closed.') 
    return num

#paid_mambers 挿入
def l3_create_user_insert(user_name, birth, mail, tel, credit_card, ip, roomname):
# def l3_create_user_insert(user_name, birth, mail, tel, credit_card, ip):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        

        # sql = "INSERT INTO paid_members (pm_user_name, pm_birth, pm_mail, pm_tel, pm_credit_card, pm_user_id) VALUES ('%s'::bytea, '%s'::bytea, '%s'::bytea, '%s'::bytea, '%s'::bytea, '%s'::bytea);"%(user_name, birth, mail, tel, credit_card, ip)
        #SQL攻撃対策 roomnameだけは裸で
        sql = "INSERT INTO paid_members (pm_user_name, pm_birth, pm_mail, pm_tel, pm_credit_card, pm_user_id, pm_room_name) VALUES (%s::bytea, %s::bytea, %s::bytea, %s::bytea, %s::bytea, %s::bytea, %s);"
        # sql = "INSERT INTO paid_members (pm_user_name, pm_birth, pm_mail, pm_tel, pm_credit_card, pm_user_id) VALUES (%s::bytea, %s::bytea, %s::bytea, %s::bytea, %s::bytea, %s::bytea);"
        para = (user_name, birth, mail, tel, credit_card, ip, roomname)
        cur.execute(sql, para)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('paid_members Database connection closed.') 

#paid_mambers 挿入
def l3_uc_update(lists, id_num, roomname):
# def l3_uc_update(lists, id_num):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()        
        
        if len(lists) == 1:
        #SQL攻撃対策?
            sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea, pm_room_name = '"+roomname+"' WHERE id = "+str(id_num)+";"
            # sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea WHERE id = "+str(id_num)+";"

        if len(lists) == 2:
        #SQL攻撃対策?
            sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea,"+lists[1][0]+" = '"+lists[1][1]+"'::bytea, pm_room_name = '"+roomname+"' WHERE id = "+str(id_num)+";"
            # sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea,"+lists[1][0]+" = '"+lists[1][1]+"'::bytea WHERE id = "+str(id_num)+";"

        if len(lists) == 3:
        #SQL攻撃対策?
            sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea,"+lists[1][0]+" = '"+lists[1][1]+"'::bytea ,"+lists[2][0]+" = '"+lists[2][1]+"'::bytea, pm_room_name = '"+roomname+"' WHERE id = "+str(id_num)+";"
            # sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea,"+lists[1][0]+" = '"+lists[1][1]+"'::bytea ,"+lists[2][0]+" = '"+lists[2][1]+"'::bytea WHERE id = "+str(id_num)+";"

        if len(lists) == 4:
        #SQL攻撃対策?
            sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea ,"+lists[1][0]+" = '"+lists[1][1]+"'::bytea ,"+lists[2][0]+" = '"+lists[2][1]+"'::bytea ,"+lists[3][0]+" = '"+lists[3][1]+"'::bytea, pm_room_name = '"+roomname+"' WHERE id = "+str(id_num)+";"
            # sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea ,"+lists[1][0]+" = '"+lists[1][1]+"'::bytea ,"+lists[2][0]+" = '"+lists[2][1]+"'::bytea ,"+lists[3][0]+" = '"+lists[3][1]+"'::bytea WHERE id = "+str(id_num)+";"

        if len(lists) == 5: #一応フル変更verも用意
        #SQL攻撃対策?
            sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea ,"+lists[1][0]+" = '"+lists[1][1]+"'::bytea ,"+lists[2][0]+" = '"+lists[2][1]+"'::bytea ,"+lists[3][0]+" = '"+lists[3][1]+"'::bytea ,"+lists[4][0]+" = '"+lists[4][1]+"'::bytea, pm_room_name = '"+roomname+"' WHERE id = "+str(id_num)+";"
            # sql = "UPDATE paid_members SET "+lists[0][0]+" = '"+lists[0][1]+"'::bytea ,"+lists[1][0]+" = '"+lists[1][1]+"'::bytea ,"+lists[2][0]+" = '"+lists[2][1]+"'::bytea ,"+lists[3][0]+" = '"+lists[3][1]+"'::bytea ,"+lists[4][0]+" = '"+lists[4][1]+"'::bytea WHERE id = "+str(id_num)+";"

        cur.execute(sql)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('paid_members Database connection closed.') 







#垢BAN / 3日間のsuspended 挿入
def suspended_and_baned(ip, level):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
    
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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


    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()        

    # sql = "SELECT * FROM suspended_and_baned WHERE sb_user_id = '%s';"%(ip,)
    #SQL攻撃対策
    sql = "SELECT * FROM suspended_and_baned WHERE sb_user_id = %s;"
    para = (ip,)
    cur.execute(sql, para)

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


    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()        

    # sql = "delete from suspended_and_baned where sb_user_id = '%s';"%(ip,)
    #SQL攻撃対策
    sql = "delete from suspended_and_baned where sb_user_id = %s;"
    para = (ip,)
    cur.execute(sql, para)
    conn.commit()

    cur.close()
    conn.close()
    print('suspended_and_baned Database connection closed.')


