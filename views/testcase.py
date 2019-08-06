import requests
import json
from common.tail_font_log import FrontLogs
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, current_app, jsonify
from modles.testcase import TestCases
from modles.case_group import CaseGroup
from modles.request_headers import RequestHeaders
from common.analysis_params import AnalysisParams
from app import cdb, db, app
from common.method_request import MethodRequest

testcase_blueprint = Blueprint('testcase_blueprint', __name__)


class TestCastList(MethodView):

    def get(self):
        # sql = 'select ROWID,id,name,url,data,result,method,group_id from testcases'
        # tests = cdb().query_db(sql)
        # 过滤有测试用例分组的查询结果
        testcases = TestCases.query.join(CaseGroup, TestCases.group_id ==
                                     CaseGroup.id).filter(TestCases.group_id == CaseGroup.id).all()
        # 获取测试用例分组的列表
        print('testcases: ', testcases)
        for testcase in testcases:
            testcase.name = AnalysisParams().analysis_params(testcase.name)
            testcase.url = AnalysisParams().analysis_params(testcase.url)
            testcase.data = AnalysisParams().analysis_params(testcase.data)
        case_groups = CaseGroup.query.all()
        print('case_groups: ', case_groups)
        request_headers = RequestHeaders.query.all()
        print('request_headers: ', request_headers)
        page = request.args.get('page', 1, type=int)
        #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
        pagination = TestCases.query.order_by(TestCases.timestamp.desc()).paginate(page, per_page=current_app.config[
            'FLASK_POST_PRE_ARGV'], error_out=False)
        # 返回一个内容对象
        testcaseses = pagination.items
        print("pagination: ", pagination)
        FrontLogs('进入测试用例列表页面 第%s页' % page).add_to_front_log()
        return render_template('test_case/test_case_list.html', pagination=pagination, items=testcaseses, case_groups=case_groups,
                               request_headers=request_headers)


class TestCaseAdd(MethodView):

    def get(self):
        case_groups_querys_sql = 'select id,name from case_group'
        case_groups = cdb().query_db(case_groups_querys_sql)

        request_headers_querys_sql = 'select id,name from request_headers'
        request_headers = cdb().query_db(request_headers_querys_sql)
        print('request_headers: ', request_headers )
        FrontLogs('进入添加测试用例页面').add_to_front_log()
        return render_template('test_case/test_case_add.html', case_groups=case_groups,
                               request_headers=request_headers)

    def post(self):
        print('要添加的测试用例：', request.form)
        name = request.form['name']
        url = request.form.get('url', 'default')
        data = request.form.get('data', 'default').replace('/n', '').replace(' ', '')
        method = request.form.get('method', 'default')
        group_id = request.form.get('case_group')
        regist_variable = request.form.get('regist_variable', None)
        regular = request.form.get('regular', None)
        request_headers_id = request.form.get('request_headers')
        request_headers_query_sql = 'select value from request_headers where id=?'
        request_headers = cdb().query_db(request_headers_query_sql, (request_headers_id,), True)[0]
        print('TestCaseAdd request_headers before: ', request_headers)
        request_headers = AnalysisParams().analysis_params(request_headers, is_change="headers")
        print('TestCaseAdd request_headers: ', request_headers)
        headers = json.loads(request_headers)
        print('request_headers_id: %s headers:%s ' % (request_headers_id, headers))
        if request.form.get('test', 0) == '测试':
            url = AnalysisParams().analysis_params(url)
            result = MethodRequest().request_value(method, url, data, headers)
            return '''%s''' % result.replace('<', '').replace('>', '')
        query_all_names_sql = 'select name from testcases'
        all_names = cdb().query_db(query_all_names_sql)
        print(all_names)
        if (name,) in all_names:
            return '已有相同测试用例名称，请修改'
        else:
            testcase = TestCases(name, url, data, regist_variable, regular, method, group_id, request_headers_id)
            db.session.add(testcase)
            db.session.commit()
            FrontLogs('添加测试用例 name: %s 成功' % name).add_to_front_log()
            app.logger.info('message:insert into testcases success, name: %s' % name)
            return redirect(url_for('testcase_blueprint.test_case_list'))


