from logs.config import FRONT_LOGS_FILE


class FrontLogs:

    def __init__(self, content):
        self.content = content

    def add_to_front_log(self):

        with open(FRONT_LOGS_FILE, 'a') as logs:
            logs.write(self.content+'\n')