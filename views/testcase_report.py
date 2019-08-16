import os
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, send_from_directory
from modles.variables import Variables
from modles.testcase_start_times import TestCaseStartTimes
from modles.testcase_result import TestCaseResult
from modles.testcase_scene import TestCaseScene
from modles.testcase import TestCases
from common.tail_font_log import FrontLogs
from app import db
from common.connect_sqlite import cdb
from common.do_report import test_report
from datetime import datetime
from common.analysis_params import AnalysisParams


testcase_report_blueprint = Blueprint('testcase_report_blueprint', __name__)


class EnvMessage:

    def __init__(self, testcase_results, testcase_time_id, testcase_time, testcase_scene_list):
        self.testcase_scene_list = testcase_scene_list
        self.test_name = Variables.query.filter(Variables.name == '_TEST_NAME').first().value
        self.zdbm_version = Variables.query.filter(Variables.name == '_TEST_VERSION').first().value
        self.test_pl = Variables.query.filter(Variables.name == '_TEST_PL').first().value
        self.test_net = Variables.query.filter(Variables.name == '_TEST_NET').first().value
        self.title_name = Variables.query.filter(Variables.name == '_TITLE_NAME').first().value
        self.fail_sum = self.count_success_testcase_scene(testcase_time_id) + self.count_testcase_fail(testcase_time_id)
        self.test_sum = len(testcase_results) + len(testcase_scene_list)
        self.test_success = self.test_sum - self.fail_sum
        self.time_strftime = testcase_time.time_strftime
        self.score = int(self.test_success * 100 / self.test_sum)

    def count_success_testcase_scene(self, testcase_time_id):
        fail_count = 0
        for testcase_scene in self.testcase_scene_list:
            for testcase in testcase_scene.testcases:
                print('testcase.testcase_result: ', testcase)
                testcase_result = TestCaseResult.query.filter(
                    TestCaseResult.testcase_id==testcase.id, TestCaseResult.testcase_start_time_id==testcase_time_id).first().testcase_test_result
                if testcase_result == "测试失败":
                    fail_count += 1
                    break
        return fail_count

    @staticmethod
    def count_testcase_fail(testcase_time_id):
        count = TestCaseResult.query.join(TestCases, TestCaseResult.testcase_id == TestCases.id).filter(
            TestCaseResult.testcase_start_time_id == testcase_time_id, TestCases.testcase_scene_id.is_(None),
            TestCaseResult.testcase_test_result == "测试失败").count()
        return count


class Test:

    def __init__(self, testcase_result):
        print('Test :', testcase_result)

        self.t_name, self.url, self.request_body, self.hope = AnalysisParams().\
            analysis_more_params(testcase_result[0], testcase_result[1], testcase_result[3], testcase_result[5])
        print('self.t_name: ', self.t_name)

        self.method, self.response_body, self.old_database_value, self.new_database_value, self.result \
            = testcase_result[2], testcase_result[4], testcase_result[6], testcase_result[7], testcase_result[8]

        try:
            self.scene_id = testcase_result[9]
        except Exception:
            pass


class Testcaseresult:

    def __init__(self, testcase_time_id, result="testcases"):
        self.testcase_time = TestCaseStartTimes.query.get(testcase_time_id)
        print('testcase_time_id: ', testcase_time_id, self.testcase_time)

        if result == 'testcases':
            testcase_results_query_sql = 'select test_case_result.testcase_name,test_case_result.testcase_url,' \
                                         'test_case_result.testcase_method,test_case_result.testcase_data,' \
                                         'test_case_result.response_body,test_case_result.' \
                                         'testcase_hope_result,test_case_result.' \
                                         'old_sql_value,test_case_result.new_sql_value,test_case_result.' \
                                         'testcase_test_result from testcases,test_case_result where testcases.id=' \
                                         'test_case_result.testcase_id and testcases.testcase_scene_id isnull and ' \
                                         'test_case_result.testcase_start_time_id=%s' \
                                         % testcase_time_id
            self.testcase_results = cdb().query_db(testcase_results_query_sql)
            print('self.testcase_results:', self.testcase_results)

        elif result == 'scene_testcases':
            testcase_results_query_sql = 'select test_case_result.testcase_name,test_case_result.testcase_url,' \
                                         'test_case_result.testcase_method,test_case_result.testcase_data,' \
                                         'test_case_result.response_body,test_case_result.testcase_hope_result,' \
                                         'test_case_result.old_sql_value,test_case_result.new_sql_value,' \
                                         'test_case_result.testcase_test_result,testcases.testcase_scene_id' \
                                         ' from testcases, test_case_result ' \
                                         'where testcases.id=test_case_result.testcase_id and ' \
                                         'testcases.testcase_scene_id not null and ' \
                                         'test_case_result.testcase_start_time_id=%s' \
                                         % testcase_time_id
            self.testcase_results = cdb().query_db(testcase_results_query_sql)

            print('self.testcase_results:', self.testcase_results)


