from flask import Blueprint,render_template,url_for,flash,get_flashed_messages,redirect,current_app
from app.forms import RegisterForm,LoginForm,ChangePhoto#导入注册的wtf表单
from app.models import User
from app.extensions import db,photo
from app.email import send_mail
from flask_login import login_user,logout_user,login_required,current_user
import os
from PIL import Image
user = Blueprint('user',__name__)
#注册视图
@user.route('/register/',methods=['get','post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data,password=form.password.data,email=form.email.data)
        # 将数据写入数据库
        db.session.add(u)
        db.session.commit()
        #生成用于验证激活状态的token
        token = u.make_active_token()
        #调用邮箱发送激活邮件
        send_mail(u.email,'账户激活','email/active',username=u.username,token=token)
        #来一个提示信息 跳转到首页
        flash('邮件已发送 请读取邮件并激活')
        return render_template('main/index.html')
    return render_template('user/register.html',form=form)

@user.route('/active/<token>')
def active(token):
    if User.check_token(token):
        flash('账户激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('账户激活失败')
        return redirect(url_for('main.index'))

#登录视图
@user.route('/login/',methods=['get','post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #查询当前用户是否存在
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('当前用户不存在')
        elif not u.confirm:
            flash('请先激活账户')
        elif u.check_password(form.password.data):
            login_user(u,remember=form.remember.data)
            flash('登录成功')
            return redirect(url_for('main.index'))
        else:
            flash('请输入正确的密码')
    return render_template('user/login.html',form=form)

#退出登录
@user.route('/logout/')
def logout():
    logout_user()
    flash('退出登录成功')
    return redirect(url_for('main.index'))

#需要登陆后才能访问的路由
@user.route('/test/')
@login_required
def test():
    return '必须登录才能范文'
#生成图片的随机图片名
def random_name(ext,length=32):
    import random,string
    myString = string.ascii_letters+'0123456789'
    return ''.join(random.choice(myString) for i in range(length))+ext

#修改头像的视图函数
@user.route('/change_photo/',methods=['post','get'])
@login_required
def change_photo():
    form = ChangePhoto()
    if form.validate_on_submit():
        #获取后缀
        ext = os.path.splitext(form.photo.data.filename)[1]
        filename = random_name(ext) #调用生成随机图片名称的函数
        photo.save(form.photo.data,name=filename) #保存图片
        #查找上传图片的路径
        s_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
        img = Image.open(s_path)
        img.thumbnail((130,130))
        img.save(s_path) #保存缩略图片
        #删除之前的图片
        if current_user.photo != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.photo))
        current_user.photo = filename #将当前的user对象的photo属性值改为当前的图片名
        db.session.add(current_user) #将更改后的当前的对象 修改到数据库中

    img_url = photo.url(current_user.photo) #获取当前用户的头像
    return render_template('user/change_photo.html',form=form,img_url=img_url)

#用户信息查看 路由
@user.route('/user_info/')
@login_required
def user_info():
    return render_template('user/user_info.html')
