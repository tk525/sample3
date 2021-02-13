import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import database, l1_login, main



class user_info():
    #カウンセラーにユーザーの情報開示 #🌟本番ではDB関連の操作を起動する

    #ユーザーが投稿した全テキストとスコア
    def scotxt():
        ip = l1_login.get_ip().pop()
        user_score_and_text_pre = np.array(database.l1_user_show(ip))
        if len(user_score_and_text_pre) > 0:
            score = []
            txt = []
            date = []
            for sco_txt in user_score_and_text_pre:
                score.append(sco_txt[2])
                txt.append(sco_txt[3])
                date.append(sco_txt[4].strftime('%Y/%m/%d'))
        return 'score', score, txt, date

    #ユーザーの性格特徴
    def personality():
        ip = l1_login.get_ip().pop()
        user_personality_pre = database.l2_personality_last_record(ip)
        if user_personality_pre is not None:
            user_personality_pre = user_personality_pre.pop()
            user_personality_pre = user_personality_pre[2].translate(str.maketrans({'[': '', ']': '', ' ': ''})) #101110001110101010010001101
            personality_name = np.array(pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', index_col=0, header=0, sheet_name='personality_x2').columns)

            user_personality = []
            for num in range(len(user_personality_pre)):
                if user_personality_pre[num] == '1':
                    user_personality.append(personality_name[num]) #['真面目Seriousness', 'サボれないCannot slack
        return 'personality', user_personality

    #ユーザーが設定した目標
    def endg_task():
        ip = l1_login.get_ip().pop()
        user_endg_and_tasks_pre = database.l2_endg_show(ip)
        if user_endg_and_tasks_pre is not None:
            user_endg_and_tasks = user_endg_and_tasks_pre.pop()
        return 'endgtask', user_endg_and_tasks[2],  user_endg_and_tasks[3]

    #ユーザーがBBSに投稿したテキスト
    def bbs_txt():
        ip = l1_login.get_ip().pop()
        user_bbs_txt_pre = np.array(database.l3_bbs_txt_show_id(ip))
        if user_bbs_txt_pre is not None:
            user_bbs_txts = np.array(user_bbs_txt_pre)
            txt=[]
            date=[]
            for bbs_txt in user_bbs_txts:
                txt.append(bbs_txt[2])
                date.append(bbs_txt[3].strftime('%Y/%m/%d'))

        return 'bbsontxt', txt, date

    #ユーザーがBBSでいいねしたテキストのみ
    def bbs_act():
        ip = l1_login.get_ip().pop()
        user_bbs_act_pre = np.array(database.l3_bbs_act_show_id(ip))
        if user_bbs_act_pre is not None:
            user_bbs_act = []
            for bbs_act in user_bbs_act_pre:
                bbs_act_id = bbs_act[2]
                bbs_act_pre = database.l3_bbs_txt_show_post_id(bbs_act_id)
                user_bbs_act.append(bbs_act_pre.pop()[2]) #アクションしたテキストのみ取得
        return 'bbsonact', user_bbs_act


def twmc(sign):

    ip = l1_login.get_ip().pop()
    memo_from_mc = 'she is fine.'

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
