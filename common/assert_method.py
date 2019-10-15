

class AssertMethod:

    def __init__(self, actual_result, hope_result):
        self.actual_result = str(actual_result)
        self.result = self.asserts = None
        print('hope_result:', hope_result)
        if ',' in hope_result:
            self.asserts = hope_result.split(',')
        else:
            self.assertmethod, self.hoperesult = hope_result.split(':', 1)
        # print("self.assertmethod: %s, self.hoperesult: %s" % (self.assertmethod, self.hoperesult))
        # self.actual_result = str(self.actual_result)
        # print('self.actual_result: ', self.actual_result)

    def assert_method(self):
        if self.asserts:
            for _assert in self.asserts:
                assertmethod, hoperesult = _assert.split(':', 1)
                if '包含' in assertmethod:
                    result = self.assert_in(hoperesult)
                elif '等于' in assertmethod:
                    result = self.assert_eq(hoperesult)
                else:
                    result = ''
                if result == '测试失败':
                    return '测试失败'
            return '测试成功'
        else:

            if '不包含' in self.assertmethod:
                result = self.not_assert_in(self.hoperesult)
            elif '不等于' in self.assertmethod:
                result = self.not_assert_eq(self.hoperesult)
            elif '等于' in self.assertmethod:
                result = self.assert_eq(self.hoperesult)
            elif '包含' in self.assertmethod:
                result = self.assert_in(self.hoperesult)
            elif '大于' in self.assertmethod:
                result = self.assert_gt(self.hoperesult)
            else:
                result = ''
            return result

    def assert_eq(self, hoperesult):
        if self.actual_result == hoperesult:    # 返回结果与期望结果相等
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        return self.result

    def assert_in(self, hoperesult):
        if hoperesult in self.actual_result:   # 期望结果在返回结果中
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        print('self.result: ', self.result)
        return self.result

    def not_assert_in(self, hoperesult):
        if hoperesult not in self.actual_result:  # 期望结果不在返回结果中
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        print('self.result: ', self.result)
        return self.result

    def not_assert_eq(self, hoperesult):
        if self.actual_result != hoperesult:    # 返回结果与期望结果相等
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        return self.result

    def assert_gt(self, hoperesult):
        if self.actual_result > hoperesult:    # 返回结果与期望结果相等
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        return self.result
