from app import db


class CaseGroup(db.Model):
    __tablename__ = 'case_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(11), nullable=False)
    descrption = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<CaseGroup:%s,%s,%s>" % (self.id, self.name, self.descrption)

    def to_json(self):
        return dict(id=self.id, name=self.name, descrption=self.descrption)