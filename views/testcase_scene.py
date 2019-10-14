import datetime
import json
from common.tail_font_log import FrontLogs
from flask.views import MethodView
from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session, flash
from common.request_get_more_values import request_get_values
from common.execute_testcase import to_execute_testcase
from views.testcase_request import post_testcase
from modles import db, TestCases, TestCaseScene, User, Wait, Variables
from . import edit

testcase_scene_blueprint = Blueprint('testcase_scene_blueprint', __name__)


class TestCaseSceneUpdate(MethodView):

    def get(self):
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        page= request_get_values('page')
        print('TestCaseSceneUpdate page: ', page)
        case_groups = user.user_case_groups
        testcase_scene_id = request.args.get('id')
        if testcase_scene_id:
            testcase_scene = TestCaseScene.query.get(testcase_scene_id)
            FrontLogs('进入编辑测试场景 name： %s 页面' % testcase_scene.name).add_to_front_log()
            return render_template('testcase_scene/scene_edit.html', testcase_scene=testcase_scene,
                                   case_groups=case_groups, page=page)
        FrontLogs('进入测试场景添加页面').add_to_front_log()
        return render_template('testcase_scene/scene_edit.html', case_groups=case_groups, page=page)

    def post(self):
        return edit(TestCaseScene, '测试场景', 'testcase_scene_blueprint', 'testcase_scene_testcase_list')


class TestCaseSceneTestCaseList(MethodView):

    def get(self):
        from common.data.dynamic_variable import get_page
        user_id = session.get('user_id')
        search = request_get_values('search')
        model_testcase_scenes = TestCaseScene.query.filter(TestCaseScene.is_model == 1, TestCaseScene.user_id == user_id).all()
        model_testcases = TestCases.query.filter(TestCases.is_model == 1, TestCases.user_id == user_id).all()
        page = request.args.get('page', 1, type=int)
        FrontLogs('进入测试场景列表 第%s页' % page).add_to_front_log()

        pagination = TestCaseScene.query.filter(TestCaseScene.name.like(
                "%"+search+"%") if search is not None else "", TestCaseScene.user_id == user_id).order_by(
            TestCaseScene.updated_time.desc(), TestCaseScene.id.desc()).paginate(page, per_page=
        next(get_page), error_out=False)
        # 返回一个内容对象
        testcase_scenes = pagination.items
        print("request_headers_pagination: ", testcase_scenes)
        return render_template('testcase_scene/testcase_scene_testcase_list.html', testcase_scenes=testcase_scenes,
                               model_testcases=model_testcases, pagination=pagination,
                               model_testcase_scenes=model_testcase_scenes, page=page, search=search)


class TestCaseSceneRun(MethodView):

    def get(self):
        sql_wait = Variables.query.filter(Variables.name == '_Sql_wait').first().value
        testcase_scene_id = request.args.get('testcase_scene_id')
        testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        testcases = testcase_scene.testcases
        if not testcases:
            return json.dumps({'testcase_results': "场景未存在用例"})
        testcase_results = []
        for testcase in testcases:
            if sql_wait != "0" :
                testcase_result, regist_variable_value = post_testcase(testcase=testcase)
            else:
                testcase_result, regist_variable_value = to_execute_testcase(testcase)
            testcase_results.extend(['【%s】' % testcase.name, testcase_result])
        testcase_results_html = '<br>'.join(testcase_results)
        print('TestCaseSceneRun: ', json.dumps({'testcase_results': testcase_results_html}))
        FrontLogs('执行测试场景 name： %s ' % testcase_scene.name).add_to_front_log()
        return json.dumps({'testcase_results': testcase_results_html})


class TestCaseSceneDelete(MethodView):

    def get(self):
        scene_page, testcase_scene_id = request_get_values('scene_page', 'testcase_scene_id')
        testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        testcases = TestCases.query.join(TestCaseScene, TestCases.testcase_scene_id == TestCaseScene.id).\
            filter(TestCases.testcase_scene_id == testcase_scene_id).all()

        if len(testcases) > 0:
            for testcase in testcases:
                if testcase.wait:
                    db.session.delete(testcase.wait[0])
                db.session.delete(testcase)
                FrontLogs('删除测试场景 id： %s  关联的测试用例名称 %s' % (testcase_scene_id, testcase.name)).add_to_front_log()
        db.session.delete(testcase_scene)
        db.session.commit()
        session['msg'] = '删除成功'
        FrontLogs('删除测试场景 id： %s' % testcase_scene_id).add_to_front_log()
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list', page=scene_page))


class TestCaseSceneTestCaseCopy(MethodView):

    def get(self):
        scene_page, testcase_scene_id, testcase_id = request_get_values('scene_page', 'testcase_scene_id', 'testcase_id')
        if not testcase_id or testcase_id == "null":
            print('TestCaseSceneTestCaseCopy:', testcase_id, type(testcase_id))
            flash('请先设置用例模板')
            return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list', page=scene_page))

        testcase = TestCases.query.get(testcase_id)
        copy_case(testcase, testcase_scene_id)
        session['msg'] = '复制用例成功'

        FrontLogs('复制场景测试用例 name： %s 成功' % testcase.name).add_to_front_log()
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list', page=scene_page))


