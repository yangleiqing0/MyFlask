import json
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, current_app
from modles.case_group import CaseGroup
from modles.request_headers import RequestHeaders
from app import cdb, db, app


case_group_blueprint = Blueprint('case_group_blueprint',__name__)


class CaseGroupAdd(MethodView):

    def get(self):
        return render_template('case_group_add.html')

    def post(self):
        name = request.form.get('name')
        description = request.form.get('description')
        case_group = CaseGroup(name, description)
        db.session.add(case_group)
        db.session.commit()
        app.logger.info('message:insert into case_group success, name: %s' % name)
        return redirect(url_for('case_group_blueprint.case_group_list'))


class CaseGroupList(MethodView):

    def get(self):
        case_groups = CaseGroup.query.all()
        print('case_groups: ', case_groups)
        if request.is_xhr:
            case_groups_query_sql = 'select id,name from case_group'
            case_groups = cdb().query_db(case_groups_query_sql)
            case_groups_dict = {}
            for index, case_group in enumerate(case_groups):
                print('case_group:', case_group)
                case_groups_dict.update({"index": index, "id%s" % index: case_group[0], "name%s" % index: case_group[1]})
            print("case_groups_dict: ", case_groups_dict)
            print('case_group_list_ajax : True')
            return json.dumps({"case_groups_dict": str(case_groups_dict)})  # 需要转行成字符串再转成json
        else:
            page = request.args.get('page', 1, type=int)
            #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
            pagination = CaseGroup.query.order_by(CaseGroup.timestamp.desc()).paginate(page,
                                                                                       per_page=current_app.config[
                                                                                           'FLASK_POST_PRE_ARGV'],
                                                                                       error_out=False)
            # 返回一个内容对象
            case_groups = pagination.items
            print("pagination: ", pagination)
            return render_template('case_group_list.html', pagination=pagination, items=case_groups)



class CaseGroupUpdate(MethodView):

    def get(self, id=-1):
        id = request.args.get('case_group_id', id) # 如果有case_group_id的get请求参数，那么用此参数作为id,否则就用id
        case_group = CaseGroup.query.get(id)
        print('case_group:', case_group)
        return render_template('case_group_update.html', item=case_group)

    def post(self, id=-1):
        name = request.form.get('name')
        description = request.form.get('description')
        case_group_update_sql = 'update case_group set name=?,description=? where id=?'
        cdb().opeat_db(case_group_update_sql, (name, description, id))
        app.logger.info('message:update case_group success, name: %s' % name)
        return redirect(url_for('case_group_blueprint.case_group_list'))



class CaseGroupDelete(MethodView):

    def get(self,id=-1):
        delete_case_group_sql = 'delete from case_group where id=?'
        cdb().opeat_db(delete_case_group_sql, (id,))
        app.logger.info('message:delete case_group success, id: %s' % id)
        return redirect(url_for('case_group_blueprint.case_group_list'))


class CaseGroupSearchCase(MethodView):

    def get(self, id=-1):
        case_group = CaseGroup.query.get(id)
        print('CaseGroupSearchCase:case_group: ',case_group)
        testcases = case_group.testcases
        print('CaseGroupSearchCase:testcases: ', testcases)
        request_headers = RequestHeaders.query.all()
        print('CaseGroupSearchCase:request_headers: ', request_headers)
        return render_template('case_group_search_case.html',
                               items=testcases, case_group=case_group,
                               request_headers=request_headers)


case_group_blueprint.add_url_rule('/addcasegroup/', view_func=CaseGroupAdd.as_view('case_group_add'))
case_group_blueprint.add_url_rule('/casegrouplist/', view_func=CaseGroupList.as_view('case_group_list'))
case_group_blueprint.add_url_rule('/casegroupupdate/<id>/', view_func=CaseGroupUpdate.as_view('case_group_update'))
case_group_blueprint.add_url_rule('/casegroupdelete/<id>/', view_func=CaseGroupDelete.as_view('case_group_delete'))
case_group_blueprint.add_url_rule('/casegroupsearchcase/<id>/', view_func=CaseGroupSearchCase.as_view('case_group_search_case'))