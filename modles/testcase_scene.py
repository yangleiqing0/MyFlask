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
    testcases = db.relationship('TestCases', backref='testcase_scene')

    def __init__(self, name, group_id, description):
        self.name = name
        self.group_id = group_id
        self.description = description
        self.timestamp = datetime.now()

    def __repr__(self):
        return "<TestCaseScene:%s,%s,%s, %s>" % (self.id, self.name, self.group_id, self.description)

    def to_json(self):
        return dict(id=self.id, name=self.name, group_id=self.group_id, description=self.description)
