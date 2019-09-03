#coding=utf-8
from datetime import datetime
from app import db
from modles.user import User


class Mail(db.Model):
    __tablename__ = 'mail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    to_user_list = db.Column(db.String(50))
    email_method = db.Column(db.Integer)

    def __init__(self, name='', subject='', user_id=1,
                 to_user_list='', email_method=1):
        self.name = name
        self.subject = subject
        self.to_user_list = to_user_list
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.email_method = email_method
