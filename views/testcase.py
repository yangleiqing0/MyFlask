import requests
import json
from common.tail_font_log import FrontLogs
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, current_app
from modles.testcase import TestCases
from modles.case_group import CaseGroup
from modles.request_headers import RequestHeaders
from common.analysis_params import AnalysisParams
from app import cdb, db, app

testcase_blueprint = Blueprint('testcase_blueprint', __name__)


class TestCastList(MethodView):

    def get(self):
        # sql = 'select ROWID,id,name,url,data,result,method,group_id from testcases'
        # tests = cdb().query_db(sql)
        # 过滤有测试用例分组的查询结果
        testcases = TestCases.query.join(CaseGroup,TestCases.group_id ==
                                     CaseGroup.id).filter(TestCases.group_id == CaseGroup.id).all()
        # 获取测试用例分组的列表
        print('testcases: ', testcases)

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
        return render_template('test_case_list.html', pagination=pagination, items=testcaseses, case_groups=case_groups,
                               request_headers=request_headers)


class TestCaseAdd(MethodView):

    def get(self):
        case_groups_querys_sql = 'select id,name from case_group'
        case_groups = cdb().query_db(case_groups_querys_sql)
        # print(case_groups, case_groups[0][0])

        request_headers_querys_sql = 'select id,name from request_headers'
        request_headers = cdb().query_db(request_headers_querys_sql)
        print('request_headers: ', request_headers )
        FrontLogs('进入添加测试用例页面').add_to_front_log()
        return render_template('test_case_add.html', case_groups=case_groups,
                               request_headers=request_headers)

    def post(self):
        print('要添加的测试用例：', request.form)
        name = request.form['name']
        url = request.form.get('url', 'default')
        data = request.form.get('data', 'default').replace('/n', '').replace(' ', '')
        method = request.form.get('method', 'default')
        group_id = request.form.get('case_group')
        request_headers_id = request.form.get('request_headers')
        request_headers_query_sql = 'select value from request_headers where id=?'
        headers = json.loads(cdb().query_db(request_headers_query_sql, (request_headers_id,), True)[0])
        print('request_headers_id: %s headers:%s ' % (request_headers_id, headers))

        sql = 'insert into testcases values (?,?,?,?,?,?,?,?)'
        if request.form.get('test', 0) == '测试':
            if method.upper() == 'GET':
                if 'https' in url:
                    result = requests.get(url, headers=headers, verify=False).text
                else:
                    result = requests.get(url, headers=headers).text
            elif method.upper() == 'POST':
                data = AnalysisParams().analysis_params(data)
                print(data)
                if 'https' in url:
                    result = requests.post(url, data=data, headers=headers, verify=False).text
                else:
                    result = requests.get(url, data=data, headers=headers).text
            else:
                result = '请求方法不对'
            return '''%s''' % result.replace('<', '').replace('>', '')
        query_all_names_sql = 'select name from testcases'
        all_names = cdb().query_db(query_all_names_sql)
        print(all_names)
        if (name,) in all_names:
            return '已有相同测试用例名称，请修改'
        else:
            testcase = TestCases(name, url, data, method, group_id, request_headers_id)
            db.session.add(testcase)
            db.session.commit()
            FrontLogs('添加测试用例 name: %s 成功' % name).add_to_front_log()
            app.logger.info('message:insert into testcases success, name: %s' % name)
            return redirect(url_for('testcase_blueprint.test_case_list'))

# class SearchTestCast(MethodView):
#
#     def get(self, id=-1):
#         testcase = TestCases.query.filter(TestCases.id == id).first()
#         print('testcase.group_id:', testcase.group_id)
#         # 获取测试用例分组的列表
#         case_group = CaseGroup.query.filter(CaseGroup.id == testcase.group_id).first()
#         request_headers = RequestHeaders.query.filter(RequestHeaders.id == testcase.request_headers_id).first()
#         print('testcase:', testcase)
#         print('case_group:', case_group)
#         print('request_headers:', request_headers)
#         # return 'o'
#         return render_template('test_case_search.html', item=testcase, case_group=case_group, request_headers=request_headers)


