# import re
# import os 
# import time
# import itertools
# import datetime
# import random
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from keras.models import Sequential
# from keras.layers import Dense, LSTM

# import database, l1_login


# personality_features_pre = np.array(pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', index_col=0, header=0, sheet_name='personality_x2').columns)
# personality_features = np.delete(np.delete(personality_features_pre, 28), 27)





# #LSTM(RNN)
# class LSTM_RNN:

#     def make_sentense(act_txt_bbs):

#         #テキストデータの前処理
#         os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
#         start = time.time()

#         text_pre = pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', index_col=None, header=0, sheet_name='sugesstion_list')
#         all_text = text_pre['text']
#         all_text = random.choice(all_text)

#         text = all_text + ' ' + act_txt_bbs + ' . '
#         print("文字数",text)



#         #LSTM設定をする
#         n_rnn = 10 #時系列の数
#         batch_size = 128 
#         epochs = 200 #多いと精度が上がるが、ラグいので20で
#         n_mid = 256 #中間層のニューロン数



#         #文字のベクトル化
#         # インデックスと文字で辞書を作成
#         chars = sorted(list(set(text)))  # setで文字の重複をなくし、各文字をリストに格納する
#         print("文字数（重複無し）", len(chars))
#         char_indices = {}  # 文字がキーでインデックスが値
#         for i, char in enumerate(chars):
#             char_indices[char] = i
#         indices_char = {}  # インデックスがキーで文字が値
#         for i, char in enumerate(chars):
#             indices_char[i] = char
        
#         # 時系列データと、それから予測すべき文字を取り出す
#         time_chars = []
#         next_chars = []
#         for i in range(0, len(text) - n_rnn):
#             time_chars.append(text[i: i + n_rnn])
#             next_chars.append(text[i + n_rnn])
        
#         # 入力と正解をone-hot表現で表す。１文字毎に0,1のベクトルをフルイメージです。
#         x = np.zeros((len(time_chars), n_rnn, len(chars)), dtype=np.bool)
#         t = np.zeros((len(time_chars), len(chars)), dtype=np.bool)
#         for i, t_cs in enumerate(time_chars):
#             t[i, char_indices[next_chars[i]]] = 1  # 正解をone-hot表現で表す
#             for j, char in enumerate(t_cs):
#                 x[i, j, char_indices[char]] = 1  # 入力をone-hot表現で表す

#         print("xの形状", x.shape)
#         print("tの形状", t.shape)



#         #LSTMモデルの構築
#         model_lstm = Sequential()
#         model_lstm.add(LSTM(n_mid, input_shape=(n_rnn, len(chars))))
#         model_lstm.add(Dense(len(chars), activation="softmax"))
#         model_lstm.compile(loss='categorical_crossentropy', optimizer="adam")
#         print(model_lstm.summary())



#         #文章生成用の関数
#         from keras.callbacks import LambdaCallback
        
#         def on_epoch_end(epoch, logs):
#             print("エポック: ", epoch)

#             elapsed_time = time.time() - start
#             print ("on_epoch_end  elapsed_time:{0}".format(elapsed_time) + "[sec]")
            
#             beta = 4  # 確率分布を調整する定数
#             prev_text = text[0:n_rnn]  # 入力に使う文字
#             created_text = prev_text  # 生成されるテキスト
            
#             print("シード: ", created_text)

#             for i in range(100):
#                 # 入力をone-hot表現に
#                 x_pred = np.zeros((1, n_rnn, len(chars)))
#                 for j, char in enumerate(prev_text):
#                     x_pred[0, j, char_indices[char]] = 1
                
#                 # 予測を行い、次の文字を得る
#                 # yの形状は、1列 1049行(文字数=出力層の数)になっている
#                 y = model.predict(x_pred)
#                 #print(y.shape )
#                 p_power = y[0] ** beta  # 確率分布の調整(1049個の配列の中から、確率が高い文字を取得しようとしている　)
#                 next_index = np.random.choice(len(p_power), p=p_power/np.sum(p_power))        
#                 next_char = indices_char[next_index]

#                 created_text += next_char
#                 prev_text = prev_text[1:] + next_char

#             print(created_text)
#             print()
            


#         # エポック終了後に実行される関数を設定
#         epock_end_callback= LambdaCallback(on_epoch_end=on_epoch_end)



#         #学習
#         model = model_lstm

