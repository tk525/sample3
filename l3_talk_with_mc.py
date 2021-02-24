# import pandas as pd
# import numpy as np
# from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt
# import matplotlib
# from kivy.app import App
# from kivy.uix.screenmanager import Screen
# from kivy.lang import Builder
# from kivy.uix.image import Image
# from kivy.graphics.texture import Texture
# from kivy.clock import Clock
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.behaviors import ButtonBehavior
# from kivy.properties import ObjectProperty, StringProperty
# from kivy.uix.label import Label
# from kivy.uix.widget import Widget
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout as nnnn
# from kivy.config import Config
# from kivy.graphics import *
# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
# from kivy.core.text import Label as CoreLabel
# from kivy.uix.accordion import Accordion, AccordionItem
# from kivy.uix.scrollview import *
# from kivy.uix.gridlayout import GridLayout

# import cv2
# import math
# import time
# import concurrent.futures
# import japanize_kivy

# import os
# import random
# from geventwebsocket.handler import WebSocketHandler
# from gevent import pywsgi, sleep

# import database, l1_login, main


# Builder.load_file("main.kv")


# ws_list = set()



# class user_info():
#     #カウンセラーにユーザーの情報開示 #🌟本番ではDB関連の操作を起動する

#     #ユーザーが投稿した全テキストとスコア
#     def scotxt():
#         ip = l1_login.get_ip().pop()
#         user_score_and_text_pre = np.array(database.l1_user_show(ip))
#         if len(user_score_and_text_pre) > 0:
#             score = []
#             txt = []
#             date = []
#             for sco_txt in user_score_and_text_pre:
#                 score.append(sco_txt[2])
#                 txt.append(sco_txt[3])
#                 date.append(sco_txt[4].strftime('%Y/%m/%d'))
#         return score, txt, date

#     #ユーザーの性格特徴
#     def personality():
#         ip = l1_login.get_ip().pop()
#         user_personality_pre = database.l2_personality_last_record(ip)
#         if user_personality_pre is not None:
#             user_personality_pre = user_personality_pre.pop()
#             user_personality_pre = user_personality_pre[2].translate(str.maketrans({'[': '', ']': '', ' ': ''})) #101110001110101010010001101
#             personality_name = np.array(pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', index_col=0, header=0, sheet_name='personality_x2').columns)

#             user_personality = []
#             for num in range(len(user_personality_pre)):
#                 if user_personality_pre[num] == '1':
#                     user_personality.append(personality_name[num]) #['真面目Seriousness', 'サボれないCannot slack
#         return user_personality

#     #ユーザーが設定した目標
#     def endg_task():
#         ip = l1_login.get_ip().pop()
#         user_endg_and_tasks_pre = database.l2_endg_show(ip)
#         if user_endg_and_tasks_pre is not None:
#             user_endg_and_tasks = user_endg_and_tasks_pre.pop()
#         return user_endg_and_tasks

#     #ユーザーがBBSに投稿したテキスト
#     def bbs_txt():
#         ip = l1_login.get_ip().pop()
#         user_bbs_txt_pre = np.array(database.l3_bbs_txt_show_id(ip))
#         if user_bbs_txt_pre is not None:
#             user_bbs_txt = user_bbs_txt_pre
#         return user_bbs_txt

#     #ユーザーがBBSでいいねしたテキストのみ
#     def bbs_act():
#         ip = l1_login.get_ip().pop()
#         user_bbs_act_pre = np.array(database.l3_bbs_act_show_id(ip))
#         if user_bbs_act_pre is not None:
#             user_bbs_act = []
#             for bbs_act in user_bbs_act_pre:
#                 bbs_act_id = bbs_act[2]
#                 bbs_act_pre = database.l3_bbs_txt_show_post_id(bbs_act_id)
#                 user_bbs_act.append(bbs_act_pre.pop()[2]) #アクションしたテキストのみ取得
#         return user_bbs_act



# #チャット
# class SMS_user(Screen, BoxLayout, object):

