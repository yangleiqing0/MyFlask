from flask_mail import Message
from flask import render_template, url_for


def send_mail(subject, to_user_list):
    from app import get_app_mail
    mail = get_app_mail()
    msg = Message(subject, recipients=to_user_list)
    msg.html = render_template('')
    mail.send(msg)





