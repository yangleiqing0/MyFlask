from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,RadioField,DateField,DecimalField,SelectField
from wtforms import validators


class RequestHeadersForm(FlaskForm):

    name = StringField('请求头部名称', [validators.DataRequired('必填'), validators.Length(min=2, max=20, message='请输入名称长度2-20字符')])
    value = StringField('请求头部的值', [validators.DataRequired('必填')])
    description = StringField('请求头部备注', [validators.Length(max=50, message='请输入备注长度50字符以内')])