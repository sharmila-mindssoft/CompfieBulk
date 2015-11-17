from types import *
from databasehandler import DatabaseHandler 
import json
from aparajitha.server.common import *

__all__ = [
    "UserGroup",
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
        values_list =  [self.userGroupId, self.userGroupName, 
                        self.formType, ",".join(self.formIds),
                        self.isActive, getCurrentTimeStamp(),1,
                        getCurrentTimeStamp(),1]
        values = listToString(values_list)
        return DatabaseHandler.instance().insert(self.tblName,columns,values)

    def update(self):
        columns = ["user_group_name","form_type",
                  "form_ids", "updated_on", "updated_by"]
        values =  [ self.userGroupName, 
                    self.formType, convertToString(",".join(self.formIds)),
                    getCurrentTimeStamp(),1]
        condition = "user_group_id='"+str(self.userGroupId)+"'"
        return DatabaseHandler.instance().update(self.tblName, columns, values, condition)

    def updateStatus(self):
        columns = ["is_active"]
        values = [self.isActive]
        condition = "user_group_id='"+str(self.userGroupId)+"'"
        return DatabaseHandler.instance().update(self.tblName, columns, values, condition)
