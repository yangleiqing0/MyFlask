import json
import re
from _datetime import datetime
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

test_case_request_blueprint = Blueprint('test_case_request_blueprint', __name__)


class TestCaseRequest(MethodView):

    def get(self):
        testcases = TestCases.query.all()
        FrontLogs('进入测试用例执行页面').add_to_front_log()
        testcase_list = []
        for testcase in testcases:
            testcase.name = AnalysisParams().analysis_params(testcase.name)
            testcase_list.append(testcase)
        print(testcases)
        return render_template('test_case_request/test_case_request.html', items=testcase_list)

    def post(self):
        testcase_ids = request.form.getlist('testcase')
        print("request_from_list: ", request.form.getlist('testcase'))
        # testcase_dict = {}
        testcase_list = []
        for index, testcase_id in enumerate(testcase_ids):
            testcase = TestCases.query.get(testcase_id)
            testcase.name = AnalysisParams().analysis_params(testcase.name)
            testcase_list.append(testcase)
        #     testcase_dict.update({"index": index, "id%s" % index: testcase_id, "name%s" % index: testcase_name})
        # testcase_dict = json.dumps({"testcase_dict": str(testcase_dict)})
        # print('testcase_dict: ', testcase_dict)
        print('testcase_list: ', testcase_list)

        return render_template('test_case_request/test_case_request_list.html', items=testcase_list)


class TestCaseRequestStart(MethodView):

    def post(self):
        if request.is_xhr:
            print(request.args)
            test_case_id = request.form.get('id')
            testcase_time_id = request.form.get('test_case_time_id')
            print('异步请求的test_case_id,testcase_time_id: ', test_case_id, testcase_time_id)
            testcase = TestCases.query.get(test_case_id)
            url = AnalysisParams().analysis_params(testcase.url)
            data = AnalysisParams().analysis_params(testcase.data)
            method = testcase.method
            regist_variable = testcase.regist_variable
            regular = testcase.regular
            headers = json.loads(AnalysisParams().analysis_params(testcase.request_headers.value, is_change="headers"))
            print('request_headers:', headers)
            response_body = MethodRequest().request_value(method, url, data, headers)
            testcase_result = TestCaseResult(test_case_id,testcase_time_id, response_body)
            db.session.add(testcase_result)
            db.session.commit()
            if regist_variable and regular:
                regist_variable_value = re.compile(regular).findall(response_body)
                if len(regist_variable_value) > 0:
                    if Variables.query.filter(Variables.name == regist_variable).count() > 0:
                        print('存在此变量时：', Variables.query.filter(Variables.name == regist_variable).first())
                        Variables.query.filter(Variables.name == regist_variable).first().value = regist_variable_value[0]
                        db.session.commit()
                        return response_body
                    private_variable_value = regist_variable_value[0]
                    private_variable = Variables(regist_variable, private_variable_value, is_private=1)
                    db.session.add(private_variable)
                    db.session.commit()
                    return response_body

                return '未成功解析报文 %s ' % response_body
            return response_body


class TestCaseTimeGet(MethodView):

    def get(self):
        time_strftime = datetime.now().strftime('%Y%m%d%H%M%S')
        testcase_time = TestCaseStartTimes(time_strftime=time_strftime)
        db.session.add(testcase_time)
        db.session.commit()
        print('testcase_time: ', testcase_time)
        return json.dumps({"testcase_time_id": str(testcase_time.id)})


test_case_request_blueprint.add_url_rule('/testcaserequest/', view_func=TestCaseRequest.as_view('test_case_request'))
test_case_request_blueprint.add_url_rule('/testcaserequeststart/', view_func=TestCaseRequestStart.as_view('test_case_request_start'))
test_case_request_blueprint.add_url_rule('/testcasetimeget/', view_func=TestCaseTimeGet.as_view('test_case_time_get'))