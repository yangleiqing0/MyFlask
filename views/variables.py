from flask.views import MethodView
from app import db
from common.connect_sqlite import cdb
from modles.variables import Variables
from modles.testcase import TestCases
from modles.user import User
from common.tail_font_log import FrontLogs
from common.request_get_more_values import request_get_values
from flask import render_template, Blueprint, request, redirect, url_for, current_app, jsonify, session


variables_blueprint = Blueprint('variables_blueprint', __name__)


class VariableAdd(MethodView):

    def get(self):
        FrontLogs('进入添加全局变量页面').add_to_front_log()
        return render_template('variable/variable_add.html')

    def post(self):
        user_id = session.get('user_id')
        name, value, description= request_get_values('name', 'value', 'description')
        FrontLogs('开始添加全局变量 name: %s' % name).add_to_front_log()
        variable = Variables(name, value, description=description, user_id=user_id)
        db.session.add(variable)
        db.session.commit()
        FrontLogs('添加全局变量 name: %s 成功' % name).add_to_front_log()
        # app.logger.info('message:insert into variables success, name: %s' % name)
        return redirect(url_for('variables_blueprint.variable_list'))


class VariableList(MethodView):

    def get(self):
        from common.data.dynamic_variable import get_page
        user_id = session.get('user_id')
        # 指定渲染的页数
        variable_search = request_get_values('variable_search')
        page = request.args.get('page', 1, type=int)
        FrontLogs('进入全局变量列表 第%s页' % page).add_to_front_log()
        #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
        if variable_search:
            pagination = Variables.query.filter(Variables.user_id == user_id, Variables.name.like(
                "%" + variable_search + "%")). \
                order_by(Variables.timestamp.desc()).paginate(1, per_page=next(get_page), error_out=False)
        else:
            pagination = Variables.query.filter(Variables.user_id == user_id,
                                                Variables.is_private ==0).\
                order_by(Variables.id.desc()).paginate(page, per_page=next(get_page), error_out=False)
        # 如果以创建时间进行排序，同一个时间内的个数大于设置的每页显示数，在每次进行筛选的时候都会不能显示超过显示数的
        # 相同时间记录的对象
        # 返回一个内容对象
        variables = pagination.items
        print("pagination: ", pagination, variables)
        return render_template('variable/variable_list.html', pagination=pagination, items=variables)


class VariableUpdate(MethodView):

    def get(self, id=-1):
        FrontLogs('进入编辑全局变量 id: %s 页面' % id).add_to_front_log()
        variable = Variables.query.get(id)
        return render_template('variable/variable_update.html', item=variable)

    def post(self, id=-1):
        name, value, description= request_get_values('name', 'value', 'description')
        variable_update_sql = 'update variables set name=%s,value=%s,description=%s where id=%s'
        cdb().opeat_db(variable_update_sql, (name, value, description, id))
        # app.logger.info('message:update variables success, name: %s' % name)
        FrontLogs('编辑全局变量 name: %s 成功' % name).add_to_front_log()
        return redirect(url_for('variables_blueprint.variable_list'))


class VariableDelete(MethodView):

    def get(self, id=-1):
        delete_variables_sql = 'delete from variables where id=%s'
        cdb().opeat_db(delete_variables_sql, (id,))
        FrontLogs('删除全局变量 id: %s 成功' % id).add_to_front_log()
        # app.logger.info('message:delete variables success, id: %s' % id)
        return redirect(url_for('variables_blueprint.variable_list'))


class VariableValidata(MethodView):

    def get(self):
        user_id = session.get('user_id')
        regist_variable, name =request_get_values('regist_variable', 'name')
        if regist_variable:
            variable = Variables.query.filter(Variables.name == regist_variable, Variables.user_id == user_id).count()
            if variable != 0:
                return jsonify(False)
            else:
                return jsonify(True)
        else:
            variable = Variables.query.filter(Variables.name == name, Variables.user_id == user_id).count()
            if variable != 0:
                return jsonify(False)
            else:
                return jsonify(True)


