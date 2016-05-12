import threading
import os
import MySQLdb as mysql
import hashlib
import string
import random
import datetime
import uuid
import json
import pytz
import logger
from types import *
from protocol import (
    core, knowledgereport, technomasters,
    technotransactions, technoreports, general
)
from distribution.protocol import (
    Company, IPAddress
)
from replication.protocol import Change
from server.emailcontroller import EmailHandler as email


__all__ = [
    "KnowledgeDatabase", "Database"
]

ROOT_PATH = os.path.join(os.path.split(__file__)[0])
KNOWLEDGE_FORMAT_PATH = os.path.join(ROOT_PATH, "knowledgeformat")
FORMAT_DOWNLOAD_URL = "compliance_format"
CLIENT_LOGO_PATH = os.path.join(ROOT_PATH, "clientlogo")
LOGO_URL = "knowledge/clientlogo"
LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")

class Database(object) :
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

    # Used to get the integer value of a month by first 3 letters
    integer_months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

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
        except Exception, e :
            logger.logKnowledge("error", "database.py-connect", e)

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
    # To execute select query
    # Used to fetch multiple rows
    ########################################################
    def select_all(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception, e:
            logger.logClientApi("select_all", query)
            logger.logClientApi("select_all", e)
            return

    ########################################################
    # To execute select query
    # Used to fetch One row
    ########################################################
    def select_one(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    ########################################################
    # To execute a query
    ########################################################
    def execute(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        return cursor.execute(query)

    ########################################################
    # To execute a procedure
    ########################################################
    def call_proc(self, procedure_name, args):
        # args is tuple e.g, (parm1, parm2)
        cursor = self.cursor()
        assert cursor is not None
        cursor.callproc(procedure_name, args)
        result = cursor.fetchall()
        return result

    ########################################################
    # To form a select query
    ########################################################
    def get_data(
        self, table, columns, condition
    ):
        query = "SELECT %s FROM %s " % (columns, table)
        if condition is not None :
            query += " WHERE %s" % (condition)
        return self.select_all(query)

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
        columns = ",".join(columns)
        stringValue = ""
        for index, value in enumerate(values):
            if(index < len(values)-1):
                stringValue = stringValue+"'"+str(value)+"',"
            else:
                stringValue = stringValue+"'"+str(value)+"'"
        query = "INSERT INTO %s (%s) VALUES (%s)" % (
            table, columns, stringValue
        )
        try:
            return self.execute(query)
        except Exception, e:
            logger.logKnowledgeApi("insert", query)
            logger.logKnowledgeApi("insert", e)
            return


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
                query += column+" = '"+str(values[index])+"', "
            else:
                query += column+" = '"+str(values[index])+"' "
        query += " WHERE "+condition
        print query
        try:
            return self.execute(query)
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
    def increment(self, table, column, condition, value = 1):
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

    ########################################################
    # To check generate a random string with alpahbets
    # and numbers
    ########################################################
    def generate_random(self):
        characters = string.ascii_uppercase + string.digits
        return ''.join(
            random.SystemRandom().choice(characters) for _ in range(7)
        )

    ########################################################
    # To generate random password encrypted with md5
    # algorithm. This function return encrypted password
    ########################################################
    def generate_password(self) :
        password = self.generate_random()
        return self.encrypt(password)

    ########################################################
    # To generate random password encrypted with md5
    # algorithm. This function return encrypted password and
    # Original password
    ########################################################
    def generate_and_return_password(self):
        password = self.generate_random()
        return self.encrypt(password), password

    ########################################################
    # Encrypts the passed argument with md5 algorithm and
    # returns the encrypted value
    ########################################################
    def encrypt(self, value):
        m = hashlib.md5()
        m.update(value)
        return m.hexdigest()

    ########################################################
    # Converts the passed date in string format to localized
    # datetime format (Time zone is India)
    ########################################################
    def string_to_datetime(self, string):
        string_in_date = string
        if string is not None:
            string_in_date = datetime.datetime.strptime(string, "%d-%b-%Y")
        return self.localize(string_in_date)

    ########################################################
    # Coverts datetime passed in string format to datetime
    # format
    ########################################################
    def string_to_datetime_with_time(self, string):
        string_in_date = string
        if string is not None:
            string_in_date = datetime.datetime.strptime(string, "%d-%b-%Y %H:%M")
        return string_in_date

    ########################################################
    # Converts the given timestamp to UTC
    ########################################################
    def toUTC(self, time_stamp):
        tz = pytz.timezone('UTC')
        utc_time_stamp = tz.normalize(
            tz.localize(time_stamp)
        ).astimezone(pytz.utc)
        return utc_time_stamp

    ########################################################
    # Localizes the given timestamp (Local Timezone is India)
    ########################################################
    def localize(self, time_stamp):
        local_dt = LOCAL_TIMEZONE.localize(
            time_stamp
        )
        tzoffseet = local_dt.utcoffset()
        local_dt = local_dt.replace(tzinfo=None)
        local_dt = local_dt+tzoffseet
        return local_dt

    ########################################################
    # Converts given datetime value to string (DATE format)
    ########################################################
    def datetime_to_string(self, datetime_val):
        date_in_string = datetime_val
        if datetime_val is not None:
            date_in_string = datetime_val.strftime("%d-%b-%Y")
        return date_in_string

    ########################################################
    # converts given datetime val to string (DATETIME format)
    ########################################################
    def datetime_to_string_time(self, datetime_val):
        datetime_in_string = datetime_val
        if datetime_val is not None:
            datetime_in_string = datetime_val.strftime("%d-%b-%Y %H:%M")
        return datetime_in_string

    ########################################################
    # Returns the database information of clients
    # If client id is given, client specific info will be
    # returned
    # Other wise Info of all clients will be returned
    ########################################################
    def get_client_db_info(self, client_id=None):
        columns = "database_ip, client_id, "
        columns += " database_username, database_password, database_name"
        condition = "1"
        if client_id is not None:
            condition = "client_id = '%d'" % client_id
        return self.get_data("tbl_client_database", columns, condition)

    ########################################################
    # To generate a new Id for the given table and given
    # field
    ########################################################
    def get_new_id(self, field , table_name, client_id=None) :
        newId = 1
        query = "SELECT max(%s) from %s " % (field, table_name)
        row = None
        row = self.select_one(query)
        if row[0] is not None :
            newId = int(row[0]) + 1
        return newId

    ########################################################
    # Returns current date and time localized to Indian time
    ########################################################
    def get_date_time(self) :
        time_stamp = datetime.datetime.utcnow()
        return self.localize(time_stamp)

    ########################################################
    # To Check Login credentials
    ########################################################
    def verify_login(self, username, password):
        tblAdminCondition = "password='%s' and username='%s'" % (
            password, username
        )
        admin_details = self.get_data("tbl_admin", "*", tblAdminCondition)

        if (len(admin_details) == 0) :
            data_columns = [
                "user_id", "user_group_id", "email_id",
                "employee_name", "employee_code",
                "contact_no", "address",
                "designation", "user_group_name", "form_ids"
            ]
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, \
                t1.address, t1.designation, \
                t2.user_group_name, t2.form_ids \
                FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
                ON t1.user_group_id = t2.user_group_id \
                WHERE t1.password='%s' and t1.email_id='%s' and t1.is_active=1" % (
                    password, username
                )
            data_list = self.select_one(query)
            if data_list is None :
                return False
            else :
                return self.convert_to_dict(data_list, data_columns)
        else :
            return True

    ########################################################
    # Convert the given data to a dictionary format with
    # columns as keys
    ########################################################
    def convert_to_dict(self, data_list, columns) :
        if data_list is None :
            return []
        assert type(data_list) in (list, tuple)
        if len(data_list) > 0:
            if type(data_list[0]) is tuple :
                result_list = []
                if len(data_list[0]) == len(columns) :
                    for data in data_list:
                        result = {}
                        for i, d in enumerate(data):
                            result[columns[i]] = d
                        result_list.append(result)
                return result_list
            else :
                result = {}
                if len(data_list) == len(columns) :
                    for i, d in enumerate(data_list):
                        result[columns[i]] = d
                return result
        else:
            return []

    ########################################################
    # Adds User session
    ########################################################
    def add_session(
        self, user_id, session_type_id, ip,
        employee, client_id=None
    ) :
        if client_id is not None:
            self.clear_old_session(user_id, session_type_id, client_id)
        else:
            self.clear_old_session(user_id, session_type_id)
        session_id = self.new_uuid()
        if client_id is not None:
            session_id = "%s-%s" % (client_id, session_id)
        updated_on = self.get_date_time()
        query = "INSERT INTO tbl_user_sessions \
            (session_token, user_id, session_type_id, last_accessed_time) \
            VALUES ('%s', %s, %s, '%s');"
        query = query % (session_id, user_id, session_type_id, updated_on)
        self.execute(query)

        action = "Log In by - \"%s\" from \"%s\"" % ( employee, ip)
        self.save_activity(user_id, 0, action)

        return session_id

    ########################################################
    # To save User login history
    ########################################################
    def save_user_login_history(self, user_id):
        updated_on = self.get_date_time()
        query = "INSERT INTO tbl_user_login_history \
            (user_id, login_time) \
            VALUES ('%s', '%s');"
        query = query % (user_id, updated_on)
        self.execute(query)

    ########################################################
    # To clear user session
    ########################################################
    def clear_old_session(self, user_id, session_type_id, client_id=None) :
        query = "DELETE FROM tbl_user_sessions \
            WHERE user_id=%s and session_type_id=%s" % (
                user_id, session_type_id
            )

        self.execute(query)

    ########################################################
    # Creates and returns random key with (32 characters)
    ########################################################
    def new_uuid(self) :
        s = str(uuid.uuid4())
        return s.replace("-", "")

    ########################################################
    # Check whether the given reset token is valid
    ########################################################
    def validate_reset_token(self, reset_token):
        column = "count(*), user_id"
        condition = " verification_code='%s'" % reset_token
        rows = self.get_data(self.tblEmailVerification, column, condition)
        count = rows[0][0]
        user_id = rows[0][1]
        if count == 1:
            column = "count(*)"
            condition = "user_id = '%d' and is_active = 1" % user_id
            rows = self.get_data(self.tblUsers, column, condition)
            if rows[0][0] > 0 or user_id == 0:
                return user_id
            else:
                return None
        else:
            return None

    ########################################################
    # Deletes a reset token, once it is used
    ########################################################
    def delete_used_token(self, reset_token):
        condition = " verification_code='%s'" % reset_token
        if self.delete(self.tblEmailVerification, condition):
            return True
        else:
            return False

class KnowledgeDatabase(Database):
    def __init__(
        self, host, port,
        username, password, database_name
    ):
        super(KnowledgeDatabase, self).__init__(
            host, port, username, password,
            database_name
        )
        self.statutory_parent_mapping = {}
        self.geography_parent_mapping = {}
        self.initialize_table_names()

    def initialize_table_names(self):
        self.tblActivityLog = "tbl_activity_log"
        self.tblAdmin = "tbl_admin"
        self.tblBusinessGroups = "tbl_business_groups"
        self.tblClientConfigurations = "tbl_client_configurations"
        self.tblClientCountries = "tbl_client_countries"
        self.tblClientDatabase = "tbl_client_database"
        self.tblClientDomains = "tbl_client_domains"
        self.tblClientGroups = "tbl_client_groups"
        self.tblClientSavedCompliances = "tbl_client_saved_compliances"
        self.tblClientSavedStatutories = "tbl_client_saved_statutories"
        self.tblClientStatutories = "tbl_client_statutories"
        self.tblClientCompliances = "tbl_client_compliances"
        self.tblClientUsers = "tbl_client_users"
        self.tblComplianceDurationType = "tbl_compliance_duration_type"
        self.tblComplianceFrequency = "tbl_compliance_frequency"
        self.tblComplianceRepeatype = "tbl_compliance_repeat_type"
        self.tblCompliances = "tbl_compliances"
        self.tblCompliancesBackup = "tbl_compliances_backup"
        self.tblCountries = "tbl_countries"
        self.tblDatabaseServer = "tbl_database_server"
        self.tblDivisions = "tbl_divisions"
        self.tblDomains = "tbl_domains"
        self.tblEmailVerification = "tbl_email_verification"
        self.tblFormCategory = "tbl_form_category"
        self.tblFormType = "tbl_form_type"
        self.tblForms = "tbl_forms"
        self.tblGeographies = "tbl_geographies"
        self.tblGeographyLevels = "tbl_geography_levels"
        self.tblIndustries = "tbl_industries"
        self.tblLegalEntities = "tbl_legal_entities"
        self.tblMachines = "tbl_machines"
        self.tblMobileRegistration = "tbl_mobile_registration"
        self.tblNotifications = "tbl_notifications"
        self.tblNotificationsStatus = "tbl_notifications_status"
        self.tblSessionTypes = "tbl_session_types"
        self.tblStatutories = "tbl_statutories"
        self.tblStatutoriesBackup = "tbl_statutories_backup"
        self.tblStatutoryGeographies = "tbl_statutory_geographies"
        self.tblStatutoryLevels = "tbl_statutory_levels"
        self.tblStatutoryMappings = "tbl_statutory_mappings"
        self.tblStatutoryNatures = "tbl_statutory_natures"
        self.tblStatutoryNotificationsLog = "tbl_statutory_notifications_log"
        self.tblStatutoryNotificationsUnits = "tbl_statutory_notifications_units"
        self.tblUnits = "tbl_units"
        self.tblUserClients = "tbl_user_clients"
        self.tblUserCountries = "tbl_user_countries"
        self.tblUserDomains = "tbl_user_domains"
        self.tblUserGroups = "tbl_user_groups"
        self.tblUserLoginHistory = "tbl_user_login_history"
        self.tblUserSessions = "tbl_user_sessions"
        self.tblUsers = "tbl_users"

    def validate_short_name(self, short_name):
        condition = "url_short_name ='%s'" % (
            short_name
        )
        return self.is_already_exists(self.tblClientGroups, condition)

    def validate_session_token(self, session_token) :
        # query = "CALL sp_validate_session_token ('%s');"
        # % (session_token)
        query = "SELECT user_id FROM tbl_user_sessions \
            WHERE session_token = '%s'" % (session_token)
        row = self.select_one(query)
        user_id = None
        if row :
            user_id = row[0]
        return user_id

    def get_user_form_ids(self, user_id) :
        if user_id == 0 :
            return "1, 2, 3, 4"
        q = "select t1.form_ids from tbl_user_groups t1 \
            INNER JOIN tbl_users t2 on t1.user_group_id = t2.user_group_id \
            AND t2.user_id = %s" % (user_id)
        row = self.select_one(q)
        if row :
            return row[0]
        else :
            return None

    def encrypt(self, value):
        m = hashlib.md5()
        m.update(value)
        return m.hexdigest()

    def save_activity(self, user_id, form_id, action):
        created_on = self.get_date_time()
        activityId = self.get_new_id("activity_log_id", "tbl_activity_log")
        query = "INSERT INTO tbl_activity_log \
            (activity_log_id, user_id, form_id, action, created_on) \
            VALUES (%s, %s, %s, '%s', '%s')" % (
                activityId, user_id, form_id, action, created_on
            )
        self.execute(query)
        return True

    #
    # Companies
    #

    def get_trail_id(self):
        query = "select IFNULL(MAX(audit_trail_id), 0) as audit_trail_id from tbl_audit_log;"
        row = self.select_one(query)
        trail_id = row[0]
        return trail_id

    def get_trail_log(self, client_id, received_count):
        query = "SELECT "
        query += "  audit_trail_id, tbl_name, tbl_auto_id,"
        query += "  column_name, value, client_id, action"
        query += " from tbl_audit_log WHERE audit_trail_id>%s AND (client_id = 0 OR client_id=%s) LIMIT 100;" % (
            received_count, client_id
        )
        rows = self.select_all(query)
        results = []
        if rows :
            columns = [
                "audit_trail_id", "tbl_name", "tbl_auto_id",
                "column_name", "value", "client_id", "action"
            ]
            results = self.convert_to_dict(rows, columns)
        return self.return_changes(results)

    def return_changes(self, data):
        results = []
        for d in data :
            change = Change(
                int(d["audit_trail_id"]),
                d["tbl_name"],
                int(d["tbl_auto_id"]),
                d["column_name"],
                d["value"],
                int(d["client_id"]),
                d["action"]
            )
            results.append(change)
        return results

    def get_servers(self):
        query = "SELECT client_id, machine_id, database_ip, "
        query += "database_port, database_username, "
        query += "database_password, client_short_name, "
        query += "database_name, server_ip, server_port "
        query += "FROM tbl_client_database"
        rows = self.select_all(query)
        results = []
        if rows :
            columns = [
                "client_id", "machine_id", "database_ip",
                "database_port", "database_username",
                "database_password", "client_short_name",
                "database_name", "server_ip", "server_port"
            ]
            results = self.convert_to_dict(rows, columns)
        return self.return_companies(results)

    def return_companies(self, data):
        results = []
        for d in data :
            database_ip = IPAddress(
                d["database_ip"],
                int(d["database_port"])
            )
            company_server_ip = IPAddress(
                d["server_ip"],
                int(d["server_port"])
            )
            results.append(Company(
                int(d["client_id"]),
                d["client_short_name"],
                d["database_username"],
                d["database_password"],
                d["database_name"],
                database_ip,
                company_server_ip
            ))
        return results

    #
    # Domain
    #

    def get_domains_for_user(self, user_id) :
        # query = "CALL sp_get_domains_for_user (%s)" % (user_id)
        query = "SELECT distinct t1.domain_id, t1.domain_name, \
            t1.is_active FROM tbl_domains t1 "
        if user_id > 0 :
            query = query + " INNER JOIN tbl_user_domains t2 ON \
                t1.domain_id = t2.domain_id WHERE t2.user_id = %s \
                AND t1.is_active=1 " % (user_id)
        query = query + " ORDER BY t1.domain_name"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["domain_id", "domain_name", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return self.return_domains(result)

    def return_domains(self, data):
        results = []
        for d in data :
            results.append(core.Domain(
                d["domain_id"], d["domain_name"], bool(d["is_active"])
            ))
        return results

    def save_domain(self, domain_name, user_id) :
        created_on = self.get_date_time()
        domain_id = self.get_new_id("domain_id", "tbl_domains")
        is_active = 1

        query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, \
            created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            domain_id, domain_name, is_active, user_id, created_on
        )
        self.execute(query)
        action = "Add Domain - \"%s\"" % domain_name
        self.save_activity(user_id, 2, action)
        return True

    def check_duplicate_domain(self, domain_name, domain_id) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_domains \
            WHERE LOWER(domain_name) = LOWER('%s') " % domain_name
        if domain_id is not None :
            query = query + " AND domain_id != %s" % domain_id
        row = self.select_one(query)
        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def get_domain_by_id(self, domain_id) :
        q = "SELECT domain_name FROM tbl_domains \
            WHERE domain_id=%s" % domain_id
        row = self.select_one(q)
        domain_name = None
        if row :
            domain_name = row[0]
        return domain_name

    def update_domain(self, domain_id, domain_name, updated_by) :
        oldData = self.get_domain_by_id(domain_id)
        if oldData is None :
            return False
        else :
            query = "UPDATE tbl_domains SET domain_name = '%s', \
            updated_by = %s WHERE domain_id = %s" % (
                domain_name, updated_by, domain_id
            )
            self.execute(query)
            action = "Edit Domain - \"%s\"" % domain_name
            self.save_activity(updated_by, 2, action)
            return True

    def check_domain_id_to_deactivate(self, domain_id) :
        q = "SELECT count(*) from tbl_statutory_mappings where domain_id = %s" % (
            domain_id
        )
        row = self.select_one(q)
        if row[0] > 0 :
            return False
        else :
            q = "SELECT count(*) from tbl_client_domains where domain_id = %s " % (
                domain_id
            )
            row = self.select_one(q)
            if row[0] > 0 :
                return False
        return True

    def update_domain_status(self, domain_id, is_active, updated_by) :
        oldData = self.get_domain_by_id(domain_id)
        if oldData is None :
            return False
        else :
            query = "UPDATE tbl_domains SET is_active = %s, \
            updated_by = %s WHERE domain_id = %s" % (
                is_active, updated_by, domain_id
            )
            self.execute(query)
            if is_active == 0 :
                status = "deactivated"
            else:
                status = "activated"
            action = "Domain %s status  - %s" % (oldData, status)
            self.save_activity(updated_by, 2, action)
            return True

    #
    # Country
    #

    def get_countries_for_user(self, user_id) :

        query = "SELECT distinct t1.country_id, t1.country_name, \
            t1.is_active FROM tbl_countries t1 "
        if user_id > 0 :
            query = query + " INNER JOIN tbl_user_countries t2 \
                ON t1.country_id = t2.country_id WHERE t2.user_id = %s \
                AND t1.is_active = 1 " % (
                    user_id
                )
        query = query + " ORDER BY t1.country_name"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["country_id", "country_name", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return self.return_countries(result)

    def return_countries(self, data) :
        results = []

        for d in data :
            results.append(core.Country(
                d["country_id"], d["country_name"], bool(d["is_active"])
            ))
        return results

    def get_country_by_id(self, country_id) :
        q = "SELECT country_name FROM tbl_countries \
            WHERE country_id=%s" % country_id
        row = self.select_one(q)
        country_name = row[0]
        return country_name

    def check_duplicate_country(self, country_name, country_id) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_countries \
        WHERE LOWER(country_name) = LOWER('%s') " % country_name
        if country_id is not None :
            query = query + " AND country_id != %s" % country_id
        row = self.select_one(query)
        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def save_country(self, country_name, created_by) :
        created_on = self.get_date_time()
        country_id = self.get_new_id("country_id", "tbl_countries")
        is_active = 1

        query = "INSERT INTO tbl_countries(country_id, country_name, \
            is_active, created_by, created_on) \
            VALUES (%s, '%s', %s, %s, '%s') " % (
            country_id, country_name, is_active, created_by, created_on
        )
        self.execute(query)
        action = "Add Country - \"%s\"" % country_name
        self.save_activity(created_by, 1, action)
        return True

    def update_country(self, country_id, country_name, updated_by) :
        oldData = self.get_country_by_id(country_id)
        if oldData is None :
            return False
        else :
            query = "UPDATE tbl_countries SET country_name = '%s', \
            updated_by = %s WHERE country_id = %s" % (
                country_name, updated_by, country_id
            )
            self.execute(query)
            action = "Edit Country - \"%s\"" % country_name
            self.save_activity(updated_by, 1, action)
            return True

    def check_country_id_to_deactivate(self, country_id) :
        q = "SELECT count(*) from tbl_statutory_mappings where country_id = %s" % (
            country_id
        )
        row = self.select_one(q)
        if row[0] > 0 :
            return False
        else :
            q = "SELECT count(*) from tbl_client_countries where country_id = %s " % (
                country_id
            )
            row = self.select_one(q)
            if row[0] > 0 :
                return False
        return True


    def update_country_status(self, country_id, is_active, updated_by) :
        oldData = self.get_country_by_id(country_id)
        if oldData is None :
            return False
        else :
            query = "UPDATE tbl_countries SET is_active = %s, \
            updated_by = %s WHERE country_id = %s" % (
                is_active, updated_by, country_id
            )
            if is_active == 0:
                status = "deactivated"
            else:
                status = "activated"
            self.execute(query)
            action = "Country %s status  - %s" % (oldData, status)
            self.save_activity(updated_by, 1, action)
            return True

    def get_user_forms(self, form_ids):

        columns = "tf.form_id, tf.form_category_id, tfc.form_category, \
            tf.form_type_id, tft.form_type,\
            tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = ["tbl_forms", "tbl_form_category", "tbl_form_type"]
        aliases = ["tf", "tfc", "tft"]
        join_conditions = [
            "tf.form_category_id = tfc.form_category_id",
            "tf.form_type_id = tft.form_type_id"
        ]
        where_condition = " tf.form_id in (%s) order by tf.form_order" % (
                form_ids
            )
        join_type = "left join"
        rows = self.get_data_from_multiple_tables(
            columns, tables,
            aliases, join_type,
            join_conditions, where_condition
        )
        row_columns = [
            "form_id", "form_category_id", "form_category",
            "form_type_id", "form_type", "form_name", "form_url",
            "form_order", "parent_menu"
        ]
        result = self.convert_to_dict(rows, row_columns)
        return result

    def get_form_types(self) :
        query = "SELECT form_type_id, form_type_name FROM tbl_form_type"
        rows = self.select_all(query)
        columns = ["form_type_id", "form_type_name"]
        data_list = self.convert_to_dict(rows, columns)
        return data_list

    def save_data(self, table_name, field, data):
        query = "INSERT INTO %s %s VALUES %s" % (
            table_name, field, str(data)
        )
        try :
            self.execute(query)
            return True
        except Exception, e :
            print e

    def update_data(self, table_name, field_with_data, where_condition) :
        query = "UPDATE %s SET %s WHERE %s" % (
            table_name, field_with_data, where_condition
        )
        try :
            self.execute(query)
            return True
        except Exception, e :
            print e

    def get_industries(self) :
        query = "SELECT industry_id, industry_name, is_active \
            FROM tbl_industries ORDER BY industry_name"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["industry_id", "industry_name", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return self.return_industry(result)

    def get_active_industries(self) :
        query = "SELECT industry_id, industry_name, is_active \
            FROM tbl_industries where is_active = 1 ORDER BY industry_name"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["industry_id", "industry_name", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return self.return_industry(result)

    def return_industry(self, data) :
        results = []
        for d in data :
            industry_id = d["industry_id"]
            industry_name = d["industry_name"]
            is_active = bool(d["is_active"])
            results.append(core.Industry(
                industry_id, industry_name, is_active
            ))
        return results

    def get_industry_by_id(self, industry_id) :
        if type(industry_id) is IntType :
            q = "SELECT industry_name FROM tbl_industries \
                WHERE industry_id=%s" % industry_id

        else :
            q = " SELECT (GROUP_CONCAT(industry_name SEPARATOR ', ')) as \
                industry_name FROM tbl_industries \
                WHERE industry_id in %s" % str(tuple(industry_id))

        row = self.select_one(q)
        industry_name = None
        if row :
            industry_name = row[0]
        return industry_name

    def check_duplicate_industry(self, industry_name, industry_id) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_industries \
            WHERE LOWER(industry_name) = LOWER('%s') " % industry_name

        if industry_id is not None :
            query = query + " AND industry_id != %s" % industry_id
        row = self.select_one(query)

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def save_industry(self, industry_name, user_id):
        table_name = "tbl_industries"
        created_on = self.get_date_time()
        industry_id = self.get_new_id("industry_id", table_name)
        field = "(industry_id, industry_name, created_by, \
            created_on)"
        data = (industry_id, industry_name, int(user_id), str(created_on))
        if (self.save_data(table_name, field, data)):
            action = "New Industry type %s added" % (industry_name)
            self.save_activity(user_id, 7, action)
            return True
        return False

    def update_industry(self, industry_id, industry_name, user_id):
        oldData = self.get_industry_by_id(industry_id)
        if oldData is None :
            return False

        table_name = "tbl_industries"
        field_with_data = " industry_name = '%s', updated_by = %s" % (
            industry_name, int(user_id)
        )
        where_condition = "industry_id = %s " % industry_id
        if (self.update_data(table_name, field_with_data, where_condition)) :
            action = "Industry type %s updated" % (industry_name)
            self.save_activity(user_id, 7, action)
            return True
        else :
            return False

    def update_industry_status(self, industry_id, is_active, user_id) :
        oldData = self.get_industry_by_id(industry_id)
        if oldData is None:
            return False

        table_name = "tbl_industries"
        field_with_data = "is_active = %s, updated_by = %s" % (
            is_active, user_id
        )
        where_condition = "industry_id = %s " % industry_id

        if (self.update_data(table_name, field_with_data, where_condition)):
            if is_active == 0:
                status = "deactivated"
            else:
                status = "activated"

            action = "Industry type %s status  - %s" % (oldData, status)
            self.save_activity(user_id, 7, action)
            return True
        else :
            return False

    def get_statutory_nature(self) :
        query = "SELECT statutory_nature_id, statutory_nature_name, \
            is_active FROM tbl_statutory_natures Order By statutory_nature_name"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = [
                "statutory_nature_id",
                "statutory_nature_name", "is_active"
            ]
            result = self.convert_to_dict(rows, columns)
        return self.return_statutory_nature(result)

    def return_statutory_nature(self, data) :
        results = []
        for d in data :
            nature_id = d["statutory_nature_id"]
            nature_name = d["statutory_nature_name"]
            is_active = bool(d["is_active"])
            results.append(core.StatutoryNature(
                nature_id, nature_name, is_active
            ))
        return results

    def get_nature_by_id(self, nature_id) :

        q = "SELECT statutory_nature_name \
            FROM tbl_statutory_natures \
            WHERE statutory_nature_id=%s" % nature_id
        row = self.select_one(q)
        nature_name = None
        if row :
            nature_name = row[0]
        return nature_name

    def check_duplicate_statutory_nature(self, nature_name, nature_id) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_statutory_natures \
            WHERE LOWER(statutory_nature_name) = LOWER('%s') " % nature_name

        if nature_id is not None :
            query = query + " AND statutory_nature_id != %s" % nature_id
        row = self.select_one(query)

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def save_statutory_nature(self, nature_name, user_id) :
        table_name = "tbl_statutory_natures"
        created_on = self.get_date_time()
        nature_id = self.get_new_id("statutory_nature_id", table_name)
        field = "(statutory_nature_id, statutory_nature_name, \
            created_by, created_on)"
        data = (nature_id, nature_name, int(user_id), str(created_on))
        if (self.save_data(table_name, field, data)):
            action = "New Statutory Nature %s added" % (nature_name)
            self.save_activity(user_id, 8, action)
            return True
        return False

    def update_statutory_nature(self, nature_id, nature_name, user_id):
        oldData = self.get_nature_by_id(nature_id)
        if oldData is None :
            return False

        table_name = "tbl_statutory_natures"
        field_with_data = " statutory_nature_name = '%s', updated_by = %s" % (
            nature_name, int(user_id)
        )
        where_condition = "statutory_nature_id = %s " % nature_id
        if (self.update_data(table_name, field_with_data, where_condition)) :
            action = "Statutory Nature %s updated" % (nature_name)
            self.save_activity(user_id, 8, action)
            return True
        else :
            return False

    def update_statutory_nature_status(self, nature_id, is_active, user_id) :
        oldData = self.get_nature_by_id(nature_id)
        if oldData is None:
            return False

        table_name = "tbl_statutory_natures"
        field_with_data = "is_active = %s, updated_by = %s" % (
            int(is_active), int(user_id)
        )
        where_condition = "statutory_nature_id = %s " % (nature_id)

        if (self.update_data(table_name, field_with_data, where_condition)):
            if is_active == 0:
                status = "deactivated"
            else:
                status = "activated"

            action = "Statutory nature %s status  - %s" % (oldData, status)
            self.save_activity(user_id, 8, action)
            return True
        else :
            return False

    def get_statutory_levels(self):
        query = "SELECT level_id, level_position, level_name, country_id, domain_id \
            FROM tbl_statutory_levels ORDER BY level_position"

        rows = self.select_all(query)
        result = []
        if rows :
            columns = [
                "level_id", "level_position",
                "level_name", "country_id", "domain_id"
            ]
            result = self.convert_to_dict(rows, columns)
        return self.return_statutory_levels(result)

    def return_statutory_levels(self, data):
        statutory_levels = {}
        for d in data :
            country_id = d["country_id"]
            domain_id = d["domain_id"]
            levels = core.Level(
                d["level_id"], d["level_position"], d["level_name"]
            )
            country_wise = statutory_levels.get(country_id)
            _list = []
            if country_wise is None :
                country_wise = {}
            else :
                _list = country_wise.get(domain_id)
                if _list is None :
                    _list = []
            _list.append(levels)
            country_wise[domain_id] = _list
            statutory_levels[country_id] = country_wise
        return statutory_levels

    def get_levels_for_country_domain(self, country_id, domain_id) :
        query = "SELECT level_id, level_position, level_name \
            FROM tbl_statutory_levels \
            WHERE country_id = %s and domain_id = %s \
            ORDER BY level_position" % (
                country_id, domain_id
            )
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["level_id", "level_position", "level_name"]
            result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_levels(
        self, country_id, domain_id, levels
    ) :
        saved_names = [
            row["level_name"] for row in self.get_levels_for_country_domain(
                country_id, domain_id
            )
        ]

        for level in levels :
            name = level.level_name
            if level.level_id is None :
                if (saved_names.count(name) > 0) :
                    return name
        return None

    def save_statutory_levels(self, country_id, domain_id, levels, user_id) :

        table_name = "tbl_statutory_levels"
        created_on = self.get_date_time()
        for level in levels :
            name = level.level_name
            position = level.level_position
            if (level.level_id is None) :
                level_id = self.get_new_id("level_id", table_name)
                field = "(level_id, level_position, level_name, \
                    country_id, domain_id, created_by, created_on)"
                data = (
                    int(level_id), position, name, int(country_id),
                    int(domain_id), int(user_id), str(created_on)
                )
                if (self.save_data(table_name, field, data)):
                    action = "New Statutory levels added"
                    self.save_activity(user_id, 9, action)
            else :
                field_with_data = "level_position=%s, \
                    level_name='%s', updated_by=%s" % (
                        position, name, user_id
                    )
                where_condition = "level_id=%s" % (level.level_id)
                if (
                    self. update_data(
                        table_name, field_with_data, where_condition
                    )
                ) :
                    action = "Statutory levels updated"
                    self.save_activity(user_id, 9, action)
        return True

    def get_geography_levels(self):
        query = "SELECT level_id, level_position, level_name, country_id \
            FROM tbl_geography_levels ORDER BY level_position"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = [
                "level_id", "level_position", "level_name", "country_id"
            ]
            result = self.convert_to_dict(rows, columns)
        return self.return_geography_levels(result)

    def return_geography_levels(self, data):
        geography_levels = {}
        for d in data:
            country_id = d["country_id"]
            level = core.Level(
                d["level_id"], d["level_position"], d["level_name"]
            )
            _list = geography_levels.get(country_id)
            if _list is None :
                _list = []
            _list.append(level)
            geography_levels[country_id] = _list
        return geography_levels

    def get_geograhpy_levels_for_user(self, user_id):
        country_ids = None
        if ((user_id is not None) and (user_id != 0)):
            country_ids = self.get_user_countries(user_id)
        columns = "level_id, level_position, level_name, country_id"
        condition = "1"
        if country_ids is not None:
            condition = "country_id in (%s) ORDER BY level_position" % country_ids
        rows = self.get_data(self.tblGeographyLevels, columns, condition)
        result = []
        if rows :
            columns = [
                "level_id", "level_position", "level_name", "country_id"
            ]
            result = self.convert_to_dict(rows, columns)
        return self.return_geography_levels(result)

    def get_geography_levels_for_country(self, country_id) :
        query = "SELECT level_id, level_position, level_name \
            FROM tbl_geography_levels WHERE country_id = %s \
            ORDER BY level_position" % country_id
        rows = self.select_all(query)
        columns = ["level_id", "level_position", "level_name"]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_gepgrahy_levels(self, country_id, levels) :
        saved_names = [
            row["level_name"] for row in self.get_geography_levels_for_country(
                country_id
            )
        ]

        for level in levels :
            name = level.level_name
            if level.level_id is None :
                if (saved_names.count(name) > 0) :
                    return name
        return None

    def save_geography_levels(self, country_id, levels, user_id):
        table_name = "tbl_geography_levels"
        created_on = self.get_date_time()
        for level in levels :
            name = level.level_name
            position = level.level_position
            if level.level_id is None :
                level_id = self.get_new_id("level_id", table_name)
                field = "(level_id, level_position, level_name, \
                    country_id, created_by, created_on)"
                data = (
                    level_id, position, name, int(country_id),
                    int(user_id), str(created_on)
                )
                if (self.save_data(table_name, field, data)):
                    action = "New Geography levels added"
                    self.save_activity(user_id, 5, action)
            else :
                field_with_data = "level_position=%s, level_name='%s', \
                updated_by=%s" % (
                    position, name, int(user_id)
                )
                where_condition = "level_id=%s" % (level.level_id)
                if (
                    self. update_data(
                        table_name, field_with_data, where_condition
                    )
                ):
                    action = "Geography levels updated"
                    self.save_activity(user_id, 5, action)
        return True

    def get_geographies(self, user_id=None, country_id=None) :
        query = "SELECT distinct t1.geography_id, \
            t1.geography_name, \
            t1.level_id, \
            t1.parent_ids, t1.is_active, \
            t2.country_id, \
            (select country_name from tbl_countries where country_id = t2.country_id)as country_name, \
            t2.level_position \
            FROM tbl_geographies t1 \
            INNER JOIN tbl_geography_levels t2 \
            on t1.level_id = t2.level_id \
            INNER JOIN tbl_user_countries t4 \
            ON t2.country_id = t4.country_id"
        if user_id :
            query = query + " AND t4.user_id=%s" % (user_id)
        if country_id :
            query = query + " AND t2.country_id=%s" % (country_id)
        query = query + " ORDER BY country_name, level_position, geography_name"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = [
                "geography_id", "geography_name", "level_id",
                "parent_ids", "is_active", "country_id", "country_name", "level_position"
            ]
            result = self.convert_to_dict(rows, columns)
            self.set_geography_parent_mapping(result)
        return self.return_geographies(result)

    def return_geographies(self, data):
        geographies = {}
        for d in data :
            parent_ids = [int(x) for x in d["parent_ids"][:-1].split(',')]
            geography = core.Geography(
                d["geography_id"], d["geography_name"],
                d["level_id"], parent_ids, parent_ids[-1],
                bool(d["is_active"])
            )
            country_id = d["country_id"]
            _list = geographies.get(country_id)
            if _list is None :
                _list = []
            _list.append(geography)
            geographies[country_id] = _list
        return geographies

    def get_geographies_for_user(self, user_id):
        country_ids = None
        if ((user_id is not None) and (user_id != 0)):
            country_ids = self.get_user_countries(user_id)
        columns = "t1.geography_id, t1.geography_name, "
        columns += "t1.level_id,t1.parent_ids, t1.is_active, "
        columns += "t2.country_id, t3.country_name"
        tables = [
            self.tblGeographies, self.tblGeographyLevels, self.tblCountries
        ]
        aliases = ["t1", "t2", "t3"]
        join_type = " INNER JOIN"
        join_conditions = [
            "t1.level_id = t2.level_id", "t2.country_id = t3.country_id"
        ]
        where_condition = "1"
        if country_ids is not None:
            where_condition = "t2.country_id in (%s)" % country_ids
        rows = self.get_data_from_multiple_tables(
            columns, tables, aliases, join_type,
            join_conditions, where_condition
        )
        result = []
        if rows :
            columns = [
                "geography_id", "geography_name",
                "level_id", "parent_ids", "is_active",
                "country_id", "country_name"
            ]
            result = self.convert_to_dict(rows, columns)
        return self.return_geographies(result)

    def get_geographies_for_user_with_mapping(self, user_id):
        # if bool(self.geography_parent_mapping) is False :
        #     self.get_geographies()
        country_ids = None
        if ((user_id is not None) and (user_id != 0)):
            country_ids = self.get_user_countries(user_id)
        columns = "t1.geography_id, t1.geography_name, t1.parent_names,"
        columns += "t1.level_id,t1.parent_ids, t1.is_active,"
        columns += " t2.country_id, t3.country_name"
        tables = [
            self.tblGeographies, self.tblGeographyLevels, self.tblCountries
        ]
        aliases = ["t1", "t2", "t3"]
        join_type = " INNER JOIN"
        join_conditions = [
            "t1.level_id = t2.level_id", "t2.country_id = t3.country_id"
        ]
        where_condition = "1"
        if country_ids is not None:
            where_condition = "t2.country_id in (%s)" % country_ids
        rows = self.get_data_from_multiple_tables(
            columns, tables, aliases, join_type,
            join_conditions, where_condition
        )
        geographies = {}
        if rows :
            columns = [
                "geography_id", "geography_name", "parent_names", "level_id",
                "parent_ids", "is_active", "country_id", "country_name"
            ]
            result = self.convert_to_dict(rows, columns)
            for d in result:
                parent_ids = [int(x) for x in d["parent_ids"][:-1].split(',')]
                geography = core.GeographyWithMapping(
                    d["geography_id"], d["geography_name"],
                    d["level_id"],
                    d["parent_names"]+">>"+d["geography_name"],
                    parent_ids[-1], bool(d["is_active"])
                )
                country_id = d["country_id"]
                _list = geographies.get(country_id)
                if _list is None :
                    _list = []
                _list.append(geography)
                geographies[country_id] = _list
        return geographies

    def get_geography_report(self):
        q = "SELECT t1.geography_id, t1.geography_name, t1.parent_names, t1.is_active, \
            (select distinct country_id FROM tbl_geography_levels where level_id = t1.level_id) country_id, \
            (select level_position FROM tbl_geography_levels where level_id = t1.level_id) position \
            FROM tbl_geographies t1 ORDER BY position, parent_names, geography_name"

        rows = self.select_all(q)
        columns = ["geography_id", "geography_name", "parent_names", "is_active", "country_id", "position"]
        result = self.convert_to_dict(rows, columns)

        def return_report_data(result) :
            mapping_dict = {}
            for item in result :
                mappings = item["parent_names"] + ">>" + item["geography_name"]
                is_active = bool(item["is_active"])
                country_id = item["country_id"]
                _list = mapping_dict.get(country_id)
                if _list is None:
                    _list = []

                _list.append(
                    knowledgereport.GeographyMapping(
                        mappings, is_active
                    )
                )
                mapping_dict[country_id] = _list
            # for key, value in result.iteritems():
            #     mappings = value[0]
            #     is_active = value[1]
            #     country_id = value[2]

            return mapping_dict

        if bool(self.geography_parent_mapping) is False :
            self.get_geographies()

        return return_report_data(result)

    def get_geography_by_id(self, geography_id):
        query = "SELECT geography_id, geography_name, \
            level_id, parent_ids, parent_names, is_active \
            FROM tbl_geographies WHERE geography_id = %s" % (geography_id)
        rows = self.select_one(query)
        result = []
        if rows :
            columns = [
                "geography_id", "geography_name",
                "level_id", "parent_ids", "parent_names", "is_active"
            ]
            result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_geography(self, country_id, parent_ids, geography_id) :
        query = "SELECT t1.geography_id, t1.geography_name, \
            t1.level_id, t1.is_active \
            FROM tbl_geographies t1 \
            INNER JOIN tbl_geography_levels t2 \
            ON t1.level_id = t2.level_id \
            WHERE t1.parent_ids='%s' \
            AND t2.country_id = %s" % (parent_ids, country_id)
        if geography_id is not None :
            query = query + " AND geography_id != %s" % geography_id

        rows = self.select_all(query)
        columns = ["geography_id", "geography_name", "level_id", "is_active"]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return result

    def save_geography(
        self, geography_level_id, geography_name, parent_ids, parent_names, user_id
    ):
        is_saved = False
        table_name = "tbl_geographies"
        created_on = self.get_date_time()
        geography_id = self.get_new_id("geography_id", table_name)
        field = "(geography_id, geography_name, level_id, \
            parent_ids, parent_names, created_by, created_on)"
        data = (
            geography_id, geography_name, int(geography_level_id),
            parent_ids, parent_names, int(user_id), str(created_on)
        )
        if (self.save_data(table_name, field, data)) :
            action = "New Geography %s added" % (geography_name)
            self.save_activity(user_id, 6, action)
            is_saved = True
        return is_saved

    def update_geography(self, geography_id, name, parent_ids, parent_names, updated_by) :
        oldData = self.get_geography_by_id(geography_id)
        if bool(oldData) is False:
            return False
        # oldparent_ids = oldData["parent_ids"]

        table_name = "tbl_geographies"
        field_with_data = "geography_name='%s', parent_ids='%s', parent_names='%s', \
            updated_by=%s " % (
                name, parent_ids, parent_names, updated_by
            )

        where_condition = "geography_id = %s" % (geography_id)

        self.update_data(table_name, field_with_data, where_condition)
        action = "Geography - %s updated" % name
        self.save_activity(updated_by, 6, action)

        qry = "SELECT geography_id, geography_name, parent_ids, level_id \
          from tbl_geographies \
            WHERE parent_ids like '%s'" % str("%" + str(geography_id) + ",%")
        rows = self.select_all(qry)
        columns = ["geography_id", "geography_name", "parent_ids", "level_id"]
        result = self.convert_to_dict(rows, columns)

        for row in result :
            if row["parent_ids"] == "0,":
                row["parent_ids"] = geography_id
            else :
                row["parent_ids"] = row["parent_ids"][:-1]
            q = "UPDATE tbl_geographies as A inner join ( \
                select p.geography_id, (select group_concat(p1.geography_name SEPARATOR '>>') \
                    from tbl_geographies as p1 where geography_id in (%s)) as names \
                from tbl_geographies as p \
                where p.geography_id = %s \
                ) as B ON A.geography_id = B.geography_id \
                inner join (select c.country_name, g.level_id from tbl_countries c \
                    inner join tbl_geography_levels g on c.country_id = g.country_id ) as C \
                    ON A.level_id  = C.level_id \
                set A.parent_names = concat(C.country_name, '>>', B.names) \
                where A.geography_id = %s AND C.level_id = %s " % (
                    row["parent_ids"], row["geography_id"], row["geography_id"], row["level_id"]
                )
            self.execute(q)
        # action = "Geography name  %s updated in child parent_names" % (name)
        # self.save_activity(updated_by, 6, action)
        # self.getAllGeographies()
        return True

    def change_geography_status(self, geography_id, is_active, updated_by) :
        oldData = self.get_geography_by_id(geography_id)
        if bool(oldData) is False:
            return False
        table_name = "tbl_geographies"
        field_with_data = "is_active=%s, updated_by=%s" % (
            int(is_active), int(updated_by)
        )
        where_condition = "geography_id = %s" % (int(geography_id))
        if (self.update_data(table_name, field_with_data, where_condition)) :
            if is_active == 0:
                status = "deactivated"
            else:
                status = "activated"
            action = "Geography %s status - %s" % (
                oldData["geography_name"], status
            )
            self.save_activity(updated_by, 6, action)
            return True

    def get_statutory_by_id(self, statutory_id):
        query = "SELECT statutory_id, statutory_name, \
            level_id, parent_ids, parent_names \
            FROM tbl_statutories WHERE statutory_id = %s" % (statutory_id)
        rows = self.select_one(query)
        result = []
        if rows :
            columns = [
                "statutory_id", "statutory_name",
                "level_id", "parent_ids", "parent_names"
            ]
            result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_statutory(self, parent_ids, statutory_id, domain_id=None) :
        query = "SELECT T1.statutory_id, T1.statutory_name, T1.level_id, T2.domain_id \
            FROM tbl_statutories T1 \
            INNER JOIN tbl_statutory_levels T2\
            ON T1.level_id = T2.level_id \
            WHERE T1.parent_ids='%s' " % (parent_ids)
        if statutory_id is not None :
            query = query + " AND T1.statutory_id != %s" % statutory_id

        if domain_id is not None :
            query = query + " AND domain_id = %s" % (domain_id)

        rows = self.select_all(query)
        columns = ["statutory_id", "statutory_name", "level_id", "domain_id"]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return result

    def get_statutory_master(self, statutory_id=None):
        columns = [
            "statutory_id", "statutory_name",
            "level_id", "parent_ids",
            "country_id", "country_name",
            "domain_id", "domain_name"
        ]
        query = "SELECT t1.statutory_id, t1.statutory_name, \
            t1.level_id, t1.parent_ids, t2.country_id, \
            t3.country_name, t2.domain_id, t4.domain_name \
            FROM tbl_statutories t1 \
            INNER JOIN tbl_statutory_levels t2 \
            on t1.level_id = t2.level_id \
            INNER JOIN tbl_countries t3 \
            on t2.country_id = t3.country_id \
            INNER JOIN tbl_domains t4 \
            on t2.domain_id = t4.domain_id"
        if statutory_id is not None :
            query = query + " WHERE t1.statutory_id = %s" % (
                statutory_id
            )
        rows = self.select_all(query)
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
            self.set_statutory_parent_mappings(result)
        return self.return_statutory_master(result)

    def return_statutory_master(self, data):
        statutories = {}
        for d in data :
            country_id = d["country_id"]
            domain_id = d["domain_id"]
            statutory_id = int(d["statutory_id"])
            mappings = self.statutory_parent_mapping.get(
                statutory_id
            )
            parent_ids = [
                int(x) for x in d["parent_ids"][:-1].split(',')
            ]

            statutory = core.Statutory(
                statutory_id, d["statutory_name"],
                d["level_id"], parent_ids, parent_ids[-1],
                mappings[1]
            )

            country_wise = statutories.get(country_id)
            _list = []
            if country_wise is None :
                country_wise = {}
            else :
                _list = country_wise.get(domain_id)
                if _list is None :
                    _list = []
            _list.append(statutory)
            country_wise[domain_id] = _list
            statutories[country_id] = country_wise
        return statutories

    def get_country_wise_level_1_statutoy(self) :
        if bool(self.statutory_parent_mapping) is False:
            self.get_statutory_master()
        query = "SELECT t1.statutory_id, t1.statutory_name, \
            t1.level_id, t1.parent_ids, t2.country_id, \
            t3.country_name, t2.domain_id, t4.domain_name \
            FROM tbl_statutories t1 \
            INNER JOIN tbl_statutory_levels t2 \
            on t1.level_id = t2.level_id \
            INNER JOIN tbl_countries t3 \
            on t2.country_id = t3.country_id \
            INNER JOIN tbl_domains t4 \
            on t2.domain_id = t4.domain_id \
            WHERE t2.level_position=1"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = [
                "statutory_id", "statutory_name", "level_id",
                "parent_ids", "country_id", "country_name",
                "domain_id", "domain_name"
            ]
            result = self.convert_to_dict(rows, columns)
        return self.return_statutory_master(result)

    def save_statutory(self, name, level_id, parent_ids, parent_names, user_id) :
        is_saved = False
        statutory_id = self.get_new_id("statutory_id", "tbl_statutories")
        created_on = self.get_date_time()
        table_name = "tbl_statutories"
        field = "(statutory_id, statutory_name, level_id, \
            parent_ids, parent_names, created_by, created_on)"
        data = (
            int(statutory_id), name, int(level_id), parent_ids, parent_names,
            int(user_id), str(created_on)
        )

        if (self.save_data(table_name, field, data)) :
            action = "Statutory - %s added" % name
            self.save_activity(user_id, 10, action)
            is_saved = True
        return is_saved

    def update_statutory(self, statutory_id, name, parent_ids, parent_names, updated_by) :
        oldData = self.get_statutory_by_id(statutory_id)
        if bool(oldData) is False:
            return False
        # oldparent_ids = oldData["parent_ids"]

        table_name = "tbl_statutories"
        field_with_data = "statutory_name='%s', parent_ids='%s', parent_names='%s', \
            updated_by=%s " % (
                name, parent_ids, parent_names, updated_by
            )

        where_condition = "statutory_id = %s" % (statutory_id)

        self.update_data(table_name, field_with_data, where_condition)
        action = "Statutory - %s updated" % name
        self.save_activity(updated_by, 10, action)

        qry = "SELECT statutory_id, statutory_name, parent_ids \
            from tbl_statutories \
            WHERE parent_ids like '%s'" % str("%" + str(statutory_id) + ",%")
        rows = self.select_all(qry)
        columns = ["statutory_id", "statutory_name", "parent_ids"]
        result = self.convert_to_dict(rows, columns)

        for row in result :
            if row["parent_ids"] == "0,":
                row["parent_ids"] = statutory_id
            else :
                row["parent_ids"] = row["parent_ids"][:-1]

            q = "Update tbl_statutories as A inner join ( \
                    select p.statutory_id, (select group_concat(p1.statutory_name SEPARATOR '>>') \
                        from tbl_statutories as p1 where statutory_id in (%s)) as names \
                    from tbl_statutories as p \
                    where p.statutory_id = %s \
                    ) as B on A.statutory_id = B.statutory_id \
                    set A.parent_names = B.names\
                    where A.statutory_id = %s " % (row["parent_ids"], row["statutory_id"], row["statutory_id"])
            self.execute(q)
            action = "statutory name %s updated in child rows." % name
            self.save_activity(updated_by, 10, action)
        return True
        # if oldparent_ids != parent_ids :
        #     oldPId = str(oldparent_ids) + str(statutory_id)
        #     newPId = str(parent_ids) + str(statutory_id)
        #     qry = "SELECT statutory_id, geography_name, parent_ids from tbl_geographies \
        #         WHERE parent_ids like '%s'" % str("%" + str(oldPId) + ",%")
        #     rows = self.dataSelect(qry)
        #     for row in rows :
        #         newParentId = str(row[2]).replace(oldPId, newPId)
        #         q = "UPDATE tbl_geographies set parent_ids='%s', updated_by=%s where geography_id=%s" % (
        #             newParentId, updated_by, row[0]
        #         )
        #         self.dataInsertUpdate(q)
        #     action = "Edit Geography Mappings Parent"
        #     self.save_activity(updated_by, 7, action)
        # self.getAllGeographies()
        # return True

    #
    # statutory mappings
    #
    def set_statutory_parent_mappings(self, rows) :
        _tempDict = {}
        for row in rows :
            _tempDict[row["statutory_id"]] = row["statutory_name"]

        for row in rows :
            statutory_id = int(row["statutory_id"])
            parent_ids = [
                int(x) for x in row["parent_ids"][:-1].split(',')
            ]
            statutory_name = row["statutory_name"]
            names = []
            for id in parent_ids :
                if id > 0 :
                    names.append(_tempDict.get(id))
            names.append(statutory_name)
            mappings = '>>'.join(str(x) for x in names)
            self.statutory_parent_mapping[statutory_id] = [
                statutory_name, mappings, parent_ids
            ]

    def set_geography_parent_mapping(self, rows):
        _tempDict = {}
        for row in rows :
            _tempDict[int(row["geography_id"])] = row["geography_name"]

        for row in rows :
            country_id = int(row["country_id"])
            geography_id = int(row["geography_id"])
            is_active = bool(row["is_active"])
            parent_ids = [int(x) for x in row["parent_ids"][:-1].split(',')]
            names = []
            names.append(row["country_name"])
            for id in parent_ids :
                if id > 0 :
                    names.append(_tempDict.get(id))
            names.append(row["geography_name"])
            mappings = ' >> '.join(str(x) for x in names)
            self.geography_parent_mapping[geography_id] = [
                mappings, is_active, country_id
            ]

    def get_compliance_duration(self):

        def return_compliance_duration(data):
            duration_list = []
            for d in data :
                duration = core.DURATION_TYPE(d["duration_type"])
                duration_list.append(
                    core.ComplianceDurationType(
                        d["duration_type_id"], duration
                    )
                )
            return duration_list

        columns = ["duration_type_id", "duration_type"]
        rows = self.get_data("tbl_compliance_duration_type", "*", None)
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return return_compliance_duration(result)

    def get_compliance_repeat(self):

        def return_compliance_repeat(data):
            repeat_list = []
            for d in data :
                repeat = core.REPEATS_TYPE(d["repeat_type"])
                repeat_list.append(
                    core.ComplianceRepeatType(
                        d["repeat_type_id"], repeat
                    )
                )
            return repeat_list

        columns = ["repeat_type_id", "repeat_type"]
        rows = self.get_data("tbl_compliance_repeat_type", "*", None)
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return return_compliance_repeat(result)

    def get_compliance_frequency(self):

        def return_compliance_frequency(data) :
            frequency_list = []
            for d in data :
                frequency = core.COMPLIANCE_FREQUENCY(
                    d["frequency"]
                )
                c_frequency = core.ComplianceFrequency(
                    d["frequency_id"], frequency
                )
                frequency_list.append(c_frequency)
            return frequency_list

        columns = ["frequency_id", "frequency"]
        rows = self.get_data("tbl_compliance_frequency", "*", None)
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return return_compliance_frequency(result)

    def get_approval_status(self, approval_id=None):

        def return_approval_status(data):
            approval_list = []
            for sts in enumerate(data) :
                approve = core.APPROVAL_STATUS(sts[1])
                c_approval = core.StatutoryApprovalStatus(
                    sts[0], approve
                )
                approval_list.append(c_approval)
            return approval_list

        status = ("Pending", "Approved", "Rejected", "Approved & Notified")

        if approval_id is None :
            return return_approval_status(status)
        else :
            return status[int(approval_id)]

    def get_statutory_mappings(self, user_id, for_approve=False) :

        q = "SELECT distinct t1.statutory_mapping_id, t1.country_id, \
            (select country_name from tbl_countries where country_id = t1.country_id) country_name, \
            t1.domain_id, \
            (select domain_name from tbl_domains where domain_id = t1.domain_id) domain_name, \
            t1.industry_ids, t1.statutory_nature_id, \
            (select statutory_nature_name from tbl_statutory_natures where statutory_nature_id = t1.statutory_nature_id)\
            statutory_nature_name, \
            t1.statutory_ids, \
            t1.geography_ids, \
            t1.approval_status, t1.is_active,  \
            (select group_concat(distinct compliance_id) from tbl_compliances where statutory_mapping_id = t1.statutory_mapping_id) compliance_ids\
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_user_domains t5 \
            ON t5.domain_id = t1.domain_id \
            and t5.user_id = %s \
            INNER JOIN tbl_user_countries t6 \
            ON t6.country_id = t1.country_id \
            and t6.user_id = %s" % (user_id, user_id)

        if for_approve is True :
            q = q + " WHERE t1.approval_status in (0, 2)"

        q = q + " ORDER BY country_name, domain_name, statutory_nature_name"
        rows = self.select_all(q)
        columns = [
            "statutory_mapping_id", "country_id",
            "country_name", "domain_id", "domain_name", "industry_ids",
            "statutory_nature_id", "statutory_nature_name",
            "statutory_ids", "geography_ids",
            "approval_status", "is_active", "compliance_ids"
        ]

        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return self.return_statutory_mappings(result)

    def return_statutory_mappings(self, data, is_report=None):
        if bool(self.statutory_parent_mapping) is False :
            self.get_statutory_master()
        if bool(self.geography_parent_mapping) is False :
            self.get_geographies()
        mapping_data_list = {}
        for d in data :
            mapping_id = int(d["statutory_mapping_id"])
            industry_names = ""
            compliance_ids = [
                int(x) for x in d["compliance_ids"].split(',')
            ]
            if len(compliance_ids) == 1 :
                compliance_ids = compliance_ids[0]
            # compliance_id = int(d["compliance_id"])

            compliances_data = self.get_compliance_by_id(
                compliance_ids, is_report
            )
            compliance_names = compliances_data[0]
            compliances = compliances_data[1]
            geography_ids = [
                int(x) for x in d["geography_ids"][:-1].split(',')
            ]
            geography_mapping_list = []
            for g_id in geography_ids :
                map_data = self.geography_parent_mapping.get(int(g_id))
                if map_data is not None:
                    map_data = map_data[0]
                geography_mapping_list.append(map_data)
            statutory_ids = [
                int(x) for x in d["statutory_ids"][:-1].split(',')
            ]
            statutory_mapping_list = []
            for s_id in statutory_ids :
                s_map_data = self.statutory_parent_mapping.get(int(s_id))
                if s_map_data is not None :
                    s_map_data = s_map_data[1]
                statutory_mapping_list.append(
                    s_map_data
                )
            industry_ids = [
                int(x) for x in d["industry_ids"][:-1].split(',')
            ]
            if len(industry_ids) == 1:
                industry_names = self.get_industry_by_id(industry_ids[0])
            else :
                industry_names = self.get_industry_by_id(industry_ids)

            approval = int(d["approval_status"])
            if approval == 0 :
                approval_status_text = "Pending"
            elif approval == 1 :
                approval_status_text = "Approved"
            elif approval == 2 :
                approval_status_text = "Rejected"
            else :
                approval_status_text = "Approved & Notified"

            statutory = core.StatutoryMapping(
                d["country_id"], d["country_name"],
                d["domain_id"], d["domain_name"],
                industry_ids, industry_names,
                d["statutory_nature_id"], d["statutory_nature_name"],
                statutory_ids, statutory_mapping_list,
                compliances, compliance_names, geography_ids,
                geography_mapping_list, int(d["approval_status"]),
                bool(d["is_active"]), approval_status_text
            )
            mapping_data_list[mapping_id] = statutory
        return mapping_data_list

    def get_statutory_mapping_report(
        self, country_id, domain_id, industry_id,
        statutory_nature_id, geography_id,
        level_1_statutory_id, user_id, from_count, to_count
    ) :
        qry_where = ""
        if industry_id is not None :
            qry_where += "AND t3.industry_id = %s " % (industry_id)
        if geography_id is not None :
            qry_where += "AND t4.geography_id = %s " % (geography_id)
        if statutory_nature_id is not None :
            qry_where += "AND t1.statutory_nature_id = %s " % (statutory_nature_id)
        if level_1_statutory_id is not None :
            qry_where += " AND t1.statutory_mapping LIKE (select group_concat(statutory_name, '%s') from tbl_statutories where statutory_id = %s)" % (str("%"), level_1_statutory_id)

        q_count = "SELECT  count(distinct t2.compliance_id) \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_compliances t2 \
            ON t2.statutory_mapping_id = t1.statutory_mapping_id \
            INNER JOIN tbl_statutory_industry t3 \
            ON t3.statutory_mapping_id = t1.statutory_mapping_id \
            INNER JOIN tbl_statutory_geographies t4 \
            ON t4.statutory_mapping_id = t1.statutory_mapping_id \
            INNER JOIN tbl_user_domains t5 \
            ON t5.domain_id = t1.domain_id \
            and t5.user_id = %s \
            INNER JOIN tbl_user_countries t6 \
            ON t6.country_id = t1.country_id \
            and t6.user_id = %s \
            WHERE t1.approval_status in (1, 3) AND t1.is_active = 1 AND \
            t1.country_id = %s \
            and t1.domain_id = %s %s  \
            ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX(t1.statutory_mapping, '>>', 1), '>>', -1), \
                t2.frequency_id " % (
                user_id, user_id,
                country_id, domain_id,
                qry_where
            )
        row = self.select_one(q_count)
        if row :
            r_count = row[0]
        else :
            r_count = 0

        q = "SELECT distinct t1.statutory_mapping_id, t1.country_id, \
            (select country_name from tbl_countries where country_id = t1.country_id) country_name, \
            t1.domain_id, \
            (select domain_name from tbl_domains where domain_id = t1.domain_id) domain_name, \
            t1.industry_ids, t1.statutory_nature_id, \
            (select statutory_nature_name from tbl_statutory_natures where statutory_nature_id = t1.statutory_nature_id)\
            statutory_nature_name, \
            t1.statutory_ids, \
            t1.geography_ids, \
            t1.approval_status, t1.is_active, t1.statutory_mapping,  \
            t2.compliance_id, t2.statutory_provision, \
            t2.compliance_task, t2.compliance_description, \
            t2.document_name, t2.format_file, t2.format_file_size, \
            t2.penal_consequences, t2.frequency_id, \
            t2.statutory_dates, t2.repeats_every, \
            t2.repeats_type_id, \
            t2.duration, t2.duration_type_id \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_compliances t2 \
            ON t2.statutory_mapping_id = t1.statutory_mapping_id\
            INNER JOIN tbl_statutory_industry t3 \
            ON t3.statutory_mapping_id = t1.statutory_mapping_id\
            INNER JOIN tbl_statutory_geographies t4 \
            ON t4.statutory_mapping_id = t1.statutory_mapping_id\
            INNER JOIN tbl_user_domains t5 \
            ON t5.domain_id = t1.domain_id \
            and t5.user_id = %s \
            INNER JOIN tbl_user_countries t6 \
            ON t6.country_id = t1.country_id \
            and t6.user_id = %s \
            WHERE t1.approval_status in (1, 3) AND t1.is_active = 1 AND \
            t1.country_id = %s \
            and t1.domain_id = %s \
            %s \
            ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX(t1.statutory_mapping, '>>', 1), '>>', -1), t2.frequency_id \
            limit %s, %s" % (
                user_id, user_id,
                country_id, domain_id,
                qry_where,
                from_count, to_count
            )
        rows = self.select_all(q)
        columns = [
            "statutory_mapping_id", "country_id",
            "country_name", "domain_id", "domain_name", "industry_ids",
            "statutory_nature_id", "statutory_nature_name",
            "statutory_ids", "geography_ids",
            "approval_status", "is_active", "statutory_mapping",
            "compliance_id", "statutory_provision",
            "compliance_task", "compliance_description",
            "document_name", "format_file",
            "format_file_size", "penal_consequences",
            "frequency_id", "statutory_dates", "repeats_every",
            "repeats_type_id", "duration", "duration_type_id"
        ]
        report_data = []
        if rows :
            report_data = self.convert_to_dict(rows, columns)

        return self.return_knowledge_report(
            report_data, r_count
        )

    def get_compliance_list_report_techno(
        self, country_id, domain_id, industry_id,
        statutory_nature_id, geography_id,
        level_1_statutory_id, user_id, from_count, to_count
    ) :
        qry_where = ""
        if industry_id is not None :
            qry_where += "AND t3.industry_id = %s " % (industry_id)
        if geography_id is not None :
            qry_where += "AND t4.geography_id = %s " % (geography_id)
        if statutory_nature_id is not None :
            qry_where += "AND t1.statutory_nature_id = %s " % (statutory_nature_id)
        if level_1_statutory_id is not None :
            qry_where += " AND t1.statutory_mapping LIKE (select group_concat(statutory_name, '%s') from tbl_statutories where statutory_id = %s)" % (str("%"), level_1_statutory_id)

        q_count = "SELECT  count(distinct t2.compliance_id) \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_compliances t2 \
            ON t2.statutory_mapping_id = t1.statutory_mapping_id \
            INNER JOIN tbl_statutory_industry t3 \
            ON t3.statutory_mapping_id = t1.statutory_mapping_id \
            INNER JOIN tbl_statutory_geographies t4 \
            ON t4.statutory_mapping_id = t1.statutory_mapping_id \
            INNER JOIN tbl_user_domains t5 \
            ON t5.domain_id = t1.domain_id \
            and t5.user_id = %s \
            INNER JOIN tbl_user_countries t6 \
            ON t6.country_id = t1.country_id \
            and t6.user_id = %s \
            WHERE t1.approval_status in (1, 3) AND t1.is_active = 1 AND \
            t1.country_id = %s \
            and t1.domain_id = %s %s \
            ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX(t1.statutory_mapping, '>>', 1), '>>', -1), \
            (select group_concat(I.industry_name) from tbl_industries I where I.industry_id  in \
            (select industry_id from tbl_statutory_industry where statutory_mapping_id = t1.statutory_mapping_id)), \
                t2.frequency_id " % (
                user_id, user_id,
                country_id, domain_id,
                qry_where
            )
        row = self.select_one(q_count)
        if row :
            r_count = row[0]
        else :
            r_count = 0

        q = "SELECT distinct t1.statutory_mapping_id, t1.country_id, \
            (select country_name from tbl_countries where country_id = t1.country_id) country_name, \
            t1.domain_id, \
            (select domain_name from tbl_domains where domain_id = t1.domain_id) domain_name, \
            t1.industry_ids, t1.statutory_nature_id, \
            (select statutory_nature_name from tbl_statutory_natures where statutory_nature_id = t1.statutory_nature_id)\
            statutory_nature_name, \
            t1.statutory_ids, \
            t1.geography_ids, \
            t1.approval_status, t1.is_active, t1.statutory_mapping,  \
            t2.compliance_id, t2.statutory_provision, \
            t2.compliance_task, t2.compliance_description, \
            t2.document_name, t2.format_file, t2.format_file_size, \
            t2.penal_consequences, t2.frequency_id, \
            t2.statutory_dates, t2.repeats_every, \
            t2.repeats_type_id, \
            t2.duration, t2.duration_type_id, \
            (select group_concat(I.industry_name) from tbl_industries I where I.industry_id  in \
            (select industry_id from tbl_statutory_industry where statutory_mapping_id = t1.statutory_mapping_id))industry \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_compliances t2 \
            ON t2.statutory_mapping_id = t1.statutory_mapping_id\
            INNER JOIN tbl_statutory_industry t3 \
            ON t3.statutory_mapping_id = t1.statutory_mapping_id\
            INNER JOIN tbl_statutory_geographies t4 \
            ON t4.statutory_mapping_id = t1.statutory_mapping_id\
            INNER JOIN tbl_user_domains t5 \
            ON t5.domain_id = t1.domain_id \
            and t5.user_id = %s \
            INNER JOIN tbl_user_countries t6 \
            ON t6.country_id = t1.country_id \
            and t6.user_id = %s \
            WHERE t1.approval_status in (1, 3) AND t1.is_active = 1 AND \
            t1.country_id = %s \
            and t1.domain_id = %s \
            %s \
            ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX(t1.statutory_mapping, '>>', 1), '>>', -1), \
                industry, t2.frequency_id \
                limit %s, %s" % (
                user_id, user_id,
                country_id, domain_id,
                qry_where,
                from_count, to_count
            )
        rows = self.select_all(q)
        columns = [
            "statutory_mapping_id", "country_id",
            "country_name", "domain_id", "domain_name", "industry_ids",
            "statutory_nature_id", "statutory_nature_name",
            "statutory_ids", "geography_ids",
            "approval_status", "is_active", "statutory_mapping",
            "compliance_id", "statutory_provision",
            "compliance_task", "compliance_description",
            "document_name", "format_file",
            "format_file_size", "penal_consequences",
            "frequency_id", "statutory_dates", "repeats_every",
            "repeats_type_id", "duration", "duration_type_id", "industry"
        ]
        report_data = []
        if rows :
            report_data = self.convert_to_dict(rows, columns)

        return self.return_knowledge_report(
            report_data, r_count
        )

    def get_mappings_id(self, statutory_id) :
        query = "select distinct t1.statutory_mapping_id \
            from tbl_statutory_statutories t1 \
            where t1.statutory_id in ( \
            select t.statutory_id from tbl_statutories t where \
            t.statutory_id = %s OR t.parent_ids like '%s' \
            )" % (
                int(statutory_id),
                str("" + str(statutory_id) + ",%")
            )
        rows = self.select_all(query)
        result = []
        if rows :
            result = self.convert_to_dict(
                rows, ["statutory_mapping_ids"]
            )
        return result

    def return_knowledge_report(self, report_data, total_count=None):
        if bool(self.geography_parent_mapping) is False :
            self.get_geographies()

        report_list = []
        for r in report_data :
            mapping = r["statutory_mapping"].split(">>")
            act_name = mapping[0].strip()
            statutory_provision = " >>".join(mapping[1:])
            statutory_provision += " " + r["statutory_provision"]
            compliance_task = r["compliance_task"]
            document_name = r["document_name"]
            if document_name == "None":
                document_name = None
            if document_name :
                name = "%s - %s" % (
                    document_name, compliance_task
                )
            else :
                name = compliance_task

            format_file = r["format_file"]
            format_file_size = r["format_file_size"]
            if format_file_size is not None :
                format_file_size = int(format_file_size)
            if format_file :
                url = "%s/%s" % (
                    FORMAT_DOWNLOAD_URL, format_file
                )
            else :
                url = None
            industry_ids = [
                int(x) for x in r["industry_ids"][:-1].split(',')
            ]
            if len(industry_ids) == 1:
                industry_names = self.get_industry_by_id(industry_ids[0])
            else :
                industry_names = self.get_industry_by_id(industry_ids)

            geography_ids = [
                int(x) for x in r["geography_ids"][:-1].split(',')
            ]
            geography_mapping_list = []
            for g_id in geography_ids :
                map_data = self.geography_parent_mapping.get(int(g_id))
                if map_data is not None:
                    map_data = map_data[0]
                geography_mapping_list.append(map_data)

            statutory_dates = r["statutory_dates"]
            statutory_dates = json.loads(statutory_dates)
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)

            info = knowledgereport.StatutoryMappingReport(
                r["country_name"],
                r["domain_name"],
                industry_names,
                r["statutory_nature_name"],
                geography_mapping_list,
                r["approval_status"],
                bool(r["is_active"]),
                act_name,
                r["compliance_id"],
                statutory_provision,
                name,
                r["compliance_description"],
                r["penal_consequences"],
                r["frequency_id"],
                date_list,
                r["repeats_type_id"],
                r["repeats_every"],
                r["duration_type_id"],
                r["duration"],
                url
            )
            report_list.append(info)
        return report_list, total_count
    #
    # compliance
    #

    def get_compliance_by_id(self, compliance_id, is_active=None):
        q = ""
        if is_active is None :
            if type(compliance_id) == IntType :
                q = " WHERE t1.compliance_id = %s" % (
                    compliance_id
                )
            else :
                q = " WHERE t1.compliance_id in %s" % (
                    str(tuple(compliance_id))
                )
        else :
            is_active = int(is_active)

            if type(compliance_id) == IntType :
                q = " WHERE t1.is_active = %s AND t1.compliance_id = %s" % (
                    is_active, compliance_id
                )
            else :
                q = " WHERE t1.is_active = %s AND t1.compliance_id in %s" % (
                    is_active, str(tuple(compliance_id))
                )

        qry = "SELECT t1.compliance_id, t1.statutory_provision, \
            t1.compliance_task, t1.compliance_description, \
            t1.document_name, t1.format_file, t1.format_file_size, \
            t1.penal_consequences, t1.frequency_id, \
            t1.statutory_dates, t1.repeats_every, \
            t1.repeats_type_id, \
            t1.duration, t1.duration_type_id, t1.is_active, \
            (select frequency from tbl_compliance_frequency where frequency_id = t1.frequency_id), \
            (select duration_type from tbl_compliance_duration_type where duration_type_id = t1.duration_type_id) duration_type,\
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t1.repeats_type_id) repeat_type \
            FROM tbl_compliances t1 %s ORDER BY t1.frequency_id" % q
        rows = self.select_all(qry)
        columns = [
            "compliance_id", "statutory_provision",
            "compliance_task", "compliance_description",
            "document_name", "format_file",
            "format_file_size", "penal_consequences",
            "frequency_id", "statutory_dates", "repeats_every",
            "repeats_type_id", "duration", "duration_type_id",
            "is_active", "frequency",
            "duration_type", "repeat_type"
        ]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return self.return_compliance(result)

    def return_compliance(self, data):
        compliance_names = []
        compalinaces = []
        for d in data :
            statutory_dates = d["statutory_dates"]
            statutory_dates = json.loads(statutory_dates)
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)

            compliance_task = d["compliance_task"]
            document_name = d["document_name"]
            if document_name == "None":
                document_name = None
            if document_name :
                name = "%s - %s" % (
                    document_name, compliance_task
                )
            else :
                name = compliance_task
            format_file = d["format_file"]
            format_file_size = d["format_file_size"]
            if format_file_size is not None :
                format_file_size = int(format_file_size)
            file_list = []
            if format_file :
                file_download = "%s/%s" % (
                    FORMAT_DOWNLOAD_URL, format_file
                )
                file_info = core.FileList(
                    format_file_size, format_file, file_download
                )
                file_list.append(file_info)

            else :
                file_list = None
                file_download = None

            compliance_names.append(core.Compliance_Download(name, file_download))

            if d["frequency_id"] in (2, 3) :
                summary = "Repeats every %s - %s" % (d["repeats_every"], d["repeat_type"])
            elif d["frequency_id"] == 4 :
                summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
            else :
                summary = None

            # compliance_names.append(name)
            compliance = core.Compliance(
                d["compliance_id"], d["statutory_provision"],
                compliance_task, d["compliance_description"],
                document_name, file_list,
                d["penal_consequences"], d["frequency_id"],
                date_list, d["repeats_type_id"],
                d["repeats_every"], d["duration_type_id"],
                d["duration"], bool(d["is_active"]),
                d["frequency"], summary
            )
            compalinaces.append(compliance)
        return [compliance_names, compalinaces]

    #
    # save statutory mapping
    #

    def convert_base64_to_file(self, file_name, file_content, file_path=None):
        if file_path is None :
            file_path = "%s/%s" % (KNOWLEDGE_FORMAT_PATH, file_name)
        else:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                os.chmod(file_path, 0777)
            file_path = "%s/%s" % (file_path, file_name)
        self.remove_uploaded_file(file_path)
        new_file = open(file_path, "wb")
        new_file.write(file_content.decode('base64'))
        new_file.close()

    def remove_uploaded_file(self, file_path):
        if os.path.exists(file_path) :
            os.remove(file_path)

    def check_duplicate_statutory_mapping(self, data, statutory_mapping_id=None) :
        country_id = data.country_id
        domain_id = data.domain_id
        statutory_nature = data.statutory_nature_id
        industry_id = data.industry_ids
        if len(industry_id) == 1  :
            industry_id = "(%s)" % (industry_id[0])
        else :
            industry_id = str(tuple(industry_id))
        statutory_id = data.statutory_ids
        if len(statutory_id) == 1 :
            statutory_id = "(%s)" % (statutory_id[0])
        else :
            statutory_id = str(tuple(statutory_id))

        q = "SELECT distinct t1.statutory_mapping_id from tbl_statutory_mappings t1 \
            inner join tbl_statutory_statutories t2 on \
            t1.statutory_mapping_id = t2.statutory_mapping_id \
            inner join tbl_statutory_industry t3 on \
            t1.statutory_mapping_id = t3.statutory_mapping_id \
            WHERE t1.country_id = %s AND t1.domain_id = %s AND \
            t1.statutory_nature_id = %s AND t2.statutory_id in %s AND \
            t3.industry_id in %s" % (
                country_id,
                domain_id,
                statutory_nature,
                statutory_id,
                industry_id
            )
        if statutory_mapping_id is not None :
            q = q + " AND t1.statutory_mapping_id != %s" % statutory_mapping_id
        row = self.select_one(q)
        if row :
            return row[0]
        else :
            return None

    def check_duplicate_compliance_name(self, request_frame):
        compliances = request_frame.compliances
        country_id = request_frame.country_id
        domain_id = request_frame.domain_id
        mapping = request_frame.mappings
        compliance_names = []
        for m in mapping :
            statutory_mappings = m
            for c in compliances :
                compliance_name = c.compliance_task
                compliance_id = c.compliance_id
                statutory_provision = c.statutory_provision
                q = "SELECT count(t1.compliance_task) FROM tbl_compliances t1 INNER JOIN \
                    tbl_statutory_mappings t2 on t1.statutory_mapping_id = t2.statutory_mapping_id \
                    WHERE t2.country_id = %s AND t2.domain_id = %s AND \
                    LOWER(t1.compliance_task) = LOWER('%s') \
                    AND LOWER (t1.statutory_provision) = LOWER('%s') \
                    AND LOWER(t2.statutory_mapping) LIKE LOWER('%s')" % (
                        country_id, domain_id, compliance_name,
                        statutory_provision,
                        str("%" + statutory_mappings + "%")
                    )
                if compliance_id is not None :
                    q = q + " AND t1.compliance_id != %s" % (compliance_id)
                row = self.select_one(q)
                if row[0] > 0 :
                    compliance_names.append(compliance_name)
        if len(compliance_names) > 0 :
            return list(set(compliance_names))
        else :
            return False

    def save_statutory_mapping(self, data, created_by) :
        country_id = data.country_id
        domain_id = data.domain_id
        industry_ids = ','.join(str(x) for x in data.industry_ids) + ","
        nature_id = data.statutory_nature_id
        statutory_ids = ','.join(str(x) for x in data.statutory_ids) + ","
        compliances = data.compliances
        geography_ids = ','.join(str(x) for x in data.geography_ids) + ","
        statutory_mapping = '-'.join(data.mappings)

        statutory_mapping_id = self.get_new_id(
            "statutory_mapping_id", "tbl_statutory_mappings"
        )
        created_on = self.get_date_time()
        is_active = 1

        statutory_table = "tbl_statutory_mappings"
        field = "(statutory_mapping_id, country_id, domain_id, \
            industry_ids, statutory_nature_id, statutory_ids, \
            geography_ids, is_active, statutory_mapping, created_by, created_on)"
        data_save = (
            statutory_mapping_id, int(country_id), int(domain_id),
            industry_ids, int(nature_id), statutory_ids,
            geography_ids, int(is_active),
            statutory_mapping,
            int(created_by), str(created_on)
        )
        if (self.save_data(statutory_table, field, data_save)) :
            self.update_statutory_mapping_id(
                data.statutory_ids,
                statutory_mapping_id, created_by
            )
            ids, names = self.save_compliance(
                statutory_mapping_id, domain_id,
                compliances, created_by
            )
            compliance_ids = ','.join(str(x) for x in ids) + ","
            qry = "UPDATE tbl_statutory_mappings set compliance_ids='%s' \
                where statutory_mapping_id = %s" % (
                    compliance_ids, statutory_mapping_id
                )
            self.execute(qry)
            self.save_statutory_industry(
                statutory_mapping_id, data.industry_ids, True
            )
            self.save_statutory_geography_id(
                statutory_mapping_id, data.geography_ids, True
            )
            self.save_statutory_statutories_id(
                statutory_mapping_id, data.statutory_ids, True
            )
            notification_log_text = "New statutory mapping has been created %s" % (statutory_mapping)
            link = "/knowledge/approve-statutory-mapping"
            self.save_notifications(
                notification_log_text, link,
                domain_id, country_id, created_by,
                user_id=None
            )
            action = "New statutory mappings added"
            self.save_activity(created_by, 10, action)
            return True
        else :
            return False

    def save_statutory_industry(self, mapping_id, industry_ids, is_new) :
        tbl_name = "tbl_statutory_industry"
        columns = ["statutory_mapping_id", "industry_id"]

        if is_new is False :
            qry = "DELETE FROM tbl_statutory_industry \
                WHERE statutory_mapping_id = %s" % (mapping_id)
            self.execute(qry)

        for i_id in industry_ids :
            values = [mapping_id, i_id]
            self.insert(tbl_name, columns, values)

    def save_statutory_geography_id(self, mapping_id, geography_ids, is_new) :
        tbl_name = "tbl_statutory_geographies"
        columns = ["statutory_mapping_id", "geography_id"]

        if is_new is False :
            qry = "DELETE FROM tbl_statutory_geographies \
                WHERE statutory_mapping_id = %s" % (mapping_id)
            self.execute(qry)

        for g_id in geography_ids :
            values = [mapping_id, g_id]
            self.insert(tbl_name, columns, values)

    def save_statutory_statutories_id(
        self, mapping_id, statutory_ids, is_new
    ) :
        tbl_name = "tbl_statutory_statutories"
        columns = ["statutory_mapping_id", "statutory_id"]

        if is_new is False :
            qry = "DELETE FROM tbl_statutory_statutories \
                WHERE statutory_mapping_id = %s" % (mapping_id)
            self.execute(qry)

        for s_id in statutory_ids :
            values = [mapping_id, s_id]
            self.insert(tbl_name, columns, values)

    def update_statutory_mapping_id(
        self, statutory_ids, mapping_id, updated_by
    ) :
        # remove mapping id
        map_id = str("%" + str(mapping_id) + ",%")
        q = "SELECT statutory_id, statutory_mapping_ids from tbl_statutories \
            WHERE statutory_mapping_ids like '%s'" % map_id
        rows = self.select_all(q)
        old_statu_ids = {}
        for row in rows :
            old_statu_ids[int(row[0])] = row[1][:-1]
        difference = list(set(old_statu_ids.keys()) - set(statutory_ids))

        tbl_statutory = "tbl_statutories"
        columns = ["statutory_mapping_ids", "updated_by"]

        for x in difference :
            old_map_id = [int(j) for j in old_statu_ids.get(x).strip().split(',') if j != '']
            if mapping_id in old_map_id:
                old_map_id = old_map_id.remove(mapping_id)

            new_map_id = ""
            if old_map_id is not None :
                new_map_id = ','.join(str(k) for k in old_map_id) + ","
            values = [new_map_id, updated_by]
            where = "statutory_id = %s" % (x)
            self.update(tbl_statutory, columns, values, where)
            print "Mapping Id %s removed from statutory table, Id=%s" % (
                mapping_id, x
            )

        # statutory_ids = statutory_ids[:-1]
        # ids = [int(x) for x in statutory_ids.split(',')]
        ids = tuple(statutory_ids)
        if (len(ids) == 1) :
            qry_where = " WHERE statutory_id = %s" % ids[0]
        else :
            qry_where = " WHERE statutory_id in %s" % str(ids)

        qry = "SELECT statutory_id, statutory_mapping_ids \
            from tbl_statutories %s" % (
                qry_where
            )
        # isUpdated = False
        rows = self.select_all(qry)
        for row in rows:
            statutory_id = int(row[0])

            if row[1] is None :
                map_id = ""
            else :
                map_id = row[1]
            _statutory_mapping_id = str(mapping_id) + ","
            if (len(map_id) > 0):
                mapping_ids = [int(x) for x in row[1][:-1].split(',')]
                if (mapping_id not in mapping_ids) :
                    mapping_ids.append(mapping_id)
                _statutory_mapping_id = ','.join(
                    str(x) for x in mapping_ids
                ) + ","
            values = [_statutory_mapping_id, updated_by]
            where = "statutory_id = %s" % (statutory_id)
            self.update(tbl_statutory, columns, values, where)

    def save_compliance(self, mapping_id, domain_id, datas, created_by) :
        compliance_ids = []
        compliance_names = []
        is_format = False
        for data in datas :
            compliance_id = self.get_new_id(
                "compliance_id", "tbl_compliances"
            )
            created_on = self.get_date_time()

            provision = data.statutory_provision
            compliance_task = data.compliance_task
            compliance_description = data.description
            document_name = data.document_name
            file_list = data.format_file_list
            file_name = ""
            file_size = 0
            file_content = ""

            if file_list is not None :
                file_list = file_list[0]
                name = file_list.file_name.split('.')[0]
                exten = file_list.file_name.split('.')[1]
                auto_code = self.new_uuid()
                file_name = "%s-%s.%s" % (name, auto_code, exten)
                file_size = file_list.file_size
                file_content = file_list.file_content
                is_format = True

            penal_consequences = data.penal_consequences
            compliance_frequency = data.frequency_id
            statutory_dates = []
            for s_d in data.statutory_dates :
                statutory_dates.append(s_d.to_structure())
            statutory_dates = json.dumps(statutory_dates)
            repeats_every = data.repeats_every
            repeats_type = data.repeats_type_id
            duration = data.duration
            duration_type = data.duration_type_id
            is_active = int(data.is_active)

            table_name = "tbl_compliances"
            columns = [
                "compliance_id", "statutory_provision",
                "compliance_task", "compliance_description",
                "document_name", "format_file", "format_file_size",
                "penal_consequences", "frequency_id",
                "statutory_dates", "statutory_mapping_id",
                "is_active", "created_by", "created_on", "domain_id"
            ]
            values = [
                compliance_id, provision, compliance_task,
                compliance_description, document_name,
                file_name, file_size, penal_consequences,
                compliance_frequency, statutory_dates,
                mapping_id, is_active, created_by, created_on, domain_id
            ]
            if compliance_frequency == 1 :
                pass

            elif compliance_frequency == 4 :
                if duration is None :
                    duration = ""
                if duration_type is None:
                    duration_type = ""
                columns.extend(["duration", "duration_type_id"])
                values.extend([duration, duration_type])
            else :
                if repeats_every is None :
                    repeats_every = ""
                if repeats_type is None :
                    repeats_type = ""
                columns.extend(["repeats_every", "repeats_type_id"])
                values.extend([repeats_every, repeats_type])
            self.insert(table_name, columns, values)
            if is_format :
                self.convert_base64_to_file(file_name, file_content)
                is_format = False
            compliance_ids.append(compliance_id)
            if document_name == "None":
                document_name = None
            if document_name :
                compliance_names.append(
                    document_name + "-" + compliance_task
                )
            else :
                compliance_names.append(compliance_task)
            # if (self.execute(query)) :
            #     compliance_ids.append(compliance_id)

        return compliance_ids, compliance_names

    def update_statutory_mapping(self, data, updated_by) :
        statutory_mapping_id = data.statutory_mapping_id
        is_exists = self.get_statutory_mapping_by_id(statutory_mapping_id)
        if bool(is_exists) is False :
            return False
        domain_id = data.domain_id
        country_id = int(is_exists["country_id"])
        industry_ids = ','.join(str(x) for x in data.industry_ids) + ","
        nature_id = data.statutory_nature_id
        statutory_ids = ','.join(str(x) for x in data.statutory_ids) + ","
        compliances = data.compliances
        geography_ids = ','.join(str(x) for x in data.geography_ids) + ","
        statutory_mapping = '-'.join(data.mappings)

        self.save_statutory_backup(statutory_mapping_id, updated_by)
        table_name = "tbl_statutory_mappings"
        columns = (
            "industry_ids", "statutory_nature_id", "statutory_ids",
            "geography_ids", "approval_status", "rejected_reason",
            "statutory_mapping",
            "updated_by"
        )
        values = (
            industry_ids, nature_id, statutory_ids, geography_ids,
            0, '', statutory_mapping, int(updated_by)
        )
        where_condition = " statutory_mapping_id= %s " % (statutory_mapping_id)

        self.update(table_name, columns, values, where_condition)
        self.update_statutory_mapping_id(data.statutory_ids, statutory_mapping_id, updated_by)
        ids, names = self.update_compliance(statutory_mapping_id, domain_id, compliances, updated_by)
        compliance_ids = ','.join(str(x) for x in ids) + ","
        self.update(table_name, ["compliance_ids"], [compliance_ids], where_condition)
        self.save_statutory_industry(
            statutory_mapping_id, data.industry_ids, False
        )
        self.save_statutory_geography_id(
            statutory_mapping_id, data.geography_ids, False
        )
        self.save_statutory_statutories_id(
            statutory_mapping_id, data.statutory_ids, False
        )
        action = "Edit Statutory Mappings"
        self.save_activity(updated_by, 10, action)
        notification_log_text = "Stautory mapping has been updated %s" % (statutory_mapping)
        link = "/knowledge/approve-statutory-mapping"
        self.save_notifications(
            notification_log_text, link,
            domain_id, country_id, updated_by,
            user_id=None
        )
        return True

    def get_saved_format_file(self, compliance_id):
        query = "SELECT format_file, format_file_size \
            FROM tbl_compliances WHERE compliance_id = %s " % (
                compliance_id
            )
        rows = self.select_one(query)
        result = self.convert_to_dict(rows, ["format_file", "format_file_size"])
        if result :
            return (result["format_file"], result["format_file_size"])
        else :
            return None

    def update_compliance(self, mapping_id, domain_id, datas, updated_by) :
        is_format = False
        compliance_ids = []
        compliance_names = []
        for data in datas :
            compliance_id = data.compliance_id

            if (compliance_id is None) :
                ids, names = self.save_compliance(mapping_id, domain_id, [data], updated_by)
                compliance_ids.extend(ids)
                continue
            else :
                saved_file = self.get_saved_format_file(compliance_id)
            provision = data.statutory_provision
            compliance_task = data.compliance_task
            description = data.description
            document_name = data.document_name
            file_list = data.format_file_list
            file_name = ""
            file_size = 0
            file_content = ""
            saved_file_name = saved_file[0]
            if saved_file_name :
                if len(saved_file_name) == 0 :
                    saved_file_name = None

            if file_list is None :
                pass
            elif file_list is None and saved_file_name is not None:
                self.remove_uploaded_file(saved_file[0])
            else :
                if saved_file_name is None :
                    file_list = file_list[0]
                    file_name = file_list.file_name
                    name = file_list.file_name.split('.')[0]
                    exten = file_list.file_name.split('.')[1]
                    auto_code = self.new_uuid()
                    file_name = "%s-%s.%s" % (name, auto_code, exten)
                    file_size = file_list.file_size
                    file_content = file_list.file_content
                    is_format = True
                else :
                    file_list = file_list[0]
                    file_name = saved_file_name
                    if len(file_name) == 0 :
                        file_name = None

                    if file_name is None :
                        file_name = file_list.file_name
                        name = file_list.file_name.split('.')[0]
                        exten = file_list.file_name.split('.')[1]
                        auto_code = self.new_uuid()
                        file_name = "%s-%s.%s" % (name, auto_code, exten)
                        is_format = True
                    file_size = file_list.file_size
                    file_content = file_list.file_content

            penal_consequences = data.penal_consequences
            compliance_frequency = data.frequency_id
            statutory_dates = []
            for s_d in data.statutory_dates :
                statutory_dates.append(s_d.to_structure())

            statutory_dates = json.dumps(statutory_dates)
            repeats_every = data.repeats_every
            repeats_type = data.repeats_type_id
            duration = data.duration
            duration_type = data.duration_type_id
            is_active = int(data.is_active)

            table_name = "tbl_compliances"
            columns = [
                "statutory_provision", "compliance_task",
                "compliance_description", "document_name",
                "format_file", "format_file_size", "penal_consequences",
                "frequency_id", "statutory_dates",
                "statutory_mapping_id", "is_active",
                "updated_by", "domain_id"
            ]
            values = [
                provision, compliance_task, description,
                document_name, file_name, file_size,
                penal_consequences, compliance_frequency,
                statutory_dates, mapping_id, is_active,
                updated_by, domain_id
            ]
            if compliance_frequency == 1 :
                pass

            elif compliance_frequency == 4 :
                columns.extend(["duration", "duration_type_id"])
                values.extend([duration, duration_type])

            else :
                columns.extend(["repeats_every", "repeats_type_id"])
                values.extend([repeats_every, repeats_type])

            where_condition = "compliance_id = %s" % (compliance_id)
            self.update(table_name, columns, values, where_condition)
            if is_format :
                self.convert_base64_to_file(file_name, file_content)
                is_format = False
            compliance_ids.append(compliance_id)

        return compliance_ids, compliance_names

    def change_compliance_status(self, mapping_id, is_active, updated_by) :
        tbl_name = "tbl_compliances"
        columns = ["is_active", "updated_by"]
        values = [is_active, int(updated_by)]
        where = "statutory_mapping_id=%s" % (mapping_id)
        self.update(tbl_name, columns, values, where)

    def change_statutory_mapping_status(self, data, updated_by):
        statutory_mapping_id = int(data.statutory_mapping_id)
        is_active = int(data.is_active)
        table_name = "tbl_statutory_mappings"
        columns = ["is_active", "updated_by"]
        values = [is_active, int(updated_by)]
        where = "statutory_mapping_id=%s" % (statutory_mapping_id)
        self.update(table_name, columns, values, where)
        self.change_compliance_status(statutory_mapping_id, is_active, updated_by)
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"
        action = "Statutory Mapping has been %s" % status
        self.save_activity(updated_by, 10, action)
        return True

    def save_statutory_backup(self, statutory_mapping_id, created_by):
        old_record = self.get_statutory_mapping_by_id(statutory_mapping_id)
        backup_id = self.get_new_id("statutory_backup_id", "tbl_statutories_backup")
        created_on = self.get_date_time()
        industry_ids = [
            int(x) for x in old_record["industry_ids"][:-1].split(',')
        ]

        if len(industry_ids) == 1:
            industry_name = self.get_industry_by_id(industry_ids[0])
        else :
            industry_name = self.get_industry_by_id(industry_ids)

        provision = []
        # for sid in old_record["statutory_ids"][:-1].split(',') :
        #     data = self.statutory_parent_mapping.get(int(sid))
        #     provision.append(data[1])
        for sid in old_record["statutory_ids"][:-1].split(',') :
            data = self.get_statutory_by_id(sid)
            provision.append(data["parent_names"])
        mappings = ','.join(provision)

        geo_map = []
        for gid in old_record["geography_ids"][:-1].split(',') :
            data = self.get_geography_by_id(gid)
            if data is not None :
                data = data["parent_names"]
            geo_map.append(data)
        geo_mappings = ','.join(geo_map)

        tbl_statutory_backup = "tbl_statutories_backup"
        columns = [
            "statutory_backup_id", "statutory_mapping_id",
            "country_name", "domain_name", "industry_name",
            "statutory_nature", "statutory_provision",
            "applicable_location", "created_by",
            "created_on"
        ]
        values = [
            backup_id, statutory_mapping_id,
            old_record["country_name"], old_record["domain_name"],
            industry_name, old_record["statutory_nature_name"],
            mappings,
            geo_mappings, int(created_by), created_on
        ]
        self.insert(tbl_statutory_backup, columns, values)

        qry = " INSERT INTO tbl_compliances_backup \
            (statutory_backup_id, statutory_provision, \
            compliance_task, compliance_description, \
            document_name, format_file, \
            penal_consequences, frequency_id, \
            statutory_dates, repeats_every, \
            repeats_type_id, duration, duration_type_id)  \
            SELECT \
            %s,t1.statutory_provision, t1.compliance_task, \
            t1.compliance_description, t1.document_name, \
            t1.format_file, t1.penal_consequences, \
            t1.frequency_id, t1.statutory_dates, \
            t1.repeats_every, t1.repeats_type_id, \
            t1.duration, t1.duration_type_id \
            FROM tbl_compliances t1 \
            WHERE statutory_mapping_id=%s" % (
                backup_id, statutory_mapping_id
            )
        self.execute(qry)

    def get_statutory_mapping_by_id(self, mapping_id) :
        q = "SELECT t1.country_id, t2.country_name, \
            t1.domain_id, t3.domain_name, t1.industry_ids, \
            t1.statutory_nature_id, t4.statutory_nature_name, \
            t1.statutory_ids, t1.compliance_ids, \
            t1.geography_ids, t1.approval_status, t1.statutory_mapping  \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_countries t2 \
            on t1.country_id = t2.country_id \
            INNER JOIN tbl_domains t3 \
            on t1.domain_id = t3.domain_id \
            INNER JOIN tbl_statutory_natures t4 \
            on t1.statutory_nature_id = t4.statutory_nature_id \
            WHERE t1.statutory_mapping_id=%s" % mapping_id
        rows = self.select_one(q)
        columns = [
            "country_id", "country_name", "domain_id",
            "domain_name", "industry_ids", "statutory_nature_id",
            "statutory_nature_name", "statutory_ids",
            "compliance_ids", "geography_ids",
            "approval_status", "statutory_mapping"
        ]
        result = {}
        if rows :
            result = self.convert_to_dict(rows, columns)
        return result

    def change_approval_status(self, data, updated_by) :
        statutory_mapping_id = int(data.statutory_mapping_id)
        provision = data.statutory_provision
        approval_status = int(data.approval_status)
        rejected_reason = data.rejected_reason
        notification_text = data.notification_text
        tbl_name = "tbl_statutory_mappings"
        columns = [
            "approval_status"
        ]
        values = [
            approval_status
        ]
        where = "statutory_mapping_id=%s" % (statutory_mapping_id)

        q = "SELECT statutory_mapping, created_by, updated_by, domain_id, \
            country_id from tbl_statutory_mappings \
            where statutory_mapping_id = %s" % (
                statutory_mapping_id
            )
        rows = self.select_one(q)
        users = self.convert_to_dict(rows, [
            "statutory_mapping", "created_by", "updated_by",
            "domain_id", "country_id"
        ])

        if approval_status == 2 :
            # Rejected
            columns.extend(["rejected_reason"])
            values.extend([rejected_reason])
            notification_log_text = "Statutory Mapping: %s \
                has been Rejected and reason is %s" % (provision, rejected_reason)
        else :
            notification_log_text = "Statutory Mapping: %s \
                has been Approved" % (provision)

        self.update(tbl_name, columns, values, where)
        if approval_status == 3 :
            self.save_statutory_notifications(
                statutory_mapping_id, notification_text
            )
            notification_log_text = "Statutory Mapping: %s \
                has been Approved & Notified" % (provision)

        link = "/knowledge/statutory-mapping"
        if users["updated_by"] is None :
            user_id = int(users["created_by"])
        else :
            user_id = int(users["updated_by"])
        self.save_notifications(
            notification_log_text, link,
            users["domain_id"], users["country_id"], updated_by,
            user_id
        )
        self.save_activity(updated_by, 11, notification_log_text)
        return True

    def save_notifications(
        self, notification_text, link,
        domain_id, country_id, current_user, user_id
    ):
        # internal notification
        notification_id = self.get_new_id(
            "notification_id", "tbl_notifications"
        )
        query = "INSERT INTO tbl_notifications \
            (notification_id, notification_text, link) \
            VALUES (%s, '%s', '%s')" % (
                notification_id, notification_text, link
            )
        self.execute(query)
        self.save_notifications_status(
            notification_id, domain_id, country_id, current_user, user_id
        )

    def save_notifications_status(
        self, notification_id, domain_id, country_id,
        current_user=None,
        user_id=None
    ):
        user_ids = []
        q = "INSERT INTO tbl_notifications_status \
                (notification_id, user_id, read_status) VALUES \
                (%s, %s, 0)"

        query = "SELECT distinct user_id from tbl_users WHERE \
            user_group_id in \
            (select user_group_id from tbl_user_groups \
            where form_ids like '%s') AND \
            user_id in (select user_id from \
                tbl_user_domains where domain_id = %s \
            )  \
            AND user_id in (select distinct user_id from \
                tbl_user_countries where country_id = %s)" % (
                str('%11,%'),
                domain_id,
                country_id
            )
        rows = self.select_all(query)
        if rows :
            for r in rows :
                notify_user_id = r[0]
                if current_user == notify_user_id :
                    continue
                user_ids.append(notify_user_id)
                self.execute(q % (notification_id, notify_user_id))
        if user_id is not None and user_id != current_user:
            if user_ids:
                if user_id not in user_ids:
                    self.execute(q % (notification_id, user_id))
            else :
                self.execute(q % (notification_id, user_id))

    def get_statutory_assigned_to_client(self, mapping_id):
        query = "SELECT distinct t1.unit_id, t1.client_id, \
            (select business_group_id from tbl_units \
                where unit_id = t1.unit_id) business_group_id, \
            (select legal_entity_id from tbl_units \
                where unit_id = t1.unit_id) legal_entity_id,\
            (select division_id from tbl_units \
                where unit_id = t1.unit_id) division_id \
            from tbl_client_statutories t1 \
            INNER JOIN tbl_client_compliances t2 \
            ON t1.client_statutory_id = t2.client_statutory_id \
            AND t2.compliance_id in \
                (select c.compliance_id from \
                tbl_compliances c where c.statutory_mapping_id = %s) " % (mapping_id)
        rows = self.select_all(query)

        if rows :
            columns = [
                "unit_id", "client_id", "business_group_id",
                "legal_entity_id", "division_id"
            ]
            result = self.convert_to_dict(rows, columns)
            return result
        else :
            return None

    def save_statutory_notifications(self, mapping_id, notification_text):
        # client notification
        client_info = self.get_statutory_assigned_to_client(mapping_id)
        # if client_info is None :
        #     return
        old_record = self.get_statutory_mapping_by_id(
            mapping_id
        )
        industry_ids = [
            int(x) for x in old_record["industry_ids"][:-1].split(',')
        ]
        if len(industry_ids) == 1:
            industry_name = self.get_industry_by_id(industry_ids[0])
        else :
            industry_name = self.get_industry_by_id(industry_ids)
        # provision = []
        # for sid in old_record["statutory_ids"][:-1].split(',') :
        #     data = self.get_statutory_by_id(int(sid))
        #     provision.append(data["parent_names"])
        # mappings = ','.join(str(x) for x in provision)
        mappings = old_record["statutory_mapping"]
        geo_map = []
        for gid in old_record["geography_ids"][:-1].split(',') :
            data = self.get_geography_by_id(int(gid))
            if data is not None :
                names = data["parent_names"]
                geo_map.append(names)
        geo_mappings = ','.join(str(x) for x in geo_map)

        notification_id = self.get_new_id(
            "statutory_notification_id",
            "tbl_statutory_notifications_log"
        )
        tbl_statutory_notification = "tbl_statutory_notifications_log"
        columns = [
            "statutory_notification_id", "statutory_mapping_id",
            "country_name", "domain_name", "industry_name",
            "statutory_nature", "statutory_provision",
            "applicable_location", "notification_text"
        ]
        values = [
            notification_id, int(mapping_id),
            old_record["country_name"], old_record["domain_name"],
            industry_name, old_record["statutory_nature_name"],
            mappings, geo_mappings, notification_text
        ]
        self.insert(tbl_statutory_notification, columns, values)
        self.save_statutory_notification_units(notification_id, mapping_id, client_info)

    def save_statutory_notification_units(self, statutory_notification_id, mapping_id, client_info):

        if client_info is not None:
            for r in client_info :
                notification_unit_id = self.get_new_id(
                    "statutory_notification_unit_id",
                    "tbl_statutory_notifications_units"
                )
                business_group = r["business_group_id"]
                division_id = r["division_id"]
                if r["business_group_id"] is None :
                    business_group = 'NULL'
                if r["division_id"] is None :
                    division_id = 'NULL'

                q = "INSERT INTO tbl_statutory_notifications_units \
                    (statutory_notification_unit_id, statutory_notification_id, client_id, \
                        business_group_id, legal_entity_id, division_id, unit_id) VALUES \
                    (%s, %s, %s, '%s', %s, '%s', %s)" % (
                        notification_unit_id,
                        statutory_notification_id,
                        int(r["client_id"]),
                        business_group,
                        int(r["legal_entity_id"]),
                        division_id,
                        int(r["unit_id"])
                    )
                self.execute(q)

    #
    #   Forms
    #
    def get_forms(self):
        columns = "tf.form_id, tf.form_category_id, tfc.form_category, "+\
        "tf.form_type_id, tft.form_type, tf.form_name, tf.form_url, "+\
        "tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormCategory, self.tblFormType]
        aliases = ["tf", "tfc", "tft"]
        join_conditions = ["tf.form_category_id = tfc.form_category_id",
        "tf.form_type_id = tft.form_type_id"]
        where_condition = " tf.form_category_id in (3,2,4) order by tf.form_order"
        join_type = "left join"

        rows = self.get_data_from_multiple_tables(columns, tables, aliases, join_type,
            join_conditions, where_condition)
        return rows

    def return_forms(self, form_ids=None):
        columns = "form_id, form_name"
        condition = " form_id != '26' "
        if form_ids is not None:
            condition += " AND form_id in (%s) " % form_ids
        forms = self.get_data(self.tblForms, columns, condition)
        results = []
        for form in forms:
            results.append(general.AuditTrailForm(form[0], form[1]))
        return results

    def get_form_categories(self):
        columns = "form_category_id, form_category"
        condition = " form_category_id in (2,3)"
        rows = self.get_data(self.tblFormCategory, columns, condition)
        return rows

    #
    #   Admin User Group
    #
    def is_duplicate_user_group_name(self, user_group_id, user_group_name):
        condition = "user_group_name ='%s' AND user_group_id != '%d'"%(
            user_group_name, user_group_id)
        return self.is_already_exists(self.tblUserGroups, condition)

    def generate_new_user_group_id(self) :
        return self.get_new_id("user_group_id", self.tblUserGroups)

    def get_user_group_detailed_list(self) :
        columns = "ug.user_group_id, user_group_name, form_category_id, "+\
                    "form_ids, is_active, (select count(*) from %s u where \
                    ug.user_group_id = u.user_group_id)" % (self.tblUsers)
        tables = self.tblUserGroups+" ug"
        where_condition = " 1 order by user_group_name"
        rows = self.get_data( tables, columns, where_condition)
        return rows

    def get_user_groups(self):
        columns = "user_group_id, user_group_name, is_active"
        where_condition = "1 order by user_group_name"
        rows = self.get_data(self.tblUserGroups, columns, where_condition)
        return rows

    def save_user_group(self, user_group_id, user_group_name,
            form_category_id, form_ids):
        time_stamp = self.get_date_time()
        columns = ["user_group_id", "user_group_name","form_category_id",
                    "form_ids", "is_active", "created_on", "created_by",
                    "updated_on", "updated_by"]
        values =  [user_group_id, user_group_name, form_category_id,
                ",".join(str(x) for x in form_ids), 1, time_stamp,
                0, time_stamp, 0]
        result = self.insert(self.tblUserGroups,columns,values)
        action = "Created User Group \"%s\"" % user_group_name
        self.save_activity(0, 3, action)
        return result

    def update_user_group(self, user_group_id, user_group_name,
            form_category_id, form_ids):
        time_stamp = self.get_date_time()
        columns = ["user_group_name","form_category_id","form_ids", "updated_on",
                 "updated_by"]
        values =  [user_group_name, form_category_id,
                ",".join(str(x) for x in form_ids), time_stamp, 0]
        condition = "user_group_id='%d'" % user_group_id
        action = "Updated User Group \"%s\"" % user_group_name
        self.save_activity(0, 3, action)
        return self.update(self.tblUserGroups, columns, values, condition)

    def update_user_group_status(self, user_group_id, is_active):
        time_stamp = self.get_date_time()
        columns = ["is_active", "updated_by", "updated_on"]
        values = [is_active, 0, time_stamp]
        condition = "user_group_id='%d'" % user_group_id
        result =  self.update(self.tblUserGroups, columns, values, condition)

        action_columns = "user_group_name"
        rows = self.get_data(self.tblUserGroups, action_columns, condition)
        user_group_name = rows[0][0]
        action = ""
        if is_active == 0:
            action = "Deactivated User Group \"%s\"" % user_group_name
        else:
            action = "Activated User Group \"%s\"" % user_group_name
        self.save_activity(0, 3, action)
        return result

    #
    #   Admin User
    #
    def generate_new_user_id(self):
        return self.get_new_id("user_id", self.tblUsers)

    def is_duplicate_email(self, email_id, user_id):
        condition = "email_id ='%s' AND user_id != '%d'" % (
            email_id, user_id)
        return self.is_already_exists(self.tblUsers, condition)

    def is_duplicate_employee_code(self, employee_code, user_id):
        condition = "employee_code ='%s' AND user_id != '%d'" % (
            employee_code, user_id)
        return self.is_already_exists(self.tblUsers, condition)

    def is_duplicate_contact_no(self, contact_no, user_id):
        condition = "contact_no ='%s' AND user_id != '%d'" % (contact_no, user_id)
        return self.is_already_exists(self.tblUsers, condition)

    def get_detailed_user_list(self):
        columns = "user_id, email_id, user_group_id, employee_name, employee_code,"+\
                "contact_no, address, designation, is_active"
        condition = "1"
        rows = self.get_data(self.tblUsers, columns, condition)
        return rows

    def get_users(self, condition = "1"):
        columns = "user_id, employee_name, employee_code, is_active"
        rows = self.get_data(self.tblUsers, columns, condition)
        return rows

    def get_techno_users(self):
        columns = "user_id, concat(employee_code,'-',employee_name), \
        is_active, (select group_concat(country_id) from  %s uc where u.user_id = uc.user_id),\
        (select group_concat(domain_id) from  %s ud where u.user_id = ud.user_id)" % (
            self.tblUserCountries, self.tblUserDomains
        )
        condition = "user_group_id in (select user_group_id from \
             %s where form_category_id = 3 )" % (
                self.tblUserGroups
            )
        rows = self.get_data(self.tblUsers + " u", columns, condition)
        columns = ["user_id", "employee_name", "is_active", "countries", "domains"]
        users = self.convert_to_dict(rows, columns)
        return self.return_techno_users(users)

    def return_techno_users(self, users):
        results = []
        for user in users :
            results.append(
                core.ClientInchargePersons(
                    user["user_id"], user["employee_name"],
                    bool(user["is_active"]), [int(x) for x in user["countries"].split(',')],
                    [int(x) for x in user["domains"].split(",")]
                )
            )
        return results

    def return_users(self, condition = "1"):
        user_rows = self.get_users(condition)
        columns = ["user_id", "employee_name", "employee_code", "is_active"]
        users = self.convert_to_dict(user_rows, columns)
        results = []
        for user in users :
            employee_name = "%s - %s"% (user["employee_code"],user["employee_name"])
            results.append(core.User(
                user["user_id"], employee_name, bool(user["is_active"])
            ))
        return results

    def get_user_countries(self, user_id):
        columns = "group_concat(country_id)"
        condition = " user_id = '%d'"% user_id
        rows = self.get_data( self.tblUserCountries, columns, condition)
        return rows[0][0]

    def get_user_domains(self, user_id):
        columns = "group_concat(domain_id)"
        condition = " user_id = '%d'"% user_id
        rows = self.get_data(self.tblUserDomains, columns, condition)
        return rows[0][0]

    def get_user_clients(self, user_id):
        result = None
        columns = "group_concat(client_id)"
        if user_id > 0:
            table = self.tblUserClients
            condition = " user_id = '%d'"% user_id
        else:
            table = self.tblClientGroups
            condition = "is_active = 1"
        rows = self.get_data(table, columns, condition)
        if rows is not None and len(rows) > 0:
            if rows[0][0] is not None:
                columns = "group_concat(client_id)"
                condition = "client_id in (%s) and is_active = 1" % (rows[0][0])
                rows = self.get_data(self.tblClientGroups, columns, condition)
                if rows:
                    result = rows[0][0]
        return result

    def notify_user(
        self, email_id, password, employee_name, employee_code
    ):
        try:
            email().send_knowledge_user_credentials(
                email_id, password, employee_name, employee_code
            )
        except Exception, e:
            print "Error while sending email : {}".format(e)

    def save_user(self, user_id, email_id, user_group_id, employee_name,
     employee_code, contact_no, address, designation, country_ids, domain_ids):
        result1 = False
        result2 = False
        result3 = False
        current_time_stamp = self.get_date_time()
        user_columns = ["user_id", "email_id", "user_group_id", "password", "employee_name",
                    "employee_code", "contact_no", "is_active",
                    "created_on", "created_by", "updated_on", "updated_by"]
        encrypted_password, password = self.generate_and_return_password()
        user_values = [user_id, email_id, user_group_id, encrypted_password,
                employee_name, employee_code, contact_no,  1,
                current_time_stamp, 0, current_time_stamp, 0]
        if address is not None:
            user_columns.append("address")
            user_values.append(address)
        if designation is not None:
            user_columns.append("designation")
            user_values.append(designation)
        result1 = self.insert(self.tblUsers, user_columns, user_values)

        country_columns = ["user_id", "country_id"]
        country_values_list = []
        for country_id in country_ids:
            country_value_tuple = (user_id, int(country_id))
            country_values_list.append(country_value_tuple)
        result2 = self.bulk_insert(self.tblUserCountries, country_columns, country_values_list)

        domain_columns = ["user_id", "domain_id"]
        domain_values_list = []
        for domain_id in domain_ids:
            domain_value_tuple = (user_id, int(domain_id))
            domain_values_list.append(domain_value_tuple)
        result3 = self.bulk_insert(self.tblUserDomains, domain_columns, domain_values_list)

        action = "Created User \"%s - %s\"" % (employee_code, employee_name)
        self.save_activity(0, 4, action)
        notify_user_thread = threading.Thread(
            target=self.notify_user, args=[
                email_id, password, employee_name, employee_code
            ]
        )
        notify_user_thread.start()
        return (result1 and result2 and result3)

    def update_user(self, user_id, user_group_id, employee_name, employee_code, contact_no,
        address, designation, country_ids, domain_ids):
        result1 = False
        result2 = False
        result3 = False

        current_time_stamp = self.get_date_time()
        user_columns = [ "user_group_id", "employee_name", "employee_code",
                    "contact_no", "address", "designation",
                    "updated_on", "updated_by"]
        user_values = [user_group_id, employee_name, employee_code, contact_no,
                    address, designation, current_time_stamp, 0]
        user_condition = "user_id = '%d'" % user_id
        result1 = self.update(self.tblUsers, user_columns, user_values, user_condition)
        self.delete(self.tblUserCountries, user_condition)
        self.delete(self.tblUserDomains, user_condition)

        country_columns = ["user_id", "country_id"]
        country_values_list = []
        for country_id in country_ids:
            country_value_tuple = (user_id, int(country_id))
            country_values_list.append(country_value_tuple)
        result2 = self.bulk_insert(self.tblUserCountries, country_columns,
            country_values_list)

        domain_columns = ["user_id", "domain_id"]
        domain_values_list = []
        for domain_id in domain_ids:
            domain_value_tuple = (user_id, int(domain_id))
            domain_values_list.append(domain_value_tuple)
        result3 = self.bulk_insert(self.tblUserDomains, domain_columns,
            domain_values_list)

        action = "Updated User \"%s - %s\"" % (employee_code, employee_name)
        self.save_activity(0, 4, action)

        return (result1 and result2 and result3)

    def update_user_status(self, user_id, is_active):
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [is_active, self.get_date_time(), 0]
        condition = "user_id='%d'" % user_id
        result = self.update(self.tblUsers, columns, values, condition)

        action_columns = "employee_name, employee_code"
        rows = self.get_data(self.tblUsers, action_columns, condition)
        employee_name = rows[0][0]
        employee_code = rows[0][1]
        action = ""
        if is_active == 1:
            action = "Activated User \"%s - %s\"" % (employee_code, employee_name)
        else:
            action = "Dectivated User \"%s - %s\"" % (employee_code, employee_name)
        self.save_activity(0, 4, action)
        return result

    #
    #   Group Company
    #
    def generate_new_client_id(self):
        return self.get_new_id("client_id", self.tblClientGroups)

    def is_duplicate_group_name(self, group_name, client_id):
        condition = "group_name ='%s' AND client_id != '%d'" % (group_name, client_id)
        return self.is_already_exists(self.tblClientGroups, condition)

    def is_duplicate_group_username(self, username, client_id):
        condition = "email_id ='%s' AND client_id != '%d'" % (username, client_id)
        return self.is_already_exists(self.tblClientGroups, condition)

    def is_duplicate_short_name(self, short_name, client_id):
        condition = "url_short_name ='%s' AND client_id != '%d'" % (short_name, client_id)
        return self.is_already_exists(self.tblClientGroups, condition)

    def is_unit_exists_under_country(self, country, client_id):
        columns = "count(*)"
        condition = "country_id = '{}' and client_id = '{}'".format(
            country, client_id
        )
        rows = self.get_data(self.tblUnits, columns, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

    def is_unit_exists_under_domain(self, domain, client_id):
        columns = "count(*)"
        condition = "((domain_ids like '{}{}{}') or \
        (domain_ids like '{}{}') or (domain_ids like '{}{}')) and client_id = {}".format(
            "%", domain, "%", domain, "%", "%", domain, client_id
        )
        rows = self.get_data(self.tblUnits, columns, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

    def is_deactivated_existing_country(self, client_id, country_ids):
        existing_countries = self.get_client_countries(client_id)
        existing_countries_list = None
        if existing_countries is not None:
            existing_countries_list = [int(x) for x in existing_countries.split(",")]
        current_countries = [int(x) for x in country_ids]
        for country in existing_countries_list:
            if country not in current_countries:
                if self.is_unit_exists_under_country(country, client_id):
                    return True
                else:
                    continue
            else:
                continue
        return False


    def is_deactivated_existing_domain(self, client_id, domain_ids):
        existing_domains = self.get_client_domains(client_id)
        existing_domains_list = None
        if existing_domains is not None:
            existing_domains_list = [int(x) for x in existing_domains.split(",")]
        current_domains = [int(x) for x in domain_ids]
        for domain in existing_domains_list:
            if domain not in current_domains:
                if self.is_unit_exists_under_domain(domain, client_id):
                    return True
                else:
                    continue
            else:
                continue
        return False

    def get_group_company_details(self):
        columns = "client_id, group_name, email_id, logo_url,  contract_from, contract_to,"+\
        " no_of_user_licence, total_disk_space, is_sms_subscribed,  incharge_persons,"+\
        " is_active, url_short_name"
        condition = "1 ORDER BY group_name"
        rows = self.get_data(self.tblClientGroups, columns, condition)
        return self.return_group_company_details(rows)

    def return_group_company_details(self, result):
        client_list = []
        for client_row in result:
            client_id = client_row[0]
            group_name = client_row[1]
            email_id = client_row[2]
            file_parts = client_row[3].split("-")
            etn_parts = client_row[3].split(".")
            original_file_name = "%s.%s" % (file_parts[0], etn_parts[1])
            logo_url = "/%s/%s" % (LOGO_URL, client_row[3])
            contract_from = self.datetime_to_string(client_row[4])
            contract_to  = self.datetime_to_string(client_row[5])
            no_of_user_licence = client_row[6]
            total_disk_space = client_row[7] / 1000000000
            is_sms_subscribed = True if client_row[8]==1 else False
            incharge_persons = [int(x) for x in client_row[9].split(",")]
            is_active = True if client_row[10]==1 else False
            short_name = client_row[11]
            client_countries = self.get_client_countries(client_id)
            country_ids = None if client_countries is None else [int(x) for x in client_countries.split(",")]
            client_domains = self.get_client_domains(client_id)
            domain_ids = None if client_domains is None else [int(x) for x in client_domains.split(",")]
            date_configurations = self.get_date_configurations(client_id)
            client_list.append(core.GroupCompanyDetail(client_id, group_name, domain_ids,
                country_ids, incharge_persons, original_file_name, logo_url, contract_from,
                contract_to, no_of_user_licence, total_disk_space, is_sms_subscribed, email_id,
                is_active, short_name, date_configurations))
        return client_list

    def get_group_companies_for_user(self, user_id):
        result = {}
        client_ids = None
        if user_id != None:
            client_ids = self.get_user_clients(user_id)
        columns = "client_id, group_name, is_active"
        condition = "is_active=1"
        if client_ids is not None:
            condition = "client_id in (%s) order by group_name ASC" % client_ids
            rows = self.get_data(self.tblClientGroups, columns, condition)
            columns = ["client_id", "group_name", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return self.return_group_companies(result)

    def return_group_companies(self, group_companies):
        results = []
        for group_company in group_companies :
            client_countries = self.get_client_countries(group_company["client_id"])
            countries = None if client_countries is None else [int(x) for x in client_countries.split(",")]
            client_domains = self.get_client_domains(group_company["client_id"])
            domains = None if client_domains is None else [int(x) for x in client_domains.split(",")]
            results.append(core.GroupCompany(
                group_company["client_id"], group_company["group_name"],
                bool(group_company["is_active"]), countries, domains
            ))
        return results

    def get_group_companies_for_user_with_max_unit_count(self, user_id):
        result = {}
        client_ids = None
        if user_id != None:
            client_ids = self.get_user_clients(user_id)
        columns = "client_id, group_name, is_active"
        condition = "is_active=1"
        if client_ids is not None:
            condition = "client_id in (%s) order by group_name ASC" % client_ids
            rows = self.get_data(self.tblClientGroups, columns, condition)
            columns = ["client_id", "group_name", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return self.return_group_companies_with_max_unit_count(result)

    def return_group_companies_with_max_unit_count(self, group_companies):
        results = []
        for group_company in group_companies :
            client_countries = self.get_client_countries(group_company["client_id"])
            countries = None if client_countries is None else [int(x) for x in client_countries.split(",")]
            client_domains = self.get_client_domains(group_company["client_id"])
            domains = None if client_domains is None else [int(x) for x in client_domains.split(",")]

            columns = "count(*)"
            condition = "client_id = '%d'" % group_company["client_id"]
            rows = self.get_data(self.tblUnits, columns, condition)
            no_of_units = rows[0][0]
            group_name = group_company["group_name"].replace(" ", "")
            unit_code_start_letters = group_name[:2].upper()

            columns = "TRIM(LEADING '%s' FROM unit_code)" % unit_code_start_letters
            condition = "unit_code like binary '%s%s' and CHAR_LENGTH(unit_code) = 7 and client_id='%d'" % (
                unit_code_start_letters, "%", group_company["client_id"]
            )
            rows = self.get_data(self.tblUnits, columns, condition)
            auto_generated_unit_codes = []
            for row in rows:
                try:
                    auto_generated_unit_codes.append(int(row[0]))
                except Exception, ex:
                    continue
            next_auto_gen_no = 1
            if len(auto_generated_unit_codes) > 0:
                existing_max_unit_code = max(auto_generated_unit_codes)
                if existing_max_unit_code == no_of_units:
                    next_auto_gen_no = no_of_units + 1
                else:
                    next_auto_gen_no = existing_max_unit_code + 1

            results.append(core.GroupCompanyForUnitCreation(
                group_company["client_id"], group_company["group_name"],
                bool(group_company["is_active"]), countries, domains,
                next_auto_gen_no
            ))
        return results

    def get_next_unit_auto_gen_no(self, client_id):
        columns = "count(*)"
        condition = "client_id = '%d'" % client_id
        rows = self.get_data(self.tblUnits, columns, condition)
        no_of_units = rows[0][0]

        group_columns = "group_name"
        group_condition = "client_id = '%d'" % client_id
        group_company = self.get_data(self.tblClientGroups, group_columns, group_condition)

        group_name = group_company[0][0].replace(" ", "")
        unit_code_start_letters = group_name[:2].upper()

        columns = "TRIM(LEADING '%s' FROM unit_code)" % unit_code_start_letters
        condition = "unit_code like binary '%s%s' and CHAR_LENGTH(unit_code) = 7 and client_id='%d'" % (
            unit_code_start_letters, "%", client_id
        )
        rows = self.get_data(self.tblUnits, columns, condition)
        auto_generated_unit_codes = []
        for row in rows:
            try:
                auto_generated_unit_codes.append(int(row[0]))
            except Exception, ex:
                print ex
                continue
        next_auto_gen_no = 1
        if len(auto_generated_unit_codes) > 0:
            existing_max_unit_code = max(auto_generated_unit_codes)
            if existing_max_unit_code == no_of_units:
                next_auto_gen_no = no_of_units + 1
            else:
                next_auto_gen_no = existing_max_unit_code + 1
        unit_code = group_name[:2].upper()
        if len(str(next_auto_gen_no)) == 1:
            unit_code += "0000"
        elif len(str(next_auto_gen_no)) == 2:
            unit_code += "000"
        elif len(str(next_auto_gen_no)) == 3:
            unit_code += "00"
        elif len(str(next_auto_gen_no)) == 4:
            unit_code += "0"
        unit_code += "%d" % (next_auto_gen_no)
        return unit_code

    def get_client_countries(self, client_id):
        columns = "group_concat(country_id)"
        condition = "client_id ='%d'" % client_id
        rows = self.get_data(self.tblClientCountries, columns, condition)
        return rows[0][0]

    def get_client_domains(self, client_id):
        columns = "group_concat(domain_id)"
        condition = "client_id ='%d'" % client_id
        rows = self.get_data(self.tblClientDomains, columns, condition)
        return rows[0][0]

    def get_date_configurations(self, client_id):
        columns = "country_id, domain_id, period_from, period_to"
        condition = "client_id='%d'"%client_id
        rows = self.get_data(self.tblClientConfigurations, columns, condition)
        columns = ["country_id" ,"domain_id", "period_from", "period_to"]
        result = self.convert_to_dict(rows, columns)
        return self.return_client_configuration(result)

    def return_client_configuration(self, configurations):
        results = []
        for configuration in configurations :
            results.append(core.ClientConfiguration(
                configuration["country_id"], configuration["domain_id"],
                configuration["period_from"], configuration["period_to"]
            ))
        return results

    def save_date_configurations(self, client_id, date_configurations, session_user):
        current_time_stamp = self.get_date_time()
        insert_columns = ["client_config_id", "client_id", "country_id" ,"domain_id", "period_from",
        "period_to", "updated_by", "updated_on"]
        update_columns = ["period_from", "period_to"]
        for configuration in date_configurations:
            country_id = configuration.country_id
            domain_id = configuration.domain_id
            period_from = configuration.period_from
            period_to = configuration.period_to
            if self.is_combination_already_exists(country_id, domain_id, client_id):
                update_values = [period_from, period_to]
                update_condition = " client_id = '%d' AND country_id = '%d' \
                AND domain_id = '%d'" % (
                    client_id, country_id, domain_id
                )
                self.update(
                    self.tblClientConfigurations, update_columns, update_values, update_condition
                )
            else:
                client_config_id = self.get_new_id(
                    "client_config_id", self.tblClientConfigurations
                )
                insert_values = [
                    client_config_id, client_id, country_id,
                    domain_id, period_from, period_to, session_user, current_time_stamp
                ]
                self.insert(
                    self.tblClientConfigurations, insert_columns, insert_values
                )

    def is_combination_already_exists(
        self, country_id, domain_id, client_id
    ):
        columns = "count(*)"
        condition = " client_id = '%d' AND country_id = '%d' \
                AND domain_id = '%d'" % (
                    client_id, country_id, domain_id
                )
        rows = self.get_data(self.tblClientConfigurations, columns, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

    def save_client_countries(self, client_id, country_ids):
        values_list = []
        columns = ["client_id", "country_id"]
        condition = "client_id = '%d'" % client_id
        self.delete(self.tblClientCountries, condition)
        for country_id in country_ids:
            # client_country_id = self.get_new_id(
            #     "client_country_id", self.tblClientCountries
            # )
            values_tuple = (client_id, country_id)
            values_list.append(values_tuple)
        return self.bulk_insert(self.tblClientCountries, columns, values_list)

    def save_client_domains(self, client_id, domain_ids):
        values_list = []
        columns = ["client_id", "domain_id"]
        condition = "client_id = '%d'" % client_id
        self.delete(self.tblClientDomains, condition)
        for domain_id in domain_ids:
            # client_domain_id = self.get_new_id(
            #     "client_domain_id", self.tblClientDomains
            # )
            values_tuple = (client_id, domain_id)
            values_list.append(values_tuple)
        return self.bulk_insert(self.tblClientDomains, columns, values_list)

    def replicate_client_countries_and_domains(self, client_id, country_ids, domain_ids):
        rows = self.get_client_db_info(client_id)

        ip = rows[0][0]
        username = rows[0][2]
        password = rows[0][3]
        dbname = rows[0][4]

        conn = self._db_connect(ip, username, password, dbname)
        cursor = conn.cursor()

        delete_countries_query = "delete from tbl_countries"
        delete_domains_query = "delete from tbl_domains"

        cursor.execute(delete_countries_query)
        cursor.execute(delete_domains_query)

        columns = "CAST(country_id as UNSIGNED), country_name, is_active"
        condition = "country_id in (%s)" %','.join(str(x) for x in country_ids)
        country_rows = self.get_data(self.tblCountries, columns, condition)

        country_values_list = []
        for country in country_rows:
            country_values_tuple = (int(country[0]), country[1], country[2])
            country_values_list.append(country_values_tuple)

        columns = "CAST(domain_id as UNSIGNED), domain_name, is_active"
        condition = "domain_id in (%s)" %','.join(str(x) for x in domain_ids)
        domain_rows = self.get_data(self.tblDomains, columns, condition)

        domain_values_list = []
        for domain in domain_rows:
            domain_values_tuple = (int(domain[0]), domain[1], domain[2])
            domain_values_list.append(domain_values_tuple)

        insert_countries_query = '''INSERT INTO tbl_countries \
        VALUES %s''' % ','.join(str(x) for x in country_values_list)

        insert_domains_query = '''INSERT INTO tbl_domains \
        VALUES %s''' % ','.join(str(x) for x in domain_values_list)

        cursor.execute(insert_countries_query)
        cursor.execute(insert_domains_query)
        conn.commit()
        return True

    def _mysql_server_connect(self, host, username, password):
        return mysql.connect(host, username, password)

    def _db_connect(self, host, username, password, database):
        return mysql.connect(host, username, password,
            database)

    def delete_database(
        self, host, database_name, username, password,
    ):
        con = self._mysql_server_connect(host, username, password)
        cursor = con.cursor()
        query = "DROP DATABASE IF EXISTS %s" % database_name
        cursor.execute(query)
        con.commit()

    def _create_database(
        self, host, username, password,
        database_name, db_username, db_password, email_id, client_id,
        short_name, country_ids, domain_ids
    ):
        client_con = self._mysql_server_connect(host, username, password)
        client_cursor = client_con.cursor()
        query = "CREATE DATABASE %s" % database_name
        print query
        client_cursor.execute(query)
        query = "GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, REFERENCES, \
            TRIGGER, EVENT, CREATE ROUTINE, aLTER  on %s.* to %s@%s IDENTIFIED BY '%s';" % (
            database_name, db_username, host, db_password)
        print query
        print "priv crossed"
        client_cursor.execute(query)
        client_cursor.execute("FLUSH PRIVILEGES;")
        client_con.commit()
        print "connection begin"
        client_db_con = self._db_connect(host, username, password, database_name)
        client_db_cursor = client_db_con.cursor()
        sql_script_path = os.path.join(
            os.path.join(os.path.split(__file__)[0]),
            "scripts/mirror-client.sql"
        )
        file_obj = open(sql_script_path, 'r')
        sql_file = file_obj.read()
        file_obj.close()
        sql_commands = sql_file.split(';')
        size = len(sql_commands)
        for index, command in enumerate(sql_commands):
            if (index < size-1):
                client_db_cursor.execute(command)
            else:
                break
        encrypted_password, password = self.generate_and_return_password()
        query = "insert into tbl_admin (username, password) values ('%s', '%s')" % (
            email_id, encrypted_password)
        client_db_cursor.execute(query)
        query = "insert into tbl_users (user_id, employee_name, email_id, password, user_level,\
        is_primary_admin, is_service_provider, is_admin)\
        values (0, 'Administrator', '%s', '%s', 1 , 1, 0, 0 )" % (
            email_id, encrypted_password)
        client_db_cursor.execute(query)
        self._save_client_countries(country_ids, client_db_cursor)
        self._save_client_domains(domain_ids, client_db_cursor)
        self._create_procedure(client_db_cursor)
        print "trigger created"
        self._create_trigger(client_db_cursor)
        print "close connection"
        client_db_con.commit()
        return password

    def _save_client_countries(self, country_ids, cursor):
        q = "SELECT country_id, country_name, is_active \
                FROM tbl_countries\
                WHERE country_id\
                IN (%s) " % (country_ids)
        rows = self.select_all(q)
        for r in rows :
            q = " INSERT INTO tbl_countries VALUES (%s, '%s', %s)" % (
                int(r[0]), r[1], int(r[2])
            )
            cursor.execute(q)

    def _save_client_domains(self, domain_ids, cursor):
        q = "SELECT domain_id, domain_name, is_active \
                FROM tbl_domains\
                WHERE domain_id\
                IN (%s)" % (domain_ids)
        rows = self.select_all(q)
        for r in rows :
            q = " INSERT INTO tbl_domains VALUES (%s, '%s', %s)" % (
                int(r[0]), r[1], int(r[2])
            )
            cursor.execute(q)

    def _create_procedure(self, cursor):
        p1 = "CREATE PROCEDURE `procedure_to_update_version` (IN update_type VARCHAR(100))\
            BEGIN \
                SET SQL_SAFE_UPDATES=0;\
                case \
                    when update_type = 'unit' then \
                    SET @count = (SELECT unit_details_version+1 FROM tbl_mobile_sync_versions ); \
                    update tbl_mobile_sync_versions set unit_details_version = @count; \
                    when update_type = 'user' then \
                    SET @count = (SELECT user_details_version+1 FROM tbl_mobile_sync_versions ); \
                    update tbl_mobile_sync_versions set user_details_version = @count; \
                    when update_type = 'compliance' then \
                    SET @count = (SELECT compliance_applicability_version+1 FROM tbl_mobile_sync_versions ); \
                    update tbl_mobile_sync_versions set compliance_applicability_version = @count; \
                    when update_type = 'history' then \
                    SET @count = (SELECT compliance_history_version+1 FROM tbl_mobile_sync_versions ); \
                    update tbl_mobile_sync_versions set compliance_history_version = @count; \
                end case; \
                SET SQL_SAFE_UPDATES=1; \
            END "
        cursor.execute(p1)

    def _create_trigger(self, cursor):
        t1 = "CREATE TRIGGER `after_tbl_statutory_notifications_units_insert` AFTER INSERT ON `tbl_statutory_notifications_units` \
            FOR EACH ROW BEGIN \
                INSERT INTO tbl_statutory_notification_status ( \
                statutory_notification_id, \
                user_id, read_status) \
                SELECT NEW.statutory_notification_id, t1.user_id, 0 \
                FROM tbl_user_units t1 where t1.unit_id = NEW.unit_id; \
                \
                INSERT INTO tbl_statutory_notification_status ( \
                    statutory_notification_id, \
                    user_id, read_status \
                ) \
                SELECT NEW.statutory_notification_id, t1.admin_id, 0 FROM \
                tbl_admin t1 where t1.admin_id != 0; \
            END; "
        cursor.execute(t1)
        t2 = " CREATE TRIGGER `after_tbl_units_insert` AFTER INSERT ON `tbl_units` \
            FOR EACH ROW BEGIN \
                CALL procedure_to_update_version('unit'); \
            END; "
        cursor.execute(t2)
        t3 = "CREATE TRIGGER `after_tbl_units_update` AFTER UPDATE ON `tbl_units` \
            FOR EACH ROW BEGIN \
                CALL procedure_to_update_version('unit'); \
            END; "
        cursor.execute(t3)
        t4 = "CREATE TRIGGER `after_tbl_users_update` AFTER UPDATE ON `tbl_users` \
            FOR EACH ROW BEGIN \
                CALL procedure_to_update_version('user'); \
            END; "
        cursor.execute(t4)
        t5 = "CREATE TRIGGER `after_tbl_users_insert` AFTER INSERT ON `tbl_users` \
            FOR EACH ROW BEGIN \
                CALL procedure_to_update_version('user'); \
            END; "
        cursor.execute(t5)
        t6 = "CREATE TRIGGER `after_tbl_compliance_history_insert` AFTER INSERT ON `tbl_compliance_history` \
            FOR EACH ROW BEGIN \
                CALL procedure_to_update_version('history'); \
            END; "
        cursor.execute(t6)
        t7 = "CREATE TRIGGER `after_tbl_compliance_history_update` AFTER UPDATE ON `tbl_compliance_history` \
            FOR EACH ROW BEGIN \
                CALL procedure_to_update_version('history'); \
            END; "
        cursor.execute(t7)
        t8 = "CREATE TRIGGER `after_tbl_client_compliances_update` AFTER UPDATE ON `tbl_client_compliances` \
            FOR EACH ROW BEGIN \
                CALL procedure_to_update_version('compliance'); \
            END; "
        cursor.execute(t8)
        t9 = "CREATE TRIGGER `after_tbl_client_compliances_insert` AFTER INSERT ON `tbl_client_compliances` \
            FOR EACH ROW BEGIN \
                CALL procedure_to_update_version('compliance'); \
            END; "
        cursor.execute(t9)

    def _get_server_details(self):
        columns = "ip, server_username,server_password, port"
        condition = "server_full = 0 order by length ASC limit 1"
        rows = self.get_data(self.tblDatabaseServer, columns, condition)
        return rows

    def _get_machine_details(self):
        columns = "machine_id, ip, port"
        condition = "server_full = 0 limit 1"
        rows = self.get_data(self.tblMachines, columns, condition)
        return rows

    def create_and_save_client_database(
        self, host, username, password, database_name, db_username,
        db_password, email_id, client_id, short_name
    ):
        result = self._create_database(
            host, username, password, database_name, db_username,
            db_password, email_id, client_id, short_name
        )
        return result

    def set_server_full(self, db_server_condition):
        columns = ["server_full"]
        values = [1]
        self.update(self.tblDatabaseServer, columns, values, db_server_condition)
        self.update(self.tblMachines, columns, values, db_server_condition)

    def update_client_db_details(self, host, client_id, db_username,
            db_password, short_name, database_name, db_port):
        db_server_column = "company_ids"
        db_server_value = client_id

        db_server_condition = "ip = '%s'" % str(host)

        self.append(
            self.tblDatabaseServer, db_server_column, db_server_value,
            db_server_condition
        )
        db_server_column = "length"
        self.increment(
            self.tblDatabaseServer, db_server_column,
            db_server_condition
        )

        result = self._get_machine_details()
        machine_id = result[0][0]
        server_ip = result[0][1]
        server_port = result[0][2]
        machine_columns = "client_ids"
        machine_value = client_id
        machine_condition = "ip='%s'" % server_ip
        self.append(
            self.tblMachines, machine_columns, machine_value,
            machine_condition
        )

        client_db_columns = [
            "client_id", "machine_id", "database_ip",
            "database_port", "database_username", "database_password",
            "client_short_name", "database_name",
            "server_ip", "server_port"
        ]
        client_dB_values = [
            client_id, machine_id, host, db_port, db_username,
            db_password, short_name, database_name,
            server_ip, server_port
        ]
        length_rows = self.get_data(
            self.tblDatabaseServer, db_server_column,
            db_server_condition
        )
        if length_rows[0][0] >= 30:
            self.set_server_full(db_server_condition)
        return self.insert(
            self.tblClientDatabase, client_db_columns,
            client_dB_values
        )

    def save_client_group(self, client_id, client_group, session_user):
        current_time_stamp = self.get_date_time()
        contract_from = self.string_to_datetime(client_group.contract_from)
        contract_to = self.string_to_datetime(client_group.contract_to)
        is_sms_subscribed = 0 if client_group.is_sms_subscribed == False else 1

        columns = ["client_id", "group_name", "email_id", "logo_url",
        "logo_size", "contract_from", "contract_to", "no_of_user_licence",
        "total_disk_space", "is_sms_subscribed", "url_short_name",
        "incharge_persons", "is_active", "created_by", "created_on",
        "updated_by", "updated_on"]
        file_name = self.save_client_logo(client_group.logo, client_id)
        values = [client_id, client_group.group_name, client_group.email_id,
        file_name, client_group.logo.file_size, contract_from, contract_to,
        client_group.no_of_user_licence, client_group.file_space * 1000000000,
        is_sms_subscribed, client_group.short_name,
        ','.join(str(x) for x in client_group.incharge_persons),1, session_user,
        current_time_stamp, session_user, current_time_stamp]
        result = self.insert(self.tblClientGroups, columns, values)
        action = "Created Client \"%s\"" % client_group.group_name
        self.save_activity(session_user, 18, action)
        return result

    def update_client_group(self, client_group, session_user):
        current_time_stamp = self.get_date_time()
        contract_from = self.string_to_datetime(client_group.contract_from)
        contract_to = self.string_to_datetime(client_group.contract_to)
        is_sms_subscribed = 0 if client_group.is_sms_subscribed == False else 1

        columns = [
            "group_name", "contract_from", "contract_to", "no_of_user_licence",
            "total_disk_space", "is_sms_subscribed", "incharge_persons",
            "updated_by", "updated_on"
        ]
        values = [
            client_group.group_name, contract_from, contract_to,
            client_group.no_of_user_licence, client_group.file_space * 1000000000,
            is_sms_subscribed,
            ','.join(str(x) for x in client_group.incharge_persons), session_user,
            current_time_stamp
        ]
        if client_group.logo is not None:
            columns.append("logo_url")
            columns.append("logo_size")
            file_name = self.update_client_logo(client_group.logo, client_group.client_id)
            values.append(file_name)
            values.append(client_group.logo.file_size)

        condition = "client_id = '%d'" % client_group.client_id

        action = "Updated Client \"%s\"" % client_group.group_name
        self.save_activity(session_user, 18, action)

        return self.update(self.tblClientGroups, columns, values, condition)

    def save_client_user(self, client_group, session_user, client_id = None):
        if client_id is None:
            client_id = client_group.client_id
        columns = ["client_id", "user_id",  "email_id",
        "employee_name", "created_on", "is_primary_admin", "is_active"]
        values = [client_id, 0, client_group.email_id, "Admin",
        self.get_date_time(), 1, 1]
        return self.insert(self.tblClientUsers, columns, values)

    def save_incharge_persons(self, client_group, client_id):
        columns = ["client_id", "user_id"]
        values_list = []
        condition = "client_id='%d'" % client_id
        self.delete(self.tblUserClients, condition)
        for incharge_person in client_group.incharge_persons:
            values_tuple = (client_id, incharge_person)
            values_list.append(values_tuple)
        return self.bulk_insert(self.tblUserClients, columns, values_list)

    def notify_incharge_persons(self, client_group):
        notification_text = "Client %s has been assigned" % client_group.group_name
        link = "/knowledge/client-unit"
        notification_id = self.get_new_id(
            "notification_id", "tbl_notifications"
        )
        query = "INSERT INTO tbl_notifications \
            (notification_id, notification_text, link) \
            VALUES (%s, '%s', '%s')" % (
                notification_id, notification_text, link
            )
        self.execute(query)
        columns = ["notification_id", "user_id", "read_status"]
        values_list = []
        for incharge_person in client_group.incharge_persons:
            values_tuple = (notification_id, incharge_person, 0)
            values_list.append(values_tuple)
        return self.bulk_insert(
            self.tblNotificationsStatus, columns, values_list
        )

    def save_client_logo(self, logo, client_id):
        file_size = logo.file_size
        name = logo.file_name.split('.')[0]
        exten = logo.file_name.split('.')[1]
        auto_code = self.new_uuid()
        file_name = "%s-%s.%s" % (name, auto_code, exten)
        self.convert_base64_to_file(file_name, logo.file_content, CLIENT_LOGO_PATH)
        return file_name

    def update_client_logo(self, logo, client_id):
        column = "logo_url"
        condition = "client_id = '%d'" % client_id
        rows = self.get_data(self.tblClientGroups, column, condition)
        old_file_name = rows[0][0]
        old_file_path = "%s/%s" % (CLIENT_LOGO_PATH, old_file_name)
        self.remove_uploaded_file(old_file_path)
        return self.save_client_logo(logo, client_id)

    def update_client_group_status(self, client_id, is_active, session_user):
        is_active = 1 if is_active != False else 0
        columns = ["is_active", "updated_by", "updated_on"]
        values = [ is_active, int(session_user), self.get_date_time()]
        condition = "client_id='%d'" % client_id

        action = ""
        action_columns = "group_name"
        rows = self.get_data(self.tblClientGroups, action_columns, condition)
        group_name = rows[0][0]
        if is_active == 1:
            action = "Activated Client \"%s\"" % group_name
        else:
            action = "Deactivated Client \"%s\"" % group_name
        self.save_activity(session_user, 18, action)

        return self.update(self.tblClientGroups, columns, values, condition)

#
#   Client Unit
#

    def generate_new_business_group_id(self) :
        return self.get_new_id("business_group_id", self.tblBusinessGroups)

    def generate_new_legal_entity_id(self) :
        return self.get_new_id("legal_entity_id", self.tblLegalEntities)

    def generate_new_division_id(self) :
        return self.get_new_id("division_id", self.tblDivisions)

    def generate_new_unit_id(self) :
        return self.get_new_id("unit_id", self.tblUnits)

    def is_duplicate_business_group(self, business_group_id, business_group_name, client_id):
        condition = "business_group_name ='%s' AND business_group_id != '%d' and client_id = '%d'" % (
            business_group_name, business_group_id, client_id)
        return self.is_already_exists(self.tblBusinessGroups, condition)

    def is_duplicate_legal_entity(self, legal_entity_id, legal_entity_name, client_id):
        condition = "legal_entity_name ='%s' AND legal_entity_id != '%d' and client_id = '%d'" % (
            legal_entity_name, legal_entity_id, client_id)
        return self.is_already_exists(self.tblLegalEntities, condition)

    def is_duplicate_division(self, division_id, division_name, client_id):
        condition = "division_name ='%s' AND division_id != '%d' and client_id = '%d'" % (
            division_name, division_id, client_id)
        return self.is_already_exists(self.tblDivisions, condition)

    def is_duplicate_unit_name(self, unit_id, unit_name, client_id):
        condition = "unit_name ='%s' AND unit_id != '%d' and client_id = '%d'" % (
            unit_name, unit_id, client_id)
        return self.is_already_exists(self.tblUnits, condition)

    def is_duplicate_unit_code(self, unit_id, unit_code, client_id):
        condition = "unit_code ='%s' AND unit_id != '%d' and client_id = '%d'" % (
            unit_code, unit_id, client_id)
        return self.is_already_exists(self.tblUnits, condition)

    def save_business_group(self, client_id, business_group_id, business_group_name,
        session_user):
        current_time_stamp = self.get_date_time()
        columns = ["client_id", "business_group_id", "business_group_name",
        "created_by", "created_on", "updated_by", "updated_on"]
        values = [client_id, business_group_id, business_group_name, session_user, current_time_stamp,
        session_user, current_time_stamp]
        result = self.insert(self.tblBusinessGroups, columns, values)

        action = "Created Business Group \"%s\"" % business_group_name
        self.save_activity(session_user, 19, action)

        return result

    def update_business_group(self, client_id, business_group_id, business_group_name,
        session_user):
        current_time_stamp = self.get_date_time()
        columns = ["business_group_name", "updated_by", "updated_on"]
        values = [business_group_name, session_user, current_time_stamp]
        condition = "business_group_id = '%d' and client_id = '%d'"%(business_group_id, client_id)
        result = self.update(self.tblBusinessGroups, columns, values, condition)

        action = "Updated Business Group \"%s\"" % business_group_name
        self.save_activity(session_user, 19, action)

        return result

    def save_legal_entity(self, client_id, legal_entity_id, legal_entity_name,
        business_group_id, session_user):
        current_time_stamp = self.get_date_time()
        columns = ["client_id", "legal_entity_id", "legal_entity_name",
        "created_by", "created_on", "updated_by", "updated_on"]
        values = [client_id, legal_entity_id, legal_entity_name,
        session_user, current_time_stamp, session_user, current_time_stamp]

        if business_group_id is not None:
            columns.append("business_group_id")
            values.append(business_group_id)

        result = self.insert(self.tblLegalEntities, columns, values)
        action = "Created Legal Entity \"%s\"" % legal_entity_name
        self.save_activity(session_user, 19, action)
        return result

    def update_legal_entity(self, client_id, legal_entity_id, legal_entity_name, business_group_id, session_user):
        current_time_stamp = self.get_date_time()
        columns = ["legal_entity_name", "updated_by", "updated_on"]
        values = [legal_entity_name, session_user, self.get_date_time()]
        condition = "legal_entity_id = '%d' and client_id = '%d'"%(legal_entity_id, client_id)
        result = self.update(self.tblLegalEntities, columns, values, condition)

        action = "Updated Legal Entity \"%s\"" % legal_entity_name
        self.save_activity(session_user, 19, action)

        return result

    def save_division(self, client_id, division_id, division_name, business_group_id,
        legal_entity_id, session_user):
        current_time_stamp = self.get_date_time()
        columns = ["client_id", "division_id", "division_name", "legal_entity_id",
        "created_by", "created_on", "updated_by", "updated_on"]
        values = [client_id, division_id, division_name, legal_entity_id,
        session_user, current_time_stamp, session_user, current_time_stamp]

        if business_group_id is not None:
            columns.append("business_group_id")
            values.append(business_group_id)

        result = self.insert(self.tblDivisions, columns, values)
        action = "Created Division \"%s\"" % division_name
        self.save_activity(session_user, 19, action)

        return result

    def update_division(self, client_id, division_id, division_name, business_group_id, legal_entity_id, session_user):
        current_time_stamp = self.get_date_time()
        columns = ["division_name", "updated_by", "updated_on"]
        values = [division_name, session_user, current_time_stamp]
        condition = "division_id = '%d' and client_id = '%d'"%(division_id, client_id)
        result = self.update(self.tblDivisions, columns, values, condition)

        action = "Updated Division \"%s\"" % division_name
        self.save_activity(session_user, 19, action)

        return result

    def save_unit(self, client_id,  units, business_group_id, legal_entity_id, division_id, session_user):
        current_time_stamp = str(self.get_date_time())
        columns = ["unit_id", "client_id", "legal_entity_id", "country_id", "geography_id", "industry_id",
        "domain_ids", "unit_code", "unit_name", "address", "postal_code", "is_active", "created_by",
        "created_on", "updated_by", "updated_on"]
        if business_group_id is not None:
            columns.append("business_group_id")
        if division_id is not None:
            columns.append("division_id")
        values_list = []
        unit_names = []
        for unit in units:
            domain_ids = ",".join(str(x) for x in unit.domain_ids)
            if business_group_id != None and division_id is not None:
                values_tuple = (str(unit.unit_id), client_id, legal_entity_id, str(unit.country_id), str(unit.geography_id),
                    str(unit.industry_id), domain_ids, str(unit.unit_code).upper(), str(unit.unit_name), str(unit.unit_address),
                    str(unit.postal_code), 1, session_user, current_time_stamp, session_user, current_time_stamp,
                    business_group_id, division_id)
            elif business_group_id is not None:
                values_tuple = (str(unit.unit_id), client_id, legal_entity_id, str(unit.country_id), str(unit.geography_id),
                    str(unit.industry_id), domain_ids, str(unit.unit_code).upper(), str(unit.unit_name), str(unit.unit_address),
                    str(unit.postal_code), 1, session_user, current_time_stamp, session_user, current_time_stamp,
                    business_group_id)
            elif division_id != None :
                values_tuple = (str(unit.unit_id), client_id, legal_entity_id, str(unit.country_id), str(unit.geography_id),
                    str(unit.industry_id), domain_ids, str(unit.unit_code).upper(), str(unit.unit_name), str(unit.unit_address),
                    str(unit.postal_code), 1, session_user, current_time_stamp, session_user, current_time_stamp,
                    division_id)
            else:
                values_tuple = (str(unit.unit_id), client_id, legal_entity_id, str(unit.country_id), str(unit.geography_id),
                        str(unit.industry_id), domain_ids, str(unit.unit_code).upper(), str(unit.unit_name), str(unit.unit_address),
                        str(unit.postal_code), 1, session_user, current_time_stamp, session_user, current_time_stamp)
            values_list.append(values_tuple)
            unit_names.append("\"%s - %s\"" % (str(unit.unit_code).upper(), unit.unit_name))
        result = self.bulk_insert(self.tblUnits, columns, values_list)

        action = "Created following Units %s" % (",".join(unit_names))
        self.save_activity(session_user, 19, action)

        return result


    def update_unit(self, client_id,  units, business_group_id, legal_entity_id, division_id, session_user):
        current_time_stamp = str(self.get_date_time())
        columns = ["country_id", "geography_id", "industry_id", "domain_ids", "unit_code", "unit_name",
        "address", "postal_code", "updated_by", "updated_on"]
        values_list = []
        for unit in units:
            domain_ids = ",".join(str(x) for x in unit.domain_ids)
            values= [unit.country_id, unit.geography_id,unit.industry_id, domain_ids,
                        str(unit.unit_code), str(unit.unit_name), str(unit.unit_address),
                        str(unit.postal_code), session_user, current_time_stamp]
            condition = "client_id='%d' and unit_id = '%d'" % (client_id, unit.unit_id)
            self.update(self.tblUnits, columns, values, condition)

        action = "Updated Unit \"%s - %s\"" % (unit.unit_code, unit.unit_name)
        self.save_activity(session_user, 19, action)

        return True

    def change_client_status(self, client_id, legal_entity_id, division_id, is_active, session_user):
        current_time_stamp = str(self.get_date_time())
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [is_active, current_time_stamp, session_user]
        condition = "legal_entity_id = '%d' and client_id = '%d' "% (legal_entity_id, client_id)
        self.update(self.tblUnits, columns, values, condition)

        division_name = None
        legal_entity_name = None
        rows = None
        if division_id is not None:
            condition += " and division_id='%d' "% division_id
            action_column = "division_name"
            action_condition = "division_id='%d' and client_id = '%d' "% (division_id, client_id)
            rows = self.get_data(self.tblDivisions, action_column, action_condition)
            division_name = rows[0][0]
        else:
            action_column = "legal_entity_name"
            action_condition = "legal_entity_id='%d' and client_id = '%d' "% (legal_entity_id, client_id)
            rows = self.get_data(self.tblLegalEntities, action_column, action_condition)
            legal_entity_name = rows[0][0]

        if is_active == 0:
            if division_id is not None:
                action = "Deactivated Division \"%s\" " % division_name
            else:
                action = "Deactivated Legal Entity \"%s\" " % legal_entity_name
        else:
            if division_id is not None:
                action = "Activated Division \"%s\" " % division_name
            else:
                action = "Activated Legal Entity \"%s\" " % legal_entity_name

        return True

    def reactivate_unit(self, client_id, unit_id, session_user):
        action_column = "business_group_id,legal_entity_id,division_id,country_id,geography_id,industry_id,unit_code,unit_name,address,postal_code,domain_ids"
        condition = "unit_id = '%d'" % (unit_id)
        rows = self.get_data(self.tblUnits, action_column, condition)
        result = self.convert_to_dict(rows, action_column.split(","))

        action = "Reactivated Unit \"%s-%s\"" % (rows[0][0], rows[0][1])
        self.save_activity(session_user, 19, action)

        columns = ["client_id", "unit_id", "is_active"] + action_column.split(",")
        new_unit_id = self.get_new_id("unit_id", self.tblUnits)
        result = result[0]
        unit_code = self.get_next_unit_auto_gen_no(client_id)
        values = [
            client_id, new_unit_id,1, result["business_group_id"], result["legal_entity_id"],
            result["division_id"], result["country_id"], result["geography_id"],
            result["industry_id"],unit_code, result["unit_name"], result["address"],
            result["postal_code"], result["domain_ids"]
        ]
        self.insert(self.tblUnits, columns, values)
        return unit_code, result["unit_name"]

    def verify_username(self, username):
        columns = "count(*), user_id"
        condition = "email_id='%s' and is_active = 1" % (username)
        rows = self.get_data(self.tblUsers, columns, condition)
        count = rows[0][0]
        if count == 1:
            return rows[0][1]
        else:
            condition = "username='%s'" % username
            columns = "count(*)"
            rows = self.get_data(self.tblAdmin, columns, condition)
            count = rows[0][0]
            if count == 1:
                return 0
            else:
                return None

    def verify_password(self, password, user_id):
        columns = "count(*)"
        encrypted_password = self.encrypt(password)
        condition = "1"
        rows= None
        if user_id == 0:
            condition = "password='%s'" % (encrypted_password)
            rows = self.get_data(self.tblAdmin, columns, condition)
        else:
            condition = "password='%s' and user_id='%d'" % (encrypted_password, user_id)
            rows = self.get_data(self.tblUsers, columns, condition)
        if(int(rows[0][0]) <= 0):
            return False
        else:
            return True

    def update_password(self, password, user_id):
        columns = ["password"]
        values = [self.encrypt(password)]
        condition = "1"
        result = False
        if user_id != 0:
            condition = " user_id='%d'" % user_id
            result = self.update(self.tblUsers, columns, values, condition)
        else:
            result = self.update(self.tblAdmin, columns, values, condition)

        if user_id != 0:
            columns = "employee_code, employee_name"
            condition = "user_id = '%d'" % user_id
            rows = self.get_data(self.tblUsers, columns, condition)
            employee_name = rows[0][1]
            if rows[0][0] is not None:
                employee_name = "%s - %s" % (rows[0][0], rows[0][1])
        else:
            employee_name = "Administrator"

        action = "\"%s\" has updated his/her password" % ( employee_name)
        self.save_activity(user_id, 0, action)

        if result:
            return True
        else:
            return False

    def get_business_groups_for_user(self, user_id):
        result = {}
        client_ids = None
        if user_id != None:
            client_ids = self.get_user_clients(user_id)
        columns = "business_group_id, business_group_name, client_id"
        condition = "1"
        if client_ids is not None:
            condition = "client_id in (%s) order by business_group_name ASC" % client_ids
            rows = self.get_data(self.tblBusinessGroups, columns, condition)
            columns = ["business_group_id", "business_group_name", "client_id"]
            result = self.convert_to_dict(rows, columns)
        return self.return_business_groups(result)

    def return_business_groups(self, business_groups):
        results = []
        for business_group in business_groups :
            results.append(core.BusinessGroup(
                business_group["business_group_id"], business_group["business_group_name"],
                business_group["client_id"]
            ))
        return results

    def get_legal_entities_for_user(self, user_id):
        client_ids = None
        result = {}
        if user_id != None:
            client_ids = self.get_user_clients(user_id)
        columns = "legal_entity_id, legal_entity_name, business_group_id, client_id"
        condition = "1"
        if client_ids is not None:
            condition = "client_id in (%s) order by legal_entity_name ASC" % client_ids
            rows = self.get_data(self.tblLegalEntities, columns, condition)
            columns = ["legal_entity_id", "legal_entity_name", "business_group_id",
            "client_id"]
            result = self.convert_to_dict(rows, columns)
        return self.return_legal_entities(result)

    def return_legal_entities(self, legal_entities):
        results = []
        for legal_entity in legal_entities :
            results.append(core.LegalEntity(
                legal_entity["legal_entity_id"], legal_entity["legal_entity_name"],
                legal_entity["business_group_id"], legal_entity["client_id"]
            ))
        return results

    def get_divisions_for_user(self, user_id):
        client_ids = None
        result = {}
        if user_id != None:
            client_ids = self.get_user_clients(user_id)
        columns = "division_id, division_name, legal_entity_id, business_group_id,"+\
        "client_id"
        condition = "1"
        if client_ids is not None:
            condition = "client_id in (%s) order by division_name ASC" % client_ids
            rows = self.get_data(self.tblDivisions, columns, condition)
            columns = ["division_id", "division_name", "legal_entity_id",
            "business_group_id", "client_id"]
            result = self.convert_to_dict(rows, columns)
        return self.return_divisions(result)

    def return_divisions(self, divisions):
        results = []
        for division in divisions :
            division_obj = core.Division(division["division_id"], division["division_name"],
                division["legal_entity_id"],division["business_group_id"],division["client_id"])
            results.append(division_obj)
        return results

    def get_units_for_user(self, user_id):
        client_ids = None
        result = {}
        if user_id != None:
            client_ids = self.get_user_clients(user_id)
        columns = "unit_id, unit_code, unit_name, address, division_id,"+\
        " legal_entity_id, business_group_id, client_id, is_active, geography_id, industry_id, domain_ids"
        condition = "1"
        if client_ids is not None:
            condition = "client_id in (%s) order by unit_name ASC" % client_ids
            rows = self.get_data(self.tblUnits, columns, condition)
            columns = ["unit_id", "unit_code", "unit_name", "unit_address", "division_id",
            "legal_entity_id", "business_group_id", "client_id", "is_active", "geography_id", "industry_id", "domain_ids"]
            result = self.convert_to_dict(rows, columns)
        return self.return_units(result)

    def return_units(self, units):
        results = []
        for unit in units :
            results.append(core.Unit(
                unit["unit_id"], unit["division_id"], unit["legal_entity_id"],
                unit["business_group_id"], unit["client_id"], unit["unit_code"],
                unit["unit_name"], unit["unit_address"], bool(unit["is_active"])
            ))
        return results

    def get_groups_for_country(self, country_id, user_id) :
        def return_result(groups) :
            group_results = []
            for group in groups :
                countries = [
                    int(x) for x in group["country_ids"].split(',')
                ]
                domains = [
                    int(y) for y in group["domain_ids"].split(',')
                ]
                group_results.append(core.GroupCompany(
                    group["client_id"],
                    group["group_name"],
                    bool(group["is_active"]),
                    countries,
                    domains
                ))
            return group_results

        query = "SELECT distinct t1.client_id, t1.group_name, \
            t1.is_active, \
            (select group_concat(distinct d.domain_id) from tbl_client_domains d where d.client_id = t1.client_id)domain_ids, \
            (select group_concat(distinct c.country_id) from tbl_client_countries c where c.client_id = t1.client_id) country_ids \
            FROM tbl_client_groups t1 \
            INNER JOIN tbl_user_clients t4 \
            ON t1.client_id = t4.client_id \
            AND t1.is_active = 1 \
            AND t4.user_id =  %s \
            AND t1.client_id in (select distinct client_id from tbl_client_countries where country_id = %s)" % (user_id, country_id)

        rows = self.select_all(query)
        columns = ["client_id", "group_name", "is_active", "domain_ids", "country_ids"]
        results = self.convert_to_dict(rows, columns)
        return return_result(results)

    def get_business_groups_for_country(self, country_id, user_id) :
        query = "SELECT distinct t1.client_id, t1.business_group_id, \
            t1.business_group_name FROM tbl_business_groups t1 \
            INNER JOIN tbl_client_countries t2 \
            ON t1.client_id = t2.client_id \
            INNER JOIN tbl_user_clients t3 \
            ON t1.client_id = t3.client_id\
            AND t3.user_id = %s\
            AND t2.country_id = %s" % (
                user_id, country_id
            )
        rows = self.select_all(query)
        columns = ["client_id", "business_group_id", "business_group_name"]
        result = self.convert_to_dict(rows, columns)
        return self.return_business_groups(result)

    def get_legal_entity_for_country(self, country_id, user_id):
        query = "SELECT distinct t1.client_id, t1.legal_entity_id, \
            t1.legal_entity_name, t1.business_group_id \
            FROM tbl_legal_entities t1 \
            INNER JOIN tbl_client_countries t2 \
            ON t1.client_id = t2.client_id \
            INNER JOIN tbl_user_clients t3 \
            ON t1.client_id = t3.client_id \
            AND t3.user_id = %s \
            AND t2.country_id = %s" % (
                user_id, country_id
            )
        rows = self.select_all(query)
        columns = ["client_id", "legal_entity_id", "legal_entity_name", "business_group_id"]
        result = self.convert_to_dict(rows, columns)
        return self.return_legal_entities(result)

    def get_divisions_for_country(self, country_id, user_id):
        query = "SELECT distinct t1.client_id, t1.business_group_id, \
            t1.legal_entity_id, t1.division_id, t1.division_name \
            FROM tbl_divisions t1 \
            INNER JOIN tbl_client_countries t2 \
            ON t1.client_id = t2.client_id \
            INNER JOIN tbl_user_clients t3 \
            ON t1.client_id = t3.client_id \
            AND t3.user_id = %s \
            AND t2.country_id=%s" % (
                user_id, country_id
            )
        rows = self.select_all(query)
        columns = ["client_id", "business_group_id", "legal_entity_id", "division_id", "division_name"]
        result = self.convert_to_dict(rows, columns)
        return self.return_divisions(result)

    def get_units_for_country(self, country_id, user_id):
        def return_unit_details(units):
            results = []
            for unit in units :
                domain_ids = [
                    int(x) for x in unit["domain_ids"].split(',')
                ]
                parent_ids = [
                    int(x) for x in unit["parent_ids"][:-1].split(',')
                ]
                parent_ids.append(int(unit["geography_id"]))
                unit_name = "%s - %s" % (unit["unit_code"], unit["unit_name"])
                results.append(technotransactions.UNIT(
                    unit["unit_id"],
                    unit_name,
                    unit["division_id"],
                    unit["legal_entity_id"],
                    unit["business_group_id"],
                    unit["client_id"],
                    domain_ids,
                    unit["industry_id"],
                    parent_ids
                ))
            return results

        query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, \
            t1.division_id, t1.legal_entity_id, t1.business_group_id,\
            t1.client_id, t1.geography_id, t1.industry_id, t1.domain_ids, \
            t3.parent_ids \
            FROM tbl_units t1 \
            INNER JOIN tbl_client_countries t2 \
            ON t2.client_id = t1.client_id \
            INNER JOIN tbl_geographies t3 \
            ON t1.geography_id = t3.geography_id \
            INNER JOIN tbl_user_clients t4 \
            ON t1.client_id = t4.client_id \
            AND t1.is_active = 1 \
            AND t4.user_id = %s \
            AND t2.country_id = %s " % (
                user_id, country_id
            )
        rows = self.select_all(query)
        columns = [
            "unit_id", "unit_code", "unit_name", "division_id",
            "legal_entity_id", "business_group_id",
            "client_id", "geography_id",
            "industry_id", "domain_ids", "parent_ids"
        ]
        result = self.convert_to_dict(rows, columns)
        return return_unit_details(result)

    def get_submited_statutory(self, unit_id, domain_id):
        q = "select client_statutory_id from tbl_client_statutories \
            where unit_id = %s and domain_id = %s and submission_type = 1" % (
                int(unit_id), int(domain_id)
            )
        rows = self.select_all(q)
        if rows :
            result = self.convert_to_dict(rows, ["client_statutory_id"])
            return result
        else :
            return None

    def get_assign_statutory_wizard_two(
        self, country_id, geography_id, industry_id,
        domain_id, unit_id, user_id
    ):
        # save_statutos = self.get_submited_statutory(unit_id, domain_id)
        # if save_statutos is not None :
        if unit_id is not None :
            return self.return_unassign_statutory_wizard_two(country_id, geography_id, industry_id, domain_id, unit_id)

        q = "select parent_ids from tbl_geographies where geography_id = %s" % (int(geography_id))
        row = self.select_one(q)
        if row :
            parent_ids = [int(x) for x in row[0].split(',')[:-1]]
            if len(parent_ids) == 1 :
                parent_ids.append(0)
        else :
            parent_ids = []

        query = "SELECT distinct t1.statutory_mapping_id, \
            t1.statutory_nature_id, t2.statutory_nature_name, \
            t5.statutory_id\
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_statutory_natures t2 \
            ON t1.statutory_nature_id = t2.statutory_nature_id\
            INNER JOIN tbl_statutory_industry t3 \
            ON t1.statutory_mapping_id = t3.statutory_mapping_id\
            INNER JOIN tbl_statutory_geographies t4 \
            ON t1.statutory_mapping_id = t4.statutory_mapping_id \
            INNER JOIN tbl_statutory_statutories t5 \
            ON t1.statutory_mapping_id = t5.statutory_mapping_id\
            WHERE t1.is_active = 1 AND t1.approval_status IN (1, 3) \
            AND t1.domain_id = %s \
            AND t1.country_id = %s \
            AND t3.industry_id = %s \
            AND t4.geography_id\
            IN ( \
                SELECT g.geography_id \
                FROM tbl_geographies g \
                WHERE g.geography_id = %s \
                OR g.parent_ids LIKE '%s' OR t4.geography_id IN %s )" % (
                    domain_id, country_id, industry_id, geography_id,
                    str("%" + str(geography_id) + ",%"),
                    (str(tuple(parent_ids)))
                )
        rows = self.select_all(query)
        columns = [
            "statutory_mapping_id", "statutory_nature_id",
            "statutory_nature_name", "statutory_id"
        ]
        result = self.convert_to_dict(rows, columns)
        final_result = []
        mapping_ids = []
        for r in result :
            mapping_id = int(r["statutory_mapping_id"])
            if mapping_id not in mapping_ids :
                mapping_ids.append(mapping_id)
                final_result.append(r)
        return self.return_assign_statutory_wizard_two(country_id, domain_id, final_result)

    def get_compliance_by_mapping_id(self, mapping_id):

        qry = "SELECT distinct t1.compliance_id, t1.statutory_provision, \
            t1.compliance_task, t1.compliance_description, \
            t1.document_name \
            FROM tbl_compliances t1 \
            WHERE t1.is_active = 1 AND t1.statutory_mapping_id = %s" % (
                mapping_id
            )
        rows = self.select_all(qry)
        columns = [
            "compliance_id", "statutory_provision",
            "compliance_task", "compliance_description",
            "document_name"
        ]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return result

    def return_unassign_statutory_wizard_two(
        self, country_id, geography_id, industry_id,
        domain_id, unit_id
    ):
        new_compliance = self.get_unassigned_compliances(
            country_id, domain_id, industry_id,
            geography_id, unit_id
        )
        assigned_statutory_list = []
        for key, value in new_compliance.items() :
            name = self.statutory_parent_mapping[int(key)][0]
            compliances = value
            applicable_status = bool(1)
            statutory_opted_status = None
            not_applicable_remarks = None
            assigned_statutory_list.append(
                core.AssignedStatutory(
                    key, name, compliances, applicable_status,
                    statutory_opted_status,
                    not_applicable_remarks
                )
            )
        return technotransactions.GetStatutoryWizardTwoDataSuccess(
            assigned_statutory_list
        )

    def return_assign_statutory_wizard_two(self, country_id, domain_id, data):
        if bool(self.statutory_parent_mapping) is False:
            self.get_statutory_master()
        level_1_compliance = {}
        for d in data :
            mapping_id = int(d["statutory_mapping_id"])
            statutory_nature_name = d["statutory_nature_name"]
            statutory_id = int(d["statutory_id"])
            compliance_list = self.get_compliance_by_mapping_id(mapping_id)
            statutory_data = self.statutory_parent_mapping.get(statutory_id)
            s_mapping = statutory_data[1]
            level_map = s_mapping.split(">>")
            if len(level_map) == 1 :
                level_map = None
            else :
                level_map = ">>".join(level_map[-1:])
            statutory_parents = statutory_data[2]
            level_1 = statutory_parents[0]
            if level_1 == 0 :
                level_1 = statutory_id
            compliance_applicable_status = bool(1)
            compliance_opted_status = None
            compliance_remarks = None
            compliance_applicable_list = level_1_compliance.get(level_1)
            if compliance_applicable_list is None:
                compliance_applicable_list = []
            for c in compliance_list :
                if level_map is not None :
                    provision = "%s - %s" % (level_map, c["statutory_provision"])
                else :
                    provision = " %s" % (c["statutory_provision"])
                # provision.replace(level_1, "")
                document_name = c["document_name"]
                if document_name == "None":
                    document_name = None
                if document_name :
                    name = "%s - %s" % (document_name, c["compliance_task"])
                else :
                    name = c["compliance_task"]
                c_data = core.ComplianceApplicability(
                    c["compliance_id"],
                    name,
                    c["compliance_description"],
                    provision,
                    statutory_nature_name,
                    compliance_applicable_status,
                    compliance_opted_status,
                    compliance_remarks
                )
                compliance_applicable_list.append(c_data)
            level_1_compliance[level_1] = compliance_applicable_list

        assigned_dict = {}
        assigned_statutory_list = []
        for key, value in level_1_compliance.iteritems() :
            name = self.statutory_parent_mapping.get(int(key))
            name = name[0]
            compliances = value
            applicable_status = bool(1)
            statutory_opted_status = None
            not_applicable_remarks = None
            assigned_dict[name] = core.AssignedStatutory(
                key, name, compliances, applicable_status,
                statutory_opted_status,
                not_applicable_remarks
            )
        for k in sorted(assigned_dict) :
            assigned_statutory_list.append(
                assigned_dict[k]
            )

        return technotransactions.GetStatutoryWizardTwoDataSuccess(
            assigned_statutory_list
        )

    def save_assigned_statutories(self, data, user_id):

        submission_type = data.submission_type
        client_statutory_id = data.client_statutory_id
        created_on = str(self.get_date_time())
        if submission_type == "Save" :
            if client_statutory_id is None:
                self.save_client_statutories(data, user_id)
            else :
                assigned_statutories = data.assigned_statutories
                value_list = self.save_update_client_complainces(client_statutory_id, assigned_statutories, user_id, created_on)
                self.execute_bulk_insert(value_list)
        elif submission_type == "Submit" :
            assigned_statutories = data.assigned_statutories
            self.submit_client_statutories_compliances(client_statutory_id, assigned_statutories, user_id)

        return technotransactions.SaveAssignedStatutorySuccess()

    def save_client_statutories(self, data, user_id):
        country_id = data.country_id
        client_id = data.client_id
        geography_id = data.geography_id
        unit_ids = data.unit_ids
        domain_id = data.domain_id
        submission_type = 0

        field = "(client_statutory_id, client_id, geography_id,\
            country_id, domain_id, unit_id, submission_type,\
            created_by, created_on)"
        value_list = []
        for unit_id in unit_ids :
            client_statutory_id = self.get_new_id("client_statutory_id", self.tblClientStatutories)
            created_on = str(self.get_date_time())
            values = (
                client_statutory_id, client_id, geography_id, country_id,
                domain_id, int(unit_id) , submission_type, int(user_id), created_on
            )
            if (self.save_data(self.tblClientStatutories, field, values)) :
                assigned_statutories = data.assigned_statutories
                value_list.extend(self.save_update_client_complainces(client_statutory_id, assigned_statutories, user_id, created_on))
        self.execute_bulk_insert(value_list)

    def execute_bulk_insert(self, value_list, submitted_on=None) :
        table = "tbl_client_compliances"
        column = [
            "client_compliance_id", "client_statutory_id",
            "compliance_id", "statutory_id", "statutory_applicable",
            "statutory_opted", "not_applicable_remarks",
            "compliance_applicable", "compliance_opted",
            "created_by",
        ]
        update_column = [
            "client_statutory_id", "compliance_id",
            "statutory_id", "statutory_applicable",
            "statutory_opted", "not_applicable_remarks",
            "compliance_applicable", "compliance_opted",
        ]
        if submitted_on is None :
            column.append("created_on")
            update_column.append("created_on")
        else :
            column.append("submitted_on")
            update_column.append("submitted_on")
        self.on_duplicate_key_update(table, ",".join(column), value_list, update_column)

    def save_update_client_complainces(self, client_statutory_id,  data, user_id, created_on):

        value_list = []
        for d in data :
            level_1_id = d.level_1_statutory_id
            applicable_status = int(d.applicable_status)
            not_applicable_remarks = d.not_applicable_remarks
            if not_applicable_remarks is None :
                not_applicable_remarks = ""
            for key, value in d.compliances.iteritems():
                compliance_id = int(key)
                compliance_applicable_status = int(value)
                values = (
                    'null', client_statutory_id, compliance_id,
                    level_1_id, applicable_status, applicable_status,
                    not_applicable_remarks,
                    compliance_applicable_status,  compliance_applicable_status,
                    int(user_id), created_on
                )
                value_list.append(values)

        return value_list

    def get_compliance_ids(self, client_statutory_id):
        query = "SELECT distinct compliance_id \
            FROM tbl_client_compliances \
            WHERE client_statutory_id = %s" % (client_statutory_id)
        row = self.select_all(query)
        compliance_ids = []
        if row :
            for r in row :
                compliance_ids.append(int(r[0]))
        return compliance_ids

    def submit_client_statutories_compliances(self, client_statutory_id, data, user_id) :
        submitted_on = str(self.get_date_time())
        query = "UPDATE tbl_client_statutories SET submission_type = 1, \
            updated_by=%s WHERE client_statutory_id = %s" % (
                int(user_id), client_statutory_id
            )
        self.execute(query)
        value_list = self.save_update_client_complainces(client_statutory_id, data, user_id, submitted_on)
        self.execute_bulk_insert(value_list, submitted_on)

    def get_assigned_statutories_list(
        self, user_id
    ):
        query = "SELECT t1.client_statutory_id, t1.client_id, \
            t1.geography_id, t1.country_id, t1.domain_id, t1.unit_id, \
            t1.submission_type, t2.group_name, \
            (select geography_name from tbl_geographies where geography_id = t1.geography_id )geography_name, \
            (select country_name from tbl_countries where country_id = t1.country_id )country_name,\
            (select domain_name from tbl_domains where domain_id  = t1.domain_id )domain_name,\
            t3.unit_name, t3.unit_code, \
            (select business_group_name from tbl_business_groups where business_group_id =  t3.business_group_id )business_group_name, \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = t3.legal_entity_id )legal_entity_name, \
            (select division_name from tbl_divisions where division_id = t3.division_id) division_name, \
            (select industry_name from tbl_industries where industry_id = t3.industry_id )industry_name \
            FROM tbl_client_statutories t1 \
            INNER JOIN tbl_client_groups t2 \
            ON t1.client_id = t2.client_id \
            INNER JOIN tbl_units t3 \
            ON t1.unit_id = t3.unit_id \
            INNER JOIN tbl_user_countries t11 \
            ON t1.country_id = t11.country_id \
            INNER JOIN tbl_user_domains t12 \
            ON t1.domain_id = t12.domain_id  AND t11.user_id = t12.user_id\
            INNER JOIN tbl_user_clients t13 \
            ON t1.client_id = t13.client_id  AND t12.user_id = t13.user_id\
            WHERE t13.user_id = %s" % (user_id)

        rows = self.select_all(query)
        columns = [
            "client_statutory_id", "client_id", "geography_id",
            "country_id", "domain_id", "unit_id", "submission_type",
            "group_name", "geography_name", "country_name",
            "domain_name", "unit_name", "unit_code", "business_group_name", "legal_entity_name",
            "division_name", "industry_name"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_assign_statutory_list(result)

    def return_assign_statutory_list(self, assigned_list):
        ASSIGNED_STATUTORIES_list = []
        for data in assigned_list :
            name = "%s - %s" % (data["unit_code"], data["unit_name"])
            ASSIGNED_STATUTORIES_list.append(
                technotransactions.ASSIGNED_STATUTORIES(
                    int(data["submission_type"]),
                    int(data["client_statutory_id"]),
                    data["country_id"],
                    data["country_name"],
                    data["client_id"],
                    data["group_name"],
                    data["business_group_name"],
                    data["legal_entity_name"],
                    data["division_name"],
                    data["unit_id"],
                    name,
                    data["geography_id"],
                    data["geography_name"],
                    data["domain_id"],
                    data["domain_name"],
                    data["industry_name"]
                )
            )

        return technotransactions.GetAssignedStatutoriesListSuccess(
            ASSIGNED_STATUTORIES_list
        )

    def get_assigned_statutories_by_id(self, client_statutory_id):
        query = "SELECT t1.client_statutory_id, t1.client_id, \
            t1.geography_id, t1.country_id, t1.domain_id, t1.unit_id, \
            t1.submission_type, t2.group_name, \
            (select geography_name from tbl_geographies where geography_id = t1.geography_id )geography_name, \
            (select country_name from tbl_countries where country_id = t1.country_id )country_name,\
            (select domain_name from tbl_domains where domain_id  = t1.domain_id )domain_name,\
            t3.unit_name, t3.unit_code, \
            (select business_group_name from tbl_business_groups where business_group_id =  t3.business_group_id )business_group_name, \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = t3.legal_entity_id )legal_entity_name, \
            (select division_name from tbl_divisions where division_id = t3.division_id) division_name, \
            (select industry_name from tbl_industries where industry_id = t3.industry_id )industry_name, \
            t3.industry_id\
            FROM tbl_client_statutories t1 \
            INNER JOIN tbl_client_groups t2 \
            ON t1.client_id = t2.client_id \
            INNER JOIN tbl_units t3 \
            ON t1.unit_id = t3.unit_id \
            WHERE t1.client_statutory_id = %s" % (client_statutory_id)

        rows = self.select_one(query)
        columns = [
            "client_statutory_id", "client_id", "geography_id",
            "country_id", "domain_id", "unit_id", "submission_type",
            "group_name", "geography_name", "country_name",
            "domain_name", "unit_name", "unit_code",
            "business_group_name", "legal_entity_name",
            "division_name", "industry_name", "industry_id"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_assigned_statutories_by_id(result)

    def return_assigned_compliances_by_id(self, client_statutory_id, statutory_id=None, applicable_status=None):
        if bool(self.statutory_parent_mapping) is False:
            self.get_statutory_master()
        if statutory_id is None :
            statutory_id = '%'
        if applicable_status is None :
            applicable_status = '%'
        query = "SELECT t1.client_statutory_id, t1.compliance_id, \
            t1.statutory_id, t1.statutory_applicable, \
            t1.statutory_opted, \
            t1.not_applicable_remarks, \
            t1.compliance_applicable, t1.compliance_opted, \
            t1.compliance_remarks, \
            t2.statutory_name, t3.compliance_task, t3.document_name, \
            t3.statutory_mapping_id, \
            t3.statutory_provision, t3.compliance_description, \
            (SELECT statutory_nature_name from tbl_statutory_natures \
                where statutory_nature_id = (select t.statutory_nature_id from tbl_statutory_mappings t where t.statutory_mapping_id = t3.statutory_mapping_id)),\
            (select distinct level_position from tbl_statutory_levels where level_id = t2.level_id)level,\
            t2.statutory_name, \
            (SELECT statutory_mapping FROM tbl_statutory_mappings where statutory_mapping_id = t3.statutory_mapping_id)\
            FROM tbl_client_compliances t1 \
            INNER JOIN tbl_statutories t2 \
            ON t2.statutory_id = t1.statutory_id \
            INNER JOIN tbl_compliances t3 \
            ON t3.compliance_id = t1.compliance_id \
            WHERE \
            t1.client_statutory_id = %s \
            AND t1.statutory_id like '%s' \
            AND  t1.compliance_applicable like '%s' \
            ORDER BY level, statutory_name, compliance_id" % (
                client_statutory_id, statutory_id,
                applicable_status
            )
        rows = self.select_all(query)
        columns = [
            "client_statutory_id", "compliance_id", "statutory_id",
            "statutory_applicable", "statutory_opted",
            "not_applicable_remarks", "compliance_applicable",
            "compliance_opted", "compliance_remarks",
            "statutory_name", "compliance_task", "document_name",
            "statutory_mapping_id",
            "statutory_provision", "compliance_description",
            "statutory_nature_name", "level", "statutory_name",
            "statutory_mapping"
        ]
        results = self.convert_to_dict(rows, columns)
        level_1_statutory_compliance = {}
        for r in results :
            compliance_opted = r["compliance_opted"]
            if compliance_opted is not None:
                compliance_opted = bool(compliance_opted)
            compliance_remarks = r["compliance_remarks"]
            statutory_opted = r["statutory_opted"]
            if statutory_opted is not None :
                statutory_opted = bool(statutory_opted)
            statutory_id = int(r["statutory_id"])
            statutory_name = r["statutory_name"]
            # mapping_id = int(r["statutory_mapping_id"])
            s_mapping = r["statutory_mapping"]
            level_map = s_mapping.split(">>")
            if len(level_map) == 1 :
                level_map = None
            else :
                level_map = ">> ".join(level_map[-1:])
            if level_map :
                provision = "%s - %s" % (level_map, r["statutory_provision"])
            else :
                provision = r["statutory_provision"]
            document_name = r["document_name"]
            if document_name == "None":
                document_name = None
            if document_name :
                name = "%s - %s" % (document_name, r["compliance_task"])
            else :
                name = r["compliance_task"]
            compliance = core.ComplianceApplicability(
                r["compliance_id"],
                name,
                r['compliance_description'],
                provision,
                r["statutory_nature_name"],
                bool(r["compliance_applicable"]),
                compliance_opted,
                compliance_remarks
            )
            compliance_list = []
            saved_data = level_1_statutory_compliance.get(statutory_name)
            if saved_data is None :
                compliance_list.append(compliance)
                s_data = core.AssignedStatutory(
                    statutory_id,
                    r["statutory_name"],
                    compliance_list,
                    bool(r["statutory_applicable"]),
                    statutory_opted,
                    r["not_applicable_remarks"]
                )
                level_1_statutory_compliance[statutory_name] = s_data
            else :
                compliance_list = saved_data.compliances
                compliance_list.append(compliance)
                saved_data.compliances = compliance_list
                level_1_statutory_compliance[statutory_name] = saved_data

        final_statutory_list = []
        for key in sorted(level_1_statutory_compliance) :
            final_statutory_list.append(
                level_1_statutory_compliance.get(key)
            )

        return final_statutory_list

    def get_unassigned_compliances(
        self, country_id, domain_id, industry_id,
        geography_id, unit_id
    ) :
        q = "select parent_ids from tbl_geographies where geography_id = %s" % (int(geography_id))
        row = self.select_one(q)
        if row :
            parent_ids = [int(x) for x in row[0].split(',')[:-1]]
            if len(parent_ids) == 1 :
                parent_ids.append(0)
        else :
            parent_ids = []

        query = "SELECT distinct \
            t2.compliance_id, t2.compliance_task, t2.document_name,\
            t2.statutory_provision, t2.compliance_description, t5.statutory_id, \
            t.statutory_nature_name \
            FROM tbl_statutory_mappings t1\
            INNER JOIN tbl_compliances t2 ON t1.statutory_mapping_id = t2.statutory_mapping_id \
            INNER JOIN tbl_statutory_industry t3 \
            ON t1.statutory_mapping_id = t3.statutory_mapping_id\
            INNER JOIN tbl_statutory_geographies t4 \
            ON t1.statutory_mapping_id = t4.statutory_mapping_id \
            INNER JOIN tbl_statutory_statutories t5 \
            ON t1.statutory_mapping_id = t5.statutory_mapping_id \
            INNER JOIN tbl_statutory_natures t\
            ON t1.statutory_nature_id = t.statutory_nature_id\
            WHERE t1.is_active = 1 AND t2.is_active = 1 ANd t1.approval_status IN (1, 3) \
            AND t1.domain_id = %s \
            AND t1.country_id = %s \
            AND t3.industry_id = %s \
            AND t4.geography_id\
            IN ( \
                SELECT g.geography_id \
                FROM tbl_geographies g \
                WHERE g.geography_id = %s \
                OR g.parent_ids LIKE '%s' OR t4.geography_id IN %s )\
            AND t2.compliance_id NOT IN ( \
                SELECT distinct c.compliance_id \
                FROM tbl_client_compliances c \
                INNER JOIN tbl_client_statutories s\
                ON c.client_statutory_id = s.client_statutory_id\
                AND s.domain_id = %s \
                AND s.unit_id = %s \
                ) \
            " % (
                    domain_id, country_id, industry_id, geography_id,
                    str("%" + str(geography_id) + ",%"),
                    (str(tuple(parent_ids))),
                    domain_id, unit_id
                )
        rows = self.select_all(query)
        columns = [
            "compliance_id", "compliance_task",
            "document_name", "statutory_provision",
            "compliance_description", "statutory_id",
            "statutory_nature_name"
        ]
        result = self.convert_to_dict(rows, columns)
        final_result = []
        compliance_ids = []
        for r in result :
            compliance_id = int(r["compliance_id"])
            if compliance_id not in compliance_ids :
                compliance_ids.append(compliance_id)
                final_result.append(r)
        # New compliances to_structure
        if bool(self.statutory_parent_mapping) is False:
            self.get_statutory_master()
        level_1_compliance = {}
        for d in final_result :
            statutory_nature_name = d["statutory_nature_name"]
            statutory_id = int(d["statutory_id"])
            statutory_data = self.statutory_parent_mapping.get(statutory_id)
            s_mapping = statutory_data[1]
            statutory_parents = statutory_data[2]
            level_1 = statutory_parents[0]
            if level_1 == 0 :
                level_1 = statutory_id
            compliance_applicable_status = bool(1)
            compliance_opted_status = None
            compliance_remarks = None
            compliance_applicable_list = level_1_compliance.get(level_1)
            if compliance_applicable_list is None:
                compliance_applicable_list = []
            provision = "%s - %s" % (s_mapping, d["statutory_provision"])
            document_name = d["document_name"]
            if document_name == "None":
                document_name = None
            if document_name :
                name = "%s - %s" % (document_name, d["compliance_task"])
            else :
                name = "%s" % (d["compliance_task"])
            c_data = core.ComplianceApplicability(
                d["compliance_id"],
                name,
                d["compliance_description"],
                provision,
                statutory_nature_name,
                compliance_applicable_status,
                compliance_opted_status,
                compliance_remarks
            )
            compliance_applicable_list.append(c_data)
            level_1_compliance[level_1] = compliance_applicable_list

        return level_1_compliance

    def return_assigned_statutories_by_id(self, data):
        client_statutory_id = data["client_statutory_id"]
        statutories = self.return_assigned_compliances_by_id(client_statutory_id)
        new_compliances = self.get_unassigned_compliances(
            data["country_id"], data["domain_id"],
            data["industry_id"], data["geography_id"],
            data["unit_id"]
        )
        for key, value in new_compliances.iteritems():
            key = int(key)
            key_exists = False
            for item in statutories :
                if key == item.level_1_statutory_id:
                    key_exists = True
                    break
            if key_exists is False :
                statutory_name = self.statutory_parent_mapping.get(key)[0]
                s_data = core.AssignedStatutory(
                    key,
                    statutory_name,
                    None,
                    True,
                    None,
                    None
                )
                statutories.append(s_data)

        return technotransactions.GetAssignedStatutoriesByIdSuccess(
            data["country_name"],
            data["group_name"],
            data["business_group_name"],
            data["legal_entity_name"],
            data["division_name"],
            data["unit_name"],
            data["geography_name"],
            data["domain_name"],
            statutories,
            new_compliances,
            data["industry_name"]
        )

    def get_assigned_statutories_report(self, request_data, user_id):
        country_id = request_data.country_id
        domain_id = request_data.domain_id
        group_id = request_data.group_id
        qry = ""
        if group_id is not None :
            qry += " AND t1.client_id = %s " % (group_id)
        business_group_id = request_data.business_group_id
        if business_group_id is not None :
            qry += " AND t3.business_group_id = %s " % (business_group_id)
        legal_entity_id = request_data.legal_entity_id
        if legal_entity_id is not None :
            qry += " AND t3.legal_entity_id = %s " % (legal_entity_id)
        division_id = request_data.division_id
        if division_id is not None :
            qry += " AND t3.division_id =%s " % (division_id)
        unit_id = request_data.unit_id
        if unit_id is not None :
            qry += " AND t3.unit_id = %s " % (unit_id)
        level_1_statutory_id = request_data.level_1_statutory_id
        if level_1_statutory_id is not None :
            qry += " AND t4.statutory_id = %s " % (level_1_statutory_id)
        applicable_status = request_data.applicability_status
        if applicable_status is not None :
            applicable_status = int(applicable_status)
            qry += " AND t4.compliance_applicable = %s " % applicable_status

        query = "SELECT distinct t1.client_statutory_id, t1.client_id, \
            t1.geography_id, t1.country_id, t1.domain_id, t1.unit_id, \
            t1.submission_type, t2.group_name, t3.unit_name, \
            (select business_group_name from tbl_business_groups where business_group_id = t3.business_group_id )business_group_name, \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = t3.legal_entity_id)legal_entity_name,\
            (select division_name from tbl_divisions where division_id = t3.division_id)division_name, \
            t3.address, t3.postal_code, t3.unit_code \
            FROM tbl_client_statutories t1 \
            INNER JOIN tbl_client_groups t2 \
            ON t1.client_id = t2.client_id \
            INNER JOIN tbl_units t3 \
            ON t1.unit_id = t3.unit_id \
            INNER JOIN tbl_client_compliances t4 \
            ON t1.client_statutory_id = t4.client_statutory_id \
            WHERE t1.submission_type =1 \
            AND t1.country_id = %s \
            AND t1.domain_id = %s " % (
                country_id, domain_id
            )

        query = query + qry
        rows = self.select_all(query)
        columns = [
            "client_statutory_id", "client_id", "geography_id",
            "country_id", "domain_id", "unit_id", "submission_type",
            "group_name", "unit_name",
            "business_group_name", "legal_entity_name",
            "division_name", "address", "postal_code", "unit_code"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_assigned_statutory_report(result, level_1_statutory_id, applicable_status)

    def return_assigned_statutory_report(self, report_data, level_1_statutory_id, applicable_status):
        if bool(self.geography_parent_mapping) is False:
            self.get_geographies()

        unit_wise_statutories_dict = {}
        for data in report_data :
            client_statutory_id = data["client_statutory_id"]
            unit_id = int(data["unit_id"])
            unit_statutories = unit_wise_statutories_dict.get(unit_id)
            if unit_statutories is None :
                geography_id = int(data["geography_id"])
                geography_parents = self.geography_parent_mapping.get(geography_id)
                temp_parents = geography_parents[0].split(">>")
                ordered = temp_parents[::-1]
                unit_name = "%s - %s" % (data["unit_code"], data["unit_name"])
                unit_address = "%s, %s, %s" % (
                    data["address"], ', '.join(ordered), data["postal_code"]
                )
                statutories = self.return_assigned_compliances_by_id(client_statutory_id, level_1_statutory_id, applicable_status)
                unit_statutories = technoreports.UNIT_WISE_ASSIGNED_STATUTORIES(
                    data["unit_id"],
                    unit_name,
                    data["group_name"],
                    data["business_group_name"],
                    data["legal_entity_name"],
                    data["division_name"],
                    unit_address,
                    statutories
                )
            else :
                statutories = unit_statutories.assigned_statutories
                new_stautory = self.return_assigned_compliances_by_id(client_statutory_id, None, applicable_status)
                for new_s in new_stautory :
                    new_id = new_s.level_1_statutory_id
                    is_exists = False
                    for x in statutories :
                        if x.level_1_statutory_id == new_id :
                            x.compliances.extend(new_s.compliances)
                            is_exists = True
                            break
                    if is_exists is False :
                        statutories.append(new_s)
                unit_statutories.assigned_statutories = statutories

            unit_wise_statutories_dict[unit_id] = unit_statutories

        final_unit_wise_statutories_list = []
        for key, value in unit_wise_statutories_dict.iteritems() :
            final_unit_wise_statutories_list.append(value)

        return technoreports.GetAssignedStatutoryReportSuccess(
            final_unit_wise_statutories_list
        )

    def get_unit_details_for_user(self, user_id):
        client_ids = None
        if ((user_id is not None) and (user_id is not 0)):
            client_ids = self.get_user_clients(user_id)

        condition = "1"
        if client_ids is not None:
            condition = "client_id in (%s)" % client_ids

        query = "SELECT business_group_id, legal_entity_id, division_id, client_id, \
        group_name, business_group_name, legal_entity_name, division_name \
        from ( \
        SELECT c.group_name, bg.business_group_name, \
        le.legal_entity_name, d.division_name, u.business_group_id,\
        u.legal_entity_id, u.division_id, u.client_id \
        FROM tbl_units  u  \
        LEFT JOIN tbl_client_groups c on (u.client_id = c.client_id) \
        LEFT JOIN  tbl_business_groups bg on (u.business_group_id = bg.business_group_id) \
        LEFT JOIN  tbl_legal_entities le on (u.legal_entity_id = le.legal_entity_id) \
        LEFT JOIN  tbl_divisions d on (u.division_id = d.division_id) \
        where  u.client_id in (select client_id from tbl_user_clients where user_id = '%d') \
        UNION \
        SELECT c.group_name, bg.business_group_name, le.legal_entity_name, d.division_name, u.business_group_id, u.legal_entity_id, u.division_id, u.client_id \
        FROM tbl_units  u  \
        RIGHT JOIN tbl_client_groups c on (u.client_id = c.client_id) \
        RIGHT JOIN  tbl_business_groups bg on (u.business_group_id = bg.business_group_id) \
        RIGHT JOIN  tbl_legal_entities le on (u.legal_entity_id = le.legal_entity_id) \
        RIGHT JOIN  tbl_divisions d on (u.division_id = d.division_id) \
        where  u.client_id in (select client_id from tbl_user_clients where user_id = '%d')) a \
        group by business_group_id, legal_entity_id, division_id, client_id  \
        order by group_name, business_group_name, legal_entity_name, division_name" % (
            user_id, user_id
        )
        rows = self.select_all(query)
        unit_details = []
        for row in rows:
            detail_columns = "country_id"
            detail_condition = "legal_entity_id = '%d' " % row[1]
            if row[0] == None:
                detail_condition += " And business_group_id is NULL"
            else:
                detail_condition += " And business_group_id = '%d'" % row[0]
            if row[2] == None:
                detail_condition += " And division_id is NULL"
            else:
                detail_condition += " AND division_id = '%d'" % row[2]
            country_condition = detail_condition + " AND country_id in (%s) \
            group by country_id" % (
                self.get_user_countries(user_id)
            )
            country_rows = self.get_data(self.tblUnits, detail_columns, country_condition)
            country_wise_units = {}
            division_is_active = bool(1)
            active_count = 0
            deactive_count = 0
            for country_row in country_rows:
                unit_columns = "unit_id, geography_id, unit_code, unit_name, industry_id, address, "+\
                "postal_code, domain_ids, is_active"
                unit_condition = detail_condition +" and country_id = '%d'" % country_row[0]
                detail_rows = self.get_data(self.tblUnits, unit_columns, unit_condition)
                units = []
                for unit_detail  in detail_rows:
                    units.append(technomasters.UnitDetails(unit_detail[0], unit_detail[1],
                        unit_detail[2], unit_detail[3], unit_detail[4], unit_detail[5],
                        unit_detail[6], [int(x) for x in unit_detail[7].split(",")], bool(unit_detail[8])))
                    if bool(unit_detail[8]) == True :
                        active_count += 1
                    else:
                        deactive_count += 1
                country_wise_units[country_row[0]] = units
            if active_count <= 0:
                division_is_active = bool(0)
            unit_details.append(technomasters.Unit(row[0], row[1], row[2], row[3], country_wise_units,division_is_active))
        return unit_details

    def get_settings(self, client_id):
        settings_columns = "contract_from, contract_to, no_of_user_licence, \
        total_disk_space, total_disk_space_used"
        condition = "client_id = '%d'" % client_id
        return  self.get_data(self.tblClientGroups, settings_columns, condition)

    def get_licence_holder_details(self, client_id):
        columns = "tcu.user_id, tcu.email_id, tcu.employee_name, tcu.employee_code, tcu.contact_no,"+\
        "tcu.is_primary_admin, tu.unit_code, tu.unit_name, tu.address, tcu.is_active, tcu.is_admin"
        tables = [self.tblClientUsers, self.tblUnits]
        aliases = ["tcu", "tu"]
        join_type = "left join"
        join_conditions = ["tcu.seating_unit_id = tu.unit_id"]
        where_condition = "tcu.client_id = '%d'" % client_id
        return self.get_data_from_multiple_tables(columns, tables, aliases, join_type, join_conditions, where_condition)

    def get_profiles(self, client_ids):
        client_ids_list = [int(x) for x in client_ids.split(",")]
        profiles = []
        for client_id in client_ids_list:
            settings_rows = self.get_settings(client_id)
            contract_from = self.datetime_to_string(settings_rows[0][0])
            contract_to = self.datetime_to_string(settings_rows[0][1])
            no_of_user_licence = settings_rows[0][2]
            file_space = settings_rows[0][3]
            used_space = settings_rows[0][4]
            licence_holder_rows = self.get_licence_holder_details(client_id)
            licence_holders = []
            for row in licence_holder_rows:
                employee_name = None
                unit_name = None
                if row[7] == None:
                    unit_name = "-"
                else:
                    unit_name =  "%s - %s" % (row[6], row[7])
                user_id = row[0]
                email_id= row[1]
                contact_no = None if row[4] is "" else row[4]
                is_primary_admin= row[5]
                is_active = row[9]
                is_admin = row[10]
                if(row[3] == None):
                    employee_name = row[2]
                elif (is_primary_admin == 1 and is_active == 1):
                    employee_name = "Administrator"
                elif (is_primary_admin == 1 and is_active == 0):
                    employee_name = "Old Administrator"
                else:
                    employee_name = "%s - %s" % (row[3], row[2])
                address= row[8]
                is_service_provider = False
                if unit_name == "-":
                    if (is_primary_admin == 1 or is_admin == 1 ):
                        is_service_provider = False
                    else:
                        is_service_provider = True
                licence_holders.append(
                    technomasters.LICENCE_HOLDER_DETAILS(
                    user_id, employee_name, email_id, contact_no,
                    unit_name, address,
                    file_space/1000000000, used_space/1000000000,
                    bool(is_active), bool(is_primary_admin),
                    is_service_provider
                ))

            remaining_licence = (no_of_user_licence) - len(licence_holder_rows)
            profile_detail = technomasters.PROFILE_DETAIL(str(contract_from),
                str(contract_to), no_of_user_licence, remaining_licence,
                file_space/1000000000, used_space/1000000000, licence_holders)
            profiles.append(technomasters.PROFILES(client_id, profile_detail))
        return profiles

#
#   Audit Trail
#

    def get_audit_trails(self, session_user):
        user_ids = ""
        form_ids = None
        if session_user != 0:
            column = "user_group_id"
            condition = "user_id = '%d'" % session_user
            rows = self.get_data(self.tblUsers, column, condition)
            user_group_id = rows[0][0]

            column = "form_category_id, form_ids"
            condition = "user_group_id = '%d'" % user_group_id
            rows = self.get_data(self.tblUserGroups, column, condition)
            form_category_id = rows[0][0]
            form_ids = rows[0][1]

            form_category_ids = "%d, 4" % form_category_id
            column = "group_concat(form_id)"
            condition = "form_category_id in (%s) AND \
            form_type_id != 3" % form_category_ids
            rows = self.get_data(
                self.tblForms, column, condition
            )
            form_ids = rows[0][0]

            column = "group_concat(user_group_id)"
            condition = "form_category_id = '%d'" % form_category_id
            rows = self.get_data(self.tblUserGroups, column, condition)
            user_group_ids = rows[0][0]

            column = "group_concat(user_id)"
            condition = "user_group_id in (%s)" % user_group_ids
            rows = self.get_data(self.tblUsers, column, condition)
            user_ids = rows[0][0]
            condition = "user_id in (%s)"% user_ids
        else:
            condition = "1"
        columns = "user_id, form_id, action, created_on"
        condition += " ORDER BY created_on DESC"
        rows = self.get_data(self.tblActivityLog, columns, condition)
        audit_trail_details = []
        for row in rows:
            user_id = row[0]
            form_id = row[1]
            action = row[2]
            date = self.datetime_to_string_time(row[3])
            audit_trail_details.append(general.AuditTrail(user_id, form_id, action, date))
        users = None
        if session_user != 0:
            condition = "user_id in (%s)" % user_ids
            users = self.return_users(condition)
        else:
            users = self.return_users()
        forms = self.return_forms(form_ids)
        return general.GetAuditTrailSuccess(audit_trail_details, users, forms)

#
#   Update Profile
#

    def update_profile(self, contact_no, address, session_user):
        columns = ["contact_no", "address"]
        values = [contact_no, address]
        condition = "user_id= '%d'" % session_user
        self.update(self.tblUsers, columns, values, condition)

#
#   Get Details Report
#
    def get_client_details_report_condition(
        self, country_id, client_id, business_group_id,
        legal_entity_id, division_id, unit_id, domain_ids
    ):
        condition = "tu.country_id = '%d' AND tu.client_id = '%d' " % (
            country_id, client_id
        )
        if business_group_id is not None:
            condition += " AND business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " AND legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " AND division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " AND unit_id = '%d'" % unit_id
        if domain_ids is not None:
            for i, domain_id in enumerate(domain_ids):
                if i == 0 :
                    condition += " AND FIND_IN_SET('%s', domain_ids)" % (domain_id)
                elif i > 0 :
                    condition += " OR FIND_IN_SET('%s', domain_ids)" % (domain_id)

        print condition
        return condition

    def get_client_details_report_count(
        self, country_id, client_id, business_group_id,
        legal_entity_id, division_id, unit_id, domain_ids
    ):
        condition = self.get_client_details_report_condition(
            country_id, client_id, business_group_id,
            legal_entity_id, division_id, unit_id, domain_ids
        )
        query = "SELECT count(*) \
        FROM %s tu \
        WHERE %s" % (
            self.tblUnits, condition
        )
        rows = self.select_all(query)
        return rows[0][0]

    def get_client_details_report(
        self, country_id, client_id, business_group_id,
        legal_entity_id, division_id, unit_id, domain_ids,
        start_count, to_count
    ):
        condition = self.get_client_details_report_condition(
            country_id, client_id, business_group_id,
            legal_entity_id, division_id, unit_id, domain_ids
        )
        columns = "unit_id, unit_code, unit_name, geography_name, \
                    address, domain_ids, postal_code, business_group_name, \
                    legal_entity_name, division_name"
        query = "SELECT %s \
        FROM %s tu \
        INNER JOIN %s tg ON (tu.geography_id = tg.geography_id) \
        LEFT JOIN %s tb ON (tb.business_group_id = tu.business_group_id) \
        INNER JOIN %s tl ON (tl.legal_entity_id = tu.legal_entity_id) \
        LEFT JOIN %s td ON (td.division_id = tu.division_id) \
        WHERE %s \
        ORDER BY tu.business_group_id, tu.legal_entity_id, tu.division_id, \
        tu.unit_id DESC LIMIT %d, %d" % (
            columns, self.tblUnits, self.tblGeographies,  self.tblBusinessGroups,
            self.tblLegalEntities, self.tblDivisions, condition,
            int(start_count), to_count
        )
        rows = self.select_all(query)
        columns_list = columns.replace(" ", "").split(",")
        unit_rows = self.convert_to_dict(rows, columns_list)
        grouped_units = {}
        for unit in unit_rows:
            business_group_name = unit["business_group_name"]
            legal_entity_name = unit["legal_entity_name"]
            division_name = unit["division_name"]
            if business_group_name in ["None", None, ""]:
                business_group_name = "null"
            if division_name in ["None", None, ""]:
                division_name = "null"
            if business_group_name not in grouped_units:
                grouped_units[business_group_name] = {}
            if legal_entity_name not in grouped_units[business_group_name]:
                grouped_units[business_group_name][legal_entity_name] = {}
            if division_name not in grouped_units[business_group_name][legal_entity_name]:
                grouped_units[business_group_name][legal_entity_name][division_name] = []
            grouped_units[business_group_name][legal_entity_name][division_name].append(
                technoreports.UnitDetails(
                    unit["unit_id"], unit["geography_name"], unit["unit_code"],
                    unit["unit_name"], unit["address"], unit["postal_code"],
                    [int(x) for x in unit["domain_ids"].split(",")]
                )
            )
        GroupedUnits = []
        for business_group in grouped_units:
            for legal_entity_name in grouped_units[business_group]:
                for division in grouped_units[business_group][legal_entity_name]:
                    if business_group == "null":
                        business_group_name = None
                    else:
                        business_group_name = business_group
                    if division == "null":
                        division_name = None
                    else:
                        division_name = division
                    GroupedUnits.append(
                        technoreports.GroupedUnits(
                            division_name, legal_entity_name, business_group_name,
                            grouped_units[business_group][legal_entity_name][division]
                        )
                    )
        return GroupedUnits


#
#   Statutory_Notification_list
#
    def get_statutory_notifications_report_data(self, request_data):
        country_id = request_data.country_id
        domain_id = request_data.domain_id
        level_1_statutory_id = request_data.level_1_statutory_id
        if level_1_statutory_id is None :
            level_1_statutory_id = '%'
        query = "SELECT  distinct tsm.country_id, tsm.domain_id\
             from `tbl_statutory_notifications_log` tsnl    \
            INNER JOIN `tbl_statutory_statutories` tss ON \
            tsnl.statutory_mapping_id = tss.statutory_mapping_id \
            INNER JOIN `tbl_statutory_mappings` tsm ON \
            tsm.statutory_mapping_id = tsnl.statutory_mapping_id \
            INNER JOIN  `tbl_statutories` ts ON \
            tss.statutory_id = ts.statutory_id \
            WHERE  \
            tsm.country_id = %s and \
            tsm.domain_id = %s \
            group by tsm.country_id, tsm.domain_id " % (
                country_id, domain_id
            )
        rows = self.select_all(query)
        columns = ["country_id", "domain_id"]
        country_wise_notifications = []
        for row in rows:
            query = "SELECT  ts.statutory_name, tsnl.statutory_provision,\
             tsnl.notification_text, tsnl.updated_on \
             from `tbl_statutory_notifications_log` tsnl    \
            INNER JOIN `tbl_statutory_statutories` tss ON \
            tsnl.statutory_mapping_id = tss.statutory_mapping_id \
            INNER JOIN `tbl_statutory_mappings` tsm ON \
            tsm.statutory_mapping_id = tsnl.statutory_mapping_id \
            INNER JOIN  `tbl_statutories` ts ON \
            tss.statutory_id = ts.statutory_id \
            WHERE  \
            tsm.country_id = %s and \
            tsm.domain_id = %s \
            group by tsm.country_id, tsm.domain_id " % (
                row[0], row[1]
            )
            notifications_rows = self.select_all(query)
            notification_columns = ["statutory_name", "statutory_provision",
            "notification_text", "updated_on" ]
            statutory_notifications = self.convert_to_dict(notifications_rows, notification_columns)
            notifications =[]
            for notification in statutory_notifications:
                notifications.append(technoreports.NOTIFICATIONS(
                    statutory_provision = notification["statutory_provision"],
                    notification_text = notification["notification_text"],
                    date_and_time = self.datetime_to_string(notification["updated_on"])
                ))
            country_wise_notifications.append(
            technoreports.COUNTRY_WISE_NOTIFICATIONS(country_id = row[0], domain_id = row[1], notifications = notifications))
        return country_wise_notifications

#
#   Notifications
#

    def get_user_type(self, user_id):
        columns = "user_group_id"
        condition = "user_id = '%d'" % user_id
        result = self.get_data(self.tblUsers, columns, condition)
        user_group_id = result[0][0]

        columns = "form_category_id"
        condition = "user_group_id = '%d'" % user_group_id
        result = self.get_data(self.tblUserGroups, columns, condition)
        if result[0][0] in [2, "2"]:
            return "Knowledge"
        else:
            return "Techno"


    def get_notifications(
        self, notification_type, session_user, client_id=None
    ):
        user_type = None
        if session_user != 0 :
            user_type = self.get_user_type(session_user)

        columns = "tn.notification_id, notification_text, link, "+\
        "created_on, read_status"
        join_type = "left join"
        tables = [self.tblNotifications, self.tblNotificationsStatus]
        aliases = ["tn", "tns"]
        join_conditions = ["tn.notification_id = tns.notification_id"]
        where_condition = " tns.user_id ='%d' " % (
            session_user
        )
        if user_type == "Techno":
            where_condition += " AND link not like '%sstatutory%s' " % ("%" , "%")
        elif user_type == "Knowledge":
            where_condition += " AND link not like '%sclient%s'" % ("%" , "%")
        where_condition += "order by created_on DESC limit 30"
        rows = self.get_data_from_multiple_tables(
            columns, tables,
            aliases, join_type, join_conditions, where_condition
        )
        notifications = []
        for row in rows:
            notifications.append(general.Notification(
                row[0], row[1], row[2],
                bool(row[4]), self.datetime_to_string(row[3])
            ))
        return notifications

    def update_notification_status(self, notification_id, has_read,
        session_user, client_id=None):
        columns = ["read_status"]
        values = [1 if has_read == True else 0]
        condition = "notification_id = '%d' and user_id='%d'"% (
            notification_id, session_user)
        self.update(self.tblNotificationsStatus, columns, values, condition)

    def get_user_name_by_id(
        self, user_id, client_id = None
    ):
        employee_name = None
        if user_id != None and user_id != 0:
            columns = "employee_code, employee_name"
            condition = "user_id ='{}'".format(user_id)
            rows = self.get_data(
                self.tblUsers, columns, condition
            )
            if len(rows) > 0:
                employee_name = "{} - {}".format(rows[0][0], rows[0][1])
        else:
            employee_name = "Administrator"
        return employee_name

    def get_client_ids(
        self,
    ):
        columns = "group_concat(client_id)"
        condition = "1"
        rows = self.get_data(
            self.tblUserClients, columns, condition
        )
        client_ids = None
        if rows:
            client_ids = rows[0][0]
        return client_ids

    def get_user_client_countries(self, session_user):
        client_ids = self.get_client_ids()
        if client_ids is not None:
            client_ids_list = client_ids.split(",")
            country_ids = []
            for client_id in client_ids_list:
                countries = self.get_client_countries(int(client_id))
                if countries is not None:
                    country_ids += countries.split(",")
            columns = "DISTINCT country_id, country_name, is_active"
            condition = "country_id in (%s) and is_active = 1 ORDER BY country_name" % (
                ",".join(
                    str(x) for x in country_ids
                )
            )
            rows = self.get_data(
                self.tblCountries, columns, condition
            )
            result = []
            if rows :
                columns = ["country_id", "country_name", "is_active"]
                result = self.convert_to_dict(rows, columns)
            return self.return_countries(result)
        else :
            return self.get_countries_for_user(session_user)

    def get_user_client_domains(self, session_user):
        client_ids = self.get_client_ids()
        if client_ids is not None:
            client_ids_list = client_ids.split(",")
            domain_ids = []
            for client_id in client_ids_list:
                domain_ids += self.get_client_domains(int(client_id)).split(",")
            columns = "DISTINCT domain_id, domain_name, is_active"
            condition = "domain_id in (%s) and is_active = 1 ORDER BY domain_name " % (
                ",".join(
                    str(x) for x in domain_ids
                )
            )
            rows = self.get_data(
                self.tblDomains, columns, condition
            )
            result = []
            if rows :
                columns = ["domain_id", "domain_name", "is_active"]
                result = self.convert_to_dict(rows, columns)
            return self.return_domains(result)
        else :
            return self.get_domains_for_user(session_user)

    def is_user_exists_under_user_group(self, user_group_id):
        columns = "count(*)"
        condition = "user_group_id = '%d'" % user_group_id
        rows = self.get_data(
            self.tblUsers, columns, condition
        )
        if rows[0][0] > 0:
            return True
        else:
            return False

    def create_new_admin(self, new_admin_id, client_id, session_user):
        columns = "database_ip, database_username, database_password, \
        database_name"
        condition = "client_id = '%d'" % client_id
        rows = self.get_data(
            self.tblClientDatabase, columns, condition
        )
        if rows:
            host = rows[0][0]
            username = rows[0][1]
            password = rows[0][2]
            database = rows[0][3]
            conn = self._db_connect(host, username, password, database)
            cursor = conn.cursor()

            # Getting old admin details
            query = "select admin_id, username, password from tbl_admin"
            cursor.execute(query)
            rows = cursor.fetchall()
            old_admin_id = rows[0][0]
            old_admin_username = rows[0][1]
            old_admin_password = rows[0][2]

            query = "select count(*) from tbl_assigned_compliances \
            where assignee = '%d' or concurrence_person = '%d' or \
            approval_person = '%d'" % (old_admin_id, old_admin_id, old_admin_id)
            cursor.execute(query)
            rows = cursor.fetchall()
            compliance_count = rows[0][0]
            if compliance_count > 0:
                return "Reassign"
            else:
                # Getting new admin details
                query = "select email_id, password from tbl_users where \
                user_id = '%d'" % (new_admin_id)
                cursor.execute(query)
                rows = cursor.fetchall()
                admin_email = rows[0][0]
                admin_password = rows[0][1]

                # Promoting to new admin in Client db
                query = "update tbl_admin set admin_id='%d', username = '%s', password='%s'" % (
                    new_admin_id, admin_email, admin_password
                )
                cursor.execute(query)
                query = "update tbl_users set is_primary_admin = 1 where user_id = '%d'" % (
                    new_admin_id
                )
                cursor.execute(query)

                # Deactivating old admin in Client db
                query = "update tbl_users set is_active = 0 \
                where user_id = '%d'" % (
                    old_admin_id
                )
                cursor.execute(query)

                # Adding all countries to new admin
                query = "select country_id from tbl_countries"
                cursor.execute(query)
                rows = cursor.fetchall()

                query = "delete from tbl_user_countries where user_id = '%d'" % (
                    new_admin_id
                )
                cursor.execute(query)
                if rows:
                    query = "Insert into tbl_user_countries (country_id, user_id) values "
                    for index, row in enumerate(rows):
                        q = "%s (%s, %s) " % ( query, row[0], new_admin_id)
                        cursor.execute(q)

                # Adding all domains to new admin
                query = "select domain_id from tbl_domains"
                cursor.execute(query)
                rows = cursor.fetchall()

                query = "delete from tbl_user_domains where user_id = '%d'" % (
                    new_admin_id
                )
                cursor.execute(query)
                if rows:
                    query = "Insert into tbl_user_domains (domain_id, user_id) values "
                    for index, row in enumerate(rows):
                        q = "%s (%s, %s) " % ( query, row[0], new_admin_id)
                        cursor.execute(q)

                # Adding all units to new admin
                query = "select unit_id from tbl_units"
                cursor.execute(query)
                rows = cursor.fetchall()

                query = "delete from tbl_user_units where user_id = '%d'" % (
                    new_admin_id
                )
                cursor.execute(query)

                if rows:
                    query = "Insert into tbl_user_units (unit_id, user_id) values "
                    for row in rows:
                        q = "%s (%s, %s) " % ( query, row[0], new_admin_id)
                        cursor.execute(q)


                query = "update tbl_assigned_compliances set concurrence_person = null,\
                approval_person = '%d' where assignee = '%d'" % (new_admin_id, new_admin_id)
                cursor.execute(query)

                query = "update tbl_compliance_history set concurred_by = null,\
                approved_by = '%d' where completed_by = '%d' and completed_on is null\
                or completed_on = 0 " % (new_admin_id, new_admin_id)
                cursor.execute(query)

                query = "update tbl_compliance_history set approve_status = 1, \
                approved_on=now(), approved_by='%d' where completed_by = '%d' and \
                completed_on is not null and completed_on != 0 and approve_status \
                is null or approve_status = 0" % (new_admin_id, new_admin_id)
                cursor.execute(query)

                query = "SELECT employee_name, employee_code FROM tbl_users \
                WHERE user_id='%d'" % new_admin_id
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows[0][1] is not None:
                    employee_name = "%s - %s" % (rows[0][1], rows[0][0])
                else:
                    employee_name = rows[0][0]

                conn.commit()

                # Promoting to new admin in Knowledge db
                query = "update tbl_client_users set is_primary_admin = 1 \
                where user_id = '%d' and client_id = '%d'" % (
                    new_admin_id, client_id
                )
                self.execute(query)

                # Deactivating old admin in Knowledge db
                query = "update tbl_client_users set is_active = 0 \
                where user_id = '%d' and client_id = '%d'" % (
                    old_admin_id, client_id
                )
                self.execute(query)

                query = "update tbl_client_groups set email_id = '%s' where client_id = '%d'" % (admin_email, client_id)
                self.execute(query)

                action = None
                action = "User \"%s\" was promoted to Primary Admin status" % (employee_name)
                self.save_activity(session_user, 20, action)
                return True
        else:
            return "ClientDatabaseNotExists"

    def is_unit_exists_under_client(self, client_id):
        column = "count(*)"
        condition = "client_id = '%d' and is_active = 1" % client_id
        rows = self.get_data(self.tblUnits, column, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

    def validate_no_of_user_licence(self, no_of_user_licence, client_id):
        column = "count(*)"
        condition = "client_id = '%d'" % client_id
        rows = self.get_data(self.tblClientUsers, column, condition)
        current_no_of_users = int(rows[0][0])
        if no_of_user_licence < current_no_of_users:
            return True
        else:
            return False

    def validate_total_disk_space(self, file_space, client_id):
        settings_columns = "total_disk_space_used"
        condition = "client_id = '%d'" % client_id
        rows = self.get_data(self.tblClientGroups, settings_columns, condition)
        used_space = int(rows[0][0])
        if file_space < used_space:
            return True
        else:
            return False
