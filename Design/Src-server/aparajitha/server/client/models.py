from types import *
from aparajitha.server.databasehandler import DatabaseHandler 
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler 
import json
from aparajitha.server.common import *

__all__ = [
    "UserPrivilege",
    "User",
    "ServiceProvider"
]

class UserPrivilege() :
    tblName = "tbl_client_user_groups"
    userTblName = "tbl_users"

    def __init__(self, clientId, userGroupId, userGroupName, formType, formIds, isActive) :
        self.clientId = clientId
        self.userGroupId =  userGroupId if userGroupId != None else self.generateNewUserGroupId()
        self.userGroupName = userGroupName
        self.formType = formType 
        self.formIds = formIds 
        self.isActive = isActive if isActive != None else 1

    def verify(self) :
        assertType(self.userGroupId, IntType)
        assertType(self.userGroupName, StringType)
        assertType(self.formType, StringType)
        assertType(self.formIds, ListType)
        assertType(self.isActive, IntType)

    def toDetailedStructure(self) :
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName,
            "form_type": self.formType,
            "form_ids": self.formIds,
            "is_active": self.isActive
        }

    def toStructure(self):
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName
        }

    def generateNewUserGroupId(self) :
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).generateNewId(
            self.tblName, "user_group_id")

    def isDuplicate(self):
        condition = "user_group_name ='"+self.userGroupName+\
                "' AND user_group_id != '"+str(self.userGroupId)+"'"
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(
            self.tblName, condition)

    def isIdInvalid(self):
        condition = "user_group_id = '"+str(self.userGroupId)+"'"
        return not ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(
            self.tblName, condition)
    
    @classmethod
    def getDetailedList(self, sessionUser) :
        userGroupList = []
        columns = "user_group_id, user_group_name,form_type, "+\
                    "form_ids, is_active"
        rows = ClientDatabaseHandler.instance(
            getClientDatabase(getClientId(sessionUser))).getData(
            UserPrivilege.tblName, columns, "1")

        for row in rows:
            userGroup = UserPrivilege(None, int(row[0]), row[1], row[2], row[3].split(","), row[4])
            userGroupList.append(userGroup.toDetailedStructure())

        return userGroupList

    @classmethod
    def getList(self, clientId):
        userGroupList = []
        columns = "user_group_id, user_group_name"
        rows = ClientDatabaseHandler.instance(
            getClientDatabase(clientId)).getData(
            UserPrivilege.tblName, columns, "1")

        for row in rows:
            userGroup = UserPrivilege(clientId, int(row[0]), row[1], None, None, None)
            userGroupList.append(userGroup.toStructure())

        return userGroupList

    def save(self, sessionUser):
        self.verify()
        columns = "user_group_id, user_group_name,form_type, form_ids, is_active,"+\
                  " created_on, created_by, updated_on, updated_by"
        valuesList =  [self.userGroupId, self.userGroupName, self.formType, ",".join(self.formIds),
                        self.isActive, getCurrentTimeStamp(), sessionUser,getCurrentTimeStamp(), 
                        sessionUser]
        values = listToString(valuesList)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).insert(
            self.tblName,columns,values)

    def update(self, sessionUser):
        self.verify()
        columns = ["user_group_name","form_type","form_ids", "updated_on", "updated_by"]
        values =  [ self.userGroupName, self.formType, convertToString(",".join(self.formIds)),
                    getCurrentTimeStamp(),sessionUser]
        condition = "user_group_id='"+str(self.userGroupId)+"'"
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.tblName, columns, values, condition)

    def updateStatus(self, sessionUser):
        assertType(self.userGroupId, IntType)
        assertType(self.isActive, IntType)
        columns = ["is_active", "updated_by", "updated_on"]
        values = [self.isActive, sessionUser, getCurrentTimeStamp()]
        condition = "user_group_id='"+str(self.userGroupId)+"'"
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.tblName, columns, values, condition)

