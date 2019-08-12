

class AssertMethod:

    def __init__(self, actual_result, hope_result, assertmethod, old_database_value=1,
                 new_database_value=1, database_assert_method=True):
        print('here', type(database_assert_method),database_assert_method,old_database_value,new_database_value,
              old_database_value==new_database_value
              )
        self.old_database_value = old_database_value
        self.new_database_value = new_database_value
        self.database_assert_method = database_assert_method
        self.actual_result = actual_result
        self.hope_result = hope_result
        self.result = None
        self.assertmethod = assertmethod
        self.actual_result = str(self.actual_result)
        # self.assert_database_result()

    def assert_database_result(self):
        if self.database_assert_method:
            if self.old_database_value == self.new_database_value:
                self.assert_method()
            else:
                self.result = '数据库验证失败'
        else:
            print('到了数据库验证')
            if self.old_database_value != self.new_database_value:
                print('到了这儿')
                self.assert_method()
            else:
                self.result = '数据库验证失败'
        return self.result

    def assert_method(self):
        if '包含' in self.assertmethod:
            self.assert_in()
        elif '等于' in self.assertmethod:
            self.assert_eq()

    def assert_eq(self):
        if self.actual_result == self.hope_result:    #返回结果与期望结果相等
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        return self.result

    def assert_in(self):
        if self.hope_result in self.actual_result:   #期望结果在返回结果中
            self.result = '测试成功'
        else:
            self.result = '测试失败'
        return self.result