class TestCaseReport(MethodView):

    def get(self):
        testcase_time_id = request.args.get('testcase_time_id')
        testcase_results = Testcaseresult(testcase_time_id).testcase_results
        testcase_time = TestCaseStartTimes.query.get(testcase_time_id)
        print('testcase_results: ', testcase_results, len(testcase_results))
        items = []
        for testcase_result in testcase_results:
            items.append(Test(testcase_result))
        print('items: ', items)

        testcase_scene_results = Testcaseresult(testcase_time_id, result="scene_testcases").testcase_results
        testcase_scene_ids = []
        print('testcase_scene_results: ', testcase_scene_results, len(testcase_scene_results))
        testcase_scene_testcases_after_list = []
        for testcase_scene_result in testcase_scene_results:
            testcase_scene_ids.append(testcase_scene_result[9])
            testcase_scene_testcases_after_list.append(Test(testcase_scene_result))
        testcase_scene_ids = set(testcase_scene_ids)
        testcase_scene_list = []
        print('testcase_scene_testcases_after_list:', testcase_scene_testcases_after_list)
        print('testcase_scene_list: ', testcase_scene_ids)
        for testcase_scene_id in testcase_scene_ids:
            print('testcase_scene_id: ', testcase_scene_id)
            testcase_scene = TestCaseScene.query.get(testcase_scene_id)
            fail_count = 0
            for testcase in testcase_scene.testcases:
                print('testcase_scene_ids testcase: ', testcase)
                testcase_result = TestCaseResult.query.filter(TestCaseResult.testcase_id==testcase.id,
                                                              TestCaseResult.testcase_start_time_id==testcase_time_id).first().testcase_test_result
                print('testcase_scene_ids testcase_result: ', testcase_result, testcase)
                if testcase_result == "测试失败":
                    fail_count += 1
            if fail_count == 0:
                testcase_scene.result = "测试成功"
            else:
                testcase_scene.result = "测试失败"
            testcase_scene_list.append(testcase_scene)
            testcase_scene_testcases = []
            for testcase_scene_testcase in testcase_scene_testcases_after_list:
                if testcase_scene_testcase.scene_id == testcase_scene.id:
                    testcase_scene_testcases.append(testcase_scene_testcase)
                print('testcase_scene_testcases:', testcase_scene_testcases)
                testcase_scene.test_cases = testcase_scene_testcases
            for a in testcase_scene_list:
                print('测试结果： ', a.result, a)
        print("TestCaseReport testcase_scene_list:", testcase_scene_list,)
        allocation = EnvMessage(testcase_results, testcase_time_id, testcase_time, testcase_scene_list)
        FrontLogs('进入测试用例执行页面 执行id: %s' % testcase_time_id).add_to_front_log()
        return render_template("testcase_report/testcase_report.html", items=items, allocation=allocation,
                               testcase_scene_list=testcase_scene_list)

    def post(self):
        testcase_time_id = request.args.get('testcase_time_id')
        time_strftime = datetime.now().strftime('%Y%m%d%H%M%S')
        testcase_report_name = Variables.query.filter(Variables.name =="_TEST_REPORT_EXCEL_NAME").first().value + "_" + \
                               time_strftime + ".xlsx"
        REPORT_FILE_PATH = Variables.query.filter(Variables.name == "_REPORT_FILE_PATH").first().value
        Filename = REPORT_FILE_PATH + testcase_report_name
        print("Filename: ", Filename)
        test_case_start_time = TestCaseStartTimes().query.get(testcase_time_id)
        test_case_start_time.filename = Filename
        test_case_start_time.name = testcase_report_name
        db.session.commit()
        test_report(testcase_time_id)  # 生成测试报告

        testcase_results = Testcaseresult(testcase_time_id).testcase_results
        testcase_time = TestCaseStartTimes.query.get(testcase_time_id)
        print('testcase_results: ', testcase_results, len(testcase_results))
        items = []
        for testcase_result in testcase_results:
            items.append(Test(testcase_result))
        print('items: ', items)

        testcase_scene_results = Testcaseresult(testcase_time_id, result="scene_testcases").testcase_results
        testcase_scene_ids = []
        print('testcase_scene_results: ', testcase_scene_results, len(testcase_scene_results))
        testcase_scene_testcases_after_list = []
        for testcase_scene_result in testcase_scene_results:
            testcase_scene_ids.append(testcase_scene_result[9])
            testcase_scene_testcases_after_list.append(Test(testcase_scene_result))
        testcase_scene_ids = set(testcase_scene_ids)
        testcase_scene_list = []
        print('testcase_scene_testcases_after_list:', testcase_scene_testcases_after_list)
        print('testcase_scene_list: ', testcase_scene_ids)
        for testcase_scene_id in testcase_scene_ids:
            print('testcase_scene_id: ', testcase_scene_id)
            testcase_scene = TestCaseScene.query.get(testcase_scene_id)
            testcase_scene_list.append(testcase_scene)
            testcase_scene_testcases = []
            for testcase_scene_testcase in testcase_scene_testcases_after_list:
                if testcase_scene_testcase.scene_id == testcase_scene.id:
                    testcase_scene_testcases.append(testcase_scene_testcase)
                print('testcase_scene_testcases:', testcase_scene_testcases)
                testcase_scene.test_cases = testcase_scene_testcases
        print("TestCaseReport testcase_scene_list:", testcase_scene_list)
        allocation = EnvMessage(testcase_results, testcase_time_id, testcase_time, testcase_scene_list)

        FrontLogs('进入测试报告页面 报告id: %s' % testcase_time_id).add_to_front_log()
        # return items, Allocation
        return render_template("testcase_report/testcase_report.html", items=items, allocation=allocation,
                               testcase_scene_list=testcase_scene_list)


