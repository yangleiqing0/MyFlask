from flask.views import MethodView
from flask import render_template, Blueprint, request
from modles.variables import Variables
from modles.testcase_start_times import TestCaseStartTimes
from common.tail_font_log import FrontLogs
from app import cdb, db, app
from common.do_report import test_report
from datetime import datetime

system_config_blueprint = Blueprint('system_config_blueprint', __name__)


class EmailConfig(MethodView):

    def get(self):
        return render_template('system_config/email_config.html')


system_config_blueprint.add_url_rule('/emailconfig/', view_func=EmailConfig.as_view('email_config'))