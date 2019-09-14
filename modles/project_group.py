from . import BaseModel, db


class ProjectGroup(BaseModel, db.Model):
    __tablename__ = 'project_group'
    description = db.Column(db.String(50))

    users = db.relationship('User', backref='project_group')

    def __init__(self, name, description=''):
        super().__init__(name)
        self.description = description

    def __repr__(self):
        return "<CaseGroup:%s,%s,%s>" % (self.id, self.name, self.description)
