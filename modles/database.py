#coding=utf-8
from datetime import datetime
from app import db
from modles.mail import Mail
from modles.user import User


class Mysql(db.Model):

    __tablename__ = 'mysql'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(50))
    port = db.Column(db.String(50))
    description = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.Column(db.String(50))
    password = db.Column(db.String(50))
    db_name = db.Column(db.Integer)

    def __init__(self, name, ip,  port, user, password, db_name, description='', user_id=None):
        self.name = name
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.timestamp = datetime.now()
        self.description = description
        self.user_id = user_id

