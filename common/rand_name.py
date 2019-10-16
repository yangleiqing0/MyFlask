from . import random, string, re
from flask import session


class RangName:

    def __init__(self, name):
        self.name = name

    def rand_str(self, testcase_name = '__testcase_name'):
        res = r'\${([^\${}]+)}'
        com_word = re.findall(re.compile(res), self.name)
        if len(com_word) > 0:
            word = re.findall(re.compile(res), self.name)[0]  # 限定最多一次随机
            ran_str = self.rand_name(word[2:])
            if isinstance(session.get(testcase_name), list):
                session[testcase_name].append(ran_str)
            self.name = self.name.replace('${%s}' % word, '%s' % ran_str, 1)
            print('随机名称self.name: ', self.name)
            return self.name
        return self.name

    @staticmethod
    def rand_name(word):
        ran_str = ''.join(random.sample(string.ascii_letters, 1)) + \
                  ''.join(random.sample(string.ascii_letters +
                                        string.digits, eval(word) - 1))
        return ran_str


if __name__ == '__main__':
    RangName("${随机4}哈哈").rand_str()
