from config import TESTCASE_XLSX_PATH
from . import datetime, xlrd, time, os, json


class NullObject:

    pass


def get_now_time():
    timestr = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    return timestr


def clear_download_xlsx(method='download'):
    from logs.config import path as root_path
    dir_path = os.path.join(root_path, TESTCASE_XLSX_PATH + method)
    path_list = os.listdir(dir_path)
    target_time = int(time.time())-300
    for _path in path_list:
        if '.py' not in _path:
            __path = dir_path + '/' + _path
            path_time = int(os.path.getctime(__path))
            print('path_time:', path_time, target_time, __path)
            if path_time <= target_time:
                os.remove(__path)
        else:
            continue


def read_xlsx(table):
    book = xlrd.open_workbook(table)
    row_list = []
    for s in range((len(book.sheets()))):
        sheet = book.sheets()[s]
        for row in range(sheet.nrows):
            row_list.append(sheet.row_values(row))
    return row_list


def is_json(_str):
    try:
        json.loads(_str)
    except ValueError:
        return False
    return True
