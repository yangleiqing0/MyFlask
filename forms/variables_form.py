from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,RadioField,DateField,DecimalField,SelectField
from wtforms import validators


class VariablesForm(FlaskForm):

    name = StringField('全局变量名称', [validators.DataRequired('必填'), validators.Length(min=2, max=20, message='请输入名称长度2-20字符')])
    value = StringField('全局变量的值', [validators.DataRequired('必填')])
    description = StringField('全局变量备注', [validators.Length(max=50, message='请输入备注长度50字符以内')])