import datetime
import os
import re
import MySQLdb as mysql
from aparajitha.server.constants import ROOT_PATH
from commonfunctions import getCurrentTimeStamp, generatePassword, generateRandom

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

    def dbConnect(self) :
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword, self.mysqlDatabase
        )

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
        columns = ",".join(columns)
        stringValue = ""
        for index,value in enumerate(values):
            if(index < len(values)-1):
                stringValue = stringValue+"'"+str(value)+"',"
            else:
                stringValue = stringValue+"'"+str(value)+"'"
        query = "INSERT INTO %s (%s) VALUES (%s)" % (table, columns, stringValue)
        return self.execute(query)

    def bulkInsert(self, table, columns, valueList) :
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

    def increment(self, table, column, condition):
        rows = self.getData(table, column, condition)
        currentValue = rows[0][0]
        if currentValue != None:
            newValue = int(currentValue)+1
        else:
            newValue = 1
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
        query = "SELECT %s FROM %s WHERE %s "  % (columns, table, condition)
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
        print query
        return self.executeAndReturn(query)

    def validateSessionToken(self, sessionToken) :
        query = "SELECT user_id FROM tbl_user_sessions \
        WHERE session_token = '%s'" % sessionToken
        rows = self.executeAndReturn(query)
        row = rows[0]
        return row[0]

    def verifyPassword(self, password, userId):
        columns = "count(*)"
        condition = "password='%s' and user_id='%d'" % (password, userId)
        rows = self.getData(self.tblUsers, columns, condition)
        if(int(rows[0][0]) <= 0):
            return False
        else:
            return True

    def add_session(self, user_id) :
        session_id = self.new_uuid()
        query = "insert into tbl_user_sessions values ('%s', '%s', '%d');"
        query = query % (session_id, user_id, current_timestamp())
        self._db.execute(query)
        return session_id

    def verifyLogin(self, userName, password):
        tblAdminCondition = "password='%s' and user_name='%s'" % (password, userName)
        adminDetails = self.getData("tbl_admin", "*", tblAdminCondition)
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


#
#  Admin User Group
#    

    def getUserGroupDetailedList(self) :
        userGroupList = []

        columns = "user_group_id, user_group_name, form_category_id, "+\
                    "form_ids, is_active"
        tables = self.tblUserGroups
        whereCondition = "1"

        rows = self.getData( tables, columns, whereCondition)
        return rows    

    def getUserGroupList(self) :
        userGroupList = []

        columns = "user_group_id, user_group_name, is_active"
        tables = self.tblUserGroups
        whereCondition = "1"

        rows = self.getData(tables, columns, whereCondition)
        return rows

    def saveUserGroup(self, userGroup):
        columns = ["user_group_id", "user_group_name","form_category_id", "form_ids", "is_active",
                  "created_on", "created_by", "updated_on", "updated_by"]
        valuesList =  [userGroup.userGroupId, userGroup.userGroupName, userGroup.formCategoryId, 
                        ",".join(str(x) for x in userGroup.formIds), userGroup.isActive, getCurrentTimeStamp(), 
                        0, getCurrentTimeStamp(), 0]
        return self.insert(self.tblUserGroups,columns,valuesList)

    def updateUserGroup(self, userGroup):
        columns = ["user_group_name","form_category_id","form_ids", "updated_on", "updated_by"]
        values =  [ userGroup.userGroupName, userGroup.formCategoryId, 
                    ",".join(str(x) for x in userGroup.formIds), getCurrentTimeStamp(),0]
        condition = "user_group_id='%d'" % userGroup.userGroupId
        return self.update(self.tblUserGroups, columns, values, condition)

    def updateUserGroupStatus(self, userGroupId, isActive):
        columns = ["is_active", "updated_by", "updated_on"]
        values = [isActive, 0, getCurrentTimeStamp()]
        condition = "user_group_id='%d'" % userGroupId
        return self.update(self.tblUserGroups, columns, values, condition)

