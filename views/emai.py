#coding=utf-8
from datetime import datetime
import json
from flask.views import MethodView
from flask import render_template, Blueprint, redirect, url_for, session, request, current_app, jsonify
from common.request_get_more_values import request_get_values
from common.send_mail import send_excel
from common.tail_font_log import FrontLogs
from modles.job import Job
from modles.mail import Mail
from modles.testcase_scene import TestCaseScene
from modles.testcase_start_times import TestCaseStartTimes
from modles.user import User
from app import db


mail_blueprint = Blueprint('mail_blueprint', __name__)


class MailAdd(MethodView):

    def get(self):
        return render_template('mail/mail_add.html')

    def post(self):
        user_id = session.get('user_id')
        name, subject, to_user_list, email_method = request_get_values(
            'name', 'subject', 'to_user_list', 'email_method')
        mail = Mail(name, subject, user_id, to_user_list, email_method)
        db.session.add(mail)
        db.session.commit()
        FrontLogs('添加邮件配置 name: %s 成功' % name).add_to_front_log()
        return redirect(url_for('mail_blueprint.mail_list'))


class MailUpdate(MethodView):

    def get(self):
        mail_id = request_get_values('mail_id')
        mail = Mail.query.get(mail_id)
        FrontLogs('进入编辑邮件配置 name: %s 页面' % mail.name).add_to_front_log()
        return render_template('mail/mail_update.html', mail=mail)

    def post(self):
        mail_id, name, subject, to_user_list, email_method = request_get_values(
            'mail_id', 'name', 'subject', 'to_user_list', 'email_method')
        print('MailUpdate post:', to_user_list.split(','))
        mail = Mail.query.get(mail_id)
        mail.name = name
        mail.subject = subject
        mail.to_user_list = to_user_list
        mail.email_method =email_method
        db.session.commit()
        FrontLogs('编辑邮件配置 name: %s 页面成功' % name).add_to_front_log()
        return redirect(url_for('mail_blueprint.mail_list'))


class MailList(MethodView):
    def get(self):
        user_id = session.get('user_id')
        mail_search = request_get_values('mail_search')
        page = request.args.get('page', 1, type=int)
        FrontLogs('进入邮件配置列表页面 第%s页' % page).add_to_front_log()
        #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
        pagination = Mail.query.filter(Mail.name.like(
                "%"+mail_search+"%") if mail_search is not None else "", Mail.user_id == user_id). \
            order_by(Mail.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASK_POST_PRE_ARGV'], error_out=False)
        # 返回一个内容对象
        mails = pagination.items
        return render_template('mail/mail_list.html', pagination=pagination, mails=mails)


class MailDelete(MethodView):

    def get(self):
        mail_id = request_get_values('mail_id')
        mail = Mail.query.get(mail_id)
        db.session.delete(mail)
        db.session.commit()
        FrontLogs('删除邮件配置 name: %s 成功' % mail.name).add_to_front_log()
        return redirect(url_for('mail_blueprint.mail_list'))


class MailNameValidate(MethodView):

    def get(self):
        user_id = session.get('user_id')
        name = request.args.get('name')
        mail = Mail.query.filter(Mail.name == name, Mail.user_id == user_id).count()
        if mail != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class MailNameUpdateValidate(MethodView):

    def get(self):
        user_id = session.get('user_id')
        name, mail_id = request_get_values('name', 'mail_id')
        mail = Mail.query.filter(Mail.id != mail_id, Mail.name == name, Mail.user_id == user_id).count()
        if mail != 0:
            return jsonify(False)
        else:
            return jsonify(True)


mail_blueprint.add_url_rule('/mail_add/', view_func=MailAdd.as_view('mail_add'))
mail_blueprint.add_url_rule('/mail_update/', view_func=MailUpdate.as_view('mail_update'))
mail_blueprint.add_url_rule('/mail_list/', view_func=MailList.as_view('mail_list'))
mail_blueprint.add_url_rule('/mail_delete/', view_func=MailDelete.as_view('mail_delete'))

mail_blueprint.add_url_rule('/email_name_validate/', view_func=MailNameValidate.as_view('email_name_validate'))
mail_blueprint.add_url_rule('/email_name_update_validate/', view_func=MailNameUpdateValidate.as_view('email_name_update_validate'))
