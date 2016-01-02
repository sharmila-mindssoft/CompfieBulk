from types import *
import json
import re
import os

from aparajitha.server.constants import ROOT_PATH
from aparajitha.server.databasehandler import DatabaseHandler
from aparajitha.server.admin.controllers import User
from aparajitha.server.knowledge.models import DomainList, CountryList, GeographyLevelList
from aparajitha.server.knowledge.models import IndustryList, Geography, GeographyAPI
from aparajitha.server.common import *

__all__ = [
    "GroupCompany",
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit",
    "ClientGroup",
    "ClientController",
    "ClientProfile"
]
clientDatabaseMappingFilePath = os.path.join(ROOT_PATH, 
    "Src-client/files/desktop/common/clientdatabase/clientdatabasemapping.txt")

class GroupCompany(object):
    db = None
    clientId = None
    groupName = None
    inchargePersons = None
    countryIds = None
    domainIds = None
    logo = None
    contractFrom = None
    contractTo = None
    noOfUserLicence = None
    fileSpace = None
    isSmsSubscribed = None
    dateConfigurations = None
    username = None
    isActive = None

    def __init__(self, db):
        self.db = db if db != None else DatabaseHandler.instance()

    def toDetailedStructure(self) :
        return {
            "client_id": self.clientId,
            "client_name": self.groupName,
            "incharge_persons": self.inchargePersons,
            "country_ids": self.countryIds,
            "domain_ids": self.domainIds,
            "logo" : self.logo,
            "contract_from": self.contractFrom,
            "contract_to": self.contractTo,
            "no_of_user_licence": self.noOfUserLicence,
            "file_space": self.fileSpace,
            "is_sms_subscribed": self.isSmsSubscribed,
            "date_configurations": self.dateConfigurations,
            "username": self.username,
            "is_active": self.isActive
        }

    def toStructure(self):
        return {
            "client_id": self.clientId,
            "group_name": self.groupName,
            "country_ids": self.countryIds,
            "domain_ids": self.domainIds,
            "is_active": self.isActive
        }

    def getGroupCompanyDetails(self, sessionUser = None, clientIds = None):
        clientRows = None
        if sessionUser != None:
            clientRows = self.db.getClientIds(sessionUser)
            clientIds = clientRows[0][0]
        elif clientIds == None:
            clientRows = self.db.getAllClientIds()
            clientIds = clientRows[0][0]
        clientRows = self.db.getGroupCompanyDetails(clientIds)
        clientList = []
        for row in clientRows:
            self.clientId = row[0]
            self.groupName = row[1]
            self.username = row[2]
            self.logo = row[3]
            self.contractFrom = datetimeToString(row[4])
            self.contractTo = datetimeToString(row[5])
            self.noOfUserLicence = row[6]
            self.fileSpace = row[7]
            self.isSmsSubscribed = row[8]
            self.inchargePersons = row[9]
            self.isActive = row[10]
            self.countryIds = [int(x) for x in self.db.getClientCountries(self.clientId).split(",")]
            self.domainIds = [int(x) for x in self.db.getClientDomains(self.clientId).split(",")]
            self.dateConfigurations = ClientConfiguration(
                self.clientId, self.db).getClientConfigurations()
            clientList.append(self.toDetailedStructure())
        return clientList

    def getGroupCompanies(self, sessionUser = None, clientIds = None):
        clientRows = None
        if sessionUser != None:
            clientRows = self.db.getClientIds(sessionUser)
            clientIds = clientRows[0][0]
        elif clientIds == None:
            clientRows = self.db.getAllClientIds()
            clientIds = clientRows[0][0]
        clientRows = self.db.getGroupCompanies(clientIds)
        clientList = []
        for row in clientRows:
            self.clientId = row[0]
            self.groupName = row[1]
            self.isActive = row[2]
            self.countryIds = [int(x) for x in self.db.getClientCountries(self.clientId).split(",")]
            self.domainIds = [int(x) for x in self.db.getClientDomains(self.clientId).split(",")]
            clientList.append(self.toStructure())
        return clientList

