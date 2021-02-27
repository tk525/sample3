import os
import sys
sys.path.append('../')

import numpy as np
import pandas as pd

from app import database, l1_login, app



class user_info():
    #カウンセラーにユーザーの情報開示 #🌟本番ではDB関連の操作を起動する

    #ユーザーが投稿した全テキストとスコア
    def scotxt():
        ip = l1_login.get_ip().pop()
        user_score_and_text_pre = np.array(database.l1_user_show(ip))
        if len(user_score_and_text_pre) > 0:
            # score = []
            # txt = []
            # date = []
            # for sco_txt in user_score_and_text_pre:
            #     score.append(sco_txt[2])
            #     txt.append(sco_txt[3])
            #     date.append(sco_txt[4].strftime('%Y/%m/%d'))
            date_score = []
            txt = []
            for sco_txt in user_score_and_text_pre:
                date_score.append(
                    [sco_txt[4].strftime('%Y/%m/%d'), float(sco_txt[2])]
                )
                txt.append(sco_txt[3])
        return 'score', date_score, txt

    #ユーザーの性格特徴
    def personality():
        ip = l1_login.get_ip().pop()
        user_personality_pre = database.l2_personality_last_record(ip)
        if user_personality_pre is not None:
            user_personality_pre = user_personality_pre.pop()
            user_personality_pre = user_personality_pre[2].translate(str.maketrans({'[': '', ']': '', ' ': ''})) #101110001110101010010001101
            personality_name = np.array(pd.read_excel('./sample.xlsx', index_col=0, header=0, sheet_name='personality_x2').columns)

            user_personality = []
            for num in range(len(user_personality_pre)):
                if user_personality_pre[num] == '1':
                    user_personality.append(personality_name[num]) #['真面目Seriousness', 'サボれないCannot slack
            try:
                user_personality.index(0)
            except ValueError:
                user_personality = 'this user has exceptional personality.'

        return 'personality', user_personality

    #ユーザーが設定した目標
    def endg_task():
        ip = l1_login.get_ip().pop()
        user_endg_and_tasks_pre = database.l2_endg_show(ip)
        if user_endg_and_tasks_pre is not None:
            user_endg_and_tasks = user_endg_and_tasks_pre.pop()
        x = user_endg_and_tasks[2]+'\n'+user_endg_and_tasks[3]
        return 'endgtask', x

    #ユーザーがBBSに投稿したテキスト
    def bbs_txt():
        ip = l1_login.get_ip().pop()
        user_bbs_txt_pre = np.array(database.l3_bbs_txt_show_id(ip))
        if user_bbs_txt_pre is not None:
            user_bbs_txts = np.array(user_bbs_txt_pre)

            datas=''
            for bbs_txt in user_bbs_txts:
                # txt.append(bbs_txt[2])
                # date.append(bbs_txt[3].strftime('%Y/%m/%d'))
                datas = datas + bbs_txt[3].strftime('%Y/%m/%d')+' '+bbs_txt[2]+'\n'

        return 'bbsontxt', datas

    #ユーザーがBBSでいいねしたテキストのみ
    def bbs_act():
        ip = l1_login.get_ip().pop()
        user_bbs_act_pre = np.array(database.l3_bbs_act_show_id(ip))
        if user_bbs_act_pre is not None:
            user_bbs_act = ''
            for bbs_act in user_bbs_act_pre:
                bbs_act_id = bbs_act[2]
                bbs_act_pre = database.l3_bbs_txt_show_post_id(bbs_act_id)

                #アクションしたテキストのみ取得
                # user_bbs_act.append(bbs_act_pre.pop()[2]) 
                user_bbs_act = user_bbs_act + bbs_act_pre.pop()[2]+'\n'

        return 'bbsonact', user_bbs_act


def twmc(sign):

    ip = l1_login.get_ip().pop()

    mher = 2

    if mher >= 1: #カウンセラーの待機が1以上の場合

        if sign == "graph":
            text = user_info.scotxt()
        elif sign == "personality":
            text = user_info.personality()
        if sign == "endgtask":
            text = user_info.endg_task()
        if sign == "bbsontxt":
            text = user_info.bbs_txt()
        if sign == "bbsonact":
            text = user_info.bbs_act()

    else:
        text = 'sorry, can you retry in a fer minuts later?'

    return text

def roomname():

    ip = l1_login.get_ip().pop()
    
    results_pre = database.l3_create_user_show_all(ip)

    if len(results_pre) > 0:
        roomname = '/'+results_pre[5]
    else:
        roomname = '/'

    return roomname

def owner():

    try:
        roomname = '/'+pd.read_pickle("own_rm.csv")
    except EOFError:
        roomname  = '/'

    return roomname