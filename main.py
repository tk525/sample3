import csv
import datetime
import os
import math
import numpy as np
import bleach
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from flask import send_from_directory, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_parameter


import database, l1_ai, l1_login , l2_pd, l2_ai, l2_record, l3_record, l2_endg, l3_create_user, l3_quest, l3_bbs, l3_twmc

from validation import *



app = Flask(__name__)



#L1/L2愚痴聞き AI Listening
@app.route("/")
def index():
    #XSS対策 validation
    form = AiForm()

    text = 'can you tell me your day?'
    return render_template('l1_l2_ai.html', word2=text, form=form)#word1=understanding, word2=empathy

@app.route("/", methods=["post"])
def post():
    #XSS対策 validation
    form = AiForm()
    if request.method == "POST":
        if form.validate_on_submit():

            text = request.form['ai_txt']

            #XSS対策 sanitizing
            text = bleach.clean(text)

            word1, word2, score = l1_ai.l1_ai(text)
            word1 = 'I see your think of ' + word1[0]
            word2 = [word2.pop()]

            if score >= 0.8:
                recommend = l2_ai.l2_ai()
                txt = 'I can reccomend to you'
                for reco in recommend:
                    txt = txt +', '+ reco
                word2.append(txt + 'and so on.')
        else:
            word1 = ''
            word2 = ''

    return render_template('l1_l2_ai.html', word1=word1, word2=word2, form=form)#word1=understanding, word2=empathy




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
        value = request.form['{}'.format(i)]

        #XSS対策
        value = bleach.clean(value)
        survey.append(int(value))

    survey = [survey] #アルゴリズムが二次元にしか対応してないので二次元に
    result = l2_pd.l2_dignosis(survey)

    message = 'I can know yourself thank to you.'+ '{:.0%}'.format(result) #🌟本番ではresultは非表示で

    return render_template('l2_pd.html', question=question, message=message)#word1=understanding, word2=empathy





#L2/L3日記 Your Dairy🌟
@app.route("/dairy")
def dairy():
    #XSS対策 validation
    form = DairyForm()

    dairy_pre = l2_record.l2_show_more()
    pagination, res = pagination_func(dairy_pre)

    return render_template('l2_l3_dairy.html', text=res, pagination=pagination, form=form)

@app.route("/dairy", methods=["post"])
def dairy_post():
    #XSS対策 validation
    form = DairyForm()
    if request.method == "POST":
        if form.validate_on_submit():

            new_text = request.form['new_text']

            #XSS対策
            new_text = bleach.clean(new_text)

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

        else:
            res=''
            pagination=''
            d_comment=''

    return render_template('l2_l3_dairy.html', text=res, pagination=pagination, d_comment=d_comment, form=form)

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





#L2最終目標 Your Final Goal🌟
@app.route("/fg_p")
def endg():
    #XSS対策 validation
    form = EndgForm()

    question = ['what is your final goal?']

    admit =l2_endg.endg_admittion()
    if admit == 0:
        question.append('for your final goal, what do you need to do?')

    fgs = l2_endg.endg_show()
    new_fgs = [fgs[0] + ' is your end goal.']
    new_fgs.append(fgs[1] + ' are your tasks.')

    return render_template('l2_endg.html', our_text=question, fgs=new_fgs, form=form)

@app.route("/fg_p", methods=["post"])
def endg_post():

    #XSS対策 validation
    form = EndgForm()
    if request.method == "POST":
        if form.validate_on_submit():

            endg = request.form['endg_txt']
            tasks = request.form['tasks_txt']

            #XSS対策
            endg = bleach.clean(endg)
            tasks = bleach.clean(tasks)

            l2_endg.endg(endg, tasks)


            question = ['what is your final goal?']
            admit =l2_endg.endg_admittion()
            if admit == 0:
                question.append('for your final goal, what do you need to do?')

            fgs = l2_endg.endg_show()
            new_fgs = [fgs[0] + ' is your end goal.']
            new_fgs.append(fgs[1] + ' are your tasks.')
        
        else:
            question=''
            new_fgs=''

    return render_template('l2_endg.html', our_text=question, fgs=new_fgs, form=form)





#L3ユーザー登録 User Registration🌟
@app.route("/uregistration_p")
def ur():
    #XSS対策 validation
    form = UserCreateForm()

    sample = show()

    datas = l3_create_user.l3_user_show()
    if datas != []:
        sample = np.ravel(datas)

    return render_template('l3_user_create.html', sample=sample, form=form)

