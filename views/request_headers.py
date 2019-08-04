import json
from flask.views import MethodView
from common.tail_font_log import FrontLogs
from app import cdb, db, app
from modles.request_headers import RequestHeaders
from flask import render_template, Blueprint, request, redirect, url_for, current_app, jsonify

request_headers_blueprint = Blueprint('request_headers_blueprint', __name__)

class RequestHeadersAdd(MethodView):

    def get(self):
        FrontLogs('进入请求头部列表页面').add_to_front_log()
        return render_template('request_headers/request_headers_add.html')

    def post(self):
        name = request.form.get('name')
        FrontLogs('添加请求头部 name: %s' % name).add_to_front_log()
        value = request.form.get('value').replace(' ','').replace('\n', '').replace('\r', '')
        description = request.form.get('description')
        request_headers = RequestHeaders(name, value, description)
        db.session.add(request_headers)
        db.session.commit()
        FrontLogs('添加请求头部 name: %s 成功' % name).add_to_front_log()
        app.logger.info('message:insert into request_headers success, name: %s' % name)
        return redirect(url_for('request_headers_blueprint.request_headers_list'))


class RequestHeadersList(MethodView):

    def get(self):
        request_headers = RequestHeaders.query.all()
        print('request_headers:', request_headers)
        if request.is_xhr:
            request_headers_query_sql = 'select id,name from request_headers'
            request_headerses = cdb().query_db(request_headers_query_sql)
            request_headers_dict = {}
            for index, request_headers in enumerate(request_headerses):
                print('request_header:', request_headers)
                request_headers_dict.update({"index": index, "id%s" % index: request_headers[0], "name%s" % index: request_headers[1]})
            print("request_headers_dict: ", request_headers_dict)
            print('request_headers_list_ajax : True')
            return json.dumps({"request_headers_dict": str(request_headers_dict)})  # 需要转行成字符串再转成json
        page = request.args.get('page', 1, type=int)
        FrontLogs('进入请求头部列表 第%s页' % page).add_to_front_log()
        #  pagination是salalchemy的方法，第一个参数：当前页数，per_pages：显示多少条内容 error_out:True 请求页数超出范围返回404错误 False：反之返回一个空列表
        pagination = RequestHeaders.query.order_by(RequestHeaders.timestamp.desc()).paginate(page, per_page=current_app.config[
            'FLASK_POST_PRE_ARGV'], error_out=False)
        # 返回一个内容对象
        request_headerses = pagination.items
        print("request_headers_pagination: ", pagination)
        return render_template('request_headers/request_headers_list.html', pagination=pagination, items=request_headerses)



class RequestHeadersUpdate(MethodView):

    def get(self, id=-1):
        id = request.args.get('request_headers_id', id)# 如果有request_headers_id的get请求参数，那么用此参数作为id,否则就用id
        FrontLogs('进入修改请求头部 id: %s 页面' % id).add_to_front_log()
        request_headers = RequestHeaders.query.get(id)
        return render_template('request_headers/request_headers_update.html', item=request_headers)

    def post(self, id=-1):
        name = request.form.get('name')
        value = request.form.get('value')
        description = request.form.get('description')
        request_headers_update_sql = 'update request_headers set name=?,value=?,description=? where id=?'
        cdb().opeat_db(request_headers_update_sql, (name, value, description, id))
        FrontLogs('编辑请求头部 name: %s 成功' % name).add_to_front_log()
        app.logger.info('message:update request_headers success, name: %s' % name)
        return redirect(url_for('request_headers_blueprint.request_headers_list'))


class RequestHeadersDelete(MethodView):

    def get(self,id=-1):

        delete_request_headers_sql = 'delete from request_headers where id=?'
        cdb().opeat_db(delete_request_headers_sql, (id,))
        FrontLogs('删除请求头部 id: %s 成功' % id).add_to_front_log()
        app.logger.info('message:delete request_headers success, id: %s' % id)
        return redirect(url_for('request_headers_blueprint.request_headers_list'))


class RequestHeadersValidata(MethodView):

    def get(self):
        name = request.args.get('name')
        request_headers = RequestHeaders.query.filter(RequestHeaders.name == name).count()
        if request_headers != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class RequestHeadersUpdateValidata(MethodView):

    def get(self):
        name = request.args.get('name')
        request_headers_id = request.args.get('case_group_id')
        request_headers = RequestHeaders.query.filter(RequestHeaders.id != request_headers_id).filter(RequestHeaders.name == name).count()
        if request_headers != 0:
            return jsonify(False)
        else:
            return jsonify(True)


request_headers_blueprint.add_url_rule('/requestheadersadd/', view_func=RequestHeadersAdd.as_view('request_headers_add'))
request_headers_blueprint.add_url_rule('/requestheaderslist/', view_func=RequestHeadersList.as_view('request_headers_list'))
request_headers_blueprint.add_url_rule('/requestheadersupdate/<id>/', view_func=RequestHeadersUpdate.as_view('request_headers_update'))
request_headers_blueprint.add_url_rule('/requestheadersdelete/<id>/', view_func=RequestHeadersDelete.as_view('request_headers_delete'))

request_headers_blueprint.add_url_rule('/requestheadersvalidate/', view_func=RequestHeadersValidata.as_view('request_headers_validate'))
request_headers_blueprint.add_url_rule('/requestheadersupdatevalidate/', view_func=RequestHeadersUpdateValidata.as_view('request_headers_update_validate'))

