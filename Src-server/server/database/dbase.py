import MySQLdb as mysql
import logger

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

    # Used to get first three letters of month by the month's integer value
    string_months = {
        1 : "Jan",
        2 : "Feb",
        3 : "Mar",
        4 : "Apr",
        5 : "May",
        6 : "Jun",
        7 : "Jul",
        8 : "Aug",
        9 : "Sep",
        10 : "Oct",
        11 : "Nov",
        12 : "Dec",
    }

    # Used to get month in string by the month's integer value
    string_full_months = {
        1 : "January",
        2 : "February",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10 : "October",
        11 : "November",
        12 : "December",
    }

    # Used to get the end day of a month
    end_day_of_month = {
         1 : 31,
         2 : 28,
         3 : 31,
         4 : 30,
         5 : 31,
         6 : 30,
         7 : 31,
         8 : 31,
         9 : 30,
         10 : 31,
         11 : 30,
         12 : 31,
    }

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
        try :
            connection = mysql.connect(
                host=self._mysqlHost, user=self._mysqlUser,
                passwd=self._mysqlPassword, db=self._mysqlDatabase,
                port=self._mysqlPort
            )
            connection.autocommit(False)
            self._connection = connection
        except Exception:
            pass
            # logger.logKnowledge("error", "database.py-connect", e)

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
    def execute(self, query, param):
        cursor = self.cursor()
        assert cursor is not None
        return cursor.execute(query, param)

    ########################################################
    # To execute a query
    ########################################################
    def execute_insert(self, query, param):
        cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query, param)
        return int(cursor.lastrowid)


