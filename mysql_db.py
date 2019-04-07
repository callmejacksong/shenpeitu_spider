import pymysql

class DB:

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def get_con(self):
        self.conn = pymysql.connect(charset="utf8",host=self.host,port=self.port,user=self.user,password=self.password, database=self.db)

    def get_cursor(self):
        try:
            self.conn.ping()
            print("ping ok")
        except:
            self.get_con()
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.cursor().close()
        self.conn.close()
        print("mysql数据库连接已关闭")
        return True

