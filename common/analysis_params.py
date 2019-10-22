import re
import json
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
            print('需要解析的变量：%s, 筛选出的变量: %s' % (params, words))
            if len(words) == 0:
                print('最后的解析结果:len(words)', params)
                return params
            in_variables_num = 0
            for word in words:
                if '随机' in word:
                    print('随机开始', word)
                    params = RangName(params).rand_str(testcase_name=testcase_name, analysis_word=word)
                else:
                    if (word,) in self.variables:
                        in_variables_num += 1
                        variable_value_query_sql = 'select value from variables where name=%s'
                        variable_value = cdb().query_db(variable_value_query_sql, (word,), True)[0]
                        print('variable_value: ${%s}' % word, variable_value)
                        if is_change == "headers":
                            params = params.replace('${%s}' % word, '"%s"' % variable_value)
                        if word == 'auto_vdb_parameter':
                            #  恢复VDB时代码处理VDB的参数
                            try:
                                target_env_tag = cdb().query_db(variable_value_query_sql,
                                                                ('target_env_tag',), True)[0]
                                # print('auto_vdb_parameter:', target_env_tag)
                                auto_vdb_cannot_parameter = cdb().query_db(variable_value_query_sql,
                                                                ('auto_vdb_cannot_parameter',), True)[0]
                                print('auto_vdb_parameter tag:', target_env_tag, params, auto_vdb_cannot_parameter, type(auto_vdb_cannot_parameter))
                                variable_value = json.loads(variable_value)
                                variable_value.extend(json.loads(auto_vdb_cannot_parameter))
                                variable_value = json.dumps(variable_value)
                                tag_name = cdb().query_db(variable_value_query_sql, 'tag_name', True)[0]
                                params = params.replace(
                                    '${%s}' % word, variable_value).replace(
                                    target_env_tag, tag_name)
                                print('auto_vdb_parameter:', tag_name, target_env_tag, params)
                            except TypeError as e:
                                print('auto_vdb_parameter error', e)
                            continue
                        elif word == 'auto_v2p_parameter':
                            try:

                                auto_v2p_cannot_parameter = cdb().query_db(variable_value_query_sql,
                                                                ('auto_v2p_cannot_parameter',), True)[0]
                                variable_value = json.loads(variable_value)
                                variable_value.extend(json.loads(auto_v2p_cannot_parameter))
                                variable_value = json.dumps(variable_value)
                                params = params.replace(
                                    '${%s}' % word, variable_value)
                                print('auto_v2p_parameter:', params)
                            except TypeError as e:
                                print('auto_v2p_parameter error', e)
                            continue
                        params = params.replace('${%s}' % word, variable_value)
            if in_variables_num == 0:
                print('最后的解析结果:', params)
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