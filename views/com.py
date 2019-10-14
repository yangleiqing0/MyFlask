from flask import request, session, redirect, url_for

from common.request_get_more_values import request_get_values
from modles import db
from common.tail_font_log import FrontLogs


def update(_object, **kwargs):
    for key, value in dict(kwargs).items():
        setattr(_object, key, value)
    db.session.commit()


def add(_object, **kwargs):
    __object = _object(**kwargs)
    db.session.add(__object)
    db.session.commit()


def resolve():
    result = request.values.to_dict()
    print('resolve', result)
    keys = result.keys()
    values = {}
    ids = {}
    for key in ['page', 'scene']:
        if key in keys:
            values.update({key: result.pop(key)})
    for key in ['id', ]:
        if key in keys:
            ids.update({key: result.pop(key)})
    print('ids', ids)
    return result, values, ids


def add_operate(sqlalchemy_object, name, blueprint, endpoint):
    result, values, _ = resolve()
    user_id = session.get('user_id')
    add(sqlalchemy_object, **result, user_id=user_id)
    session['msg'] = '添加成功'
    FrontLogs('添加%s name： %s 成功' % (name, result.get('name'))).add_to_front_log()
    return redirect(url_for('{}.{}'.format(blueprint, endpoint), **values))


def update_operate(sqlalchemy_object, name, blueprint, endpoint):
    result, values, ids = resolve()
    _object = sqlalchemy_object.query.get(ids.get('id'))
    user_id = session.get('user_id')
    update(_object, **result, user_id=user_id)
    session['msg'] = '编辑成功'
    FrontLogs('编辑%s name： %s 成功' % (name, result.get('name'))).add_to_front_log()
    return redirect(url_for('{}.{}'.format(blueprint, endpoint), **values))


def edit(sqlalchemy_object, name, blueprint, endpoint):
    if request.values.get('id'):
        return update_operate(sqlalchemy_object, name, blueprint, endpoint)
    return add_operate(sqlalchemy_object, name, blueprint, endpoint)
