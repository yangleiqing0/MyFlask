# FLASK_LOGS_FILE = '../logs/flask.log'
# with open(FLASK_LOGS_FILE) as logs:
#     flask_logs = logs.readlines()
#     flask_logs = "<br/>".join(flask_logs[len(flask_logs) - 10:])
# print(flask_logs[len(flask_logs) - 10:], "flask_logs: ", flask_logs)

# import requests
# ht = requests.get('http://www.woniuxy.com').text
# print(ht)
# #
# a = 12
# print(a in(None, "None"))
# import datetime
# print(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
import re
# a = '{"code":0,"data":{"user":{"id":56,"createdAt":"2019-08-13T10:49:23.534204197+08:00","updatedAt":"2019-08-13T10:49:23.534204197+08:00","username":"ehYSvD","name":"","mail":"1@q.com","phone":"","enable":true,"isInitialCipher":true}},"errMsg":""}	'
# passent = re.compile(r'\"id\":([^,]+)')
# c = passent.findall(a)[0]
# print(c)
a = [1,2,3,4,5]
a = a[-2:]
for i in range(len(a)):
    a[i] += 1
    print(a[i])
for a1 in a:
    a1 += 1
print(a)
