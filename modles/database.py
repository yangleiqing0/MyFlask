#coding=utf-8

from . import BaseModel, User, db


class Mysql(BaseModel, db.Model):

    __tablename__ = 'mysql'
    ip = db.Column(db.String(50))
    port = db.Column(db.String(50))
    description = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.Column(db.String(50))
    password = db.Column(db.String(50))
    db_name = db.Column(db.String(50))

    def __init__(self, name, ip,  port, user, password, db_name, description='', user_id=1):
        super().__init__(name)
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.description = description
        self.user_id = user_id

