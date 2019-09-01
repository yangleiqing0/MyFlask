from app import db
from datetime import datetime
from modles.testcase_scene import TestCaseScene
from modles.testcase_start_times import TestCaseStartTimes


class TestCaseSceneResult(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scene_id = db.Column(db.Integer, db.ForeignKey(TestCaseScene.id))
    name = db.Column(db.String(50))
    count = db.Column(db.Integer)
    result = db.Column(db.String(50))

    time_id = db.Column(db.Integer, db.ForeignKey(TestCaseStartTimes.id))

    timestamp = db.Column(db.DateTime, index=True)

    scenes = db.relationship('TestCaseScene', backref='scene_result')
    start_time = db.relationship('TestCaseStartTimes', backref='time_scene_results')

    def __init__(self, scene_id, name, count,  result, time_id):
        self.scene_id = scene_id
        self.name = name
        self.count = count
        self.result = result
        self.time_id = time_id
        self.timestamp = datetime.now()

