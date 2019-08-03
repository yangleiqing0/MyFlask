from app import db
from datetime import datetime


class RequestHeaders(db.Model):

    __tablename__ = 'request_headers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(11), nullable=False)
    value = db.Column(db.TEXT, nullable=False)
    description= db.Column(db.String(50))

    timestamp = db.Column(db.DateTime, index=True)
    testcases = db.relationship('TestCases', backref='request_headers')

    def __init__(self, name, value, description):
        self.name = name
        self.value = value
        self.description = description
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<请求头部 {}： {} {} {}>'.format(self.name, self.value, self.description, self.timestamp)

    def to_json(self):
        return dict(id=self.id, name=self.name, value=self.value,
                    description=self.description)