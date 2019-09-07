
from . import BaseModel, db, User


class RequestHeaders(BaseModel, db.Model):

    __tablename__ = 'request_headers'
    value = db.Column(db.TEXT, nullable=False)
    description= db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    testcases = db.relationship('TestCases', backref='testcase_request_header')

    def __init__(self, name, value, description='', user_id=1):
        super().__init__(name)
        self.value = value
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return '<请求头部 {}： {} {} {} {}>'.format(self.name, self.value, self.description, self.timestamp, self.user_id)

    def to_json(self):
        return dict(id=self.id, name=self.name, value=self.value,
                    description=self.description, user_id=self.user_id)