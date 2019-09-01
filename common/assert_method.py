

class AssertMethod:

    def __init__(self, actual_result, hope_result):
        self.actual_result = actual_result
        self.result = None
        print('hope_result:', hope_result)
        self.assertmethod, self.hoperesult = hope_result.split(':', 1)
        print("self.assertmethod: %s, self.hoperesult: %s" % (self.assertmethod, self.hoperesult))
        self.actual_result = str(self.actual_result)
        print('self.actual_result: ', self.actual_result)

    def assert_method(self):
        if '包含' in self.assertmethod:
            result = self.assert_in()
        elif '等于' in self.assertmethod:
            result = self.assert_eq()
        return result

    def assert_eq(self):
        if self.actual_result == self.hoperesult:    # 返回结果与期望结果相等
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        return self.result

    def assert_in(self):
        if self.hoperesult in self.actual_result:   #期望结果在返回结果中
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        print('self.result: ', self.result)
        return self.result
