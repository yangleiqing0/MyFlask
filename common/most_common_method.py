import datetime


class NullObject:

    pass


def get_now_time():
    timestr = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    return timestr
