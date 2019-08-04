import inspect, re

class Dict(dict):
    __setattr__ = dict.__setitem__


def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for key, value in dictObj.items():
        inst[key] = dict_to_object(value)
    return inst




if __name__ == '__main__':
    a = 4

