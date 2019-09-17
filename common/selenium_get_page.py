from flask import session
from selenium import webdriver
import time
import os
from modles import User, Variables


class ReportImage:

    def __init__(self, user_id, testcase_time_id=0):
        self.testcase_time_id = testcase_time_id
        self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.start_time = time.time()
        self.user_id = user_id
        self.port = Variables.query.filter(Variables.name == '_LOCAL_FLASK_PORT', Variables.user_id == 1).first().value
        print('ReportImage:', self.testcase_time_id, self.port)

    def get_web(self):
        self.driver.get('http://127.0.0.1:%s/login/' % self.port)
        shot_name = self.to_report_page()
        self.driver.quit()
        print('get_web shot_name:', shot_name)
        return shot_name

    def to_report_page(self):
        user = User.query.get(self.user_id)
        print('ReportImage user_id:', user, user.username, user.password)
        self.driver.find_element_by_id('username').send_keys(user.username)
        self.driver.find_element_by_id('password').send_keys(user.password)
        self.driver.find_element_by_id('login').click()
        self.driver.get('http://127.0.0.1:%s/testcase_report_sendmail/?testcase_time_id=%s&report_type=phantomjs' % (self.port, self.testcase_time_id))
        from logs.config import path
        shot_name = os.path.join(path, 'reports/' +str(self.start_time) + 'screen.png')
        self.driver.save_screenshot(shot_name)
        print('over save shot:', time.time(), shot_name)
        return shot_name

        # self.remove_shot(shot_name)

    @staticmethod
    def remove_shot(shot_name):
        try:
            os.remove(shot_name)
        except Exception as e:
            pass





