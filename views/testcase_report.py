import os
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, send_from_directory
from modles.variables import Variables
from modles.testcase_start_times import TestCaseStartTimes
from modles.testcase_result import TestCaseResult
from common.tail_font_log import FrontLogs
from app import cdb, db, app
from common.do_report import test_report
from datetime import datetime
from common.analysis_params import AnalysisParams


testcase_report_blueprint = Blueprint('testcase_report_blueprint', __name__)


class TestCaseReport(MethodView):

    def get(self):
        testcase_time_id = request.args.get('testcase_time_id')
        testcase_time = TestCaseStartTimes.query.get(testcase_time_id)
        print('testcase_time_id: ', testcase_time_id, testcase_time)
        testcase_results_query_sql = 'select testcases.name,testcases.url,testcases.method,testcases.data,test_case_result.response_body,' \
                                     ' testcases.hope_result,test_case_result.old_sql_value,test_case_result.new_sql_value,' \
                                     'test_case_result.testcase_test_result' \
                                     ' from testcases,test_case_result where testcases.id=test_case_result.testcase_id ' \
                                     'and test_case_result.testcase_start_time_id=%s' % testcase_time_id
        testcase_results = cdb().query_db(testcase_results_query_sql)
        print('testcase_results: ', testcase_results, len(testcase_results))
        items = []
        for testcase_result in testcase_results:
            Test = type('Test', (object,), dict(a=-1))  # 需要创建两次对象  否则共用同一个对象的列表指向
            t_name = Test.name = AnalysisParams().analysis_params(testcase_result[0])
            print(Test.name, t_name)
            Test.url = AnalysisParams().analysis_params(testcase_result[1])
            Test.method = testcase_result[2]
            Test.request_body = AnalysisParams().analysis_params(testcase_result[3])
            Test.response_body = testcase_result[4]
            Test.hope = AnalysisParams().analysis_params(testcase_result[5])
            Test.old_database_value = testcase_result[6]
            Test.new_database_value = testcase_result[7]
            Test.result = testcase_result[8]
            items.append(Test())
        print('items: ', items[0].response_body)

        Allocation = type('Allocation', (object,), dict(a=-1))
        Allocation.test_name = Variables.query.filter(Variables.name == '_TEST_NAME').first().value
        Allocation.zdbm_version = Variables.query.filter(Variables.name == '_TEST_VERSION').first().value
        Allocation.test_pl = Variables.query.filter(Variables.name == '_TEST_PL').first().value
        Allocation.test_net = Variables.query.filter(Variables.name == '_TEST_NET').first().value
        Allocation.title_name = Variables.query.filter(Variables.name == '_TITLE_NAME').first().value
        Allocation.test_sum = len(testcase_results)
        Allocation.test_success = TestCaseResult.query.filter(TestCaseResult.testcase_test_result == "测试成功",
                                                              TestCaseResult.testcase_start_time_id == testcase_time_id).count()
        Allocation.time_strftime = testcase_time.time_strftime
        Allocation.fail_sum = len(testcase_results) - Allocation.test_success
        Allocation.score = int(Allocation.test_success * 100 / Allocation.test_sum)

        Allocation()
        return render_template("testcase_report/testcase_report.html", items=items, allocation=Allocation)

    def post(self):
        testcase_time_id = request.args.get('testcase_time_id')
        time_strftime = datetime.now().strftime('%Y%m%d%H%M%S')
        testcase_report_name = Variables.query.filter(Variables.name=="_TEST_REPORT_EXCEL_NAME").first().value + "_" + \
                               time_strftime + ".xlsx"
        REPORT_FILE_PATH = Variables.query.filter(Variables.name=="_REPORT_FILE_PATH").first().value
        Filename = REPORT_FILE_PATH + testcase_report_name
        print("Filename: ", Filename)
        test_case_start_time = TestCaseStartTimes().query.get(testcase_time_id)
        test_case_start_time.filename = Filename
        test_case_start_time.name = testcase_report_name
        db.session.commit()
        test_report(testcase_time_id)  # 生成测试报告

        testcase_time = TestCaseStartTimes.query.get(testcase_time_id)
        print('testcase_time_id: ', testcase_time_id, testcase_time)
        testcase_results_query_sql = 'select testcases.name,testcases.url,testcases.method,testcases.data,test_case_result.response_body,' \
                                     ' testcases.hope_result,test_case_result.old_sql_value,test_case_result.new_sql_value,' \
                                     'test_case_result.testcase_test_result' \
                                     ' from testcases,test_case_result where testcases.id=test_case_result.testcase_id ' \
                                     'and test_case_result.testcase_start_time_id=%s' % testcase_time_id
        testcase_results = cdb().query_db(testcase_results_query_sql)
        print('testcase_results: ', testcase_results, len(testcase_results))
        items = []
        for testcase_result in testcase_results:
            Test = type('Test', (object,), dict(a=-1)) #需要创建两次对象  否则共用同一个对象的列表指向
            t_name = Test.name = AnalysisParams().analysis_params(testcase_result[0])
            print(Test.name, t_name)
            Test.url = AnalysisParams().analysis_params(testcase_result[1])
            Test.method = testcase_result[2]
            Test.request_body = AnalysisParams().analysis_params(testcase_result[3])
            Test.response_body = testcase_result[4]
            Test.hope = AnalysisParams().analysis_params(testcase_result[5])
            Test.old_database_value = testcase_result[6]
            Test.new_database_value = testcase_result[7]
            Test.result = testcase_result[8]
            items.append(Test())
        print(items)

        Allocation = type('Allocation', (object,), dict(a=-1))
        Allocation.test_name = Variables.query.filter(Variables.name == '_TEST_NAME').first().value
        Allocation.zdbm_version = Variables.query.filter(Variables.name == '_TEST_VERSION').first().value
        Allocation.test_pl = Variables.query.filter(Variables.name == '_TEST_PL').first().value
        Allocation.test_net = Variables.query.filter(Variables.name == '_TEST_NET').first().value
        Allocation.title_name = Variables.query.filter(Variables.name == '_TITLE_NAME').first().value
        Allocation.test_sum = len(testcase_results)
        Allocation.test_success = TestCaseResult.query.filter(TestCaseResult.testcase_test_result == "测试成功",
                                                   TestCaseResult.testcase_start_time_id == testcase_time_id).count()
        Allocation.time_strftime = testcase_time.time_strftime
        Allocation.fail_sum = len(testcase_results) - Allocation.test_success
        Allocation.score = int(Allocation.test_success * 100 / Allocation.test_sum)

        Allocation()
        return render_template("testcase_report/testcase_report.html", items=items, allocation=Allocation)


