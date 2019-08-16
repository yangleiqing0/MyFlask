from modles.variables import Variables
from app import db
from pre_data import variable as var
from pre_data.variable import *


def add_pre_data(key, table="Variavles"):
    # 根据需要插入的表明  进行预配置参数插入
    var_name = "_%s" % key
    if table == "Variavles":
        instance = Variables(var_name, eval(key))
        if Variables.query.filter(Variables.name == "%s" % var_name).count() == 0:
            db.session.add(instance)
            db.session.commit()


def add_pre_data_go():

    pre_variable = dir(var)
    # 获取var模块的所有属性
    pre_variable = [add_pre_data(key) for key in pre_variable if "__" not in key and key[0].isupper()]
    # 通过列表生成式 过滤首字符非大写，没有__的变量




