import os
import sys
sys.path.append('../')

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from app import database, l1_login


def l2_show_more():
    ip = l1_login.get_ip().pop()
    dairys_pre = np.array(database.l2_dairy_show(ip))
    # dairys_date = np.ravel(dairys_date)
    dairys_text_pre = np.array(database.l2_dairy_show_text_encode(ip))
    dairys_text = np.ravel(dairys_text_pre)

    txt_date = []
    # print(dairys_pre[0])
    for num in range(len(dairys_pre)):
        date = str(dairys_pre[num][4]).split()[0]

        if not dairys_pre[num][5] is None: #Noneじゃないなら
            img = str(dairys_pre[num][5])
            txt_date.append([dairys_text[num], date, img])
        else:
            # img = ''
            txt_date.append([dairys_text[num], date])

    return txt_date

def l2_dairy(new_text, new_mood, img):
    # text = pd.read_csv('/Users/takipon/Desktop/dprapp/tester.csv')
    text = new_text

    # mind_pre = 3,4,3,4,3 #今までの評価
    ip = l1_login.get_ip().pop()
    datas_pre = database.l2_dairy_show(ip)

    mind_pre = []
    if datas_pre == []:
        mind_pre.append(0)
    else:
        for data in datas_pre:
            mind_pre.append([int(data[2])])

    mind_new = [[len(mind_pre)]] #次の値の予想



    #数値 過去の心の変化の傾向から、未来の心の変化を予測する
    # mind = np.array(mind_pre).reshape(-1,1) #二次元配列に変換
    mind = mind_pre #二次元配列に変換
    mind_num = [[index+1] for index, mind in enumerate(mind_pre)] #配列番号を二次元配列にして挿入


    lr = LinearRegression().fit(mind_num,mind) #配列リストX・紐付けした結果Yを基準に、新規Yを予測する
    mind_trend_new = lr.predict(mind_new) #[[3.4]]
    mind_trend_past = lr.predict([[len(mind_pre)]]) #[[3.4]]



    #数値 過去/未来の心の傾向から付けるコメントを判断する
    diary_comment = 'Awesome!' if mind_trend_new > mind_trend_past else 'Now is the time to take it easy and rest.'



    #日記 + 数値 挿入
    ip = l1_login.get_ip().pop()
    # mind = mind_trend_new[0][0]
    mind = new_mood

    # re_text = ''
    # for col in text.columns.values: #csvのcolumnsの値のみを取得。つまりcsvのテキストのみを取得し、付属の説明を無視する リスト内包をすると加工前と同じ状態になるので不可
    #     re_text = col + re_text
    re_text = new_text

    database.l2_dairy(ip, mind, re_text, img)

    return diary_comment