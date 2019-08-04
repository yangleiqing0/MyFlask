import xlsxwriter
from modles.testcase import TestCases
from modles.testcase_result import TestCaseResult
from modles.testcase_start_times import TestCaseStartTimes
from modles.variables import Variables
from app import cdb
from common.analysis_params import AnalysisParams


def test_report(testcase_time_id):
    data = []
    testcase_time = TestCaseStartTimes.query.get(testcase_time_id)
    print('testcase_time_id: ', testcase_time_id, testcase_time)
    testcase_results_query_sql = 'select testcases.name,testcases.url,testcases.method,testcases.data,test_case_result.response_body,' \
                                 ' testcases.hope_result,test_case_result.old_sql_value,test_case_result.new_sql_value,' \
                                 'test_case_result.testcase_test_result' \
                                 ' from testcases,test_case_result where testcases.id=test_case_result.testcase_id ' \
                                 'and test_case_result.testcase_start_time_id=%s' % testcase_time_id
    testcase_results = cdb().query_db(testcase_results_query_sql)
    print('testcase_results: ', testcase_results, len(testcase_results))
    for testcase_result in testcase_results:
        t_name = AnalysisParams().analysis_params(testcase_result[0])
        t_url = AnalysisParams().analysis_params(testcase_result[1])
        t_method = testcase_result[2]
        t_request_body = AnalysisParams().analysis_params(testcase_result[3])
        t_response_body = testcase_result[4]
        t_hope = AnalysisParams().analysis_params(testcase_result[5])
        old_database_value = testcase_result[6]
        new_database_value = testcase_result[7]
        t_result = testcase_result[8]
        print('testcase_result: ', testcase_result)
        content = {"t_name": t_name,
                   "t_url": t_url,
                   "t_method": t_method,
                   "t_request_body": t_request_body,
                   "t_hope": t_hope,
                   "t_response_body": t_response_body,
                   "old_database_value": old_database_value,
                   "new_database_value": new_database_value,
                   "t_result": t_result,
                   }
        data.append(content)
    print(data)
    test_name = Variables.query.filter(Variables.name == '_TEST_NAME').first().value
    zdbm_version = Variables.query.filter(Variables.name == '_TEST_VERSION').first().value
    test_pl = Variables.query.filter(Variables.name == '_TEST_PL').first().value
    test_net = Variables.query.filter(Variables.name == '_TEST_NET').first().value
    title_name = Variables.query.filter(Variables.name == '_TITLE_NAME').first().value
    test_sum = len(testcase_results)
    test_success = TestCaseResult.query.filter(TestCaseResult.testcase_test_result == "测试成功",
                                                   TestCaseResult.testcase_start_time_id == testcase_time_id).count()
    time_strftime = testcase_time.time_strftime
    filename = testcase_time.filename
    data_title = {"test_name": test_name, "test_version": zdbm_version, "test_pl": test_pl, "test_net": test_net}
    data_re = {"test_sum": test_sum, "test_success": test_success, "test_failed": test_sum-test_success,
               "test_date": time_strftime}
    r = Report()
    print("data_re", data_title, data_re, time_strftime, filename)
    r.init(data_title, data_re, int(test_success * 100 / test_sum), title_name=title_name, filename=filename)
    r.test_detail(data, test_sum, len(data))



