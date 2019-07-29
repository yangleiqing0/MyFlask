import sqlite3
import config




class cdb:
    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE_URL)

    def db_cur(self):
        return self.conn.cursor()

    def query_db(self, sql, params=None, one=False):
        try:
            self.cur = self.db_cur()
            if params:
                self.re = self.cur.execute(sql, params)
            else:
                self.re = self.cur.execute(sql)
            if one:
                self.result = self.re.fetchone()
            else:
                self.result = self.re.fetchall()
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