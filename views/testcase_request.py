import json
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, current_app
from modles.case_group import CaseGroup
from modles.request_headers import RequestHeaders
from modles.testcase import TestCases
from common.tail_font_log import FrontLogs
from app import cdb, db, app

test_case_request_blueprint = Blueprint('test_case_request_blueprint', __name__)


class TestCaseRequest(MethodView):

    def get(self):
        testcases = TestCases.query.all()
        FrontLogs('进入测试用例执行页面').add_to_front_log()
        print(testcases)
        return render_template('test_case_request.html', items=testcases)

    def post(self):
        print("request_from_list: ", request.form.getlist('testcase'))
        return 'OK'
test_case_request_blueprint.add_url_rule('/testcaserequest/', view_func=TestCaseRequest.as_view('test_case_request'))