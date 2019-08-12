import requests
import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from logs.config import file_log_handler, logging

requests.packages.urllib3.disable_warnings()
app = Flask(__name__)
app.debug = True
app.config.from_object(config)

logging.getLogger().addHandler(file_log_handler)
db = SQLAlchemy(app)

from common.connect_sqlite import cdb
from modles.testcase import TestCases
from modles.case_group import CaseGroup
from modles.variables import Variables
from modles.request_headers import RequestHeaders
from modles.testcase_start_times import TestCaseStartTimes
from modles.testcase_result import TestCaseResult
from modles.testcase_scene import TestCaseScene
db.create_all()

from common.pre_db_insert_data import *  # 建表后的预配置参数

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

if __name__ == '__main__':
    app.run()

    app.run(host='127.0.0.1', debug=True, threadad=True)