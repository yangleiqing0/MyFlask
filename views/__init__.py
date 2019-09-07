from .testcase import testcase_blueprint  # 不能放在其他位置
from .home import home_blueprint
from .case_group import case_group_blueprint
from .variables import variables_blueprint
from .request_headers import request_headers_blueprint
from .testcase_request import test_case_request_blueprint
from .testcase_report import testcase_report_blueprint
from .system_config import system_config_blueprint
from .testcase_scene import testcase_scene_blueprint
from .login import login_blueprint
from .user import user_blueprint
from .job import job_blueprint
from .emai import mail_blueprint
from .mysql import mysql_blueprint

view_list = []
[view_list.append(eval(dr)) if '_blueprint' in dr else "" for dr in dir()]
