import MySQLdb as mysql
import logger
from server.common import (convert_to_dict, get_date_time)
from server.exceptionmessage import fetch_error, process_procedure_error


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

    # Used to get first three letters of month by the month's integer value
    string_months = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    # Used to get month in string by the month's integer value
    string_full_months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    # Used to get the end day of a month
    end_day_of_month = {
         1: 31,
         2: 28,
         3: 31,
         4: 30,
         5: 31,
         6: 30,
         7: 31,
         8: 31,
         9: 30,
         10: 31,
         11: 30,
         12: 31,
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
        try:
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
        # assert self._cursor is None
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
                logger.logQuery(self._for_client, "execute", query % param)
                cursor.execute(query, param)
            elif type(param) is list:
                if len(param) > 1:
                    logger.logQuery(
                        self._for_client, "execute", query % tuple(param)
                    )
                else:
                    logger.logQuery(
                        self._for_client, "execute", query % param[0]
                    )
                cursor.execute(query, param)
            else:
                logger.logQuery(self._for_client, "execute", query)
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
                logger.logQuery(
                    self._for_client, "execute_insert", query % param
                )
                cursor.execute(query, param)
            elif type(param) is list:
                if len(param) > 1:
                    logger.logQuery(
                        self._for_client, "execute_insert",
                        query % tuple(param)
                    )
                else:
                    logger.logQuery(
                        self._for_client, "execute_insert", query % param[0]
                    )
                cursor.execute(query, param)
            else:
                logger.logQuery(self._for_client, "execute_insert")
                cursor.execute(query)
            return int(cursor.lastrowid)
        except mysql.Error, e:
            print e
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
                    logger.logQuery(
                        self._for_client, "select_all", query % param
                    )
                    cursor.execute(query, param)

                elif type(param) is list:
                    if len(param) > 1:
                        logger.logQuery(
                            self._for_client, "select_all",
                            query % tuple(param)
                        )
                    else:
                        logger.logQuery(
                            self._for_client, "select_all", query % param
                        )
                    cursor.execute(query, param)

                else:
                    logger.logQuery(self._for_client, "select_all", query)
                    cursor.execute(query)
            res = cursor.fetchall()
            return res
        except mysql.Error, e:
            print e
            # print query
            # print param
            logger.logClientApi("select_all", query)
            logger.logClientApi("select_all", e)
            raise fetch_error()

    def select_one(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None

        try:
            if param is None:
                cursor.execute(query)
            else:
                if type(param) is tuple:
                    logger.logQuery(
                        self._for_client, "select_one", query % param
                    )
                    cursor.execute(query, param)
                elif type(param) is list:
                    if len(param) > 1:
                        logger.logQuery(
                            self._for_client, "select_one",
                            query % tuple(param)
                        )
                    else:
                        logger.logQuery(
                            self._for_client, "select_one", query % param
                        )
                    cursor.execute(query, param)
                else:
                    logger.logQuery(
                        self._for_client, "select_one", query % param
                    )
                    cursor.execute(query)
            res = cursor.fetchone()
            return res
        except mysql.Error, e:
            print "Exception"
            # print query
            # print param
            print e
            logger.logClientApi("select_one", query)
            logger.logClientApi("select_one", e)
            raise fetch_error()

    ########################################################
    # To form a select query
    # params : table_name, list of columns and where condition
    # returns result in list of dictionary
    ########################################################
    def get_data(
        self, table, columns, condition, condition_val=None, order=None
    ):
        assert type(columns) in (list, str)
        param = []
        if type(columns) is str:
            param = columns.split(',')
            params = []
            for p in param:
                if "as " in p:
                    params.append(p.split('as ')[1].strip())
                elif '.' in p:
                    params.append(p.split('.')[1].strip())
                else:
                    params.append(p.strip())
            param = params
        elif type(columns) is list:
            param = []
            for c in columns:
                if "as " in c:
                    param.append(c.split('as ')[1].strip())
                elif '.' in c:
                    param.append(c.split('.')[1].strip())
                else:
                    param.append(c.strip())
            columns = ", ".join(columns)

        query = "SELECT %s FROM %s " % (columns, table)
        if condition is not None:
            query += " WHERE %s " % condition
            if order is not None:
                query += order
            # print query
            # print condition_val
            if condition_val is None:
                logger.logQuery(self._for_client, "get_data", query)
                rows = self.select_all(query)
            else:
                logger.logQuery(
                    self._for_client, "get_data", query % tuple(condition_val)
                )
                rows = self.select_all(query, condition_val)

        else:
            if order is not None:
                query += order
            logger.logQuery(self._for_client, "get_data", query)
            rows = self.select_all(query)
        result = []
        # print rows
        if rows:
            result = convert_to_dict(rows, param)
        return result

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
    # To form a join query
    ########################################################
    def get_data_from_multiple_tables(
        self, columns, tables, aliases, join_type,
        join_conditions, where_condition, where_condition_val=None
    ):
        assert type(columns) in (list, str)
        param = []
        if type(columns) is str:
            param = columns.split(',')
            params = []
            for p in param:
                if '.' in p:
                    params.append(p.split('.')[1].strip())
                else:
                    params.append(p.strip())
            param = params
        elif type(columns) is list:
            param = []
            for c in columns:
                if "as " in c:
                    param.append(c.split('as ')[1].strip())
                elif '.' in c:
                    param.append(c.split('.')[1].strip())
                else:
                    param.append(c.strip())
            columns = ", ".join(columns)

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

        if where_condition is not None:
            query += " WHERE %s " % (where_condition)
            logger.logQuery(
                self._for_client, "get_data_from_multiple_tables", query
            )
        else:
            logger.logQuery(
                self._for_client, "get_data_from_multiple_tables", query
            )
        if where_condition_val is not None:
            # print query
            # print where_condition_val
            rows = self.select_all(query, where_condition_val)
        else:
            # print query
            rows = self.select_all(query)

        result = []
        if rows:
            result = convert_to_dict(rows, param)
        return result

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
            # print query, values
            logger.logKnowledgeApi("insert", query + " -- " + values)
            logger.logKnowledgeApi("insert", e)
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
            logger.logKnowledgeApi("bulk_insert", query)
            logger.logKnowledgeApi("bulk_insert", e)
            return False

    ########################################################
    # To form a bulk update query
    ########################################################
    def bulk_update(self, table, columns, values, conditions):
        try:
            for outer_index, cond in enumerate(conditions):
                query = "UPDATE "+table+" set "
                for index, column in enumerate(columns):
                    if values[outer_index][index] is not None:
                        if(index < len(columns)-1):
                            query += column+" = '%s', " % (
                                values[outer_index][index])
                        else:
                            query += column+" = '%s' " % values[outer_index][index]
                query += " WHERE " + cond + "; "
                cursor = self.cursor()
                assert cursor is not None
                cursor.execute(query)
            return True
        except mysql.Error, e:
            print e
            logger.logKnowledgeApi("bulk_update", query)
            logger.logKnowledgeApi("bulk_update", e)
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
            print query, values
            print e
            logger.logKnowledgeApi("update", query + " , " + values)
            logger.logKnowledgeApi("update", e)
            return False

    ########################################################
    # Insert a row If already key exists
    # else update the columns specified in the
    # updateColumns list
    ########################################################
    def on_duplicate_key_update(
        self, table, columns, valueList, updateColumnsList
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
    def delete(self, table, condition, condition_val):
        query = "DELETE from "+table+" WHERE "+condition
        try:
            return self.execute(query, condition_val)
        except mysql.Error, e:
            print e
            logger.logClientApi("delete", query)
            logger.logClientApi("delete", e)
            return

    ########################################################
    # To concate the value with the existing value in the
    # specified column
    ########################################################
    def append(self, table, column, value, condition, condition_val):
        try:
            rows = self.get_data(table, column, condition, condition_val)
            currentValue = rows[0][column]
            if currentValue is not None:
                newValue = currentValue+","+str(value)
            else:
                newValue = str(value)
            columns = [column]
            values = [newValue]
            values += condition_val
            res = self.update(
                table, columns, values, condition)
            return res
        except mysql.Error, e:
            print table, column, value
            print e
            return False

    ########################################################
    # To increment value in the specified column by the
    # passed value. This function can be used only for int,
    # float, double values
    ########################################################

    def increment(self, table, column, condition, value=1, condition_val=None):
        rows = self.get_data(table, column, condition, condition_val)
        currentValue = int(rows[0][column[0]]) if(
            rows[0][column[0]] is not None) else 0
        if currentValue is not None:
            newValue = int(currentValue) + value
        else:
            newValue = value
        values = [newValue]
        if condition_val is not None:
            values = values + condition_val
        return self.update(table, column, values, condition)

    ########################################################
    # To check whether a row exists with the condition in the
    # given table. if a row exists this function will return
    # True otherwise returns false
    ########################################################
    def is_already_exists(self, table, condition, condition_val):
        query = "SELECT count(0) FROM %s WHERE %s " % (table, condition)
        rows = None
        rows = self.select_one(query, condition_val)
        if rows:
            if rows[0] > 0:
                return True
            else:
                return False
        else:
            return False

    ########################################################
    # To check whether a row exists with the "value"
    # for the column "field". if a row exists this function
    # will return True otherwise return false
    ########################################################
    def is_invalid_id(self, table, field, value, client_id=None):
        condition = field + "= %s"
        condition_val = [value]
        return not self.is_already_exists(table, condition, condition_val)

    ########################################################
    # To generate a new Id for the given table and given
    # field
    ########################################################
    def get_new_id(self, field, table_name, client_id=None):
        new_id = 1
        query = "SELECT max(%s) from %s " % (field, table_name)
        row = self.select_one(query)
        if row[0] is not None:
            new_id = int(row[0]) + 1
        return new_id

    def save_activity(self, user_id, form_id, action):
        created_on = get_date_time()
        activityId = self.get_new_id("activity_log_id", "tbl_activity_log")
        query = " INSERT INTO tbl_activity_log " + \
            " (activity_log_id, user_id, form_id, action, created_on) " + \
            " VALUES (%s, %s, %s, %s, %s) "
        self.execute(query, (
                activityId, user_id, form_id, action, created_on
        ))
        return True

    def validate_session_token(self, session_token):
        query = "SELECT t01.user_id FROM tbl_user_sessions t01 " + \
            " LEFT JOIN tbl_users t02 ON t01.user_id = t02.user_id " + \
            " and is_active = 1 " + \
            " WHERE  session_token=%s"
        param = [session_token]
        row = self.select_one(query, param)
        user_id = None
        if row:
            user_id = row[0]
            self.update_session_time(session_token)
        return user_id

    def update_session_time(self, session_token):
        q = '''
            update tbl_user_sessions set last_accessed_time = now()
            where session_token = %s'''
        self.execute(q, [str(session_token)])

    def clear_session(self, session_cutouff):
        q = "delete from tbl_user_sessions where " + \
            " last_accessed_time < DATE_SUB(NOW(),INTERVAL %s MINUTE)"
        self.execute(q, [session_cutouff])

    def reconnect(self):
        self.close()
        self.connect()

    def call_proc(self, procedure_name, args, columns=None):
        # columns no longer need here, so remove argument once removed from the reference place
        # args is tuple e.g, (parm1, parm2)
        cursor = self.cursor()
        assert cursor is not None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)
        except Exception, e:
            print e
            raise process_procedure_error(procedure_name, args, e)

        cols = [x[0] for x in cursor.description]
        rows = []
        rows = convert_to_dict(cursor.fetchall(), cols)
        cursor.nextset()
        return rows

    def call_insert_proc(self, procedure_name, args):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)
        except Exception, e:
            print e
            raise process_procedure_error(procedure_name, args, e)

        cursor.nextset()
        cursor.execute("SELECT LAST_INSERT_ID()")
        r = cursor.fetchone()
        new_id = r[0]
        return new_id

    def call_update_proc(self, procedure_name, args):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)
        except Exception, e:
            print e
            raise process_procedure_error(procedure_name, args, e)
        cursor.nextset()
        return True

    def call_proc_with_multiresult_set(self, procedure_name, args, expected_result_count):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)
        except Exception, e:
            print e

        rows = []
        print type(expected_result_count)
        assert type(expected_result_count) is int
        for i in range(0, expected_result_count):
            cols = [x[0] for x in cursor.description]
            r = convert_to_dict(cursor.fetchall(), cols)
            rows.append(r)
            cursor.nextset()

        return rows
