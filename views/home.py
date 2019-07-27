from flask.views import MethodView
from flask import render_template
from flask import Blueprint

home_blueprint = Blueprint('home_blueprint', __name__)


class Home(MethodView):

    def get(self):
        return render_template('homepage.html')


home_blueprint.add_url_rule('/', view_func=Home.as_view('home'))