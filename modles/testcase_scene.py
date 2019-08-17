from datetime import datetime
from app import db
from modles.case_group import CaseGroup


class TestCaseScene(db.Model):
    __tablename__ = 'testcase_scenes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50))
    group_id = db.Column(db.Integer, db.ForeignKey(CaseGroup.id))
    timestamp = db.Column(db.DateTime, index=True)
    is_model = db.Column(db.Integer)

    testcases = db.relationship('TestCases', backref='testcase_scene')

    def __init__(self, name, group_id=None, description='', is_model=0):
        self.name = name
        self.group_id = group_id
        self.description = description
        self.timestamp = datetime.now()
        self.is_model = is_model

    def __repr__(self):
        return "<TestCaseScene:%s,%s,%s, %s, %s>" % (self.id, self.name, self.group_id, self.description, self.is_model)

    def to_json(self):
        return dict(id=self.id, name=self.name, group_id=self.group_id, description=self.description, is_model=self.is_model)
