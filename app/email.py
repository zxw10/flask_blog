from flask import current_app,render_template
from flask_mail import Message
from threading import Thread
from app.extensions import mail

def async_send_mail(app,msg):
    #发送邮件 获取 程序的上下文
    with app.app_context():
        mail.send(message=msg)

def send_mail(to,subject,template,**kwargs):
    #此刻的app就是外部实例化的app
    app = current_app._get_current_object()
    msg = Message(subject=subject,recipients=[to],sender=app.config['MAIL_USERNAME'])
    msg.html = render_template(template+'.html',**kwargs)
    # msg.body = render_template(template+'.txt')
    #发送邮件
    thr = Thread(target=async_send_mail,args=(app,msg))
    thr.start()
    return thr