# class PostTestCase(MethodView):
#
#     def post(self):
#         print('要添加的测试用例：', request.form)
#         name = request.form['name']
#         url = request.form.get('url', 'default')
#         data = request.form.get('data', 'default').replace('/n', '').replace(' ', '')
#         method = request.form.get('method', 'default')
#         group_id = request.form.get('case_group')
#         request_headers_id = request.form.get('request_headers')
#         request_headers_query_sql = 'select value from request_headers where id=?'
#         headers = json.loads(cdb().query_db(request_headers_query_sql, (request_headers_id,), True)[0])
#         print('headers: ', headers, type(headers))
#
#         sql = 'insert into testcases values (?,?,?,?,?,?,?,?)'
#         if request.form.get('test', 0) == '测试':
#             if method.upper() == 'GET':
#                 if 'https' in url:
#                     result = requests.get(url, headers=headers, verify=False).text
#                 else:
#                     result = requests.get(url, headers=headers).text
#             elif method.upper() == 'POST':
#                 data = AnalysisParams().analysis_params(data)
#                 print(data)
#                 if 'https' in url:
#                     result = requests.post(url, data=data, headers=headers, verify=False).text
#                 else:
#                     result = requests.get(url, data=data, headers=headers).text
#             else:
#                 result = '请求方法不对'
#             return '''%s''' % result.replace('<', '').replace('>', '')
#         query_all_names_sql = 'select name from testcases'
#         all_names = cdb().query_db(query_all_names_sql)
#         print(all_names)
#         if (name,) in all_names:
#             return '已有相同测试用例名称，请修改'
#         else:
#             cdb().opeat_db(sql, (None, name, url, data, None, method, group_id, request_headers_id))
#             return '插入数据库成功'


class UpdateTestCase(MethodView):

    def get(self, id=-1):
        testcase = TestCases.query.filter(TestCases.id == id).first()
        print('testcase.group_id:', testcase.group_id)
        # 获取测试用例分组的列表
        case_group = CaseGroup.query.filter(CaseGroup.id == testcase.group_id).first()
        request_headers = RequestHeaders.query.filter(RequestHeaders.id == testcase.request_headers_id).first()
        print('testcase:', testcase)
        print('case_group:', case_group)
        print('request_headers:', request_headers)
        FrontLogs('进入编辑测试用例 id: %s 页面' % id).add_to_front_log()
        return render_template('test_case_search.html', item=testcase, case_group=case_group, request_headers=request_headers)

    def post(self, id=-1):
        print('UpdateTestCase：request_form: ', request.form)
        if request.form.get('test', 0) == '测试':
            print('进入测试：')
            url = request.form.get('url', 'default')
            data = request.form.get('data', 'default').replace('/n', '').replace(' ', '')
            data = AnalysisParams().analysis_params(data)
            print('测试：', data)
            method = request.form.get('method', 'default')
            request_headers_query_sql = 'select request_headers.value from request_headers,testcases where testcases.request_headers_id=request_headers.id and testcases.id=?'
            print("query_headers_value: ", cdb().query_db(request_headers_query_sql, (id,), True)[0])
            headers = json.loads(cdb().query_db(request_headers_query_sql, (id,), True)[0])
            print('UpdataTestCase:headers: ', headers)
            if method.upper() == 'GET':
                if 'https' in url:
                    result = requests.get(url, headers=headers, verify=False).text
                else:
                    result = requests.get(url, headers=headers).text
            elif method.upper() == 'POST':
                if 'https' in url:
                    result = requests.post(url, data=data, headers=headers, verify=False).text
                else:
                    result = requests.get(url, data=data, headers=headers).text
            else:
                result = '请求方法不对'
            return '''%s''' % result.replace('<', '').replace('>', '')
        name = request.form.get('name')
        url = request.form.get('url')
        data = request.form.get('data')
        method = request.form.get('method')
        update_test_case_sql = 'update testcases set name=?,url=?,data=?,method=? where id=?'
        cdb().opeat_db(update_test_case_sql, (name, url, data, method, id))
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


testcase_blueprint.add_url_rule('/testcaselist/', view_func=TestCastList.as_view('test_case_list'))
testcase_blueprint.add_url_rule('/addtestcase/', view_func=TestCaseAdd.as_view('add_test_case'))
# testcase_blueprint.add_url_rule('/posttestcase/', view_func=PostTestCase.as_view('post_test_case'),)
testcase_blueprint.add_url_rule('/deletetestcase/<id>/', view_func=DeleteTestCase.as_view('delete_test_case'))
testcase_blueprint.add_url_rule('/updatetestcase/<id>/', view_func=UpdateTestCase.as_view('update_test_case'))
# testcase_blueprint.add_url_rule('/searchtestcase/<id>/', view_func=SearchTestCast.as_view('search_test_case'))