import os
import sys
sys.path.append('../')

import re
import pandas as pd
import numpy as np

from app import database, l2_ai, l1_login

def endg_show():
    endg = 'what'
    task = 'what'

    # ip = l1_login.get_ip().pop()
    show = np.array(database.l2_endg_show())
    show = np.ravel(show)

    if len(show) > 0:
        endg = show[2]
        task = show[3]

    return endg, task

def endg_admittion():
    
    # ip = l1_login.get_ip().pop()
    personal_score = l2_ai.personal_score()
    # personal_score = 0.9

    if personal_score >= 0.75:
        result = 0
    else:
        result = 1
    return result

def endg(eg, task):
    #もし初めてなら文を作れ＋login
    # tester = pd.read_csv('/Users/takipon/Desktop/dprapp/tester_endg.csv')

    ##🌟本番では外すこと。
    # ip = l1_login.get_ip().pop()
    # personal_score = l2_ai.l2_ai.personal_score(ip) #0.144814814814815

    # if personal_score >= 0.50:

    #     if personal_score <= 0.75:
    #         database.l2_endg(ip, eg)

    #     elif personal_score >= 0.75:

    end_goal_tasks = task.split(',')
    eg_task = ''
    for txt in end_goal_tasks:
        eg_task = eg_task + txt + ','
            # end_goal_tasks = re.sub(r"'","''", end_goal_tasks) #クォーテーション対策。クォーテーションがある部分にもう１つ入れるとクォーテーションとして機能するらしい
    database.l2_endg(eg, eg_task)

