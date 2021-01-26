import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import cv2
import math

import pyaudio
import wave
import time
import sys

import database, l1_login



Builder.load_file("main.kv")



#チャット
class SMS_user(Screen):
    def send_txt(self):
        self.ids.rv.data.append({'text': self.ids.txt.text, 'halign': 'left'})
        self.ids.txt.text = ''

# class SMS_mher(Screen):
#     def receive_txt(self):
#         self.ids.rv.data.append({'text': self.ids.txt.text, 'halign': 'right', })
#         self.ids.txt.text = ''

class Chat_user(App):
    def build(self):
        return SMS_user()
# class Chat_mher(App):
#     def build(self):
#         return SMS_mher()



#ビデオチャット
class VChat(Widget):

    def camera(self):

        time = 1            # 計測時間[s]
        samplerate = 44100  # サンプリングレート
        fs = 512 * 2           # フレームサイズ
        index = 0           # マイクのチャンネル指標

        pa = pyaudio.PyAudio()
        data = []
        dt = 1 / samplerate


        # 0番目のカメラに接続
        self.capture = cv2.VideoCapture(0)

        # ストリームの開始
        stream = pa.open(format=pyaudio.paInt16, channels=1, rate=samplerate,
                        input=True, input_device_index=index, frames_per_buffer=fs)

        # 描画のインターバルを設定
        while(True):
    
            # フレームサイズ毎に音声を録音していくループ
            for i in range(int(((time / dt) / fs))):
                frame = stream.read(fs)
                data.append(frame)


            ret, frame = self.capture.read()

            x = math.floor(frame.shape[0]/5)
            y = math.floor(frame.shape[1]/5)

            cam = cv2.rectangle(frame,
                (20, 20), #左上から何px目か
                (y, x), #横,縦
                (255, 0, 0), #(255, 0, 0) カラーコード
                ) #塗りつぶし
            # cam = np.hstack((frame, test_img))

            cv2.imshow('VChat',cam)

            # ここからグラフ描画
            voice_pre = np.arange(0, fs * (i+1) * (1 / samplerate), 1 / samplerate)
            print(voice_pre) #とりあえず


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        self.capture.release()
        cv2.destroyAllWindows()

        # ストリームの終了
        stream.stop_stream()
        stream.close()
        pa.terminate()
    

class VChatApp(App):
    def __init__(self, **kwargs):
        super(VChatApp, self).__init__(**kwargs)
        self.title = 'VCさんぷるう'

    def build(self):
        return VChat()



#TEL
class Tel(Widget):

    def tel_record(self):

        time = 1            # 計測時間[s]
        samplerate = 44100  # サンプリングレート
        fs = 1024           # フレームサイズ
        index = 0           # マイクのチャンネル指標

        wfm, i = CameraPreview.record(time, samplerate, fs, index)
        voice_pre = np.arange(0, fs * (i+1) * (1 / samplerate), 1 / samplerate)

        print(voice_pre)
        # plt.rcParams['font.size'] = 14
        # plt.rcParams['font.family'] = 'Times New Roman'
        
        # # 目盛を内側にする。
        # plt.rcParams['xtick.direction'] = 'in'
        # plt.rcParams['ytick.direction'] = 'in'
            
        # # グラフの上下左右に目盛線を付ける。
        # fig = plt.figure()
        # ax1 = fig.add_subplot(111)
        # ax1.yaxis.set_ticks_position('both')
        # ax1.xaxis.set_ticks_position('both')
            
        # # 軸のラベルを設定する。
        # ax1.set_xlabel('Time [s]')
        # ax1.set_ylabel('Sound pressure [Pa]')
            
        # # データプロットの準備とともに、ラベルと線の太さ、凡例の設置を行う。
        # ax1.plot(t, wfm, label='signal', lw=1)
            
        # fig.tight_layout()
            
        # # グラフを表示する。
        # plt.show()
        # plt.close()


class TelApp(App):
    def __init__(self, **kwargs):
        super(TelApp, self).__init__(**kwargs)
        self.title = 'Tさんぷるう'

    def build(self):
        return Tel()







#0:チャット 1:ビデオ電話 2:電話のみ
order = 0

ip = l1_login.get_ip().pop()
memo_from_mc = 'she is fine.'

mher = 2

if mher >= 1: #カウンセラーの待機が1以上の場合


    # #カウンセラーにユーザーの情報開示 #🌟本番ではDB関連の操作を起動する
    # ip = l1_login.get_ip().pop()


    # #ユーザーが投稿した全テキストとスコア
    # user_score_and_text_pre = database.l1_user_show(ip)
    # if user_score_and_text_pre is not None:
    #     user_score_and_text = user_score_and_text_pre.pop()


    # #ユーザーの性格特徴
    # user_personality_pre = database.l2_personality_last_record(ip)
    # if user_personality_pre is not None:
    #     user_personality_pre = user_personality_pre.pop()
    #     user_personality_pre = user_personality_pre[2].translate(str.maketrans({'[': '', ']': '', ' ': ''})) #101110001110101010010001101
    #     personality_name = np.array(pd.read_excel('/Users/takipon/Desktop/dprapp/sample.xlsx', index_col=0, header=0, sheet_name='personality_x2').columns)

    #     user_personality = []
    #     for num in range(len(user_personality_pre)):
    #         if user_personality_pre[num] == '1':
    #             user_personality.append(personality_name[num]) #['真面目Seriousness', 'サボれないCannot slack


    # #ユーザーが設定した目標
    # user_endg_and_tasks_pre = database.l2_endg_show(ip)
    # if user_endg_and_tasks_pre is not None:
    #     user_endg_and_tasks = user_endg_and_tasks_pre.pop()


    # #ユーザーがBBSに投稿したテキスト
    # user_bbs_txt_pre = np.array(database.l3_bbs_txt_show_id(ip))
    # if user_bbs_txt_pre is not None:
    #     user_bbs_txt = user_bbs_txt_pre


    # #ユーザーがBBSでいいねしたテキストのみ
    # user_bbs_act_pre = np.array(database.l3_bbs_act_show_id(ip))
    # if user_bbs_act_pre is not None:
    #     user_bbs_act = []
    #     for bbs_act in user_bbs_act_pre:
    #         bbs_act_id = bbs_act[2]
    #         bbs_act_pre = database.l3_bbs_txt_show_post_id(bbs_act_id)
    #         user_bbs_act.append(bbs_act_pre.pop()[2]) #アクションしたテキストのみ取得


    if order == 0: #チャット
        print('チャット')
        Chat_user().run()
    #     Chat_mher().run()

    if order == 1: #ビデオチャット
        print('ビデオチャット')
        # CameraPreview()
        VChatApp().run()

    if order == 2: #TEL
        print('TEL')
        TelApp().run()

    database.l3_mc_insert(ip, memo_from_mc)    
    
else:
    print('現在混み合っております')


