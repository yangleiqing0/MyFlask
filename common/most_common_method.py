from config import TESTCASE_XLSX_PATH
from . import datetime, xlrd, time, os


class NullObject:

    pass


def get_now_time():
    timestr = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    return timestr


def clear_download_xlsx(method='download'):
    dir_path = TESTCASE_XLSX_PATH + method
    path_list = os.listdir(dir_path)
    target_time = int(time.time())-300
    for path in path_list:
        if '.py' not in path:
            __path = dir_path + '/' + path
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
