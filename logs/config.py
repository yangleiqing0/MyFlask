# 日志等级   ：
# FATAL/CRITICAL = 重大的，危险的
# ERROR = 错误
# WARNING = 警告
# INFO = 信息
# DEBUG = 调试
# NOTSET = 没有设置

import logging

FLASK_LOGS_FILE = 'logs/flask.log'
FRONT_LOGS_FILE = 'logs/frontlogs.log'   # 输入到前端的日志路径
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = logging.FileHandler(FLASK_LOGS_FILE)
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器

