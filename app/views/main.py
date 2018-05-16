from flask import Blueprint,render_template,url_for,redirect,flash,request
from app.models import Posts,User
from flask_login import current_user
from app.extensions import db
from app.forms import Posts as posts

main = Blueprint('main',__name__)


@main.route('/',methods=['get','post'])
def index():
    form = posts()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            p = Posts(content=form.content.data,user=u)
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('您还没有登陆')
            return redirect(url_for('user.login'))
    page = request.args.get('page',1,type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page,per_page=1,error_out=False)
    # print(postsData.all())
    #获取当前页的数据
    postsData = pagination.items
    return render_template('main/index.html', form=form,data=postsData,pagination=pagination,viewFunc='main.index')