class ClientConfiguration(object):
    db = None
    clientId = None
    countryId = None
    domainId = None
    periodFrom = None
    periodTo = None
    def __init__(self, clientId, db):
        self.db = db if db != None else DatabaseHandler.instance()
        self.clientId = clientId

    def toStructure(self):
        return {
            "country_id": self.countryId,
            "domain_id": self.domainId,
            "period_from": self.periodFrom,
            "period_to": self.periodTo
        }

    def getClientConfigurations(self):
        configurationsList = []
        configRows = self.db.getClientConfigurations(self.clientId)
        for row in configRows:
            self.countryId = row[0]
            self.domainId = row[1]
            self.periodFrom = row[2]
            self.periodTo = row[3]
            configurationsList.append(self.toStructure())
        return configurationsList

class BusinessGroup(object):
    db = None
    businessGroupId = None
    businessGroupName = None
    clientId = None
    def __init__(self, clientId, db):
        self.db = db if db != None else DatabaseHandler.instance()
        self.clientId = clientId

    def toStructure(self) :
        return {
            "business_group_id": self.businessGroupId,
            "business_group_name": self.businessGroupName,
            "client_id": self.clientId
        }

    def getBusinessGroups(self):
        businessGroupList = []
        rows = self.db.getBusinessGroups(self.clientId)
        for row in rows:
            self.businessGroupId = row[0]
            self.businessGroupName = row[1]
            businessGroupList.append(self.toStructure())
        return businessGroupList

    def getBusinessGroupById(self, businessGroupIds):
        businessGroupList = []
        rows = self.db.getUserBusinessGroups(businessGroupIds)
        for row in rows:
            self.businessGroupId = row[0]
            self.businessGroupName = row[1]
            businessGroupList.append(self.toStructure())
        return businessGroupList

class LegalEntity(object):
    db = None
    legalEntityId = None
    legalEntityName = None
    businessGroupId = None
    clientId = None

    def __init__(self, clientId, db):
        self.db = db if db != None else DatabaseHandler.instance()
        self.clientId = clientId

    def toStructure(self) :
        return {
            "legal_entity_id": self.legalEntityId,
            "legal_entity_name": self.legalEntityName,
            "business_group_id": self.businessGroupId,
            "client_id": self.clientId
        }

    def getLegalEntities(self):
        legalEntitiesList = []
        rows = self.db.getLegalEntities(self.clientId)
        for row in rows:
            self.businessGroupId = row[2]
            self.legalEntityName = row[1]
            self.legalEntityId = row[0]
            legalEntitiesList.append(self.toStructure())
        return legalEntitiesList

    def getLegalEntitiesById(self, legalEntityIds):
        legalEntitiesList = []
        rows = self.db.getUserLegalEntities(legalEntityIds)
        for row in rows:
            self.businessGroupId = row[2]
            self.legalEntityName = row[1]
            self.legalEntityId = row[0]
            legalEntitiesList.append(self.toStructure())
        return legalEntitiesList

class Division(object):
    db = None
    legalEntityId = None
    divisionId = None
    divisionName = None
    businessGroupId = None
    clientId = None

    def __init__(self, clientId, db):
        self.db = db if db != None else DatabaseHandler.instance()
        self.clientId = clientId

    def toStructure(self) :
        return {
            "division_id": self.divisionId,
            "division_name": self.divisionName,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId,
            "client_id": self.clientId
        }

    def getDivisions(self):
        divisionsList = []
        rows = self.db.getDivisions(self.clientId)
        for row in rows:
            self.divisionId = row[0]
            self.divisionName = row[1]
            self.legalEntityId = row[2]
            self.businessGroupId = row[3]
            divisionsList.append(self.toStructure())
        return divisionsList

    def getDivisionsById(self, divisionIds):
        divisionsList = []
        rows = self.db.getUserDivisions(divisionIds)
        for row in rows:
            self.divisionId = row[0]
            self.divisionName = row[1]
            self.legalEntityId = row[2]
            self.businessGroupId = row[3]
            divisionsList.append(self.toStructure())
        return divisionsList        

