import json
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, current_app, jsonify, session
from modles.case_group import CaseGroup
from modles.request_headers import RequestHeaders
from modles.testcase import TestCases
from common.tail_font_log import FrontLogs
from common.request_get_more_values import request_get_values
from app import db
from common.connect_sqlite import cdb
from modles.user import User


case_group_blueprint = Blueprint('case_group_blueprint', __name__)


class CaseGroupAdd(MethodView):

    def get(self):
        FrontLogs('进入测试用例分组添加页面').add_to_front_log()
        return render_template('case_group/case_group_add.html')

    def post(self):
        user_id =session.get('user_id')
        name, description = request_get_values('name', 'description')
        FrontLogs('开始添加测试用例分组 name: %s ' % name).add_to_front_log()
        case_group = CaseGroup(name, description, user_id)
        db.session.add(case_group)
        db.session.commit()
        FrontLogs('开始添加测试用例分组 name: %s 成功' % name).add_to_front_log()
        # app.logger.info('message:insert into case_group success, name: %s' % name)
        return redirect(url_for('case_group_blueprint.case_group_list'))


class CaseGroupList(MethodView):
    def get(self):
        user_id =session.get('user_id')
        case_group_search = request_get_values('case_group_search')
        user = User.query.get(user_id)
        case_groups = user.user_case_groups
        print('case_groups: ', case_groups)
        if request.is_xhr:
            case_groups_query_sql = 'select id,name from case_group where user_id=%s'
            case_groups = cdb().query_db(case_groups_query_sql, (user_id,))
            case_groups_dict = {}
            for index, case_group in enumerate(case_groups):
                print('case_group:', case_group)
                case_groups_dict.update({"index": index, "id%s" % index: case_group[0], "name%s" % index: case_group[1]})
            print("case_groups_dict: ", case_groups_dict)
            print('case_group_list_ajax : True')
            return json.dumps({"case_groups_dict": str(case_groups_dict)})  # 需要转行成字符串再转成json
        else:
            page = request.args.get('page', 1, type=int)
            FrontLogs('进入测试用例分组列表页面 第%s页' % page).add_to_front_log()
            #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
            from common.data.dynamic_variable import get_page
            pagination = CaseGroup.query.filter(CaseGroup.name.like(
                "%"+case_group_search+"%") if case_group_search is not None else "", CaseGroup.user_id == user_id).\
                order_by(CaseGroup.timestamp.desc()).paginate(
                page, per_page=next(get_page), error_out=False)
            # 返回一个内容对象
            case_groups = pagination.items
            print("pagination: ", pagination)
            return render_template('case_group/case_group_list.html', pagination=pagination, items=case_groups)


class CaseGroupUpdate(MethodView):

    def get(self, id=-1):
        FrontLogs('进入编辑测试用例分组 id:%s 页面' % id).add_to_front_log()
        id = request.args.get('case_group_id', id) # 如果有case_group_id的get请求参数，那么用此参数作为id,否则就用id
        case_group = CaseGroup.query.get(id)
        print('case_group:', case_group)
        return render_template('case_group/case_group_update.html', item=case_group)

    def post(self, id=-1):
        name, description = request_get_values('name', 'description')
        case_group = CaseGroup.query.get(id)
        case_group.name = name
        case_group.description = description
        db.session.commit()
        FrontLogs('编辑测试用例分组 name:%s 成功' % name).add_to_front_log()
        # app.logger.info('message:update case_group success, name: %s' % name)
        return redirect(url_for('case_group_blueprint.case_group_list'))


class CaseGroupDelete(MethodView):

    def get(self, id=-1):
        case_group = CaseGroup.query.get(id)
        db.session.delete(case_group)
        db.session.commit()
        FrontLogs('删除测试用例分组 id:%s 成功' % id).add_to_front_log()
        # app.logger.info('message:delete case_group success, id: %s' % id)
        return redirect(url_for('case_group_blueprint.case_group_list'))


class CaseGroupSearchCase(MethodView):

    def get(self, id=-1):
        user_id = session.get('user_id')
        case_group = CaseGroup.query.get(id)
        print('CaseGroupSearchCase:case_group: ', case_group)
        testcases = TestCases.query.filter(TestCases.group_id == id, TestCases.user_id == user_id, TestCases.testcase_scene_id.is_(None)).all()
        print('CaseGroupSearchCase:testcases: ', testcases)
        request_headers = RequestHeaders.query.all()
        print('CaseGroupSearchCase:request_headers: ', request_headers)
        FrontLogs('进入测试用例分组  id:%s 关联测试用例页面' % id).add_to_front_log()
        return render_template('case_group/case_group_search_case.html',
                               items=testcases, case_group=case_group,
                               request_headers=request_headers)


class CaseGroupValidata(MethodView):

    def get(self):
        user_id =session.get('user_id')
        name = request.args.get('name')
        case_group = CaseGroup.query.filter(CaseGroup.name == name, CaseGroup.user_id == user_id).count()
        if case_group != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class CaseGroupUpdateValidata(MethodView):

    def get(self):
        user_id = session.get('user_id')
        name, case_group_id = request_get_values('name', 'case_group_id')
        case_group = CaseGroup.query.filter(
            CaseGroup.id != case_group_id, CaseGroup.name == name, CaseGroup.user_id == user_id).count()
        if case_group != 0:
            return jsonify(False)
        else:
            return jsonify(True)


case_group_blueprint.add_url_rule('/addcasegroup/', view_func=CaseGroupAdd.as_view('case_group_add'))
case_group_blueprint.add_url_rule('/casegrouplist/', view_func=CaseGroupList.as_view('case_group_list'))
case_group_blueprint.add_url_rule('/casegroupupdate/<id>/', view_func=CaseGroupUpdate.as_view('case_group_update'))
case_group_blueprint.add_url_rule('/casegroupdelete/<id>/', view_func=CaseGroupDelete.as_view('case_group_delete'))
case_group_blueprint.add_url_rule('/casegroupsearchcase/<id>/', view_func=CaseGroupSearchCase.as_view('case_group_search_case'))

case_group_blueprint.add_url_rule('/casegroupvalidate/', view_func=CaseGroupValidata.as_view('case_group_validate'))
case_group_blueprint.add_url_rule('/casegroupupdatevalidate/', view_func=CaseGroupUpdateValidata.as_view('case_group_update_validate'))