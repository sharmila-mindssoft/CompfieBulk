import MySQLdb as mysql
from processes.process_logger import logProcessError

def fetch_error():
    return RuntimeError("Transaction failed while processing data.")

class Database(object):
    def __init__(
        self,
        mysqlHost, mysqlPort, mysqlUser,
        mysqlPassword, mysqlDatabase
    ):
        self._mysqlHost = mysqlHost
        self._mysqlPort = mysqlPort
        self._mysqlUser = mysqlUser
        self._mysqlPassword = mysqlPassword
        self._mysqlDatabase = mysqlDatabase
        self._connection = None
        self._cursor = None
        self._for_client = False

    ########################################################
    # To Redirect Requests to Functions
    ########################################################
    def cursor(self):
        return self._cursor

    ########################################################
    # To Establish database connection
    ########################################################
    def connect(self):
        assert self._connection is None
        try:
            connection = mysql.connect(
                host=self._mysqlHost, user=self._mysqlUser,
                passwd=self._mysqlPassword, db=self._mysqlDatabase,
                port=self._mysqlPort
            )
            connection.autocommit(False)
            self._connection = connection
        except Exception, e:
            print e
            self._connection = None

    def _db_connect(self, host, username, password, database):
        return mysql.connect(host, username, password, database)

    ########################################################
    # To Close database connection
    ########################################################
    def close(self):
        assert self._connection is not None
        self._connection.close()
        self._connection = None

    ########################################################
    # To begin a database transaction
    ########################################################
    def begin(self):
        assert self._connection is not None
        assert self._cursor is None
        self._cursor = self._connection.cursor()
        return self._cursor

    ########################################################
    # To commit a database transaction
    ########################################################
    def commit(self):
        assert self._connection is not None
        assert self._cursor is not None
        self._cursor.close()
        self._connection.commit()
        self._cursor = None

    ########################################################
    # To rollback a connection
    ########################################################
    def rollback(self):
        assert self._connection is not None
        assert self._cursor is not None
        self._cursor.close()
        self._connection.rollback()
        self._cursor = None

    ########################################################
    # To execute a query
    ########################################################
    def execute(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if type(param) is tuple:
                cursor.execute(query, param)
            elif type(param) is list:
                cursor.execute(query, param)
            else:
                cursor.execute(query)
            return True
        except mysql.Error, e:
            print e
            # print query
            # print param
            return False

    ########################################################
    # To execute a query
    ########################################################
    def execute_insert(self, query, param):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if type(param) is tuple:
                cursor.execute(query, param)
            elif type(param) is list:
                # print "inside elif "
                cursor.execute(query, param)
            else:
                cursor.execute(query)
            return int(cursor.lastrowid)
        except mysql.Error, e:
            print e
            logProcessError("insert", str(e))
            # print query
            # print param
            return False

    ########################################################
    # To execute select query
    # Used to fetch multiple rows
    # select_all : query is string and param is tuple which return result in tuple of tuples
    # select_one : query is string and param is typle which return result in tuple
    ########################################################
    def select_all(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if param is None:
                cursor.execute(query)
            else:
                if type(param) is tuple:
                    cursor.execute(query, param)

                elif type(param) is list:
                    cursor.execute(query, param)

                else:
                    cursor.execute(query)
            res = cursor.fetchall()
            return res
        except mysql.Error, e:
            print e
            logProcessError("select", str(e))
            # print query
            # print param
            raise fetch_error()

    def select_one(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None

        try:
            if param is None:
                cursor.execute(query)
            else:
                if type(param) is tuple:
                    cursor.execute(query, param)
                elif type(param) is list:
                    cursor.execute(query, param)
                else:
                    cursor.execute(query)
            res = cursor.fetchone()
            return res
        except mysql.Error, e:
            print "Exception"
            # print query
            # print param
            print e
            logProcessError("select_one", str(e))
            raise fetch_error()

    def generate_tuple_condition(self, column, values_list):
        condition = " 1 "
        condition_val = "%"
        if values_list not in [None, ""]:
            if len(values_list) > 1:
                condition = " %s in %s " % (column, "%s")
                condition_val = tuple(values_list)
            else:
                condition = " %s = %s " % (column, "%s")
                condition_val = values_list[0]
        return condition, condition_val

    ########################################################
    # To form a insert query
    ########################################################
    def insert(self, table, columns, values):
        # columns = ", ".join(columns)
        stringValue = []
        for i in range(len(values)):
            stringValue.append('%s')

        if type(columns) is list:
            columns = ", ".join(columns)
            columns = "(%s)" % columns

        query = """INSERT INTO %s %s """ % (table, columns)
        query += " VALUES (%s) " % (",".join(stringValue))
        try:
            n_id = int(self.execute_insert(query, values))
            return n_id
        except mysql.Error, e:
            print e
            logProcessError("insert", str(e))
            # print query, values
            return False

    ########################################################
    # To form a bulk insert query
    ########################################################
    def bulk_insert(self, table, columns, valueList):

        stringValue = []
        for i in range(len(columns)):
            stringValue.append('%s')

        if type(columns) is list:
            columns = ", ".join(columns)
        query = "INSERT INTO %s (%s) " % (table, columns)
        query += " VALUES (%s) " % (",".join(stringValue))

        try:
            cursor = self.cursor()
            assert cursor is not None
            cursor.executemany(query, valueList)
            return True
        except mysql.Error, e:
            print e
            logProcessError("bulk-insert", str(e))
            return False

    ########################################################
    # To form a update query
    ########################################################
    def update(self, table, columns, values, condition):
        query = "UPDATE "+table+" set "
        for index, column in enumerate(columns):
            if index < len(columns)-1:
                query += column+" = %s, "
            else:
                query += column+" = %s "

        query += " WHERE " + condition
        # print query
        try:
            status = self.execute(query, values)
            return status
        except mysql.Error, e:
            logProcessError("update", str(e))
            print query, values
            print e
            return False
