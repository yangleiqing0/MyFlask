import datetime
import os
import time
from config import TESTCASE_XLSX_PATH


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
        __path = dir_path + '/' + path
        path_time = int(os.path.getctime(__path))
        print('path_time:', path_time, target_time, __path)
        if path_time <= target_time:
            os.remove(__path)
