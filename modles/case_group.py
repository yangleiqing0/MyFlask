from datetime import datetime
from app import db
from modles.user import User


class CaseGroup(db.Model):
    __tablename__ = 'case_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(11), nullable=False)
    description = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    case_group_testcase_scenes = db.relationship('TestCaseScene', backref='testcase_scene_case_group')
    testcases = db.relationship('TestCases', backref='case_group')

    def __init__(self, name, description='', user_id=1):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.timestamp = datetime.now()

    def __repr__(self):
        return "<CaseGroup:%s,%s,%s. %s>" % (self.id, self.name, self.description, self.user_id)

    def to_json(self):
        return dict(id=self.id, name=self.name, description=self.description, user_id=self.user_id)