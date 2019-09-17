# import datetime
# timestr = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
#
# print(timestr)
#
# import os
# # path = (os.path.split(os.path.realpath(__file__))[0])
# _path = r'D:\PycharmProjects\new Project\MyFlask\data\download'
# dir_path, name = os.path.split(_path)
# path_list = os.listdir(_path)
# for path in path_list:
#     print(os.path.getctime(_path + '/' + path))
# print(path_list)
# import config

import os
path = os.path.join('path', 'data/')
print('path', path)