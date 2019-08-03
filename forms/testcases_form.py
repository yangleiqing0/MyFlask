from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,RadioField,DateField,DecimalField,SelectField
from wtforms import validators


class TestCasesForm(FlaskForm):

    name = StringField('测试用例名称', [validators.DataRequired('必填'), validators.Length(min=2, max=20, message='请输入名称长度2-20字符')])
    url = StringField('请求接口', [validators.DataRequired('必填'), validators.Length(max=500, message='请输入长度500以内字符')])
    data = StringField('请求报文', [validators.DataRequired('必填')])
    regist_variable = StringField('注册变量', [validators.Length(max=30, message='请输入长度30以内字符')])
    regular = StringField('正则匹配')
    method = StringField('请求方式', [validators.DataRequired('必填'),validators.Length(max=10, message='请输入长度10以内字符')])