#         elapsed_time = time.time() - start
#         print ("学習開始 elapsed_time:{0}".format(elapsed_time) + "[sec]")
#         history_lstm = model_lstm.fit(x, t,
#                             batch_size=batch_size,
#                             epochs=epochs,
#                             callbacks=[epock_end_callback])





#         # def get_antifical_text(lstm_predict):
#         def get_antifical_text():
    
#             beta = 4  # 確率分布を調整する定数
#             prev_text = text[0:n_rnn]  # 入力に使う文字
#             created_text = prev_text  # 生成されるテキスト

#             for i in range(100):
#                 x_pred = np.zeros((1, n_rnn, len(chars)))
#                 for j, char in enumerate(prev_text):
#                     x_pred[0, j, char_indices[char]] = 1
                    
#                 y = model.predict(x_pred)
#                 p_power = y[0] ** beta  # 確率分布の調整(1049個の配列の中から、確率が高い文字を取得しようとしている　)
#                 next_index = np.random.choice(len(p_power), p=p_power/np.sum(p_power))        
#                 next_char = indices_char[next_index]

#                 created_text += next_char
#                 prev_text = prev_text[1:] + next_char

#             return created_text


#         # lstm_predict = model_lstm.predict(x, batch_size=batch_size)
#         # antifical_txt_pre = get_antifical_text(lstm_predict)
#         antifical_txt_pre = get_antifical_text()
#         # print('AI文章',antifical_txt_pre)
#         antifical_txt = antifical_txt_pre.split()
#         # print(antifical_txt_pre)

#         ai_txt_num = antifical_txt.index('.')

#         #カンマがあるところまで作った文章を単語を入れていく
#         ai_txt = ''
#         for num in range(ai_txt_num):
#             ai_txt = ai_txt + ' ' + antifical_txt[num]

#         return ai_txt





# #協調フィルタリング 同じ目標
# def word_cut(x):

#     vect = CountVectorizer(stop_words='english').fit(x)
#     vect.transform(x)
#     words = vect.get_feature_names()
#     return words






# def suggest():
#     #協調フィルタリング
#     ip = l1_login.get_ip().pop()
#     personality_pre = np.array(database.l2_personality_last_record(ip))
#     personality_num = np.ravel(personality_pre)[2] #[1 0 1 1 1 0 0 0 1 1 1 0 1 0 1 0 1 0 0 1 0 0 0 1 1 0 1]
#     personality_num = personality_num.translate(str.maketrans({' ':'', '[':'', ']':''})) #101110001110101010010001101
#     print('1', personality_num)

#     all_personality_record_pre= np.array(database.l2_personality_all_record())
#     all_personality_record = pd.DataFrame(all_personality_record_pre).iloc[:, 2] #0~79 [1 0 1 1 1 0 0 0 1 1 1 0 1 0 1 0 1 0 0 1 0 0 0...
#     print('2', all_personality_record)



#     #協調フィルタリング 同じ性格
#     similarity_rate=[]
#     for num in range(len(all_personality_record)):

#         x_personality_num = all_personality_record[num].translate(str.maketrans({' ':'', '[':'', ']':''})) #101110001110101010010001101

#         common_features = []
#         for i in range(len(personality_features)):
#             if personality_num[i] == x_personality_num[i]:
#                 common_features.append(personality_features[i]) #両者の共通する性格を探す

#         if len(common_features) / len(personality_features) >= 0.7: #19/27=70%共鳴 #🌟本番では0.8に
#             similarity_rate.append(num) #性格が似てる人たちの配列番号が入ってる
#     print('3', similarity_rate)



#     user_end_goal_pre = database.l2_endg_show(ip)
#     user_endg_task_pre = list(itertools.chain.from_iterable(user_end_goal_pre))[3].split(',') #[' build better relationships.', " work on goals you've given up on", 'Travel', '']
#     user_endg_task = word_cut(user_endg_task_pre) #['better', 'build', 'given', 'goals', 'relationships', 'travel', 've', 'work']
#     print('4', user_endg_task)



#     tips_list = []
#     end_goal_list = []
#     for num in similarity_rate:

#         other_user_ip = all_personality_record_pre[num][1] #性格似てるユーザーのip獲得

