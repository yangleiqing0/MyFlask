# encoding=utf-8
import re
from common.method_request import MethodRequest
from flask import session
from modles import Variables, db


def to_regist_variables(name, method, url, data, headers, regist_variable='', regular=''):
    response_body = MethodRequest().request_value(method, url, data, headers)
    user_id = session.get('user_id')
    if 'html' in response_body:
        response_body = '<xmp> %s </xmp>' % response_body
    # print('response_body:', response_body.encode('utf-8').decode('gbk'))
    if regist_variable:
        # 判断是否有注册变量和正则方法，有的话进行获取
        if regular:
            if ',' in regular:
                regular_list = regular.split(',')
                regist_variable_list = regist_variable.split(',')
                if len(regular_list) <= len(regist_variable_list):
                    regist_variable_value_list = []
                    for index in range(len(regular_list)):
                        regist_variable_value = re.compile(regular_list[index]).findall(response_body)
                        if len(regist_variable_value) > 0:
                            regist_variable_value_list.append(regist_variable_value[0])
                            if Variables.query.filter(Variables.name == regist_variable_list[index]).count() > 0:
                                print('%s 请求结束,存在此变量时：' % url,
                                      Variables.query.filter(Variables.name == regist_variable_list[index]).first())
                                Variables.query.filter(Variables.name == regist_variable_list[index]).first().value = \
                                regist_variable_value[0]
                                db.session.commit()
                            private_variable_value = regist_variable_value[0]
                            private_variable = Variables(regist_variable_list[index], private_variable_value, is_private=1,
                                                         user_id=user_id)
                            db.session.add(private_variable)
                            db.session.commit()
                        else:
                            regist_variable_value_list.append(regist_variable_value)
                    return response_body, str(regist_variable_value_list)
                return response_body, '正则匹配规则数量过多'
            regist_variable_value = re.compile(regular).findall(response_body)
            if len(regist_variable_value) > 0:
                if Variables.query.filter(Variables.name == regist_variable).count() > 0:
                    print('%s 请求结束,存在此变量时：' % url,  Variables.query.filter(Variables.name == regist_variable).first())
                    Variables.query.filter(Variables.name == regist_variable).first().value = regist_variable_value[0]
                    db.session.commit()
                    return response_body, regist_variable_value[0]
                private_variable_value = regist_variable_value[0]
                private_variable = Variables(regist_variable, private_variable_value, is_private=1, user_id=user_id)
                db.session.add(private_variable)
                db.session.commit()
                return response_body, regist_variable_value[0]
            return response_body, '未成功解析报文 %s ' % response_body
        if Variables.query.filter(Variables.name == regist_variable).count() > 0:
            Variables.query.filter(Variables.name == regist_variable).first().value = response_body
            db.session.commit()
            return response_body, response_body
        private_variable_value = response_body
        # print('no regular：', regist_variable, private_variable_value)
        private_variable = Variables(regist_variable, private_variable_value, is_private=1, user_id=user_id)
        db.session.add(private_variable)
        db.session.commit()
        return response_body, response_body
    return response_body, '未注册变量'
