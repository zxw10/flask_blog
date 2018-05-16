from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import Length

class Posts(FlaskForm):
    content = TextAreaField('',render_kw={'style':'resize:none;','rows':4,'placeholder':'请发表你的感想...'},validators=[Length(6,120,message='允许的内容长度为6~120个字符')])
    submit = SubmitField('发表')

