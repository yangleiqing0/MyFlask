import os


basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'db\\test.sqlite')

SQLALCHEMY_ECHO = True
base_dir = os.path.join(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db\\test.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_TEARDOWN = False


FLASK_POST_PRE_ARGV = 6

# 这个配置将来会被禁用,设置为True或者False可以解除警告信息,建议设置False

EXCEL_TO_HTML_PATH = 'templates/reports/'
