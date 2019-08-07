# FLASK_LOGS_FILE = '../logs/flask.log'
# with open(FLASK_LOGS_FILE) as logs:
#     flask_logs = logs.readlines()
#     flask_logs = "<br/>".join(flask_logs[len(flask_logs) - 10:])
# print(flask_logs[len(flask_logs) - 10:], "flask_logs: ", flask_logs)

# import requests
# ht = requests.get('http://www.woniuxy.com').text
# print(ht)
def te():
    a=0
    while 1:
        a += 1
        if a ==10:
            return a
print(te())