from selenium import webdriver
from modles.user import User
from common.send_mail import send_mail
from flask import session
import time
import os


class ReportImage:

    def __init__(self, user_id, testcase_time_id=0):
        self.testcase_time_id = testcase_time_id
        self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()
        self.start_time = time.time()
        self.user_id = user_id

    def get_web(self):
        self.driver.get('http://127.0.0.1:5000/login/')
        self.to_report_page()

    def to_report_page(self):
        user = User.query.filter(User.id == self.user_id).first()
        self.driver.find_element_by_id('username').send_keys(user.username)
        self.driver.find_element_by_id('password').send_keys(user.password)
        self.driver.find_element_by_xpath('//*[@id="get_container_height"]/div[2]/div/div/div[2]/form/div[6]/input[1]').click()
        self.driver.get('http://127.0.0.1:5000/testcase_report_sendmail/?testcase_time_id=5&report_type=phantomjs')
        shot_name = 'reports/' +str(self.start_time) + 'screen.png'
        self.driver.save_screenshot(shot_name)
        self.driver.close()
        return shot_name
        # self.remove_shot(shot_name)

    @staticmethod
    def remove_shot(shot_name):
        try:
            os.remove(shot_name)
        except Exception as e:
            pass

    def __del__(self):
        self.driver.quit()




