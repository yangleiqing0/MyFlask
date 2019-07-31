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


home_blueprint.add_url_rule('/', view_func=Home.as_view('home'))
home_blueprint.add_url_rule('/test/', view_func=Test.as_view('test'))