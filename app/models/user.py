from app.extensions import db
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize
from flask import current_app
from app.extensions import login_manager
from flask_login import UserMixin #判断当前用户状态的一个模块
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(12),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(60),unique=True)
    confirm = db.Column(db.Boolean,default=False)
    photo = db.Column(db.String(40),default='default.jpg')
    #反响引用
    #参数1 为反向引用的类名
    #参数2 反向引用字段名称
    #参数3 加载时机  提供数据集的查询
    posts = db.relationship('Posts',backref='user',lazy='dynamic')
    @property #设置当前
    def password(self):
        raise AttributeError('密码不可读')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    #生成token方法
    def make_active_token(self):
        s = Seralize(current_app.config['SECRET_KEY'])
        return s.dumps({'id':self.id})

    #定义一个 验证token的函数
    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token) #从token中 反向加载出字典
        except:
            return False
        u = User.query.get(data['id'])
        if not u: #判断当前用户的数据 是否存在
            return False
        if not u.confirm: #如果没激活则 激活 否则直接return True
            u.confirm = True
            db.session.add(u)
        return True
    #验证输入密码是否正确的方法
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

#登录模块的回调函数
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
