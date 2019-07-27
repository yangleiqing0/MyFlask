from app import db


class CaseGroup(db.Model):
    __tablename__ = 'case_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(11), nullable=False)
    description = db.Column(db.String(50), nullable=False)

    # testcases = db.relationship('TestCases',backref=db.backref('casegroup', lazy='dynamic'))

    def __repr__(self):
        return "<CaseGroup:%s,%s,%s>" % (self.id, self.name, self.description)

    def to_json(self):
        return dict(id=self.id, name=self.name, description=self.description)