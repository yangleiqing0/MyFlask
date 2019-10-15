# encoding=utf-8
import re
from common.method_request import MethodRequest
from common import is_json, json
from flask import session
from modles import Variables, db


def to_regist_variables(name, method, url, data, headers, regist_variable='', regular='', is_commit=True):
    response_body = MethodRequest().request_value(method, url, data, headers)
    user_id = session.get('user_id')
    if 'html' in response_body:
        response_body = '<xmp> %s </xmp>' % response_body
    # print('response_body:', response_body.encode('utf-8').decode('gbk'))
    if regist_variable:
        # 判断是否有注册变量和正则方法，有的话进行获取
        if regular:
            #  判断是否有正则匹配规则
            regular_list = regular.split(',')
            regist_variable_list = regist_variable.split(',')
            print('regular_list:', regular_list, len(regular_list), len(regist_variable_list))
            if len(regular_list) <= len(regist_variable_list):
                # 判断正则和注册变量数目是否相符 小于或等于
                regist_variable_value_list = []
                for index in range(len(regular_list)):
                    # 循环取正则的规则
                    if '$.' in regular_list[index]:
                        if not is_json(response_body):
                            regist_variable_value = "不是合法的字典响应信息"
                        else:
                            keys = regular_list[index][2:].split('.')
                            if '' in keys:
                                keys.remove('')
                            print('keys:', keys)
                            regist_variable_value = json.loads(response_body)
                            for key in keys:
                                if key:
                                    try:
                                        if ']' in key and '[' in key:
                                            key, _index = key.split('[')
                                            regist_variable_value = regist_variable_value.get(key)[int(_index[:-1])]
                                        else:
                                            regist_variable_value = regist_variable_value.get(key)
                                    except AttributeError as e:
                                        print(e)
                                        regist_variable_value = ''
                                    print('regist_variable_value:', regist_variable_value)
                    elif '$[' in regular_list[index]:
                        # try:
                            print('session params', session['params'])
                            p_index = int(regular_list[index][2:-1])
                            regist_variable_value = session['params'][p_index]
                        # except Exception as e:
                        #     regist_variable_value = str(e)
                    else:
                        try:
                            regist_variable_value = re.compile(regular_list[index]).findall(response_body)
                        except Exception as e:
                            regist_variable_value = str(e)

                    if not regist_variable_value:
                        regist_variable_value = ''
                    elif isinstance(regist_variable_value, (int, str, dict)):
                        regist_variable_value = regist_variable_value
                    elif len(regist_variable_value) > 0:
                        regist_variable_value = regist_variable_value[0]
                    else:
                        regist_variable_value = '未知的值'
                    regist_variable_value_list.append(regist_variable_value)
                    if Variables.query.filter(Variables.name == regist_variable_list[index], Variables.user_id == user_id).count() > 0:
                        print('%s 请求结束,存在此变量时：' % url,
                              Variables.query.filter(Variables.name == regist_variable_list[index], Variables.user_id == user_id).first())
                        Variables.query.filter(Variables.name == regist_variable_list[index], Variables.user_id == user_id).first().value = \
                          regist_variable_value
                        if is_commit:
                            db.session.commit()
                    else:
                        private_variable_value = regist_variable_value
                        private_variable = Variables(regist_variable_list[index], private_variable_value, is_private=1,
                                                     user_id=user_id)
                        db.session.add(private_variable)
                        if is_commit:
                            db.session.commit()
                return response_body, str(regist_variable_value_list)
            return response_body, '正则匹配规则数量过多'
        return response_body, '未存在正则匹配'
    return response_body, '存在未注册变量'
