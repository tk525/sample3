import random
import math
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN

import database, l1_login, l2_pd


recommend = pd.read_excel('./sample.xlsx', index_col=0, header=0, sheet_name='recommend')
recommend_concrete = pd.read_excel('./sample.xlsx', index_col=0, header=0, sheet_name='recommend_concrete')

    #最終スコアから性格の得点を合わせる
def personal_score(ip):
    
    ip = l1_login.get_ip().pop()
    score = np.ravel(database.l1_user_last_record(ip))[1] #ユーザーの最終スコア取得

    # personality_judge = database.l2_personality_last_record(ip).pop()[3] #0.185185185185185
    personality_judge = 0.185185185185185
    total_score_personality = float(score) + -personality_judge #0.144814814814815
    return total_score_personality

def l2_ai():

    #l2_personalityDBからrecord取得して、操作可能の二次元配列に変換
    ip = l1_login.get_ip().pop()
    score = np.ravel(database.l1_user_last_record(ip))[1] #ユーザーの最終スコア取得
    record_list = np.ravel(database.l2_personality_last_record(ip))[2] #l2パーソナリティの最終レコード取得
    record_replace = record_list.translate(str.maketrans({' ':'', '[':'', ']':''})) #大量置換
    record_intlist = [int(record_replace[i]) for i in range(len(record_replace))] #intの[1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1]
    record_2_deminsion = np.array(record_intlist).reshape(1,len(record_intlist)) #データの二次元配列化


    # #最終スコアから性格の得点を合わせる
    # def personal_score(ip):
    #     # personality_judge = database.l2_personality_last_record(ip).pop()[3] #0.185185185185185
    #     personality_judge = 0.185185185185185
    #     total_score_personality = float(score) + -personality_judge #0.144814814814815
    #     return total_score_personality


    recommend_name_list = np.array(recommend.index)
    recommend_features = [list(recommend.loc[i]) for i in recommend_name_list] #reccomendの中身



    #pca/dbscanでデータの関係性を学習し、それを基準に新規患者の性格から対処法を予測する
    pca = PCA(n_components=len(record_2_deminsion[0]))
    pca.fit_transform(recommend_features)
    recommend_pca = pca.fit_transform(recommend_features) #sample/recommend(性格別対処法の効果がある性格)を学習 [[-3.80887819e-01  1.11491213e+00 -6.09904078e-01 ...
    recommend_dbscan = DBSCAN().fit_predict(recommend_pca) #高密度領域にある点を同じグループにまとめる 



    recommend_key = [i for i, v in enumerate(recommend_dbscan) if v == min(recommend_dbscan)] #リスト内の最小値たちを全て取得 [89, 90, 91, 92, 93, 94, 95, 96, 97, 99]

    recommend_value = [recommend_name_list[i] for i in recommend_key] #対処法をリスト配列化



    #sample/recommend_concreteの解決策を参照し、文字で提案
    recommend_concrete_more = recommend_concrete.loc[:, '日本語']#'具体的な解決策'
    recommend_all_options = [recommend_concrete_more[i] for i in recommend_value] #['Be grateful.'....



    x = math.ceil(len(recommend_all_options) * personal_score(ip)) #3.62を切り上げ
    # recommend_random = random.choices(recommend_all_options, k=len(recommend_all_options)-x) #選択肢の中からランダムに１つ選択する 21選択/total25
    recommend_random = random.choices(recommend_all_options, k=math.ceil(42/(len(recommend_all_options)-x))) #あまりにも多いので、万物の回答42を割った

    # print(recommend_random)
    # ['できるだけ許すこと。', '嫌なことがあったら、SNSでつぶやきましょう。', '直感を利用する。', 'ポジティブな言葉を使いましょう。', '手をつなぐ。', '温かいコップを握る。', '自分を見下している人に注意を払うな。', '無視されても気にしないこと。', 'できるだけ許すこと。', '怒りを抱えている人を見ないようにする。', '一度に一つずつチェックしてみましょう。', '他人と自分を比べないこと。', 'ミラーニューロンを活用する。', '三人称で話せ', '批判的な意見に注意を払うな。', '自分の理想を高く持ちすぎないように。', 'SNSを使う場合は、1日30分までに制限しましょう。', '手をつなぐ。', 'SNSを使う場合は、1日30分までに制限しましょう。', '精神的に病んでしまうことは避けられないと考える。', '強く押しすぎないでください。']

    return recommend_random