#         other_users_end_goal_pre = database.l2_endg_show(other_user_ip)#🌟本番ではこっち
#         other_users_endg_pre = list(itertools.chain.from_iterable(other_users_end_goal_pre))[3].split(',') #🌟本番ではこっち#[' build better relationships.', " work on goals you've given up on", 'Travel', '']
#         other_user_endg_task = word_cut(other_users_endg_pre) #['better', 'build', 'given', 'goals', 'relationships', 'travel', 've', 'work'] #🌟本番ではこっち
#         # other_user_endg_task = ['better', 'build', 'BTS', 'sweden', 'relationships', 'programmer', 've', 'work','21'] 
#         print('5', other_user_endg_task)


#         tips = []
#         for x in user_endg_task:
#             for i in other_user_endg_task:
#                 if x == i:
#                     tips.append(1)
#                 else:
#                     tips.append(0)
#         tips_list.append(tips)

#     similarity_rate_endg = []
#     for num in range(len(tips_list)): #01セットたちの個数
#         if sum(tips_list[num]) / len(user_endg_task) >= 0.6: #🌟本番では0.8
#             similarity_rate_endg.append(similarity_rate[num]) #同じ目標を持ってる人たちの配列番号が入ってる
#     print('6', similarity_rate_endg)




#     #LDA 
#     other_user_txt_bbs = []
#     other_user_act_bbs = []
#     for num in similarity_rate_endg:
#         other_user_ip = all_personality_record_pre[num][1]
#         other_user_dairy = np.array(database.l2_dairy_show(other_user_ip))

#         mind = int(other_user_dairy[0][2]) #1つ目を取得
#         print('7-1', other_user_dairy)
#         print('7-2', mind)

#         for next_mind in other_user_dairy: #2つ目からしたいけど、余計なコードが増えるのでスルー
#             if int(next_mind[2]) > mind: #🌟本番は>=ではなく>のみ

#                 x_day = (next_mind[4] - mind_datetime).days #数値上昇前日-数値上昇日。何日かのみ取得、時間切り捨て 
#                 print('7-3', x_day)
#                 print('7-4', next_mind[4])
#                 print('7-5', mind_datetime)

#                 for day in range(-x_day):
#                     add_day = mind_datetime + datetime.timedelta(days = -day) #数値上昇前日から１日ずつ追加 🌟本番ではこっち
#                     add_day = add_day.strftime('%Y-%m-%d') #時刻を捨てる 🌟本番ではこっち
#                     # add_day = '2021-01-07'
#                     print('7-6', add_day)

#                     #掲示板での発言回収
#                     other_user_txt_bbs_pre = np.array(database.l3_bbs_txt_show_date(add_day))
#                     print('8', other_user_txt_bbs_pre)
#                     if len(other_user_txt_bbs_pre) != 0: #掲示板での発言があったら
#                         for num in other_user_txt_bbs_pre:
#                             other_user_txt_bbs.append(num[2]) #掲示板での発言を回収

#                     #掲示板でのアクション回収 アクション→リアクションしたid→掲示板での発言id
#                     other_user_act_bbs_pre = np.array(database.l3_bbs_act_show_date(add_day))
#                     print('9', other_user_act_bbs_pre)

#                     if len(other_user_act_bbs_pre) > 0: #掲示板での行動があったら
#                         print('9-1', other_user_act_bbs_pre)
#                         for num in other_user_act_bbs_pre:
#                             print('9-2', num)
#                             bbs_txt_pre = np.array(database.l3_bbs_txt_show_id(num[2]))
#                             print('9-3', bbs_txt_pre)
#                             bbs_txt = np.ravel(bbs_txt_pre)
#                             try:
#                                 other_user_act_bbs.append(bbs_txt[2]) #掲示板でのアクションを回収
#                             except IndexError:
#                                 pass
#                             print('10', other_user_act_bbs)

#             mind_datetime = next_mind[4]
#             mind = int(next_mind[2])

#         break #🌟本番ではこれを解除 大量に似てる人がいるので演算が長くなるので
    
#     if other_user_act_bbs == []:
#         ai_txt = 'sorry, we can not any suggestion'
#     else:
#         act_bbs = word_cut(other_user_act_bbs)
#         txt_bbs = word_cut(other_user_txt_bbs)
#         act_txt_bbs_pre = act_bbs + txt_bbs

#         act_txt_bbs = ''
#         for bbs in act_txt_bbs_pre:
#             act_txt_bbs = bbs +' '+ act_txt_bbs #today making great fuck day app today making great day app


#         ai_txt = LSTM_RNN.make_sentense(act_txt_bbs)
#         # print(ai_txt)

#     return ai_txt