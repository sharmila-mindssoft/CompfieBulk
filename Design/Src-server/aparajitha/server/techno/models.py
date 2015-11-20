from types import *
import json
import re

from aparajitha.server.databasehandler import DatabaseHandler 
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler 
from aparajitha.server.common import *
from aparajitha.server.clientdatabasemapping import clientDatabaseMapping

__all__ = [
    "GroupCompany",
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit",
    "SaveClient"
]

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

class SaveClient(object) :
    clientTblName = "tbl_client_groups"
    businessGroupTblName = "tbl_business_groups"
    legalEntityTblName = "tbl_legal_entities"
    divisionTblName = "tbl_divisions"
    unitTblName = "tbl_units"
    clientDBName = ""

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = sessionUser

        assertType(requestData, DictType)
        print "validated request data"
        assertType(sessionUser, LongType)
        print "validated session user"
        self.processRequest()

    def processRequest(self):
        print "inside process request"
        requestData = self.requestData
        groupCompany = JSONHelper.getDict(requestData, "group_company")
        businessGroup = JSONHelper.getDict(requestData, "business_group")
        legalEntity = JSONHelper.getDict(requestData, "legal_entity")
        division = JSONHelper.getDict(requestData, "division")
        logo = JSONHelper.getString(requestData, "logo")
        domainIds = JSONHelper.getList(requestData, "domain_ids")
        username = JSONHelper.getString(requestData, "username")
        noOfLicence = JSONHelper.getInt(requestData, "no_of_licence")
        contractFrom = JSONHelper.getString(requestData, "contract_from")
        contractTo = JSONHelper.getString(requestData, "contract_to")
        totalDiskSpace = JSONHelper.getFloat(requestData, "total_disk_space")
        isSmsSubscribed = JSONHelper.getInt(requestData, "is_sms_subscribed")
        countryWiseUnits = JSONHelper.getList(requestData, "country_wise_units")

        assertType(groupCompany, DictType)
        print "validated group company"
        assertType(businessGroup, DictType)
        assertType(legalEntity, DictType)
        assertType(division, DictType)
        assertType(logo, StringType)
        assertType(domainIds, ListType)
        assertType(username, StringType)
        assertType(noOfLicence, IntType)
        assertType(contractFrom, StringType)
        assertType(contractTo, StringType)
        assertType(totalDiskSpace, FloatType)
        assertType(isSmsSubscribed, IntType)
        assertType(countryWiseUnits, ListType)


        self.processGroupCompany(groupCompany)

    def generateNewId(self, idType) :
        if idType == "client":
            return DatabaseHandler.instance().generateNewId(self.clientTblName, "client_id")
        elif idType == "businessGroup":
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

    def processGroupCompany(self, groupCompany):
        clientId = JSONHelper.getInt(groupCompany, "client_id")
        groupName = JSONHelper.getString(groupCompany, "group_name")

        assertType(groupName, StringType)
        print "client ID: %s",clientId
        if(clientId == 0):
            clientId = self.generateNewId("client")
            print clientId
            if self.saveGroupCompany(clientId, groupName):
                print "GroupCompany saved"
                self.createClientDatabase(clientId, groupName)
        else:
            print clientId
            self.updateGroupCompany(clientId, groupName)

    def saveGroupCompany(self, clientId, groupName):
        columns = "client_id, group_name, created_on, created_by, updated_on, updated_by"
        valuesList =  [clientId, groupName, getCurrentTimeStamp(), self.sessionUser,
                        getCurrentTimeStamp(), self.sessionUser]
        values = listToString(valuesList)
        return DatabaseHandler.instance().insert(self.clientTblName,columns,values)

    def updateGroupCompany(self, clientId, groupName):
        print "Group company updated"
        columns = ["group_name", "updated_on", "updated_by"]
        values =  [ groupName, getCurrentTimeStamp(), self.sessionUser]
        condition = "client_id='%s'",clientId
        return DatabaseHandler.instance().update(self.clientTblName, columns, values, condition)

    def createClientDatabase(self, clientId, groupName):
        print "client database created"
        isComplete = False
        databaseName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(clientId)+groupName)
        databaseName = databaseName.replace (" ", "")
        if DatabaseHandler.instance().createDatabase(databaseName):
            clientDatabaseMapping[clientId] = databaseName
            ClientDatabaseHandler.instance(databaseName).createClientDatabaseTables()
            isComplete = True
        return isComplete
