import os
import sqlite3
import requests
from flask import Flask,render_template, redirect,url_for,request
requests.packages.urllib3.disable_warnings()



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.path.join(os.path.split(os.path.realpath(__file__))[0],'db\\test.sqlite')
print(DATABASE_URL)
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# UPLOAD_FORLER = os.path.join(os.path.split(os.path.realpath(__file__))[0],'uploads')
# ALLOWED_EXTENSIONS=['.jpg', '.png', '.gif']   #允许上传的文件类型
app.secret_key = 'asldfwadadw@fwq@#!Eewew'
# db = SQLAlchemy(app)
# db.create_all()
class cdb:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_URL)

    def db_cur(self):
        return self.conn.cursor()

    def query_db(self,sql,params=None, one=False):
        try:
            self.cur = self.db_cur()
            if params:
                self.re = self.cur.execute(sql, params)
            else:
                self.re = self.cur.execute(sql)
            if one:
                self.result = self.re.fetchone()
            else:
                self.result = self.re.fetchall()
            return self.result
        finally:
            self.cur.close()
            self.conn.close()

    def opeat_db(self,sql,params):
        try:
            self.cur = self.db_cur()
            self.cur.execute(sql,params)
            self.conn.commit()
        finally:
            self.conn.close()
# cdb().opeat_db('insert into testcases values (?,?,?,?,?)',(None,"yi","dqw","dwq",1))


@app.route('/')
def hello_world():
    return redirect(url_for('test_case_list'))

@app.route('/index/')
def home():
    return render_template('homepage.html')
    
    
@app.route('/testcaselist/')
def test_case_list():
    sql = 'select ROWID,id,name,url,data,result,method from testcases'
    tests = cdb().query_db(sql)
    return render_template('test_case_list.html', items = tests)


@app.route('/addtestcase/')
def test_case_add():
    return render_template('test_case_add.html')


@app.route('/post_test_case/<id>/', methods=['POST', 'GET'])
def post_test_case(id=-1):
    print(id)
    if request.method.upper() == 'POST':
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json, text/plain, */*'
        }
        name = request.form['name']
        url = request.form.get('url', 'default')
        data = request.form.get('data', 'default').replace('/n', '').replace(' ', '')
        method = request.form.get('method', 'default')
        print(request.form)
        sql = 'insert into testcases values (?,?,?,?,?,?)'
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
    elif request.method.upper() == 'GET':
        print('here')
        sql = 'select name,url,data,method,result from testcases where id=(?)'
        testcase = cdb().query_db(sql, (id,), True)
        print(testcase)
        # return 'o'
        return render_template('test_case_search.html', items=testcase)
    return 'OK'

@app.route('/delete_test_case/<id>/')
def delete_test_case(id=0):
    print('删除测试用例')
    delete_test_case_sql = 'delete from testcases where id=(?)'
    cdb().opeat_db(delete_test_case_sql,(id,))
    return redirect(url_for('test_case_list'))




if __name__ == '__main__':
    app.debug = True
    app.run()
