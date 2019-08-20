from flask_mail import Message
from flask import render_template
from threading import Thread
from email.mime.image import MIMEImage
import base64
import os, sys


def async_send_mail(mail, app, msg):
    # 获 取当前程序的上下文
    with app.app_context():
        mail.send(message=msg)  # Mail的成员方法send（）


def get_image():
    pass


def send_mail(subject, to_user_list, items=None, allocation=None, testcase_scene_list=None, shot_name=None):
    from app import get_app_mail
    app, mail = get_app_mail()
    msg = Message(subject, recipients=to_user_list)
    print('this path:', sys.argv[0])
    with open(r'D:\PythonProject\MytestFlask\common\1566314652.642001screen.png', 'rb') as file:
        img_data = file.read()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', '<image1>')
        msg.attach(img)
        send = Thread(target=async_send_mail, args=(mail, app, msg))  # 实例化一个线程，
        send.start()  # 开始线程

    # msg.html = render_template("testcase_report/testcase_report_email.html", items=items, allocation=allocation,
    #                            testcase_scene_list=testcase_scene_list)
    send = Thread(target=async_send_mail, args=(mail, app, msg))  # 实例化一个线程，
    # send.start()  # 开始线程








