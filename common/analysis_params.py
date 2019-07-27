import re
from app import cdb

class AnalysisParams:

    def __init__(self, params=None):
        variables_query_sql = 'select name from variables'
        self.variables = cdb().query_db(variables_query_sql)
        print('init:self.variables:',self.variables)


    def analysis_describe(self, params):
        print('analysis_before:', params)
        res = r'\${([^\${}]+)}'
        words = re.findall(re.compile(res), params)
        for word in words:
            if (word,) in self.variables:
                variable_value_query_sql = 'select value from variables where name=?'
                variable_value = cdb().query_db(variable_value_query_sql, (word,), True)[0]
                print('${%s}' % word, variable_value)
                params = params.replace('${%s}' % word, variable_value)
            else:
                continue
        print('解析后的参数为:', params)
        # return params
        # res = r'\${|}'

        #     match_indexs = re.sub
        #
        #     print('匹配的下标:', match_indexs, type(match_indexs))
        # except AttributeError:
        #     lists = re.split(re.compile(res), params)
        #     print('切割后的列表:', lists)
        #     print('无匹配解析后的参数为:', params)
        #     return params
        # lists = re.split(re.compile(res), params)
        # print('切割后的列表:', lists)
        # for num in range(len(lists)):
        #     if (lists[num],) in self.variables and num in match_indexs:
        #         variable_value_query_sql = 'select value from variables where name=?'
        #         variable_value = cdb().query_db(variable_value_query_sql, (lists[num],), True)[0]
        #         lists[num] = variable_value
        #     elif (lists[num],) not in self.variables and num in match_indexs:
        #         lists[num] = '${%s}' % lists[num]
        # params = ''.join(lists)
        # print('解析后的参数为:', params)
        # return params


if __name__ == '__main__':
    AnalysisParams().analysis_describe('${btest${A}${B}${C}hhh')