#     Config.set('graphics', 'fullscreen', 0)
#     # Config.set('graphics', 'width', 320)
#     # Config.set('graphics', 'height', 568)
#     # Config.set('graphics', 'resizable', 0)
    
#     def send_txt(self): #できればkivyでwebsocket使いたかった
#         self.ids.rv.data.append({'text': self.ids.txt.text, 'halign': 'left'})
#         self.ids.txt.text = ''

#         #受け取った値を.jsで処理して戻す？



#     def on_label(self, **kwargs):
#         self.ids.gogo.clear_widgets() #初期化

#         self.ids.score.size_hint_y = 1
#         self.ids.personality.size_hint_y = 1
#         self.ids.kkk.size_hint_y = 0.05

#     def score(self, *args, **kwargs):
#         score, txt, date = user_info.scotxt()
        
#         self.ids.kkk.size_hint_y = 1
#         plt.clf()
#         bar_plt=plt.bar(date, score)
#         self.ids.gogo.clear_widgets() #初期化
#         self.ids.gogo.add_widget(FigureCanvasKivyAgg(plt.gcf())) #グラフ描画

#     def personality(self, **kwargs):
#         self.ids.kkk.size_hint_y = 1

#         personarity = user_info.personality()
#         per = np.array(personarity).reshape(round(len(personarity)/2),2)

#         self.ids.gogo.clear_widgets() #初期化
#         for p in per:
#             self.ids.gogo.add_widget(Label( text='{}, {}\n'.format(p[0],p[1] ) )) #描画

#     def endg_task(self, **kwargs):
#         endg_task = user_info.endg_task()
#         end = ['end goal is '+endg_task[2], 'task is '+endg_task[3]]

#         self.ids.kkk.size_hint_y = 1
#         self.ids.gogo.clear_widgets() #初期化
#         for i in range(len(end)):
#             self.ids.gogo.add_widget(Label( text='{}\n'.format(end[i]) ))

#     def bbs_txt(self, **kwargs):

#         bbs_txt = user_info.bbs_txt()
#         txt=[]
#         for i in range(len(bbs_txt)):
#             txt.append([ bbs_txt[i][3].strftime('%Y/%m/%d'), bbs_txt[i][2] ])
        
#         self.ids.kkk.size_hint_y = 1
#         self.ids.gogo.clear_widgets() #初期化

#         #ここでスクロールばー
#         self.ids.gogo.row_default_height = 200
#         self.ids.gogo.size_hint_y = 0.9
#         self.ids.gogo.height = self.ids.gogo.minimum_height

#         for i in range(len(txt)):
#             self.ids.gogo.add_widget(Label( text='{} : {}\n'.format(txt[i][0], txt[i][1]) ))

#     def bbs_act(self, **kwargs):

#         bbs_act = user_info.bbs_act()

#         self.ids.kkk.size_hint_y = 1
#         self.ids.gogo.clear_widgets() #初期化

#         #ここでスクロールばー
#         self.ids.gogo.row_default_height = 200
#         self.ids.gogo.size_hint_y = 0.9
#         self.ids.gogo.height = self.ids.gogo.minimum_height   

#         for i in range(len(bbs_act)):
#             self.ids.gogo.add_widget(Label( text='{}\n'.format(bbs_act[i] )))


# class Chat_user(App):
#     def build(self):
#         return SMS_user()



# #ビデオチャット
# class VChat(Widget):

#     def camera(self):

#         time = 1            # 計測時間[s]
#         samplerate = 44100  # サンプリングレート
#         fs = 512 * 2           # フレームサイズ
#         index = 0           # マイクのチャンネル指標

#         pa = pyaudio.PyAudio()
#         data = []
#         dt = 1 / samplerate


#         # 0番目のカメラに接続
#         self.capture = cv2.VideoCapture(0)

#         # ストリームの開始
#         stream = pa.open(format=pyaudio.paInt16, channels=1, rate=samplerate,
#                         input=True, input_device_index=index, frames_per_buffer=fs)

#         # 描画のインターバルを設定
#         while(True):
    
#             # フレームサイズ毎に音声を録音していくループ
#             for i in range(int(((time / dt) / fs))):
#                 frame = stream.read(fs)
#                 data.append(frame)


