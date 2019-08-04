from datetime import datetime
from app import db


class CaseGroup(db.Model):
    __tablename__ = 'case_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(11), nullable=False)
    description = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True)

    testcases = db.relationship('TestCases', backref='case_group')

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.timestamp = datetime.now()

    def __repr__(self):
        return "<CaseGroup:%s,%s,%s>" % (self.id, self.name, self.description)

    def to_json(self):
        return dict(id=self.id, name=self.name, description=self.description)