from app import db
from datetime import datetime


class TestCaseStartTimes(db.Model):

    __tablename__ = 'test_case_start_times'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100))
    time_strftime = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, index=True)

    this_time_testcase_result = db.relationship('TestCaseResult', backref='test_case_which_time')

    def __init__(self, time_strftime="", filename=""):
        self.time_strftime = time_strftime
        self.filename = filename


        self.timestamp = datetime.now()

    def __repr__(self):
        return '<测试用例执行次数{} {} {} {}>' . format(self.filename, self.id, self.time_strftime, self.timestamp )

    def to_json(self):
        return dict(id=self.id, time_strftime=self.time_strftime, filename=self.filename)