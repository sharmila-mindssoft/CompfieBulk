from types import *
import json
import re
import os

from aparajitha.server.constants import ROOT_PATH
from aparajitha.server.databasehandler import DatabaseHandler 
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler 
from aparajitha.server.admin.models import User
from aparajitha.server.common import *

__all__ = [
    "GroupCompany",
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit",
    "SaveClientGroup",
    "SaveClient"
]
clientDatabaseMappingFilePath = os.path.join(ROOT_PATH, 
    "Src-client/files/desktop/common/clientdatabase/clientdatabasemapping.txt")

class GroupCompany(object):

    def __init__(self, clientId, groupName, inchargePersons, countryIds ,domainIds, logo, 
        contractFrom, contractTo, noOfUserLicence, fileSpace, isSmsSubscribed,
        dateConfigurations, username, isActive):
        self.clientId = clientId
        self.groupName = groupName
        self.inchargePersons = inchargePersons
        self.countryIds = countryIds
        self.domainIds = domainIds
        self.logo = logo
        self.contractFrom = contractFrom
        self.contractTo = contractTo
        self.noOfUserLicence = noOfUserLicence
        self.fileSpace = fileSpace
        self.isSmsSubscribed = isSmsSubscribed
        self.dateConfigurations = dateConfigurations
        self.username = username
        self.isActive = isActive

    def verify(self) :
        assertType(self.clientId, IntType)
        assertType(self.groupName, StringType)
        assertType(self.inchargePersons, ListType)
        assertType(self.countryIds, ListType)
        assertType(self.domainIds, ListType)
        assertType(self.logo, StringType)
        assertType(self.contractFrom, StringType)
        assertType(self.contractTo, StringType)
        assertType(self.noOfUserLicence, IntType)
        assertType(self.fileSpace, FloatType)
        assertType(self.isSmsSubscribed, IntType)
        assertType(self.dateConfigurations, ListType)
        assertType(self.username, StringType)
        assertType(self.isActive, IntType)

    def toDetailedStructure(self) :
        return {
            "client_id": self.clientId,
            "client_name": self.groupName,
            "incharge_persons": self.inchargePersons,
            "countries": self.countryIds,
            "domain_ids": self.domainIds,
            "logo" : self.logo,
            "contract_from": self.contractFrom,
            "contract_to": self.contractTo,
            "incharge_persons": self.inchargePersons,
            "no_of_user_licence": self.noOfUserLicence,
            "file_space": self.fileSpace,
            "is_sms_subscribed": self.isSmsSubscribed,
            "date_configurations": self.dateConfigurations,
            "username": self.username,
            "is_active": self.isActive
        }

    # def getDetailedStructure(self):


class BusinessGroup(object):

    def __init__(self, businessGroupId, businessGroupName):
        self.businessGroupId = businessGroupId
        self.businessGroupName = businessGroupName

    def verify(self) :
        assertType(self.businessGroupId, IntType)
        assertType(self.businessGroupName, StringType)

    def toStructure(self) :
        return {
            "business_group_id": self.businessGroupId,
            "business_group_name": self.businessGroupName
        }

class LegalEntity(object):

    def __init__(self, legalEntityId, legalEntityName, businessGroupId):
        self.legalEntityId = legalEntityId
        self.legalEntityName = legalEntityName
        self.businessGroupId = businessGroupId

    def verify(self) :
        assertType(self.legalEntityId, IntType)
        assertType(self.legalEntityName, StringType)
        assertType(self.businessGroupId, IntType)

    def toStructure(self) :
        return {
            "legal_entity_id": self.legalEntityId,
            "legal_entity_name": self.legalEntityName,
            "business_group_id": self.businessGroupId
        }

class Division(object):

    def __init__(self, divisionId, divisionName,legalEntityId, businessGroupId):
        self.divisionId = divisionId
        self.divisionName = divisionName
        self.legalEntityId = legalEntityId
        self.businessGroupId = businessGroupId

    def verify(self) :
        assertType(self.divisionId, IntType)
        assertType(self.divisionName, StringType)
        assertType(self.legalEntityId, IntType)
        assertType(self.businessGroupId, IntType)

    def toStructure(self) :
        return {
            "division_id": self.divisionID,
            "division_name": self.divisionName,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId
        }

