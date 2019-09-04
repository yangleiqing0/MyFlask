from datetime import datetime
from app import db


class BaseModel:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, index=True)
    name = db.Column(db.String(11), nullable=False)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name):
        self.timestamp = datetime.now()
        self.name = name


class TestGroup(BaseModel, db.Model):

    description = db.Column(db.String(50))

    def __init__(self, name, description=''):
        super().__init__(name)
        self.description = description