class Report:

    def get_format(self,wd, option):
        return wd.add_format(option)
    # 设置居中

    def get_format_center(self,wb,num=1):
        return wb.add_format({'align': 'center','valign': 'vcenter','border':num,'text_wrap':1})

    def set_border_(self,wb, num=1):
        return wb.add_format({}).set_border(num)
    # 写数据

    def write_center(self,worksheet, cl, data, wb):
        return worksheet.write(cl, data, self.get_format_center(wb))

    def init(self, data, data1, score, filename, title_name):
        print(filename)
        self.workbook = xlsxwriter.Workbook(filename)

        # print(self.workbook)
        self.worksheet = self.workbook.add_worksheet("%s总况" % title_name)
        self.worksheet2 = self.workbook.add_worksheet("%s详情" % title_name)
        # 设置列行的宽高
        self.worksheet.set_column("A:A", 15)
        self.worksheet.set_column("B:B", 20)
        self.worksheet.set_column("C:C", 20)
        self.worksheet.set_column("D:D", 20)
        self.worksheet.set_column("E:E", 20)
        self.worksheet.set_column("F:F", 20)
        self.worksheet.set_column("F:F", 20)
        self.worksheet.set_row(1, 30)
        self.worksheet.set_row(2, 30)
        self.worksheet.set_row(3, 30)
        self.worksheet.set_row(4, 30)
        self.worksheet.set_row(5, 30)
        self.worksheet.set_row(6, 30)

        define_format_H1 = self.get_format(self.workbook, {'bold': True, 'font_size': 18})
        define_format_H2 = self.get_format(self.workbook, {'bold': True, 'font_size': 14})
        define_format_H1.set_border(1)

        define_format_H2.set_border(1)
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H2.set_bg_color("#70DB93")
        define_format_H2.set_color("#ffffff")
        # Create a new Chart object.

        self.worksheet.merge_range('A1:F1', '%s总概况' % title_name, define_format_H1)
        self.worksheet.merge_range('A2:F2', '%s概括' % title_name, define_format_H2)
        self.worksheet.merge_range('A3:A6', '项目图片', self.get_format_center(self.workbook))

        self.write_center(self.worksheet, "B3", '项目名称', self.workbook)
        self.write_center(self.worksheet, "B4", '项目版本', self.workbook)
        self.write_center(self.worksheet, "B5", '运行环境', self.workbook)
        self.write_center(self.worksheet, "B6", '测试网络', self.workbook)

        self.write_center(self.worksheet, "C3", data['test_name'], self.workbook)
        self.write_center(self.worksheet, "C4", data['test_version'], self.workbook)
        self.write_center(self.worksheet, "C5", data['test_pl'], self.workbook)
        self.write_center(self.worksheet, "C6", data['test_net'], self.workbook)

        self.write_center(self.worksheet, "D3", "用例总数", self.workbook)
        self.write_center(self.worksheet, "D4", "通过总数", self.workbook)
        self.write_center(self.worksheet, "D5", "失败总数", self.workbook)
        self.write_center(self.worksheet, "D6", "测试时间", self.workbook)

        self.write_center(self.worksheet, "E3", data1['test_sum'], self.workbook)
        self.write_center(self.worksheet, "E4", data1['test_success'], self.workbook)
        self.write_center(self.worksheet, "E5", data1['test_failed'], self.workbook)
        self.write_center(self.worksheet, "E6", data1['test_date'], self.workbook)

        self.write_center(self.worksheet, "F3", "分数", self.workbook)

        self.worksheet.merge_range('F4:F6', '%s'% score, self.get_format_center(self.workbook))

        self.pie(self.workbook, self.worksheet, title_name)

     # 生成饼形图
    def pie(self,wob, wos, title_name):
        chart1 = wob.add_chart({'type': 'pie'})
        chart1.add_series({
            'name': '%s统计' % title_name,
            'categories': '=%s总况!$D$4:$D$5' % title_name,
            'values': '=%s总况!$E$4:$E$5' % title_name,
        })
        chart1.set_title({'name': '%s统计' % title_name})
        chart1.set_style(10)
        wos.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})

    def test_detail(self,data,tmp,row):

        # 设置列行的宽高
        self.worksheet2.set_column("A:A", 16)
        self.worksheet2.set_column("B:B", 16)
        self.worksheet2.set_column("C:C", 25)
        self.worksheet2.set_column("D:D", 30)
        self.worksheet2.set_column("E:E", 25)
        self.worksheet2.set_column("F:F", 35)
        self.worksheet2.set_column("G:G", 20)
        self.worksheet2.set_column("H:H", 20)
        self.worksheet2.set_column("I:I", 11)
        for i in range(1,(row+2)):
            self.worksheet2.set_row(i, 40)
        self.worksheet2.merge_range('A1:I1', '测试详情', self.get_format(self.workbook, {'bold': True, 'font_size': 18 ,'align': 'center','valign': 'vcenter','bg_color': '#70DB93', 'font_color': '#ffffff'}))
        self.write_center(self.worksheet2, "A2", '用例名称', self.workbook)
        self.write_center(self.worksheet2,"B2", '请求接口', self.workbook)
        self.write_center(self.worksheet2,"C2", '请求方法', self.workbook)
        self.write_center(self.worksheet2, "D2", '请求报文', self.workbook)
        self.write_center(self.worksheet2,"E2", '预期结果', self.workbook)
        self.write_center(self.worksheet2,"F2", '响应报文', self.workbook)
        self.write_center(self.worksheet2,"G2", '数据库原值', self.workbook)
        self.write_center(self.worksheet2,"H2", '数据库现值', self.workbook)
        self.write_center(self.worksheet2, "I2", '测试结果', self.workbook)

        temp = tmp+2
        for item in data:
            self.write_center(self.worksheet2,"A"+str(temp), item["t_name"], self.workbook)
            self.write_center(self.worksheet2,"B"+str(temp), item["t_url"], self.workbook)
            self.write_center(self.worksheet2,"C"+str(temp), item["t_method"], self.workbook)
            self.write_center(self.worksheet2,"D"+str(temp), item["t_request_body"], self.workbook)
            self.write_center(self.worksheet2,"E"+str(temp), item["t_hope"], self.workbook)
            self.write_center(self.worksheet2,"F"+str(temp), item["t_response_body"], self.workbook)
            self.write_center(self.worksheet2,"G"+str(temp), item["old_database_value"], self.workbook)
            self.write_center(self.worksheet2, "H" + str(temp), item["new_database_value"], self.workbook)
            self.write_center(self.worksheet2, "I" + str(temp), item["t_result"], self.workbook)
            temp = temp-1

        self.worksheet.hide_gridlines(2)    # 隐藏网格线
        self.worksheet2.hide_gridlines(2)   # 隐藏网格线

    def __del__(self):
        self.workbook.close()

