from flask.views import MethodView
from flask import render_template, Blueprint, request


system_config_blueprint = Blueprint('system_config_blueprint', __name__)


class EmailConfig(MethodView):

    def get(self):
        return render_template('system_config/email_config.html')


system_config_blueprint.add_url_rule('/emailconfig/', view_func=EmailConfig.as_view('email_config'))