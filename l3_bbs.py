import pandas as pd
import numpy as np
import datetime

import database, l1_login



text_pre = 'damn it!'
text = text_pre.split()

bad_words_pre = list(pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', sheet_name='bad_word')['text'])


#ユーザーの最終スコア呼び出し
ip = l1_login.get_ip().pop()
score_pre = np.array(database.l1_user_last_record(ip))
score_pre = np.ravel(score_pre)
score = float(score_pre[1])


if score > 0.1: #🌟本番では0.8

    for text in text:
        if  text in bad_words_pre: #text内に悪い単語が含まれているか検索

            #悪い単語が含まれていた場合    
            new_score = score - (score / 20) #所持者の0.5%をスコアから引く

            if type(score_pre[len(score_pre)-1]) == datetime.datetime: #最後のレコードの挿入されてるデータ型が日付であれば。つまり、初回であれば
                num_of_bw = 1

            elif type(score_pre[len(score_pre)-1]) == int:
                num_of_bw = score_pre[len(score_pre)-1] + 1 

            # database.l1_user_connect_with_bw(ip, new_score, text_pre, num_of_bw) #l1_userに-5%したスコアを挿入 🌟本番では使って
            print('少し落ち着きましょう')

            if num_of_bw % 3 == 0: #🌟本番では0.5 3日停止＋アンガーマネージメントに誘導

                
                

else:
    print('bbs利用不可')


                

