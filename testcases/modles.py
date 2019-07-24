from app import db


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(64))
    data = db.Column(db.String(64))
    result = db.Column(db.Integer)

    def __repr__(self):
        return '<TestCase %r>' % (self.name)