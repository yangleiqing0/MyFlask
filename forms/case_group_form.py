from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import validators


class CaseGroupForm(FlaskForm):

    name = StringField('测试用例分组名称', [validators.DataRequired('必填'), validators.Length(min=2,max=20,message='请输入名称长度2-20字符')])
    description = StringField('测试用例分组备注', [validators.Length(max=50, message='请输入备注长度50字符以内')])