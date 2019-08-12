import random
import string
import re


class RangName:

    def __init__(self, name):
        self.name = name

    def rand_str(self):
        res = r'\${([^\${}]+)}'
        word = re.findall(re.compile(res), self.name)[0]  #限定最多一次随机
        ran_str = ''.join(random.sample(string.ascii_letters, 1)) + \
                  ''.join(random.sample(string.ascii_letters +
                                        string.digits, eval(word[2:]) - 1))
        self.name = self.name.replace('${%s}' % word, '%s' % ran_str)
        print('随机名称self.name: ', self.name)
        return self.name


if __name__ == '__main__':
    RangName("${随机4}哈哈").rand_str()
