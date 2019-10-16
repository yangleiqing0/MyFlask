import re
from common.rand_name import RangName
from common.connect_sqlite import cdb
from flask import session


class AnalysisParams:

    def __init__(self):
        user_id = session.get('user_id')
        variables_query_sql = 'select name from variables where user_id=%s'
        self.variables = cdb().query_db(variables_query_sql, (user_id,))
        print('init:self.variables:', self.variables)

    def analysis_params(self,  params, is_change=None, testcase_name='__testcase_name'):
        if params in ("", None):
            params = ""
            return params
        while 1:
            print('analysis_before:', type(params), params)
            res = r'\${([^\${}]+)}'
            words = re.findall(re.compile(res), params)
            # print('需要解析的变量：%s, 筛选出的变量: %s' % (params, words))
            if len(words) == 0:
                return params
            in_variables_num = 0
            for word in words:
                if '随机' in word:
                    params = RangName(params).rand_str(testcase_name=testcase_name)
                if (word,) in self.variables:
                    in_variables_num += 1
                    variable_value_query_sql = 'select value from variables where name=%s'
                    variable_value = cdb().query_db(variable_value_query_sql, (word,), True)[0]
                    print('variable_value: ${%s}' % word, variable_value)
                    if is_change == "headers":
                        params = params.replace('${%s}' % word, '"%s"' % variable_value)
                    params = params.replace('${%s}' % word, variable_value)
                    # print('解析后的参数为:', params, type(params))
            if in_variables_num == 0:
                return params

    def analysis_more_params(self, *args, testcase_name='__testcase_name', not_repeat=False):
        if len(args) == 1:
            arg = AnalysisParams().analysis_params(*args, testcase_name=testcase_name)
            return arg

        new_args = []
        for arg in args:
            if not_repeat:
                arg = self.analysis_params(arg, testcase_name=testcase_name)
            else:
                arg = AnalysisParams().analysis_params(arg, testcase_name=testcase_name)
            new_args.append(arg)

        return new_args

    def analysis_headers(self, headers):
        print('header_before:', headers)
        header = headers.replace(' ', '').replace('\n', '').replace('\r', '')
        return header


if __name__ == '__main__':
    AnalysisParams().analysis_params('{btest{A}{B}{C}hhh')