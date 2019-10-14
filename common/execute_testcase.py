# encoding=utf-8
import json
from common.analysis_params import AnalysisParams
from common.regist_variables import to_regist_variables


def to_execute_testcase(testcase, is_commit=True):

    testcase_request_header = testcase.testcase_request_header  # 通过反向引用获得case对应的请求头对象
    print('testcase:', testcase, testcase_request_header)

    testcase_name, testcase_url, testcase_data = AnalysisParams().analysis_more_params(testcase.name, testcase.url, testcase.data)

    testcase_request_header_value = AnalysisParams().analysis_params(
        testcase_request_header.value, is_change='headers')
    print('请求的url:%s 请求的headers:%s' % (testcase_url, testcase_request_header_value))
    testcase_result, regist_variable_value = to_regist_variables(testcase_name, testcase.method, testcase_url, testcase_data,
                                          json.loads(testcase_request_header_value),
                                          testcase.regist_variable, testcase.regular, is_commit=is_commit)

    return testcase_result, regist_variable_value
