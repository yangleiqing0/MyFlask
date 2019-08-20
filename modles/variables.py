from app import db
from datetime import datetime
from modles.user import User


class Variables(db.Model):

    __tablename__ = 'variables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.TEXT, nullable=False, default=None)
    description= db.Column(db.String(50))
    is_private = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, value, description='', is_private=0, user_id=None):
        self.name = name
        self.value = value
        self.description = description
        self.is_private = is_private
        self.timestamp = datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return '<全局变量 {}： {} {} {} {}>' . format(
            self.name, self.value, self.description, self.timestamp,self.user_id)

    def to_json(self):
        return dict(id=self.id, name=self.name, value=self.value,
                    description=self.description, is_private=self.is_private, user_id=self.user_id)