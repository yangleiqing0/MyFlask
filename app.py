import requests
import config
from flask import Flask, session
from logs.config import file_log_handler, logging
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_mail import Mail
from flask_apscheduler import APScheduler
from common.connect_sql.connect_mysql import ConnMysql
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
# flask_mail需要安装0.9.1版本

requests.packages.urllib3.disable_warnings()

logging.getLogger().addHandler(file_log_handler)
app = Flask(__name__)


def create_app():
    from db_create import db
    app.debug = True
    app.threaded = True
    app.secret_key = 'asldfwadadw@fwq@#!Eewew'
    app.config.from_object(config)
    db.init_app(app)
    from views import view_list
    [app.register_blueprint(_view) for _view in view_list]
    return db


def create_db():
    # sql = 'drop database if EXISTS flasktest'
    # ConnMysql(config.host, config.port, config.root, config.pwd, '', sql).operate_mysql()
    sql2 = 'create database IF NOT EXISTS %s' % config.db
    ConnMysql(config.host, config.port, config.root, config.pwd, '', sql2).operate_mysql()


def return_app():
    return app


create_db()

db = create_app()


manager = Manager(app)
# 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例

migrate = Migrate(app, db)
# manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db', MigrateCommand)


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


