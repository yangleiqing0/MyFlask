
from . import Base, db, TestCases, TestCaseStartTimes


class TestCaseResult(Base, db.Model):

    testcase_name = db.Column(db.String(50), nullable=False)
    testcase_url = db.Column(db.String(300), nullable=False)
    testcase_data = db.Column(db.TEXT)
    testcase_method = db.Column(db.String(10), nullable=False)
    testcase_hope_result = db.Column(db.String(200))

    response_body = db.Column(db.UnicodeText)
    testcase_test_result = db.Column(db.TEXT)
    testcase_id = db.Column(db.Integer, db.ForeignKey(TestCases.id))
    scene_id = db.Column(db.Integer)
    testcase_start_time_id = db.Column(db.Integer, db.ForeignKey(TestCaseStartTimes.id))
    old_sql_value = db.Column(db.TEXT)
    new_sql_value = db.Column(db.TEXT)
    old_sql_value_result = db.Column(db.String(100))
    new_sql_value_result = db.Column(db.String(100))
    result = db.Column(db.String(100))

    testcases = db.relationship('TestCases', backref='testcase_result')

    def __init__(self, testcase_id, testcase_name,  testcase_url, testcase_data, testcase_method, testcase_hope_result,
                 testcase_start_time_id, response_body, testcase_test_result='',
                 old_sql_value='', new_sql_value='', old_sql_value_result='', new_sql_value_result='', result='', scene_id=''):
        super().__init__()
        self.testcase_id = testcase_id
        self.testcase_name = testcase_name
        self.testcase_url = testcase_url
        self.testcase_data = testcase_data
        self.testcase_method = testcase_method
        self.testcase_hope_result = testcase_hope_result
        self.testcase_start_time_id = testcase_start_time_id
        self.response_body = response_body
        self.testcase_test_result = testcase_test_result
        self.old_sql_value = old_sql_value
        self.new_sql_value = new_sql_value
        self.old_sql_value_result = old_sql_value_result
        self.new_sql_value_result = new_sql_value_result
        self.result = result
        self.scene_id = scene_id

    def __repr__(self):
        return '<测试用例执行结果 {} {} {} {} {} {}{} {} {} {} {} {}>'.format(self.response_body,
                self.response_body, self.testcase_id, self.testcase_start_time_id,
                self.old_sql_value, self.new_sql_value, self.testcase_test_result,self.testcase_name,
                self.testcase_url, self.testcase_data, self.testcase_method, self.testcase_hope_result)

    def to_json(self):
        return dict(id=self.id, testcase_id=self.testcase_id, testcase_start_time_id=self.testcase_start_time_id,
                    response_body =self.response_body, testcase_test_result=self.testcase_test_result,
                    old_sql_value=self.old_sql_value, new_sql_value=self.new_sql_value)