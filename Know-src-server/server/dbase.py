# from flaskext.mysql import MySQL
import logger
from server.common import (convert_to_dict, get_date_time)
from server.exceptionmessage import fetch_error, process_procedure_error

class BaseDatabase(object):
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

    def dbConfig(self, app):
        app.config['MYSQL_DATABASE_USER'] = self._mysqlUser
        app.config['MYSQL_DATABASE_PASSWORD'] = self._mysqlPassword
        app.config['MYSQL_DATABASE_DB'] = self._mysqlDatabase
        app.config['MYSQL_DATABASE_HOST'] = self._mysqlHost
        self._mysql.init_app(app)

    def connect(self):
        assert self._connection is None
        try:
            connection = self._mysql.get_db
            connection.autocommit(True)
            self._connection = connection
            logger.logKnowledge("info", "database connection initiate", "")
            return self._connection
        except Exception, e:
            logger.logKnowledge("error", "database.py-connect", e)


class Database(object):
    def __init__(
        self,
        mysqlConnection
    ):
        self._connection = mysqlConnection
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
    # def connect(self):
    #     assert self._connection is None
    #     try:
    #         connection = mysql.connect(
    #             host=self._mysqlHost, user=self._mysqlUser,
    #             passwd=self._mysqlPassword, db=self._mysqlDatabase,
    #             port=self._mysqlPort
    #         )
    #         connection.autocommit(True)
    #         self._connection = connection
    #     except Exception:
    #         pass
    #         # logger.logKnowledge("error", "database.py-connect", e)

    def _db_connect(self, host, username, password, database):
        pass
        # return mysql.connect(host, username, password, database)

    ########################################################
    # To Close database connection
    ########################################################
    def close(self):
        assert self._connection is not None
        if self._cursor is not None :
            self._cursor.close()
        self._connection.close()
        self._connection = None

    ########################################################
    # To begin a database transaction
    ########################################################
    def begin(self):
        assert self._connection is not None
        assert self._cursor is None
        self._cursor = self._connection.cursor(dictionary=True, buffered=True)
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

            logger.logKnowledge("query", "execute", "query: %s, param:%s" % (query, param))
            cursor.nextset()
            return True

        except Exception, e:
            logger.logKnowledge("error", "execute", "query: %s, param:%s" % (query, param))
            logger.logKnowledge("error", "execute", str(e))
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
                cursor.execute(query, param)
            else:
                cursor.execute(query)

            logger.logKnowledge("query", "execute_insert", "query: %s, param:%s" % (query, param))
            cursor.nextset()
            no = int(cursor.lastrowid)
            if no == 0 :
                return False
            else :
                return no
        except Exception, e:
            logger.logKnowledge("error", "execute_insert", "query: %s, param:%s" % (query, param))
            logger.logKnowledge("error", "execute_insert", str(e))
            return False

    ########################################################
    # To execute select query
    # Used to fetch multiple rows
    # select_all: query is string and param is tuple which return result in tuple of tuples
    # select_one: query is string and param is typle which return result in tuple
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
            logger.logKnowledge("query", "select_all", "query: %s, param:%s" % (query, param))
            cursor.nextset()
            res = cursor.fetchall()
            cursor.nextset()
            return res

        except Exception, e:
            logger.logKnowledge("error", "select_all", "query: %s, param:%s" % (query, param))
            logger.logKnowledge("error", "select_all", str(e))
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
            logger.logKnowledge("query", "select_one", "query: %s, param:%s" % (query, param))
            cursor.nextset()
            res = cursor.fetchone()
            cursor.nextset()
            return res

        except Exception, e:
            logger.logKnowledge("error", "select_one", "query: %s, param:%s" % (query, param))
            logger.logKnowledge("error", "select_one", str(e))
            raise fetch_error()

    ########################################################
    # To form a select query
    # params: table_name, list of columns and where condition
    # returns result in list of dictionary
    ########################################################
    def get_data(
        self, table, columns, condition, condition_val=None, order=None
    ):
        assert type(columns) in (list, str)
        param = []
        rows = []
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
            if condition_val is None:
                rows = self.select_all(query)
            else:
                rows = self.select_all(query, condition_val)

        else:
            if order is not None:
                query += order
            rows = self.select_all(query)

        return rows

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

        if where_condition_val is not None:
            rows = self.select_all(query, where_condition_val)
        else:
            rows = self.select_all(query)

        return rows

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
            print n_id
            logger.logKnowledge("query", "insert", "query: %s, param:%s" % (query, values))
            return n_id
            if n_id == 0 :
                return False
        except Exception, e:
            print e
            logger.logKnowledge("error", "insert", "query: %s, param:%s" % (query, values))
            logger.logKnowledge("error", "insert", str(e))
            raise fetch_error()

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
            logger.logKnowledge("query", "bulk_insert", "query: %s, param:%s" % (query, valueList))
            cursor.nextset()
            return True
        except Exception, e:
            logger.logKnowledge("error", "bulk_insert", "query: %s, param:%s" % (query, valueList))
            logger.logKnowledge("error", "bulk_insert", str(e))
            raise fetch_error()

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
                            query += column+" = '%s' " % (
                                values[outer_index][index])
                query += " WHERE " + cond + "; "
                cursor = self.cursor()
                assert cursor is not None
                cursor.execute(query)
                logger.logKnowledge("query", "bulk_update", "query: %s, param:%s" % (query, values))
                cursor.nextset()
            return True
        except Exception, e:
            logger.logKnowledge("error", "bulk_update", "query: %s, param:%s" % (query, values))
            logger.logKnowledge("error", "bulk_update", str(e))
            raise fetch_error()

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
        try:
            status = self.execute(query, values)
            logger.logKnowledge("query", "update", "query: %s, param:%s" % (query, values))

            return status
        except Exception, e:
            print e
            logger.logKnowledge("error", "update", "query: %s, param:%s" % (query, values))
            logger.logKnowledge("error", "update", str(e))
            raise fetch_error()

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
        except Exception, e:
            logger.logKnowledge("error", "delete", "query: %s, param:%s" % (query, condition_val))
            logger.logKnowledge("error", "delete", str(e))
            raise fetch_error()

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
        except Exception, e:
            logger.logKnowledge("error", "append", "table: %s, column:%s, value:%s" % (table, column, value))
            logger.logKnowledge("error", "append", str(e))
            raise fetch_error()

    ########################################################
    # To increment value in the specified column by the
    # passed value. This function can be used only for int,
    # float, double values
    ########################################################

    def increment(self, table, column, condition, value=1, condition_val=None):
        rows = self.get_data(table, column, condition, condition_val)
        currentValue = int(rows[column[0]][column[0]]) if(
            rows[column[0]][column[0]] is not None) else 0
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
        query = "SELECT count(0) as count FROM %s WHERE %s " % (table, condition)
        rows = None
        rows = self.select_one(query, condition_val)
        if rows:
            if rows["count"] > 0:
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
        query = "SELECT max(%s) as maxid from %s " % (field, table_name)
        row = self.select_one(query)
        if row["maxid"] is not None:
            new_id = int(row["maxid"]) + 1
        return new_id

    def save_activity(self, user_id, form_id, action):
        # created_on = get_date_time()
        # q = "select user_category_id from tbl_user_login_details where user_id = %s"
        # row = self.select_one(q, [user_id])
        # user_cat_id = row.get("user_category_id")

        # query = " INSERT INTO tbl_activity_log " + \
        #     " (user_category_id, user_id, form_id, action, created_on) " + \
        #     " VALUES (%s, %s, %s, %s, %s) "
        # self.execute(query, (
        #         user_cat_id, user_id, form_id, action, created_on
        # ))
        return True

    def validate_session_token(self, session_token):
        query = "SELECT t01.user_id FROM tbl_user_sessions t01 " + \
            " inner JOIN tbl_user_login_details t02 ON t01.user_id = t02.user_id " + \
            " and is_active = 1 " + \
            " WHERE  session_token=%s"
        param = [session_token]
        row = self.select_one(query, param)
        user_id = None
        if row:
            user_id = row["user_id"]
            self.update_session_time(session_token)
        return user_id

    def update_session_time(self, session_token):
        q = "update tbl_user_sessions set last_accessed_time = current_ist_datetime() " + \
            "where session_token = %s "
        # q = '''
        #     update tbl_user_sessions set last_accessed_time = now()
        #     where session_token = %s'''
        self.execute(q, [str(session_token)])

    def clear_session(self, session_cutouff):
        q = "delete from tbl_user_sessions where " + \
            " last_accessed_time < DATE_SUB(current_ist_datetime(),INTERVAL %s MINUTE)"
        self.execute(q, [session_cutouff])

    def reconnect(self):
        self.close()
        self.connect()

    def call_proc(self, procedure_name, args=None, columns=None):
        # columns no longer need here, so remove argument once removed from the reference place
        # args can be tuple/list e.g, (parm1, parm2)/[param1, param2]
        cursor = self.cursor()
        rows = []
        assert cursor is not None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)

            logger.logKnowledge("query", "call_proc", "procedure: %s, param:%s" % (procedure_name, args))

            cols = cursor.description
            if cols:
                cols = [x[0] for x in cols]
            else:
                cols = []

            for c in cursor.stored_results():
                cols = c.description
                if cols :
                    cols = [x[0] for x in cols]
                else :
                    cols = []
                r = convert_to_dict(c.fetchall(), cols)
                rows.append(r)

            if len(rows) > 0 :
                rows = rows[0]
            cursor.nextset()
        except Exception, e:
            logger.logKnowledge("error", "call_proc", "procedure: %s, param:%s" % (procedure_name, args))
            logger.logKnowledge("error", "call_proc", str(e))
            raise process_procedure_error(procedure_name, args, e)

        return rows

    def call_insert_proc(self, procedure_name, args):
        cursor = self.cursor()
        assert cursor is not None
        new_id = None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)
            logger.logKnowledge("query", "call_insert_proc", "procedure: %s, param:%s" % (procedure_name, args))

            cursor.nextset()
            cursor.execute("SELECT LAST_INSERT_ID() as newid")
            r = cursor.fetchone()
            cursor.nextset()
            new_id = r["newid"]
        except Exception, e:
            logger.logKnowledge("error", "call_insert_proc", "procedure: %s, param:%s" % (procedure_name, args))
            logger.logKnowledge("error", "call_insert_proc", str(e))
            raise process_procedure_error(procedure_name, args, e)

        return new_id

    def call_update_proc(self, procedure_name, args):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)
            logger.logKnowledge("query", "call_update_proc", "procedure: %s, param:%s" % (procedure_name, args))

            cursor.nextset()
        except Exception, e:
            logger.logKnowledge("error", "call_update_proc", "procedure: %s, param:%s" % (procedure_name, args))
            logger.logKnowledge("error", "call_update_proc", str(e))
            raise process_procedure_error(procedure_name, args, e)

        return True

    def call_proc_with_multiresult_set(
        self, procedure_name, args, expected_result_count
    ):
        cursor = self.cursor()
        rows = []
        assert cursor is not None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)

            logger.logKnowledge("query", "call_proc_with_multiresult_set", "procedure: %s, param:%s" % (procedure_name, args))
            rows = []
            for c in cursor.stored_results():
                cols = c.description
                if cols:
                    cols = [x[0] for x in cols]
                else:
                    cols = []
                r = convert_to_dict(c.fetchall(), cols)
                rows.append(r)

        except Exception, e:
            logger.logKnowledge("error", "call_proc_with_multiresult_set", "procedure: %s, param:%s" % (procedure_name, args))
            logger.logKnowledge("error", "call_proc_with_multiresult_set", str(e))

        return rows

    def save_toast_messages(self, user_cat_id, message_head, message_text, link, users_to_notify, session_user):
        created_on = get_date_time()
        m1 = "INSERT INTO tbl_messages (user_category_id, message_heading, message_text, " + \
            "link, created_by, created_on) values (%s, %s, %s, %s, %s, %s)"

        msg_id = self.execute_insert(m1, [
            user_cat_id, message_head, message_text, link, session_user, created_on]
        )
        print "------------------", msg_id
        if msg_id is False or msg_id == 0:
            raise fetch_error()

        m2 = "INSERT INTO tbl_message_users (message_id, user_id) values (%s, %s)"
        for u in users_to_notify :
            self.execute(m2, [msg_id, u])

        return True

    def save_messages_users(self, msg_id, user_ids):
        m2 = "INSERT INTO tbl_message_users (message_id, user_id) values (%s, %s)"
        for u in user_ids:
            self.execute(m2, [msg_id, u])

    ########################################################
    # To Check Forgot Password
    ########################################################
    def verify_username(db, username):
        result = db.call_proc_with_multiresult_set(
           "sp_forgot_password", (username,), 2
        )
        if result[0]:
            return result[1]
        else:
            return 0
