
from . import Base, db, TestCaseStartTimes


class TimeMessage(Base, db.Model):

    test_name = db.Column(db.String(100))
    zdbm_version = db.Column(db.String(100))
    test_pl = db.Column(db.String(100))
    test_net = db.Column(db.String(100))
    title_name = db.Column(db.String(100))
    fail_sum = db.Column(db.Integer())
    test_sum = db.Column(db.Integer())
    test_success = db.Column(db.Integer())
    time_strftime = db.Column(db.String(100))
    score = db.Column(db.Integer())

    time_id = db.Column(db.Integer, db.ForeignKey(TestCaseStartTimes.id))

    start_time = db.relationship('TestCaseStartTimes', backref='time_scene_mes')

    def __init__(self, test_name, zdbm_version, test_pl, test_net, title_name, fail_sum, test_sum, test_success, time_strftime, score, time_id):
        super().__init__()
        self.test_name = test_name
        self.zdbm_version = zdbm_version
        self.test_pl = test_pl
        self.test_net = test_net
        self.title_name = title_name
        self.fail_sum = fail_sum
        self.test_sum = test_sum
        self.test_success = test_success
        self.time_strftime = time_strftime
        self.score = score
        self.time_id = time_id
