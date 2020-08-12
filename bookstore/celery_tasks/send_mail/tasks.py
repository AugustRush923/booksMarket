from celery_tasks.main import app
from django.conf import settings
from django.core.mail import send_mail


@app.task(name="bookstore_send_mail")
def send_active_mail(token, username, email):
    """发送激活邮件"""
    subject = "书城用户激活"  # 标题
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [email]  # 收件人列表
    html_message = '<a href="http://127.0.0.1:8000/user/active/%s/">http://127.0.0.1:8000/user/active/</a>' % token
    send_mail(subject, message, sender, receiver, html_message=html_message)