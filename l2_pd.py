import math
import itertools
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

import database, l1_login, main



def personality_judge(tester_x):

    personality = pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', index_col=0, header=0, sheet_name='personality_x2')


    personality_except_dep = personality.drop(['鬱度', '鬱度判定'], axis=1)
    patient_name_list = np.array(personality.index)
    petinet_dpr = personality.loc[:, '鬱度']

    patient_value = [list(personality_except_dep.loc['%s'%key]) for key in patient_name_list] #値のみを抜き出して、二次元 X_train兼X_test
    dep_per = list(personality['鬱度判定']) #鬱度のみを抜き出し、一次元 y_train兼y_test



    # knn = KNeighborsClassifier(n_neighbors=math.floor(len(personality_except_dep-1)/len(np.bincount(dep_per)))) #28/3=9.33→9
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(patient_value, dep_per)

    # tester_x = [[1,0,1,1,1,0,0,0,1,1,1,0,1,0,1,0,1,0,0,1,0,0,0,1,1,0,1]] #14
    # tester_y = [1] #0.51
    # print(knn.score(tester_x, tester_y)) #1.0だよ...


    presonality_result_patient_names = [patient_name_list[value] for value in list(itertools.chain.from_iterable(knn.kneighbors(tester_x)[1]))] #結果の２番目にあるarray(つまり、配列番号)を抜き出す、二次元を一次元に。そして患者リストの名前を参照する ['O', 'K', 'Q', 'M', 'E', 'N', 'J', 'D', 'F']

    personality_result = [petinet_dpr[i] for i in presonality_result_patient_names] #各患者名の鬱度カテを引用し、そのまま変換 [0.555555555555556, 0.407407407407407...
    personality_result = float(personality_result[0]) #小数点の文字列をfloatで変換

    return personality_result



def personality_to_db(tester_x, personality_judge):

    ip = l1_login.get_ip().pop()

    #DBのSQL攻撃対策の弊害の対策
    tester_x = str(tester_x)
    
    database.l2_personality(ip, tester_x, personality_judge)

def l2_dignosis(survey):

    # tester_x = [[1,0,1,1,1,0,0,0,1,1,1,0,1,0,1,0,1,0,0,1,0,0,0,1,1,0,1]] #14
    tester_x = survey

    #挿入コマンド
    p_judge = personality_judge(tester_x)

    tester_x = np.ravel(tester_x)
    personality_to_db(tester_x, p_judge)

    return p_judge