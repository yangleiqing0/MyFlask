import requests
from flask.views import MethodView
from flask import render_template,Blueprint,request,redirect,url_for
from modles.testcase import TestCases
from app import cdb

testcase_blueprint = Blueprint('testcase_blueprint', __name__)


class TestCastList(MethodView):

    def get(self):
        sql = 'select ROWID,id,name,url,data,result,method from testcases'
        tests = cdb().query_db(sql)
        return render_template('test_case_list.html', items=tests)


class TestCaseAdd(MethodView):

    def get(self):
        return render_template('test_case_add.html')


class PostTestCase(MethodView):
    def get(self, id=-1):
        print('here')
        sql = 'select name,url,data,method,result from testcases where id=(?)'
        testcase = cdb().query_db(sql, (id,), True)
        print(testcase)
        # return 'o'
        return render_template('test_case_search.html', items=testcase)

    def post(self, id=-1):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json, text/plain, */*'
        }
        name = request.form['name']
        url = request.form.get('url', 'default')
        data = request.form.get('data', 'default').replace('/n', '').replace(' ', '')
        method = request.form.get('method', 'default')
        print(request.form)
        sql = 'insert into testcases values (?,?,?,?,?,?,?)'
        if request.form.get('test', 0) == '测试':
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
        query_all_names_sql = 'select name from testcases'
        all_names = cdb().query_db(query_all_names_sql)
        print(all_names)
        if (name,) in all_names:
            return '已有相同测试用例名称，请修改'
        else:
            cdb().opeat_db(sql, (None, name, url, data, None, method))
            return '插入数据库成功'


class DeleteTestCase(MethodView):
    id = -1
    def post(self):
        print('删除测试用例')
        delete_test_case_sql = 'delete from testcases where id=(?)'
        cdb().opeat_db(delete_test_case_sql, (id,))
        return redirect(url_for('test_case_list'))


testcase_blueprint.add_url_rule('/testcaselist/', view_func=TestCastList.as_view('test_case_list'))
testcase_blueprint.add_url_rule('/addtestcase/', view_func=TestCaseAdd.as_view('add_test_case'))
testcase_blueprint.add_url_rule('/posttestcase/<id>/', view_func=PostTestCase.as_view('post_test_case'),)
testcase_blueprint.add_url_rule('/deletetestcase/<id>/', view_func=DeleteTestCase.as_view('delete_test_case'))