class User(object) :
    mainTblName = "tbl_users"
    detailTblName = "tbl_client_user_details"

    def __init__(self, clientId ,userId, emailId, userGroupId, employeeName, employeeCode, 
        contactNo, seatingUnitId, userLevel, countryIds, domainIds, unitIds, 
        isAdmin, isServiceProvider, serviceProviderId ) :
        self.clientId = clientId
        self.userId =  userId if userId != None else self.generateNewUserId()
        self.emailId =  emailId
        self.userGroupId =  userGroupId
        self.employeeName =  employeeName
        self.employeeCode =  employeeCode
        self.contactNo =  contactNo
        self.seatingUnitId =  seatingUnitId
        self.userLevel =  userLevel
        self.countryIds =  countryIds
        self.domainIds =  domainIds
        self.unitIds =  unitIds
        self.isAdmin =  isAdmin
        self.isServiceProvider =  isServiceProvider
        self.serviceProviderId =  serviceProviderId

    def verify(self) :
        assertType(self.userId, IntType)
        assertType(self.emailId, StringType)
        assertType(self.userGroupId, IntType)
        assertType(self.employeeName, StringType)
        assertType(self.employeeCode, StringType)
        assertType(self.contactNo, StringType)
        assertType(self.seatingUnitId, IntType)
        assertType(self.userLevel, IntType)
        assertType(self.countryIds, ListType)
        assertType(self.domainIds, ListType)
        assertType(self.unitIds, ListType)
        assertType(self.isAdmin, IntType)
        assertType(self.isServiceProvider, IntType)
        assertType(self.serviceProviderId, IntType)

    def toDetailedStructure(self) :
        employeeName = "%s - %s" % (self.employeeCode,self.employeeName)
        return {
            "user_id": self.userId,
            "email_id": self.emailId,
            "user_group_id": self.userGroupId,
            "employee_name": employeeName,
            "contact_no": self.contactNo,
            "seating_unit_id": self.seatingUnitId, 
            "user_level": self.userLevel,
            "country_ids": self.countryIds,
            "domain_ids": self.domainIds,
            "unit_ids": self.unitIds,
            "is_admin": self.isAdmin,
            "is_service_provider": self.isServiceProvider,
            "service_provider_id": self.serviceProviderId
        }

    def toStructure(self):
        employeeName = None
        if self.employeeCode == None:
            employeeName = self.employeeName
        else:
            employeeName = "%s-%s" % (self.employeeCode, self.employeeName)
        return {
            "user_id": self.userId,
            "employee_name": employeeName,
            "user_level": self.userLevel
        }

    @classmethod
    def getDetailedList(self, clientId):
        userList = []
        columns = "user_id, is_active"
        condition = "client_id='%d'" % int(clientId)
        rows = DatabaseHandler.instance().getData(
            User.mainTblName, columns, condition)
        for row in rows:
            userId = row[0]
            isActive = row[1]
            subColumns = "email_id, user_group_id, employee_name, employee_code,"+\
                        " contact_no, seating_unit_id, user_level, country_ids,"+\
                        " domain_ids, unit_ids, is_admin, is_service_provider"
            condition = " user_id ='%d'" % int(userId)                               
            subRows = ClientDatabaseHandler.instance(
                        getClientDatabase(clientId)).getData(
                        User.detailTblName, subColumns, condition)
            for subRow in subRows:
                emailId = subRow[0]
                userGroupId = subRow[1]
                employeeName = subRow[2]
                employeeCode = subRow[3]
                contactNo =  subRow[4]
                seatingUnitId = subRow[5]
                userLevel = subRow[6]
                countryIds = subRow[7]
                domainIds = subRow[8]
                unitIds = subRow[9]
                isAdmin = subRow[10]
                isServiceProvider = subRow[11]
                user = User(clientId,userId, emailId, userGroupId, 
                            employeeName, employeeCode, contactNo, 
                            seatingUnitId, userLevel, countryIds, 
                            domainIds, unitIds, isAdmin, isServiceProvider, 
                            None )
                userList.append(user.toDetailedStructure())
        return userList

    @classmethod
    def getList(self, clientId):
        userList = []
        columns = "user_id, employee_name, employee_code"
        rows = ClientDatabaseHandler.instance(
                        getClientDatabase(self.clientId)).getData(
                        User.detailTblName, columns, "1")

        for row in rows:
            user = User(int(row[0]),None,None, row[1], row[2],
                 None, None, None, None, None, None, None)
            userList.append(user.toStructure())

        return userList

    def generateNewUserId(self) :
        return DatabaseHandler.instance().generateNewId(self.mainTblName, "user_id")

    def isDuplicateEmail(self):
        condition = "username ='%s' AND user_id != '%d'" % (self.emailId, self.userId)
        return DatabaseHandler.instance().isAlreadyExists(self.mainTblName, condition)

    def isDuplicateEmployeeCode(self):
        condition = "employee_code ='%s' AND user_id != '%d'" % (self.employeeCode, self.userId)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.detailTblName, condition)

    def isDuplicateContactNo(self):
        condition = "contact_no ='%s' AND user_id != '%d'" % (self.contactNo, self.userId)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.detailTblName, condition)

    def isIdInvalid(self):
        condition = "user_id = '%d'" % self.userId
        return not DatabaseHandler.instance().isAlreadyExists(self.mainTblName, condition)


    def save(self, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        mainTblColumns = "user_id, username, password, client_id,created_on,created_by,"+\
                        " updated_on, updated_by"
        mainTblValuesList = [self.userId, self.emailId, generatePassword(), self.clientId,
                            currentTimeStamp,sessionUser,
                            currentTimeStamp,sessionUser]
        detailTblcolumns = "user_id, email_id, user_group_id, employee_name, employee_code,"+\
                            " contact_no, seating_unit_id, user_level, country_ids,"+\
                            " domain_ids, unit_ids, is_admin, is_service_provider, "+\
                            " created_by, created_on, updated_by,updated_on"
        detailTblValuesList = [ self.userId, self.emailId, self.userGroupId, self.employeeName,
                                self.employeeCode, self.contactNo, self.seatingUnitId, 
                                self.userLevel, ",".join(str(x) for x in self.countryIds), 
                                ",".join(str(x) for x in self.domainIds), 
                                ",".join(str(x) for x in self.unitIds), self.isAdmin,
                                self.isServiceProvider, sessionUser,currentTimeStamp,
                                sessionUser, currentTimeStamp,]

        if self.isServiceProvider == 1:
            detailTblcolumns += ", service_provider_id" 
            detailTblValuesList.append(self.serviceProviderId)

        mainTblValues = listToString(mainTblValuesList)
        detailTblValues = listToString(detailTblValuesList)

        if DatabaseHandler.instance().insert(self.mainTblName, mainTblColumns, mainTblValues): 
            return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).insert(
                self.detailTblName, detailTblcolumns, detailTblValues)
        else : 
            return False

    def update(self, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        detailTblcolumns = [ "user_group_id", "employee_name", "employee_code",
                            "contact_no", "seating_unit_id", "user_level", "country_ids",
                            "domain_ids", "unit_ids", "is_admin", "is_service_provider",
                             "updated_on", "updated_by"]
        detailTblValuesList = [ self.userGroupId, self.employeeName, self.employeeCode,
                            self.contactNo, self.seatingUnitId, self.userLevel, 
                            ",".join(str(x) for x in self.countryIds),
                            ",".join(str(x) for x in self.domainIds),
                            ",".join(str(x) for x in self.unitIds), self.isAdmin, 
                            self.isServiceProvider, currentTimeStamp, sessionUser ]
        condition = "user_id='%d'" % self.userId

        if self.isServiceProvider == 1:
            detailTblcolumns.append("service_provider_id")
            detailTblValuesList.append(self.serviceProviderId)

        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.detailTblName, detailTblcolumns, detailTblValuesList, condition)

    def updateAdminStatus(self, sessionUser):
        print "inside update Admin status in model"
        columns = ["is_admin", "updated_on" , "updated_by"]
        values = [self.isAdmin, getCurrentTimeStamp(), sessionUser]
        condition = "user_id='%d'" % self.userId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.detailTblName, columns, values, condition)

            
