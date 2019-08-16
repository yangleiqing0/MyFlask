from flask import request


def request_get_values(*args, default=''):
    print('args:', args)
    arg_list = []
    for arg in args:
        arg_list.append(request.values.get(arg, default))
    return arg_list
