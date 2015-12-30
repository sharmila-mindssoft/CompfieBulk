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
        query = "INSERT INTO %s (%s) VALUES" % (table, columns)

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

    def getDataFromMultipleTables(self, columns, tables, conditions, joinType):

        query = "SELECT %s FROM " % columns

        for index,table in enumerate(tables):
            if index == 0:
                query += "%s alias%d  %s" % (table, index, joinType)
            elif index <= len(tables) -2:
                query += " %s alias%d on (alias%d.%s = alias%d.%s) %s " % (table, 
                    index, index-1, conditions[index-1][0], index, 
                    conditions[index-1][1], joinType)
            else:
                query += " %s alias%d on (alias%d.%s = alias%d.%s)" % (table, index,
                    index-1, conditions[index-1][0], index, conditions[index-1][1])

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

    def getUserPrivileges(self):
        columns = "user_group_id, user_group_name, form_ids, is_active"
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

    def saveUser(self, user, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        
        columns = ["user_id", "user_group_id", "email_id", "password", "employee_name", 
                "employee_code", "contact_no", "seating_unit_id", "user_level", 
                "is_admin", "is_service_provider","created_by", "created_on", 
                "updated_by", "updated_on"]
        values = [ user.userId, user.userGroupId, user.emailId, generatePassword(), user.employeeName,
                user.employeeCode, user.contactNo, user.seatingUnitId, user.userLevel, 
                user.isAdmin, user.isServiceProvider, sessionUser,currentTimeStamp,
                sessionUser, currentTimeStamp]

        if self.isServiceProvider == 1:
            columns += ", service_provider_id" 
            values.append(user.serviceProviderId)
        return self.insert(self.tblUsers, columns, values)

    def updateUser(self, user, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = [ "user_group_id", "employee_name", "employee_code",
                "contact_no", "seating_unit_id", "user_level", "country_ids",
                "domain_ids", "unit_ids", "is_admin", "is_service_provider",
                "updated_on", "updated_by"]
        values = [ user.userGroupId, user.employeeName, user.employeeCode,
                user.contactNo, user.seatingUnitId, user.userLevel, 
                user.isAdmin, user.isServiceProvider, currentTimeStamp, sessionUser ]
        condition = "user_id='%d'" % user.userId

        if user.isServiceProvider == 1:
            columns.append("service_provider_id")
            values.append(user.serviceProviderId)

        return self.update(self.tblUsers, columns, values, condition)

    def updateAdminStatus(self, userId, isAdmin, sessionUser):
        columns = ["is_admin", "updated_on" , "updated_by"]
        values = [isAdmin, getCurrentTimeStamp(), sessionUser]
        condition = "user_id='%d'" % userId
        return self.update(self.tblUsers, columns, values, condition)

    def getServiceProviders(self):
        columns = "service_provider_id, service_provider_name, address, contract_from,"+\
                "contract_to, contact_person, contact_no, is_active"
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
