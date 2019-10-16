# encoding=utf-8
import json
from common.analysis_params import AnalysisParams
from common.regist_variables import to_regist_variables
from flask import session


def to_execute_testcase(testcase, url, data, is_commit=True):
    # session[testcase.name] = []
    testcase_request_header = testcase.testcase_request_header  # 通过反向引用获得case对应的请求头对象
    print('testcase:', testcase, testcase_request_header)

    testcase_name = AnalysisParams().analysis_more_params(testcase.name)

    testcase_request_header_value = AnalysisParams().analysis_params(
        testcase_request_header.value, is_change='headers')
    print('请求的url:%s 请求的headers:%s' % (url, testcase_request_header_value))
    testcase_result, regist_variable_value = to_regist_variables(testcase_name, testcase.method, url, data,
                                          json.loads(testcase_request_header_value),
                                          testcase.regist_variable, testcase.regular, is_commit=is_commit,
                                                                 testcase_name=testcase.name)

    return testcase_result, regist_variable_value
