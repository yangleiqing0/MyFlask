from datetime import datetime, timedelta
from flask.views import MethodView
from flask import render_template, Blueprint, make_response, redirect, url_for, session, flash
from common.request_get_more_values import request_get_values
from common.connect_sqlite import cdb
from modles.user import User


login_blueprint = Blueprint('login_blueprint', __name__)


class Login(MethodView):

    def get(self):

        return render_template('login/login.html')

    def post(self):
        username, password = request_get_values('username', 'password')
        user_query_sql = 'select password from users where username=%s'
        pwd = cdb().query_db(user_query_sql, (username,), True)
        if pwd and password == pwd[0]:
            user = User.query.filter(User.username == username).first()
            resp = make_response(redirect(url_for('testcase_blueprint.test_case_list')))
            resp.set_cookie('SESSIONID', '{};{}'.format(username, password), path='/',
                            expires=datetime.now() + timedelta(days=7))
            session['username'] = username
            session['user_id'] = user.id
            return resp
        flash('账号或密码错误')
        return render_template('login/login.html')


class LoginOut(MethodView):

    def get(self):
        session['username'] = None
        session['user_id'] = None
        return redirect(url_for('login_blueprint.login'))


login_blueprint.add_url_rule('/login/', view_func=Login.as_view('login'))
login_blueprint.add_url_rule('/logout/', view_func=LoginOut.as_view('logout'))
