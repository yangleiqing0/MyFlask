from flask_mail import Message
from flask import render_template
import time
import os
from common.selenium_get_page import ReportImage
from modles.testcase_start_times import TestCaseStartTimes


def async_send_mail(app, func, func_name='send_image', *args):
    # 获 取当前程序的上下文
    with app.app_context():
        if func_name == 'send_image':
            func(message=args[0])  # Mail的成员方法send（）
        else:
            func()


def send_mail(subject, to_user_list, user_id=None,
              testcase_time_id=None, items=None, allocation=None, testcase_scene_list=None, shot_name=None):
    from app import get_app_mail
    app, mail = get_app_mail()
    msg = Message(subject, recipients=to_user_list)
    print('send_mail shot_name', shot_name)
    if not shot_name:
        shot_name = ReportImage(user_id, testcase_time_id=testcase_time_id).get_web()
    while 1:
        time.sleep(2)
        try:
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
    mail.send(message=msg)
    os.remove(shot_name)


def send_excel(subject, to_user_list, testcase_time_id):
    from app import get_app_mail
    app, mail = get_app_mail()
    testcase_time = TestCaseStartTimes.query.get(testcase_time_id)
    filename = testcase_time.filename
    print('send_excel filename', filename)
    message = Message(subject, recipients=to_user_list, body='自动化测试报告 : %s' % testcase_time.name)
    try:

        with open(filename, 'rb') as fp:
            message.attach(filename=testcase_time.name,
                           content_type='application/octet-stream',
                           data=fp.read(), disposition='attachment', headers=None)
        mail.send(message)
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'