class Unit(object):
    db = None
    unitId = None
    divisionId = None
    legalEntityId = None
    businessGroupId = None
    clientId = None
    countryId = None
    geographyId = None
    unitCode = None
    unitName = None
    industryId = None
    address = None
    postalCode = None
    domainIds = None
    isActive = None
    industryName = None
    geography = None

    def __init__(self, clientId, db):
        self.clientId = clientId
        self.db = db if db != None else DatabaseHandler.instance()

    def toDetailedStructure(self) :
        return {
            "unit_id": self.unitId,
            "division_id": self.divisionId,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId,
            "client_id"  : self.clientId,
            "country_id": self.countryId,
            "geography_id": self.geographyId,
            "unit_code": self.unitCode,
            "unit_name": self.unitName,
            "industry_id": self.industryId,
            "unit_address": self.address,
            "postal_code": self.postalCode,
            "domain_ids": self.domainIds,
            "is_active": self.isActive
        }

    def toStructure(self):
        unitName = "%s - %s" % (self.unitCode, self.unitName)
        return{
            "unit_id": self.unitId,
            "division_id": self.divisionId,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId,
            "client_id": self.clientId,
            "unit_code":self.unitCode,
            "unit_name": self.unitName,
            "unit_address": self.address,
            "is_active": self.isActive
        }

    def getUnitDetails(self):
        unitList = []
        rows = self.db.getUnitDetails(self.clientId)
        for row in rows:
            self.unitId = row[0]
            self.divisionId = row[1]
            self.legalEntityId = row[2]
            self.businessGroupId = row[3]
            self.unitCode = row[4]
            self.unitName = row[5]
            self.countryId = row[6]
            self.address = row[7]
            self.postalCode = row[8]
            self.domainIds = row[9]
            self.industryId = row[10]
            self.geographyId = row[11]
            self.isActive = row[12]
            unitList.append(self.toDetailedStructure())
        return unitList

    def getUnits(self):
        unitList = []
        rows = self.db.getUnits(self.clientId)
        for row in rows:
            self.unitId = row[0]
            self.divisionId = row[1]
            self.legalEntityId = row[2]
            self.businessGroupId = row[3]
            self.unitCode = row[4]
            self.unitName = row[5]
            self.address = row[6]
            self.isActive = row[7]
            unitList.append(self.toStructure())
        return unitList

    def getUnitsById(self, unitIds):
        unitList = []
        rows = self.db.getUserUnits(unitIds)
        for row in rows:
            self.unitId = row[0]
            self.divisionId = row[1]
            self.legalEntityId = row[2]
            self.businessGroupId = row[3]
            self.unitCode = row[4]
            self.unitName = row[5]
            self.address = row[6]
            self.isActive = row[7]
            unitList.append(self.toStructure())
        return unitList

    def getUnitListForClosure(self, clientId):
        unitList = []
        rows = self.db.getUnitClosureList()
        for row in rows:
            unitStructure = {}
            unitStructure["unit_id"] = row[0]
            unitStructure["unit_name"] = "%s - %s" % (row[2], row[1])
            unitStructure["division_name"] = row[3]
            unitStructure["legal_entity_name"] = row[4]
            unitStructure["business_group_name"] = row[5]
            unitStructure["address"] = row[6]
            unitStructure["is_active"] = row[7]
            unitList.append(unitStructure)
        return unitList