########################################################
# To execute select query
# Used to fetch multiple rows
# select_all : query is string and param is tuple which return result in tuple of tuples
# select_one : query is string and param is typle which return result in tuple
########################################################
    def select_all(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None
        assert type(query) is not str
        try:
            if param is None :
                cursor.execute(query)
            else :
                cursor.execute(query, param)
            return cursor.fetchall()
        except Exception, e:
            logger.logClientApi("select_all", query)
            logger.logClientApi("select_all", e)
            return

    def select_one(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None
        assert type(param) is not tuple
        assert type(query) is not str
        try:
            if param is None :
                cursor.execute(query)
            else :
                cursor.execute(query, param)
            return cursor.fetchone()
        except Exception, e:
            logger.logClientApi("select_one", query)
            logger.logClientApi("select_one", e)
            return

    ########################################################
    # To form a select query
    # params : table_name, list of columns and where condition
    # returns result in list of dictionary
    ########################################################
    def get_data(
        self, table, columns, condition
    ):
        assert type(columns) in (list, str)
        param = []
        if type(columns) is str :
            param = columns.split(',')
        elif type(columns) is list :
            param = columns
            columns = ", ".join(columns)

        query = "SELECT %s FROM %s " % (columns, table)
        if condition is not None :
            query += " WHERE %s"
            rows = self.select_all(query, condition)
        else :
            rows = self.select_all(query)

        result = []
        if rows :
            result = self.convert_to_dict(rows, param)
        return result

    ########################################################
    # To form a join query
    ########################################################
    def get_data_from_multiple_tables(
        self, columns, tables, aliases, join_type,
        join_conditions, where_condition
    ):
        query = "SELECT %s FROM " % columns

        for index, table in enumerate(tables):
            if index == 0:
                query += "%s  %s  %s" % (
                    table, aliases[index], join_type
                )
            elif index <= len(tables) - 2:
                query += " %s %s on (%s) %s " % (
                    table, aliases[index],
                    join_conditions[index-1], join_type
                )
            else:
                query += " %s %s on (%s)" % (
                    table, aliases[index],
                    join_conditions[index-1]
                )

        query += " where %s" % where_condition
        return self.select_all(query)

    ########################################################
    # To form a insert query
    ########################################################
    def insert(self, table, columns, values, client_id=None) :
        columns = ", ".join(columns)
        stringValue = []
        for i in values :
            stringValue.append('%s')

        query = """INSERT INTO %s (%s) VALUES (%s) """
        params = []
        params.append(table)
        params.append(columns)
        params.append(",".join(stringValue))
        try:
            return self.execute_insert(query, params)
        except Exception, e:
            logger.logKnowledgeApi("insert", query)
            logger.logKnowledgeApi("insert", e)
            return False

    ########################################################
    # To form a bulk insert query
    ########################################################
    def bulk_insert(self, table, columns, valueList, client_id=None) :
        query = "INSERT INTO %s (%s)  VALUES" % (
            table, ",".join(str(x) for x in columns)
        )
        for index, value in enumerate(valueList):
            if index < len(valueList)-1:
                query += "%s," % str(value)
            else:
                query += str(value)
        try:
            return self.execute(query)
        except Exception, e:
            logger.logKnowledgeApi("bulk_insert", query)
            logger.logKnowledgeApi("bulk_insert", e)
            return

    ########################################################
    # To form a update query
    ########################################################
    def update(self, table, columns, values, condition, client_id=None) :
        query = "UPDATE "+table+" set "
        for index, column in enumerate(columns):
            if index < len(columns)-1:
                query += column+" = '%s', "
            else:
                query += column+" = '%s' "

        query += " WHERE " + condition
        try:
            return self.execute(query, values)
        except Exception, e:
            logger.logKnowledgeApi("update", query)
            logger.logKnowledgeApi("update", e)
            return

    ########################################################
    # Insert a row If already key exists
    # else update the columns specified in the
    # updateColumns list
    ########################################################
    def on_duplicate_key_update(
        self, table, columns, valueList,
        updateColumnsList, client_id=None
    ):
        query = "INSERT INTO %s (%s) VALUES " % (table, columns)

        for index, value in enumerate(valueList):
            if index < len(valueList)-1:
                query += "%s," % str(value)
            else:
                query += "%s" % str(value)

        query += " ON DUPLICATE KEY UPDATE "

        for index, updateColumn in enumerate(updateColumnsList):

            if index < len(updateColumnsList)-1:
                query += "%s = VALUES(%s)," % (updateColumn, updateColumn)
            else:
                query += "%s = VALUES(%s)" % (updateColumn, updateColumn)

        return self.execute(query)

    ########################################################
    # To form a delete query
    ########################################################
    def delete(self, table, condition, client_id=None):
        query = "DELETE from "+table+" WHERE "+condition
        try:
            return self.execute(query)
        except Exception, e:
            logger.logClientApi("delete", query)
            logger.logClientApi("delete", e)
            return

    ########################################################
    # To concate the value with the existing value in the
    # specified column
    ########################################################
    def append(self, table, column, value, condition):
        rows = self.get_data(table, column, condition)
        currentValue = rows[0][0]
        if currentValue is not None:
            newValue = currentValue+","+str(value)
        else:
            newValue = str(value)
        columns = [column]
        values = [newValue]
        return self.update(table, columns, values, condition)

    ########################################################
    # To increment value in the specified column by the
    # passed value. This function can be used only for int,
    # float, double values
    ########################################################

    def increment(self, table, column, condition, value=1):
        rows = self.get_data(table, column, condition)
        currentValue = rows[0][0]
        if currentValue is not None:
            newValue = int(currentValue) + value
        else:
            newValue = value
        columns = [column]
        values = [newValue]
        return self.update(table, columns, values, condition)

    ########################################################
    # To check whether a row exists with the condition in the
    # given table. if a row exists this function will return
    # True otherwise returns false
    ########################################################

    def is_already_exists(self, table, condition, client_id=None) :
        query = "SELECT count(*) FROM "+table+" WHERE "+condition
        rows = None
        rows = self.select_all(query)
        if rows[0][0] > 0:
            return True
        else :
            return False

    ########################################################
    # To check whether a row exists with the "value"
    # for the column "field". if a row exists this function
    # will return True otherwise return false
    ########################################################
    def is_invalid_id(self, table, field, value, client_id=None):
        condition = "%s = '%d'" % (field, value)
        return not self.is_already_exists(table, condition)
