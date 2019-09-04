from app import db
from modles.user import User
from . import BaseModel


class TestCaseStartTimes(BaseModel, db.Model):

    __tablename__ = 'test_case_start_times'
    filename = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    this_time_testcase_result = db.relationship('TestCaseResult', backref='test_case_which_time')

    def __init__(self, time_strftime='', filename='', name='', user_id=1):
        super().__init__(name)
        self.time_strftime = time_strftime
        self.filename = filename
        self.user_id = user_id

    def __repr__(self):
        return '<测试用例执行次数{} {} {} {} {} {}>' . format(
            self.name, self.filename, self.id, self.time_strftime, self.timestamp, self.user_id )

    def to_json(self):
        return dict(id=self.id, time_strftime=self.time_strftime,
                    filename=self.filename, name=self.name, user_id=self.user_id)