#
#   Admin User
#

    def getDetailedUserList(self):
        columns = "user_id, email_id, user_group_id, employee_name, employee_code,"+\
                "contact_no, address, designation, is_active"
        condition = "1"
        rows = self.getData(self.tblUsers, columns, condition)
        return rows

    def getUserCountries(self, userId):
        columns = "group_concat(country_id)"
        condition = " user_id = '%d'"% userId
        rows = self.getData( self.tblUserCountries, columns, condition)
        return rows[0][0]

    def getUserDomains(self, userId):
        columns = "group_concat(domain_id)"
        condition = " user_id = '%d'"% userId
        rows = self.getData(self.tblUserDomains, columns, condition)
        return rows[0][0]

    def getUserClients(self, userId):
        columns = "group_concat(client_id)"
        condition = " user_id = '%d'"% userId
        rows = self.getData( self.tblUserClients, columns,  condition)
        return rows[0][0]

    def getUserList(self):
        columns = "user_id, employee_name, employee_code, is_active"
        rows = self.getData(self.tblUsers, columns, "1")
        return rows

    def saveUser(self, user):
        result1 = False
        result2 = False
        result3 = False
        currentTimeStamp = getCurrentTimeStamp()
        userColumns = ["user_id", "email_id", "user_group_id", "password", "employee_name", 
                    "employee_code", "contact_no", "address", "designation", "is_active", 
                    "created_on", "created_by", "updated_on", "updated_by"]
        userValues = [user.userId, user.emailId, user.userGroupId, generatePassword(),
                user.employeeName, user.employeeCode, user.contactNo, user.address,
                user.designation, user.isActive, currentTimeStamp, 0, currentTimeStamp, 0]
        result1 = self.insert(self.tblUsers, userColumns, userValues)

        countryColumns = ["user_id", "country_id"]
        countryValuesList = []
        for countryId in user.countryIds:
            countryValueTuple = (user.userId, int(countryId))
            countryValuesList.append(countryValueTuple)
        result2 = self.bulkInsert(self.tblUserCountries, countryColumns, countryValuesList)

        domainColumns = ["user_id", "domain_id"]
        domainValuesList = []
        for domainId in user.domainIds:
            domainValueTuple = (user.userId, int(domainId))
            domainValuesList.append(domainValueTuple)
        result3 = self.bulkInsert(self.tblUserDomains, domainColumns, domainValuesList)

        return (result1 and result2 and result3)

    def updateUser(self, user):
        result1 = False
        result2 = False
        result3 = False

        currentTimeStamp = getCurrentTimeStamp()
        userColumns = [ "user_group_id", "employee_name", "employee_code", 
                    "contact_no", "address", "designation",
                    "updated_on", "updated_by"]
        userValues = [user.userGroupId, user.employeeName, user.employeeCode, 
                    user.contactNo, user.address, user.designation, 
                    currentTimeStamp, 0]
        userCondition = "user_id = '%d'" % user.userId
        result1 = self.update(self.tblUsers,userColumns,userValues, userCondition)
        self.delete(self.tblUserCountries, userCondition)
        self.delete(self.tblUserDomains, userCondition)

        countryColumns = ["user_id", "country_id"]
        countryValuesList = []
        for countryId in user.countryIds:
            countryValueTuple = (user.userId, int(countryId))
            countryValuesList.append(countryValueTuple)
        result2 = self.bulkInsert(self.tblUserCountries, countryColumns, countryValuesList)

        domainColumns = ["user_id", "domain_id"]
        domainValuesList = []
        for domainId in user.domainIds:
            domainValueTuple = (user.userId, int(domainId))
            domainValuesList.append(domainValueTuple)
        result3 = self.bulkInsert(self.tblUserDomains, domainColumns, domainValuesList)

        return (result1 and result2 and result3)    

    def updateUserStatus(self, userId, isActive):
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [isActive, getCurrentTimeStamp(), 0]
        condition = "user_id='%d'" % userId
        return self.update(self.tblUsers, columns, values, condition)    

    def getClientIds(self, sessionUser):
        columns = "group_concat(client_id)"
        condition = "user_id = '%d'" % sessionUser
        return self.getData(self.tblUserClients, columns, condition)

    def getGroupCompanyDetails(self, clientIds):
        columns = "client_id, group_name, email_id, logo_url,  contract_from, contract_to,"+\
        " no_of_user_licence, total_disk_space, is_sms_subscribed,  incharge_persons,"+\
        " is_active"
        condition = "client_id in (%s)" % clientIds
        return self.getData(self.tblClientGroups, columns, condition)

    def getGroupCompanies(self, clientIds):
        columns = "client_id, group_name,  is_active"
        condition = "client_id in (%s)" % clientIds
        return self.getData(self.tblClientGroups, columns, condition)        

    def getClientConfigurations(self, clientId):
        columns = "country_id, domain_id, period_from, period_to"
        condition = "client_id = '%d'"% clientId
        return self.getData(self.tblClientConfigurations, columns, condition)

    def getBusinessGroups(self, clientId):
        columns = "business_group_id, business_group_name"
        condition = "client_id = '%d'" % clientId
        return self.getData(self.tblBusinessGroups, columns, condition)

    def getLegalEntities(self, clientId):
        columns = "legal_entity_id, legal_entity_name, business_group_id"
        condition = "client_id = '%d'" % clientId
        return self.getData(self.tblLegalEntities, columns, condition)

    def getDivisions(self, clientId):
        columns = "division_id, division_name, legal_entity_id, business_group_id"
        condition = "client_id = '%d'"% clientId
        return self.getData(self.tblDivisions,columns, condition)

    def getUnitDetails(self, clientId):
        columns = "unit_id, division_id, legal_entity_id, business_group_id, "+\
                "unit_code, unit_name, country_id,  address,"+\
                "postal_code, domain_ids, industry_id, geography_id, is_active"
        condition = "client_id = '%d'"% clientId
        return self.getData(self.tblUnits, columns, condition)

    def getUnits(self, clientId):
        columns = "unit_id, division_id, legal_entity_id, "+\
                "business_group_id, unit_code, unit_name,"+\
                " address, is_active"
        condition = "client_id = '%d'" % clientId
        return self.getData(self.tblUnits, colums, condition)

