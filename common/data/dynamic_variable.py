from modles import Variables


def get_page():
    while 1:
        FLASK_POST_PRE_ARGV = eval(Variables.query.filter(Variables.name == '_FLASK_POST_PRE_ARGV').limit(1).first().value)
        print('FLASK_POST_PRE_ARGV:', FLASK_POST_PRE_ARGV)
        yield FLASK_POST_PRE_ARGV


get_page = get_page()



