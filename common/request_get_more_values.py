from flask import request


def request_get_values(*args, default=''):
    print('args:', args)
    arg_list = []
    for arg in args:
        if 'id' in arg:
            default = None
        else:
            default = ''
        arg_list.append(request.values.get(arg, default))
    if len(arg_list) == 1:
        arg_list = arg_list[0]
    return arg_list