class Unit(object):

    def __init__(self, unitId, divisionId, legalEntityId, businessGroupId, clientId, 
                countryId, geographyId, unitCode, unitName, industryId, address, 
                postalCode, domainIds, isActive):
        self.unitId = unitId
        self.divisionId = divisionId
        self.legalEntityId = legalEntityId
        self.businessGroupId = businessGroupId
        self.clientId = clientId
        self.countryId = countryId
        self.geographyId = geographyId
        self.unitCode = unitCode
        self.unitName = unitName
        self.industryId = industryId
        self.address = address
        self.postalCode = postalCode
        self.domainIds = domainIds
        self.isActive = isActive

    def verify(self) :
        assertType(self.unitId, IntType)
        assertType(self.divisionId, StringType)
        assertType(self.legalEntityId, IntType)
        assertType(self.businessGroupId, IntType)
        assertType(self.clientId, IntType)
        assertType(self.countryId, IntType)
        assertType(self.geographyId, IntType)
        assertType(self.unitCode, StringType)
        assertType(self.unitName, StringType)
        assertType(self.industryId, IntType)
        assertType(self.address, StringType)
        assertType(self.postalCode, StringType)
        assertType(self.domainIds, ListType)
        assertType(self.isActive, IntType)

    def toDetailedStructure(self) :
        return {
            "unit_id": unitId,
            "division_id": divisionId,
            "legal_entity_id": legalEntityId,
            "business_group_id": businessGroupId,
            "client_id"  : clientId,
            "country_id": countryId,
            "geography_id": geographyId,
            "unit_code": unitCode,
            "unit_name": unitName,
            "industry_id": industryId,
            "unit_address": address,
            "postal_code": postalCode,
            "domain_ids": domainIds,
            "is_active": isActive
        }

    def toStructure(self):
        return{
            "unit_id": unitId,
            "division_id": divisionId,
            "legal_entity_id": legalEntityId,
            "business_group_id": businessGroupId,
            "client_id"  : clientId,
            "unit_name": unitName,
            "unit_address": address
        }