class UpdateTestCase(MethodView):

    def get(self, id=-1):
        testcase = TestCases.query.filter(TestCases.id == id).first()
        print('testcase.group_id:', testcase.group_id)
        # 获取测试用例分组的列表
        case_groups = CaseGroup.query.all()
        case_group_id_before = testcase.group_id
        request_headers_id_before = testcase.request_headers_id
        request_headerses = RequestHeaders.query.all()
        print('testcase:', testcase)
        print('case_groups :', case_groups)
        print('request_headerses:', request_headerses)
        FrontLogs('进入编辑测试用例 id: %s 页面' % id).add_to_front_log()
        return render_template('test_case/test_case_search.html', item=testcase, case_groups=case_groups,
                               request_headers_id_before=request_headers_id_before, case_group_id_before=case_group_id_before,
                               request_headerses=request_headerses)

    def post(self, id=-1):
        print('UpdateTestCase：request_form: ', request.form)
        name = request.form.get('name')
        url = request.form.get('url')
        data = request.form.get('data')
        method = request.form.get('method')
        group_id = request.form.get('case_group')
        request_headers_id = request.form.get('request_headers')
        regist_variable = request.form.get('regist_variable', '')
        regular = request.form.get('regular', '')
        id = request.args.get('id', id)
        print('UpdateTestCase: id', id)
        if request.form.get('test', 0) == '测试':
            print('进入测试：')
            url = AnalysisParams().analysis_params(url)
            data = AnalysisParams().analysis_params(data.replace('/n', '').replace(' ', ''))
            print('测试：', name, data, method, url, group_id, request_headers_id, regist_variable, regular, id)
            request_headers_value_sql = 'select value from request_headers where id=?'
            query_headers_value = cdb().query_db(request_headers_value_sql, (request_headers_id,), True)[0]
            print("query_headers_value: ", query_headers_value)
            headers = json.loads(AnalysisParams().analysis_params(query_headers_value, is_change="headers"))
            print('UpdataTestCase:headers: ', headers, url, method, data)
            result = MethodRequest().request_value(method, url, data, headers)
            print('UpdataTestCase TEST: 响应报文: %s' % result)
            return '''%s''' % result.replace('<', '').replace('>', '')
        update_test_case_sql = 'update testcases set name=?,url=?,data=?,method=?,group_id=?,' \
                               'request_headers_id=?,regist_variable=?,regular=? where id=?'
        cdb().opeat_db(update_test_case_sql, (name, url, data, method, group_id,
                                              request_headers_id, regist_variable, regular, id))
        FrontLogs('编辑测试用例 name: %s 成功' % name).add_to_front_log()
        app.logger.info('message:update testcases success, name: %s' % name)
        return redirect(url_for('testcase_blueprint.test_case_list'))


class DeleteTestCase(MethodView):

    def get(self,id=-1):
        delete_test_case_sql = 'delete from testcases where id=?'
        cdb().opeat_db(delete_test_case_sql, (id,))
        FrontLogs('删除测试用例 id: %s 成功' % id).add_to_front_log()
        app.logger.info('message:delete testcases success, id: %s' % id)
        return redirect(url_for('testcase_blueprint.test_case_list'))

class TestCaseValidata(MethodView):

    def get(self):
        name = request.args.get('name')
        testcase = TestCases.query.filter(TestCases.name == name).count()
        if testcase != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class TestCaseUpdateValidata(MethodView):

    def get(self):
        name = request.args.get('name')
        testcase_id = request.args.get('testcase_id')
        testcase = TestCases.query.filter(TestCases.id != testcase_id).filter(TestCases.name == name).count()
        if testcase != 0:
            return jsonify(False)
        else:
            return jsonify(True)



testcase_blueprint.add_url_rule('/testcaselist/', view_func=TestCastList.as_view('test_case_list'))
testcase_blueprint.add_url_rule('/addtestcase/', view_func=TestCaseAdd.as_view('add_test_case'))
# testcase_blueprint.add_url_rule('/posttestcase/', view_func=PostTestCase.as_view('post_test_case'),)
testcase_blueprint.add_url_rule('/deletetestcase/<id>/', view_func=DeleteTestCase.as_view('delete_test_case'))
testcase_blueprint.add_url_rule('/updatetestcase/<id>/', view_func=UpdateTestCase.as_view('update_test_case'))
# testcase_blueprint.add_url_rule('/searchtestcase/<id>/', view_func=SearchTestCast.as_view('search_test_case'))

testcase_blueprint.add_url_rule('/testcasevalidate/', view_func=TestCaseValidata.as_view('testcase_validate'))
testcase_blueprint.add_url_rule('/testcaseupdatevalidate/', view_func=TestCaseUpdateValidata.as_view('testcase_update_validate'))
