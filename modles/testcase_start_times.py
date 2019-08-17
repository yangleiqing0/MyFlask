from app import db
from datetime import datetime
from modles.user import User


class TestCaseStartTimes(db.Model):

    __tablename__ = 'test_case_start_times'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    filename = db.Column(db.String(100))
    time_strftime = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    this_time_testcase_result = db.relationship('TestCaseResult', backref='test_case_which_time')

    def __init__(self, time_strftime=None, filename=None, name=None, user_id=None):
        self.time_strftime = time_strftime
        self.filename = filename
        self.name = name
        self.user_id = user_id
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<测试用例执行次数{} {} {} {} {} {}>' . format(
            self.name, self.filename, self.id, self.time_strftime, self.timestamp, self.user_id )

    def to_json(self):
        return dict(id=self.id, time_strftime=self.time_strftime,
                    filename=self.filename, name=self.name, user_id=self.user_id)