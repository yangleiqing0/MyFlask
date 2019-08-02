class Dict(dict):
    __setattr__ = dict.__setitem__

def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for key, value in dictObj.items():
        inst[key] = dict_to_object(value)
    return inst


# def object_to_dict(object):
#     dic = {}
#     for column in object.__table__.columns:
#         dic[column.name] = str(getattr(object, column.name))
#
#     return dic
