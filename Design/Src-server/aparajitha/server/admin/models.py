from types import *
from databasehandler import DatabaseHandler 
import json
import datetime
import time


__all__ = [
    "CMObject", "UserGroup",
]

def assertType (x, typeObject) :
    if type(x) is not typeObject :
        msg = "expected type %s, received invalid type  %s " % (typeObject, type(x))
        raise TypeError(msg)

def listToString(list_value):
    print "Entering into list to string"
    string_value = ""
    for index,value in enumerate(list_value):
        if(index < len(list_value)-1):
            string_value = string_value+"'"+str(value)+"',"
        else:
            string_value = string_value+"'"+str(value)+"'"

    return string_value

def getCurrentTimeStamp() :
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

class CMObject(object) :
    def toJSON(self) :
        data = self.toStructure()
        return json.dumps(data)
    @classmethod
    def fromJSON(klass, jsonData) :
        data = json.loads(jsonData)
        return klass.fromStructure(data)

class UserGroup(CMObject) :
    tblUserGroup = "tbl_user_groups"

    def __init__(self, userGroupId, userGroupName, formType, formIds, isActive) :
        self.userGroupId =  userGroupId if userGroupId != None else self.generateNewUserGroupId()
        self.userGroupName = userGroupName
        self.formType = formType
        self.formIds = formIds
        self.isActive = isActive if isActive != None else 1
        self.verify()

    def verify(self) :
        assertType(self.userGroupId, IntType)
        print "Crossed verifying group id"
        assertType(self.userGroupName, StringType)
        print "Crossed verifying group name"
        assertType(self.formType, StringType)
        print "Crossed verifying form type"
        assertType(self.formIds, ListType)
        print "Crossed verifying form ids"
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
        return DatabaseHandler.instance().generateNewId(tblUserGroup, "user_group_id")

    def isDuplicate(self):
        return DatabaseHandler.instance().isAlreadyExists(tblUserGroup, "user_group_id", 
            "user_group_name", self.userGroupId, self.userGroupName)

    def save(self):
        columns = "user_group_id, user_group_name,form_type, "+\
                  "form_ids, is_active, created_on, created_by, "+\
                  "updated_on, updated_by"
        values = listToString(  [self.userGroupId, 
                                self.userGroupName, 
                                self.formType, 
                                self.formIds, 
                                self.isActive,
                                getCurrentTimeStamp(),1,
                                getCurrentTimeStamp(),1])
        return DatabaseHandler.instance().insert(tblUserGroup,columns,values)