@app.route("/uregistration_p", methods=["post"])
def ur_post():
    #XSS対策 validation
    form = UserCreateForm()
    if request.method == "POST":
        if form.validate_on_submit():

            sample = show()

            name = request.form['uc_name']
            birth = request.form['uc_birth']
            email = request.form['uc_email']
            phonenum = request.form['uc_phonenum']
            card = request.form['uc_dcard']

            #XSS対策   
            name = ['pm_user_name', bleach.clean(name)]
            birth = ['pm_birth', bleach.clean(birth)]
            email = ['pm_mail', bleach.clean(email)]
            tel = ['pm_tel', bleach.clean(phonenum)]
            card = ['pm_credit_card', bleach.clean(card)]

            #データをまとめる
            lists = []
            list_pre = [name, birth, email, tel, card]
            for i in range(len(list_pre)):
                if list_pre[i][1] != '':
                    lists.append(list_pre[i])
            
            #すでにDBにあるかチェック
            result = l3_create_user.user_check()
            if result == 'OK': #部分更新

                l3_create_user.cuser_update(lists)

                # 確認用 名前のみ
                print(database.l3_create_user_show())

            else: #新規作成
                l3_create_user.l3_cuser(name[1], birth[1], email[1], tel[1], card[1])
            
            # #データがあれば、以前入力したものを下書きに入れる
            sample = l3_create_user.l3_user_show()

    return render_template('l3_user_create.html', sample=sample, form=form)

def show():
    sample = ['Louis Brown', '19901201', 'pasta@pizza.com','00011118888' ,'xxx111dddd']
    return sample





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





#L3掲示板 Message Board🌟
@app.route("/bbs_p")
def bbs():
    #XSS対策 validation
    form = BbsForm()

    warn = ''
    txt, date, bbs_id = l3_bbs.bbs_show()
    act = l3_bbs.bbs_show_act()

    pagination, txt, date, act, bbs_id = bbs_pagination_func(txt, date, act, bbs_id) #paginationでデータを調整

    return render_template('l3_bbs.html', bbs_id=bbs_id, act=act, txt=txt, date=date, warn=warn, pagination=pagination, form=form)

@app.route("/bbs_p", methods=["post"])
def bbs_post():
    #XSS対策 validation
    form = BbsForm()
    if request.method == "POST":
        if form.validate_on_submit():

            txt = request.form['bbs_txt']
            print(txt)

            #XSS対策
            txt = bleach.clean(txt)

            warn = l3_bbs.bbs(txt)

            txt, date, bbs_id = l3_bbs.bbs_show()
            act = l3_bbs.bbs_show_act()
            pagination, txt, date, act, bbs_id = bbs_pagination_func(txt, date, act, bbs_id)

        else:
            bbs_id=''
            act=''
            txt=''
            date=''
            warn=''
            pagination=''

    return render_template('l3_bbs.html', bbs_id=bbs_id, act=act, txt=txt, date=date, warn=warn, pagination=pagination, form=form)

@app.route("/bbs_ajax", methods=["post"])
def bbs_ajax():

    #いいねはバリデーションしていないが、もしかすると必要？
    value = request.form['text']
    act = request.form['act']

    if len(value) > 0: #ifの中に書かないと起動しない
        value = int(value) + 1
        l3_bbs.bbs_act_insert_remove(act)

        return jsonify({'output':value})

    else:
        return jsonify({'output':form})

def bbs_pagination_func(datas, date, act, bbs_id):  #ページネーション
    page = request.args.get(get_page_parameter(), type=int, default=1)
    res_data = datas[(page - 1)*10: page*10]
    res_day = date[(page - 1)*10: page*10]
    res_act = act[(page - 1)*10: page*10]
    bbs_id = bbs_id[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(datas),  per_page=10, css_framework='foundation')
    return pagination, res_data, res_day, res_act, bbs_id





#L3会話withMC Conversation with MC🌟
@app.route("/twmc_p")
def twmc():

    txt =''

    return render_template('l3_twmc.html', txt=txt)

@app.route("/twmc_p", methods=["post"])
def twmc_post():

    form = TwmcForm()
    sign = request.form['action']

    return render_template('l3_twmc.html', txt=sign, form=form)

@app.route("/twmc_ajax", methods=["post"])
def twmc_ajax():

    #XSS対策 validation
    form = TwmcForm()
    if request.method == "POST":
        if form.validate_on_submit():

            sign = request.form['sign']

            #XSS対策
            sign = bleach.clean(sign)

            if len(sign) > 0: #ifの中に書かないと起動しない

                print('いま',sign)
                sign = l3_twmc.twmc(sign)
                print('こうなったよ',sign)

                return jsonify({'output':sign})

        else:
            return jsonify({'output':form})


app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
	# print('Message: ' + msg)
	send(msg, broadcast=True)




#管理者ページ
@app.route("/own_p")
def own():

    return render_template('own.html')




if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)