import re
import mglearn
import netifaces as ni
import psutil
import os
import socket
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.decomposition import LatentDirichletAllocation

import database



dp_list = pd.read_excel('depression_wrod_list.xlsx', index_col=0, header=0)
tester = pd.read_csv('/Users/takipon/Desktop/dprapp/tester.csv')



#新規データの重要な単語抜き出し
tester = list(tester) #csvを文章でlist化

vect = CountVectorizer(max_df=1, stop_words='english').fit(tester)
X_train = vect.transform(tester)

new_tester = vect.get_feature_names()
# print('TESTER features:\n{}'.format(new_tester)) #文字リスト ['alive', 'death', 'die', 'think', 'want', 'way']



#変数インスタンス + 小文字化 + append作業 + アルファベットリスト同士を結合 = for文１行
dp_list_low = [dp_list.vocabulary[num].lower() for num in range(len(dp_list))]

#１つのセルに連続してある特徴量(str)を分解
tif = TfidfVectorizer()
x = tif.fit_transform(dp_list_low)
dp_list_eachwords = tif.get_feature_names()

# print(dp_list_eachwords) #各単語から構成される一次元配列



#新規データ内にあるネガティブワードを、単語リストを参照しながらカウント
badwords=0
see_badwords = [badwords+dp_list_eachwords.count(new_tester[i]) for i in range(len(new_tester))]
# print(see_badwords) #リスト型、単語があれば１/なければ0 #[0, 1, 1, 0, 0, 0]



#新規テキストに対するネガティブワードの計算を小数点で実行
once_neg_percent = '{:.2}'.format(sum(see_badwords) / len(see_badwords))
# print(once_neg_percent) #0.33



#IPアドレス取得
def get_ip() -> list:
    if os.name == "nt":
        # Windows
        return socket.gethostbyname_ex(socket.gethostname())[2]
        pass
    else:
        # それ以外
        result = []
        address_list = psutil.net_if_addrs()
        for nic in address_list.keys():
            ni.ifaddresses(nic)
            try:
                ip = ni.ifaddresses(nic)[ni.AF_INET][0]['addr']
                if ip not in ["127.0.0.1"]:
                    result.append(ip)
            except KeyError as err:
                pass
        return result
ip = get_ip().pop()



#データベース.pyにIPアドレスとネガティブパーセンテージ受け渡し
# x = database.l1_connect(ip, once_neg_percent)



# データベース.pyでデータベースの中身を取得
l1_ip_df = pd.DataFrame(database.l1_show(ip))
l1_ip_df_col = list(l1_ip_df[2])

l1_ip_total=0
for i in range(len(l1_ip_df_col)):
    l1_ip_total = l1_ip_total + float(l1_ip_df_col[i])
print(l1_ip_total/3)


