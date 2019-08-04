from flask.views import MethodView
from app import cdb, db, app
from modles.variables import Variables
from common.tail_font_log import FrontLogs
from flask import render_template, Blueprint, request, redirect, url_for, current_app, jsonify


variables_blueprint = Blueprint('variables_blueprint', __name__)


class VariableAdd(MethodView):

    def get(self):
        FrontLogs('进入添加全局变量页面').add_to_front_log()
        return render_template('variable/variable_add.html')

    def post(self):
        name = request.form.get('name')
        value = request.form.get('value')
        description = request.form.get('description', None)
        FrontLogs('开始添加全局变量 name: %s' % name).add_to_front_log()
        variable = Variables(name, value, description=description)
        db.session.add(variable)
        db.session.commit()
        FrontLogs('添加全局变量 name: %s 成功' % name).add_to_front_log()
        app.logger.info('message:insert into variables success, name: %s' % name)
        return redirect(url_for('variables_blueprint.variable_list'))


class VariableList(MethodView):

    def get(self):
        # 指定渲染的页数
        page = request.args.get('page', 1, type=int)
        FrontLogs('进入全局变量列表 第%s页' % page).add_to_front_log()
        #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
        pagination = Variables.query.order_by(Variables.timestamp.desc()).paginate(page, per_page=current_app.config[
            'FLASK_POST_PRE_ARGV'], error_out=False)
        # 返回一个内容对象
        variables = pagination.items
        print("pagination: ", pagination)
        return render_template('variable/variable_list.html', pagination=pagination, items=variables)



class VariableUpdate(MethodView):

    def get(self, id=-1):
        FrontLogs('进入编辑全局变量 id: %s 页面' % id).add_to_front_log()
        variable = Variables.query.get(id)
        return render_template('variable/variable_update.html', item=variable)

    def post(self, id=-1):
        name = request.form.get('name')
        value = request.form.get('value')
        description = request.form.get('description')
        variable_update_sql = 'update variables set name=?,value=?,description=? where id=?'
        cdb().opeat_db(variable_update_sql, (name, value, description, id))
        app.logger.info('message:update variables success, name: %s' % name)
        FrontLogs('编辑全局变量 name: %s 成功' % name).add_to_front_log()
        return redirect(url_for('variables_blueprint.variable_list'))



class VariableDelete(MethodView):

    def get(self,id=-1):
        delete_variables_sql = 'delete from variables where id=?'
        cdb().opeat_db(delete_variables_sql, (id,))
        FrontLogs('删除全局变量 id: %s 成功' % id).add_to_front_log()
        app.logger.info('message:delete variables success, id: %s' % id)
        return redirect(url_for('variables_blueprint.variable_list'))


class VariableValidata(MethodView):

    def get(self):
        name = request.args.get('name')
        variable = Variables.query.filter(Variables.name == name).count()
        if variable != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class VariableUpdateValidata(MethodView):

    def get(self):
        name = request.args.get('name')
        variable_id = request.args.get('variable_id')
        request_headers = Variables.query.filter(Variables.id != variable_id).filter(Variables.name == name).count()
        if request_headers != 0:
            return jsonify(False)
        else:
            return jsonify(True)


variables_blueprint.add_url_rule('/variableadd/', view_func=VariableAdd.as_view('variable_add'))
variables_blueprint.add_url_rule('/variablelist/', view_func=VariableList.as_view('variable_list'))
variables_blueprint.add_url_rule('/variableupdate/<id>/', view_func=VariableUpdate.as_view('variable_update'))
variables_blueprint.add_url_rule('/variabledelete/<id>/', view_func=VariableDelete.as_view('variable_delete'))

variables_blueprint.add_url_rule('/variablevalidate/', view_func=VariableValidata.as_view('variable_validate'))
variables_blueprint.add_url_rule('/variableupdatevalidate/', view_func=VariableUpdateValidata.as_view('variable_update_validate'))