class TestCaseReportList(MethodView):

    def get(self):
        testcase_reports = TestCaseStartTimes.query.filter(TestCaseStartTimes.name != "").order_by(TestCaseStartTimes.timestamp.desc()).all()
        print('testcase_reports: ', testcase_reports)
        FrontLogs('进入测试报告列表页面').add_to_front_log()
        return render_template('testcase_report/testcase_report_list.html', items=testcase_reports)


class TestCaseReportDelete(MethodView):

    def get(self, id=-1):
        testcase_time_id = request.args.get('id', id)
        testcase_report = TestCaseStartTimes.query.get(testcase_time_id)
        testcase_results = testcase_report.this_time_testcase_result
        print('testcase_report: ', testcase_report, id)
        db.session.delete(testcase_report)
        db.session.commit()
        try:
            for testcase_result in testcase_results:
                db.session.delete(testcase_result)
                db.session.commit()
            os.remove(testcase_report.filename)
        except FileNotFoundError:
            pass
        FrontLogs('删除测试报告 id: %s 成功' % testcase_time_id).add_to_front_log()
        # app.logger.info('message:delete testcase_report success, id: %s' % id)
        return redirect(url_for('testcase_report_blueprint.testcase_report_list'))


class TestCaseReportDownLoad(MethodView):

    def get(self, name):
        download_path = TestCaseStartTimes.query.filter(TestCaseStartTimes.name == name).first().filename.replace(name, '')
        print('download_path:', download_path)
        dirpath = os.path.join(app.root_path, download_path)  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
        print('dirpath:', dirpath)
        FrontLogs('下载测试报告 测试报告名称: %s ' % name).add_to_front_log()
        return send_from_directory(dirpath, name, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载


testcase_report_blueprint.add_url_rule('/testcasereport/', view_func=TestCaseReport.as_view('testcase_report'))
testcase_report_blueprint.add_url_rule('/testcasereportlist/', view_func=TestCaseReportList.as_view('testcase_report_list'))
testcase_report_blueprint.add_url_rule('/testcasereportdelete/', view_func=TestCaseReportDelete.as_view('testcase_report_delete'))
testcase_report_blueprint.add_url_rule('/testcasereportdownload/<path:name>', view_func=TestCaseReportDownLoad.as_view('testcase_report_download'))




