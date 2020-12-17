import re
import mglearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.decomposition import LatentDirichletAllocation

dp_list = pd.read_excel('depression_wrod_list.xlsx', index_col=0, header=0)
tester = pd.read_csv('/Users/takipon/Desktop/dprapp/tester.csv')



#新規データの重要な単語抜き出し
tester = list(tester) #csvを文章でlist化

vect = CountVectorizer(max_df=1, stop_words='english').fit(tester)
X_train = vect.transform(tester)

new_tester = vect.get_feature_names()
print('TESTER features:\n{}'.format(new_tester)) #文字リスト



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
print(see_badwords) #リスト型、単語があれば１/なければ0



#新規テキストに対するネガティブワードのパーセンテージ計算
once_neg_percent = '{:.0%}'.format(sum(see_badwords) / len(see_badwords))
print(once_neg_percent)