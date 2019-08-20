import requests
import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session, redirect, url_for
from logs.config import file_log_handler, logging
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_mail import Mail
# flask_mail需要安装0.9.0版本

requests.packages.urllib3.disable_warnings()

logging.getLogger().addHandler(file_log_handler)
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True
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
    return app


app = create_app()


manager = Manager(app)
# 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例

migrate = Migrate(app, db)
# manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db', MigrateCommand)


@app.before_request    # 在请求达到视图前执行
def login_required():
    print('username: ', session.get('username'), type(session.get('username')))

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


from common.pre_db_insert_data import to_insert_data
from modles.testcase import TestCases
from modles.case_group import CaseGroup
from modles.variables import Variables
from modles.request_headers import RequestHeaders
from modles.testcase_start_times import TestCaseStartTimes
from modles.testcase_result import TestCaseResult
from modles.testcase_scene import TestCaseScene
from modles.user import User


@app.before_first_request  # 在第一个次请求前执行创建数据库和预插入数据的操作
def db_create_pre_all():
    session['app_rootpath'] = app.root_path

    db.create_all()

    to_insert_data(user_id=1)


def get_app_mail():
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


if __name__ == '__main__':

    manager.run()


