import datetime
import os
import MySQLdb as mysql
from aparajitha.server.constants import ROOT_PATH
from commonfunctions import getCurrentTimeStamp, generatePassword

__all__ = [
    "ClientDatabaseHandler"
]



_databaseHandlerInstance = None 
sqlScriptPath = os.path.join(ROOT_PATH, "Src-client/files/desktop/common/clientdatabase/client-tables.sql")

class ClientDatabaseHandler(object) :

    tblActivityLog = "tbl_activity_log"
    tblAdmin = "tbl_admin"
    tblApprovalStatus = "tbl_approval_status"
    tblAssignedCompliances = "tbl_assigned_compliances"
    tblBusinessGroups = "tbl_business_groups"
    tblClientCompliances = "tbl_client_compliances"
    tblClientConfigurations = "tbl_client_configurations"
    tblClientSettings = "tbl_client_settings"
    tblClientStatutories = "tbl_client_statutories"
    tblComplianceActivityLog = "tbl_compliance_activity_log"
    tblComplianceDurationType = "tbl_compliance_duration_type"
    tblComplianceFrequency = "tbl_compliance_frequency"
    tblComplianceHistory = "tbl_compliance_history"
    tblComplianceRepeatType = "tbl_compliance_repeat_type"
    tblComplianceStatus = "tbl_compliance_status"
    tblCompliances = "tbl_compliances"
    tblCountries = "tbl_countries"
    tblDivisions = "tbl_divisions"
    tblDomains = "tbl_domains"
    tblEmailVerification = "tbl_email_verification"
    tblFormType = "tbl_form_type"
    tblForms = "tbl_forms"
    tblLegalEntities = "tbl_legal_entities"
    tblMobileRegistration = "tbl_mobile_registration"
    tblNotificationTypes = "tbl_notification_types"
    tblNotificationUserLog = "tbl_notification_user_log"
    tblNotificationsLog = "tbl_notifications_log"
    tblReassignedCompliancesHistory = "tbl_reassigned_compliances_history"
    tblServiceProviders = "tbl_service_providers"
    tblSessionTypes = "tbl_session_types"
    tblStatutoryNotificationStatus = "tbl_statutory_notification_status"
    tblStatutoryNotificationsLog = "tbl_statutory_notifications_log"
    tblStatutoryNotificationsUnits = "tbl_statutory_notifications_units"
    tblUnits = "tbl_units"
    tblUserCountries = "tbl_user_countries"
    tblUserDomains = "tbl_user_domains"
    tblUserGroups = "tbl_user_groups"
    tblUserLoginHistory = "tbl_user_login_history"
    tblUserSessions = "tbl_user_sessions"
    tblUserUnits = "tbl_user_units"
    tblUsers = "tbl_users"



    def __init__(self,  databaseName) :
        self.mysqlHost = "localhost"
        self.mysqlUser = "root"
        self.mysqlPassword = "123456"
        self.mysqlDatabase = databaseName

    def dbConnect(self) :
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword, self.mysqlDatabase
        )

    def createClientDatabaseTables(self):
        fileObj = open(sqlScriptPath, 'r')
        sqlFile = fileObj.read()
        fileObj.close()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            if command != "":
                self.execute(command)
            else:
                continue


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
        query = "SELECT %s FROM %s WHERE %s" %(columns, table, condition)
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
        WHERE session_id = '%s'" % sessionToken
        rows = self.executeAndReturn(query)
        row = rows[0]
        return row[0]

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

    def truncate(self, table):
        query = "TRUNCATE TABLE  %s;" % table
        return self.execute(query)

    def verifyPassword(self, password, userId):
        columns = "count(*)"
        condition = "password='%s' and user_id='%d'" % (password, userId)
        rows = self.getData(self.tblUsers, columns, condition)
        if(int(rows[0][0]) <= 0):
            return False
        else:
            return True

    def getUserPrivilegeDetailsList(self):
        columns = "user_group_id, user_group_name, form_ids, is_active"
        rows = self.getData(self.tblUserGroups, columns, "1")
        return rows

    def getUserPrivileges(self):
        columns = "user_group_id, user_group_name, is_active"
        rows = self.getData(self.tblUserGroups, columns, "1")
        return rows        
    
    def saveUserPrivilege(self, userprivilege, sessionUser):
        columns = ["user_group_id", "user_group_name","form_ids", "is_active",
                  "created_on", "created_by", "updated_on", "updated_by"]
        valuesList =  [userprivilege.userGroupId, userprivilege.userGroupName, 
                        ",".join(str(x) for x in userprivilege.formIds), userprivilege.isActive, 
                        getCurrentTimeStamp(), sessionUser,getCurrentTimeStamp(), 
                        sessionUser]
        return self.insert(self.tblUserGroups, columns, valuesList)

    def updateUserPrivilege(self, userPrivilege, sessionUser):
        columns = ["user_group_name","form_ids", "updated_on", "updated_by"]
        values =  [ userPrivilege.userGroupName, ",".join(str(x) for x in userPrivilege.formIds),
                    getCurrentTimeStamp(),sessionUser]
        condition = "user_group_id='%d'" % userPrivilege.userGroupId
        return self.update(self.tblUserGroups, columns, values, condition)

    def updateUserPrivilegeStatus(self, userGroupId, isActive, sessionUser):
        columns = ["is_active", "updated_by", "updated_on"]
        values = [isActive, sessionUser, getCurrentTimeStamp()]
        condition = "user_group_id='%d'" % userGroupId
        return self.update(self.tblUserGroups, columns, values, condition)

    def getUserDetails(self):
        columns = "user_id, email_id, user_group_id, employee_name,"+\
        "employee_code, contact_no, seating_unit_id, user_level, "+\
        " is_admin, is_service_provider, service_provider_id, is_active"
        condition = "1"
        return self.getData(self.tblUsers,columns, condition)

    def saveUser(self, user, sessionUser):
        result1 = None
        result2 = None
        result3 = None
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["user_id", "user_group_id", "email_id", "password", "employee_name", 
                "employee_code", "contact_no", "seating_unit_id", "user_level", 
                "is_admin", "is_service_provider","created_by", "created_on", 
                "updated_by", "updated_on"]
        values = [ user.userId, user.userGroupId, user.emailId, generatePassword(), user.employeeName,
                user.employeeCode, user.contactNo, user.seatingUnitId, user.userLevel, 
                user.isAdmin, user.isServiceProvider, sessionUser,currentTimeStamp,
                sessionUser, currentTimeStamp]
        if user.isServiceProvider == 1:
            columns.append("service_provider_id")
            values.append(user.serviceProviderId)

        result1 = self.insert(self.tblUsers, columns, values)

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
        
        unitColumns = ["user_id", "unit_id"]
        unitValuesList = []
        for unitId in user.unitIds:
            unitValueTuple = (user.userId, int(unitId))
            unitValuesList.append(unitValueTuple)
        result4 = self.bulkInsert(self.tblUserUnits, unitColumns, unitValuesList)

        return (result1 and result2 and result3 and result4)

    def updateUser(self, user, sessionUser):
        result1 = None
        result2 = None
        result3 = None
        result4 = None

        currentTimeStamp = getCurrentTimeStamp()
        columns = [ "user_group_id", "employee_name", "employee_code",
                "contact_no", "seating_unit_id", "user_level", "is_admin", 
                "is_service_provider", "updated_on", "updated_by"]
        values = [ user.userGroupId, user.employeeName, user.employeeCode,
                user.contactNo, user.seatingUnitId, user.userLevel, 
                user.isAdmin, user.isServiceProvider, currentTimeStamp, sessionUser ]
        condition = "user_id='%d'" % user.userId

        if user.isServiceProvider == 1:
            columns.append("service_provider_id")
            values.append(user.serviceProviderId)

        result1 = self.update(self.tblUsers, columns, values, condition)
        self.delete(self.tblUserCountries, condition)
        self.delete(self.tblUserDomains, condition)
        self.delete(self.tblUserUnits, condition)

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
        
        unitColumns = ["user_id", "unit_id"]
        unitValuesList = []
        for unitId in user.unitIds:
            unitValueTuple = (user.userId, int(unitId))
            unitValuesList.append(unitValueTuple)
        result4 = self.bulkInsert(self.tblUserUnits, unitColumns, unitValuesList)

        return (result1 and result2 and result3 and result4)

    def updateUserStatus(self, userId, isActive, sessionUser):
        columns = ["is_active", "updated_on", "updated_by"]
        values = [isActive, getCurrentTimeStamp(), sessionUser]
        condition = "user_id = '%d'"% userId
        return self.update(self.tblUsers, columns, values, condition)

    def updateAdminStatus(self, userId, isAdmin, sessionUser):
        columns = ["is_admin", "updated_on" , "updated_by"]
        values = [isAdmin, getCurrentTimeStamp(), sessionUser]
        condition = "user_id='%d'" % userId
        return self.update(self.tblUsers, columns, values, condition)

    def getUserCompanyDetails(self, userId):
        columns = "group_concat(unit_id)"
        condition = " user_id = '%d'"% userId
        rows = self.getData(self.tblUserUnits, columns, condition)
        unitIds = rows[0][0]

        columns = "group_concat(division_id), group_concat(legal_entity_id), "+\
        "group_concat(business_group_id)"
        unitCondition = "unit_id in (%s)" % unitIds
        rows = self.getData(self.tblUnits , columns, unitCondition)

        divisionIds = rows[0][0]
        legalEntityIds = rows[0][1]
        businessGroupIds = rows[0][2]
        return unitIds, divisionIds, legalEntityIds, businessGroupIds
        
    def getUserCountries(self, userId):
        columns = "group_concat(country_id)"
        condition = " user_id = '%d'"% userId
        rows = self.getData( self.tblUserCountries,columns, condition)
        return rows[0][0]

    def getUserDomains(self, userId):
        columns = "group_concat(domain_id)"
        condition = " user_id = '%d'"% userId
        rows = self.getData(self.tblUserDomains, columns, condition)
        return rows[0][0]

    def getUserUnitIds(self, userId):
        columns = "group_concat(unit_id)"
        condition = " user_id = '%d'"% userId
        rows = self.getData(self.tblUserUnits, columns, condition)
        return rows[0][0]

    def deactivateUnit(self, unitId):
        columns = ["is_active"]
        values = [0]
        condition = "unit_id ='%d'" % unitId
        return self.update(self.tblUnits, columns, values, condition)

    def getUnitClosureList(self):
        columns = "tu.unit_id, tu.unit_name, tu.unit_code, td.division_name, tle.legal_entity_name,"+\
        "tbg.business_group_name, tu.address, tu.is_active"
        tables = [self.tblUnits, self.tblDivisions, self.tblLegalEntities, 
                self.tblBusinessGroups]
        aliases = ["tu", "td", "tle", "tbg"]
        joinConditions = ["tu.division_id = td.division_id", "tu.legal_entity_id = tle.legal_entity_id",
        "tu.business_group_id =tbg.business_group_id" ]
        whereCondition = "1"
        joinType = "left join"

        rows = self.getDataFromMultipleTables(columns, tables, aliases, joinType, 
            joinConditions, whereCondition)

        return rows

    def getUserUnits(self, unitIds):
        unitColumns = "unit_id, division_id, legal_entity_id, business_group_id, unit_code,"+\
        "unit_name, address, is_active"
        unitCondition = "unit_id in (%s)"% unitIds
        return self.getData(self.tblUnits, unitColumns,  unitCondition)

    def getUserDivisions(self, divisionIds):
        divisionColumns = " division_id, legal_entity_id, business_group_id, division_name"
        divisionCondition = "division_id in (%s)"% divisionIds
        return self.getData(self.tblDivisions, divisionColumns, divisionCondition)
    
    def getUserLegalEntities(self, legalEntityIds):
        legalEntityColumns = "legal_entity_id, business_group_id, legal_entity_name"
        legalEntityCondition = "legal_entity_id in (%s)"% legalEntityIds
        return self.getData(self.tblLegalEntities, legalEntityColumns,legalEntityCondition)        

    def getUserBusinessGroups(self, businessGroupIds):
        businessGroupColumns = "business_group_id, business_group_name"
        businessGroupCondition = "business_group_id in (%s)"% businessGroupIds
        return self.getData(self.tblBusinessGroups, businessGroupColumns, businessGroupCondition)

    def getServiceProviderDetailsList(self):
        columns = "service_provider_id, service_provider_name, address, contract_from,"+\
                "contract_to, contact_person, contact_no, is_active"
        rows = self.getData(self.tblServiceProviders, columns, "1")
        return rows

    def getServiceProviders(self):
        columns = "service_provider_id, service_provider_name, is_active"
        rows = self.getData(self.tblServiceProviders, columns, "1")
        return rows          

    def saveServiceProvider(self, serviceProvider, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = ["service_provider_id", "service_provider_name", "address", "contract_from",
                "contract_to", "contact_person", "contact_no", "created_on", "created_by", 
                "updated_on", "updated_by"]
        values = [serviceProvider.serviceProviderId, serviceProvider.serviceProviderName, 
                    serviceProvider.address, serviceProvider.contractFrom, serviceProvider.contractTo, 
                    serviceProvider.contactPerson, serviceProvider.contactNo,
                    currentTimeStamp, sessionUser, currentTimeStamp, sessionUser]

        return self.insert(self.tblServiceProviders,columns, values)

    def updateServiceProvider(self, serviceProvider, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columnsList = [ "service_provider_name", "address", "contract_from", "contract_to", 
                    "contact_person", "contact_no", "updated_on", "updated_by"]
        valuesList = [serviceProvider.serviceProviderName, serviceProvider.address, 
                serviceProvider.contractFrom, serviceProvider.contractTo, serviceProvider.contactPerson, 
                serviceProvider.contactNo, currentTimeStamp, sessionUser]
        condition = "service_provider_id='%d'" % serviceProvider.serviceProviderId
        return self.update(self.tblServiceProviders, columnsList, valuesList, condition)

    def updateServiceProviderStatus(self, serviceProviderId,  isActive, sessionUser):
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [isActive, getCurrentTimeStamp(), sessionUser]
        condition = "service_provider_id='%d'" % serviceProviderId
        return self.update(self.tblServiceProviders, columns, values, condition)

    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        _databaseHandlerInstance = None 
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = ClientDatabaseHandler("mirror_client")
        return _databaseHandlerInstance