class TestCaseReportList(MethodView):

    def get(self):
        testcase_reports = TestCaseStartTimes.query.filter(TestCaseStartTimes.name != "").order_by(TestCaseStartTimes.timestamp.desc()).all()
        print('testcase_reports: ', testcase_reports)
        return render_template('testcase_report/testcase_report_list.html', items=testcase_reports)


class TestCaseReportDelete(MethodView):

    def get(self, id=-1):
        testcase_time_id = request.args.get('id', id)
        testcase_report = TestCaseStartTimes.query.get(testcase_time_id)
        print('testcase_report: ', testcase_report, id)
        db.session.delete(testcase_report)
        db.session.commit()
        try:
            os.remove(testcase_report.filename)
        except FileNotFoundError:
            pass
        FrontLogs('删除测试报告 id: %s 成功' % testcase_time_id).add_to_front_log()
        app.logger.info('message:delete testcase_report success, id: %s' % id)
        return redirect(url_for('testcase_report_blueprint.testcase_report_list'))


class TestCaseReportDownLoad(MethodView):

    def get(self, name):
        download_path = TestCaseStartTimes.query.filter(TestCaseStartTimes.name == name).first().filename.replace(name, '')
        print('download_path:', download_path)
        dirpath = os.path.join(app.root_path, download_path)  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
        print('dirpath:', dirpath)
        return send_from_directory(dirpath, name, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载

testcase_report_blueprint.add_url_rule('/testcasereport/', view_func=TestCaseReport.as_view('testcase_report'))
testcase_report_blueprint.add_url_rule('/testcasereportlist/', view_func=TestCaseReportList.as_view('testcase_report_list'))
testcase_report_blueprint.add_url_rule('/testcasereportdelete/', view_func=TestCaseReportDelete.as_view('testcase_report_delete'))
testcase_report_blueprint.add_url_rule('/testcasereportdownload/<path:name>', view_func=TestCaseReportDownLoad.as_view('testcase_report_download'))




