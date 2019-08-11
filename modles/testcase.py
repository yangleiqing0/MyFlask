from modles.case_group import CaseGroup
from modles.testcase_scene import TestCaseScene
from modles.request_headers import RequestHeaders
from app import db
from datetime import datetime

class TestCases(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
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

    def __init__(self, name, url, data, regist_variable, regular, method, group_id,
                 request_headers_id,  testcase_scene_id=None, hope_result=None, is_model=0):
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

    def __repr__(self):
        return "<TestCase:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s >" % (
            self.id, self.name, self.url, self.data, self.method,
            self.group_id, self.request_headers_id, self.timestamp, self.regist_variable,
            self.regular, self.hope_result, self.testcase_scene_id, self.is_model)

    def to_json(self):
        return dict(id=self.id, name=self.name, url=self.url,
                    data=self.data, regist_variable=self.regist_variable,
                    method=self.method, group_id=self.group_id,
                    regular=self.regular, hope_result=self.hope_result,
                    testcase_scene_id=self.testcase_scene_id,
                    is_model=self.is_model)
