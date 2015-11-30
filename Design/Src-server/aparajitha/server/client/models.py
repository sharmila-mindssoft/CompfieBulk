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
    def getList(self):
        userGroupList = []
        columns = "user_group_id, user_group_name"
        rows = ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).getData(
            UserGroup.tblName, columns, "1")

        for row in rows:
            userGroup = UserGroup(int(row[0]), row[1], None, None, None)
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
    detailTblName = "tbl_user_details"

    def __init__(self, userId, emailId, userGroupId, employeeName, 
                employeeCode, contactNo, address, designation, countryIds,
                domainIds, clientId,isActive) :
        self.userId =  userId if userId != None else self.generateNewUserId()
        self.emailId =  emailId
        self.userGroupId =  userGroupId
        self.employeeName =  employeeName
        self.employeeCode =  employeeCode
        self.contactNo =  contactNo
        self.address =  address
        self.designation =  designation
        self.countryIds =  countryIds
        self.domainIds =  domainIds
        self.clientId = clientId
        self.isActive = isActive if isActive != None else 1

    def verify(self) :
        assertType(self.userId, IntType)
        assertType(self.emailId, StringType)
        assertType(self.userGroupId, IntType)
        assertType(self.employeeName, StringType)
        assertType(self.employeeCode, StringType)
        assertType(self.contactNo, StringType)
        assertType(self.address, StringType)
        assertType(self.designation, StringType)
        assertType(self.countryIds, ListType)
        assertType(self.domainIds, ListType)
        assertType(self.clientId, IntType)
        assertType(self.isActive, IntType)

    def toDetailedStructure(self) :
        return {
            "user_id": self.userId,
            "email_id": self.emailId,
            "user_group_id": self.userGroupId,
            "employee_name": self.employeeName,
            "employee_code": self.employeeCode,
            "contact_no": self.contactNo,
            "address": self.address, 
            "designation": self.designation,
            "country_ids": self.countryIds,
            "domain_ids": self.domainIds,
            "client_id": self.clientId,
            "is_active": self.isActive
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
        }

    @classmethod
    def getDetailedList(self):
        userList = []
        columns = "user_id, is_active"
        rows = DatabaseHandler.instance().getData(User.mainTblName, columns, "1")

        for row in rows:
            userId = row[0]
            isActive = row[1]
            subColumns = "email_id, user_group_id, employee_name, employee_code,"+\
                                "contact_no, address, designation, country_ids,"+\
                                "domain_ids,client_ids"
            condition = " user_id ='"+str(userId)+"'"                                
            subRows = DatabaseHandler.instance().getData(User.detailTblName, subColumns, condition)
            for subRow in subRows:
                user = User(userId,subRow[0], subRow[1],subRow[2], subRow[3],
                     subRow[4], subRow[5], subRow[6], subRow[7], subRow[8], subRow[9],isActive)
                userList.append(user.toDetailedStructure())
        return userList

    @classmethod
    def getList(self):
        userList = []
        columns = "user_id, employee_name, employee_code"
        rows = DatabaseHandler.instance().getData(User.detailTblName, columns, "1")

        for row in rows:
            print "inside for loop in user model"
            user = User(int(row[0]),None,None, row[1], row[2],
                 None, None, None, None, None, None, None)
            userList.append(user.toStructure())

        return userList

    def generateNewUserId(self) :
        return DatabaseHandler.instance().generateNewId(self.mainTblName, "user_id")

    def isDuplicateEmail(self):
        condition = "username ='"+self.emailId+\
                "' AND user_id != '"+str(self.userId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.mainTblName, condition)

    def isDuplicateEmployeeCode(self):
        condition = "employee_code ='"+self.employeeCode+\
                "' AND user_id != '"+str(self.userId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.detailTblName, condition)

    def isDuplicateContactNo(self):
        condition = "contact_no ='"+self.contactNo+\
                "' AND user_id != '"+str(self.userId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.detailTblName, condition)

    def isIdInvalid(self):
        condition = "user_id = '"+str(self.userId)+"'"
        return not DatabaseHandler.instance().isAlreadyExists(self.mainTblName, condition)

    def getFormType(self) :
        rows = DatabaseHandler.instance().getData(UserGroup.tblName, 
                    "form_type", "user_group_id='"+str(self.userGroupId)+"'")
        return rows[0][0]

    def saveAdmin(self, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()

        mainTblColumns = "user_id, username, password, client_id, created_on,created_by, updated_on, updated_by"
        mainTblValuesList = [ self.userId, self.emailId, generatePassword(), self.clientId, 
                            currentTimeStamp,sessionUser,
                            currentTimeStamp,sessionUser]
        mainTblValues = listToString(mainTblValuesList)
        return DatabaseHandler.instance().insert(self.mainTblName, mainTblColumns, mainTblValues)

    def save(self, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        mainTblColumns = "user_id, username, password, client_id,created_on,created_by, updated_on, updated_by"
        mainTblValuesList = [self.userId, self.emailId, generatePassword(), self.clientId,
                            currentTimeStamp,sessionUser,
                            currentTimeStamp,sessionUser]
        detailTblcolumns = "user_id, email_id, user_group_id, form_type,employee_name, "+\
                            "employee_code, contact_no, address, designation, country_ids,"+\
                            " domain_ids, created_on, created_by, updated_on, updated_by"
        detailTblValuesList = [ self.userId, self.emailId, self.userGroupId, self.getFormType(),
                            self.employeeName, self.employeeCode, self.contactNo, self.address,
                            self.designation, ",".join(str(x) for x in self.countryIds), 
                            ",".join(str(x) for x in self.domainIds), currentTimeStamp,sessionUser,
                            currentTimeStamp,sessionUser]

        mainTblValues = listToString(mainTblValuesList)
        detailTblValues = listToString(detailTblValuesList)

        if DatabaseHandler.instance().insert(self.mainTblName, mainTblColumns, mainTblValues): 
            return DatabaseHandler.instance().insert(self.detailTblName, 
                detailTblcolumns, detailTblValues)
        else : 
            return False

    def update(self, sessionUser):
        currentTimeStamp = getCurrentTimeStamp()
        detailTblcolumns = [ "user_group_id", "form_type", "employee_name", "employee_code", 
                            "contact_no", "address", "designation", "country_ids", "domain_ids",
                            "updated_on", "updated_by"]
        detailTblValuesList = [ self.userGroupId, self.getFormType(), self.employeeName, self.employeeCode,
                            self.contactNo, self.address, self.designation, convertToString(",".join(self.countryIds)),
                            convertToString(",".join(self.domainIds)), currentTimeStamp,sessionUser ]
        condition = "user_id='"+str(self.userId)+"'"
        return DatabaseHandler.instance().update(self.detailTblName, detailTblcolumns,
                                                detailTblValuesList, condition)

    def updateStatus(self, sessionUser):
        assertType(self.userId, IntType)
        assertType(self.isActive, IntType)
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [self.isActive, getCurrentTimeStamp(), sessionUser]
        condition = "user_id='"+str(self.userId)+"'"
        return DatabaseHandler.instance().update(self.mainTblName, columns, values, condition)
            
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
