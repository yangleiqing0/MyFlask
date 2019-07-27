import os
import sqlite3
import requests
import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request

requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

app.config.from_object(config)

db = SQLAlchemy(app)


# @app.before_first_request
# def create_db():
#
#   conn = sqlite3.connect(config.DATABASE_URL)
#   c = conn.cursor()
#   # 创建表
#   # c.execute('''DROP TABLE IF EXISTS testcases''')
#   c.execute('''CREATE TABLE if not exists case_group(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,descrption TEXT)''')
#   c.execute('''CREATE TABLE if not exists testcases(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,url TEXT,data TEXT,result TEXT,method text,group_id INTEGER,FOREIGN KEY (group_id) REFERENCES case_group(id))''')
#   c.close()
#   conn.close()

class cdb:
    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE_URL)

    def db_cur(self):
        return self.conn.cursor()

    def query_db(self, sql, params=None, one=False):
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

    def opeat_db(self, sql, params):
        try:
            self.cur = self.db_cur()
            self.cur.execute(sql, params)
            self.conn.commit()
        finally:
            self.conn.close()


# cdb().opeat_db('insert into testcases values (?,?,?,?,?)',(None,"yi","dqw","dwq",1))

# @app.route('/testcaselist/')
# def test_case_list():
#     sql = 'select ROWID,id,name,url,data,result,method from testcases'
#     tests = cdb().query_db(sql)
#     return render_template('test_case_list.html', items = tests)


from modles.testcase import TestCases
from modles.case_group import CaseGroup

db.create_all()
from views.testcase import testcase_blueprint  # 不能放在其他位置
from views.home import home_blueprint

app.register_blueprint(testcase_blueprint)
app.register_blueprint(home_blueprint)

if __name__ == '__main__':
    app.debug = True
    app.run()
