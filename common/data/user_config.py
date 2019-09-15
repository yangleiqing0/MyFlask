from common.data.dynamic_variable import PageConfig


def user_config(user_id):
    get_page = PageConfig().get_page(user_id)
    return get_page
