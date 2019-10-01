import os

host = '192.168.1.11'
port = 3333
db = 'flasktest'
root = 'root'
pwd = 'zdbm123'

project_path = 'D:/PythonProject/MytestFlask'   # 工作目录，考虑到其他方式启动flask 需要先把flask目录提供
basedir = os.path.abspath(os.path.dirname(__file__))
# DATABASE_URL = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'db\\test.sqlite')

SQLALCHEMY_ECHO = False
base_dir = os.path.join(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(root, pwd, host, port, db)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_TEARDOWN = False

# processes = 5
threaded = True

# 这个配置将来会被禁用,设置为True或者False可以解除警告信息,建议设置False


TESTCASE_XLSX_PATH = 'data/'

ALLOWED_EXTENSIONS=['.xlsx', '.xls', '.xlsm']   # 允许上传的文件类型