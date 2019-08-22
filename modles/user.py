from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, index=True)

    user_testcase_scenes = db.relationship('TestCaseScene', backref='testcase_scene_user')
    user_testcases = db.relationship('TestCases', backref='testcase_user')
    user_case_groups = db.relationship('CaseGroup', backref='case_group_user')
    user_request_headers = db.relationship('RequestHeaders', backref='request_headers_user')
    user_testcase_start_times = db.relationship('TestCaseStartTimes', backref='testcase_start_time_user')
    user_scheduler_jobs = db.relationship('SchedulerJobs', backref='scheduler_job_user')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.timestamp = datetime.now()

    def __repr__(self):
        return "<CaseGroup:%s,%s,%s>" % (self.id, self.username, self.password)

    def to_json(self):
        return dict(id=self.id, username=self.username, password=self.password)