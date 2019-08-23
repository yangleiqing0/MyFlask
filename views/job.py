#coding=utf-8
from datetime import datetime, timedelta
import json
from flask.views import MethodView
from flask import render_template, Blueprint, make_response, redirect, url_for, session, flash, jsonify
from common.request_get_more_values import request_get_values
from common.connect_sqlite import cdb
from common.tail_font_log import FrontLogs
from modles.job import Job
from app import db

job_blueprint = Blueprint('job_blueprint', __name__)


class JobAdd(MethodView):

    def get(self):
        FrontLogs('进入任务添加页面').add_to_front_log()
        return render_template('job/job_add.html')

    def post(self):
        user_id =session.get('user_id')
        testcases, testcase_scenes, description = request_get_values('testcases', 'testcase_scenes', 'description')
        print('JobAdd: ', testcases, type(testcases), eval(testcases), type(eval(testcases)), testcase_scenes)
        job = Job(testcases, testcase_scenes, description, user_id)
        db.session.add(job)
        db.session.commit()
        FrontLogs('添加任务 name 成功: %s ' % job.name).add_to_front_log()
        # app.logger.info('message:insert into SchedulerJobs success, name: %s' % name)
        return json.dumps({"job_id": str(job.id)})


class JobUpdate(MethodView):

    def get(self):
        job_id = request_get_values('job_id')
        job = Job.query.get(job_id)
        return render_template('job/job_update.html', job=job)

    def post(self):
        job_id, name, testcases, testcase_scenes, description = request_get_values(
            'job_id', 'name', 'testcases', 'testcase_scenes', 'description')
        job = Job.query.get(job_id)
        job.name = name
        job.testcases = testcases
        job.testcase_scenes = testcase_scenes
        job.description = description
        db.session.commit()
        return redirect(url_for('test_case_request_blueprint.test_case_request'))


job_blueprint.add_url_rule('/job_add/', view_func=JobAdd.as_view('job_add'))
job_blueprint.add_url_rule('/job_update/', view_func=JobUpdate.as_view('job_update'))