class ClientGroup(object) :

    def __init__(self):
        self.db = DatabaseHandler.instance()

    def getClientGroups(self):
        responseData = {}
        domainList = DomainList.getDomainList()
        countryList = CountryList.getCountryList()
        userList = User().getList()
        clientList = GroupCompany(self.db).getGroupCompanyDetails()

        responseData["domains"] = domainList
        responseData["countries"] = countryList
        responseData["users"] = userList
        responseData["client_list"] = clientList
        return commonResponseStructure("GetClientGroupsSuccess",responseData)

    def generateNewClientId(self) :
        return self.db.generateNewId(self.db.tblClientGroups, "client_id")

    def isIdInvalid(self):
        condition = "client_id = '%d'" % self.clientId
        return not self.db.isAlreadyExists(self.db.tblClientGroups, condition)

    def isDuplicateGroupName(self):
        condition = "group_name ='%s' AND client_id != '%d'" % (self.groupName, self.clientId)
        return self.db.isAlreadyExists(self.db.tblClientGroups, condition)   

    def isDuplicateUsername(self):
        condition = "email_id ='%s' AND client_id != '%d'" % (self.username, self.clientId)
        return self.db.isAlreadyExists(self.db.tblClientGroups, condition)           

    def saveClientGroup(self, requestData, sessionUser):
        self.sessionUser = int(sessionUser)
        self.response = ""
        self.groupName = JSONHelper.getString(requestData, "group_name")
        self.countryIds = JSONHelper.getList(requestData, "country_ids")
        self.domainIds = JSONHelper.getList(requestData, "domain_ids")
        self.logo = JSONHelper.getString(requestData, "logo")
        self.contractFrom = JSONHelper.getString(requestData, "contract_from")
        self.contractTo = JSONHelper.getString(requestData, "contract_to")
        self.inchargePersons = JSONHelper.getList(requestData, "incharge_persons")
        self.noOfLicence = JSONHelper.getInt(requestData, "no_of_user_licence")
        self.fileSpace = JSONHelper.getInt(requestData, "file_space") * 1000000000
        self.isSmsSubscribed = JSONHelper.getInt(requestData, "is_sms_subscribed")
        self.username = JSONHelper.getString(requestData, "email_id")     
        self.shortName = JSONHelper.getString(requestData, "short_name")     
        self.dateConfigurations = JSONHelper.getList(requestData, "date_configurations")
        self.contractFrom = stringToDatetime(self.contractFrom)
        self.contractTo = stringToDatetime(self.contractTo)
        self.clientId = self.generateNewClientId()
        if self.isDuplicateGroupName():
            self.response = "GroupNameAlreadyExists"
        elif self.isDuplicateUsername():
            self.response = "EmailIdAlreadyExists"
        else:
            self.db.saveClientGroup(self, sessionUser)
            self.db.saveDateConfigurations(self.clientId, self.dateConfigurations, sessionUser)
            self.db.saveClientCountries(self.clientId, self.countryIds)
            self.db.saveClientDomains(self.clientId, self.domainIds)
            self.db.createAndSaveClientDatabase(self.groupName, self.clientId, self.shortName, self.username)
            self.db.saveInchargePersons(self)
            self.response = "SaveClientGroupSuccess"
        return commonResponseStructure(self.response,{})

    def updateClientGroup(self, requestData, sessionUser):
        self.sessionUser = int(sessionUser)
        self.response = ""
        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.groupName = JSONHelper.getString(requestData, "group_name")
        self.countryIds = JSONHelper.getList(requestData, "country_ids")
        self.domainIds = JSONHelper.getList(requestData, "domain_ids")
        self.logo = JSONHelper.getString(requestData, "logo")
        self.contractFrom = JSONHelper.getString(requestData, "contract_from")
        self.contractTo = JSONHelper.getString(requestData, "contract_to")
        self.inchargePersons = JSONHelper.getList(requestData, "incharge_persons")
        self.noOfLicence = JSONHelper.getInt(requestData, "no_of_user_licence")
        self.fileSpace = JSONHelper.getInt(requestData, "file_space") * 1000000000
        self.isSmsSubscribed = JSONHelper.getInt(requestData, "is_sms_subscribed")    
        self.dateConfigurations = JSONHelper.getList(requestData, "date_configurations")
        self.contractFrom = stringToDatetime(self.contractFrom)
        self.contractTo = stringToDatetime(self.contractTo)
        if self.isIdInvalid():
            self.response = "InvalidClientId"
        elif self.isDuplicateGroupName():
            self.response = "GroupNameAlreadyExists"
        else:
            self.db.updateClientGroup(self, sessionUser)
            self.db.saveDateConfigurations(self.clientId, self.dateConfigurations, sessionUser)
            self.db.saveClientCountries(self.clientId, self.countryIds)
            self.db.saveClientDomains(self.clientId, self.domainIds)
            self.db.saveInchargePersons(self)
            self.response = "UpdateClientGroupSuccess"
        return commonResponseStructure(self.response,{})

    def changeClientGroupStatus(self, requestData, sessionUser):
        self.sessionUser = int(sessionUser)
        self.response = ""
        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.isIdInvalid():
            self.response = "InvalidClientId"
        else:
            self.db.updateClientGroupStatus(self.clientId, self.isActive, sessionUser)
            self.response = "ChangeClientGroupStatusSuccess"
        return commonResponseStructure(self.response, {})
     
