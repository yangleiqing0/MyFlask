from modles.variables import Variables
from modles.user import User
from app import db
from pre_data import variable as var
from pre_data import user
from pre_data.variable import *
from pre_data.user import *


def add_pre_data(key, table="Variavles"):
    # 根据需要插入的表明  进行预配置参数插入
    print('key:', key, eval(key))
    var_name = "_%s" % key
    if table == "Variavles":

        instance = Variables(var_name, eval(key))
        if Variables.query.filter(Variables.name == "%s" % var_name).count() == 0:
            db.session.add(instance)
            db.session.commit()

    elif table == 'User':
        username, password = eval(key)
        _user = User(username, password)
        if Variables.query.filter(User.username == "%s" % username).count() == 0:
            db.session.add(_user)
            db.session.commit()


def add_pre_data_go():

    pre_variable = dir(var)
    # 获取var模块的所有属性
    pre_variable = [add_pre_data(key) for key in pre_variable if "__" not in key and key[0].isupper()]
    # 通过列表生成式 过滤首字符非大写，没有__的变量


def add_pre_user():
    pre_user = dir(user)
    [add_pre_data(key, table='User') for key in pre_user if "__" not in key and key[0].isupper()]


def to_insert_data():
    add_pre_data_go()
    add_pre_user()


if __name__ == '__main__':
    add_pre_user()
