from flask.views import MethodView
from app import cdb
from modles.variables import Variables
from flask import render_template,Blueprint,request,redirect,url_for

variables_blueprint = Blueprint('variables_blueprint', __name__)

class VariableAdd(MethodView):

    def get(self):
        return render_template('variable_add.html')

    def post(self):
        name = request.form.get('name')
        value = request.form.get('value')
        description = request.form.get('description')
        variable_add_sql = 'insert into variables values (?,?,?,?)'
        cdb().opeat_db(variable_add_sql, (None, name, value, description))
        return '插入全部变量成功'

class VariableList(MethodView):

    def get(self):
        tests = Variables.query.all()
        print(tests)
        return render_template('variable_list.html', items=tests)


class VariableUpdate(MethodView):

    def get(self, id=-1):
        variable = Variables.query.get(id)
        return render_template('variable_update.html', item=variable)

    def post(self, id=-1):
        name = request.form.get('name')
        value = request.form.get('value')
        description = request.form.get('description')
        variable_update_sql = 'update variables set name=?,value=?,description=? where id=?'
        cdb().opeat_db(variable_update_sql, (name, value, description, id))
        return '修改全局变量成功'


class VariableDelete(MethodView):

    def get(self,id=-1):
        print('删除全局变量')
        delete_variables_sql = 'delete from variables where id=?'
        cdb().opeat_db(delete_variables_sql, (id,))
        return redirect(url_for('variables_blueprint.variable_list'))

variables_blueprint.add_url_rule('/variableadd/', view_func=VariableAdd.as_view('variable_add'))
variables_blueprint.add_url_rule('/variablelist/', view_func=VariableList.as_view('variable_list'))
variables_blueprint.add_url_rule('/variableupdate/<id>/', view_func=VariableUpdate.as_view('variable_update'))
variables_blueprint.add_url_rule('/variabledelete/<id>/', view_func=VariableDelete.as_view('variable_delete'))