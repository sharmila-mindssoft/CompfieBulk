from types import *
from aparajitha.server.databasehandler import DatabaseHandler 
import json
from aparajitha.server.common import *

__all__ = [
    "UserGroup",
    "User"
]

class UserGroup() :
    tblName = "tbl_user_groups"

    def __init__(self, userGroupId, userGroupName, formType, formIds, isActive) :
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
        return DatabaseHandler.instance().generateNewId(self.tblName, "user_group_id")

    def isDuplicate(self):
        print "inside is duplicate"
        condition = "user_group_name ='"+self.userGroupName+\
                "' AND user_group_id != '"+str(self.userGroupId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.tblName, condition)

    def isIdInvalid(self):
        print "inside isIdInvalid"
        condition = "user_group_id = '"+str(self.userGroupId)+"'"
        return not DatabaseHandler.instance().isAlreadyExists(self.tblName, condition)

    @classmethod
    def getDetailedList(self) :
        userGroupList = []
        columns = "user_group_id, user_group_name,form_type, "+\
                    "form_ids, is_active"
        rows = DatabaseHandler.instance().getData(UserGroup.tblName, columns, "1")

        for row in rows:
            userGroup = UserGroup(int(row[0]), row[1], row[2], row[3].split(","), row[4])
            userGroupList.append(userGroup.toDetailedStructure())

        return userGroupList

    @classmethod
    def getList(self):
        userGroupList = []
        columns = "user_group_id, user_group_name"
        rows = DatabaseHandler.instance().getData(UserGroup.tblName, columns, "1")

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
        return DatabaseHandler.instance().insert(self.tblName,columns,values)

    def update(self, sessionUser):
        self.verify()
        columns = ["user_group_name","form_type","form_ids", "updated_on", "updated_by"]
        values =  [ self.userGroupName, self.formType, convertToString(",".join(self.formIds)),
                    getCurrentTimeStamp(),sessionUser]
        condition = "user_group_id='"+str(self.userGroupId)+"'"
        return DatabaseHandler.instance().update(self.tblName, columns, values, condition)

    def updateStatus(self, sessionUser):
        assertType(self.userGroupId, IntType)
        assertType(self.isActive, IntType)
        columns = ["is_active", "updated_by", "updated_on"]
        values = [self.isActive, sessionUser, getCurrentTimeStamp()]
        condition = "user_group_id='"+str(self.userGroupId)+"'"
        return DatabaseHandler.instance().update(self.tblName, columns, values, condition)

class User(object) :
    mainTblName = "tbl_users"
    detailTblName = "tbl_user_details"

    def __init__(self, userId, emailId, userGroupId, employeeName, 
                employeeCode, contactNo, address, designation, countryIds,
                domainIds, isActive) :
        print "inside user constructor"
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
            "is_active": self.isActive
        }

    def toStructure(self):
        return {
            "user_id": self.userId,
            "employee_name": self.employeeName,
            "employee_code": self.employeeCode
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
                                "contact_no, address, designation, country_ids,domain_ids"
            condition = " user_id ='"+str(userId)+"'"                                
            subRows = DatabaseHandler.instance().getData(User.detailTblName, subColumns, condition)
            for subRow in subRows:
                user = User(userId,subRow[0], subRow[1],subRow[2], subRow[3],
                     subRow[4], subRow[5], subRow[6], subRow[7], subRow[8],isActive)
                userList.append(user.toDetailedStructure())
        return userList

    @classmethod
    def getList(self):
        userList = []
        columns = "user_id, employee_name, employee_code"
        rows = DatabaseHandler.instance().getData(User.detailTblName, columns, "1")

        for row in rows:
            user = User(int(row[0]),None,None, row[1], row[2],
                 None, None, None, None, None, None)
            userList.append(user.toStructure())

        return userList


    def generateNewUserId(self) :
        return DatabaseHandler.instance().generateNewId(self.mainTblName, "user_id")

    def isDuplicateEmail(self):
        print "inside isDuplicateEmail"
        condition = "username ='"+self.emailId+\
                "' AND user_id != '"+str(self.userId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.mainTblName, condition)

    def isDuplicateEmployeeCode(self):
        print "inside isDuplicateEmployeeCode"
        condition = "employee_code ='"+self.employeeCode+\
                "' AND user_id != '"+str(self.userId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.detailTblName, condition)

    def isDuplicateContactNo(self):
        print "inside isDuplicateContactNo"
        condition = "contact_no ='"+self.contactNo+\
                "' AND user_id != '"+str(self.userId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.detailTblName, condition)

    def isIdInvalid(self):
        print "inside isIdInvalid"
        condition = "user_id = '"+str(self.userId)+"'"
        return not DatabaseHandler.instance().isAlreadyExists(self.mainTblName, condition)

    def getFormType(self) :
        rows = DatabaseHandler.instance().getData(UserGroup.tblName, 
                "form_type", "user_group_id='"+str(self.userGroupId)+"'")
        return rows[0][0]

    def save(self, sessionUser):
        print "Entered save user iin models"
        currentTimeStamp = getCurrentTimeStamp()
        mainTblColumns = "user_id, username, password, created_on,created_by, updated_on, updated_by"
        mainTblValuesList = [ self.userId, self.emailId, generatePassword(), currentTimeStamp,sessionUser,
                            currentTimeStamp,sessionUser]

        detailTblcolumns = "user_id, email_id, user_group_id, form_type,employee_name, "+\
                            "employee_code, contact_no, address, designation, country_ids,"+\
                            " domain_ids, created_on, created_by, updated_on, updated_by"
        detailTblValuesList = [ self.userId, self.emailId, self.userGroupId, self.getFormType(),
                            self.employeeName, self.employeeCode, self.contactNo, self.address,
                            self.designation, ",".join(self.countryIds), ",".join(self.domainIds),
                            currentTimeStamp,sessionUser,currentTimeStamp,sessionUser]

        mainTblValues = listToString(mainTblValuesList)
        detailTblValues = listToString(detailTblValuesList)

        if DatabaseHandler.instance().insert(self.mainTblName, mainTblColumns, mainTblValues): 
            return DatabaseHandler.instance().insert(self.detailTblName, 
                detailTblcolumns, detailTblValues)
        else : 
            return False

    def update(self, sessionUser):
        print "inside user model update"
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
        print "inside user model update status"
        assertType(self.userId, IntType)
        assertType(self.isActive, IntType)
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [self.isActive, getCurrentTimeStamp(), sessionUser]
        condition = "user_id='"+str(self.userId)+"'"
        return DatabaseHandler.instance().update(self.mainTblName, columns, values, condition)
            
