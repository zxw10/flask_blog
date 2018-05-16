from .user import user
from .main import main
#蓝本的配置
DEFAULT_BULEPRINT = (
    (user,'/user'),
    (main,'/main'),
)
def config_blueprint(app):
    for blueprint,url_prefix in DEFAULT_BULEPRINT:
        app.register_blueprint(blueprint,url_prefix=url_prefix)


