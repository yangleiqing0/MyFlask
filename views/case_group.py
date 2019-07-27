from flask.views import MethodView
from flask import render_template,Blueprint,request
from modles.case_group import CaseGroup
from app import cdb

case_group_blueprint = Blueprint('case_group_blueprint',__name__)

class CaseGroupAdd(MethodView):

    def get(self):
        return render_template('add_case_group.html')

    def post(self):
        name = request.form.get('name')
        description = request.form.get('description')
        case_group_add_sql = 'insert into case_group values (?,?,?)'
        cdb().opeat_db(case_group_add_sql,(None, name, description))
        return '插入测试用例分组成功'


class CaseGroupList(MethodView):

    def get(self):
        tests = CaseGroup.query.all()
        print(tests)
        return render_template('case_group_list.html', items=tests)


case_group_blueprint.add_url_rule('/addcasegroup/', view_func=CaseGroupAdd.as_view('add_case_group'))
case_group_blueprint.add_url_rule('/casegrouplist/', view_func=CaseGroupList.as_view('case_group_list'))
