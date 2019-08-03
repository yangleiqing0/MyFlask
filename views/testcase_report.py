import json
import re
import os
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, current_app
from modles.variables import Variables
from modles.testcase import TestCases
from modles.testcase_result import TestCaseResult
from modles.testcase_start_times import TestCaseStartTimes
from common.tail_font_log import FrontLogs
from app import cdb, db, app
from common.analysis_params import AnalysisParams
from common.method_request import MethodRequest
from common.do_report import test_report
from datetime import datetime


testcase_report_blueprint = Blueprint('testcase_report_blueprint', __name__)


class TestCaseReport(MethodView):

    def get(self):
        testcase_time_id = request.args.get('testcase_time_id')
        time_strftime = datetime.now().strftime('%Y%m%d%H%M%S')
        testcase_report_name = Variables.query.filter(Variables.name=="_TEST_REPORT_EXCEL_NAME").first().value + "_" + \
                               time_strftime + ".xlsx"
        REPORT_FILE_PATH = Variables.query.filter(Variables.name=="_REPORT_FILE_PATH").first().value
        Filename = REPORT_FILE_PATH + testcase_report_name
        print("Filename: ", Filename)
        test_case_start_time = TestCaseStartTimes().query.get(testcase_time_id)
        test_case_start_time.filename = Filename
        db.session.commit()
        test_report(testcase_time_id)
        return render_template("testcase_report.html")


testcase_report_blueprint.add_url_rule('/testcasereport/', view_func=TestCaseReport.as_view('testcase_report'))




