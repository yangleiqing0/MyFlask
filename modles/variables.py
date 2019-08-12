from app import db
from datetime import datetime


class Variables(db.Model):

    __tablename__ = 'variables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(11), unique=True, nullable=False)
    value = db.Column(db.TEXT, nullable=False, default=None)
    description= db.Column(db.String(50))
    is_private = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True)

    def __init__(self, name, value, description='', is_private=0):
        self.name = name
        self.value = value
        self.description = description
        self.is_private = is_private
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<全局变量 {}： {} {} {}>' . format(self.name, self.value, self.description, self.timestamp )

    def to_json(self):
        return dict(id=self.id, name=self.name, value=self.value,
                    description=self.description, is_private=self.is_private)