class ClientController(object):
    def __init__(self):
        self.db = DatabaseHandler.instance()

    def generateNewBusinessGroupId(self) :
        return self.db.generateNewId(self.db.tblBusinessGroups, "business_group_id")

    def generateNewLegalEntityId(self) :
        return self.db.generateNewId(self.db.tblLegalEntities, "legal_entity_id")

    def generateNewDivisionId(self) :
        return self.db.generateNewId(self.db.tblDivisions, "division_id")

    def generateNewUnitId(self) :
        return self.db.generateNewId(self.db.tblUnits, "unit_id")

    def isBusinessGroupIdInvalid(self, businessGroupId):
        condition = "business_group_id = '%d'" % businessGroupId
        return not self.db.isAlreadyExists(self.db.tblBusinessGroups, condition)

    def isLegalEntityIdInvalid(self, legalEntityId):
        condition = "legal_entity_id = '%d'" % legalEntityId
        return not self.db.isAlreadyExists(self.db.tblLegalEntities, condition)

    def isDivisionIdInvalid(self, divisionId):
        condition = "division_id = '%d'" % divisionId
        return not self.db.isAlreadyExists(self.db.tblDivisions, condition)

    def isUnitIdInvalid(self, unitId):
        condition = "unit_id = '%d'" % unitId
        return not self.db.isAlreadyExists(self.db.tblUnits, condition)

    def isDuplicateBusinessGroup(self, businessGroupId, businessGroupName, clientId):
        condition = "business_group_name ='%s' AND business_group_id != '%d' and client_id = '%d'" % (
            businessGroupName, businessGroupId, clientId)
        return self.db.isAlreadyExists(self.db.tblBusinessGroups, condition)

    def isDuplicateLegalEntity(self, legalEntityId, legalEntityName, clientId):
        condition = "legal_entity_name ='%s' AND legal_entity_id != '%d' and client_id = '%d'" % (
            legalEntityName, legalEntityId, clientId)
        return self.db.isAlreadyExists(self.db.tblLegalEntities, condition)

    def isDuplicateDivision(self, divisionId, divisionName, clientId):
        condition = "division_name ='%s' AND division_id != '%d' and client_id = '%d'" % (
            divisionName, divisionId, clientId)
        return self.db.isAlreadyExists(self.db.tblDivisions, condition)        

    def isDuplicateUnitName(self, unitId, unitName, clientId):
        condition = "unit_name ='%s' AND unit_id != '%d' and client_id = '%d'" % (
            unitName, unitId, clientId)
        return self.db.isAlreadyExists(self.db.tblUnits, condition)

    def isDuplicateUnitCode(self, unitId, unitCode, clientId):
        condition = "unit_code ='%s' AND unit_id != '%d' and client_id = '%d'" % (
            unitCode, unitId, clientId)
        return self.db.isAlreadyExists(self.db.tblUnits, condition)

    def saveClient(self, requestData, sessionUser):
        sessionUser = int(sessionUser)
        clientId = requestData["client_id"]
        businessGroup = requestData["business_group"]
        legalEntity = requestData["legal_entity"]
        division = requestData["division"]
        countryWiseUnits = requestData["country_wise_units"]
        businessGroupId = None
        businessGroupName = None
        divisionId = None
        divisionName = None
        optionalBusinessGroup = False
        optionalDivision = False
        result1 = False
        result2 = False
        result3 = False
        result4 = False
        existingBusinessGroup = False
        existingEntity = False
        existingDivision = False
        
        if businessGroup == None:
            optionalBusinessGroup = True
            result1 = True
        else:
            businessGroupId = businessGroup["business_group_id"]
            businessGroupName = businessGroup["business_group_name"]
            if businessGroupId == None:
                businessGroupId = self.generateNewBusinessGroupId()
            else:
                existingBusinessGroup = True
            if self.isDuplicateBusinessGroup(businessGroupId, businessGroupName, clientId):
                return commonResponseStructure("BusinessGroupNameAlreadyExists", {})

        legalEntityId = legalEntity["legal_entity_id"]
        legalEntityName = legalEntity["legal_entity_name"]
        if legalEntityId == None:
            legalEntityId = self.generateNewLegalEntityId()
        else:
            existingEntity = True
        if self.isDuplicateLegalEntity(legalEntityId, legalEntityName, clientId):
            return commonResponseStructure("LegalEntityNameAlreadyExists", {})

        if division == None:
            optionalDivision = True
            result3 = True
        else:
            divisionId = division["division_id"]
            divisionName = division["division_name"] 
            if divisionId == None:
                divisionId = self.generateNewDivisionId()
            else:
                existingDivision = True
            if self.isDuplicateDivision(divisionId, divisionName, clientId):
                return commonResponseStructure("DivisionNameAlreadyExists", {})
       
        unitsList = []
        unitId = None
        for country in countryWiseUnits:
            countryId = country["country_id"]
            units = country["units"]
            for unit in units:
                unitId = (unitId+1) if unitId != None else self.generateNewUnitId()
                domainIds = ",".join(str(x) for x in unit["domain_ids"])
                if self.isDuplicateUnitName(unitId, unit["unit_name"], clientId):
                    return commonResponseStructure("UnitNameAlreadyExists",{})
                elif self.isDuplicateUnitCode(unitId, unit["unit_code"], clientId):
                    return commonResponseStructure("UnitCodeAlreadyExists",{})
                else:
                    unit["unit_id"] = unitId
                    unit["country_id"] = countryId
                    unitsList.append(unit)
        if not optionalBusinessGroup:
            if not existingBusinessGroup:
                result1 = self.db.saveBusinessGroup(clientId, businessGroupId, businessGroupName, sessionUser)
            else:
                result1 = True
        if not existingEntity:
            result2 = self.db.saveLegalEntity(clientId, legalEntityId, legalEntityName, businessGroupId, sessionUser)
        else:
            result2 = True
        if not optionalDivision:
            if not existingDivision:
                result3 = self.db.saveDivision(clientId, divisionId, divisionName, businessGroupId, legalEntityId, sessionUser)
            else:
                result3 = True
        result4 = self.db.saveUnit(clientId, unitsList, businessGroupId, legalEntityId, divisionId, sessionUser)
        if result1 and result2 and result3 and result4:
            return commonResponseStructure("SaveClientSuccess", {})

    def updateClient(self, requestData, sessionUser):
        sessionUser = int(sessionUser)
        clientId = requestData["client_id"]
        businessGroup = requestData["business_group"]
        legalEntity = requestData["legal_entity"]
        division = requestData["division"]
        countryWiseUnits = requestData["country_wise_units"]

        businessGroupId = None
        businessGroupName = None
        divisionId = None
        divisionName = None
        optionalBusinessGroup = False
        optionalDivision = False
        result1 = False
        result2 = False
        result3 = False
        result4 = False
        result5 = False

        if businessGroup == None:
            optionalBusinessGroup = True
            result1 = True
        else:
            businessGroupId = businessGroup["business_group_id"]
            businessGroupName = businessGroup["business_group_name"]
            if self.isBusinessGroupIdInvalid(businessGroupId):
                return commonResponseStructure("InvalidBusinessGroupId", {})
            elif self.isDuplicateBusinessGroup(businessGroupId, businessGroupName, clientId):
                return commonResponseStructure("BusinessGroupNameAlreadyExists", {})

        legalEntityId = legalEntity["legal_entity_id"]
        legalEntityName = legalEntity["legal_entity_name"]
        if self.isLegalEntityIdInvalid(legalEntityId):
            return commonResponseStructure("InvalidLegalEntityId", {})
        elif self.isDuplicateLegalEntity(legalEntityId, legalEntityName, clientId):
            return commonResponseStructure("LegalEntityNameAlreadyExists", {})

        if division == None:
            optionalDivision = True
            result3 = True
        else:
            divisionId = division["division_id"]
            divisionName = division["division_name"] 
            if self.isDivisionIdInvalid(divisionId):
                return commonResponseStructure("InvalidDivisionId", {})
            elif self.isDuplicateDivision(divisionId, divisionName, clientId):
                return commonResponseStructure("DivisionNameAlreadyExists", {})
        
        newUnitsList = []
        existingUnitsList = []
        unitId = None
        for country in countryWiseUnits:
            countryId = country["country_id"]
            units = country["units"]
            for unit in units:
                domainIds = ",".join(str(x) for x in unit["domain_ids"])
                if unit["unit_id"] == None:
                    unitId = (unitId+1) if unitId != None else self.generateNewUnitId()
                    if self.isDuplicateUnitName(unitId, unit["unit_name"], clientId):
                        return commonResponseStructure("UnitNameAlreadyExists",{})
                    elif self.isDuplicateUnitCode(unitId, unit["unit_code"], clientId):
                        return commonResponseStructure("UnitCodeAlreadyExists",{})
                    else:
                        unit["unit_id"] = unitId
                        unit["country_id"] = countryId
                        newUnitsList.append(unit)
                else:
                    if self.isUnitIdInvalid(unit["unit_id"]):
                        return commonResponseStructure("InvalidUnitId", {})
                    elif self.isDuplicateUnitName(unit["unit_id"], unit["unit_name"], clientId):
                        return commonResponseStructure("UnitNameAlreadyExists",{})
                    elif self.isDuplicateUnitCode(unit["unit_id"], unit["unit_code"], clientId):
                        return commonResponseStructure("UnitCodeAlreadyExists",{})
                    else:
                        unit["country_id"] = countryId
                        existingUnitsList.append(unit)

        if not optionalBusinessGroup:
            result1 = self.db.updateBusinessGroup(clientId, businessGroupId, businessGroupName, sessionUser)
        result2 = self.db.updateLegalEntity(clientId, legalEntityId, legalEntityName, businessGroupId, sessionUser)
        if not optionalDivision:
            result3 = self.db.updateDivision(clientId, divisionId, divisionName, businessGroupId, legalEntityId, sessionUser)
        if len(newUnitsList) > 0:
            result4 = self.db.saveUnit(clientId, newUnitsList, businessGroupId, legalEntityId, divisionId, sessionUser)
        else:
            result4 = True
        result5 = self.db.updateUnit(clientId, existingUnitsList, businessGroupId, legalEntityId, divisionId, sessionUser)
        if result1 and result2 and result3 and result4 and result5:
            return commonResponseStructure("UpdateClientSuccess", {})


    def getClients(self, sessionUser):
        responseData = {}

        countryList = CountryList.getCountryList()
        domainList = DomainList.getDomainList()
        geographyLevelList = GeographyLevelList.getCountryWiseList()
        industryList = IndustryList.getList()
        geographyList = GeographyAPI.getList()

        clientIds =  self.db.getUserClients(sessionUser)
        if clientIds ==  None:
            print "Error : User is not responsible for any client"
        else:
            groupCompanyList = GroupCompany(self.db).getGroupCompanies(
                sessionUser = sessionUser, clientIds = clientIds)
            businessGroupList = []
            legalEntityList = []
            divisionList = []
            unitList = []
            for clientId in [int(x) for x in clientIds.split(",")]:
                businessGroupList = businessGroupList + BusinessGroup(clientId, self.db).getBusinessGroups()
                legalEntityList = legalEntityList + LegalEntity(clientId, self.db).getLegalEntities()
                divisionList = divisionList + Division(clientId, self.db).getDivisions()
                unitList = unitList + Unit(clientId, self.db).getUnitDetails()

            responseData["group_companies"] = groupCompanyList
            responseData["business_groups"] = businessGroupList
            responseData["legal_entities"] = legalEntityList
            responseData["divisions"] = divisionList
            responseData["units"] = unitList
            
        responseData["countries"] = countryList
        responseData["domains"] = domainList
        responseData["geography_levels"] = geographyLevelList
        responseData["geographies"] =geographyList
        responseData["industries"] = industryList
        
        return commonResponseStructure("GetClientsSuccess", responseData)
    
    def changeClientStatus(self, requestData, sessionUser):
        sessionUser = int(sessionUser)

        clientId = requestData["client_id"]
        legalEntityId = requestData["legal_entity_id"]
        isActive = requestData["is_active"]
        divisionId = requestData["division_id"]

        if self.db.changeClientStatus(clientId, legalEntityId, divisionId, 
            isActive, sessionUser):
            return commonResponseStructure("ChangeClientStatusSuccess",{})
        

    def reactivateUnit(self, requestData, sessionUser):
        sessionUser = int(sessionUser)
        clientId = requestData["client_id"]
        unitId = requestData["unit_id"]
        password = requestData["password"]
        encryptedPassword = encrypt(password)
        if self.db.verifyPassword(encryptedPassword, sessionUser):
            if self.db.reactivateUnit(clientId, unitId, sessionUser):
                return commonResponseStructure("ReactivateUnitSuccess", {})
        else:
            return commonResponseStructure("InvalidPassword", {})

