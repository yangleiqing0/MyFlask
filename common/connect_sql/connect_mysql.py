# encoding=utf-8
import pymysql
from common.analysis_params import AnalysisParams


class ConnMysql:

    def __init__(self, host, port, user, password, db_name, sql):
        print('ConnMysql:', host, port, user, password, db_name, sql)
        self.db = pymysql.connect(host=host, port=port, user=user,
                                  passwd=password, db=db_name, charset='utf8')
        if sql:
            sql = AnalysisParams().analysis_params(sql)
        self.sql = sql

    def select_mysql(self):
        if not self.sql:
            return 'sql语句不可为空'
        cur = self.db.cursor()
        cur.execute(self.sql)
        r = cur.fetchall()
        print('ConnMysql result:', r)
        cur.close()
        if not r:
            return ''
        elif len(r) == 1:
            if len(r[0]) == 1:
                print('r', len(r[0]), r[0])
                return r[0][0]
            return r[0]
        return r

    def operate_mysql(self, sql):
        cur = self.db.cursor()
        cur.execute(sql)
        self.db.commit()
        cur.close()

    def __del__(self):
        self.db.close()


if __name__ == "__main__":
    ConnMysql().select_mysql('select name from zdbm_license_infos where id=1')