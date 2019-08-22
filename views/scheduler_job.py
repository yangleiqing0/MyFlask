#coding=utf-8
from datetime import datetime, timedelta
from flask.views import MethodView
from flask import render_template, Blueprint, make_response, redirect, url_for, session, flash
from common.request_get_more_values import request_get_values
from common.connect_sqlite import cdb
from common.tail_font_log import FrontLogs
from modles.scheduler_job import SchedulerJobs
from app import db

scheduler_jobs_blueprint = Blueprint('scheduler_jobs_blueprint', __name__)


class SchedulerJobsAdd(MethodView):

    def get(self):
        FrontLogs('进入定时任务添加页面').add_to_front_log()
        return render_template('scheduler_job/scheduler_job_add.html')

    def post(self):
        user_id =session.get('user_id')
        name, triggers, cron, description = request_get_values('name', 'triggers', 'cron', 'description')
        scheduler_job = SchedulerJobs(name, triggers, cron, description, user_id)
        db.session.add(scheduler_job)
        db.session.commit()
        FrontLogs('开始添加定时任务 name 成功: %s ' % name).add_to_front_log()
        # app.logger.info('message:insert into SchedulerJobs success, name: %s' % name)
        return redirect(url_for('test_case_request_blueprint.test_case_request'))


scheduler_jobs_blueprint.add_url_rule('/scheduler_job_add/', view_func=SchedulerJobsAdd.as_view('scheduler_job_add'))