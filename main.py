import csv
import datetime
import os
import math
import numpy as np
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from flask import send_from_directory, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_parameter

import database, l1_ai, l1_login , l2_pd, l2_ai, l2_record, l3_record, l2_endg, l3_create_user, l3_quest, l3_bbs, l3_twmc



app = Flask(__name__)


#L1/L2愚痴聞き AI Listening
@app.route("/")
def index():
    text = 'can you tell me your day?'
    return render_template('l1_l2_ai.html', word2=text)#word1=understanding, word2=empathy

@app.route("/", methods=["post"])
def post():
    text = request.form['text']
    word1, word2, score = l1_ai.l1_ai(text)
    word1 = 'I see your think of ' + word1[0]
    word2 = [word2.pop()]

    if score >= 0.8:
        recommend = l2_ai.l2_ai()
        txt = 'I can reccomend to you'
        for reco in recommend:
            txt = txt +', '+ reco
        word2.append(txt + 'and so on.')

    return render_template('l1_l2_ai.html', word1=word1, word2=word2)#word1=understanding, word2=empathy



#L2性格診断 diagnosis personarity
@app.route("/diagnosis_p")
def diagnosis():

    question = []
    with open('/Users/takipon/Desktop/dprapp/question.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            question.append(row)
    question = sum(question, [])

    message='can you tell me youself?'

    return render_template('l2_pd.html', question=question, message=message)#word1=understanding, word2=empathy

@app.route("/diagnosis_p", methods=["post"])
def diagnosis_post():

    question = []
    with open('/Users/takipon/Desktop/dprapp/question.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            question.append(row)
    question = sum(question, [])

    survey = []
    for i in range(len(question)):
        survey.append(int(request.form['{}'.format(i)]))

    survey = [survey] #アルゴリズムが二次元にしか対応してないので二次元に
    result = l2_pd.l2_dignosis(survey)

    message = 'I can know yourself thank to you.'+ '{:.0%}'.format(result) #🌟本番ではresultは非表示で

    return render_template('l2_pd.html', question=question, message=message)#word1=understanding, word2=empathy



#L2/L3日記 Your Dairy
@app.route("/dairy")
def dairy():
    dairy_pre = l2_record.l2_show_more()
    pagination, res = pagination_func(dairy_pre)

    return render_template('l2_l3_dairy.html', text=res, pagination=pagination)

@app.route("/dairy", methods=["post"])
def dairy_post():
    new_text = request.form['new_text']

    admit = l3_record.l3_record()
    if admit is 'OK':
        UPLOAD_FOLDER = os.path.join('static', 'img')
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        file = request.files['imgfile']
        # if file and allwed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        img = '/static/img/' + file.filename
    else:
        img = ''
    # img = 'static/img/tester.png'
    # d = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    d_comment = l2_record.l2_dairy(new_text, img)

    dairy_pre = l2_record.l2_show_more()
    pagination, res = pagination_func(dairy_pre)

    return render_template('l2_l3_dairy.html', text=res, pagination=pagination, d_comment=d_comment)

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    ALLOWED_EXTENSIONS = set(['png', 'jpeg' , 'jpg', 'gif'])

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pagination_func(datas):  #ページネーション
    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = datas[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(datas),  per_page=10, css_framework='foundation')
    return pagination, res



#L2最終目標 Your Final Goal
@app.route("/fg_p")
def endg():

    question = ['what is your final goal?']

    admit =l2_endg.endg_admittion()
    if admit == 0:
        question.append('for your final goal, what do you need to do?')

    fgs = l2_endg.endg_show()
    new_fgs = [fgs[0] + ' is your end goal.']
    new_fgs.append(fgs[1] + ' are your tasks.')

    return render_template('l2_endg.html', our_text=question, fgs=new_fgs)

@app.route("/fg_p", methods=["post"])
def endg_post():

    endg = request.form['0']
    tasks = request.form['1']

    l2_endg.endg(endg, tasks)


    question = ['what is your final goal?']
    admit =l2_endg.endg_admittion()
    if admit == 0:
        question.append('for your final goal, what do you need to do?')

    fgs = l2_endg.endg_show()
    new_fgs = [fgs[0] + ' is your end goal.']
    new_fgs.append(fgs[1] + ' are your tasks.')

    return render_template('l2_endg.html', our_text=question, fgs=new_fgs)



#L3ユーザー登録 User Registration
@app.route("/uregistration_p")
def ur():
    title, sample = show()

    datas = l3_create_user.l3_user_show()
    if datas != []:
        sample = np.ravel(datas)

    return render_template('l3_user_create.html', title=title, sample=sample)

@app.route("/uregistration_p", methods=["post"])
def ur_post():
    title, sample = show()

    data = []
    for i in range(len(title)):
        data.append(request.form['{}'.format(i)])
    
    l3_create_user.l3_cuser(data[0], data[1], data[2], data[3], data[4])

    #データがあれば、以前入力したものを下書きに入れる
    datas = l3_create_user.l3_user_show()
    if datas != []:
        sample = np.ravel(datas)

    return render_template('l3_user_create.html', title=title, sample=sample)

def show():
    title = ['Your name', 'Your birthday', 'Your e-mail address', 'Your Phone number', 'Your credit card']
    sample = ['Louis Brown', '19901201', 'pasta@pizza.com','00011118888' ,'xxx111dddd']
    return title, sample



#L3クエスト Self Quest
@app.route("/quest_p")
def quest():

    fgs = l2_endg.endg_show()
    new_fgs = fgs[1].split(',')
    for i in range(len(new_fgs)): #blank除外
        if new_fgs[i] == '':
            new_fgs.pop(i)

    sug = l3_quest.suggest()

    return render_template('l3_quest.html', fgs=new_fgs, sug=sug)



#L3掲示板 Message Board
@app.route("/bbs_p")
def bbs():

    warn = ''
    txt, date, bbs_id = l3_bbs.bbs_show()
    act = l3_bbs.bbs_show_act()

    pagination, txt, date, act, bbs_id = bbs_pagination_func(txt, date, act, bbs_id) #paginationでデータを調整

    return render_template('l3_bbs.html', bbs_id=bbs_id, act=act, txt=txt, date=date, warn=warn, pagination=pagination)

@app.route("/bbs_p", methods=["post"])
def bbs_post():

    txt = request.form['new_post']
    warn = l3_bbs.bbs(txt)

    txt, date, bbs_id = l3_bbs.bbs_show()
    act = l3_bbs.bbs_show_act()
    pagination, txt, date, act, bbs_id = bbs_pagination_func(txt, date, act, bbs_id)

    return render_template('l3_bbs.html', bbs_id=bbs_id, act=act, txt=txt, date=date, warn=warn, pagination=pagination)

@app.route("/bbs_ajax", methods=["post"])
def bbs_ajax():

    value = request.form['text']
    act = request.form['act']

    if len(value) > 0: #ifの中に書かないと起動しない
        value = int(value) + 1
        l3_bbs.bbs_act_insert_remove(act)

        return jsonify({'output':value})

def bbs_pagination_func(datas, date, act, bbs_id):  #ページネーション
    page = request.args.get(get_page_parameter(), type=int, default=1)
    res_data = datas[(page - 1)*10: page*10]
    res_day = date[(page - 1)*10: page*10]
    res_act = act[(page - 1)*10: page*10]
    bbs_id = bbs_id[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(datas),  per_page=10, css_framework='foundation')
    return pagination, res_data, res_day, res_act, bbs_id



#L3会話withMC Conversation with MC
@app.route("/twmc_p")
def twmc():

    txt =''

    return render_template('l3_twmc.html', txt=txt)

@app.route("/twmc_p", methods=["post"])
def twmc_post():

    sign = request.form['action']

    return render_template('l3_twmc.html', txt=sign)

@app.route("/twmc_ajax", methods=["post"])
def twmc_ajax():

    sign = request.form['sign']

    if len(sign) > 0: #ifの中に書かないと起動しない

        print('いま',sign)
        sign = l3_twmc.twmc(sign)
        print('こうなったよ',sign)

        return jsonify({'output':sign})

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
	# print('Message: ' + msg)
	send(msg, broadcast=True)




if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)