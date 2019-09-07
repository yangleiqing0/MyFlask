
from . import Base, db


class User(Base, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)

    user_testcase_scenes = db.relationship('TestCaseScene', backref='testcase_scene_user')
    user_testcases = db.relationship('TestCases', backref='testcase_user')
    user_case_groups = db.relationship('CaseGroup', backref='case_group_user')
    user_request_headers = db.relationship('RequestHeaders', backref='request_headers_user')
    user_testcase_start_times = db.relationship('TestCaseStartTimes', backref='testcase_start_time_user')
    user_jobs = db.relationship('Job', backref='job_user')
    user_mails = db.relationship('Mail', backref='mail_user')
    user_mysqls = db.relationship('Mysql', backref='mysql_user')

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def __repr__(self):
        return "<CaseGroup:%s,%s,%s>" % (self.id, self.username, self.password)

    def to_json(self):
        return dict(id=self.id, username=self.username, password=self.password)