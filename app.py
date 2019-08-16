import requests
import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from logs.config import file_log_handler, logging
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

requests.packages.urllib3.disable_warnings()

logging.getLogger().addHandler(file_log_handler)
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True
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

    app.register_blueprint(testcase_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(case_group_blueprint)
    app.register_blueprint(variables_blueprint)
    app.register_blueprint(request_headers_blueprint)
    app.register_blueprint(test_case_request_blueprint)
    app.register_blueprint(testcase_report_blueprint)
    app.register_blueprint(system_config_blueprint)
    app.register_blueprint(testcase_scene_blueprint)
    return app


app = create_app()

manager = Manager(app)
# 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app, db)
# manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db', MigrateCommand)

# 数据库迁移方法
# app.py层控制台执行
# 1:flask db init  创建 迁移数据库脚本
# 2:flask db migrate  检查模型定义和数据库当前状态的差异
# 3:flask db upgrade  更新数据库
# 不要随便手段改字段内容，容易导致自动扩展数据库字段时候失败

# 创建数据库办法   在浏览器路由/db_create_all/

if __name__ == '__main__':

    manager.run()


