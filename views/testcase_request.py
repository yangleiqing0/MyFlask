import json
import re
from _datetime import datetime
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, current_app
from modles.variables import Variables
from modles.testcase import TestCases
from modles.testcase_result import TestCaseResult
from modles.case_group import CaseGroup
from modles.testcase_start_times import TestCaseStartTimes
from modles.testcase_scene import TestCaseScene
from common.tail_font_log import FrontLogs
from app import cdb, db, app
from common.analysis_params import AnalysisParams
from common.method_request import MethodRequest

test_case_request_blueprint = Blueprint('test_case_request_blueprint', __name__)


class TestCaseRequest(MethodView):

    def get(self):
        testcases = TestCases.query.filter(TestCases.testcase_scene_id.is_(None)).all()
        FrontLogs('进入测试用例执行页面').add_to_front_log()
        case_groups = CaseGroup.query.all()
        testcase_list = []
        for testcase in testcases:
            testcase.name = AnalysisParams().analysis_params(testcase.name)
            testcase_list.append(testcase)
        for case_group in case_groups:
            case_group_testcases = case_group.testcases
            num = 0
            while num < len(case_group_testcases):
                if case_group_testcases[num].testcase_scene_id not in (None, "", "None"):
                    print('remove:', case_group_testcases[num].testcase_scene_id)
                    del(case_group_testcases[num])
                else:
                    num += 1
            for case_group_testcase in case_group_testcases:
                case_group_testcase.name = AnalysisParams().analysis_params(case_group_testcase.name)
        no_case_group = type('no_case_group', (object,), dict(a=-1))
        case_groups.append(no_case_group)
        no_case_group.testcases = TestCases.query.filter(TestCases.group_id == "", TestCases.testcase_scene_id.is_(None)).all()
        no_case_group.name = "未分组测试用例"
        print('testcase :', testcases)
        print('test_case_request case_groups :', case_groups)

        testcase_scene_group = type('testcase_scene_group', (object,), dict(a=-1))
        case_groups.append(testcase_scene_group)
        testcase_scene_group.testcases = TestCaseScene.query.all()
        testcase_scene_group.name = "测试场景"

        for case_group in case_groups:
            print('test_case_request case_group :', case_group.testcases)

        return render_template('test_case_request/test_case_request.html', case_groups=case_groups)

    def post(self):
        print('TestCaseRequest post request.form: ', request.form)
        testcase_ids = request.form.getlist('testcase')
        print("request_from_list: ", testcase_ids)
        testcase_list = []
        for index, testcase_id in enumerate(testcase_ids):
            testcase = TestCases.query.get(testcase_id)
            testcase.name = AnalysisParams().analysis_params(testcase.name)
            testcase_list.append(testcase)
        print('testcase_list: ', testcase_list)

        testcase_scene_ids = request.form.getlist('testcase_scene')
        for testcase_scene_id in testcase_scene_ids:
            testcase_scene = TestCaseScene.query.get(testcase_scene_id)
            testcases = testcase_scene.testcases
            for testcase in testcases:
                testcase.scene_name = testcase.testcase_scene.name
                testcase_list.append(testcase)
        print("request_testcase_ids_list: ", testcase_ids)

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
            if 'html' in response_body:
                response_body = '<xmp> %s </xmp>' % response_body
            print('response_body:', response_body)
            testcase_result = TestCaseResult(test_case_id, testcase_time_id, response_body)
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