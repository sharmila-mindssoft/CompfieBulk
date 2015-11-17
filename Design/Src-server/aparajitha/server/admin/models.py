from types import *
from databasehandler import DatabaseHandler 
import json
from aparajitha.server.common import *

__all__ = [
    "UserGroup",
    "User"
]

class UserGroup(CMObject) :
    tblName = "tbl_user_groups"

    def __init__(self, userGroupId, userGroupName, formType, formIds, isActive) :
        self.userGroupId =  userGroupId if userGroupId != None else self.generateNewUserGroupId()
        self.userGroupName = userGroupName if userGroupName != None else ""
        self.formType = formType if formType != None else ""
        self.formIds = formIds if formIds != None else []
        self.isActive = isActive if isActive != None else 1
        self.verify()

    def verify(self) :
        assertType(self.userGroupId, IntType)
        assertType(self.userGroupName, StringType)
        assertType(self.formType, StringType)
        assertType(self.formIds, ListType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName,
            "form_type": self.formType,
            "form_ids": self.formIds,
            "is_active": self.isActive
        }

    def generateNewUserGroupId(self) :
        return DatabaseHandler.instance().generateNewId(self.tblName, "user_group_id")

    def isDuplicate(self):
        condition = "user_group_name ='"+self.userGroupName+\
                "' AND user_group_id != '"+str(self.userGroupId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.tblName, condition)

    def isIdInvalid(self):
        condition = "user_group_id = '"+str(self.userGroupId)+"'"
        return not DatabaseHandler.instance().isAlreadyExists(self.tblName, condition)

    def save(self):
        columns = "user_group_id, user_group_name,form_type, "+\
                  "form_ids, is_active, created_on, created_by, "+\
                  "updated_on, updated_by"
        valuesList =  [self.userGroupId, 
                        self.userGroupName, 
                        self.formType, 
                        ",".join(self.formIds),
                        self.isActive, 
                        getCurrentTimeStamp(),1,
                        getCurrentTimeStamp(),1
                    ]
        values = listToString(valuesList)
        return DatabaseHandler.instance().insert(self.tblName,columns,values)

    def update(self):
        columns = ["user_group_name","form_type",
                  "form_ids", "updated_on", "updated_by"]
        values =  [ self.userGroupName, 
                    self.formType, 
                    convertToString(",".join(self.formIds)),
                    getCurrentTimeStamp(),1]
        condition = "user_group_id='"+str(self.userGroupId)+"'"
        return DatabaseHandler.instance().update(self.tblName, columns, values, condition)

    def updateStatus(self):
        columns = ["is_active"]
        values = [self.isActive]
        condition = "user_group_id='"+str(self.userGroupId)+"'"
        return DatabaseHandler.instance().update(self.tblName, columns, values, condition)

class User(CMObject) :
    mainTblName = "tbl_users"
    detailTblName = "tbl_user_details"

    def __init__(self, userId, emailId, userGroupId, employeeName, 
                employeeCode, contactNo, address, designation, 
                domainIds, isActive) :
        self.userId =  userId if userId != None else self.generateNewUserId()
        self.emailId =  emailId
        self.userGroupId =  userGroupId
        self.employeeName =  employeeName
        self.employeeCode =  employeeCode
        self.contactNo =  contactNo
        self.address =  address
        self.designation =  designation
        self.domainIds =  domainIds
        self.isActive = isActive if isActive != None else 1
        self.verify()

    def verify(self) :
        assertType(self.userId, IntType)
        assertType(self.emailId, StringType)
        assertType(self.userGroupId, IntType)
        assertType(self.employeeName, StringType)
        assertType(self.employeeCode, StringType)
        assertType(self.contactNo, StringType)
        assertType(self.address, StringType)
        assertType(self.designation, StringType)
        assertType(self.domainIds, ListType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        return {
            "user_id": userId,
            "email_id": emailId,
            "user_group_id": userGroupId,
            "employee_name": employeeName,
            "employee_code": employeeCode,
            "contact_no": contactNo,
            "address": address, 
            "designation": designation,
            "domain_ids": domainIds,
            "is_active": isActive
        }

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
                "' AND user_id != '"+str(self.contactNo)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.detailTblName, condition)

    def isIdInvalid(self):
        condition = "user_id = '"+str(self.userId)+"'"
        return not DatabaseHandler.instance().isAlreadyExists(self.mainTblName, condition)

    def getFormType(self) :
        rows = DatabaseHandler.instance().getData(UserGroup.tblName, 
                                            "form_type", 
                                            "user_group_id='"+str(self.userGroupId)+"'")
        return rows[0][0]

    def save(self):
        currentTimeStamp = getCurrentTimeStamp()
        mainTblColumns = "user_id, username, password, created_on, "+\
                            "created_by, updated_on, updated_by"
        mainTblValuesList = [   
                            self.userId, 
                            self.emailId, 
                            generatePassword(),
                            currentTimeStamp,1,
                            currentTimeStamp,1
                        ]
        detailTblcolumns = "user_id, email_id, user_group_id, form_type,employee_name, "+\
                  "employee_code, contact_no, address, designation, domain_ids,"+\
                  " created_on, created_by, updated_on, updated_by"
        detailTblValuesList = [
                            self.userId,
                            self.emailId,
                            self.userGroupId,
                            self.getFormType(),
                            self.employeeName,
                            self.employeeCode,
                            self.contactNo,
                            self.address,
                            self.designation,
                            ",".join(self.domainIds),
                            currentTimeStamp,1,
                            currentTimeStamp,1
                        ]

        mainTblValues = listToString(mainTblValuesList)
        detailTblValues = listToString(detailTblValuesList)

        if DatabaseHandler.instance().insert(self.mainTblName, mainTblColumns, mainTblValues): 
            return DatabaseHandler.instance().insert(self.detailTblName, 
                detailTblcolumns, detailTblValues)
        else : 
            return False

    def update(self):
        currentTimeStamp = getCurrentTimeStamp()
        detailTblcolumns = ["email_id", 
                            "user_group_id", 
                            "form_type",
                            "employee_name",
                            "employee_code", 
                            "contact_no", 
                            "address", 
                            "designation", 
                            "domain_ids",
                            "updated_on",
                            "updated_by"]
        detailTblValuesList = [
                            self.emailId,
                            self.userGroupId,
                            self.getFormType(),
                            self.employeeName,
                            self.employeeCode,
                            self.contactNo,
                            self.address,
                            self.designation,
                            convertToString(",".join(self.domainIds)),
                            currentTimeStamp,1 ]
        condition = "user_id='"+str(self.userId)+"'"
        return DatabaseHandler.instance().update(self.detailTblName, detailTblcolumns,
                                                detailTblValuesList, condition)
