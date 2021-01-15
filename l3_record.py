import numpy as np

import l1_login, database

"""
有料ユーザーのDBは最後に連携するので、仮でl1_userのipを取得
flask連携してから再度実行すること。
.gitignoreから解除しろよい
"""

ip = l1_login.get_ip().pop()

paid_member_pre = np.array(database.l3_dairy(ip))
paid_member = np.ravel(paid_member_pre)



if ip == paid_member[1]:
    print('1')

    def uploads_file():

        # if request.method == 'POST': 本番では解除
        print('2')
            # ファイルがなかった場合の処理
        if 'file' not in request.files:
            print('3')
            flash('ファイルがありません')
            return redirect(request.url)

            # データの取り出し
            # file = request.files['file']  本番では解除
        file = '/Users/takipon/Desktop/dprapp/tester.png'

            # ファイル名がなかった時の処理
        if file.filename == '':
            print('4')
            flash('ファイルがありません')
            return redirect(request.url)

            # ファイルのチェック
        if file and allwed_file(file.filename):
            print('4')
                # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
                # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # アップロード後のページに転送
            return redirect(url_for('uploaded_file', filename=filename))
        print('5')
        return 

    uploads_file()