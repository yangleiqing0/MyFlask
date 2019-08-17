# !/usr/bin/env python3
# encoding: utf-8
import json
from logs.config import FRONT_LOGS_FILE, FLASK_LOGS_FILE
from flask.views import MethodView
from flask import render_template, Blueprint, request
from app import db
from common.pre_db_insert_data import to_insert_data

home_blueprint = Blueprint('home_blueprint', __name__)


class Home(MethodView):

    def get(self):
        return render_template('home.html')


class DbCreatAll(MethodView):

    def get(self):

        from modles.testcase import TestCases
        from modles.case_group import CaseGroup
        from modles.variables import Variables
        from modles.request_headers import RequestHeaders
        from modles.testcase_start_times import TestCaseStartTimes
        from modles.testcase_result import TestCaseResult
        from modles.testcase_scene import TestCaseScene
        from modles.user import User
        db.create_all()
        to_insert_data()

        return '数据库表创建OK'


class Test(MethodView):
    
    def get(self):
        print(request.args.get('id'))
        return request.form
    
    def post(self):
        print(request.args)
        return request.form


class FrontLog(MethodView):

    def get(self):
        with open(FRONT_LOGS_FILE, 'rb') as logs:
            offset = -50
            while True:
                """
                file.seek(off, whence=0)：从文件中移动off个操作标记（文件指针），正往结束方向移动，负往开始方向移动。
                如果设定了whence参数，就以whence设定的起始位为准，0代表从头开始，1代表当前位置，2代表文件最末尾位置。 
                """
                logs.seek(offset, 2)  # seek(offset, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)
                front_logs = logs.readlines()  # 读取文件指针范围内所有行
                lens = len(front_logs)
                front_log = []
                if lens >= 11:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                    front_logs = front_logs[-10:]
                    for ii in range(10):
                        front_log.append(front_logs[ii].decode('gbk'))
                    break
                offset *= 2
            front_log = "<br/>".join(front_log)
        print("front_logs: ", len(front_log), front_log)
        return json.dumps({"front_log": front_log})


class FlaskLog(MethodView):

    def get(self):
        with open(FLASK_LOGS_FILE) as logs:
            flask_logs = logs.readlines()
            flask_logs = "<br/>".join(flask_logs[len(flask_logs)-9:])
        print(flask_logs[len(flask_logs)-9:], "flask_logs: ", flask_logs)
        return json.dumps({"flask_logs": str(flask_logs)})


def to_read_last_row(file, row):
    with open(file, 'rb') as logs:
        offset = -50
        while True:
            """
            file.seek(off, whence=0)：从文件中移动off个操作标记（文件指针），正往结束方向移动，负往开始方向移动。
            如果设定了whence参数，就以whence设定的起始位为准，0代表从头开始，1代表当前位置，2代表文件最末尾位置。 
            """
            logs.seek(offset, 2)  # seek(offset, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)
            front_logs = logs.readlines()  # 读取文件指针范围内所有行
            if len(front_logs) >= row+1:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                front_logs = front_logs[-row:]
                for i in range(len(front_logs)):
                    front_logs[i] = front_logs[i].decode('gbk')
                break
            offset *= 2
        front_logs = "<br/>".join(front_logs)
    return json.dumps({"front_logs": str(front_logs)})


home_blueprint.add_url_rule('/', view_func=Home.as_view('home'))
home_blueprint.add_url_rule('/test/', view_func=Test.as_view('test'))
home_blueprint.add_url_rule('/db_create_all/', view_func=DbCreatAll.as_view('db_create_all'))
home_blueprint.add_url_rule('/frontlogs/', view_func=FrontLog.as_view('front_logs'))
home_blueprint.add_url_rule('/flasklogs/', view_func=FlaskLog.as_view('flask_logs'))