import re
import itertools
import datetime
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

import database, l1_login


personality_features_pre = np.array(pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', index_col=0, header=0, sheet_name='personality_x2').columns)
personality_features = np.delete(np.delete(personality_features_pre, 28), 27)





#協調フィルタリング
ip = l1_login.get_ip().pop()
personality_pre = np.array(database.l2_personality_last_record(ip))
personality_num = np.ravel(personality_pre)[2] #[1 0 1 1 1 0 0 0 1 1 1 0 1 0 1 0 1 0 0 1 0 0 0 1 1 0 1]
personality_num = personality_num.translate(str.maketrans({' ':'', '[':'', ']':''})) #101110001110101010010001101

all_personality_record_pre= np.array(database.l2_personality_all_record())
all_personality_record = pd.DataFrame(all_personality_record_pre).iloc[:, 2] #0~79 [1 0 1 1 1 0 0 0 1 1 1 0 1 0 1 0 1 0 0 1 0 0 0...



#協調フィルタリング 同じ性格
similarity_rate=[]
for num in range(len(all_personality_record)):

    x_personality_num = all_personality_record[num].translate(str.maketrans({' ':'', '[':'', ']':''})) #101110001110101010010001101

    common_features = []
    for i in range(len(personality_features)):
        if personality_num[i] == x_personality_num[i]:
            common_features.append(personality_features[i]) #両者の共通する性格を探す

    if len(common_features) / len(personality_features) >= 0.7: #19/27=70%共鳴 #🌟本番では0.8に
        similarity_rate.append(num) #性格が似てる人たちの配列番号が入ってる



#協調フィルタリング 同じ目標
def word_cut(x):

    vect = CountVectorizer(stop_words='english').fit(x)
    vect.transform(x)
    words = vect.get_feature_names()
    return words


user_end_goal_pre = database.l2_endg_show(ip)
user_endg_task_pre = list(itertools.chain.from_iterable(user_end_goal_pre))[3].split(',') #[' build better relationships.', " work on goals you've given up on", 'Travel', '']
user_endg_task = word_cut(user_endg_task_pre) #['better', 'build', 'given', 'goals', 'relationships', 'travel', 've', 'work']


tips_list = []
end_goal_list = []
for num in similarity_rate:

    other_user_ip = all_personality_record_pre[num][1] #性格似てるユーザーのip獲得

    # other_users_end_goal_pre = database.l2_endg_show(other_user_ip)#🌟本番ではこっち
    # other_users_endg_pre = list(itertools.chain.from_iterable(other_users_end_goal_pre))[3].split(',') #🌟本番ではこっち#[' build better relationships.', " work on goals you've given up on", 'Travel', '']
    # other_user_endg_task = word_cut(other_users_endg_pre) #['better', 'build', 'given', 'goals', 'relationships', 'travel', 've', 'work'] #🌟本番ではこっち
    other_user_endg_task = ['better', 'build', 'BTS', 'sweden', 'relationships', 'programmer', 've', 'work','21'] 

    tips = []
    for x in user_endg_task:
        for i in other_user_endg_task:
            if x == i:
                tips.append(1)
            else:
                tips.append(0)
    tips_list.append(tips)

similarity_rate_endg = []
for num in range(len(tips_list)): #01セットたちの個数
    if sum(tips_list[num]) / len(user_endg_task) >= 0.6: #🌟本番では0.8
        similarity_rate_endg.append(similarity_rate[num]) #同じ目標を持ってる人たちの配列番号が入ってる





#LDA 
other_user_txt_bbs = []
other_user_act_bbs = []
for num in similarity_rate_endg:
    other_user_ip = all_personality_record_pre[num][1]
    other_user_dairy = np.array(database.l2_dairy_show(other_user_ip))

    mind = int(other_user_dairy[0][2]) #1つ目を取得

    for next_mind in other_user_dairy: #2つ目からしたいけど、余計なコードが増えるのでスルー
        if int(next_mind[2]) > mind: #🌟本番は>=ではなく>のみ
            x_day = (next_mind[4] - mind_datetime).days #数値上昇前日-数値上昇日。何日かのみ取得、時間切り捨て
            
            for day in range(x_day):
                # add_day = mind_datetime + datetime.timedelta(days=day) #数値上昇前日から１日ずつ追加 🌟本番ではこっち
                # add_day = add_day.strftime('%Y-%m-%d') #時刻を捨てる 🌟本番ではこっち
                add_day = '2021-01-07'

                #掲示板での発言回収
                other_user_txt_bbs_pre = np.array(database.l3_bbs_txt_show_date(add_day))
                if len(other_user_txt_bbs_pre) != 0: #掲示板での発言があったら
                    for num in other_user_txt_bbs_pre:
                        other_user_txt_bbs.append(num[2]) #掲示板での発言を回収

                #掲示板でのアクション回収 アクション→リアクションしたid→掲示板での発言id
                other_user_act_bbs_pre = np.array(database.l3_bbs_act_show_date(add_day))
                if len(other_user_act_bbs_pre) != 0: #掲示板での行動があったら
                    for num in other_user_act_bbs_pre:
                        bbs_txt_pre = np.array(database.l3_bbs_txt_show_id(num[2]))
                        bbs_txt = np.ravel(bbs_txt_pre)
                        other_user_act_bbs.append(bbs_txt[2]) #掲示板でのアクションを回収

        mind_datetime = next_mind[4]
        mind = int(next_mind[2])

    break #🌟本番ではこれを解除 大量に似てる人がいるので演算が長くなりうざい

act_bbs = word_cut(other_user_act_bbs)
txt_bbs = word_cut(other_user_txt_bbs)





#LSTM(RNN)
