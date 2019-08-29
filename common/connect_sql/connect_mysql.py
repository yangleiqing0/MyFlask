# encoding=utf-8
import pymysql


class ConnMysql:

    def __init__(self, host, port, user, password, db_name):
        print('ConnMysql:', host, port, user, password, db_name)
        self.db = pymysql.connect(host=host, port=port, user=user,
                                  passwd=password, db=db_name, charset='utf8')

    def select_mysql(self, sql):
        print('sql:', sql)
        if not sql:
            return 'sql语句不可为空'
        cur = self.db.cursor()
        cur.execute(sql)
        r = cur.fetchall()
        print('ConnMysql result:', r)
        cur.close()
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