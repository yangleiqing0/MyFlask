from modles import Variables
from flask import session

# class PageConfig:
#
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def get_page(user_id):
#         while 1:
#             FLASK_POST_PRE_ARGV = eval(Variables.query.filter(Variables.name == '_FLASK_POST_PRE_ARGV', Variables.user_id == user_id).limit(1).first().value)
#             print('FLASK_POST_PRE_ARGV:', FLASK_POST_PRE_ARGV)
#             yield FLASK_POST_PRE_ARGV


def _get_page():
    while 1:
        user_id = session.get('user_id')
        FLASK_POST_PRE_ARGV = eval(
            Variables.query.filter(Variables.name == '_FLASK_POST_PRE_ARGV', Variables.user_id == user_id).limit(
                1).first().value)
        print('FLASK_POST_PRE_ARGV:', FLASK_POST_PRE_ARGV)
        yield FLASK_POST_PRE_ARGV


get_page = _get_page()



