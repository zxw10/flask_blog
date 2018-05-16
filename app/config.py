import os
path = os.path.abspath(os.path.dirname(__file__))
class Config():
    #秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY','123456')
    #配置数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False #配置是否追踪
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True #配置是否默认提交
    #配置是否加载本地bootstrap样式
    BOOTSTRAP_SERVE_LOCAL = True
    # 配置smtp服务器
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.1000phone.com')
    # 用户名
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'xialigang@1000phone.com')
    # 密码
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '123456')

    #设置上传大小
    MAX_CONTENT_LENGTH = 8*1024*1024
    #设置上传路径
    UPLOADED_PHOTOS_DEST = os.path.join(path,'static/upload')

#配置开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(path,'blog-dev.sqlite')
#测试环境
class TestingConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(path, 'blog-test.sqlite')

#生产环境
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(path, 'blog.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    #设置一个默认的环境
    'default':DevelopmentConfig
}