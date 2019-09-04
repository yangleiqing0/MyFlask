from app import db
from modles.user import User
from . import BaseModel


class Variables(BaseModel, db.Model):

    __tablename__ = 'variables'
    value = db.Column(db.TEXT, nullable=False, default=None)
    description= db.Column(db.String(50))
    is_private = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, value, description='', is_private=0, user_id=1):
        super().__init__(name)
        self.value = value
        self.description = description
        self.is_private = is_private
        self.user_id = user_id
    #
    # def __repr__(self):
    #     return '<全局变量 {}： {} {} {} {}>' . format(
    #         self.name, self.value, self.description, self.timestamp,self.user_id)
    #
    # def to_json(self):
    #     return dict(id=self.id, name=self.name, value=self.value,
    #                 description=self.description, is_private=self.is_private, user_id=self.user_id)