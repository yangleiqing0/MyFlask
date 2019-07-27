import os
import sqlite3
import requests
import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request

requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

app.config.from_object(config)
app.debug = True
db = SQLAlchemy(app)


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




from modles.testcase import TestCases
from modles.case_group import CaseGroup
from modles.variables import Variables
db.create_all()
from views.testcase import testcase_blueprint  # 不能放在其他位置
from views.home import home_blueprint
from views.case_group import case_group_blueprint
from views.variables import variables_blueprint

app.register_blueprint(testcase_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(case_group_blueprint)
app.register_blueprint(variables_blueprint)

if __name__ == '__main__':
    app.run()