class SaveClientGroup(object) :
    clientTblName = "tbl_client_groups"
    clientSettingsTblName = "tbl_client_settings"
    clietConfigurationTblName = "tbl_client_configurations"
    usersTblName = "tbl_users"
    countryTblName = "tbl_countries"
    domainTblName = "tbl_domains"
    clientDBName = ""

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = sessionUser
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def processRequest(self):
        print "Entered into process request"
        requestData = self.requestData
        print requestData
        self.groupName = JSONHelper.getString(requestData, "group_name")
        self.countryIds = JSONHelper.getList(requestData, "country_ids")
        self.domainIds = JSONHelper.getList(requestData, "domain_ids")
        self.logo = JSONHelper.getString(requestData, "logo")
        self.contractFrom = JSONHelper.getLong(requestData, "contract_from")
        self.contractTo = JSONHelper.getLong(requestData, "contract_to")
        self.inchargePersons = JSONHelper.getList(requestData, "incharge_persons")
        self.noOfLicence = JSONHelper.getInt(requestData, "no_of_user_licence")
        self.fileSpace = JSONHelper.getFloat(requestData, "file_space")
        self.isSmsSubscribed = JSONHelper.getInt(requestData, "is_sms_subscribed")
        self.username = JSONHelper.getString(requestData, "email_id")     
        self.dateConfigurations = JSONHelper.getList(requestData, "date_configurations")

        self.clientId = self.generateNewId()

        if self.isDuplicateGroupName():
            print "Duplicate grup name"
            self.response = "GroupNameAlreadyExists"
        elif self.saveGroupCompany():
            print "Saved group company" 
            if self.createClientDatabase():
                print "Saved client database"
                if self.saveClientDetails():
                    print "Saved client details"
                    if self.copyBasicData():
                        print "Copied Basic data"
                        if self.saveDateConfigurations():
                            print "Saved date configurations"
                            if self.saveCredentials():
                                print "Saved Credentials"
                                self.response = "SaveClientGroupSuccess"
                            else:
                                print "Save credentials failed"
                        else:
                            print "Saving date configurations Failed"
                    else:
                        print "Copying Data Failed"
                else:
                    print "Saving client settings failed"
            else:
                print "Creating client database failed"
        else:
            print "Save Group company failed"

        return commonResponseStructure(self.response,{})

    def generateNewId(self) :
        return DatabaseHandler.instance().generateNewId(self.clientTblName, "client_id")

    def isDuplicateGroupName(self):
        condition = "group_name ='"+self.groupName+\
                "' AND client_id != '"+str(self.clientId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.clientTblName, condition)

    def copyBasicData(self):
        if self.insertCountries() and self.insertDomains():
            return True
    
    def insertCountries(self):
        valuesList = []
        countryIdsStrVal = ",".join(str(x) for x in self.countryIds)
        condition = "country_id in ("+countryIdsStrVal+")"
        columns = "country_id, country_name, is_active"
        rows = DatabaseHandler.instance().getData(self.countryTblName, columns, condition)
        for row in rows:
            countryId = int(row[0])
            countryName = row[1]
            isActive = row[2]
            valuesTuple = (countryId, countryName, isActive)
            valuesList.append(valuesTuple)
        print valuesList
        return ClientDatabaseHandler.instance(self.getDatabaseName()).bulkInsert(self.countryTblName,columns,valuesList)

    def insertDomains(self):
        valuesList = []
        domainIdsStrVal = ",".join(str(x) for x in self.domainIds)
        condition = "domain_id in ("+domainIdsStrVal+")"
        columns = "domain_id, domain_name, is_active"
        rows = DatabaseHandler.instance().getData(self.domainTblName, columns, condition)
        for row in rows:
            domainId = int(row[0])
            doaminName = row[1]
            isActive = row[2]
            valuesTuple = (domainId, doaminName, isActive)
            valuesList.append(valuesTuple)
        print valuesList
        return ClientDatabaseHandler.instance(self.getDatabaseName()).bulkInsert(self.domainTblName,columns,valuesList)

    def saveGroupCompany(self):
        columns = "client_id, group_name, incharge_persons,created_on, created_by, updated_on, updated_by"
        valuesList =  [self.clientId, self.groupName, ",".join(str(x) for x in self.inchargePersons),
                        getCurrentTimeStamp(), self.sessionUser,
                        getCurrentTimeStamp(), self.sessionUser]
        values = listToString(valuesList)

        userColumns = "client_ids"
        userValues = str(self.clientId)
        for inchargePerson in self.inchargePersons:
            condition = " user_id='"+inchargePerson+"'"
            DatabaseHandler.instance().append(self.userTblName,userColumns, userValues, condition)

        return DatabaseHandler.instance().insert(self.clientTblName,columns,values)

    # def updateGroupCompany(self, clientId, groupName):
    #     columns = ["group_name", "updated_on", "updated_by"]
    #     values =  [ groupName, getCurrentTimeStamp(), self.sessionUser]
    #     condition = "client_id='%s'",clientId
    #     return DatabaseHandler.instance().update(self.clientTblName, columns, values, condition)

    def saveClientDatabaseMapping(self, clientId, databaseName):
        clientDatabaseMappingJson = json.load(open(clientDatabaseMappingFilePath))
        clientDatabaseMappingJson[clientId] = databaseName
        json.dump(clientDatabaseMappingJson, 
            open(clientDatabaseMappingFilePath,'w'))

    def createClientDatabase(self):
        isComplete = False
        self.groupName = re.sub('[^a-zA-Z0-9 \n\.]', '', self.groupName)
        self.groupName = self.groupName.replace (" ", "")
        databaseName = "mirror_"+self.groupName+"_"+str(self.clientId)
        if DatabaseHandler.instance().createDatabase(databaseName):
            ClientDatabaseHandler.instance(databaseName).createClientDatabaseTables()
            self.saveClientDatabaseMapping(self.clientId, databaseName)
            isComplete = True
        return isComplete

    def getDatabaseName(self):
        if self.clientDBName == None:
            self.clientDBName = self.getClientDatabase(self.clientId)
        return self.clientDBName

    def saveClientDetails(self):
        columns = "country_ids ,domain_ids, logo_url, contract_from, contract_to,"+\
                  "no_of_user_licence,total_disk_space, is_sms_subscribed,"+\
                  "  updated_on, updated_by"
        valuesList =  [ ",".join(str(x) for x in self.countryIds),
                         ",".join(str(x) for x in self.countryIds),
                        self.logo, self.contractFrom, self.contractTo, self.noOfLicence, 
                        self.fileSpace, self.isSmsSubscribed, getCurrentTimeStamp(), 
                        self.sessionUser]
        values = listToString(valuesList)
        return ClientDatabaseHandler.instance(self.getDatabaseName()).insert(self.clientSettingsTblName,columns,values)

    def saveDateConfigurations(self):
        valuesList = []
        columns = "country_id ,domain_id, period_from, period_to, updated_on, updated_by"
        for configuration in self.dateConfigurations:
            assertType(configuration, DictType)
            countryId = JSONHelper.getInt(configuration, "country_id")
            domainId = JSONHelper.getInt(configuration, "domain_id")
            peroidFrom = JSONHelper.getInt(configuration, "period_from")
            perodTo = JSONHelper.getInt(configuration, "period_to")
            valuesTuple = (countryId, domainId, peroidFrom, perodTo, 
                getCurrentTimeStamp(), int(self.sessionUser))
            valuesList.append(valuesTuple)

        return ClientDatabaseHandler.instance(self.getDatabaseName()).bulkInsert(self.clietConfigurationTblName,columns,valuesList)

    def saveCredentials(self):
        password = generatePassword()
        user = User(None, self.username, None, self.groupName+" Admin", "",
            None, " ", "Admin", self.countryIds,self.domainIds, None)

        if user.isDuplicateEmail():
            self.response = "UsernameAlreadyExists"
        elif user.saveAdmin(self.sessionUser):
            return True
        else:
            return False

