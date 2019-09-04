from app import db
from modles.testcase_scene import TestCaseScene
from modles.testcase_start_times import TestCaseStartTimes
from . import BaseModel


class TestCaseSceneResult(BaseModel, db.Model):

    scene_id = db.Column(db.Integer, db.ForeignKey(TestCaseScene.id))
    count = db.Column(db.Integer)
    result = db.Column(db.String(50))

    time_id = db.Column(db.Integer, db.ForeignKey(TestCaseStartTimes.id))


    scenes = db.relationship('TestCaseScene', backref='scene_result')
    start_time = db.relationship('TestCaseStartTimes', backref='time_scene_results')

    def __init__(self, scene_id, name, count,  result, time_id):
        super().__init__(name)
        self.scene_id = scene_id
        self.count = count
        self.result = result
        self.time_id = time_id