class ServiceProvider(object):
    tblName = " tbl_service_providers"

    def __init__(self, clientId, serviceProviderId, serviceProviderName, address, 
                contractFrom, contractTo, contactPerson, contactNo, isActive) :
        self.clientId = clientId
        self.serviceProviderId =  serviceProviderId if serviceProviderId != None else self.generateNewUserId()
        self.serviceProviderName =  serviceProviderName
        self.address =  address
        self.contractFrom =  contractFrom
        self.contractTo =  contractTo
        self.contactPerson =  contactPerson
        self.contactNo =  contactNo
        self.isActive = isActive if isActive != None else 1

    def verify(self) :
        assertType(self.serviceProviderId, IntType)
        assertType(self.serviceProviderName, StringType)
        assertType(self.address, StringType)
        assertType(self.contractFrom, StringType)
        assertType(self.contractTo, StringType)
        assertType(self.contactPerson, StringType)
        assertType(self.contactNo, StringType)
        assertType(self.isActive, IntType)

    def toStructure(self):
        return {
        "service_provider_id": self.serviceProviderId,
        "service_provider_name": self.serviceProviderName, 
        "address": self.address,
        "contract_from": self.contractFrom,
        "contract_to": self.contractTo, 
        "contact_person": self.contactPerson,
        "contact_no": self.contactNo,
        "is_active": self.isActive
    }

    @classmethod
    def getList(self, sessionUser):
        servcieProviderList = []
        columns = "service_provider_id, service_provider_name, address, contract_from,"+\
                "contract_to, contact_person, contact_no, is_active"

        clientId = getClientId(sessionUser)
        rows = ClientDatabaseHandler.instance(getClientDatabase(clientId)).getData(
            ServiceProvider.tblName, columns, "1")

        for row in rows:
            serviceProviderId = int(row[0])
            serviceProviderName = row[1]
            address = row[2]
            contractFrom = datetimeToString(timestampToDatetime(row[3]))
            contractTo = datetimeToString(timestampToDatetime(row[4]))
            contactPerson = row[5]
            contactNo = row[6]
            isActive = row[7]
            serviceProvider = ServiceProvider(None, serviceProviderId, serviceProviderName, address, 
                contractFrom, contractTo, contactPerson, contactNo, isActive)
            servcieProviderList.append(serviceProvider.toStructure())

        return servcieProviderList

    def generateNewUserId(self) :
        return ClientDatabaseHandler.instance(getClientDatabase(
            self.clientId)).generateNewId(self.tblName, "service_provider_id")

    def isDuplicate(self):
        condition = "service_provider_name ='%s' AND service_provider_id != '%d'" %(
            self.serviceProviderName, self.serviceProviderId)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(
            self.tblName, condition)

    def isDuplicateContactNo(self):
        condition = "contact_no ='%s' AND service_provider_id != '%d'" % (self.contactNo, 
            self.serviceProviderId)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.tblName, condition)

    def isIdInvalid(self):
        condition = "service_provider_id = '%d'" % self.serviceProviderId
        return not ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.tblName, condition)

    def save(self, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columns = "service_provider_id, service_provider_name, address, contract_from,"+\
                "contract_to, contact_person, contact_no, created_on,created_by, "+\
                "updated_on, updated_by"
        valuesList = [self.serviceProviderId, self.serviceProviderName, self.address, 
                    self.contractFrom, self.contractTo, self.contactPerson, self.contactNo,
                    currentTimeStamp, sessionUser, currentTimeStamp, sessionUser]

        values = listToString(valuesList)

        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).insert(self.tblName, columns, values)

    def update(self, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        columnsList = [ "service_provider_name", "address", "contract_from", "contract_to", 
                    "contact_person", "contact_no", "updated_on", "updated_by"]
        valuesList = [self.serviceProviderName, self.address, self.contractFrom, self.contractTo,
                    self.contactPerson, self.contactNo, currentTimeStamp, sessionUser]
        condition = "service_provider_id='%d'" % self.serviceProviderId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.tblName, columnsList, valuesList, condition)

    def updateStatus(self, sessionUser):
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [self.isActive, getCurrentTimeStamp(), sessionUser]
        condition = "service_provider_id='%d'" % self.serviceProviderId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.tblName, columns, values, condition)
