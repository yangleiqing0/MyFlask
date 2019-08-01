from logs.config import FLASK_LOGS_FILE
with open(FLASK_LOGS_FILE) as logs:
    flask_logs = logs.readlines()
    flask_logs = "<br/>".join(flask_logs[len(flask_logs) - 10:])
print(flask_logs[len(flask_logs) - 10:], "flask_logs: ", flask_logs)

