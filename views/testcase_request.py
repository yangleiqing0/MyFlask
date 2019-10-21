# encoding=utf-8
import json
import time
import operator
from _datetime import datetime
from flask.views import MethodView
from flask import render_template, Blueprint, request, session, current_app
from common.tail_font_log import FrontLogs
from common.analysis_params import AnalysisParams
from common.execute_testcase import to_execute_testcase
from common.assert_method import AssertMethod
from common.most_common_method import NullObject
from views.mysql import mysqlrun
from modles import datetime, TestCases, TestCaseResult, CaseGroup, TestCaseStartTimes, TestCaseScene, User, db, \
    Variables

test_case_request_blueprint = Blueprint('test_case_request_blueprint', __name__)


class TestCaseRequest(MethodView):

    def get(self):
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        print('user_id:', user_id)
        FrontLogs('进入测试用例执行页面').add_to_front_log()
        case_groups = CaseGroup.query.filter(CaseGroup.user_id == user_id).order_by(
            CaseGroup.updated_time.desc(), CaseGroup.id.desc()).all()
        case_groups_new = []
        for case_group in case_groups:
            case_group_NullObject = NullObject()
            case_group_NullObject.name = case_group.name
            testcase_list = []
            testcases = TestCases.query.join(CaseGroup, CaseGroup.id == TestCases.group_id).filter(
                TestCases.testcase_scene_id.is_(None), TestCases.group_id == case_group.id, TestCases.user_id == user_id
            ).order_by(TestCases.updated_time.desc(), TestCases.id.desc()).all()
            print(' %s testcases_:' % case_group, testcases)
            for testcase in testcases:
                testcase_NullObject = NullObject()
                testcase_NullObject.id = testcase.id
                testcase_NullObject.name = testcase.name
                testcase_NullObject.is_testcase_scene = 0
                testcase_list.append(testcase_NullObject)
            try:
                case_group_scene = TestCaseScene.query.join(CaseGroup, CaseGroup.id == TestCaseScene.group_id).filter(
                    TestCaseScene.user_id == user_id, CaseGroup.name == case_group.name).order_by(
                    TestCaseScene.updated_time.desc(), TestCaseScene.id.desc()).all()
                for testcase_scene in case_group_scene:
                    testcase_scene_NullObject = NullObject()
                    testcase_scene_NullObject.id = testcase_scene.id
                    testcase_scene_NullObject.name = testcase_scene.name
                    testcase_scene_NullObject.is_testcase_scene = 1
                    testcase_list.append(testcase_scene_NullObject)
            except KeyError:
                pass

            case_group_NullObject.testcase_list = testcase_list
            case_groups_new.append(case_group_NullObject)
            print('testcase_list: ', case_group_NullObject.name, testcase_list)

        return render_template('test_case_request/test_case_request.html', case_groups=case_groups_new)

    def post(self):
        print('TestCaseRequest post request.form: ', request.form)
        testcase_ids = request.form.getlist('testcase')
        for _i in range(len(testcase_ids)):
            testcase_ids[_i] = int(testcase_ids[_i])
        print("request_from_list: ", testcase_ids)
        scene_case_list = []
        testcase_list = []
        for index, testcase_id in enumerate(testcase_ids):
            testcase = TestCases.query.get(testcase_id)
            testcase.name = AnalysisParams().analysis_params(testcase.name)
            testcase_list.append(testcase)
            scene_case_list.append([testcase.id, ])
        print('testcase_list post: ', testcase_list,  scene_case_list)

        testcase_scene_ids = request.form.getlist('testcase_scene')
        scene_list = []
        for testcase_scene_id in testcase_scene_ids:
            testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        #     scene_list.append(_testcase_scene)
        #
        # cmpfun = operator.attrgetter('updated_time')
        # scene_list.sort(key=cmpfun, reverse=True)
        # print('scene_list', scene_list)
        # for testcase_scene in scene_list:
            testcases = testcase_scene.testcases
            case_list = []
            for testcase in testcases:
                testcase.scene_name = testcase.testcase_scene.name
                testcase_list.append(testcase)
                case_list.append(testcase.id)
                testcase_ids.append(testcase.id)
            scene_case_list.append(case_list)
        print("request_testcase_ids_list: ", scene_list)

        return render_template('test_case_request/test_case_request_list.html', items=testcase_list,
                               scene_case_list=scene_case_list, testcase_ids=testcase_ids)