def copy_case(testcase, testcase_scene_id=None):
    timestr = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    if len(testcase.name) > 30:
        name = testcase.name[:21] + timestr
    else:
        name = testcase.name + timestr
    testcase_new = TestCases(name, testcase.url, testcase.data, testcase.regist_variable,
                             testcase.regular, testcase.method, testcase.group_id, testcase.request_headers_id,
                             testcase_scene_id, testcase.hope_result, user_id=testcase.user_id,
                             old_sql=testcase.old_sql,
                             new_sql=testcase.old_sql, old_sql_regist_variable=testcase.old_sql_regist_variable,
                             new_sql_regist_variable=testcase.new_sql_regist_variable,
                             old_sql_hope_result=testcase.old_sql_hope_result,
                             new_sql_hope_result=testcase.new_sql_hope_result, old_sql_id=testcase.old_sql_id,
                             new_sql_id=testcase.new_sql_id)
    db.session.add(testcase_new)
    db.session.commit()
    if Wait.query.filter(Wait.testcase_id == testcase.id).count() > 0:
        old_wait = Wait.query.filter(Wait.testcase_id == testcase.id).first()
        wait = Wait(old_wait.old_wait_sql, old_wait.old_wait, old_wait.old_wait_time, old_wait.old_wait_mysql,
                    old_wait.new_wait_sql, old_wait.new_wait, old_wait.new_wait_time,
                    old_wait.new_wait_mysql, testcase_new.id)
        db.session.add(wait)
        db.session.commit()


class TestCaseSceneCopy(MethodView):

    def get(self):
        scene_page, testcase_scene_id = request_get_values('scene_page', 'testcase_scene_id')
        if not testcase_scene_id or testcase_scene_id == "null":
            flash('请先设置场景模板')
            return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list', page=scene_page))
        testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        timestr = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

        if len(testcase_scene.name) > 30:
            name = testcase_scene.name[:21] + timestr
        else:
            name = testcase_scene.name + timestr
        testcase_scene_copy = TestCaseScene(name, testcase_scene.group_id, description=testcase_scene.description, user_id=testcase_scene.user_id)
        db.session.add(testcase_scene_copy)
        db.session.commit()
        session['msg'] = '复制场景成功'
        if testcase_scene.testcases:
            for testcase in testcase_scene.testcases:
                copy_case(testcase, testcase_scene_copy.id)
        FrontLogs('复制测试场景 name： %s 成功' % testcase_scene.name).add_to_front_log()
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list', page=scene_page))


class TestCaseSceneModel(MethodView):

    def get(self, testcase_scene_id):
        testcase_scene = TestCaseScene.query.get(testcase_scene_id)
        page = request.args.get('page')
        if testcase_scene.is_model == 0 or testcase_scene.is_model is None:
            testcase_scene.is_model = 1
            flash('设置场景模板成功')
            FrontLogs('设置测试场景 name： %s 作为模板成功' % testcase_scene.name).add_to_front_log()
        else:
            testcase_scene.is_model = 0
            flash('取消场景模板成功')
            FrontLogs('取消设置测试场景 name： %s 作为模板成功' % testcase_scene.name).add_to_front_log()
        db.session.commit()
        return redirect(url_for('testcase_scene_blueprint.testcase_scene_testcase_list', page=page))


class SceneUp(MethodView):
    def get(self):
        _id = request_get_values('id')
        scene = TestCaseScene.query.get(_id)
        scene.updated_time = datetime.datetime.now()
        db.session.commit()
        return redirect(url_for('test_case_request_blueprint.test_case_request'))


class TestCaseSceneAddValidate(MethodView):

    def get(self):
        user_id = session.get('user_id')
        name = request.args.get('name')
        testcase = TestCaseScene.query.filter(TestCaseScene.name == name, TestCaseScene.user_id == user_id).count()
        if testcase != 0:
            return jsonify(False)
        else:
            return jsonify(True)


class TestCaseSceneUpdateValidate(MethodView):

    def get(self):
        user_id = session.get('user_id')
        name = request.args.get('name')
        testcase_scene_id = request.args.get('testcase_scene_id')
        if testcase_scene_id:
            print('TestCaseSceneUpdateValidate:', name, testcase_scene_id)
            testcase_scene = TestCaseScene.query.filter(
                TestCaseScene.id != testcase_scene_id, TestCaseScene.name == name, TestCaseScene.user_id == user_id).count()
            if testcase_scene != 0:
                return jsonify(False)
            else:
                return jsonify(True)
        testcase_scene = TestCaseScene.query.filter(TestCaseScene.name == name, TestCaseScene.user_id == user_id).count()
        if testcase_scene != 0:
            return jsonify(False)
        else:
            return jsonify(True)


testcase_scene_blueprint.add_url_rule('/testcase_scene_update/', view_func=TestCaseSceneUpdate.as_view('testcase_scene_update'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_copy_scene/', view_func=TestCaseSceneCopy.as_view('testcase_scene_copy_scene'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_model/<testcase_scene_id>/', view_func=TestCaseSceneModel.as_view('testcase_scene_model'))


testcase_scene_blueprint.add_url_rule('/testcase_scene_copy/', view_func=TestCaseSceneTestCaseCopy.as_view('testcase_scene_copy'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_testcase_list/', view_func=TestCaseSceneTestCaseList.as_view('testcase_scene_testcase_list'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_delete/', view_func=TestCaseSceneDelete.as_view('testcase_scene_delete'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_run/', view_func=TestCaseSceneRun.as_view('testcase_scene_run'))
testcase_scene_blueprint.add_url_rule('/scene_up/', view_func=SceneUp.as_view('scene_up'))


testcase_scene_blueprint.add_url_rule('/testcase_scene_add_validate/', view_func=TestCaseSceneAddValidate.as_view('testcase_scene_add_validate'))
testcase_scene_blueprint.add_url_rule('/testcase_scene_update_validate/', view_func=TestCaseSceneUpdateValidate.as_view('testcase_scene_update_validate'))

