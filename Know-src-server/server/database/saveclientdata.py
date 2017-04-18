import MySQLdb as mysql
from server.dbase import Database
from server.exceptionmessage import process_error
from server.database.general import get_group_servers_db_info
__all__ = [
    "ClientdbConect",
    "SaveRegistrationData"
]

class ClientdbConect(object):
    def __init__(self):
        self._k_db = None

    def get_client_connect(self, db_host, db_port, db_username, db_password, db_name):
        if db_host is None:
            return
        conn = mysql.connect(
            host=db_host, port=db_port,
            user=db_username, passwd=db_password,
            db=db_name
        )
        print conn
        self._k_db = Database(conn)

    def get_client_close(self):
        if self._k_db is not None :
            self._k_db.close()

class SaveRegistrationData(ClientdbConect):
    def __init__(self, know_db, token, expiry, email_id, client_id, email_date, u_id):
        super(SaveRegistrationData, self).__init__()
        self.know_db = know_db
        self.token = token
        self.expiry = expiry
        self.email_id = email_id
        self.client_id = client_id
        self.email_date = email_date
        self.u_id = u_id
        self.is_group = True

        self._host = None
        self._port = None
        self._db_name = None
        self._db_username = None
        self._db_password = None
        self.get_client_info()
        self.process_save_token()

    def get_client_info(self):
        rows = get_group_servers_db_info(self.know_db, self.client_id)
        if rows :
            r = rows[0]
            print r
            self._host = r["database_ip"]
            self._port = r["database_port"]
            self._db_name = r["database_name"]
            self._db_username = r["database_username"]
            self._db_password = r["database_password"]

    def _save_token(self):
        try :
            qq = "select user_id from tbl_users where user_category_id = 1 and email_id = %s"
            user_id_rows = self._k_db.select_all(qq, [self.email_id])
            print user_id_rows
            # print user_id_rows["user_id"]
            if user_id_rows :
                user_id = user_id_rows["user_id"]
            else :
                user_id = 1

            if user_id :
                self._k_db.execute("delete from tbl_email_verification where user_id = %s and verification_type_id = 1", [user_id])
                q = "insert into tbl_email_verification(user_id, verification_code, " + \
                    " verification_type_id, expiry_date ) values(%s, %s, %s, %s)"
                self._k_db.execute(q, [user_id, self.token, 1, self.expiry])

        except Exception, e :
            print e

    def process_save_token(self):
        try:
            print self._host, self._port, self._db_username, self._db_password, self._db_name
            self.get_client_connect(self._host, self._port, self._db_username, self._db_password, self._db_name)
            # self._k_db.begin()
            self._k_db._cursor = self._k_db._connection.cursor()
            self._save_token()
            self._k_db._cursor.close()
            self._k_db._connection.commit()
            self._k_db._connection.close()
        except Exception, e:
            print e
            if self._k_db is None:
                return
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            self._k_db._connection.close()
            raise process_error("E090")
