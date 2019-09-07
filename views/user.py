#coding=utf-8
from common.tail_font_log import FrontLogs
from flask.views import MethodView
from flask import render_template, Blueprint, redirect, url_for, jsonify
from common.request_get_more_values import request_get_values
from common.pre_db_insert_data import add_pre_data_go
from modles import User, db

user_blueprint = Blueprint('user_blueprint', __name__)


class UserRegist(MethodView):

    def get(self):
        FrontLogs('进入添加用户页面').add_to_front_log()
        return render_template('user/user_regist.html')

    def post(self):
        username, password = request_get_values('username', 'password')
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        new_user = User.query.filter(User.username == username).first().id
        add_pre_data_go(new_user)
        FrontLogs('添加用户 name : %s 成功 ' % username).add_to_front_log()
        return redirect(url_for('login_blueprint.login'))


class UserRegistValidate(MethodView):

    def get(self):
        username = request_get_values('username')
        user_count = User.query.filter(User.username == username).count()
        if user_count != 0:
            return jsonify(False)
        else:
            return jsonify(True)


user_blueprint.add_url_rule('/user_regist/', view_func=UserRegist.as_view('user_regist'))

user_blueprint.add_url_rule('/user_regist_validate/', view_func=UserRegistValidate.as_view('user_regist_validate'))

