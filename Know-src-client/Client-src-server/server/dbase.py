# from flaskext.mysql import MySQL
import mysql.connector
import logger
import threading
from server.common import (convert_to_dict, get_date_time, get_current_date, encrypt, datetime_to_string_time)
from server.exceptionmessage import fetch_error, process_procedure_error
from server.emailcontroller import EmailHandler

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
            logger.logclient("info", "database connection initiate", "")
            return self._connection
        except Exception, e:
            logger.logclient("error", "database.py-connect", e)


class Database(object):
    def __init__(
        self,
        mysqlConnection
    ):
        self._connection = mysqlConnection
        self._cursor = None
        self._for_client = False
        self.owner_id = None

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

    @classmethod
    def make_connection(self, data):
        try:
            if data is None :
                raise ValueError(str("database connection information is empty"))
            return mysql.connector.connect(
                autocommit=False,
                user=data.db_username,
                password=data.db_password,
                host=data.db_ip.ip_address,
                database=data.db_name,
                port=data.db_ip.port
            )
        except Exception, e:
            raise ValueError(str(e))

    def set_owner_id(self, o_id):
        self.owner_id = o_id

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

    def _db_connect(self, host, username, password, database):
        pass
        # return mysql.connect(host, username, password, database)

    ########################################################
    # To Close database connection
    ########################################################
    def close(self):
        if self._connection is not None :
            # self._cursor.close()
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

            logger.logclient("query", "execute", "query: %s, param:%s" % (query, param))
            cursor.nextset()
            return True
        except Exception, e:
            logger.logclient("error", "execute", "query: %s, param:%s" % (query, param))
            logger.logclient("error", "execute", str(e))
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
            cursor.nextset()
            no = int(cursor.lastrowid)
            logger.logclient("query", "execute_insert", "query: %s, param:%s" % (query, param))

            if no == 0 :
                return False
            else :
                return no
        except Exception, e:
            logger.logclient("error", "execute_insert", "query: %s, param:%s" % (query, param))
            logger.logclient("error", "execute_insert", str(e))
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
            cursor.nextset()
            res = cursor.fetchall()
            cursor.nextset()
            logger.logclient("query", "select_all", "query: %s, param:%s" % (query, param))
            return res
        except Exception, e:
            logger.logclient("error", "select_all", "query: %s, param:%s" % (query, param))
            logger.logclient("error", "select_all", str(e))
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
            cursor.nextset()
            res = cursor.fetchone()
            cursor.nextset()
            logger.logclient("query", "select_one", "query: %s, param:%s" % (query, param))
            return res
        except Exception, e:
            logger.logclient("error", "select_one", "query: %s, param:%s" % (query, param))
            logger.logclient("error", "select_one", str(e))
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
        # result = []
        # if rows:
        #     result = convert_to_dict(rows, param)
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
            logger.logclient("query", "insert", "query: %s, param:%s" % (query, values))
            return n_id
            if n_id == 0 :
                return False
        except Exception, e:
            logger.logclient("error", "insert", "query: %s, param:%s" % (query, values))
            logger.logclient("error", "insert", str(e))
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
            cursor.nextset()
            logger.logclient("query", "bulk_insert", "query: %s, param:%s" % (query, valueList))
            return True
        except Exception, e:
            logger.logclient("error", "bulk_insert", "query: %s, param:%s" % (query, valueList))
            logger.logclient("error", "bulk_insert", str(e))
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
                            query += column+" = '%s' " % (
                                values[outer_index][index])
                query += " WHERE " + cond + "; "
                cursor = self.cursor()
                assert cursor is not None
                cursor.execute(query)
                cursor.nextset()
                logger.logclient("query", "bulk_update", "query: %s, param:%s" % (query, values))
            return True
        except Exception, e:
            logger.logclient("error", "bulk_update", "query: %s, param:%s" % (query, values))
            logger.logclient("error", "bulk_update", str(e))
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
        try:
            status = self.execute(query, values)
            logger.logclient("query", "update", "query: %s, param:%s" % (query, values))
            return status
        except Exception, e:
            logger.logclient("error", "update", "query: %s, param:%s" % (query, values))
            logger.logclient("error", "update", str(e))
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
        except Exception, e:
            logger.logclient("error", "delete", "query: %s, param:%s" % (query, condition_val))
            logger.logclient("error", "delete", str(e))
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
        except Exception, e:
            logger.logclient("error", "append", "table: %s, column:%s, value:%s" % (table, column, value))
            logger.logclient("error", "append", str(e))
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

    def save_activity(
        self, user_id, form_id, action, legal_entity_id=None, unit_id=None,
    ):  
        if len(action) > 500:
            action = action[0:500]
            
        created_on = get_date_time()
        # if legal_entity_id is None :
        #     legal_entity_id = ''
        # if unit_id is None :
        #     unit_id = ''
        tblUsers = "tbl_users"
        column = ["user_category_id, client_id"]
        condition_val = "user_id= %s" % user_id
        rows = self.get_data(tblUsers, column, condition_val)
        client_id = rows[0]["client_id"]
        category_id = rows[0]["user_category_id"]
        query = " INSERT INTO tbl_activity_log " + \
            " (client_id, legal_entity_id, unit_id, user_category_id, " + \
            " user_id, form_id, action, created_on) " + \
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
        values = [
            client_id, legal_entity_id, unit_id, category_id,
            user_id, form_id, action, created_on
        ]
        self.execute(query, values)

        return True

    def validate_session_token(self, session_token):
        query = "SELECT t01.user_id, t02.user_category_id FROM tbl_user_sessions t01 " + \
            " LEFT JOIN tbl_user_login_details t02 ON t01.user_id = t02.user_id " + \
            " and is_active = 1 " + \
            " WHERE  session_token=%s"
        param = [session_token]
        row = self.select_one(query, param)
        user_id = None
        user_cat_id = None
        if row:
            user_id = row["user_id"]
            user_cat_id = row["user_category_id"]
            self.update_session_time(session_token)
        return user_id, user_cat_id

    def validate_user_rights(self, session_token, rcaller_name, is_mobile):
        if is_mobile is True:
            user_id, user_category_id = self.validate_session_token(session_token)
            return user_id, user_category_id

        caller_name = [str(x) for x in rcaller_name.split("/") if x != ""]
        caller_name = "/%s" % (caller_name[0])
        try :
            user_id, user_category_id = self.validate_session_token(session_token)
            if user_id is not None :
                if user_category_id == 1 :
                    q = "select t2.form_url from tbl_form_category as t1 " + \
                        " inner join tbl_forms as t2 on t1.form_id = t2.form_id where " + \
                        " t1.user_category_id = 1 " + \
                        " and t2.form_url = %s "
                    param = [caller_name]
                else :
                    q = "select t3.form_url " + \
                        " from tbl_users as t1 " + \
                        " inner join tbl_user_group_forms as t2 on t1.user_group_id = t2.user_group_id " + \
                        " inner join tbl_forms as t3 on t2.form_id = t3.form_id " + \
                        " where t1.user_id = %s and t3.form_url = %s"
                    param = [user_id, caller_name]

                if caller_name not in (
                    "/welcome", "/home", "/profile", "/themes", "/reminders", "/escalations",
                    "/message", "/notifications", "/view-profile", "/settings"
                ) :
                    rows = self.select_one(q, param)
                    if rows :
                        if rows.get("form_url") == caller_name :
                            return user_id, user_category_id
                    else :
                        return None, None
                else :
                    return user_id, user_category_id
            else :
                return user_id, user_category_id

        except Exception, e :
            logger.logclient("error", "validate_rights", str(e))
            raise fetch_error()

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
            logger.logclient("query", "call_proc", "procedure: %s, param:%s" % (procedure_name, args))

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

            # rows = list(cursor.fetchall())
            # rows = convert_to_dict(cursor.fetchall(), cols)
            if len(rows) > 0 :
                rows = rows[0]
            cursor.nextset()
        except Exception, e:
            logger.logclient("error", "call_proc", "procedure: %s, param:%s" % (procedure_name, args))
            logger.logclient("error", "call_proc", str(e))
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
            logger.logclient("query", "call_insert_proc", "procedure: %s, param:%s" % (procedure_name, args))

            cursor.nextset()
            cursor.execute("SELECT LAST_INSERT_ID() as newid")
            r = cursor.fetchone()
            cursor.nextset()
            new_id = r["newid"]
        except Exception, e:
            logger.logclient("error", "call_insert_proc", "procedure: %s, param:%s" % (procedure_name, args))
            logger.logclient("error", "call_insert_proc", str(e))
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
            logger.logclient("query", "call_update_proc", "procedure: %s, param:%s" % (procedure_name, args))

            cursor.nextset()
        except Exception, e:
            logger.logclient("error", "call_update_proc", "procedure: %s, param:%s" % (procedure_name, args))
            logger.logclient("error", "call_update_proc", str(e))
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

            logger.logclient("query", "call_proc_with_multiresult_set", "procedure: %s, param:%s" % (procedure_name, args))
            rows = []
            for c in cursor.stored_results():
                cols = c.description
                if cols :
                    cols = [x[0] for x in cols]
                else :
                    cols = []
                r = convert_to_dict(c.fetchall(), cols)
                rows.append(r)

        except Exception, e:
            logger.logclient("error", "call_proc_with_multiresult_set", "procedure: %s, param:%s" % (procedure_name, args))
            logger.logclient("error", "call_proc_with_multiresult_set", str(e))
        return rows

    def save_messages_users(self, msg_id, user_ids):
        m2 = "INSERT INTO tbl_message_users (message_id, user_id) values (%s, %s)"
        for u in user_ids :
            self.execute(m2 , [msg_id, u])

    ##########################################################
    #  verify password
    ##########################################################

    def verify_password(db, user_id, password):
        ec_password = encrypt(password)
        q = "SELECT username from tbl_user_login_details where user_id = %s and password = %s"
        data_list = db.select_one(q, [user_id, ec_password])
        if data_list is None:
            return False
        else:
            return True

    def save_notification_users(self, notification_id, user_id):
        if user_id is not "NULL" and user_id is not None  :
            q = "INSERT INTO tbl_notifications_user_log(notification_id, user_id) " + \
                " VALUES (%s, %s) "
            v = (notification_id, user_id)
            self.execute(q, v)

    def save_in_notification(
        self, country_id, domain_id, business_group_id, legal_entity_id, division_id,
        unit_id, compliance_id, assignee, concurrence_person, approval_person,
        notification_text, extra_details, notification_type_id, notify_to_all=True
    ):
        def save_notification_users(notification_id, user_id):
            if user_id is not "NULL" and user_id is not None :
                q = "INSERT INTO tbl_notifications_user_log(notification_id, user_id) " + \
                    " VALUES (%s, %s) "
                v = (notification_id, user_id)
                self.execute(q, v)

        # notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
        created_on = get_current_date()
        column = [
                "country_id", "domain_id",
                "legal_entity_id", "unit_id", "compliance_id",
                "assignee", "approval_person", "notification_type_id",
                "notification_text", "extra_details", "created_on"
            ]
        values = [
            country_id, domain_id,
            legal_entity_id, unit_id, compliance_id,
            assignee, approval_person, notification_type_id,
            notification_text, extra_details, created_on
        ]
        if business_group_id is not None :
            column.append("business_group_id")
            values.append(business_group_id)
        if division_id is not None :
            column.append("division_id")
            values.append(division_id)
        if concurrence_person is not None :
            column.append("concurrence_person")
            values.append(concurrence_person)

        notification_id = self.insert("tbl_notifications_log", column, values)
        save_notification_users(notification_id, assignee)
        if notify_to_all:
            if approval_person is not None and assignee != approval_person :
                save_notification_users(notification_id, approval_person)
            if concurrence_person is not None or concurrence_person is not "NULL" :
                save_notification_users(notification_id, concurrence_person)

    def get_onoccurance_compliance_to_notify(self):
        q = "SELECT ch.compliance_history_id,ch.compliance_id,com.compliance_task,com.document_name,ch.unit_id, " + \
            " ch.start_date,ch.due_date, IF(TIMESTAMPDIFF(HOUR, " + \
            "DATE_FORMAT((DATE_SUB(ch.due_date,INTERVAL (TIMESTAMPDIFF(SECOND,ch.start_date,ch.due_date) / 2) SECOND)),'%Y-%m-%d %H:%i'),due_date) <= 24, " + \
            " IF(TIMESTAMPDIFF(SECOND, " + \
            "     DATE_FORMAT((DATE_SUB(ch.due_date, " + \
            "                 INTERVAL (TIMESTAMPDIFF(SECOND, " + \
            "                     ch.start_date, " + \
            "                     ch.due_date) / 2) SECOND)), " + \
            "             '%Y-%m-%d %H:%i'), " + \
            "     due_date) <= 60, " + \
            " CONCAT(TIMESTAMPDIFF(SECOND, " + \
            "             DATE_FORMAT((DATE_SUB(ch.due_date, " + \
            "                         INTERVAL (TIMESTAMPDIFF(SECOND, " + \
            "                             ch.start_date, " + \
            "                             ch.due_date) / 2) SECOND)), " + \
            "                     '%Y-%m-%d %H:%i'), " + \
            "             due_date), " + \
            "         ' seconds'), " + \
            " CONCAT(TIMESTAMPDIFF(HOUR, " + \
            "             DATE_FORMAT((DATE_SUB(ch.due_date, " + \
            "                         INTERVAL (TIMESTAMPDIFF(SECOND, " + \
            "                             ch.start_date, " + \
            " ch.due_date) / 2) SECOND)), " + \
            "                    '%Y-%m-%d %H:%i'), " + \
            "             due_date), " + \
            "         ' hours')), " + \
            " CONCAT(TIMESTAMPDIFF(DAY, " + \
            "             DATE_FORMAT((DATE_SUB(ch.due_date, " + \
            "                         INTERVAL (TIMESTAMPDIFF(SECOND, " + \
            "                             ch.start_date, " + \
            "                             ch.due_date) / 2) SECOND)), " + \
            "                     '%Y-%m-%d %H:%i'), " + \
            "             due_date), " + \
            "         ' days')) AS hours_left, " + \
            "usr.email_id, usr.employee_code, usr.employee_name, u.country_id, " + \
            " com.domain_id, u.business_group_id, u.legal_entity_id, u.division_id, u.unit_code, " + \
            " u.unit_name,ch.completed_by,ch.concurred_by,ch.approved_by " + \
            " FROM " + \
            "     tbl_compliance_history ch " + \
            "         INNER JOIN " + \
            "     tbl_compliances AS com ON ch.compliance_id = com.compliance_id " + \
            "         INNER JOIN " + \
            "     tbl_users AS usr ON ch.completed_by = usr.user_id " + \
            "         INNER JOIN " + \
            "     tbl_units AS u ON ch.unit_id = u.unit_id " + \
            " WHERE " + \
            "     com.frequency_id = 5 " + \
            "         AND ch.current_status < 3 " + \
            "         AND DATE_FORMAT((DATE_SUB(ch.due_date, " + \
            "                 INTERVAL (TIMESTAMPDIFF(SECOND, " + \
            "                     ch.start_date, " + \
            "                     ch.due_date) / 2) SECOND)), " + \
            "             '%Y-%m-%d %H:%i') >= DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP, '+00:00', '+05:15'), " + \
            "             '%Y-%m-%d %H:%i') " + \
            "         AND DATE_FORMAT((DATE_SUB(ch.due_date, " + \
            "                 INTERVAL (TIMESTAMPDIFF(SECOND, " + \
            "                     ch.start_date, " + \
            "                     ch.due_date) / 2) SECOND)), " + \
            "             '%Y-%m-%d %H:%i') <= DATE_FORMAT(CONVERT_TZ(UTC_TIMESTAMP, '+00:00', '+05:30'), " + \
            "             '%Y-%m-%d %H:%i')"

        email = EmailHandler()

        rows = self.select_all(q)

        for r in rows :

            country_id = r["country_id"]
            domain_id = r["domain_id"]
            ch_id = r["compliance_history_id"]
            comp_id = r["compliance_id"]
            c_task = r["compliance_task"]
            doc_name = r["document_name"]
            cname = c_task
            if doc_name is not None :
                cname = "%s - %s" % (doc_name, c_task)
            unit_id = r["unit_id"]
            due_date = r["due_date"]
            left = r["hours_left"]
            email_id = r["email_id"]
            emp_name = r["employee_name"]
            emp_code = r["employee_code"]
            if emp_code is not None :
                name = "%s - %s" % (emp_code, emp_name)
            else :
                name = emp_name
            assignee = r["completed_by"]
            concurr = r["concurred_by"]
            approver = r["approved_by"]
            bg_id = r["business_group_id"]
            div_id = r["division_id"]
            le_id = r["legal_entity_id"]
            unit_name = "%s - %s" % (r["unit_code"], r["unit_name"])

            notification_text = "%s left to complete %s task on due date %s" % (left, cname, datetime_to_string_time(due_date))
            extra_details = " %s - Reminder" % (ch_id)
            self.save_in_notification(
                country_id, domain_id, bg_id, le_id, div_id, unit_id, comp_id, assignee,
                concurr, approver, notification_text, extra_details, 2

            )
            email.notify_occurrence_to_assignee

            notify_occur_compliance = threading.Thread(
                target=email.notify_occurrence_to_assignee,
                args=[
                    name, left, cname, unit_name,
                    email_id
                ]
            )
            notify_occur_compliance.start()
