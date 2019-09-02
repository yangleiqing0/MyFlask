import pymysql
from config import host, port, root, pwd, db


class cdb:
    # def __init__(self):
    #     self.conn = sqlite3.connect(config.DATABASE_URL)
    #     self.cur = self.re = self.result = None

    def __init__(self):
        self.conn = pymysql.connect(host, root, pwd, db, port, charset='utf8mb4')

    def db_cur(self):
        return self.conn.cursor()

    def query_db(self, sql, params='', one=False):
        try:
            self.cur = self.db_cur()
            if params:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)
            if one:
                self.result = self.cur.fetchone()
            else:
                self.result = self.cur.fetchall()
            return self.result
        finally:
            self.cur.close()
            self.conn.close()

    def opeat_db(self, sql, params):
        try:
            self.cur = self.db_cur()
            self.cur.execute(sql, params)
            self.conn.commit()
        finally:
            self.conn.close()
