import os
import MySQLdb as mysql
import hashlib
import string
import random
import datetime
import re
import uuid
import json

from types import *
from protocol import core, knowledgereport

__all__ = [
    "KnowledgeDatabase", "ClientDatabase"
]
    
class Database(object) :
    def __init__(
        self, 
        mysqlHost, mysqlUser, 
        mysqlPassword, mysqlDatabase
    ):
        self._mysqlHost = mysqlHost
        self._mysqlUser = mysqlUser
        self._mysqlPassword = mysqlPassword
        self._mysqlDatabase = mysqlDatabase
        self._connection = None
        self._cursor = None 

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

    def cursor(self):
        return self._cursor
 
    def connect(self):
        assert self._connection is None
        connection = mysql.connect(
            self._mysqlHost, self._mysqlUser, 
            self._mysqlPassword, self._mysqlDatabase
        )
        connection.autocommit(False)
        self._connection = connection

    def close(self):
        assert self._connection is not None
        self._connection.close()
        self._connection = None

    def begin(self):
        self.connect()
        assert self._connection is not None
        assert self._cursor is None
        self._cursor = self._connection.cursor()
        return self._cursor

    def commit(self):
        assert self._connection is not None
        assert self._cursor is not None
        self._cursor.close()
        self._connection.commit()
        self._cursor = None
        self.close()

    def rollback(self):
        assert self._connection is not None
        assert self._cursor is not None
        self._cursor.close()
        self._connection.rollback()
        self._cursor = None
        self.close()

    def select_all(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query)
        return cursor.fetchall()

    def select_one(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    def execute(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        return cursor.execute(query)


    def call_proc(self, procedure_name, args):
        # args is tuple e.g, (parm1, parm2)
        cursor = self.cursor()
        assert cursor is not None
        print "calling proc", procedure_name, args
        cursor.callproc(procedure_name, args)
        print "end proc", procedure_name
        result = cursor.fetchall()
        return result

    def get_data(self, table, columns, condition):
        # query = "SELECT "+columns+" FROM "+table+" \
        #WHERE "+condition 
        query = "SELECT %s FROM %s "  % (columns, table)
        if condition is not None :
            query += " WHERE %s" % (condition)
        print query
        return self.select_all(query)

    def get_data_from_multiple_tables(self, columns, tables, aliases, joinType, 
            joinConditions, whereCondition
        ):
        query = "SELECT %s FROM " % columns

        for index,table in enumerate(tables):
            if index == 0:
                query += "%s  %s  %s" % (
                    table, aliases[index], joinType
                )
            elif index <= len(tables) -2:
                query += " %s %s on (%s) %s " % (
                    table, aliases[index], 
                    joinConditions[index-1], joinType
                )
            else:
                query += " %s %s on (%s)" % (
                    table, aliases[index], 
                    joinConditions[index-1]
                )

        query += " where %s" % whereCondition
        return self.select_all(query)

    def insert(self, table, columns, values) :
        columns = ",".join(columns)
        stringValue = ""
        for index,value in enumerate(values):
            if(index < len(values)-1):
                stringValue = stringValue+"'"+str(value)+"',"
            else:
                stringValue = stringValue+"'"+str(value)+"'"
        query = "INSERT INTO %s (%s) VALUES (%s)" % (table, columns, stringValue)
        return self.execute(query)

    def bulk_insert(self, table, columns, valueList) :
        query = "INSERT INTO %s (%s)  VALUES" % (table, ",".join(str(x) for x in columns))
        for index, value in enumerate(valueList):
            if index < len(valueList)-1:
                query += "%s," % str(value)
            else:
                query += str(value)
        return self.execute(query)

    def update(self, table, columns, values, condition) :
        query = "UPDATE "+table+" set "
        for index,column in enumerate(columns):
            if index < len(columns)-1:
                query += column+" = '"+str(values[index])+"', "
            else:
                query += column+" = '"+str(values[index])+"' "

        query += " WHERE "+condition
        print query
        return self.execute(query)

    def on_duplicate_key_update(self, table, columns, valueList, updateColumnsList):
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

    def delete(self, table, condition):
        query = "DELETE from "+table+" WHERE "+condition
        return self.execute(query)        

    def append(self, table, column, value, condition):
        rows = self.get_data(table, column, condition)
        currentValue = rows[0][0]
        if currentValue != None:
            newValue = currentValue+","+str(value)
        else:
            newValue = str(value)
        columns = [column]
        values = [newValue]
        return self.update(table, columns, values, condition)

    def increment(self, table, column, condition):
        rows = self.get_data(table, column, condition)
        currentValue = rows[0][0]
        if currentValue != None:
            newValue = int(currentValue)+1
        else:
            newValue = 1
        columns = [column]
        values = [newValue]
        return self.update(table, columns, values, condition)        

    def is_already_exists(self, table, condition) :
        query = "SELECT count(*) FROM "+table+" WHERE "+condition
        rows = self.select_all(query)     
        if rows[0][0] > 0:
            return True
        else : 
            return False

    def is_invalid_id(self, table, field, value):
        condition = "%s = '%d'" % (field, value)
        return not self.is_already_exists(table, condition)

    def generate_random(self):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.SystemRandom().choice(characters) for _ in range(7))

    def generate_password(self) : 
        password = self.generate_random()
        return self.encrypt(password)

    def encrypt(self, value):
        m = hashlib.md5()
        m.update(value)
        return m.hexdigest()

    def string_to_datetime(self, string):
        date = string.split("-")
        datetime_val = datetime.datetime(year=int(date[2]),month=self.integer_months[date[1]], day=int(date[0]))
        return datetime_val

class KnowledgeDatabase(Database):
    def __init__(
        self, 
        mysqlHost, mysqlUser, 
        mysqlPassword, mysqlDatabase
    ):
        super(KnowledgeDatabase, self).__init__(
            mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase
        )
        self.statutory_parent_mapping = {}
        self.geography_parent_mapping = {}
        self.initialize_table_names()

    def initialize_table_names(self):
        self.tblActivityLog = "tbl_activity_log"
        self.tblAdmin = "tbl_admin"
        self.tblBusinessGroups = "tbl_business_groups"
        self.tblClientCompliances = "tbl_client_compliances"
        self.tblClientConfigurations = "tbl_client_configurations"
        self.tblClientCountries = "tbl_client_countries"
        self.tblClientDatabase = "tbl_client_database"
        self.tblClientDomains = "tbl_client_domains"
        self.tblClientGroups = "tbl_client_groups"
        self.tblClientSavedCompliances = "tbl_client_saved_compliances"
        self.tblClientSavedStatutories = "tbl_client_saved_statutories"
        self.tblClientStatutories = "tbl_client_statutories"
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
        self.tblUnits = "tbl_units"
        self.tblUserClients = "tbl_user_clients"
        self.tblUserCountries = "tbl_user_countries"
        self.tblUserDomains = "tbl_user_domains"
        self.tblUserGroups = "tbl_user_groups"
        self.tblUserLoginHistory = "tbl_user_login_history"
        self.tblUserSessions = "tbl_user_sessions"
        self.tblUsers = "tbl_users"

    def convert_to_dict(self, data_list, columns) :
        assert type(data_list) in (list, tuple)
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

        


    def validate_session_token(self, session_token) :
        # query = "CALL sp_validate_session_token ('%s');" 
        #% (session_token)
        query = "SELECT user_id FROM tbl_user_sessions \
            WHERE session_token = '%s'" % (session_token)
        row = self.select_one(query)
        user_id = row[0]
        return user_id

    def encrypt(self, value):
        m = hashlib.md5()
        m.update(value)
        return m.hexdigest()


    def verify_login(self, username, password):
        tblAdminCondition = "password='%s' and user_name='%s'" % (
            password, username
        )
        admin_details = self.get_data("tbl_admin", "*", tblAdminCondition)

        if (len(admin_details) == 0) :
            data_columns = ["user_id", "user_group_id", "email_id", 
                "employee_name", "employee_code", "contact_no", "address", 
                "designation", "user_group_name", "form_ids"
            ]
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, \
                t1.address, t1.designation, \
                t2.user_group_name, t2.form_ids \
                FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
                ON t1.user_group_id = t2.user_group_id \
                WHERE t1.password='%s' and t1.email_id='%s'" % (
                    password, username
                )
            data_list = self.select_one(query)
            if data_list is None :
                return False
            else :
                return self.convert_to_dict(data_list, data_columns)
        else :
            return True

    def get_date_time(self) :
        return datetime.datetime.now()

    def new_uuid(self) :
        s = str(uuid.uuid4())
        return s.replace("-", "")

    def clear_old_session(self, user_id, session_type_id) :
        query = "DELETE FROM tbl_user_sessions \
            WHERE user_id=%s and session_type_id=%s" % (
                user_id, session_type_id
            )
        self.execute(query)

    def add_session(self, user_id, session_type_id) :
        self.clear_old_session(user_id, session_type_id)
        session_id = self.new_uuid()
        updated_on = self.get_date_time()
        query = "INSERT INTO tbl_user_sessions \
            (session_token, user_id, session_type_id, last_accessed_time) \
            VALUES ('%s', %s, %s, '%s');"
        query = query % (session_id, user_id, session_type_id, updated_on)

        self.execute(query)
        return session_id

    def get_new_id(self, field , table_name) :
        newId = 1
        query = "SELECT max(%s) from %s " % (field, table_name)

        row = self.select_one(query)
        if row[0] is not None :
            newId = int(row[0]) + 1
        return newId
    
    def save_activity(self, user_id, form_id, action):
        created_on = self.get_date_time()
        activityId = self.get_new_id("activity_log_id", "tbl_activity_log")
        query = "INSERT INTO tbl_activity_log \
            (activity_log_id, user_id, form_id, action, created_on) \
            VALUES (%s, %s, %s, '%s', '%s')" % (
                activityId, user_id, form_id, action, created_on
            )
        print query
        self.execute(query)
        return True

    #
    # Domain
    #

    def get_domains_for_user(self, user_id) :
        # query = "CALL sp_get_domains_for_user (%s)" % (user_id)
        query = "SELECT distinct t1.domain_id, t1.domain_name, \
            t1.is_active FROM tbl_domains t1 "
        if user_id > 0 :
            query = query + " INNER JOIN tbl_user_domains t2 ON \
                t1.domain_id = t2.domain_id WHERE t2.user_id = %s" % (user_id)
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
                ON t1.country_id = t2.country_id WHERE t2.user_id = %s" % (
                    user_id
                )
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
            is_active, created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
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
        forms = []

        columns = "tf.form_id, tf.form_category_id, tfc.form_category, \
            tf.form_type_id, tft.form_type,\
            tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = ["tbl_forms", "tbl_form_category", "tbl_form_type"]
        aliases = ["tf", "tfc", "tft"]
        joinConditions = [
            "tf.form_category_id = tfc.form_category_id", 
            "tf.form_type_id = tft.form_type_id"
        ]
        whereCondition = " tf.form_id in (%s) order by tf.form_order" % (
                form_ids
            )
        joinType = "left join"
        rows = self.get_data_from_multiple_tables(
            columns, tables, aliases, joinType, joinConditions, whereCondition
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
        print query
        self.execute(query)
        return True

    def update_data(self, table_name, field_with_data, where_condition) :
        query = "UPDATE %s SET %s WHERE %s" % (
            table_name, field_with_data, where_condition
        )
        print query
        self.execute(query)
        return True

    def get_industries(self) :
        query = "SELECT industry_id, industry_name, is_active \
            FROM tbl_industries "
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
            qry = " SELECT (GROUP_CONCAT(industry_name SEPARATOR ', ')) as \
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
            is_active FROM tbl_statutory_natures "
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["statutory_nature_id", "statutory_nature_name", "is_active"]
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
        q = "SELECT sttautory_nature_name FROM tbl_statutory_natures WHERE statutory_nature_id=%s" % nature_id
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
        field_with_data = " nature_name = '%s', updated_by = %s" % (
            nature_name, updated_by
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
            is_active, user_id
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
            columns = ["level_id", "level_position", "level_name", "country_id", "domain_id"]
            result = self.convert_to_dict(rows, columns)
        return self.return_statutory_levels(result)


    def return_statutory_levels(self, data):
        statutory_levels = {}
        for d in data :
            country_id = d["country_id"]
            domain_id = d["domain_id"]
            levels = core.Level(d["level_id"], d["level_position"], d["level_name"])
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
            FROM tbl_statutory_levels WHERE country_id = %s and domain_id = %s ORDER BY level_position" % (
                country_id, domain_id
            )
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["level_id", "level_position", "level_name"]
            result = self.convert_to_dict(rows, columns)
        return result


    def check_duplicate_levels(self, country_id, domain_id, levels) :
        saved_names = [row["level_name"] for row in self.get_levels_for_country_domain(country_id, domain_id)]

        for level in levels :
            name = level.level_name
            if level.level_id  is None :
                if (saved_names.count(name) > 0) :
                    print "LevelIdCannotNullFor '%s'" % name
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
                field_with_data = "level_position=%s, level_name='%s', updated_by=%s" % (
                    position, name, user_id
                )
                where_condition = "level_id=%s" % (level.level_id)
                if (self. update_data(table_name, field_with_data, where_condition)):
                    action = "Statutory levels updated"
                    self.save_activity(user_id, 9, action)
        return True

    def get_geography_levels(self):
        query = "SELECT level_id, level_position, level_name, country_id \
            FROM tbl_geography_levels ORDER BY level_position"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["level_id", "level_position", "level_name", "country_id"]
            result = self.convert_to_dict(rows, columns)
        return self.return_geography_levels(result)


    def return_geography_levels(self, data):
        geography_levels = {}
        results = []
        for d in data:
            country_id = d["country_id"]
            level = core.Level(d["level_id"], d["level_position"], d["level_name"])
            _list = geography_levels.get(country_id)
            if _list is None :
                _list = []
            _list.append(level)
            geography_levels[country_id] = _list
        return geography_levels

    def get_geograhpy_levels_for_user(self, user_id):
        country_ids = self.get_user_countries(user_id)
        columns = "level_id, level_position, level_name, country_id"
        condition = "country_id in (%s)"% country_ids
        rows = self.get_data(self.tblGeographyLevels, columns, condition)
        result = []
        if rows :
            columns = ["level_id", "level_position", "level_name", "country_id"]
            result = self.convert_to_dict(rows, columns)
        return self.return_geography_levels(result)


    def get_geography_levels_for_country(self, country_id) :
        query = "SELECT level_id, level_position, level_name \
            FROM tbl_geography_levels WHERE country_id = %s ORDER BY level_position" % country_id
        rows = self.select_all(query)
        columns = ["level_id", "level_position", "level_name"]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_gepgrahy_levels(self, country_id, levels) :
        saved_names = [row["level_name"] for row in self.get_geography_levels_for_country(country_id)]

        for level in levels :
            name = level.level_name
            if level.level_id  is None :
                if (saved_names.count(name) > 0) :
                    print "LevelIdCannotNullFor '%s'" % name
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
                field_with_data = "level_position=%s, level_name='%s', updated_by=%s" % (
                    position, name, int(user_id)
                )
                where_condition = "level_id=%s" % (level.level_id)
                if (self. update_data(table_name, field_with_data, where_condition)):
                    action = "Geography levels updated"
                    self.save_activity(user_id, 5, action)
        return True

    def get_geographies(self) :
        query = "SELECT t1.geography_id, t1.geography_name, t1.level_id, \
            t1.parent_ids, t1.is_active, t2.country_id, t3.country_name FROM tbl_geographies t1 \
            INNER JOIN tbl_geography_levels t2 on t1.level_id = t2.level_id \
            INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id"
        rows = self.select_all(query)
        result = []
        if rows :
            columns = ["geography_id", "geography_name", "level_id", "parent_ids", "is_active", "country_id", "country_name"]
            result = self.convert_to_dict(rows, columns)
            self.set_geography_parent_mapping(result)
        return self.return_geographies(result)


    def return_geographies(self, data):
        geographies = {}
        for d in data :
            parent_ids = [int(x) for x in d["parent_ids"][:-1].split(',')]
            geography = core.Geography(d["geography_id"], d["geography_name"], d["level_id"], parent_ids, parent_ids[-1], bool(d["is_active"]))
            country_id = d["country_id"]
            _list = geographies.get(country_id)
            if _list is None :
                _list = []
            _list.append(geography)
            geographies[country_id] = _list
        return geographies

    def get_geographies_for_user(self, user_id):
        coutry_ids = self.get_user_countries(user_id)
        columns = "t1.geography_id, t1.geography_name, "+\
        "t1.level_id,t1.parent_ids, t1.is_active, t2.country_id, t3.country_name"
        tables = [self.tblGeographies, self.tblGeographyLevels, self.tblCountries]
        aliases = ["t1", "t2", "t3"]
        joinType = " INNER JOIN"
        joinConditions = ["t1.level_id = t2.level_id", "t2.country_id = t3.country_id"]
        whereCondition = "1"
        rows = self.get_data_from_multiple_tables(columns, tables, aliases, joinType, 
            joinConditions, whereCondition)
        result = []
        if rows :        
            columns = ["geography_id", "geography_name", "level_id", "parent_ids", "is_active", "country_id", "country_name"]
            result = self.convert_to_dict(rows, columns)
            # self.geography_parent_mapping(result)
        return self.return_geographies(result)

    def get_geography_report(self):
        def return_report_data(result) :
            mapping_dict = {}
            for key, value in result.iteritems():
                mappings = value[0]
                is_active = value[1]
                country_id = value[2]
                _list = mapping_dict.get(country_id)
                if _list is None:
                    _list = []

                _list.append(
                    knowledgereport.GeographyMapping(
                        mappings, is_active
                    )
                )
                mapping_dict[country_id] = _list
            return mapping_dict

        if bool(self.geography_parent_mapping) is False :
            data = self.get_geographies()

        return return_report_data(self.geography_parent_mapping)

    def get_geography_by_id(self, geography_id):
        query = "SELECT geography_id, geography_name, level_id, parent_ids, is_active \
            FROM tbl_geographies WHERE geography_id = %s" % (geography_id)
        rows = self.select_one(query)
        result = []
        if rows :
            columns = ["geography_id", "geography_name", "level_id", "parent_ids", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_geography(self, parent_ids, geography_id) :
        query = "SELECT geography_id, geography_name, level_id, is_active \
            FROM tbl_geographies WHERE parent_ids='%s' " % (parent_ids)
        if geography_id is not None :
            query = query + " AND geography_id != %s" % geography_id
        
        rows = self.select_all(query)
        columns = ["geography_id", "geography_name", "level_id", "is_active"]
        return self.convert_to_dict(rows, columns)


    def save_geography(self, geography_level_id, geography_name, parent_ids, user_id) :
        is_saved = False
        table_name = "tbl_geographies"
        created_on = self.get_date_time()
        geography_id = self.get_new_id("geography_id", table_name)
        field = "(geography_id, geography_name, level_id, \
            parent_ids, created_by, created_on)"
        data = (
            geography_id, geography_name, int(geography_level_id), 
            parent_ids, int(user_id), str(created_on)
        )
        if (self.save_data(table_name, field, data)) :
            action = "New Geography %s added" % (geography_id)
            self.save_activity(user_id, 6, action)
            is_saved = True
        return is_saved

    def update_geography(self, geography_id, name, parent_ids, updated_by) :
        oldData = self.get_geography_by_id(geography_id)
        if bool(oldData) is False:
            return False
        oldparent_ids = oldData["parent_ids"]

        table_name = "tbl_geographies"
        field_with_data = "geography_name='%s', parent_ids='%s', updated_by=%s " % (
            name, parent_ids, updated_by
        )

        where_condition = "geography_id = %s" % (geography_id)
        
        self.update_data(table_name, field_with_data, where_condition)
        action = "Geography - %s updated" % name
        self.save_activity(updated_by, 6, action)
        return True

        # if oldparent_ids != parent_ids :
        #     oldPId = str(oldparent_ids) + str(geography_id)
        #     newPId = str(parent_ids) + str(geography_id)
        #     qry = "SELECT geography_id, geography_name, parent_ids from tbl_geographies \
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

    def change_geography_status(self,geography_id, is_active, updated_by) :
        oldData = self.get_geography_by_id(geography_id)
        if bool(oldData) is False:
            return False
        table_name = "tbl_geographies"
        field_with_data = "is_active=%s, updated_by=%s"  % (
            int(is_active), int(updated_by)
        )
        where_condition = "geography_id = %s" %  (int(geography_id))
        if (self.update_data(table_name, field_with_data, where_condition)) :
            print "update status"
            if is_active == 0:
                status = "deactivated"
            else:
                status = "activated"
            action = "Geography %s status  - %s" % (oldData["geography_name"], status)
            self.save_activity(updated_by, 6, action)
            return True

    def get_statutory_by_id(self, statutory_id):
        query = "SELECT statutory_id, statutory_name, level_id, parent_ids, is_active \
            FROM tbl_statutories WHERE statutory_id = %s" % (statutory_id)
        rows = self.select_one(query)
        result = []
        if rows :
            columns = ["statutory_id", "statutory_name", "level_id", "parent_ids", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_statutory(self, parent_ids, statutory_id) :
        query = "SELECT statutory_id, statutory_name, level_id, is_active \
            FROM tbl_statutories WHERE parent_ids='%s' " % (parent_ids)
        if statutory_id is not None :
            query = query + " AND statutory_id != %s" % statutory_id
        
        rows = self.select_all(query)
        columns = ["statutory_id", "statutory_name", "level_id", "is_active"]
        return self.convert_to_dict(rows, columns)

    def get_statutory_master(self, statutory_id = None): 
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



    def save_statutory(self, name, level_id, parent_ids, user_id) :
        is_saved = False
        statutory_id = self.get_new_id("statutory_id", "tbl_statutories")
        created_on = self.get_date_time()
        table_name = "tbl_statutories"
        field = "(statutory_id, statutory_name, level_id, \
            parent_ids, created_by, created_on)"
        data = (
            statutory_id, name, int(level_id), parent_ids, 
            int(user_id), str(created_on)
        )

        if (self.save_data(db, field, data)) :
            action = "Statutory - %s added" % name
            self.save_activity(user_id, 12, action)
            is_saved = True
        return is_saved

    def update_statutory(self, statutory_id, name, parent_ids, updated_by) :
        oldData = self.get_statutory_by_id(statutory_id)
        if bool(oldData) is False:
            return False
        oldparent_ids = oldData["parent_ids"]

        table_name = "tbl_statutories"
        field_with_data = "statutory_name='%s', parent_ids='%s', updated_by=%s " % (
            name, parent_ids, updated_by
        )

        where_condition = "statutory_id = %s" % (statutory_id)
        
        self.update_data(table_name, field_with_data, where_condition)
        action = "Statutory - %s updated" % name
        self.save_activity(updated_by, 6, action)
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
            statutory_id = row["statutory_id"]
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
                statutory_name, mappings
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
            mappings = '>>'.join(str(x) for x in names)
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
                c_approval = core.ComplianceApprovalStatus(
                    sts[0], approve
                )
                approval_list.append(c_approval)
            return approval_list

        status = ("Pending", "Approve", "Reject", "Approve & Notify")
        
        if approval_id is None :
            return return_approval_status(status)
        else :
            return status[int(approval_id)]

    def get_statutory_mappings(self, user_id) :
        q = "SELECT t1.statutory_mapping_id, t1.country_id, \
            t2.country_name, t1.domain_id, t3.domain_name, \
            t1.industry_ids, t1.statutory_nature_id, \
            t4.statutory_nature_name, t1.statutory_ids, \
            t1.compliance_ids, t1.geography_ids, \
            t1.approval_status, t1.is_active  \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_countries t2 \
            ON t1.country_id = t2.country_id \
            INNER JOIN tbl_domains t3 \
            ON t1.domain_id = t3.domain_id \
            INNER JOIN tbl_statutory_natures t4 \
            ON t1.statutory_nature_id = t4.statutory_nature_id \
            INNER JOIN tbl_user_domains t5 \
            ON t1.domain_id = t5.domain_id \
            and t5.user_id = %s \
            INNER JOIN tbl_user_countries t6 \
            ON t1.country_id = t6.country_id \
            and t6.user_id = %s" %(user_id, user_id)
        rows = self.select_all(q)
        columns = [
            "statutory_mapping_id", "country_id", 
            "country_name", "domain_id", "domain_name", "industry_ids", 
            "statutory_nature_id", "statutory_nature_name", 
            "statutory_ids", "compliance_ids", "geography_ids",
            "approval_status", "is_active"
        ]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return self.return_statutory_mappings(result)

    def return_statutory_mappings(self, data):
        mapping_data_list = {}
        for d in data :
            mapping_id = int(d["statutory_mapping_id"])
            industry_names = ""
            compliance_ids = d["compliance_ids"]
            compliances_data = self.get_compliance_by_id (
                compliance_ids
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
                statutory_mapping_list.append(
                    self.statutory_parent_mapping.get(int(g_id))[1]
                )
            approval_status = self.get_approval_status(
                int(d["approval_status"])
            )
            industry_ids = [
                int(x) for x in d["industry_ids"][:-1].split(',')
            ]
            statutory = core.StatutoryMapping(
                d["country_id"], d["country_name"],
                d["domain_id"], d["domain_name"],
                industry_ids, industry_names,
                d["statutory_nature_id"], d["statutory_nature_name"],
                statutory_ids, statutory_mapping_list,
                compliances, compliance_names, geography_ids,
                geography_mapping_list, int(d["approval_status"]),
                bool(d["is_active"]),
            )
            mapping_data_list[mapping_id] = statutory
        return mapping_data_list

    def get_statutory_mapping_report(
        self, country_id, domain_id, industry_id, 
        statutory_nature_id, geography_id
    ) :
        q = "SELECT t1.statutory_mapping_id, t1.country_id, \
            t2.country_name, t1.domain_id, t3.domain_name, \
            t1.industry_ids, t1.statutory_nature_id, \
            t4.statutory_nature_name, t1.statutory_ids, \
            t1.compliance_ids, t1.geography_ids, \
            t1.approval_status, t1.is_active  \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_countries t2 \
            ON t1.country_id = t2.country_id \
            INNER JOIN tbl_domains t3 \
            ON t1.domain_id = t3.domain_id \
            INNER JOIN tbl_statutory_natures t4 \
            ON t1.statutory_nature_id = t4.statutory_nature_id \
            INNER JOIN tbl_user_domains t5 \
            ON t1.domain_id = t5.domain_id \
            and t5.user_id = %s \
            INNER JOIN tbl_user_countries t6 \
            ON t1.country_id = t6.country_id \
            and t6.user_id = %s \
            WHERE t1.country_id = %s \
            and t1.domain_id = %s \
            and t1.industry_ids like '%s' \
            and t1.statutory_nature_id like '%s' \
            and t1.geography_ids like '%s'" % (
                user_id, user_id,
                country_id, domain_id, 
                str("%" + str(industry_id) + ",%"), 
                str(statutory_nature_id),
                str("%" + str(geography_id) + ",%")
            )

        rows = self.select_all(q)
        columns = [
            "statutory_mapping_id", "country_id", 
            "country_name", "domain_id", "domain_name", "industry_ids", 
            "statutory_nature_id", "statutory_nature_name", 
            "statutory_ids", "compliance_ids", "geography_ids",
            "approval_status", "is_active"
        ]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        report_data = {}
        for r in result :
            report_data[r.statutory_mapping_id] = r
        return self.return_knowledge_report(
            country_id, domain_id, report_data
        )


    def get_mappings_id(self, statutory_id) :
        query = "SELECT t1.statutory_mapping_ids from tbl_statutories t1 \
            WHERE t1.parent_ids like '%0%' OR t1.parent_ids like '%s'" % str("%" + str(statutory_id) + ",%")
        rows = self.select_all(query)
        result = []
        if rows :
            result = self.convert_to_dict(
                rows, ["statutory_mapping_ids"]
            )
        return result


    def return_knowledge_report(self, country_id, domain_id, report_data):
        level_1_statutory = self.get_country_wise_level_1_statutoy()

        level1s = level_1_statutory[country_id][domain_id]
        level_1_mappings = {}
        for x in level1s :
            statutory_id = x.statutory_id
            rows = self.get_mappings_id(statutory_id)
            mapping_list = []
            for row in rows :
                mapping_ids = row["statutory_mapping_ids"]
                if (mapping_ids is None) or (mapping_ids == "") :
                    continue
                def getData(i) :
                    return report_data.get(int(i))
                mapping_list.extend(
                    [getData(x) for x in mapping_ids[:-1].split(',') if getData(x) is not None]  
                )
            level_1_mappings[statutory_id] = mapping_list
        return level_1_mappings


    #
    # compliance
    #
    def get_compliance_by_id(self, compliance_id):
        if type(compliance_id) == IntType :
            q = " WHERE t1.compliance_id = %s" % (
                compliance_id
            )
        else :
            q = " WHERE t1.compliance_id in %s" % (
                str(tuple(compliance_id))
            )

        qry = "SELECT t1.compliance_id, t1.statutory_provision, \
            t1.compliance_task, t1.compliance_description, \
            t1.document_name, t1.format_file, \
            t1.penal_consequences, t1.frequency_id, \
            t1.statutory_dates, t1.repeats_every, \
            t1.repeats_type_id, \
            t1.duration, t1.duration_type_id, t1.is_active \
            FROM tbl_compliances t1 %s" % q
        rows = self.select_all(qry)
        columns = [
            "compliance_id", "statutory_provision", 
            "compliance_task", "compliance_description", 
            "document_name","format_file", "penal_consequences",
            "frequency_id", "statutory_dates", "repeats_every",
            "repeats_type_id", "duration", "duration_type_id",
            "is_active"
        ]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return self.return_compliance(result)

    def return_compliance(self, data):
        compliance_names =  []
        compalinaces = []
        for d in data :
            statutory_dates = d["statutory_dates"]
            statutory_dates = json.loads(statutory_dates)
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"]
                )
                date_list.append(s_date)



            compliance_task = d["compliance_task"]
            document_name = d["document_name"]
            name = "%s - %s" % (
                document_name, compliance_task
            )
            format_file = d["format_file"]
            if not format_file :
                format_file = None

            compliance_names.append(name)
            compliance = core.Compliance(
                d["compliance_id"], d["statutory_provision"],
                compliance_task, d["compliance_description"],
                document_name, format_file,
                d["penal_consequences"], d["frequency_id"],
                date_list, d["repeats_type_id"],
                d["repeats_every"], d["duration_type_id"],
                d["duration"], bool(d["is_active"])
            )
            compalinaces.append(compliance)
        return [compliance_names, compalinaces]


    #
    # save statutory mapping
    #

    def save_statutory_mapping(self, data, created_by) :
        country_id =data.country_id
        domain_id =data.domain_id
        industry_ids = ','.join(str(x) for x in data.industry_ids) + ","
        nature_id =data.statutory_nature_id
        statutory_ids = ','.join(str(x) for x in data.statutory_ids) + ","
        compliances = data.compliances
        geography_ids = ','.join(str(x) for x in data.geography_ids) + ","
        statutory_mapping_id = self.get_new_id("statutory_mapping_id", "tbl_statutory_mappings")
        created_on = self.get_date_time()
        is_active = 1

        statutory_table = "tbl_statutory_mappings"
        field = "(statutory_mapping_id, country_id, domain_id, \
            industry_ids, statutory_nature_id, statutory_ids, \
            geography_ids, is_active, created_by, created_on)"
        data = (
            statutory_mapping_id, int(country_id), int(domain_id), 
            industry_ids, int(nature_id), statutory_ids, 
            geography_ids, int(is_active), 
            int(created_by), str(created_on)
        )
        if (self.save_data(statutory_table, field, data)) :            
            self.update_statutory_mapping_id(
                data.statutory_ids, 
                statutory_mapping_id, created_by
            )
            ids = self.save_compliance(
                statutory_mapping_id, compliances, created_by
            )
            compliance_ids = ','.join(str(x) for x in ids) + ","
            qry = "UPDATE tbl_statutory_mappings set compliance_ids='%s' \
                where statutory_mapping_id = %s" % (compliance_ids, statutory_mapping_id)
            self.execute(qry)
            action = "New statutory mappings added"
            self.save_activity(created_by, 17, action)
            return True
        else :
            return False

    def update_statutory_mapping_id(
        self, statutory_id, mapping_id, user_id
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

        for x in difference :
            old_map_id =  [int(j) for j in old_statu_ids.get(x).split(',')]
            old_map_id = old_map_id.remove(mapping_id)

            new_map_id = ""
            if old_map_id is not None : 
                new_map_id = ','.join(str(k) for k in old_map_id) + ","

            qry1 = "UPDATE tbl_statutories set statutory_mapping_ids = '%s', updated_by = %s \
                WHERE statutory_id = %s" % (new_map_id, updated_by, x)
            if (self.execute(qry1)) :
                print "Mapping Id %s removed from statutory table, Id=%s" % (mapping_id, x)


        # statutory_ids = statutory_ids[:-1]
        # ids = [int(x) for x in statutory_ids.split(',')]
        ids = tuple(statutory_ids)
        if (len(ids) == 1) :
            qry_where = " WHERE statutory_id = %s" % ids[0]
        else :
            qry_where = " WHERE statutory_id in %s" % str(ids)

        qry = "SELECT statutory_id, statutory_mapping_ids from tbl_statutories %s" % qry_where
        isUpdated = False
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
                _statutory_mapping_id = ','.join(str(x) for x in mapping_ids) + ","
            query = "UPDATE tbl_statutories set statutory_mapping_ids = '%s', updated_by = %s \
                WHERE statutory_id = %s" % (
                _statutory_mapping_id, updated_by, statutory_id
            )
            isUpdated = self.execute(query)
        return isUpdated

    def save_compliance(self, mapping_id, datas, created_by) :
        compliance_ids = []
        for data in datas :
            compliance_id = self.get_new_id(
                "compliance_id", "tbl_compliances"
            )
            created_on = self.get_date_time()

            provision = data.statutory_provision
            compliance_task = data.compliance_task
            compliance_description = data.description
            document_name = data.document_name
            format_file = ','.join(str(x) for x in data.format_file_name)
            penal_consequences = data.penal_consequences
            compliance_frequency = data.frequency_id
            statutory_dates =  json.dumps(data.statutory_dates)
            repeats_every = data.repeats_every
            repeats_type = data.repeats_type_id
            duration = data.duration
            duration_type = data.duration_type_id
            is_active = data.is_active

            if compliance_frequency == 1 :
                query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
                    compliance_task, compliance_description, document_name, format_file, \
                    penal_consequences, frequency_id, statutory_dates, statutory_mapping_id, \
                    is_active, created_by, created_on) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                    '%s', %s, %s, %s, '%s')" % (compliance_id, provision, compliance_task, 
                    compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
                    statutory_dates, mapping_id, is_active, created_by, created_on)

            elif compliance_frequency == 4 :
                query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
                    compliance_task, compliance_description, document_name, format_file, \
                    penal_consequences, frequency_id, statutory_dates, duration, \
                    duration_type_id, statutory_mapping_id, \
                    is_active, created_by, created_on) VALUES (%s,'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, \
                    '%s', %s, %s, %s, '%s')" % (compliance_id, provision, compliance_task, 
                    compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
                    statutory_dates, int(duration), duration_type, mapping_id, is_active, created_by, created_on)

            else :
                query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
                    compliance_task, compliance_description, document_name, format_file, \
                    penal_consequences, frequency_id, statutory_dates, repeats_every, \
                    repeats_type_id, statutory_mapping_id, \
                    is_active, created_by, created_on) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                    %s, '%s', %s, %s, %s, '%s')"  % (compliance_id, provision, compliance_task, 
                    compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
                    statutory_dates, int(repeats_every), repeats_type, mapping_id, is_active, created_by, created_on)

            if (self.execute(query)) :
                compliance_ids.append(compliance_id)

        return compliance_ids

    def update_statutory_mapping(self, data, updated_by) :
        statutory_mapping_id = data.statutory_mapping_id
        country_id =data.country_id
        domain_id =data.domain_id
        industry_ids = ','.join(str(x) for x in data.industry_ids) + ","
        nature_id =data.statutory_nature_id
        statutory_ids = ','.join(str(x) for x in data.statutory_ids) + ","
        compliances = data.compliances
        geography_ids = ','.join(str(x) for x in data.geography_ids) + ","

        self.save_statutory_backup(statutory_mapping_id, updated_by)
        query = "UPDATE tbl_statutory_mappings set country_id=%s, domain_id=%s, industry_ids='%s', \
            statutory_nature_id=%s, statutory_ids='%s', geography_ids='%s', approval_status=0, rejected_reason=NULL, updated_by=%s \
            WHERE statutory_mapping_id=%s" % (
                country_id, domain_id, industry_ids, nature_id, statutory_ids, geography_ids,
                updated_by, statutory_mapping_id
            )

        if (self.execute(query)) :
            print "update mapping"
            self.update_statutory_mapping_id(data.statutory_ids, statutory_mapping_id, updated_by)
            ids = self.update_compliance(statutory_mapping_id, compliances, updated_by)
            compliance_ids = ','.join(str(x) for x in ids) + ","
            qry = "UPDATE tbl_statutory_mappings set compliance_ids='%s' \
                where statutory_mapping_id = %s" % (compliance_ids, statutory_mapping_id)
            self.execute(qry)
            action = "Edit Statutory Mappings"
            self.save_activity(updated_by, 17, action)
            return True
        else :
            return False

    def update_compliance(self, mapping_id, datas, updated_by) :
        compliance_ids = []
        for data in datas :
            compliance_id = data.compliance_id
            if (compliance_id == "") :
                ids = self.save_compliance(mapping_id, [data], updated_by)
                compliance_ids.extend(ids)
                continue
            provision = data.statutory_provision
            compliance_task = data.compliance_task
            description = data.description
            document_name = data.document_name
            format_file = ','.join(str(x) for x in data.format_file_name)
            penal_consequences = data.penal_consequences
            compliance_frequency = data.frequency_id
            statutory_dates =  json.dumps(data.statutory_dates)
            repeats_every = data.repeats_every
            repeats_type = data.repeats_type_id
            duration = data.duration
            duration_type = data.duration_type_id
            is_active = int(data.is_active)

            if compliance_frequency == 1 :
                query = "UPDATE tbl_compliances set statutory_provision = '%s', \
                    compliance_task = '%s', compliance_description = '%s', document_name = '%s' , format_file = '%s', \
                    penal_consequences = '%s', frequency_id = '%s', statutory_dates = '%s', statutory_mapping_id = %s, \
                    is_active = %s, updated_by = %s WHERE compliance_id = %s "  % (
                        provision, compliance_task, 
                        description, document_name, format_file, penal_consequences, compliance_frequency,
                        statutory_dates, mapping_id, is_active, updated_by, compliance_id
                    )

            elif compliance_frequency == 4 :
                query = "UPDATE tbl_compliances set statutory_provision='%s', \
                    compliance_task='%s', compliance_description='%s', document_name='%s', format_file='%s', \
                    penal_consequences='%s', frequency_id='%s', statutory_dates='%s', duration=%s, \
                    duration_type_id='%s', statutory_mapping_id = %s, \
                    is_active = %s, updated_by = %s WHERE compliance_id = %s "% (
                        provision, compliance_task, 
                        description, document_name, format_file, penal_consequences, compliance_frequency,
                        statutory_dates, int(duration), duration_type, mapping_id, is_active, updated_by, compliance_id
                    )

            else :
                query = "UPDATE tbl_compliances set statutory_provision ='%s', \
                    compliance_task ='%s', compliance_description='%s', document_name='%s', format_file='%s', \
                    penal_consequences='%s', frequency_id='%s', statutory_dates='%s', repeats_every=%s, \
                    repeats_type_id='%s', statutory_mapping_id=%s, \
                    is_active=%s, updated_by=%s WHERE compliance_id = %s "  % (
                        provision, compliance_task, 
                        description, document_name, format_file, penal_consequences, compliance_frequency,
                        statutory_dates, int(repeats_every), repeats_type, mapping_id, is_active, updated_by, compliance_id
                    )

            if (self.execute(query)) :
                compliance_ids.append(compliance_id)

        return compliance_ids

    def change_compliance_status(self, mapping_id, is_active, updated_by) :
        query = "UPDATE tbl_compliances set is_active=%s, \
            updated_by=%s WHERE statutory_mapping_id=%s" % (
                is_active, updated_by, mapping_id
            )
        return self.execute(query)

    def chenge_statutory_mapping_status(self, data, updated_by):
        statutory_mapping_id = data.statutory_mapping_id
        is_active = data.is_active

        query = "UPDATE tbl_statutory_mappings set is_active=%s, updated_by=%s \
            WHERE statutory_mapping_id=%s" % (
            is_active, updated_by, statutory_mapping_id
        )
        if (self.execute(query)) :
            self.change_compliance_status(statutory_mapping_id, is_active, updated_by)
            if is_active == 0:
                status = "deactivated"
            else:
                status = "activated"
            action = "Statutory Mapping status changed"
            self.save_activity(updated_by, 17, action)
            return True

    def save_statutory_backup(self, statutory_mapping_id, created_by):
        old_record = self.get_statutory_mapping_by_id(statutory_mapping_id)
        backup_id = self.get_new_id("statutory_backup_id", "tbl_statutories_backup")
        created_on = self.get_date_time()
        industry_ids = [
            int(x) for x in old_record["industry_ids"][:-1].split(',')
        ]
        industry_name = self.get_industry_by_id(industry_ids)

        provision = []
        for sid in old_record["statutory_ids"][:-1].split(',') :
            data = self.statutory_parent_mapping.get(int(sid))
            provision.append(data)
        mappings = ','.join(str(x) for x in provision)
        
        geo_map = []
        for gid in old_record["geography_ids"][:-1].split(',') :
            data = self.geography_parent_mapping.get(int(geo_map))
            if data is not None :
                data = data[0]
            geo_map.append(data)
        geo_mappings = ','.join(str(x) for x in geo_map)
        
        q = "INSERT INTO tbl_statutories_backup \
            (statutory_backup_id, statutory_mapping_id, \
            country_name, domain_name, industry_name, \
            statutory_nature, statutory_provision, \
            applicable_location, created_by, created_on) \
            VALUES(%s, %s, '%s', '%s', '%s', '%s', '%s', \
                '%s', %s, '%s') " % (
                backup_id, statutory_mapping_id, 
                old_record["country_name"], 
                old_record["domain_name"], 
                industry_name, old_record["statutory_nature"], 
                mappings, 
                geo_mappings, created_by, created_on
            )
        if (self.execute(q)) :
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

    def get_statutory_mapping_by_id (self, mapping_id) :
        q = "SELECT t1.country_id, t2.country_name, \
            t1.domain_id, t3.domain_name, t1.industry_ids, \
            t1.statutory_nature_id, t4.statutory_nature_name, \
            t1.statutory_ids, t1.compliance_ids, \
            t1.geography_ids, t1.approval_status  \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_countries t2 \
            on t1.country_id = t2.country_id \
            INNER JOIN tbl_domains t3 \
            on t1.domain_id = t3.domain_id \
            INNER JOIN tbl_statutory_natures t4 \
            on t1.statutory_nature_id = t4.statutory_nature_id \
            WHERE t1.statutory_mapping_id=%s" % mapping_id
        rows = self.select_all(q)
        columns = [
            "country_id", "country_name", "domain_id",
            "domain_name", "industry_ids", "statutory_nature_id",
            "statutory_nature_name", "statutory_ids",
            "compliance_ids", "geography_ids",
            "approval_status"            
        ]
        result = []
        if rows :
            result = self.convert_to_dict(rows, columns)
        return result

    def change_approval_status(self, data, updated_by) :
        statutory_mapping_id = data.statutory_mapping_id
        provision = data.statutory_provision
        approval_status = data.approval_status
        rejected_reason = data.rejected_reason
        notification_text = data.notification_text

        if approval_status == 2 :
            #Rejected
            query = "UPDATE tbl_statutory_mappings set \
                approval_status='%s', rejected_reason='%s', \
                updated_by=%s WHERE \
                statutory_mapping_id = %s" % (
                    approval_status, rejected_reason, updated_by, statutory_mapping_id
                )
            self.execute(query)
            notification_log_text = "Statutory Mapping: %s \
                has been Rejected" % (provision)
        else :
            
            query = "UPDATE tbl_statutory_mappings set \
                approval_status='%s', \
                updated_by=%s WHERE \
                statutory_mapping_id = %s" % (
                    approval_status, updated_by, 
                    statutory_mapping_id
                )
            self.execute(query)
            notification_log_text = "Statutory Mapping: %s \
                has been Approved" % (provision)            
            if approval_status == 3 :
                self.save_statutory_notifications(
                    statutory_mapping_id, notification_text
                )
                notification_log_text = "Statutory Mapping: %s \
                    has been Approve & Notified" % (provision)
        
        link = "/statutorymapping/list"
        self.save_notifications(notification_log_text, link)
        action = "Statutory Mapping approval status changed"
        self.save_activity(updated_by, 17, action)
        return True

    def save_notifications(self, notification_text, link):
        #internal notification
        notification_id = self.get_new_id(
            "notification_id", "tbl_notifications"
        )
        query = "INSERT INTO tbl_notifications \
            (notification_id, notification_text, link) \
            VALUES (%s, '%s', '%s')" % (
                notification_id, notification_text, link
            )
        self.execute(query)

    def save_statutory_notifications(self, mapping_id, notification_text ):
        # client notification
        old_record = self.get_statutory_mapping_by_id(
            mapping_id
        )
        industry_ids = [
            int(x) for x in old_record["industry_ids"][:-1].split(',')
        ]
        industry_name = self.get_industry_by_id(industry_ids)

        provision = []
        for sid in old_record["statutory_ids"][:-1].split(',') :
            data = self.statutory_parent_mapping.get(int(sid))
            provision.append(data)
        mappings = ','.join(str(x) for x in provision)
        geo_map = []
        for gid in old_record["geography_ids"][:-1].split(',') :
            data = self.geography_parent_mapping.get(int(gid))
            if data is not None :
                data = data[0]
            geo_map.append(data)
        geo_mappings = ','.join(str(x) for x in geo_map)

        notification_id = self.get_new_id(
            "statutory_notification_id", 
            "tbl_statutory_notifications_log"
        )

        query = " INSERT INTO tbl_statutory_notifications_log \
            (statutory_notification_id, statutory_mapping_id, \
            country_name, domain_name, industry_name, \
            statutory_nature, statutory_provision, \
            applicable_location, notification_text) \
            VALUES \
            (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s') \
            " % (
                notification_id, mapping_id, 
                old_record["country_name"], 
                old_record["domain_name"], industry_name, 
                old_record["statutory_nature"], 
                mappings, geo_mappings,notification_text
            )
        self.execute(query)


    #
    #   Forms
    #
    def get_forms(self):
        columns = "tf.form_id, tf.form_category_id, tfc.form_category, "+\
        "tf.form_type_id, tft.form_type, tf.form_name, tf.form_url, "+\
        "tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormCategory, self.tblFormType]
        aliases = ["tf", "tfc", "tft"]
        joinConditions = ["tf.form_category_id = tfc.form_category_id", 
        "tf.form_type_id = tft.form_type_id"]
        whereCondition = " tf.form_category_id in (3,2,4) order by tf.form_order"
        joinType = "left join"

        rows = self.get_data_from_multiple_tables(columns, tables, aliases, joinType, 
            joinConditions, whereCondition)
        return rows

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
        columns = "user_group_id, user_group_name, form_category_id, "+\
                    "form_ids, is_active"
        tables = self.tblUserGroups
        where_condition = "1"
        rows = self.get_data( tables, columns, where_condition)
        return rows

    def get_user_groups(self):
        columns = "user_group_id, user_group_name, is_active"
        where_condition = "1"
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
        return result

    def update_user_group(self, user_group_id, user_group_name,
            form_category_id, form_ids):
        time_stamp = self.get_date_time()
        columns = ["user_group_name","form_category_id","form_ids", "updated_on",
                 "updated_by"]
        values =  [user_group_name, form_category_id, 
                ",".join(str(x) for x in form_ids), time_stamp, 0]
        condition = "user_group_id='%d'" % user_group_id
        return self.update(self.tblUserGroups, columns, values, condition)

    def update_user_group_status(self, user_group_id, is_active):
        time_stamp = self.get_date_time()
        columns = ["is_active", "updated_by", "updated_on"]
        values = [is_active, 0, time_stamp]
        condition = "user_group_id='%d'" % user_group_id
        result =  self.update(self.tblUserGroups, columns, values, condition)
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

    def get_users(self):
        columns = "user_id, employee_name, employee_code, is_active"
        condition = "1"
        rows = self.get_data(self.tblUsers, columns, condition)
        return rows

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
        columns = "group_concat(client_id)"
        condition = " user_id = '%d'"% user_id
        rows = self.get_data(self.tblUserClients, columns, condition)
        return rows[0][0]

    def save_user(self, user_id, email_id, user_group_id, employee_name,
     employee_code, contact_no, address, designation, country_ids, domain_ids):
        result1 = False
        result2 = False
        result3 = False
        current_time_stamp = self.get_date_time()
        user_columns = ["user_id", "email_id", "user_group_id", "password", "employee_name", 
                    "employee_code", "contact_no", "address", "designation", "is_active", 
                    "created_on", "created_by", "updated_on", "updated_by"]
        user_values = [user_id, email_id, user_group_id, self.generate_password(),
                employee_name, employee_code, contact_no, address,
                designation, 1, current_time_stamp, 0, current_time_stamp, 0]
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

        return (result1 and result2 and result3)    

    def update_user_status(self, user_id, is_active):
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [is_active, self.get_date_time(), 0]
        condition = "user_id='%d'" % user_id
        return self.update(self.tblUsers, columns, values, condition)

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

    def get_group_company_details(self):
        columns = "client_id, group_name, email_id, logo_url,  contract_from, contract_to,"+\
        " no_of_user_licence, total_disk_space, is_sms_subscribed,  incharge_persons,"+\
        " is_active"
        condition = "1"
        return self.get_data(self.tblClientGroups, columns, condition)

    def get_group_companies_for_user(self, user_id):
        client_ids = self.get_user_clients(user_id)
        columns = "client_id, group_name,  is_active"
        condition = "client_id in (%s)" % client_ids
        rows = self.get_data(self.tblClientGroups, columns, condition) 
        columns = ["client_id", "group_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_group_companies(result)

    def return_group_companies(self, group_companies):
        results = []
        for group_company in group_companies :
            results.append(core.GroupCompany(
                group_company["client_id"], group_company["group_name"], 
                bool(group_company["is_active"]), self.get_client_countries(
                group_company["client_id"]),self.get_client_domains(
                group_company["client_id"])
            ))
        return results       

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

    def save_date_configurations(self, client_id, date_configurations, session_user):
        values_list = []
        current_time_stamp = self.get_date_time()
        columns = ["client_id", "country_id" ,"domain_id", "period_from", 
        "period_to", "updated_by", "updated_on"]
        condition = "client_id='%d'"%client_id
        self.delete(self.tblClientConfigurations, condition)
        for configuration in date_configurations:
            country_id = configuration.country_id
            domain_id = configuration.domain_id
            period_from = configuration.period_from
            period_to = configuration.period_to
            values_tuple = (client_id, country_id, domain_id, period_from, period_to, 
                 int(session_user), str(current_time_stamp))
            values_list.append(values_tuple)
        return self.bulk_insert(self.tblClientConfigurations,columns,values_list)

    def save_client_countries(self, client_id, country_ids):
        values_list = []
        columns = ["client_id", "country_id"]
        condition = "client_id = '%d'" % client_id
        self.delete(self.tblClientCountries, condition)
        for country_id in country_ids:
            values_tuple = (client_id, country_id)
            values_list.append(values_tuple)
        return self.bulk_insert(self.tblClientCountries, columns, values_list)

    def save_client_domains(self, client_id, domain_ids):
        values_list = []
        columns = ["client_id", "domain_id"]
        condition = "client_id = '%d'" % client_id
        self.delete(self.tblClientDomains, condition)
        for domain_id in domain_ids:
            values_tuple = (client_id, domain_id)
            values_list.append(values_tuple)
        return self.bulk_insert(self.tblClientDomains, columns, values_list)

    def _mysql_server_connect(self, host, username, password):
        return mysql.connect(host, username, password)

    def _db_connect(self, host, username, password, database) :
        return mysql.connect(host, username, password, 
            database)

    def _create_database(self, host, username, password, 
        database_name, db_username, db_password, email_id, client_id):
        con = self._mysql_server_connect(host, username, password)
        cursor = con.cursor()
        query = "CREATE DATABASE %s" % database_name
        cursor.execute(query)
        query = "grant all privileges on %s.* to %s@%s IDENTIFIED BY '%s';" %(
            database_name, db_username, host, db_password)
        con.commit()

        con = self._db_connect(host, username, password, database_name)
        cursor = con.cursor()
        sql_script_path = os.path.join(os.path.join(os.path.split(__file__)[0]), 
        "scripts/mirror-client.sql")
        file_obj = open(sql_script_path, 'r')
        sql_file = file_obj.read()
        file_obj.close()
        sql_commands = sql_file.split(';')
        size = len(sql_commands)
        for index,command in enumerate(sql_commands):
            if (index < size-1):
                cursor.execute(command)
            else:
                break
        query = "insert into tbl_admin (username, password) values ('%s', '%s')"%(
            email_id, self.generate_password())        
        cursor.execute(query)
        return True

    def _get_server_details(self):
        columns = "ip, server_username,server_password"
        condition = "server_full = 0 order by length ASC limit 1"
        rows = self.get_data(self.tblDatabaseServer, columns, condition)
        return rows[0]

    def create_and_save_client_database(self, group_name, client_id, short_name, email_id):
        group_name = re.sub('[^a-zA-Z0-9 \n\.]', '', group_name)
        group_name = group_name.replace (" ", "")
        database_name = "mirror_%s_%d" %(group_name.lower(),client_id)
        row = self._get_server_details()
        host = row[0]
        username = row[1]
        password = row[2]
        db_username = self.generate_random()
        db_password = self.generate_random()

        if self._create_database(host, username, password, database_name, db_username, 
            db_password, email_id, client_id):
            db_server_column = "company_ids"
            db_server_value = client_id
            db_server_condition = "ip='%s'"% host
            self.append(self.tblDatabaseServer, db_server_column, db_server_value,
                db_server_condition)
            db_server_column = "length"
            self.increment(self.tblDatabaseServer, db_server_column,
                db_server_condition)

            machine_columns = "client_ids"
            machine_value = db_server_value
            machine_condition = db_server_condition
            self.append(self.tblMachines, machine_columns, machine_value,
                machine_condition)

            rows = self.get_data(self.tblMachines, "machine_id", machine_condition)
            machine_id = rows[0][0]

            client_db_columns = ["client_id", "machine_id", "database_ip", 
                    "database_port", "database_username", "database_password",
                    "client_short_name", "database_name"]
            client_dB_values = [client_id, machine_id, host, 90, db_username,
            db_password, short_name, database_name]

            return self.insert(self.tblClientDatabase, client_db_columns, client_dB_values)

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
        values = [client_id, client_group.group_name, client_group.email_id,
        client_group.logo, 1200, contract_from, contract_to,
        client_group.no_of_user_licence, client_group.file_space * 10000, 
        is_sms_subscribed, client_group.short_name, 
        ','.join(str(x) for x in client_group.incharge_persons),1, session_user,
        current_time_stamp, session_user, current_time_stamp]
        result = self.insert(self.tblClientGroups, columns, values)
        return result

    def update_client_group(self, client_group, session_user):
        current_time_stamp = self.get_date_time()
        contract_from = self.string_to_datetime(client_group.contract_from)
        contract_to = self.string_to_datetime(client_group.contract_to)
        is_sms_subscribed = 0 if client_group.is_sms_subscribed == False else 1

        columns = ["group_name", "logo_url", "logo_size", "contract_from", 
        "contract_to", "no_of_user_licence", "total_disk_space", "is_sms_subscribed", 
        "incharge_persons", "is_active", "updated_by", "updated_on"]
        values = [client_group.group_name, client_group.logo,1200, contract_from, contract_to,
        client_group.no_of_user_licence, client_group.file_space, is_sms_subscribed,
        ','.join(str(x) for x in client_group.incharge_persons),1, session_user,
        current_time_stamp]
        condition = "client_id = '%d'" % client_group.client_id
        return self.update(self.tblClientGroups, columns, values, condition)

    def save_client_user(self, client_group, session_user):
        columns = ["client_id", "user_id",  "email_id", 
        "employee_name", "created_on", "is_admin", "is_active"]
        values = [client_group.client_id, 0, self.username, "Admin",
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

    def update_client_group_status(self, client_id, is_active, session_user):
        columns = ["is_active", "updated_by", "updated_on"]
        values = [ is_active, int(session_user), self.get_date_time()]
        condition = "client_id='%d'" % client_id
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
        return self.insert(self.tblBusinessGroups, columns, values)

    def update_business_group(self, client_id, business_group_id, business_group_name, 
        session_user):
        current_time_stamp = self.get_date_time()
        columns = ["business_group_name", "updated_by", "updated_on"]
        values = [business_group_name, session_user, current_time_stamp]
        condition = "business_group_id = '%d' and client_id = '%d'"%(business_group_id, client_id)
        return self.update(self.tblBusinessGroups, columns, values, condition)

    def save_legal_entity(self, client_id, legal_entity_id, legal_entity_name, 
        business_group_id, session_user):
        current_time_stamp = self.get_date_time()
        columns = ["client_id", "legal_entity_id", "legal_entity_name", "business_group_id", 
        "created_by", "created_on", "updated_by", "updated_on"]
        values = [client_id, legal_entity_id, legal_entity_name, business_group_id, 
        session_user, current_time_stamp, session_user, current_time_stamp]
        return self.insert(self.tblLegalEntities, columns, values)

    def update_legal_entity(self, client_id, legal_entity_id, legal_entity_name, business_group_id, session_user):
        current_time_stamp = self.get_date_time()
        columns = ["legal_entity_name", "updated_by", "updated_on"]
        values = [legal_entity_name, session_user, self.get_date_time()]
        condition = "legal_entity_id = '%d' and client_id = '%d'"%(legal_entity_id, client_id)
        return self.update(self.tblLegalEntities, columns, values, condition)

    def save_division(self, client_id, division_id, division_name, business_group_id, legal_entity_id, session_user):
        current_time_stamp = self.get_date_time()
        columns = ["client_id", "division_id", "division_name", "business_group_id", "legal_entity_id",
        "created_by", "created_on", "updated_by", "updated_on"]
        values = [client_id, division_id, division_name, business_group_id, legal_entity_id,
        session_user, current_time_stamp, session_user, current_time_stamp]
        return self.insert(self.tblDivisions, columns, values)

    def update_division(self, client_id, division_id, division_name, business_group_id, legal_entity_id, session_user):
        current_time_stamp = self.get_date_time()
        columns = ["division_name", "updated_by", "updated_on"]
        values = [division_name, session_user, current_time_stamp]
        condition = "division_id = '%d' and client_id = '%d'"%(division_id, client_id)
        return self.update(self.tblDivisions, columns, values, condition)

    def save_unit(self, client_id,  units, business_group_id, legal_entity_id, division_id, session_user):
        current_time_stamp = str(self.get_date_time())
        columns = ["unit_id", "client_id", "legal_entity_id", "country_id", "geography_id", "industry_id", 
        "domain_ids", "unit_code", "unit_name", "address", "postal_code", "is_active", "created_by", 
        "created_on", "updated_by", "updated_on"]
        if business_group_id != None:
            columns.append("business_group_id")
        if division_id != None:
            columns.append("division_id")
        values_list = []
        for unit in units:
            domain_ids = ",".join(str(x) for x in unit.domain_ids)
            if business_group_id != None and division_id != None:
                values_tuple = (str(unit.unit_id), client_id, legal_entity_id, str(unit.country_id), str(unit.geography_id),
                    str(unit.industry_id), domain_ids, str(unit.unit_code), str(unit.unit_name), str(unit.unit_address),
                    str(unit.postal_code), 1, session_user, current_time_stamp, session_user, current_time_stamp, 
                    business_group_id, division_id)
            elif business_group_id != None:
                values_tuple = (str(unit.unit_id), client_id, legal_entity_id, str(unit.country_id), str(unit.geography_id),
                    str(unit.industry_id), domain_ids, str(unit.unit_code), str(unit.unit_name), str(unit.unit_address),
                    str(unit.postal_code), 1, session_user, current_time_stamp, session_user, current_time_stamp, 
                    business_group_id)    
            elif division_id != None :
                values_tuple = (str(unit.unit_id), client_id, legal_entity_id, str(unit.country_id), str(unit.geography_id),
                    str(unit.industry_id), domain_ids, str(unit.unit_code), str(unit.unit_name), str(unit.unit_address),
                    str(unit.postal_code), 1, session_user, current_time_stamp, session_user, current_time_stamp, 
                    division_id)   
            else: 
                values_tuple = (str(unit.unit_id), client_id, legal_entity_id, str(unit.country_id), str(unit.geography_id),
                        str(unit.industry_id), domain_ids, str(unit.unit_code), str(unit.unit_name), str(unit.unit_address),
                        str(unit.postal_code), 1, session_user, current_time_stamp, session_user, current_time_stamp)
            values_list.append(values_tuple)
        return self.bulk_insert(self.tblUnits, columns, values_list)


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
        return True

    def change_client_status(self, client_id, legal_entity_id, division_id, is_active, session_user):
        current_time_stamp = str(self.get_date_time())
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [is_active, current_time_stamp, session_user]
        condition = "legal_entity_id = '%d' and client_id = '%d' "% (legal_entity_id, client_id)
        if division_id != None:
            condition += " and division_id='%d' "% division_id
        return self.update(self.tblUnits, columns, values, condition)

    def reactivate_unit(self, client_id, unit_id, session_user):
        current_time_stamp = str(self.get_date_time())
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [1, current_time_stamp, session_user]
        condition = "unit_id = '%d' and client_id = '%d' "% (unit_id, client_id)
        return self.update(self.tblUnits, columns, values, condition)

    def verify_password(self, password, userId):
        columns = "count(*)"
        encrypted_password = self.encrypt(password)
        condition = "password='%s' and user_id='%d'" % (encrypted_password, userId)
        rows = self.get_data(self.tblUsers, columns, condition)
        if(int(rows[0][0]) <= 0):
            return False
        else:
            return True

    def get_business_groups_for_user(self, user_id):
        client_ids = self.get_user_clients(user_id)
        columns = "business_group_id, business_group_name, client_id"
        condition = "client_id in (%s)" % client_ids
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
        client_ids = self.get_user_clients(user_id)
        columns = "legal_entity_id, legal_entity_name, business_group_id, client_id"
        condition = "client_id in (%s)" % client_ids
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
        client_ids = self.get_user_clients(user_id)
        columns = "division_id, division_name, legal_entity_id, business_group_id,"+\
        "client_id"
        condition = "client_id in (%s)" % client_ids
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
        client_ids = self.get_user_clients(user_id)
        columns = "unit_id, unit_code, unit_name, address, division_id,"+\
        " legal_entity_id, business_group_id, client_id, is_active"
        condition = "client_id in (%s)" % client_ids
        rows = self.get_data(self.tblUnits, columns, condition) 
        columns = ["unit_id", "unit_code", "unit_name", "unit_address", "division_id", 
        "legal_entity_id", "business_group_id", "client_id", "is_active"]
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
