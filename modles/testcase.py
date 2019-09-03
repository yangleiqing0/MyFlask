from modles.case_group import CaseGroup
from modles.testcase_scene import TestCaseScene
from modles.request_headers import RequestHeaders
from modles.user import User
from app import db
from datetime import datetime


class TestCases(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    data = db.Column(db.TEXT)
    regist_variable = db.Column(db.String(30))
    regular = db.Column(db.TEXT)
    method = db.Column(db.String(10), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey(CaseGroup.id))
    request_headers_id = db.Column(db.Integer, db.ForeignKey(RequestHeaders.id))
    testcase_scene_id = db.Column(db.Integer, db.ForeignKey(TestCaseScene.id))
    hope_result = db.Column(db.String(200))
    is_model = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    old_sql = db.Column(db.String(200))
    new_sql = db.Column(db.String(200))
    old_sql_regist_variable = db.Column(db.String(200))
    new_sql_regist_variable = db.Column(db.String(200))
    old_sql_hope_result = db.Column(db.String(200))
    new_sql_hope_result = db.Column(db.String(200))
    old_sql_id = db.Column(db.Integer)
    new_sql_id = db.Column(db.Integer)

    def __init__(self, name, url, data, regist_variable, regular, method, group_id=1,
                 request_headers_id=1,  testcase_scene_id=1, hope_result='', is_model=0, user_id=1,
                 old_sql='', new_sql='', old_sql_regist_variable='', new_sql_regist_variable='',
                 old_sql_hope_result='', new_sql_hope_result='', old_sql_id=None, new_sql_id=None):
        self.regist_variable = regist_variable
        self.regular = regular
        self.timestamp = datetime.now()
        self.name = name
        self.url = url
        self.data = data
        self.method = method
        self.group_id = group_id
        self.request_headers_id = request_headers_id
        self.hope_result = hope_result
        self.testcase_scene_id = testcase_scene_id
        self.is_model = is_model
        self.user_id = user_id
        self.old_sql = old_sql
        self.new_sql = new_sql
        self.old_sql_regist_variable = old_sql_regist_variable
        self.new_sql_regist_variable = new_sql_regist_variable
        self.old_sql_hope_result = old_sql_hope_result
        self.new_sql_hope_result = new_sql_hope_result
        self.old_sql_id = old_sql_id
        self.new_sql_id = new_sql_id

    def __repr__(self):
        return "<TestCase:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s >" % (
            self.id, self.name, self.url, self.data, self.method,
            self.group_id, self.request_headers_id, self.timestamp, self.regist_variable,
            self.regular, self.hope_result, self.testcase_scene_id, self.is_model, self.user_id)

    def to_json(self):
        return dict(id=self.id, name=self.name, url=self.url,
                    data=self.data, regist_variable=self.regist_variable,
                    method=self.method, group_id=self.group_id,
                    regular=self.regular, hope_result=self.hope_result,
                    testcase_scene_id=self.testcase_scene_id,
                    is_model=self.is_model, user_id=self.user_id)
