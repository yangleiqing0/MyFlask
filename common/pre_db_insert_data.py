from modles.variables import Variables
from modles.user import User
from app import db
from common.connect_sqlite import cdb
from pre_data import variable as var
from pre_data import user
from pre_data.variable import *
from pre_data.user import *


def add_pre_data(key, user_id, table="Variavles"):
    # 根据需要插入的表明  进行预配置参数插入
    print('add_pre_data user_id:', user_id)
    print('key:', key, eval(key))
    var_name = "_%s" % key
    if table == "Variavles":
        if Variables.query.filter(Variables.name == "%s" % var_name, Variables.user_id == user_id).count() == 0:
            print('Variables.query.filter user_id:', user_id)
            instance = Variables(var_name, eval(key), user_id=user_id)
            db.session.add(instance)
            db.session.commit()

    elif table == 'User':
        username, password = eval(key)
        if Variables.query.filter(User.username == "%s" % username).count() == 0:
            _user = User(username, password)
            db.session.add(_user)
            db.session.commit()


def add_pre_data_go(user_id):
    print('add_pre_data_go user_id:', user_id)
    pre_variable = dir(var)
    # 获取var模块的所有属性
    pre_variable = [add_pre_data(key, user_id) for key in pre_variable if "__" not in key and key[0].isupper()]
    # 通过列表生成式 过滤首字符非大写，没有__的变量


def add_pre_user(user_id):
    pre_user = dir(user)
    [add_pre_data(key, table='User', user_id=user_id) for key in pre_user if "__" not in key and key[0].isupper()]


def to_insert_data(user_id):
    add_pre_data_go(user_id=user_id)
    add_pre_user(user_id=user_id)


if __name__ == '__main__':
    add_pre_user()