class TestCaseRequestStart(MethodView):

    def post(self, request_is_xhr=None):
        if request.is_xhr or request_is_xhr:
            print(request.args)
            test_case_id = request.form.get('testcase_id')
            testcase_time_id = request.form.get('test_case_time_id')
            print('异步请求的test_case_id,testcase_time_id: ', test_case_id, testcase_time_id)
            response_body = post_testcase(test_case_id, testcase_time_id)
            return response_body


def post_testcase(test_case_id=None, testcase_time_id=None, testcase=None, is_run=False, is_commit=True):

    if not testcase:
        testcase = TestCases.query.get(test_case_id)
    else:
        is_run = True
    session[testcase.name] = []
    url, data = AnalysisParams().analysis_more_params(testcase.url, testcase.data, testcase_name=testcase.name)
    method = testcase.method
    if isinstance(testcase, NullObject):
        return to_execute_testcase(testcase, url, data , is_commit=is_commit)

    if testcase.wait:
        # 前置等待验证
        # url, data = AnalysisParams().analysis_more_params(testcase.url, testcase.data, testcase_name=testcase.name)
        hope_result = AnalysisParams().analysis_more_params(testcase.hope_result)
        wait = testcase.wait[0]
        time_count = 0
        if wait.old_wait_mysql and wait.old_wait and wait.old_wait_sql:
            _hope_result = AnalysisParams().analysis_params(wait.old_wait)
            mysqlrun(mysql_id=wait.old_wait_mysql, sql=wait.old_wait_sql, is_request=False, regist=False, is_cache=True)
            while 1:
                old_wait_value = mysqlrun(mysql_id=wait.old_wait_mysql, sql=wait.old_wait_sql, is_request=False,
                                          regist=False, cache=True)
                old_wait_assert_result = AssertMethod(actual_result=old_wait_value,
                             hope_result=_hope_result).assert_method()
                if old_wait_assert_result == "测试成功":
                    break
                else:
                    print('5s后执行下一次前置验证, 此次查询结果: %s 已执行 %ss  等待超时%s' % (old_wait_value, time_count,  int(wait.old_wait_time) * 60))
                    time_count += 5
                    time.sleep(5)
                if wait.old_wait_time:
                    if time_count == int(wait.old_wait_time) * 60:
                        time_out_mes = "前置等待超时, 查询结果 %s" % old_wait_value
                        if testcase_time_id:
                            testcase_result = TestCaseResult(test_case_id, testcase.name, testcase.url, testcase.data, method, hope_result,
                                                             testcase_time_id, '', '',
                                                             old_sql_value='',
                                                             new_sql_value='',
                                                             old_sql_value_result='',
                                                             new_sql_value_result='', result=time_out_mes,
                                                             scene_id=testcase.testcase_scene_id)
                            # 测试结果实例化
                            db.session.add(testcase_result)
                            db.session.commit()
                        return time_out_mes
    print('testcase.old', testcase.old_sql, testcase.old_sql_id, testcase.old_sql_regist_variable)
    old_sql_value, old_sql_value_result = get_assert_value(testcase, 'old_sql')

    url, data = AnalysisParams().analysis_more_params(testcase.url, testcase.data, testcase_name=testcase.name)

    response_body, regist_variable_value = to_execute_testcase(testcase, url, data)
    # 发送请求

    hope_result = AnalysisParams().analysis_more_params(testcase.hope_result)
    # 结果比较前进行解析期望参数
    testcase_test_result = AssertMethod(actual_result=response_body, hope_result=hope_result).assert_method()

    new_sql_value, new_sql_value_result = get_assert_value(testcase, 'new_sql')

    print('testcase_test_result:', testcase_test_result)
    if testcase_test_result == "测试失败" or old_sql_value_result == "测试失败" or new_sql_value_result == "测试失败":
        test_result = "测试失败"
    else:
        test_result = "测试成功"

    if testcase.wait:
        # 后置等待验证
        print('进入后置等待:', testcase)
        wait = testcase.wait[0]
        time_new_count = 0
        if wait.new_wait_mysql and wait.new_wait and wait.new_wait_sql:
            __hope_result = AnalysisParams().analysis_params(wait.new_wait)
            mysqlrun(mysql_id=wait.new_wait_mysql, sql=wait.new_wait_sql, is_request=False,
                     regist=False, is_cache=True)
            # 先运行一次进行缓存数据，后面每次直接调用
            while 1:
                new_wait_value = mysqlrun(mysql_id=wait.new_wait_mysql, sql=wait.new_wait_sql, is_request=False,
                                          regist=False, cache=True)
                new_wait_assert_result = AssertMethod(actual_result=new_wait_value,
                                                      hope_result=__hope_result).assert_method()
                if new_wait_assert_result == "测试成功":
                    break
                else:
                    print('5s后执行下一次后置验证, 此次查询结果: %s 已执行 %ss  等待超时%s' % (
                    new_wait_value, time_new_count, int(wait.new_wait_time) * 60))
                    time_new_count += 5
                    time.sleep(5)
                if wait.new_wait_time:
                    if time_new_count == int(wait.new_wait_time) * 60:
                        time_out_new_mes = "后置等待超时, 查询结果 %s" % new_wait_value
                        test_result = time_out_new_mes
                        break
    if testcase_time_id:
        testcase_result = TestCaseResult(test_case_id, testcase.name, url, data, method, hope_result,
                                         testcase_time_id, response_body, testcase_test_result, old_sql_value=str(old_sql_value),
                                         new_sql_value=str(new_sql_value), old_sql_value_result=old_sql_value_result,
                                         new_sql_value_result=new_sql_value_result, result=test_result, scene_id=testcase.testcase_scene_id)
        # 测试结果实例化
        db.session.add(testcase_result)
        db.session.commit()
    session.pop(testcase.name)
    if is_run:
        return response_body, regist_variable_value

    return response_body


