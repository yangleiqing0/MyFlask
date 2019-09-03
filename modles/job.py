#coding=utf-8
from datetime import datetime
from app import db
from modles.mail import Mail
from modles.user import User


class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    testcases = db.Column(db.String(50))
    testcase_scenes = db.Column(db.String(50))
    description = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    triggers = db.Column(db.String(50))
    cron = db.Column(db.String(50))
    is_start = db.Column(db.Integer)
    mail_id = db.Column(db.Integer, db.ForeignKey(Mail.id))

    def __init__(self, testcases='', testcase_scenes='',  description='', user_id=1,
                 triggers='cron', cron='', is_start=0, mail_id=1):
        self.name = '任务' + str(datetime.now())[:19]
        self.testcases = testcases
        self.testcase_scenes = testcase_scenes
        self.description = description
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.triggers = triggers
        self.cron = cron
        self.is_start = is_start
        self.mail_id = mail_id