#             ret, frame = self.capture.read()

#             x = math.floor(frame.shape[0]/5)
#             y = math.floor(frame.shape[1]/5)

#             cam = cv2.rectangle(frame,
#                 (20, 20), #左上から何px目か
#                 (y, x), #横,縦
#                 (255, 0, 0), #(255, 0, 0) カラーコード
#                 ) #塗りつぶし
#             # cam = np.hstack((frame, test_img))

#             cv2.imshow('VChat',cam)

#             # ここからグラフ描画
#             voice_pre = np.arange(0, fs * (i+1) * (1 / samplerate), 1 / samplerate)
#             print(voice_pre) #とりあえず


#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break


#         self.capture.release()
#         cv2.destroyAllWindows()

#         # ストリームの終了
#         stream.stop_stream()
#         stream.close()
#         pa.terminate()
    

# class VChatApp(App):
#     def __init__(self, **kwargs):
#         super(VChatApp, self).__init__(**kwargs)
#         self.title = 'VCさんぷるう'

#     def build(self):
#         return VChat()



# #TEL
# class Tel(Widget):

#     def tel_record(self):

#         time = 1            # 計測時間[s]
#         samplerate = 44100  # サンプリングレート
#         fs = 1024           # フレームサイズ
#         index = 0           # マイクのチャンネル指標

#         wfm, i = CameraPreview.record(time, samplerate, fs, index)
#         voice_pre = np.arange(0, fs * (i+1) * (1 / samplerate), 1 / samplerate)

#         print(voice_pre)
#         # plt.rcParams['font.size'] = 14
#         # plt.rcParams['font.family'] = 'Times New Roman'
        
#         # # 目盛を内側にする。
#         # plt.rcParams['xtick.direction'] = 'in'
#         # plt.rcParams['ytick.direction'] = 'in'
            
#         # # グラフの上下左右に目盛線を付ける。
#         # fig = plt.figure()
#         # ax1 = fig.add_subplot(111)
#         # ax1.yaxis.set_ticks_position('both')
#         # ax1.xaxis.set_ticks_position('both')
            
#         # # 軸のラベルを設定する。
#         # ax1.set_xlabel('Time [s]')
#         # ax1.set_ylabel('Sound pressure [Pa]')
            
#         # # データプロットの準備とともに、ラベルと線の太さ、凡例の設置を行う。
#         # ax1.plot(t, wfm, label='signal', lw=1)
            
#         # fig.tight_layout()
            
#         # # グラフを表示する。
#         # plt.show()
#         # plt.close()


# class TelApp(App):
#     def __init__(self, **kwargs):
#         super(TelApp, self).__init__(**kwargs)
#         self.title = 'Tさんぷるう'

#     def build(self):
#         return Tel()






# def okurairi():
#     #0:チャット 1:ビデオ電話 2:電話のみ
#     order = 0

#     ip = l1_login.get_ip().pop()
#     memo_from_mc = 'she is fine.'

#     mher = 2

#     if mher >= 1: #カウンセラーの待機が1以上の場合


#         if order == 0: #チャット
#             print('チャット')
#             Chat_user().run() #これをこのまま起動すればkivyで描画されたものが表示される
#             # executor.map(plt.show())
#             #     Chat_mher().run()

#         # if order == 1: #ビデオチャット
#         #     print('ビデオチャット')
#         #         # CameraPreview()
#         #     VChatApp().run()

#         # if order == 2: #TEL
#         #     print('TEL')
#         #     TelApp().run()

#         # database.l3_mc_insert(ip, memo_from_mc)    
            

#     else:
#         text = 'sorry, can you retry in a fer minuts later?'
#         # return text

# def twmc():

#     ip = l1_login.get_ip().pop()
#     memo_from_mc = 'she is fine.'

#     mher = 2

#     if mher >= 1: #カウンセラーの待機が1以上の場合

#         score, txt, date = user_info.scotxt()
#         plt.clf()
#         text=plt.bar(date, score)

#     else:
#         text = 'sorry, can you retry in a fer minuts later?'

#     return text