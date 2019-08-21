from flask_mail import Message
from flask import render_template, session
from threading import Thread
import time
import os
from common.selenium_get_page import ReportImage
from common.temporary_variable import variables


def async_send_mail(app, func, func_name='send_image', *args):
    # 获 取当前程序的上下文
    with app.app_context():
        if func_name == 'send_image':
            func(message=args[0])  # Mail的成员方法send（）
            os.remove(variables['shot_name'])
        else:
            func()


def send_mail(subject, to_user_list, user_id=None, testcase_time_id=None, items=None, allocation=None, testcase_scene_list=None, shot_name=None):
    from app import get_app_mail
    app, mail = get_app_mail()
    msg = Message(subject, recipients=to_user_list)
    print('send_mail shot_name', shot_name)
    variables.clear()
    if not shot_name:
        send = Thread(target=async_send_mail, args=(app, ReportImage(user_id, testcase_time_id=testcase_time_id).get_web, 'no'))  # 实例化一个线程，
        send.start()  # 开始线程
    while 1:
        time.sleep(2)
        try:
            shot_name = variables['shot_name']
            print('shot_name os :', os.path.exists(shot_name), shot_name)
            if os.path.exists(shot_name):
                break
            continue
        except KeyError as e:
            print(e)
            continue

    with open(shot_name, 'rb') as file:
        img_data = file.read()
    msg.attach(filename=shot_name, data=img_data, content_type='application/octet-stream', disposition='inline',
                    headers=[('Content-ID', 'report_image')])
    msg.html = render_template('testcase_report/testcase_report_email_image.html')
    mail_send = mail.send
    send = Thread(target=async_send_mail, args=(app, mail_send, 'send_image', msg))  # 实例化一个线程，
    send.start()  # 开始线程


    # msg.html = render_template("testcase_report/testcase_report_email.html", items=items, allocation=allocation,
    #                            testcase_scene_list=testcase_scene_list)
    # send = Thread(target=async_send_mail, args=(mail, app, msg))  # 实例化一个线程，
    # send.start()  # 开始线程








