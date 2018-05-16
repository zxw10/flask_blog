from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import ValidationError,DataRequired,Length,Email,EqualTo
from app.models import User
from flask_wtf.file import FileField,FileRequired,FileAllowed
from app.extensions import photo

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='用户名不能为空'),Length(6,12,message='长度为6-12位')])
    password = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(6,12,message='密码长度为6-12位')])
    confirm = PasswordField('确认密码',validators=[EqualTo('password',message='俩次密码输入不一致')])
    email = StringField('邮箱',validators=[Email(message='请输入正确的邮箱格式')])
    submit = SubmitField('立即注册')
    #自定义 字段验证
    #验证用户名是否存在
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('当前用户已存在')
    #验证邮箱是否存在
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('当前邮箱已存在')


#登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(6, 12, message='长度为6-12位')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6, 12, message='密码长度为6-12位')])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')


class ChangePhoto(FlaskForm):
    photo = FileField('上传头像',validators=[FileRequired('请选择文件'),FileAllowed(photo,message='请选择正常类型的图片')])
    submit = SubmitField('上传头像')