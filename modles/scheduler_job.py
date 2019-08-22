from datetime import datetime
from app import db
from modles.user import User


class SchedulerJobs(db.Model):
    __tablename__ = 'scheduler_jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    triggers = db.Column(db.String(50))
    cron = db.Column(db.String(50))
    description = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, cron, triggers, description, user_id=None):
        self.name = name
        self.triggers = triggers
        self.cron = cron
        self.description = description
        self.user_id = user_id
        self.timestamp = datetime.now()
