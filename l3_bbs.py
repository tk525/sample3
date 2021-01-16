import pandas as pd
import numpy as np
import datetime
import random

import database, l1_login



class program:

    def anger_program():
        calm_mind_pre = list(pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', sheet_name='calm_the_mind_pg')['text'])
        
        calm_mind = random.choice(calm_mind_pre)

        return calm_mind
        


text_pre = 'love you'
text = text_pre.split()

bad_words_pre = list(pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', sheet_name='bad_word')['text'])


#ユーザーの最終スコア呼び出し
ip = l1_login.get_ip().pop()
score_pre = np.array(database.l1_user_last_record(ip))
score_pre = np.ravel(score_pre)
score = float(score_pre[1])
num_of_bw = int(score_pre[3])

#垢BANリスト呼び出し
ban_user_pre = np.array(database.suspended_and_baned_show(ip))
ban_user = np.ravel(ban_user_pre)
if len(ban_user) > 0:
    ban_user_date = ban_user[3]
    ban_user_lv = ban_user[2]
else:
    ban_user_date = datetime.datetime.now()
    ban_user_lv = 1

#実験用
# database.suspended_and_baned(ip, 1)
ban_user_lv = 0



# スコアが規定以上 / 垢BANの謹慎期間を超えた / sb_level=1
if score > 0.1 and ban_user_date <= datetime.datetime.now() and ban_user_lv == 1: #🌟本番ではscore > 0.8 and ban_user_date+datetime.timedelta(days=3) <= datetime.datetime.now() and ban_user_lv == 1

    #垢BANの謹慎期間を超えたので削除
    database.suspended_and_baned_delete(ip)

    if num_of_bw % 3 != 0: #禁止ワード3回目 🌟本番ではnum_of_bw % 3 != 0
        print('3日間使用停止')
        database.suspended_and_baned(ip, 1)

    else:
        result_bw = 0
        for text in text:
            if  text.lower() in bad_words_pre: #text内に悪い単語が含まれているか検索 textを全て小文字に変換

                result_bw = result_bw + 1

        if result_bw > 0: #悪い単語が使われていた場合
   
            new_score = score - (score / 20) #所持者の0.5%をスコアから引く

            if type(score_pre[len(score_pre)-1]) == datetime.datetime: #最後のレコードの挿入されてるデータ型が日付であれば。つまり、初回であれば
                    num_of_bw = 1

            elif type(score_pre[len(score_pre)-1]) == int:
                num_of_bw = score_pre[len(score_pre)-1] + 1 

                # database.l1_user_connect_with_bw(ip, new_score, text_pre, num_of_bw) #l1_userに-5%したスコアを挿入 🌟本番では使って
            print('少し落ち着きましょう')

        else:
            print('BBSに投稿しますた')
                
            database.l3_bbs_txt_insert(ip, text_pre)
                
else:
    print('BBS利用不可')

    calm_mind = program.anger_program()
    print(calm_mind)
                

