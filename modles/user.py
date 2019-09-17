
from . import Base, db, ProjectGroup


class User(Base, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    project_group_id = db.Column(db.Integer, db.ForeignKey(ProjectGroup.id))

    user_testcase_scenes = db.relationship('TestCaseScene', backref='testcase_scene_user')
    user_testcases = db.relationship('TestCases', backref='testcase_user')
    user_case_groups = db.relationship('CaseGroup', backref='case_group_user')
    user_request_headers = db.relationship('RequestHeaders', backref='request_headers_user')
    user_testcase_start_times = db.relationship('TestCaseStartTimes', backref='testcase_start_time_user')
    user_jobs = db.relationship('Job', backref='job_user')
    user_mails = db.relationship('Mail', backref='mail_user')
    user_mysqls = db.relationship('Mysql', backref='mysql_user')

    def __init__(self, username, password, project_group_id=1):
        super().__init__()
        self.username = username
        self.password = password
        self.project_group_id = project_group_id
