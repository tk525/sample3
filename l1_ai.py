import re
import mglearn
import psutil
import os
import socket
import itertools
import pandas as pd
import numpy as np
import netifaces as ni
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier

import database
import l1_login



dp_list = pd.read_excel('depression_wrod_list.xlsx', index_col=0, header=0)
tester = pd.read_csv('/Users/takipon/Desktop/dprapp/tester.csv')
enco_list = pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', index_col=None, header=1, sheet_name='encouraging_list')



#新規データの重要な単語抜き出し
tester_list = list(tester) #csvを文章でlist化

vect = CountVectorizer(max_df=1, stop_words='english').fit(tester_list)
X_train = vect.transform(tester_list)

new_tester_words = vect.get_feature_names()
# print('TESTER features:\n{}'.format(new_tester_words
#)) #文字リスト ['alive', 'death', 'die', 'think', 'want', 'way']



#「理解・共感」辞書型ボキャの頻出度のキーと値を入れ替えて、頻出度の高い単語を使う
new_tester_words_voca = vect.vocabulary_
# print(new_tester_words_voca) #{'want': 4, 'die': 2, 'alive': 0, 'think': 3, 'way': 5, 'death': 1}

renew_tester_words_voca = {v: k for k, v in new_tester_words_voca.items()}
#辞書(new_tester_words_voca)のキーと値を入れ替え {4: 'want', 2: 'die', 0: 'alive', 3: 'think', 5: 'way', 1: 'death'}

print('「理解」I see your think of %s' % renew_tester_words_voca[0])



#「感想」新規データポイント(文字数)をsample.xlsx/encouraging_listデータポイント(X:文字数 Y:配列番号)をK近傍で適切なものを探す(精度がクソなので恐らく意味がない)、中身を確認し新規データポイントと近ければ反映する
tester_words_num = 1
for i in range(len(tester_list)):
    tester_words_num = tester_words_num + len(re.findall(" ", tester_list[i])) #新規データポイント(tester)の単語数カウント #17

enco_list_words_num = []
enco_list = list(enco_list.sentence)
for i in range(0, len(enco_list)):
    enco_list_words_num.append(len(re.findall(" ", enco_list[i]))+1) #１番目から、encoの各文の単語数カウント 
enco_list_words_num = np.array(enco_list_words_num)
# print(enco_list_words_num) #enco_listの文字数カウント #[ 5  4  3  2  2  4  3  3  5  4  2  5  4  5  3  4  5  3  2  4  4  9  3  1  13]

enco_list_array_num = []
for i in range(len(enco_list)):
    enco_list_array_num.append(i)
# print(enco_list_array_num) #enco_listの配列番号カウント #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

enco_list_words_num_4knn = enco_list_words_num.reshape(len(enco_list_words_num), 1) #Xに使うデータを二次元配列に変更
tester_words_num_4knn = np.array(tester_words_num).reshape(1, 1) #本番に使うデータを二次元配列に変更

knn = KNeighborsClassifier(n_neighbors=4,weights='distance') 
knn.fit(enco_list_words_num_4knn, enco_list_array_num)
# print(knn.score(enco_list_words_num_4knn, enco_list_array_num)) #knn精度確認 #0.28 データがなさすぎ?Yの範囲がデカすぎる?

enco_array_num_4knn = knn.kneighbors(tester_words_num_4knn) #新規データポイントをknnに入れて、近いものを引き抜く
enco_array_num_4knn = list(itertools.chain.from_iterable(knn.kneighbors(tester_words_num_4knn)[1])) #結果の２番目にあるarray(つまり、配列番号)を抜き出す、二次元を一次元に

enco_respond = []
num = 0
for i in range(len(enco_array_num_4knn)):
    num = enco_list_words_num[enco_array_num_4knn[i]]+num
    enco_respond.append(enco_list[enco_array_num_4knn[i]])
    if num >= tester_words_num-5:
        break
    else:
        enco_respond.append(enco_list[enco_array_num_4knn[i]])
        continue

print('「感想」 %s'%enco_respond) #新規データポイントの数に追いつくまで、enco_listの単語たちが入力されるようになる



#変数インスタンス + 小文字化 + append作業 + アルファベットリスト同士を結合 = for文１行
dp_list_low = [dp_list.vocabulary[num].lower() for num in range(len(dp_list))]

#１つのセルに連続してある特徴量(str)を分解
tif = TfidfVectorizer()
x = tif.fit_transform(dp_list_low)
dp_list_eachwords = tif.get_feature_names()

# print(dp_list_eachwords) #各単語から構成される一次元配列



#新規データ内にあるネガティブワードを、単語リストを参照しながらカウント
badwords=0
see_badwords = [badwords+dp_list_eachwords.count(new_tester_words[i]) for i in range(len(new_tester_words))]
# print(see_badwords) #リスト型、単語があれば１/なければ0 #[0, 1, 1, 0, 0, 0]



#新規テキストに対するネガティブワードの計算を小数点で実行
once_neg_percent = '{:.2}'.format(sum(see_badwords) / len(see_badwords))
# print(once_neg_percent) #0.33



ip = l1_login.get_ip().pop()
text = ''.join(tester_list)


#データベース.pyにIPアドレスとネガティブパーセンテージ＋テキスト受け渡し
x = database.l1_user_connect(ip, once_neg_percent, text)


# データベース.pyでデータベースの中身を取得
l1_ip_df = pd.DataFrame(database.l1_user_show(ip))
l1_ip_df_col = list(l1_ip_df[2])

l1_ip_total=0
for i in range(len(l1_ip_df_col)):
    l1_ip_total = l1_ip_total + float(l1_ip_df_col[i])
l1_ip_total = l1_ip_total/len(l1_ip_df_col)

if l1_ip_total >= 0.8:
    print('L2に進め')
else:
    print('L1残留')