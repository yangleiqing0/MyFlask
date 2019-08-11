from app import db
from datetime import datetime
from modles.testcase import TestCases
from modles.testcase_start_times import TestCaseStartTimes


class TestCaseResult(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_body = db.Column(db.TEXT)
    testcase_test_result = db.Column(db.String(10))
    testcase_id = db.Column(db.Integer, db.ForeignKey(TestCases.id))
    testcase_start_time_id = db.Column(db.Integer, db.ForeignKey(TestCaseStartTimes.id))
    old_sql_value = db.Column(db.TEXT)
    new_sql_value = db.Column(db.TEXT)
    timestamp = db.Column(db.DateTime, index=True)

    testcases = db.relationship('TestCases', backref='testcase_result')

    def __init__(self, testcase_id, testcase_start_time_id, response_body, testcase_test_result="测试成功",
                 old_sql_value=None, new_sql_value=None):
        self.testcase_id = testcase_id
        self.testcase_start_time_id = testcase_start_time_id
        self.response_body = response_body
        self.testcase_test_result = testcase_test_result
        self.timestamp = datetime.now()
        self.old_sql_value = old_sql_value
        self.new_sql_value = new_sql_value

    def __repr__(self):
        return '<测试用例执行结果 {} {} {} {} {} {}{}>'.format(self.response_body,
                self.response_body, self.testcase_id, self.testcase_start_time_id,
                self.old_sql_value, self.new_sql_value, self.testcase_test_result)

    def to_json(self):
        return dict(id=self.id, testcase_id=self.testcase_id, testcase_start_time_id=self.testcase_start_time_id,
                    response_body =self.response_body, testcase_test_result=self.testcase_test_result,
                    old_sql_value=self.old_sql_value, new_sql_value=self.new_sql_value)