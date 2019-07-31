from app import db
from datetime import datetime


class Variables(db.Model):

    __tablename__ = 'variables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(11), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    description= db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True)

    def __init__(self, name, value, description):
        self.name = name
        self.value = value
        self.description = description
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<全局变量 {}： {} {} {}>' . format(self.name, self.value, self.description, self.timestamp )