class OldSqlVariableValidata(MethodView):

    def get(self):
        user_id = session.get('user_id')
        old_sql_regist_variable = request_get_values('old_sql_regist_variable')
        if not old_sql_regist_variable:
            return jsonify(True)
        variable = Variables.query.filter(Variables.name == old_sql_regist_variable, Variables.user_id == user_id).count()
        if variable != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class NewSqlVariableValidata(MethodView):

    def get(self):
        user_id = session.get('user_id')
        new_sql_regist_variable = request_get_values('new_sql_regist_variable')
        if not new_sql_regist_variable:
            return jsonify(True)
        variable = Variables.query.filter(Variables.name == new_sql_regist_variable,
                                          Variables.user_id == user_id).count()
        if variable != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class OldSqlVariableUpdateValidata(MethodView):

    def get(self):
        user_id = session.get('user_id')
        old_sql_regist_variable, testcase_id = request_get_values('old_sql_regist_variable', 'testcase_id')
        print('OldSqlVariableUpdateValidata:', old_sql_regist_variable, testcase_id)
        testcase = TestCases.query.get(testcase_id)
        if not old_sql_regist_variable:
            return jsonify(True)
        var = Variables.query.filter(Variables.name == testcase.old_sql_regist_variable).first()
        # print('OldSqlVariableUpdateValidata var:', var, var.id)
        if var:
            variable = Variables.query.filter(
                Variables.id != var.id, Variables.name == old_sql_regist_variable, Variables.user_id == user_id).count()
        else:
            variable = Variables.query.filter(
                Variables.name == old_sql_regist_variable, Variables.user_id == user_id).count()
        if variable != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class NewSqlVariableUpdateValidata(MethodView):

    def get(self):
        user_id = session.get('user_id')
        new_sql_regist_variable, testcase_id = request_get_values('new_sql_regist_variable', 'testcase_id')
        testcase = TestCases.query.get(testcase_id)
        print('new_sql_regist_variable:', new_sql_regist_variable)
        if not new_sql_regist_variable:
            return jsonify(True)
        var = Variables.query.filter(Variables.name == testcase.new_sql_regist_variable).first()
        if var:
            variable = Variables.query.filter(
                Variables.id != var.id, Variables.name == new_sql_regist_variable, Variables.user_id == user_id).count()
        else:
            variable = Variables.query.filter(
                Variables.name == new_sql_regist_variable, Variables.user_id == user_id).count()
        if variable != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class VariableUpdateValidata(MethodView):

    def get(self):
        user_id = session.get('user_id')
        variable_id, name, testcase_id, regist_variable = request_get_values('variable_id', 'name', 'testcase_id', 'regist_variable')
        print('VariableUpdateValidata: %s, %s, %s, %s' %(variable_id, name, testcase_id, regist_variable))
        if variable_id:
            variables = Variables.query.filter(
                Variables.id != variable_id, Variables.name == name, Variables.user_id == user_id).count()
            if variables != 0:
                return jsonify(False)
            else:
                return jsonify(True)
        else:
            testcase = TestCases.query.get(testcase_id)
            var = Variables.query.filter(Variables.name == testcase.regist_variable).first()
            print('VariableUpdateValidata var: ', var)
            if var:
                variable = Variables.query.filter(
                    Variables.id != var.id, Variables.name == regist_variable, Variables.user_id == user_id).count()
            else:
                variable = Variables.query.filter(
                    Variables.name == regist_variable, Variables.user_id == user_id).count()
            if variable != 0:
                return jsonify(False)
            else:
                return jsonify(True)


variables_blueprint.add_url_rule('/variableadd/', view_func=VariableAdd.as_view('variable_add'))
variables_blueprint.add_url_rule('/variablelist/', view_func=VariableList.as_view('variable_list'))
variables_blueprint.add_url_rule('/variableupdate/<id>/', view_func=VariableUpdate.as_view('variable_update'))
variables_blueprint.add_url_rule('/variabledelete/<id>/', view_func=VariableDelete.as_view('variable_delete'))

variables_blueprint.add_url_rule('/variable_validate/', view_func=VariableValidata.as_view('variable_validate'))
variables_blueprint.add_url_rule('/variableupdatevalidate/', view_func=VariableUpdateValidata.as_view('variable_update_validate'))
variables_blueprint.add_url_rule('/old_sql_regist_variable/', view_func=OldSqlVariableValidata.as_view('old_sql_regist_variable'))
variables_blueprint.add_url_rule('/new_sql_regist_variable/', view_func=NewSqlVariableValidata.as_view('new_sql_regist_variable'))
variables_blueprint.add_url_rule('/old_sql_regist_update_variable/', view_func=OldSqlVariableUpdateValidata.as_view('old_sql_regist_update_variable'))
variables_blueprint.add_url_rule('/new_sql_regist_update_variable/', view_func=NewSqlVariableUpdateValidata.as_view('new_sql_regist_update_variable'))