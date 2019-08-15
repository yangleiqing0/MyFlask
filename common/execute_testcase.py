import json
from common.analysis_params import AnalysisParams
from common.regist_variables import to_regist_variables


def to_execute_testcase(testcase):

    testcase_request_header = testcase.testcase_request_header
    testcase.name, testcase.url, testcase.data, testcase.regist_variable, testcase.regular = AnalysisParams(). \
        analysis_more_params(testcase.name, testcase.url, testcase.data, testcase.regist_variable, testcase.regular)
    testcase_request_header.value = AnalysisParams().analysis_params(
        testcase_request_header.value, is_change='headers')
    testcase_result = to_regist_variables(testcase.method, testcase.url, testcase.data,
                                          json.loads(testcase_request_header.value),
                                          testcase.regist_variable, testcase.regular)
    return testcase_result
