from flask.views import MethodView
from app import cdb
from modles.request_headers import RequestHeaders
from flask import render_template,Blueprint,request

request_headers_blueprint = Blueprint('request_headers_blueprint', __name__)

class RequestHeadersAdd(MethodView):

    def get(self):
        return render_template('request_headers_add.html')

    def post(self):
        name = request.form.get('name')
        value = request.form.get('value')
        description = request.form.get('description')
        request_headers__add_sql = 'insert into request_headers values (?,?,?,?)'
        cdb().opeat_db(request_headers__add_sql, (None, name, value, description))
        return '添加头部成功'

class RequestHeadersList(MethodView):

    def get(self):
        request_headers = RequestHeaders.query.all()
        print('request_headers:', request_headers)
        return render_template('request_headers_list.html', items=request_headers)


request_headers_blueprint.add_url_rule('/requestheadersadd/', view_func=RequestHeadersAdd.as_view('request_headers_add'))
request_headers_blueprint.add_url_rule('/requestheaderslist/', view_func=RequestHeadersList.as_view('request_headers_list'))