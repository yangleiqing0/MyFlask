from app import db
from datetime import datetime
from modles.testcase import TestCases
from modles.testcase_start_times import TestCaseStartTimes


class TestCaseResult(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_body = db.Column(db.TEXT)
    testcase_result = db.Column(db.Integer)
    testcase_id = db.Column(db.Integer,db.ForeignKey(TestCases.id))
    testcase_start_time_id = db.Column(db.Integer,db.ForeignKey(TestCaseStartTimes.id))
    timestamp = db.Column(db.DateTime, index=True)

    def __init__(self, testcase_id, testcase_start_time_id, response_body, testcase_result):
        self.testcase_id = testcase_id
        self.testcase_start_time_id = testcase_start_time_id
        self.response_body = response_body
        self.testcase_result = testcase_result
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<测试用例执行结果 {} {} {} {}>'.format(self.response_body, self.response_body, self.testcase_id, self.testcase_start_time_id)

    def to_json(self):
        return dict(id=self.id, testcase_id=self.testcase_id, testcase_start_time_id=self.testcase_start_time_id,
                    response_body =self.response_body, testcase_result=self.testcase_result)