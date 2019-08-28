import pymysql


class ConnMysql:

    def __init__(self, host, port, user, password, db_name):
        self.db = pymysql.connect(host=host, port=port, user=user,
                                  passwd=password, db=db_name, charset='utf8')

    def select_mysql(self, sql):
        cur = self.db.cursor()
        cur.execute(sql)
        r = cur.fetchall()
        if r == ():
            return '查询结果为空',
        return r[0]

    def operate_mysql(self, sql):
        cur = self.db.cursor()
        cur.execute(sql)

    def __del__(self):
        self.db.commit()
        self.db.close()


if __name__ == "__main__":
    ConnMysql().select_mysql('select name from zdbm_license_infos where id=1')