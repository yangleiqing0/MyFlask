from . import Base, db, TestCases


class Wait(Base, db.Model):
    __tablename__ = 'wait'
    old_wait_sql = db.Column(db.String(200))
    old_wait = db.Column(db.String(50))
    old_wait_time = db.Column(db.String(200))
    old_wait_mysql = db.Column(db.Integer)
    new_wait_sql = db.Column(db.String(200))
    new_wait = db.Column(db.String(50))
    new_wait_time = db.Column(db.String(200))
    new_wait_mysql = db.Column(db.Integer)
    testcase_id = db.Column(db.Integer, db.ForeignKey(TestCases.id))

    testcase = db.relationship('TestCases', backref='wait')

    def __init__(self, old_wait_sql, old_wait, old_wait_time, old_wait_mysql, new_wait_sql,
                   new_wait, new_wait_time, new_wait_mysql, testcase_id):
        super().__init__()
        self.old_wait_sql = old_wait_sql
        self.old_wait = old_wait
        self.old_wait_time = old_wait_time
        self.old_wait_mysql = old_wait_mysql
        self.new_wait_sql = new_wait_sql
        self.new_wait = new_wait
        self.new_wait_time = new_wait_time
        self.new_wait_mysql = new_wait_mysql
        self.testcase_id = testcase_id