class ClientProfile(object):

    def getClientProfile(self, sessionUser):
        clientIds = User.getClientIds(sessionUser)

        if clientIds ==  None:
            print "Error : User is not responsible for any client"
        else:
            client = Client()
            profiles = client.getProfiles(clientIds)
            groupCompanies = GroupCompany.getClientList(clientIds)

            responseData = {}
            responseData["group_companies"] = groupCompanies
            responseData["profiles"] = profiles
            return commonResponseStructure("GetClientProfileSuccess", responseData)

    def getClientDetailsReportFilters(self, sessionUser):
        clientIds = User.getClientIds(sessionUser)

        if clientIds ==  None:
            print "Error : User is not responsible for any client"
        else:
            countryList = CountryList.getCountryList()
            domainList = DomainList.getDomainList()
            groupCompanyList = GroupCompany.getClientList(clientIds)
            businessGroupList = BusinessGroup.getList(clientIds)
            legalEntityList = LegalEntity.getList(clientIds)
            divisionList = Division.getList(clientIds)
            unitList = Unit.getList(clientIds)

            responseData = {}
            responseData["countries"] = countryList
            responseData["domains"] = domainList
            responseData["group_companies"] = groupCompanyList
            responseData["business_groups"] = businessGroupList
            responseData["legal_entities"] = legalEntityList
            responseData["divisions"] = divisionList
            responseData["units"] = unitList

            return commonResponseStructure(
                "GetClientDetailsReportFiltersSuccess", responseData)

    def getClientDetailsReport(self, requestData, sessionUser):

        countryId = requestData["country_id"]
        clientId = requestData["group_id"]
        businessGroupId = requestData["business_group_id"]
        legalEntityId = requestData["legal_entity_id"]
        divisionId = requestData["division_id"]
        unitId = requestData["unit_id"]
        domainIds = requestData["domain_ids"]

        client = Client()
        divisionWiseUnitDetails = client.getReport(
                countryId, clientId, businessGroupId, legalEntityId, 
                divisionId, unitId, domainIds)

        responseData = {}
        responseData["units"] = divisionWiseUnitDetails

        return commonResponseStructure(
            "GetClientDetailsReportSuccess", responseData)

        