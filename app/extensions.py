#导入类库
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager #pip install falsk-login
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
from flask_moment import Moment

#创建对象
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate(db=db)
login_manager = LoginManager()
photo = UploadSet('photos',IMAGES)
moment = Moment()

#将对象初始化的函数 只需要在app.__init__.py 中导入调用即可
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    #指定登录的路由
    login_manager.login_view = 'user.login'
    #指定登录的提示信息
    login_manager.login_message = '需要登录才可以访问'
    #设置当前 session的保护级别
    login_manager.session_protection = 'strong'
    #配置文件上传的操作
    configure_uploads(app,photo)
    patch_request_class(app,size=None)

    #时间对象
    moment.init_app(app)