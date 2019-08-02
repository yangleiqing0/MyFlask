from app import db
from datetime import datetime


class TestCaseStartTimes(db.Model):

    __tablename__ = 'test_case_start_times'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, index=True)

    this_time_testcase_result = db.relationship('TestCaseResult', backref='test_case_which_time')


    def __init__(self):
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<测试用例执行次数 {} {}>' . format(self.id, self.timestamp )

    def to_json(self):
        return dict(id=self.id)