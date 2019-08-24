#coding=utf-8
from datetime import datetime, timedelta
import json
from flask.views import MethodView
from flask import render_template, Blueprint, make_response, \
    redirect, url_for, session, flash, jsonify, request, current_app

from common.do_report import test_report
from common.request_get_more_values import request_get_values
from common.connect_sqlite import cdb
from common.send_mail import send_excel
from common.tail_font_log import FrontLogs
from modles.job import Job
from modles.testcase import TestCases
from modles.testcase_scene import TestCaseScene
from modles.user import User
from app import db
from views.testcase_report import TestCaseReport, get_report
from views.testcase_request import post_testcase

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
        page, job_id = request_get_values('page', 'job_id')
        job = Job.query.get(job_id)
        testcases_ids = job.testcases
        testcase_scenes_ids = job.testcase_scenes
        job.testcase_list, job.testcase_scene_list = [], []
        if len(testcases_ids) > 0:
            print('JobUpdate:', page, testcases_ids, type(testcases_ids), eval(testcases_ids), type(eval(testcases_ids)))
            for testcase_id in eval(testcases_ids):
                job.testcase_list.append(TestCases.query.get(testcase_id))
        if len(testcase_scenes_ids) > 0:
            for testcase_scene_id in eval(testcase_scenes_ids):
                job.testcase_scene_list.append(TestCaseScene.query.get(testcase_scene_id))
        return render_template('job/job_update.html', job=job, page=page)

    def post(self):
        page, job_id, name, description, triggers, cron, is_start = request_get_values(
            'page', 'job_id', 'name', 'description', 'triggers', 'cron', 'is_start')
        testcases = request.form.getlist('testcase')
        testcase_scenes = request.form.getlist('testcase_scene')
        print('JobUpdate post:', testcases, testcase_scenes, is_start)
        if len(testcases) > 0:
            testcases = ','.join(testcases)+','
        else:
            testcases = ''
        if len(testcase_scenes) > 0:
            testcase_scenes = ','.join(testcase_scenes)+','
        else:
            testcase_scenes = ''
        job = Job.query.get(job_id)
        job.name = name
        job.testcases = testcases
        job.testcase_scenes = testcase_scenes
        job.description = description
        job.triggers = triggers
        job.cron = cron
        job.is_start = is_start
        db.session.commit()
        return redirect(url_for('job_blueprint.job_list', page=page))


class JobSchedulerUpdate(MethodView):

    def get(self):
        job_id, is_start = request_get_values('job_id', 'is_start')
        job = Job.query.get(job_id)
        job.is_start = is_start
        db.session.commit()
        scheduler_job(job)
        return 'OK'


class JobList(MethodView):

    def get(self):
        user_id = session.get('user_id')
        page = request.args.get('page', 1, type=int)
        FrontLogs('进入测试任务列表页面 第%s页' % page).add_to_front_log()
        #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
        pagination = Job.query.filter(Job.user_id == user_id). \
            order_by(Job.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASK_POST_PRE_ARGV'], error_out=False)
        # 返回一个内容对象
        jobs = pagination.items
        return render_template('job/job_list.html', pagination=pagination, jobs=jobs, page=page)


job_blueprint.add_url_rule('/job_add/', view_func=JobAdd.as_view('job_add'))
job_blueprint.add_url_rule('/job_update/', view_func=JobUpdate.as_view('job_update'))
job_blueprint.add_url_rule('/job_list/', view_func=JobList.as_view('job_list'))


job_blueprint.add_url_rule('/job_scheduler_update/', view_func=JobSchedulerUpdate.as_view('job_scheduler_update'))


def scheduler_job(job):
    from app import scheduler
    print('scheduler_job:', job.is_start)
    if job.is_start == 1:
        scheduler.add_job(id='job_1', func=auto_send_mail, trigger='cron', second='*/50', args=(job,))
        print('get_jobs:', scheduler.get_jobs())
        scheduler.start()

    elif job.is_start == 0:
        print('get_jobs is:', scheduler.get_jobs())
        scheduler.remove_job('job_1')
        print('get_jobs is_after:', scheduler.get_jobs())


def print_job_name(job):
    print(job.name)


def auto_send_mail(job):
    id = job.id
    testcases_ids = eval(job.testcases)
    testcase_scenes_ids = eval(job.testcase_scenes)
    from werkzeug.test import EnvironBuilder
    from app import return_app
    app = return_app()
    ctx = app.request_context(EnvironBuilder('/', 'http://localhost/').get_environ())
    # 构建一个request上下文对象放入app
    ctx.push()
    session['user_id'] = job.user_id
    testcase_time_id = get_testcase_time_id()
    post_request(testcases_ids, testcase_scenes_ids, testcase_time_id)
    get_report(testcase_time_id)
    send_excel('haha', ['253775405@qq.com'], testcase_time_id=testcase_time_id)


def get_testcase_time_id():
    from views.testcase_request import TestCaseTimeGet
    testcase_time_id = json.loads(TestCaseTimeGet().get())['testcase_time_id']
    print('request_test:', testcase_time_id, session.get('user_id'))
    return testcase_time_id


def post_request(testcases_ids, testcase_scenes_ids, testcase_time_id):
    for testcase_id in testcases_ids:
        post_testcase(testcase_id, testcase_time_id)
    for testcase_scene_id in testcase_scenes_ids:
        testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        for testcase_scene_testcase in testcase_scene.testcases:
            post_testcase(testcase_scene_testcase.id, testcase_time_id)







