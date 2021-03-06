import requests
import config
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session, redirect, url_for, render_template
from logs.config import file_log_handler, logging, FLASK_LOGS_FILE, FRONT_LOGS_FILE
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_mail import Mail
from flask_apscheduler import APScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
# flask_mail需要安装0.9.1版本


requests.packages.urllib3.disable_warnings()

logging.getLogger().addHandler(file_log_handler)
db = SQLAlchemy()

app = Flask(__name__)


def create_app():
    app.debug = True
    app.threaded = True
    app.secret_key = 'asldfwadadw@fwq@#!Eewew'
    app.config.from_object(config)
    db.init_app(app)

    from views.testcase import testcase_blueprint  # 不能放在其他位置
    from views.home import home_blueprint
    from views.case_group import case_group_blueprint
    from views.variables import variables_blueprint
    from views.request_headers import request_headers_blueprint
    from views.testcase_request import test_case_request_blueprint
    from views.testcase_report import testcase_report_blueprint
    from views.system_config import system_config_blueprint
    from views.testcase_scene import testcase_scene_blueprint
    from views.login import login_blueprint
    from views.user import user_blueprint
    from views.job import job_blueprint
    from views.emai import mail_blueprint
    from views.mysql import mysql_blueprint

    app.register_blueprint(testcase_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(case_group_blueprint)
    app.register_blueprint(variables_blueprint)
    app.register_blueprint(request_headers_blueprint)
    app.register_blueprint(test_case_request_blueprint)
    app.register_blueprint(testcase_report_blueprint)
    app.register_blueprint(system_config_blueprint)
    app.register_blueprint(testcase_scene_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(job_blueprint)
    app.register_blueprint(mail_blueprint)
    app.register_blueprint(mysql_blueprint)
    return app


create_app()


@app.before_request    # 在请求达到视图前执行
def login_required():

    # print('username: ', session.get('username'), request.path, type(session.get('username')))

    if request.path == '/user_regist/':
        if session.get('username') != 'admin':
            return redirect(url_for('testcase_blueprint.test_case_list'))

    if request.path in ('/login/', '/frontlogs/', '/flasklogs/'):
        return
    elif 'static' in request.path or 'validate' in request.path:
        return

    elif session.get('username'):
        return

    else:
        return redirect(url_for('login_blueprint.login'))


@app.errorhandler(404)
# 当发生404错误时，会被该路由匹配
def handle_404_error(err_msg):
    """自定义的异常处理函数"""
    # 这个函数的返回值就是前端用户看到的最终结果 (404错误页面)
    return render_template('exception/404.html', err_msg=err_msg)


manager = Manager(app)
# 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例

migrate = Migrate(app, db)
# manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db', MigrateCommand)


@app.before_first_request  # 在第一个次请求前执行创建数据库和预插入数据的操作
def db_create_pre_all():
    session['app_rootpath'] = app.root_path
    from views.job import init_scheduler
    from common.pre_db_insert_data import to_insert_data
    from modles.testcase import TestCases
    from modles.case_group import CaseGroup
    from modles.variables import Variables
    from modles.request_headers import RequestHeaders
    from modles.testcase_start_times import TestCaseStartTimes
    from modles.testcase_result import TestCaseResult
    from modles.testcase_scene import TestCaseScene
    from modles.user import User
    from modles.job import Job
    from modles.mail import Mail
    from modles.database import Mysql
    from modles.testcase_scene_result import TestCaseSceneResult
    from modles.time_message import TimeMessage

    db.create_all()

    to_insert_data(user_id=1)


def get_app_mail():
    from modles.variables import Variables
    user_id = session.get('user_id')
    MAIL_DEFAULT_SENDER_NAME = Variables.query.filter(
        Variables.user_id == user_id, Variables.name == '_MAIL_DEFAULT_SENDER_NAME').first().value
    MAIL_DEFAULT_SENDER_EMAIL = Variables.query.filter(
        Variables.user_id == user_id, Variables.name == '_MAIL_DEFAULT_SENDER_EMAIL').first().value
    MAIL_SERVER = Variables.query.filter(Variables.user_id == user_id, Variables.name == '_MAIL_SERVER').first().value,
    MAIL_USERNAME = Variables.query.filter(Variables.user_id == user_id,
                                           Variables.name == '_MAIL_USERNAME').first().value
    MAIL_PASSWORD = Variables.query.filter(Variables.user_id == user_id,
                                           Variables.name == '_MAIL_PASSWORD').first().value
    MAIL_DEFAULT_SENDER = (MAIL_DEFAULT_SENDER_NAME + '<%s>'% MAIL_DEFAULT_SENDER_EMAIL)
    app.config.update(
        MAIL_SERVER=MAIL_SERVER[0],
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_DEFAULT_SENDER=MAIL_DEFAULT_SENDER
    )
    print('发送邮件的参数:', MAIL_SERVER, type(MAIL_SERVER), MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER, sep='\n')
    mail = Mail(app)
    return app, mail


# 数据库迁移方法
# app.py层控制台执行
# 1:flask db init  创建 迁移数据库脚本
# 2:flask db migrate  检查模型定义和数据库当前状态的差异
# 3:flask db upgrade  更新数据库
# 不要随便手段改字段内容，容易导致自动扩展数据库字段时候失败

# 创建数据库办法   在浏览器路由/db_create_all/
def my_listener(event):
    if event.exception:
        print('任务出错了！！！！！！')
    else:
        print('任务照常运行...')


@app.before_first_request
def init_flask_log():
    with open(FLASK_LOGS_FILE, 'w+') as f:
        f.write('#coding=utf-8\n')
    with open(FRONT_LOGS_FILE, 'w+') as f:
        f.writelines(['#coding=utf-8\n',
                      '欢迎使用自动化测试平台\n', '欢迎使用自动化测试平台\n', '欢迎使用自动化测试平台\n', '欢迎使用自动化测试平台\n',
                      '欢迎使用自动化测试平台\n', '欢迎使用自动化测试平台\n', '欢迎使用自动化测试平台\n', '欢迎使用自动化测试平台\n',
                      '欢迎使用自动化测试平台\n', '联系QQ253775405\n', '微信15155492421\n', 'github地址\n',
                      'https://github.com/yangleiqing0/MyFlask.git\n', '遇到任何bug请直接联系我\n',
                      '接定制任务\n', '欢迎使用自动化测试平台\n', '欢迎使用自动化测试平台\n',
                      ])


scheduler = APScheduler()

scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.start()


@app.before_first_request
def init_scheduler_job():
    from modles.job import Job
    from views.job import scheduler_job
    jobs = Job.query.filter(Job.is_start == 1).all()
    for job in jobs:
        scheduler_job(job, scheduler)


def return_app():
    return app


if __name__ == '__main__':

    manager.run()


