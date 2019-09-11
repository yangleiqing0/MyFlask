#coding=utf-8
from datetime import datetime
import json
from flask.views import MethodView
from flask import render_template, Blueprint, redirect, url_for, session, request, current_app, jsonify
from common.request_get_more_values import request_get_values
from common.send_mail import send_excel, send_mail
from common.tail_font_log import FrontLogs
from views.testcase_report import get_report
from views.testcase_request import post_testcase
from modles import Job, Mail, TestCases, TestCaseScene, TestCaseStartTimes, db


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
        mails = Mail.query.filter(Mail.user_id == job.user_id).all()
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
        FrontLogs('进入编辑任务 name 页面: %s ' % job.name).add_to_front_log()
        return render_template('job/job_update.html', job=job, page=page, mails=mails)

    def post(self):

        page, job_id, name, description, triggers, cron, is_start, mail_id= request_get_values(
            'page', 'job_id', 'name', 'description', 'triggers', 'cron', 'is_start', 'email')
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
        old_cron = job.cron
        job.name = name
        job.testcases = testcases
        job.testcase_scenes = testcase_scenes
        job.description = description
        job.triggers = triggers
        job.cron = cron
        job.is_start = is_start
        job.mail_id = mail_id
        db.session.commit()
        print('old_cron cron:', old_cron, cron)
        if old_cron == cron:
            scheduler_job(job)
        else:
            scheduler_job(job, cron_change=1)
        FrontLogs('编辑任务 name 成功: %s ' % name).add_to_front_log()
        return redirect(url_for('job_blueprint.job_list', page=page))


class JobDelete(MethodView):

    def get(self):
        page, job_id = request_get_values('page', 'job_id')
        job = Job.query.get(job_id)
        job.is_start = 0
        db.session.commit()
        scheduler_job(job)
        db.session.delete(job)
        db.session.commit()
        FrontLogs('删除测试任务 name: %s 成功' % job.name).add_to_front_log()
        # app.logger.info('message:delete testcases success, id: %s' % id)
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
        from common.data.dynamic_variable import get_page
        user_id = session.get('user_id')
        page = request.args.get('page', 1, type=int)
        search = request_get_values('search')
        FrontLogs('进入测试任务列表页面 第%s页' % page).add_to_front_log()
        #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
        pagination = Job.query.filter(Job.name.like(
                "%"+search+"%") if search is not None else "", Job.user_id == user_id). \
            order_by(Job.timestamp.desc()).paginate(
            page, per_page=next(get_page), error_out=False)
        # 返回一个内容对象
        jobs = pagination.items
        return render_template('job/job_list.html', pagination=pagination, jobs=jobs, page=page, search=search)


class JobUpdateValidate(MethodView):

    def get(self):
        user_id = session.get('user_id')
        name = request.args.get('name')
        job_id = request.args.get('job_id')
        print('TestCaseSceneUpdateValidate:', name, job_id)
        job = Job.query.filter(
            Job.id != job_id, Job.name == name, Job.user_id == user_id).count()
        if job != 0:
            return jsonify(False)
        else:
            return jsonify(True)


job_blueprint.add_url_rule('/job_add/', view_func=JobAdd.as_view('job_add'))
job_blueprint.add_url_rule('/job_update/', view_func=JobUpdate.as_view('job_update'))
job_blueprint.add_url_rule('/job_list/', view_func=JobList.as_view('job_list'))
job_blueprint.add_url_rule('/job_delete/', view_func=JobDelete.as_view('job_delete'))

job_blueprint.add_url_rule('/job_scheduler_update/', view_func=JobSchedulerUpdate.as_view('job_scheduler_update'))

job_blueprint.add_url_rule('/job_update_validate/', view_func=JobUpdateValidate.as_view('job_update_validate'))


def scheduler_job(job, scheduler=None, cron_change=None):
    if not scheduler:
        from app import scheduler
    scheduler_job_id = 'job_' + str(job.id)
    print('scheduler_job:', job.id, job.is_start, job.mail_id, scheduler.get_jobs())
    mail = None
    if scheduler.get_job(scheduler_job_id) and not cron_change and job.is_start==1:
        print('此任务已在执行')
        return
    if job.cron and job.triggers:
        if job.mail_id:
            mail = Mail.query.get(job.mail_id)
        else:
            print('此任务没有配置邮件接收人')
        if job.is_start == 1:
            cron = job.cron.split(' ')
            print(cron)
            if len(cron) !=6:
                print('cron表达式不正确', job.name)
                return
            if cron_change:
                print('定时任务规则改变')

                try:
                    scheduler.remove_job(scheduler_job_id)
                except Exception as e:
                    print(e, '无此任务', job.name)
            scheduler.add_job(id=scheduler_job_id, func=auto_send_mail,
                                  trigger=job.triggers, year=cron[5], month=cron[4],
                              day=cron[3], hour=cron[2], minute=cron[1],
                                  second=cron[0], args=(job, mail))
            print('get_jobs:', scheduler.get_jobs(), scheduler.get_job(scheduler_job_id))

            print(scheduler.get_job('scheduler_job_id'))

        elif job.is_start == 0:
            print('get_jobs is:', scheduler.get_jobs())
            try:
                scheduler.remove_job(scheduler_job_id)
            except Exception as e:
                print(e, '无此任务', job.name)
                return
            print('get_jobs is_after:', scheduler.get_jobs())
        print('现在有的任务：', scheduler.get_jobs())
    else:
        print('未输入cron表达式或trigger')
        return


def print_job_name(job):
    print(job.name)


def auto_send_mail(job, mail):
    user_id = job.user_id
    testcases_ids = eval(job.testcases)
    testcase_scenes_ids = eval(job.testcase_scenes)
    testcase_time_id = get_testcase_time_id(user_id)
    post_request(testcases_ids, testcase_scenes_ids, testcase_time_id)
    get_report(testcase_time_id)
    if mail:
        if mail.email_method == 1:
            send_mail(mail.subject, mail.to_user_list.split(','), user_id=user_id, testcase_time_id=testcase_time_id)
        elif mail.email_method == 2:
            send_excel(mail.subject, mail.to_user_list.split(','), testcase_time_id=testcase_time_id)
        else:
            print('auto_send_mail:错误的邮件发送方式')


def get_testcase_time_id(user_id):
    from werkzeug.test import EnvironBuilder
    from app import return_app
    app = return_app()
    ctx = app.request_context(EnvironBuilder('/', 'http://localhost/').get_environ())
    # 构建一个request上下文对象放入app
    ctx.push()
    session['user_id'] = user_id
    time_strftime = datetime.now().strftime('%Y%m%d%H%M%S')
    testcase_time = TestCaseStartTimes(time_strftime=time_strftime, user_id=user_id)
    db.session.add(testcase_time)
    db.session.commit()
    return testcase_time.id


def post_request(testcases_ids, testcase_scenes_ids, testcase_time_id):
    for testcase_id in testcases_ids:
        post_testcase(testcase_id, testcase_time_id)
    for testcase_scene_id in testcase_scenes_ids:
        testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        for testcase_scene_testcase in testcase_scene.testcases:
            post_testcase(testcase_scene_testcase.id, testcase_time_id)


def init_scheduler():
    is_start_job = Job.query.filter(Job.is_start == 1).all()
    for job in is_start_job:
        scheduler_job(job)

