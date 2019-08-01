import json
from logs.config import FRONT_LOGS_FILE, FLASK_LOGS_FILE
from flask.views import MethodView
from flask import render_template, Blueprint, request

home_blueprint = Blueprint('home_blueprint', __name__)


class Home(MethodView):

    def get(self):
        return render_template('home.html')

class Test(MethodView):
    
    def get(self):
        print(request.args.get('id'))
        return request.form
    
    def post(self):
        print(request.args)
        return request.form


class FrontLog(MethodView):

    def get(self):
        with open(FRONT_LOGS_FILE) as logs:
            front_logs = logs.readlines()
            front_logs = "<br/>".join(front_logs[len(front_logs)-10:])
        print(front_logs[len(front_logs)-10:], "front_logs: ", front_logs)
        return json.dumps({"front_logs": str(front_logs)})


class FlaskLog(MethodView):

    def get(self):
        with open(FLASK_LOGS_FILE) as logs:
            flask_logs = logs.readlines()
            flask_logs = "<br/>".join(flask_logs[len(flask_logs)-8:])
        print(flask_logs[len(flask_logs)-8:], "flask_logs: ", flask_logs)
        return json.dumps({"flask_logs": str(flask_logs)})


home_blueprint.add_url_rule('/', view_func=Home.as_view('home'))
home_blueprint.add_url_rule('/test/', view_func=Test.as_view('test'))
home_blueprint.add_url_rule('/frontlogs/', view_func=FrontLog.as_view('front_logs'))
home_blueprint.add_url_rule('/flasklogs/', view_func=FlaskLog.as_view('flask_logs'))