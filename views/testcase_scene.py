import datetime
import json
import time
from common.tail_font_log import FrontLogs
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, current_app, jsonify
from modles.testcase import TestCases
from modles.testcase_scene import TestCaseScene
from app import db
from common.execute_testcase import to_execute_testcase


testcase_scene_blueprint = Blueprint('testcase_scene_blueprint', __name__)


class TestCaseSceneAdd(MethodView):

    def get(self):
        return render_template('testcase_scene/testcase_scene_add.html')

    def post(self):
        name = request.form.get('name')
        description = request.form.get('description')
        testcase_scene = TestCaseScene(name, description)
        db.session.add(testcase_scene)
        db.session.commit()
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list'))


class TestCaseSceneTestCaseList(MethodView):

    def get(self):
        model_testcases = TestCases.query.filter(TestCases.is_model == 1).all()
        page = request.args.get('page', 1, type=int)
        FrontLogs('进入测试场景列表 第%s页' % page).add_to_front_log()

        pagination = TestCaseScene.query.order_by(TestCaseScene.timestamp.desc()).paginate(page, per_page=
        current_app.config['FLASK_POST_PRE_ARGV'], error_out=False)
        # 返回一个内容对象
        testcase_scenes = pagination.items
        print("request_headers_pagination: ", pagination)
        return render_template('testcase_scene/testcase_scene_testcase_list.html', testcase_scenes=testcase_scenes,
                               model_testcases=model_testcases, pagination=pagination)

    def post(self):
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list'))


class TestCaseSceneRun(MethodView):

    def get(self):
        testcase_scene_id = request.args.get('testcase_scene_id')
        testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        testcases = testcase_scene.testcases
        testcase_results = []
        for testcase in testcases:
            testcase_result = to_execute_testcase(testcase)
            testcase_results.extend(['【%s】' % testcase.name, testcase_result])
        testcase_results_html = '<br>'.join(testcase_results)
        print('TestCaseSceneRun: ', json.dumps({'testcase_results': testcase_results_html}))
        return json.dumps({'testcase_results': testcase_results_html})


class TestCaseSceneDelete(MethodView):

    def get(self):
        testcase_scene_id = request.args.get('testcase_scene_id')
        testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        testcases = testcase_scene.testcases
        for testcase in testcases:
            db.session.delete(testcase)
            FrontLogs('删除测试场景 id： %s  关联的测试用例名称 %s' % (testcase_scene_id, testcase.name)).add_to_front_log()
        db.session.delete(testcase_scene)
        db.session.commit()
        FrontLogs('删除测试场景 id： %s' % testcase_scene_id).add_to_front_log()
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list'))

    def post(self):
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list'))


class TestCaseSceneTestCaseCopy(MethodView):

    def get(self):
        testcase_scene_id = request.args.get('testcase_scene_id')
        testcase_id = request.args.get('testcase_id')
        testcase = TestCases.query.get(testcase_id)

        timestr = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        name = testcase.name + timestr
        db.session.add(TestCases(name, testcase.url, testcase.data, testcase.regist_variable,
                       testcase.regular, testcase.method, testcase.group_id, testcase.request_headers_id,
                       testcase_scene_id, testcase.hope_result))
        db.session.commit()
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list'))

    def post(self):
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list'))


class TestCaseSceneAddValidate(MethodView):

    def get(self):
        name = request.args.get('name')
        testcase = TestCaseScene.query.filter(TestCaseScene.name == name).count()
        if testcase != 0:
            return jsonify(False)
        else:
            return jsonify(True)


testcase_scene_blueprint.add_url_rule('/testcase_scene_add/', view_func=TestCaseSceneAdd.as_view('testcase_scene_add'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_copy/', view_func=TestCaseSceneTestCaseCopy.as_view('testcase_scene_copy'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_testcase_list/', view_func=TestCaseSceneTestCaseList.as_view('testcase_scene_testcase_list'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_delete/', view_func=TestCaseSceneDelete.as_view('testcase_scene_delete'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_run/', view_func=TestCaseSceneRun.as_view('testcase_scene_run'))

testcase_scene_blueprint.add_url_rule('/testcase_scene_add_validate/', view_func=TestCaseSceneAddValidate.as_view('testcase_scene_add_validate'))

