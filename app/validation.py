from flask_wtf import FlaskForm
from wtforms import * #simple.pyの中身
from wtforms.validators import *
from wtforms.fields.html5 import * #html5.pyのなかみ

class AiForm(FlaskForm):
    ai_txt = TextAreaField('ai_txt', 
        validators=[
            DataRequired(),
            # Length(max=140),
        ]
    )

class DairyForm(FlaskForm):
    dairy_txt = TextAreaField('dairy_txt', 
        validators=[
            DataRequired(),
            Length(max=70),
        ]
    )
    
class EndgForm(FlaskForm):
    endg_txt = TextAreaField('endg_txt', 
        validators=[
            DataRequired(),
            Length(max=70),
        ],
    )
    tasks_txt = TextAreaField('tasks_txt', 
        validators=[
            DataRequired(),
            Length(max=140),
        ],
    )

class UserCreateForm(FlaskForm):
    uc_name = TextField('uc_name', 
        validators=[
            Length(max=20),
        ]
    )
    
    uc_birth = TextField('uc_birth', 
        validators=[
            Length(max=8),
        ]
    )
    uc_email = EmailField('uc_email')
    uc_phonenum = TextField('uc_phonenum')
    uc_dcard = TextField('uc_dcard', 
        validators=[
            Length(max=15),
        ]
    )

class BbsForm(FlaskForm):
    bbs_txt = TextAreaField('bbs_txt', 
        validators=[
            DataRequired(),
            Length(max=140),
        ]
    )
class TwmcForm(FlaskForm):
    twmc_txt = TextField('twmc_txt', 
        validators=[
            DataRequired(),
            Length(max=70),
        ]
    )
    twmc_room = TextField('twmc_room', 
        validators=[
            DataRequired(),
            Length(max=10),
        ]
    )
