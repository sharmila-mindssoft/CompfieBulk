from types import *
import json
import re
import os

from aparajitha.server.constants import ROOT_PATH
from aparajitha.server.databasehandler import DatabaseHandler 
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler 
from aparajitha.server.common import *

__all__ = [
    "GroupCompany",
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit",
    "SaveClient"
]
clientDatabaseMappingFilePath = os.path.join(ROOT_PATH, 
    "Src-client/files/desktop/common/clientdatabase/clientdatabasemapping.txt")

class GroupCompany(object):

    def __init__(self, clientId, groupName, domainIds, logo, contractFrom, contractTo,
        noOfUserLicence, totalDiskSpace, isSmsSubscribed):
        self.clientId = clientId
        self.groupName = groupName
        self.domainIds = domainIds
        self.logo = logo
        self.contractFrom = contractFrom
        self.contractTo = contractTo
        self.noOfUserLicence = noOfUserLicence
        self.totalDiskSpace = totalDiskSpace
        self.isSmsSubscribed = isSmsSubscribed

    def verify(self) :
        assertType(self.clientId, IntType)
        assertType(self.groupName, StringType)
        assertType(self.domainIds, ListType)
        assertType(self.logo, StringType)
        assertType(self.contractFrom, StringType)
        assertType(self.contractTo, StringType)
        assertType(self.noOfUserLicence, IntType)
        assertType(self.totalDiskSpace, FloatType)
        assertType(self.isSmsSubscribed, IntType)

    def toStructure(self) :
        return {
            "client_id": clientId,
            "group_company_name": groupName,
            "domains": domainIds,
            "logo": logo,
            "contract_from": contractFrom,
            "contract_to": contractTo,
            "no_of_user_licence": noOfUserLicence,
            "total_disk_space": totalDiskSpace,
            "is_sms_subscribed": isSmsSubscribed
        }

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
    clientDBName = ""

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = sessionUser

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)
        self.processRequest()

    def processRequest(self):
        requestData = self.requestData
        self.groupName = JSONHelper.getString(requestData, "group_name")
        self.countryIds = JSONHelper.getList(requestData, "country_ids")
        self.domainIds = JSONHelper.getList(requestData, "domain_ids")
        self.logo = JSONHelper.getString(requestData, "logo")
        self.contractFrom = JSONHelper.getString(requestData, "contract_from")
        self.contractTo = JSONHelper.getString(requestData, "contract_to")
        self.inchargePersons = JSONHelper.getList(requestData, "incharge_persons")
        self.noOfLicence = JSONHelper.getInt(requestData, "no_of_licence")
        self.fileSpace = JSONHelper.getFloat(requestData, "file_space")
        self.isSmsSubscribed = JSONHelper.getInt(requestData, "is_sms_subscribed")
        self.username = JSONHelper.getString(requestData, "email_id")     
        self.dateConfigurations = JSONHelper.getString(requestData, "date_configurations")

        assertType(groupName, StringType)
        assertType(countryIds, ListType)
        assertType(domainIds, ListType)
        assertType(logo, StringType)
        assertType(contractFrom, StringType)
        assertType(contractTo, StringType)
        assertType(inchargePersons, ListType)
        assertType(noOfLicence, IntType)
        assertType(fileSpace, FloatType)
        assertType(isSmsSubscribed, IntType)
        assertType(username, StringType)
        assertType(dateConfigurations, ListType)

        self.clientId = self.generateNewId("client")

        if self.saveGroupCompany():
            self.createClientDatabase(clientId, groupName)
            self.saveClientDetails()
            self.saveDateConfigurations()
            self.saveCredentials()

    def generateNewId(self) :
        return DatabaseHandler.instance().generateNewId(self.clientTblName, "client_id")

    def saveGroupCompany(self):
        columns = "client_id, group_name, created_on, created_by, updated_on, updated_by"
        valuesList =  [self.clientId, self.groupName, getCurrentTimeStamp(), self.sessionUser,
                        getCurrentTimeStamp(), self.sessionUser]
        values = listToString(valuesList)
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
        databaseName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(self.clientId)+self.groupName)
        databaseName = databaseName.replace (" ", "")
        if DatabaseHandler.instance().createDatabase(databaseName):
            ClientDatabaseHandler.instance(databaseName).createClientDatabaseTables()
            self.saveClientDatabaseMapping(self.clientId, databaseName)
            isComplete = True
        return isComplete

    def getDatabaseName(self):
        if clientDBName == None:
            clientDBName = getClientDatabase(self.clientId)
        return clientDBName

    def saveClientDetails(self):
        columns = "country_ids ,domain_ids, logo, contract_from, contract_to,"+\
                  "no_of_user_licence,total_disk_space, is_sms_subscribed"+\
                  "created_on, created_by, updated_on, updated_by"
        valuesList =  [ self.countryIds, self.domainIds, self.logo, self.contractFrom, 
                        self.contractTo, self.noOfLicence, self.totalDiskSpace, 
                        self.isSmsSubscribed, getCurrentTimeStamp(), self.sessionUser, 
                        getCurrentTimeStamp(), self.sessionUser]
        values = listToString(valuesList)
        return ClientDatabaseHandler.instance(getDatabaseName()).insert(self.clientSettingsTblName,columns,values)

    def saveDateConfigurations():
        for configuration in self.dateConfigurations:
            assertType(configuration, DictType)


    def saveCredentials():
        userName = self.userName
        password = generatePassword()
        print "inside save credentials %s", password

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