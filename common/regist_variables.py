import re
from modles.variables import Variables
from common.method_request import MethodRequest
from app import db


def to_regist_variables(name, method, url, data, headers, regist_variable='', regular=''):
    name = name
    response_body = MethodRequest().request_value(method, url, data, headers)
    if 'html' in response_body:
        response_body = '<xmp> %s </xmp>' % response_body
    print('response_body:', response_body)
    if regist_variable and regular:
        # 判断是否有注册变量和正则方法，有的话进行获取
        regist_variable_value = re.compile(regular).findall(response_body)
        if len(regist_variable_value) > 0:
            if Variables.query.filter(Variables.name == regist_variable).count() > 0:
                print('%s 请求结束,存在此变量时：' % url,  Variables.query.filter(Variables.name == regist_variable).first())
                Variables.query.filter(Variables.name == regist_variable).first().value = regist_variable_value[0]
                db.session.commit()
                return response_body
            private_variable_value = regist_variable_value[0]
            private_variable = Variables(regist_variable, private_variable_value, is_private=1)
            db.session.add(private_variable)
            db.session.commit()
            return response_body
        return '未成功解析报文 %s ' % response_body
    return response_body
