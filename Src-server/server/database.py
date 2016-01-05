import datetime
import MySQLdb as mysql
import hashlib
import string
import random

from protocol import core
import hashlib
import uuid

__all__ = [
    "KnowledgeDatabase", "ClientDatabase"
]

def generateRandom():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(characters) for _ in range(7))

def generatePassword() : 
    password = generateRandom()
    return encrypt(password)

def encrypt(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()
    
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

class KnowledgeDatabase(Database):

    tblActivityLog = "tbl_activity_log"
    tblAdmin = "tbl_admin"
    tblBusinessGroups = "tbl_business_groups"
    tblClientCompliances = "tbl_client_compliances"
    tblClientConfigurations = "tbl_client_configurations"
    tblClientCountries = "tbl_client_countries"
    tblClientDatabase = "tbl_client_database"
    tblClientDomains = "tbl_client_domains"
    tblClientGroups = "tbl_client_groups"
    tblClientSavedCompliances = "tbl_client_saved_compliances"
    tblClientSavedStatutories = "tbl_client_saved_statutories"
    tblClientStatutories = "tbl_client_statutories"
    tblClientUsers = "tbl_client_users"
    tblComplianceDurationType = "tbl_compliance_duration_type"
    tblComplianceFrequency = "tbl_compliance_frequency"
    tblComplianceRepeatype = "tbl_compliance_repeat_type"
    tblCompliances = "tbl_compliances"
    tblCompliancesBackup = "tbl_compliances_backup"
    tblCountries = "tbl_countries"
    tblDatabaseServer = "tbl_database_server"
    tblDivisions = "tbl_divisions"
    tblDomains = "tbl_domains"
    tblEmailVerification = "tbl_email_verification"
    tblFormCategory = "tbl_form_category"
    tblFormType = "tbl_form_type"
    tblForms = "tbl_forms"
    tblGeographies = "tbl_geographies"
    tblGeographyLevels = "tbl_geography_levels"
    tblIndustries = "tbl_industries"
    tblLegalEntities = "tbl_legal_entities"
    tblMachines = "tbl_machines"
    tblMobileRegistration = "tbl_mobile_registration"
    tblNotifications = "tbl_notifications"
    tblNotificationsStatus = "tbl_notifications_status"
    tblSessionTypes = "tbl_session_types"
    tblStatutories = "tbl_statutories"
    tblStatutoriesBackup = "tbl_statutories_backup"
    tblStatutoryGeographies = "tbl_statutory_geographies"
    tblStatutoryLevels = "tbl_statutory_levels"
    tblStatutoryMappings = "tbl_statutory_mappings"
    tblStatutoryNatures = "tbl_statutory_natures"
    tblStatutoryNotificationsLog = "tbl_statutory_notifications_log"
    tblUnits = "tbl_units"
    tblUserClients = "tbl_user_clients"
    tblUserCountries = "tbl_user_countries"
    tblUserDomains = "tbl_user_domains"
    tblUserGroups = "tbl_user_groups"
    tblUserLoginHistory = "tbl_user_login_history"
    tblUserSessions = "tbl_user_sessions"
    tblUsers = "tbl_users"

    def __init__(
        self, 
        mysqlHost, mysqlUser, 
        mysqlPassword, mysqlDatabase
    ):
        super(KnowledgeDatabase, self).__init__(
            mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase
        )

    def encrypt(self, value):
        m = hashlib.md5()
        m.update(value)
        return m.hexdigest()

    def convert_to_dict(self, data_list, columns) :
        print data_list
        print len(data_list), len(columns)
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
            if len(data_list) == len(columns) :
                result = {}
                for i, d in enumerate(data_list):
                    result[columns[i]] = d
            return result


    def validate_session_token(self, session_token) :
        # query = "CALL sp_validate_session_token ('%s');" % (session_token)
        query = "SELECT user_id FROM tbl_user_sessions \
            WHERE session_token = '%s'" % (session_token)
        row = self.select_one(query)
        user_id = row[0]
        return user_id

    def get_data(self, table, columns, condition):

        query = "SELECT %s FROM %s WHERE %s "  % (columns, table, condition)
        return self.select_all(query)

    def get_data_from_multiple_tables(self, columns, tables, aliases, joinType, joinConditions, whereCondition):
        query = "SELECT %s FROM " % columns

        for index,table in enumerate(tables):
            if index == 0:
                query += "%s  %s  %s" % (table, aliases[index], joinType)
            elif index <= len(tables) -2:
                query += " %s %s on (%s) %s " % (table, aliases[index], joinConditions[index-1], joinType)
            else:
                query += " %s %s on (%s)" % (table, aliases[index],joinConditions[index-1])

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

    def verify_login(self, username, password):
        tblAdminCondition = "password='%s' and user_name='%s'" % (password, username)
        admin_details = self.get_data("tbl_admin", "*", tblAdminCondition)
        print admin_details
        if (len(admin_details) == 0) :
            data_columns = ["user_id", "user_group_id", "email_id", 
                "employee_name", "employee_code", "contact_no", "address", "designation",
                "user_group_name", "form_ids"
            ]
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, t1.address, t1.designation, \
                t2.user_group_name, t2.form_ids \
                FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
                ON t1.user_group_id = t2.user_group_id \
                WHERE t1.password='%s' and t1.email_id='%s'" % (password, username)
            print query
            data_list = self.select_one(query)
            return self.convert_to_dict(data_list, data_columns)
        else :
            return True

    def get_date_time(self) :
        return datetime.datetime.now()

    def new_uuid(self) :
        s = str(uuid.uuid4())
        return s.replace("-", "")

    def add_session(self, user_id, session_type_id) :
        session_id = self.new_uuid()
        updated_on = self.get_date_time()
        query = "INSERT INTO tbl_user_sessions (session_token, user_id, session_type_id, last_accessed_time) \
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
        createdOn = self.get_date_time()
        activityId = self.get_new_id("activity_log_id", "tbl_activity_log")
        query = "INSERT INTO tbl_activity_log(activity_log_id, user_id, form_id, \
            action, created_on) \
            VALUES (%s, %s, %s, '%s', '%s')" % (
                activityId, user_id, form_id, action, createdOn
            )
        self.execute(query)
        return True

  #
  # Domain
  #

    def get_domains(self):
        columns = "domain_id, domain_name, is_active"
        condition = "1"
        return self.get_data(self.tblDomains, columns, condition)

    def get_domains_for_user(self, user_id) :
        # query = "CALL sp_get_domains_for_user (%s)" % (user_id)
        query = "SELECT distinct t1.domain_id, t1.domain_name, t1.is_active FROM tbl_domains t1 "
        if user_id > 0 :
            query = query + " INNER JOIN tbl_user_domains t2 ON t1.domain_id = t2.domain_id WHERE t2.user_id = %s" % (user_id)
        rows = self.select_all(query)
        columns = ["domain_id", "domain_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_domains(result)
    
    def return_domains(self, data):
        results = []
        for d in data :
            results.append(core.Domain(d["domain_id"], d["domain_name"], bool(d["is_active"])))
        return results
    
    def save_domain(self, domain_name, user_id) :
        createdOn = self.get_date_time()
        domain_id = self.get_new_id("domain_id", "tbl_domains")
        is_active = 1

        query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, \
            created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            domain_id, domain_name, is_active, user_id, createdOn
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
        q = "SELECT domain_name FROM tbl_domains WHERE domain_id=%s" % domain_id
        row = self.select_one(q)
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

    def get_countries(self):
        columns = "country_id, country_name, is_active"
        condition = "1"
        return self.get_data(self.tblCountries, columns, condition)

    def get_countries_for_user(self, user_id) :
        query = "SELECT distinct t1.country_id, t1.country_name, t1.is_active FROM tbl_countries t1 "
        if user_id > 0 :
            query = query + " INNER JOIN tbl_user_countries t2 ON t1.country_id = t2.country_id WHERE t2.user_id = %s" % (user_id)
        rows = self.select_all(query)
        columns = ["country_id", "country_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_countries(result)

    def return_countries(self, data) :
        results = []

        for d in data :
            results.append(core.Country(d["country_id"], d["country_name"], bool(d["is_active"])))
        return results


    
    def get_country_by_id(self, country_id) :
        q = "SELECT country_name FROM tbl_countries WHERE country_id=%s" % country_id
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
        createdOn = self.get_date_time()
        country_id = self.get_new_id("country_id", "tbl_countries")
        is_active = 1

        query = "INSERT INTO tbl_countries(country_id, country_name, \
            is_active, created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            country_id, country_name, is_active, created_by, createdOn
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

        columns = "tf.form_id, tf.form_category_id, tfc.form_category, tf.form_type_id, tft.form_type,"+\
        "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = ["tbl_forms", "tbl_form_category", "tbl_form_type"]
        aliases = ["tf", "tfc", "tft"]
        joinConditions = ["tf.form_category_id = tfc.form_category_id", "tf.form_type_id = tft.form_type_id"]
        whereCondition = " tf.form_id in (%s) order by tf.form_order" % (form_ids)
        joinType = "left join"
        rows = self.get_data_from_multiple_tables(columns, tables, aliases, joinType, joinConditions, whereCondition)
        row_columns = ["form_id", "form_category_id", "form_category", "form_type_id", "form_type", "form_name", "form_url", "form_order", "parent_menu"]
        return self.convert_to_dict(rows, row_columns)

    def get_form_types(self) :
        query = "SELECT form_type_id, form_type_name FROM tbl_form_type"
        rows = self.select_all(query)
        columns = ["form_type_id", "form_type_name"]
        data_list = self.convert_to_dict(rows, columns)
        return data_list

    def save_data(self, table_name, field, data):
        query = "INSERT INTO %s '%s' VALUES '%s'" % (
            table_name, str(field), str(data)
        )
        self.execute(query)
        return True

    def update_data(self, table_name, field_with_data, where_condition) :
        query = "UPDATE %s SET %s WHERE %s" % (
            table_name, field_with_data, where_condition
        )
        self.execute(query)
        return True

    def get_industries(self) :
        query = "SELECT industry_id, industry_name, is_active FROM tbl_industries "
        rows = self.select_all(query)
        columns = ["industry_id", "industry_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_industry(result)

    def return_industry(self, data) :
        results = []
        for d in data :
            industry_id = d["industry_id"]
            industry_name = d["industry_name"]
            is_active = bool(d["is_active"])
            results.append(core.Industry(industry_id, industry_name, is_active))
        return results



    def get_industry_by_id(self, industry_id) :
        q = "SELECT industry_name FROM tbl_industries WHERE industry_id=%s" % industry_id
        row = self.select_one(q)
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
        field = ("industry_id", "industry_name", "created_by", "created_on")
        data = (industry_id, industry_name, user_id, created_on)
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
            industry_name, updated_by
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
        query = "SELECT statutory_nature_id, statutory_nature_name, is_active \
            FROM tbl_statutory_natures "
        rows = self.select_all(query)
        columns = ["statutory_nature_id", "statutory_nature_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_statutory_nature(result)

    def return_statutory_nature(self, data) :
        results = []
        for d in data :
            nature_id = d["statutory_nature_id"]
            nature_name = d["statutory_nature_name"]
            is_active = bool(d["is_active"])
            results.append(core.StatutoryNature(nature_id, nature_name, is_active))
        return results


    def get_nature_by_id(self, nature_id) :
        q = "SELECT sttautory_nature_name FROM tbl_statutory_natures WHERE statutory_nature_id=%s" % nature_id
        row = self.select_one(q)
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
        field = ("statutory_nature_id", "statutory_nature_name", "created_by", "created_on")
        data = (nature_id, nature_name, user_id, created_on)
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

    def get_levels_for_country_domain(self, country_id, domainId) :
        query = "SELECT level_id, level_position, level_name \
            FROM tbl_statutory_levels WHERE country_id = %s and domain_id = %s ORDER BY level_position" % (
                country_id, domainId
            )
        rows = self.select_all(query)
        columns = ["level_id", "level_position", "level_name"]
        result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_levels(self, country_id, domain_id, levels) :
        saved_names = [row["level_name"] for row in self.get_levels_for_country_domain(country_id, domainId)]

        level_names = []
        level_positions = []
        for level in levels :
            name = level.level_name
            position = level.level_position
            if level.level_id  is None :
                if (saved_names.count(name) > 0) :
                    print "LevelIdCannotNullFor '%s'" % name
                    return name
            level_names.append(name)
            level_positions.append(position)

        duplicate_names = [x for i, x in enumerate(level_names) if level_names.count(x) > 1]
        duplicate_position = [x for i, x in enumerate(level_positions) if level_positions.count(x) > 1]
        if len(duplicate_names) > 0 :
            # self.responseData = "DuplicateStatutoryLevelNamesExists"
            return True
        elif len(duplicate_position) > 0 :
            # self.responseData = "DuplicateStatutoryLevelPositionsExists"
            return True
        return False

    def save_statutory_levels(self, country_id, domain_id, levels, user_id) :

        table_name = "tbl_statutory_levels"
        created_on = self.get_date_time()
        for level in levels :
            name = level.level_name
            position = level.level_position
            if (level.level_id is None) :
                level_id = self.get_new_id("level_id", table_name)
                field = ("level_id", "level_position", "level_name", "country_id", "domain_id", "created_by", "created_on")
                data = (level_id, position, name, country_id, domain_id, user_id, created_on)
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

    def get_geography_levels_for_country(self, country_id) :
        query = "SELECT level_id, level_position, level_name \
            FROM tbl_geography_levels WHERE country_id = %s ORDER BY level_position" % country_id
        rows = self.select_all(query)
        columns = ["level_id", "level_position", "level_name"]
        result = self.convert_to_dict(rows, columns)
        return result

    def check_duplicate_gepgrahy_levels(self, country_id, levels) :
        saved_names = [row["level_name"] for row in self.get_geography_levels_for_country(country_id)]

        level_names = []
        level_positions = []
        for level in levels :
            name = level.level_name
            position = level.level_position
            if level.level_id  is None :
                if (saved_names.count(name) > 0) :
                    print "LevelIdCannotNullFor '%s'" % name
                    return name
            level_names.append(name)
            level_positions.append(position)

        duplicate_names = [x for i, x in enumerate(level_names) if level_names.count(x) > 1]
        duplicate_position = [x for i, x in enumerate(level_positions) if level_positions.count(x) > 1]
        if len(duplicate_names) > 0 :
            # self.responseData = "DuplicateStatutoryLevelNamesExists"
            return True
        elif len(duplicate_position) > 0 :
            # self.responseData = "DuplicateStatutoryLevelPositionsExists"
            return True
        return False

    def save_geography_levels(self, country_id, levels):
        table_name = "tbl_geography_levels"
        created_on = self.get_date_time()
        for level in levels :
            name = level.level_name
            position = lavel.level_position
            if level.level_id is None :
                level_id = self.get_new_id("level_id", table_name)
                field = ("level_id", "level_position", "level_name", "country_id", "created_by", "created_on")
                data = (level_id, position, name, country_id, user_id, created_on)
                if (self.save_data(table_name, field, data)):
                    action = "New Geography levels added"
                    self.save_activity(user_id, 5, action)
            else :
                field_with_data = "level_position=%s, level_name='%s', updated_by=%s" % (
                    position, name, user_id
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
        columns = ["geography_id", "geography_name", "level_id", "parent_ids", "is_active", "country_id", "country_name"]
        result = self.convert_to_dict(rows, columns)
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

    def get_geography_by_id(self, geography_id):
        query = "SELECT geography_id, geography_name, level_id, parent_ids, is_active \
            FROM tbl_geographies WHERE geography_id = %s" % (geography_id)
        rows = self.select_one(query)
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
        field = ("geography_id", "geography_name", "level_id", "parent_ids", "created_by", "created_on") 
        data = (geography_id, geography_name, geography_level_id, parent_ids, user_id, created_on)
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
        #     self.saveActivity(updated_by, 7, action)
        # self.getAllGeographies()
        # return True

    def change_geography_status(self,geography_id, is_active, updated_by) :
        oldData = self.get_geography_by_id(geography_id)
        if bool(oldData) is False:
            return False
        table_name = "tbl_geographies"
        field_with_data = "is_active=%s, updated_by=%s"  % (
            int(is_active), updated_by
        )
        where_condition = "geography_id = %s" %  (geography_id)
        if (self. update_data(table_name, field_with_data, where_condition)) :
            if is_active == 0:
                status = "deactivated"
            else:
                status = "activated"
            action = "Geography %s status  - %s" % (name, status)
            self.save_activity(updated_by, 6, action)
            return True

    def get_statutory_by_id(self, statutory_id):
        query = "SELECT statutory_id, statutory_name, level_id, parent_ids, is_active \
            FROM tbl_statutories WHERE statutory_id = %s" % (statutory_id)
        rows = self.select_one(query)
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


    def save_statutory(self, name, level_id, parent_ids, user_id) :
        is_saved = False
        statutory_id = self.get_new_id("statutory_id", "tbl_statutories")
        created_on = self.get_date_time()
        table_name = "tbl_statutories"
        field = ("statutory_id", "statutory_name", "level_id", "parent_ids", "created_by", "created_on")
        data = (statutory_id, name, level_id, parent_ids, user_id, created_on)

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
        #     self.saveActivity(updated_by, 7, action)
        # self.getAllGeographies()
        # return True


        
#
#   Forms
#
    def get_forms(self):
        columns = "tf.form_id, tf.form_category_id, tfc.form_category, "+\
        "tf.form_type_id, tft.form_type, tf.form_name, tf.form_url, "+\
        "tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormCategory, self.tblFormType]
        aliases = ["tf", "tfc", "tft"]
        joinConditions = ["tf.form_catEgory_id = tfc.form_category_id", 
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

    def save_user(self, user_id, email_id, user_group_id, employee_name,
     employee_code, contact_no, address, designation, country_ids, domain_ids):
        result1 = False
        result2 = False
        result3 = False
        current_time_stamp = self.get_date_time()
        user_columns = ["user_id", "email_id", "user_group_id", "password", "employee_name", 
                    "employee_code", "contact_no", "address", "designation", "is_active", 
                    "created_on", "created_by", "updated_on", "updated_by"]
        user_values = [user_id, email_id, user_group_id, generatePassword(),
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
    def get_group_company_details(self):
        columns = "client_id, group_name, email_id, logo_url,  contract_from, contract_to,"+\
        " no_of_user_licence, total_disk_space, is_sms_subscribed,  incharge_persons,"+\
        " is_active"
        condition = "1"
        return self.get_data(self.tblClientGroups, columns, condition)

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