class GetClientGroup(object):

    def __init__(self):
        domainList = DomainList.getDomainList()
        countryList = CountryList.getCountryList()
        userList = User.getList()
        # clientList = 

        response_data = {}
        response_data["domains"] = domainList
        response_data["countries"] = countryList
        response_data["users"] = userList
        response_data["client_list"] = clientList



class SaveClient(object):
    businessGroupTblName = "tbl_business_groups"
    legalEntityTblName = "tbl_legal_entities"
    divisionTblName = "tbl_divisions"
    unitTblName = "tbl_units"

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = sessionUser

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)
        self.processRequest()

    def processRequest(self):
        requestData = self.requestData
        businessGroup = JSONHelper.getDict(requestData, "business_group")
        legalEntity = JSONHelper.getDict(requestData, "legal_entity")
        division = JSONHelper.getDict(requestData, "division")
        countryWiseUnits = JSONHelper.getList(requestData, "country_wise_units")

        assertType(businessGroup, DictType)
        assertType(legalEntity, DictType)
        assertType(division, DictType)
        assertType(countryWiseUnits, ListType)

        self.businessGroupId = self.processBusinessGroup(businessGroup)
        self.legalEntityId = self.processLegalEntity(legalEntity)
        self.divisionId = self.processDivision(division)

    def generateNewId(self, idType) :
        if idType == "businessGroup":
            return DatabaseHandler.instance().generateNewId(
                self.businessGroupTblName, "business_group_id")
        elif idType == "legalEntity":
            return DatabaseHandler.instance().generateNewId(
                self.legalEntityTblName, "legal_entity_id")
        elif idType == "division":
            return DatabaseHandler.instance().generateNewId(
                self.divisionTblName, "division_id")
        elif idType == "unit":
            return DatabaseHandler.instance().generateNewId(
                self.unitTblName, "unit_id")

    def processBusinessGroup(self, businessGroup):
        businessGroupId = JSONHelper.getInt(businessGroup, "business_group_id")
        businessGroupName = JSONHelper.getString(businessGroup, "business_group_name")

        assertType(businessGroupName, StringType)

        if(businessGroupId == 0):
            businessGroupId = self.generateNewId("businessGroup")
        if self.saveBusinessGroup(businessGroupId, businessGroupName):
            return businessGroupId

    def saveBusinessGroup(self, businessGroupId, businessGroupName):
        columns = "business_group_id, business_group_name, created_on, created_by,"+\
                "updated_on, updated_by"
        valuesList =  [businessGroupId, businessGroupName, getCurrentTimeStamp(), 
                        self.sessionUser, getCurrentTimeStamp(), self.sessionUser]
        values = listToString(valuesList)
        return ClientDatabaseHandler.instance(getDatabaseName()).insert(self.businessGroupTblName,columns,values)

    def processLegalEntity(self, legalEntity):
        legalEntityId = JSONHelper.getInt(legalEntity, "legal_entity_id")
        legalEntityName = JSONHelper.getString(legalEntity, "legal_entity_name")

        assertType(legalEntityName, StringType)

        if(legalEntityId == 0):
            legalEntityId = self.generateNewId("legalEntity")
        if self.saveLegalEntity(legalEntityId, legalEntityName):
            return legalEntityId

    def saveLegalEntity(self, legalEntityId, legalEntityName):
        columns = "legal_entity_id, legal_entity_name, business_group_id,"+\
                  "created_on, created_by, updated_on, updated_by"
        valuesList =  [legalEntityId, legalEntityName, self.businessGroupId, 
                        getCurrentTimeStamp(), self.sessionUser, 
                        getCurrentTimeStamp(), self.sessionUser]
        values = listToString(valuesList)
        return ClientDatabaseHandler.instance(getDatabaseName()).insert(self.legalEntityTblName,columns,values)

    def processDivision(self, division):
        divisionId = JSONHelper.getInt(legalEntity, "division_id")
        divisionName = JSONHelper.getString(legalEntity, "division_name")

        assertType(divisionName, StringType)

        if(divisionId == 0):
            divisionId = self.generateNewId("division")
        if self.saveDivision(divisionId, divisionName):
            return divisionId

    def saveDivision(self, divisionId, divisionName):
        columns = "division_id, division_name, legal_entity_id, business_group_id,"+\
                  "created_on, created_by, updated_on, updated_by"
        valuesList =  [divisionId, divisionName, self.legalEntityId, 
                        self.businessGroupId, getCurrentTimeStamp(), self.sessionUser, 
                        getCurrentTimeStamp(), self.sessionUser]
        values = listToString(valuesList)
        return ClientDatabaseHandler.instance(getDatabaseName()).insert(self.divisionTblName,columns,values)