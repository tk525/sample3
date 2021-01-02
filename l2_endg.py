import re
import pandas as pd
import database, l2_ai, l1_login


#もし初めてなら文を作れ＋login
tester = pd.read_csv('/Users/takipon/Desktop/dprapp/tester_endg.csv')

ip = l1_login.get_ip().pop()

# personal_score = l2_ai.personal_score(ip) #0.144814814814815
personal_score = 0.80

end_goal = '最終目標はXだよ'



if personal_score <= 0.75:
    end_goal_tasks = 'empty'
elif personal_score >= 0.75:
    # end_goal_tasks = list(tester.columns)
    end_goal_tasks = ""
    for col in tester.columns:
        end_goal_tasks = col + "," + end_goal_tasks
    end_goal_tasks = re.sub(r"'","''", end_goal_tasks) #クォーテーション対策。クォーテーションがある部分にもう１つ入れるとクォーテーションとして機能するらしい

database.l2_endg(ip, end_goal, end_goal_tasks)
