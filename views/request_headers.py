from flask.views import MethodView
from app import cdb
from modles.request_headers import RequestHeaders
from flask import render_template, Blueprint, request, redirect, url_for

request_headers_blueprint = Blueprint('request_headers_blueprint', __name__)

class RequestHeadersAdd(MethodView):

    def get(self):
        return render_template('request_headers_add.html')

    def post(self):
        name = request.form.get('name')
        value = request.form.get('value').replace(' ','').replace('\n', '').replace('\r', '')
        description = request.form.get('description')
        request_headers__add_sql = 'insert into request_headers values (?,?,?,?)'
        cdb().opeat_db(request_headers__add_sql, (None, name, value, description))
        return '添加头部成功'


class RequestHeadersList(MethodView):

    def get(self):
        request_headers = RequestHeaders.query.all()
        print('request_headers:', request_headers)
        return render_template('request_headers_list.html', items=request_headers)


class RequestHeadersUpdate(MethodView):

    def get(self, id=-1):
        request_headers = RequestHeaders.query.get(id)
        return render_template('request_headers_update.html', item=request_headers)

    def post(self, id=-1):
        name = request.form.get('name')
        value = request.form.get('value')
        description = request.form.get('description')
        request_headers_update_sql = 'update request_headers set name=?,value=?,description=? where id=?'
        cdb().opeat_db(request_headers_update_sql, (name, value, description, id))
        return '修改请求头部成功'

class RequestHeadersDelete(MethodView):

    def get(self,id=-1):
        print('删除请求头部')
        delete_request_headers_sql = 'delete from request_headers where id=?'
        cdb().opeat_db(delete_request_headers_sql, (id,))
        return redirect(url_for('request_headers_blueprint.request_headers_list'))


request_headers_blueprint.add_url_rule('/requestheadersadd/', view_func=RequestHeadersAdd.as_view('request_headers_add'))
request_headers_blueprint.add_url_rule('/requestheaderslist/', view_func=RequestHeadersList.as_view('request_headers_list'))
request_headers_blueprint.add_url_rule('/requestheadersupdate/<id>/', view_func=RequestHeadersUpdate.as_view('request_headers_update'))
request_headers_blueprint.add_url_rule('/requestheadersdelete/<id>/', view_func=RequestHeadersDelete.as_view('request_headers_delete'))