#
#   Group Company
#
    def saveDateConfigurations(self, clientId, dateConfigurations, sessionUser):
        valuesList = []
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["client_id", "country_id" ,"domain_id", "period_from", 
        "period_to", "updated_by", "updated_on"]
        condition = "client_id='%d'"%clientId
        self.delete(self.tblClientConfigurations, condition)
        for configuration in dateConfigurations:
            countryId = configuration["country_id"]
            domainId = configuration["domain_id"]
            periodFrom = configuration["period_from"]
            periodTo = configuration["period_to"]
            valuesTuple = (clientId, countryId, domainId, periodFrom, periodTo, 
                 int(sessionUser), str(currentTimeStamp))
            valuesList.append(valuesTuple)
        return self.bulkInsert(self.tblClientConfigurations,columns,valuesList)

    def saveClientCountries(self, clientId, countryIds):
        valuesList = []
        columns = ["client_id", "country_id"]
        condition = "client_id = '%d'" % clientId
        self.delete(self.tblClientCountries, condition)
        for countryId in countryIds:
            valuesTuple = (clientId, countryId)
            valuesList.append(valuesTuple)
        return self.bulkInsert(self.tblClientCountries, columns, valuesList)

    def saveClientDomains(self, clientId, domainIds):
        valuesList = []
        columns = ["client_id", "domain_id"]
        condition = "client_id = '%d'" % clientId
        self.delete(self.tblClientDomains, condition)
        for domainId in domainIds:
            valuesTuple = (clientId, domainId)
            valuesList.append(valuesTuple)
        return self.bulkInsert(self.tblClientDomains, columns, valuesList)

    def _mysqlServerConnect(self, host, username, password):
        return mysql.connect(host, username, password)

    def _dbConnect(self, host, username, password, database) :
        return mysql.connect(host, username, password, 
            database)

    def _createDatabase(self, host, username, password, 
        databaseName, dbUsername, dbPassword, emailId):
        con = self._mysqlServerConnect(host, username, password)
        cursor = con.cursor()
        query = "CREATE DATABASE %s" % databaseName
        cursor.execute(query)
        query = "grant all privileges on %s.* to %s@%s IDENTIFIED BY '%s';" %(
            databaseName, dbUsername, host, dbPassword)
        con.commit()

        con = self._dbConnect(host, username, password, databaseName)
        cursor = con.cursor()
        sqlScriptPath = os.path.join(ROOT_PATH, 
        "Src-client/files/desktop/common/clientdatabase/client-tables.sql")
        fileObj = open(sqlScriptPath, 'r')
        sqlFile = fileObj.read()
        fileObj.close()
        sqlCommands = sqlFile.split(';')
        size = len(sqlCommands)
        for index,command in enumerate(sqlCommands):
            if (index < size-1):
                cursor.execute(command)
            else:
                break
        query = "insert into tbl_admin (username, password) values ('%s', '%s')"%(
            emailId, generatePassword())        
        cursor.execute(query)
        con.commit()

    def _getServerDetails(self):
        columns = "ip, server_username,server_password"
        condition = "server_full = 0 order by length ASC limit 1"
        rows = self.getData(self.tblDatabaseServer, columns, condition)
        return rows[0]

    def createAndSaveClientDatabase(self, groupName, clientId, shortName, emailId):
        print "inside create and save client database"
        groupName = re.sub('[^a-zA-Z0-9 \n\.]', '', groupName)
        groupName = groupName.replace (" ", "")
        databaseName = "mirror_%s_%d" %(groupName.lower(),clientId)
        row = self._getServerDetails()
        host = row[0]
        username = row[1]
        password = row[2]
        dbUsername = generateRandom()
        dbPassword = generateRandom()

        if self._createDatabase(host, username, password, databaseName, dbUsername, 
            dbPassword, emailId):
            print "database created"
            dbServerColumn = "company_ids"
            dbServerValue = clientId
            dbServerCondition = "ip='%s'"% host
            self.append(self.tblDatabaseServer, dbServercolumn, dbServerValue,
                dbServerCondition)
            dbServercolumn = "length"
            self.increment(self.tblDatabaseServer, dbServerColumn,
                dbServerCondition)

            machineColumns = "client_ids"
            machineValue = dbServerValue
            machineCondition = dbServerCondition
            self.append(self.tblMachines, machineColumns, machineValue,
                machineCondition)

            rows = self.getData(self.tblMachines, "machin_id", machineCondition)
            machineId = rows[0][0]

            clientDbColumns = ["client_id", "machine_id", "database_ip", 
                    "database_port", "database_username", "database_password",
                    "client_short_name", "database_name"]
            clientDBValues = [clientId, machineId, host, 90, dbUsername,
            dbPassword, shortName, databaseName]
            return self.insert(self.tblClientDatabase, clientDbColumns, clientDBValues)

    def saveClientGroup(self, clientGroup, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["client_id", "group_name", "email_id", "logo_url", 
        "logo_size", "contract_from", "contract_to", "no_of_user_licence", 
        "total_disk_space", "is_sms_subscribed", "url_short_name", 
        "incharge_persons", "is_active", "created_by", "created_on", 
        "updated_by", "updated_on"]
        values = [clientGroup.clientId, clientGroup.groupName, clientGroup.username,
        clientGroup.logo,1200, clientGroup.contractFrom, clientGroup.contractTo,
        clientGroup.noOfLicence, clientGroup.fileSpace, clientGroup.isSmsSubscribed,
        clientGroup.shortName, ','.join(str(x) for x in clientGroup.inchargePersons),1, sessionUser,
        currentTimeStamp, sessionUser, currentTimeStamp]
        return self.insert(self.tblClientGroups, columns, values)

    def updateClientGroup(self, clientGroup, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["group_name", "logo_url", "logo_size", "contract_from", 
        "contract_to", "no_of_user_licence", "total_disk_space", "is_sms_subscribed", 
        "incharge_persons", "is_active", "updated_by", "updated_on"]
        values = [clientGroup.groupName, clientGroup.logo,1200, clientGroup.contractFrom, clientGroup.contractTo,
        clientGroup.noOfLicence, clientGroup.fileSpace, clientGroup.isSmsSubscribed,
        ','.join(str(x) for x in clientGroup.inchargePersons),1, sessionUser,
        currentTimeStamp]
        condition = "client_id = '%d'" % clientGroup.clientId
        return self.update(self.tblClientGroups, columns, values, condition)

    def saveClientUser(self, clientGroup, sessionUser):
        columns = ["client_id", "user_id",  "email_id", 
        "employee_name", "created_on", "is_admin", "is_active"]
        values = [clientGroup.clientId, 0, self.username, "Admin",
        getCurrentTimeStamp(), 1, 1]
        return self.insert(self.tblClientUsers, columns, values)

    def saveInchargePersons(self, clientGroup):
        columns = ["client_id", "user_id"]
        valuesList = []
        condition = "client_id='%d'" % clientGroup.clientId
        self.delete(self.tblUserClients, condition)
        for inchargePerson in clientGroup.inchargePersons:
            valuesTuple = (clientGroup.clientId, inchargePerson)
            valuesList.append(valuesTuple)
        return self.bulkInsert(self.tblUserClients, columns, valuesList)

    def updateClientGroupStatus(self, clientId, isActive, sessionUser):
        columns = ["is_active", "updated_by", "updated_on"]
        values = [ isActive, int(sessionUser), getCurrentTimeStamp()]
        condition = "client_id='%d'" % clientId
        return self.update(self.tblClientGroups, columns, values, condition)

    def getAllClientIds(self):
        columns = "group_concat(client_id)"
        return self.getData(self.tblClientGroups, columns, "1")

    def getClientCountries(self, clientId):
        columns = "group_concat(country_id)"
        condition = "client_id ='%d'" % clientId
        rows = self.getData(self.tblClientCountries, columns, condition)
        return rows[0][0]

    def getClientDomains(self, clientId):
        columns = "group_concat(domain_id)"
        condition = "client_id ='%d'" % clientId
        rows = self.getData(self.tblClientDomains, columns, condition)
        return rows[0][0]
#
#   Unit creation
#
    
    def saveBusinessGroup(self, clientId, busienssGroupId, businessGroupName, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["client_id", "business_group_id", "business_group_name", 
        "created_by", "created_on", "updated_by", "updated_on"]
        values = [clientId, busienssGroupId, businessGroupName, sessionUser, currentTimeStamp,
        sessionUser, currentTimeStamp]
        return self.insert(self.tblBusinessGroups, columns, values)

    def updateBusinessGroup(self, clientId, businessGroupId, businessGroupName, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["business_group_name", "updated_by", "updated_on"]
        values = [businessGroupName, sessionUser, currentTimeStamp]
        condition = "business_group_id = '%d' and client_id = '%d'"%(businessGroupId, clientId)
        return self.update(self.tblBusinessGroups, columns, values, condition)

    def saveLegalEntity(self, clientId, legalEntityId, legalEntityName, businessGroupId, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["client_id", "legal_entity_id", "legal_entity_name", "business_group_id", 
        "created_by", "created_on", "updated_by", "updated_on"]
        values = [clientId, legalEntityId, legalEntityName, businessGroupId, 
        sessionUser, currentTimeStamp, sessionUser, currentTimeStamp]
        return self.insert(self.tblLegalEntities, columns, values)
    
    def updateLegalEntity(self, clientId, legalEntityId, legalEntityName, businessGroupId, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["legal_entity_name", "updated_by", "updated_on"]
        values = [legalEntityName, businessGroupId, sessionUser, currentTimeStamp]
        condition = "legal_entity_id = '%d' and client_id = '%d'"%(legalEntityId, clientId)
        return self.update(self.tblLegalEntities, columns, values, condition)

    def saveDivision(self, clientId, divisionId, divisionName, businessGroupId, legalEntityId, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["client_id", "division_id", "division_name", "business_group_id", "legal_entity_id",
        "created_by", "created_on", "updated_by", "updated_on"]
        values = [clientId, divisionId, divisionName, businessGroupId, legalEntityId,
        sessionUser, currentTimeStamp, sessionUser, currentTimeStamp]
        return self.insert(self.tblDivisions, columns, values)

    def updateDivision(self, clientId, divisionId, divisionName, businessGroupId, legalEntityId, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["division_name", "updated_by", "updated_on"]
        values = [divisionName, sessionUser, currentTimeStamp]
        condition = "division_id = '%d' and client_id = '%d'"%(divisionId, clientId)
        return self.update(self.tblDivisions, columns, values, condition)

    def saveUnit(self, clientId,  units, businessGroupId, legalEntityId, divisionId, sessionUser):
        currentTimeStamp = str(getCurrentTimeStamp())
        columns = ["unit_id", "client_id", "legal_entity_id", "country_id", "geography_id", "industry_id", 
        "domain_ids", "unit_code", "unit_name", "address", "postal_code", "is_active", "created_by", 
        "created_on", "updated_by", "updated_on"]
        if businessGroupId != None:
            columns.append("business_group_id")
        if divisionId != None:
            columns.append("division_id")
        valuesList = []
        for unit in units:
            domainIds = ",".join(str(x) for x in unit["domain_ids"])
            if businessGroupId != None and divisionId != None:
                valuesTuple = (str(unit["unit_id"]), clientId, legalEntityId, str(unit["country_id"]), str(unit["geography_id"]),
                    str(unit["industry_id"]), domainIds, str(unit["unit_code"]), str(unit["unit_name"]), str(unit["unit_address"]),
                    str(unit["postal_code"]), 1, sessionUser, currentTimeStamp, sessionUser, currentTimeStamp, 
                    businessGroupId, divisionId)
            elif businessGroupId != None:
                valuesTuple = (str(unit["unit_id"]), clientId, legalEntityId, str(unit["country_id"]), str(unit["geography_id"]),
                    str(unit["industry_id"]), domainIds, str(unit["unit_code"]), str(unit["unit_name"]), str(unit["unit_address"]),
                    str(unit["postal_code"]), 1, sessionUser, currentTimeStamp, sessionUser, currentTimeStamp, 
                    businessGroupId)    
            elif divisionId != None :
                valuesTuple = (str(unit["unit_id"]), clientId, legalEntityId, str(unit["country_id"]), str(unit["geography_id"]),
                    str(unit["industry_id"]), domainIds, str(unit["unit_code"]), str(unit["unit_name"]), str(unit["unit_address"]),
                    str(unit["postal_code"]), 1, sessionUser, currentTimeStamp, sessionUser, currentTimeStamp, 
                    divisionId)   
            else: 
                valuesTuple = (str(unit["unit_id"]), clientId, legalEntityId, str(unit["country_id"]), str(unit["geography_id"]),
                        str(unit["industry_id"]), domainIds, str(unit["unit_code"]), str(unit["unit_name"]), str(unit["unit_address"]),
                        str(unit["postal_code"]), 1, sessionUser, currentTimeStamp, sessionUser, currentTimeStamp)
            valuesList.append(valuesTuple)
        return self.bulkInsert(self.tblUnits, columns, valuesList)


    def updateUnit(self, clientId,  units, businessGroupId, legalEntityId, divisionId, sessionUser):
        currentTimeStamp = str(getCurrentTimeStamp())
        columns = ["country_id", "geography_id", "industry_id", "domain_ids", "unit_code", "unit_name", 
        "address", "postal_code", "updated_by", "updated_on"]
        valuesList = []
        for unit in units:
            domainIds = ",".join(str(x) for x in unit["domain_ids"])
            values= [unit["country_id"], unit["geography_id"],unit["industry_id"], domainIds, 
                        str(unit["unit_code"]), str(unit["unit_name"]), str(unit["unit_address"]),
                        str(unit["postal_code"]), sessionUser, currentTimeStamp]
            condition = "client_id='%d' and unit_id = '%d'" % (clientId, unit["unit_id"])
            self.update(self.tblUnits, columns, values, condition)
        return True

    def changeClientStatus(self, clientId, legalEntityId, divisionId, isActive, sessionUser):
        currentTimeStamp = str(getCurrentTimeStamp())
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [isActive, currentTimeStamp, sessionUser]
        condition = "legal_entity_id = '%d' and client_id = '%d' "% (legalEntityId, clientId)
        if divisionId != None:
            condition += " and division_id='%d' "% divisionId
        return self.update(self.tblUnits, columns, values, condition)

    def reactivateUnit(self, clientId, unitId, sessionUser):
        currentTimeStamp = str(getCurrentTimeStamp())
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [1, currentTimeStamp, sessionUser]
        condition = "unit_id = '%d' and client_id = '%d' "% (unitId, clientId)
        return self.update(self.tblUnits, columns, values, condition)

    def truncate(self, table):
        query = "TRUNCATE TABLE  %s;" % table
        return self.execute(query)

    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
        return _databaseHandlerInstance