class TestCaseTimeGet(MethodView):

    def get(self):
        #  获得本次测试批号和是否开启异步场景功能
        print('current_app.name: ', current_app.name)
        user_id = session.get('user_id')
        time_strftime = datetime.now().strftime('%Y%m%d%H%M%S')
        testcase_time = TestCaseStartTimes(time_strftime=time_strftime, user_id=user_id)
        db.session.add(testcase_time)
        db.session.commit()
        print('testcase_time: ', testcase_time)

        scene_async = Variables.query.filter(Variables.name == '_Scene_Async', Variables.user_id == user_id).first().value
        return json.dumps({"testcase_time_id": str(testcase_time.id), 'scene_async': scene_async})


test_case_request_blueprint.add_url_rule('/testcaserequest/', view_func=TestCaseRequest.as_view('test_case_request'))
test_case_request_blueprint.add_url_rule('/testcaserequeststart/', view_func=TestCaseRequestStart.as_view('test_case_request_start'))
test_case_request_blueprint.add_url_rule('/testcasetimeget/', view_func=TestCaseTimeGet.as_view('test_case_time_get'))


def get_assert_value(testcase, value):
    if value == 'old_sql':
        if testcase.old_sql and testcase.old_sql_id:
            if not testcase.old_sql_regist_variable:
                old_sql_regist_variable = ''
            else:
                old_sql_regist_variable = testcase.old_sql_regist_variable
            old_sql_value = mysqlrun(mysql_id=testcase.old_sql_id, sql=testcase.old_sql,
                                     regist_variable=old_sql_regist_variable, is_request=False)
            if testcase.old_sql_hope_result:
                old_sql_value_result = AssertMethod(actual_result=old_sql_value, hope_result=AnalysisParams().analysis_params(testcase.old_sql_hope_result)).assert_method()
            else:
                old_sql_value_result = ''
            print('old_sql_value_result:', old_sql_value_result, old_sql_value)
        else:
            old_sql_value = old_sql_value_result = ''
        return old_sql_value, old_sql_value_result

    elif value == 'new_sql':
        if testcase.new_sql and testcase.new_sql_id:
            if not testcase.new_sql_regist_variable:
                new_sql_regist_variable = ''
            else:
                new_sql_regist_variable = testcase.new_sql_regist_variable
            new_sql_value = mysqlrun(mysql_id=testcase.new_sql_id, sql=testcase.new_sql,
                                     regist_variable=new_sql_regist_variable, is_request=False)
            print('new_sql_regist_variable:', testcase.new_sql_regist_variable)
            if testcase.new_sql_hope_result:
                new_sql_value_result = AssertMethod(actual_result=new_sql_value,
                                                    hope_result=AnalysisParams().analysis_params(
                                                        testcase.new_sql_hope_result)).assert_method()
            else:
                new_sql_value_result = ''
            print('new_sql_value_result:', new_sql_value_result)
        else:
            new_sql_value = new_sql_value_result = ''
        # 调用比较的方法判断响应报文是否满足期望
        return new_sql_value, new_sql_value_result

