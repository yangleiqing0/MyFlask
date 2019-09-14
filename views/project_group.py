from flask import render_template, Blueprint, redirect, url_for, jsonify, session
from modles import User, db, ProjectGroup, TestCases
from flask.views import MethodView
from common.analysis_params import AnalysisParams
from common.connect_sqlite import cdb

project_group_blueprint = Blueprint('project_group_blueprint', __name__)


class ProjectGroupLook(MethodView):

    def get(self):
        user_id = session.get('user_id')
        testcases_urls = []
        project_group_id = User.query.get(user_id).project_group_id
        urls_sql = 'select testcases.url from testcases,users where testcases.user_id=users.id and users.project_group_id=%s'
        urls = list(set(cdb().query_db(urls_sql, params=(project_group_id,))))
        [testcases_urls.append(AnalysisParams().analysis_params(url[0])) for url in urls]
        testcases_urls.sort()
        return render_template('project_group/testcases.html', testcases_urls=testcases_urls)


project_group_blueprint.add_url_rule('/project_group_urls/', view_func=ProjectGroupLook.as_view('project_group_urls'))