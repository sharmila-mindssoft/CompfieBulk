import datetime
import os
import uuid
import MySQLdb as mysql


__all__ = [
    "DatabaseHandler"
]

_databaseHandlerInstance = None

class DatabaseHandler(object) :

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


    def __init__(self) :
        self.mysqlHost = "localhost"
        self.mysqlUser = "root"
        self.mysqlPassword = "123456"
        self.mysqlDatabase = "mirror_knowledge"

    def mysqlServerConnect(self):
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword
        )

    def dbConnect(self) :
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword, self.mysqlDatabase
        )

    def createDatabase(self, databaseName):
        con = None
        cursor = None
        isComplete = True
        try:
            con = self.mysqlServerConnect()
            cursor = con.cursor()
            query = "CREATE DATABASE "+databaseName
            cursor.execute(query)
            con.commit()

        except mysql.Error, e:
            print ("Error:%s - %s" % (query, e))
            isComplete = False

        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()

        return isComplete

    def execute(self, query):
        con = None
        cursor = None
        isComplete = True
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()

        except mysql.Error, e:
            print ("Error:%s - %s" % (query, e))
            isComplete = False

        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()

        return isComplete

    def executeAndReturn(self, query) :
        con = None
        cursor = None
        result = None
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        except mysql.Error, e:
            print ("Error:%s - %s" % (query, e))

        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()

        return result

    def insert(self, table, columns, values) :
        # columns = 
        query = "INSERT INTO %s (%s) VALUES (%s)" % (table, columns, values)
        query = "INSERT INTO "+table+" ("+columns+")" + \
            " VALUES ("+values+")"
        return self.execute(query)

    def bulkInsert(self, table, columns, valueList) :
        query = "INSERT INTO %s (%s)  VALUES" % (table, columns)

        for index, value in enumerate(valueList):
            if index < len(valueList)-1:
                query += +"%s," % str(value)
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

    def onDuplicateKeyUpdate(self, table, columns, valueList, updateColumnsList):
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
        rows = self.getData(table, column, condition)
        currentValue = rows[0][0]
        if currentValue != None:
            newValue = currentValue+","+str(value)
        else:
            newValue = str(value)
        columns = [column]
        values = [newValue]
        return self.update(table, columns, values, condition)

    def generateNewId(self, table, column):
        query = "SELECT max("+column+") FROM "+table
        rows = self.executeAndReturn(query)

        for row in rows :
            newId = row[0] + 1 if row[0] != None else 1

        return int(newId)

    def isAlreadyExists(self, table, condition) :
        query = "SELECT count(*) FROM "+table+" WHERE "+condition
        rows = self.executeAndReturn(query)     
        if rows[0][0] > 0:
            return True
        else : 
            return False

    def getData(self, table, columns, condition):
        # query = "SELECT "+columns+" FROM "+table+" WHERE "+condition 
        query = "SELECT %s FROM %s WHERE %s "  % (table, columns, condition)
        return self.executeAndReturn(query)

    def getDataFromMultipleTables(self, columns, tables, aliases, joinType, joinConditions, whereCondition):

        query = "SELECT %s FROM " % columns

        for index,table in enumerate(tables):
            if index == 0:
                query += "%s  %s  %s" % (table, aliases[index], joinType)
            elif index <= len(tables) -2:
                query += " %s %s on (%s) %s " % (table, aliases[index], joinConditions[index-1], joinType)
            else:
                query += " %s %s on (%s)" % (table, aliases[index],joinConditions[index-1])

        query += " where %s" % whereCondition
        return self.executeAndReturn(query)

    def validateSessionToken(self, sessionToken) :
        query = "SELECT user_id FROM tbl_user_sessions \
        WHERE session_token = '%s'" % sessionToken
        rows = self.executeAndReturn(query)
        row = rows[0]
        return row[0]

    def verifyPassword(self, password, userId, clientId):
        columns = "count(*)"
        condition = "password='%s' and user_id='%d'" % (password, userId)
        if clientId != None:
            condition += " and client_id='%d'" % clientId
        rows = self.getData("tbl_users", columns, condition)
        if(int(rows[0][0]) <= 0):
            return False
        else:
            return True

    def new_uuid(self) :
        s = str(uuid.uuid4())
        return s.replace("-", "")

    def add_session(self, user_id, session_type_id) :
        session_id = self.new_uuid()
        updated_by = datetime.datetime.now()
        query = "insert into tbl_user_sessions values ('%s', %s, %s, '%s');"
        query = query % (session_id, user_id, session_type_id, updated_by)
        self.execute(query)
        return session_id

    def verifyLogin(self, userName, password):
        tblAdminCondition = "password='%s' and user_name='%s'" % (password, userName)
        adminDetails = self.getData("*", "tbl_admin", tblAdminCondition)
        print adminDetails
        if (len(adminDetails) == 0) :
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, t1.address, t1.designation \
                t2.user_group_name, t2.form_ids \
                FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
                ON t1.user_group_id = t2.user_group_id \
                WHERE t1.password='%s' and t1.email_id='%s'" % (password, userName)
            return self.executeAndReturn(query)
        else :
            return True

    def getForms(self, form_category_id, form_ids):
        query = "SELECT t1.form_id, t1.form_category_id, t1.form_type_id, t1.form_name, \
            t1.form_url, t1.form_order, t1.parent_menu, t2.form_category_name, t3.form_type_name \
            FROM tbl_forms t1 INNER JOIN tbl_form_category t2 ON t1.form_category_id = t2.form_category_id \
            INNER JOIN tbl_form_types t3 ON t1.form_type_id = t3.form_type_id "
        qry = ""

        if (form_category_id is not None) :
            qry = " WHERE t1.form_category_id = %s" % (form_category_id)
        if (form_ids is not None):
            ids = [int(x) for x in form_ids.split(',')]
            qry = " WHERE t1.form_id in '%s' " % str(tuple(ids))

        return self.executeAndReturn(query + qry)

    def getUserForms(self, formIds):
        forms = []

        columns = "tf.form_id, tf.form_category_id, tfc.form_category, tf.form_type_id, tft.form_type,"+\
        "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormCategory, self.tblFormType]
        aliases = ["tf", "tfc", "tft"]
        joinConditions = ["tf.form_category_id = tfc.form_category_id", "tf.form_type_id = tft.form_type_id"]
        whereCondition = " tf.form_id in ("+formIds+") order by tf.form_order"
        joinType = "left join"

        rows = self.getDataFromMultipleTables(columns, tables, aliases, joinType, 
            joinConditions, whereCondition)
        return rows    

    def getUserGroupDetailedList(self) :
        userGroupList = []

        columns = "user_group_id, user_group_name, form_category_id, "+\
                    "form_ids, is_active"
        tables = self.tblUserGroups
        whereCondition = "1"

        rows = self.getData(columns, tables, whereCondition)
        return rows    

    def saveUserGroup(self, userGroup, sessionUser):
        print "inside saveUserGroup"
        columns = ["user_group_id", "user_group_name","form_category", "form_ids", "is_active",
                  "created_on", "created_by", "updated_on", "updated_by"]
        valuesList =  [userGroup.userGroupId, userGroup.userGroupName, userGroup.formCategoryId, 
                        ",".join(str(x) for x in userGroup.formIds), userGroup.isActive, getCurrentTimeStamp(), 
                        sessionUser,getCurrentTimeStamp(), sessionUser]
        return self.insert(self.db.tblUserGroups,columns,valuesList)

    def truncate(self, table):
        query = "TRUNCATE TABLE  %s;" % table
        return self.execute(query)

    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
        return _databaseHandlerInstance
