from . import BaseModel, User, db


class CaseGroup(BaseModel, db.Model):
    __tablename__ = 'case_group'
    description = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    case_group_testcase_scenes = db.relationship('TestCaseScene', backref='testcase_scene_case_group')
    testcases = db.relationship('TestCases', backref='case_group')

    def __init__(self, name, description='', user_id=1):
        super().__init__(name)
        self.user_id = user_id
        self.description = description

    def __repr__(self):
        return "<CaseGroup:%s,%s,%s. %s>" % (self.id, self.name, self.description, self.user_id)

    def to_json(self):
        return dict(id=self.id, name=self.name, description=self.description, user_id=self.user_id)