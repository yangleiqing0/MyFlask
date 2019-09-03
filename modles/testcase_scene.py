from datetime import datetime
from app import db
from modles.case_group import CaseGroup
from modles.user import User


class TestCaseScene(db.Model):
    __tablename__ = 'testcase_scenes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50))
    group_id = db.Column(db.Integer, db.ForeignKey(CaseGroup.id))
    timestamp = db.Column(db.DateTime, index=True)
    is_model = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    testcases = db.relationship('TestCases', backref='testcase_scene')

    def __init__(self, name, group_id=1, description='', is_model=0, user_id=1):
        self.name = name
        self.group_id = group_id
        self.description = description
        self.timestamp = datetime.now()
        self.is_model = is_model
        self.user_id = user_id

    def __repr__(self):
        return "<TestCaseScene:%s,%s,%s, %s, %s, %s>" % (
            self.id, self.name, self.group_id, self.description, self.is_model, self.user_id)

    def to_json(self):
        return dict(id=self.id, name=self.name, group_id=self.group_id, description=self.description,
                    is_model=self.is_model, user_id=self.user_id)
