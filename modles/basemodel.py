from . import datetime, db


class Base:
    timestamp = db.Column(db.DateTime, index=True)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self):
        self.timestamp = datetime.now()


class BaseModel(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name





