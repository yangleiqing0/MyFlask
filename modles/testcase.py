from modles.case_group import CaseGroup
from modles.request_headers import RequestHeaders
from app import db
from datetime import datetime

class TestCases(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    url = db.Column(db.String(20))
    data = db.Column(db.TEXT)
    result = db.Column(db.String(20))
    method = db.Column(db.String(20))
    group_id = db.Column(db.Integer, db.ForeignKey(CaseGroup.id))
    request_headers_id = db.Column(db.Integer, db.ForeignKey(RequestHeaders.id))
    timestamp = db.Column(db.DateTime, index=True)

    def __init__(self, name, url, data, method, group_id, request_headers_id):
        self.result = None
        self.timestamp = datetime.utcnow()
        self.name = name
        self.url = url
        self.data = data
        self.method = method
        self.group_id = group_id
        self.request_headers_id = request_headers_id

    def __repr__(self):
        return "<TestCase:%s,%s,%s,%s,%s,%s,%s,%s %s>" % (
            self.id, self.name, self.url, self.data, self.method,
            self.group_id, self.request_headers_id, self.timestamp, self.result)

    def to_json(self):
        return dict(id=self.id, name=self.name, url=self.url,
                    data=self.data, result=self.result,
                    method=self.method, group_id=self.group_id)