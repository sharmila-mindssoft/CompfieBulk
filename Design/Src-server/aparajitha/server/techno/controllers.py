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

    def toStructure(self, clientId) :
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
    businessGroupTblName = "tbl_business_groups"
    legalEntityTblName = "tbl_legal_entities"
    divisionTblName = "tbl_divisions"
    unitTblName = "tbl_units"
    clientDBName = None
    responseData = None
    unitObjList = []
    businessGroupObj = None
    legalEntityObj = None
    divisionObj = None
    optionalBusinessGroup = False
    optionalDivision = False

    def saveClient(self, requestData, sessionUser, savetype):
        self.sessionUser = int(sessionUser)
        self.clientId = requestData["client_id"]
        self.type = savetype
        
        self.businessGroup = requestData["business_group"]
        self.legalEntity = requestData["legal_entity"]
        self.division = requestData["division"]
        self.countryWiseUnits = requestData["country_wise_units"]

        if self.businessGroup == None:
            self.optionalBusinessGroup = True     
        
        if self.division == None:
            self.optionalDivision = True        

        if self.type == "save":
            if self.processRequest():
                if self.saveUnit():
                   self.responseData = commonResponseStructure("SaveClientSuccess", {}) 
                else:
                    print "Error: Failed to save client"
            else:
                print "Error : Save Client request validation failed"
        elif self.type == "update":
            if self.processUpdateRequest():
                if self.updateUnit():
                    self.responseData = commonResponseStructure("UpdateClientSuccess", {}) 
                else:
                    print "Error: Failed to update client"
            else:
                print "Error : Update Client request validation failed"

        return self.responseData

    def processRequest(self):
        print "inside process request"
        if not self.optionalBusinessGroup:
            print "inside not optionalBusinessGroup"
            self.businessGroupId = self.businessGroup["business_group_id"]
            self.businessGroupName = self.businessGroup["business_group_name"]
            if self.businessGroupId == None:
                if not self.saveBusinessGroup():
                    return False
            print self.businessGroupId
            print self.businessGroupName
        else:
            self.businessGroupId = None
            self.businessGroupName = None
            
        self.legalEntityId = self.legalEntity["legal_entity_id"]
        self.legalEntityName = self.legalEntity["legal_entity_name"]
        if self.legalEntityId == None:
            if not self.saveLegalEntity():
                return False
        print self.legalEntityId
        print self.legalEntityName

        if not self.optionalDivision:
            print "inside not optionaldivision"
            self.divisionId = self.division["division_id"]
            self.divisionName = self.division["division_name"]
            if self.divisionId == None:
                if not self.saveDivision():
                    return False
            print self.divisionId
            print self.divisionName
        else:
            self.divisionId = None
            self.divisionName = None                      
        self.unitObjList = []
        for country in self.countryWiseUnits:
            countryId = JSONHelper.getInt(country,"country_id")
            units = JSONHelper.getList(country, "units")
            for unit in units:
                try:
                    self.unitId = JSONHelper.getInt(unit, "unit_id")
                    print "inside try unit id {unitId}".format(unitId = self.unitId)
                except:
                    print "inside except.. will generate new id"
                    self.unitId = None
                unitCode = JSONHelper.getString(unit, "unit_code")
                unitName = JSONHelper.getString(unit, "unit_name")
                address = JSONHelper.getString(unit, "unit_address")
                postalCode = JSONHelper.getString(unit, "postal_code")
                geographyId = JSONHelper.getInt(unit, "geography_id")
                geography = JSONHelper.getString(unit, "unit_location")
                industryId = JSONHelper.getInt(unit, "industry_id")
                industryName = JSONHelper.getString(unit, "industry_name")
                domainIds = JSONHelper.getList(unit, "domain_ids")

                unitObj = Unit(self.unitId, 
                               self.divisionId,
                               self.legalEntityId, 
                                self.businessGroupId, 
                                self.clientId, countryId,geographyId, unitCode, 
                                unitName, industryId, address, postalCode, domainIds, 
                                None, industryName, geography)
                if unitObj.isDuplicateUnitName():
                    self.responseData = commonResponseStructure("UnitNameAlreadyExists",{})
                    return False
                elif unitObj.isDuplicateUnitCode():
                    self.responseData = commonResponseStructure("UnitCodeAlreadyExists",{})
                    return False
                elif self.unitId != None:
                    if unitObj.isIdInvalid():
                        self.responseData = commonResponseStructure("InvalidUnitId",{})
                        return False
                    else:
                        self.unitObjList.append(unitObj)
                else:
                    self.unitObjList.append(unitObj)
        print self.unitObjList
        return True

    def processUpdateRequest(self):
        print "inside update request"
        if not self.optionalBusinessGroup:
            print "inside not optionalBusinessGroup"
            self.businessGroupId = self.businessGroup["business_group_id"]
            self.businessGroupName = self.businessGroup["business_group_name"]
            if not self.updateBusinessGroup():
                return False
        else:
            self.businessGroupId = None
            self.businessGroupName = None
            
        self.legalEntityId = self.legalEntity["legal_entity_id"]
        self.legalEntityName = self.legalEntity["legal_entity_name"]
        if not self.updateLegalEntity():
            return False

        if not self.optionalDivision:
            print "inside not optionalBusinessGroup"
            self.divisionId = self.division["division_id"]
            self.divisionName = self.division["division_name"]
            if not self.updateDivision():
                return False
        else:
            self.divisionId = None
            self.divisionName = None                      

        for country in self.countryWiseUnits:
            countryId = JSONHelper.getInt(country,"country_id")
            units = JSONHelper.getList(country, "units")
            for unit in units:
                self.unitId = JSONHelper.getInt(unit, "unit_id")
                unitCode = JSONHelper.getString(unit, "unit_code")
                unitName = JSONHelper.getString(unit, "unit_name")
                address = JSONHelper.getString(unit, "unit_address")
                postalCode = JSONHelper.getString(unit, "postal_code")
                geographyId = JSONHelper.getInt(unit, "geography_id")
                geography = JSONHelper.getString(unit, "unit_location")
                industryId = JSONHelper.getInt(unit, "industry_id")
                industryName = JSONHelper.getString(unit, "industry_name")
                domainIds = JSONHelper.getList(unit, "domain_ids")

                unitObj = Unit(self.unitId, 
                               self.divisionId,
                               self.legalEntityObj.legalEntityId, 
                                self.businessGroupId, 
                                self.clientId, countryId,geographyId, unitCode, 
                                unitName, industryId, address, postalCode, domainIds, 
                                None, industryName, geography)
                
                if unitObj.isIdInvalid():
                    self.responseData = commonResponseStructure("InvalidUnitId",{})
                    return False
                elif unitObj.isDuplicateUnitName():
                    self.responseData = commonResponseStructure("UnitNameAlreadyExists",{})
                    return False
                elif unitObj.isDuplicateUnitCode():
                    self.responseData = commonResponseStructure("UnitCodeAlreadyExists",{})
                    return False
                elif self.unitId != None:
                    if unitObj.isIdInvalid():
                        self.responseData = commonResponseStructure("InvalidUnitId",{})
                        return False
                    else:
                        self.unitObjList.append(unitObj)
                else:
                    self.unitObjList.append(unitObj)
        return True
            
    def saveBusinessGroup(self):
        print "inside save Business group"
        self.businessGroupObj = BusinessGroup(self.businessGroupId, self.businessGroupName, self.clientId) 
        self.businessGroupId = self.businessGroupObj.businessGroupId
        if (self.businessGroupObj.isDuplicate()):
            self.responseData = commonResponseStructure("BusinessGroupNameAlreadyExists", {})
            return False
        elif self.businessGroupObj.save(self.sessionUser):
            return True

    def saveLegalEntity(self):
        print "inside save legal entity"
        self.legalEntityObj = LegalEntity(self.legalEntityId, self.legalEntityName, 
                                self.businessGroupId, 
                                self.clientId)
        self.legalEntityId = self.legalEntityObj.legalEntityId
        if self.legalEntityObj.isDuplicate():
            self.responseData = commonResponseStructure("LegalEntityNameAlreadyExists", {})
            return False
        elif self.legalEntityObj.save(self.sessionUser):
            return True

    def saveDivision(self):
        print "inside save division"
        self.divisionObj = Division(self.divisionId, self.divisionName, 
                            self.legalEntityId, 
                            self.businessGroupId, 
                            self.clientId)
        self.divisionId = self.divisionObj.divisionId
        if self.divisionObj.isDuplicate():
            self.responseData = commonResponseStructure("DivisionNameAlreadyExists", {})
            return False
        elif self.divisionObj.save(self.sessionUser):
            return True

    def saveUnit(self):
        print "inside save unit"
        for unitObj in self.unitObjList:
            print "unitObj.unitId :{x}".format(x= unitObj.unitId)
            if unitObj.save(self.sessionUser):
                continue
            else:
                return False
        return True

    def updateBusinessGroup(self):
        print "inside update bg"
        self.businessGroupObj = BusinessGroup(self.businessGroupId, self.businessGroupName, self.clientId) 
        if self.businessGroupObj.isIdInvalid():
            self.responseData = commonResponseStructure("InvalidBusinessGroupId",{})
            return False
        elif (self.businessGroupObj.isDuplicate()):
            self.responseData = commonResponseStructure("BusinessGroupNameAlreadyExists", {})
            return False
        elif self.businessGroupObj.update(self.sessionUser):
            return True

    def updateLegalEntity(self):
        print "inside update legal entity"
        self.legalEntityObj = LegalEntity(self.legalEntityId, self.legalEntityName, 
                                self.businessGroupId, 
                                self.clientId)
        if self.legalEntityObj.isIdInvalid():
            self.responseData = commonResponseStructure("InvalidLegalEntityId",{})
            return False
        elif self.legalEntityObj.isDuplicate():
            self.responseData = commonResponseStructure("LegalEntityNameAlreadyExists", {})
            return False
        elif self.legalEntityObj.update(self.sessionUser):
            return True

    def updateDivision(self):
        print "inside update division"
        self.divisionObj = Division(self.divisionId, self.divisionName, 
                            self.legalEntityObj.legalEntityId, 
                            self.businessGroupId, 
                            self.clientId)
        if self.divisionObj.isIdInvalid():
            self.responseData = commonResponseStructure("InvalidDivisionId",{})
            return False
        elif self.divisionObj.isDuplicate():
            self.responseData = commonResponseStructure("DivisionNameAlreadyExists", {})
            return False
        elif self.divisionObj.update(self.sessionUser):
            return True

    def updateUnit(self):
        print "inside update unit"
        for unitObj in self.unitObjList:
            if unitObj.update(self.sessionUser):
                continue
            else:
                return False
        return True


    def getClients(self, sessionUser):
        responseData = {}

        countryList = CountryList.getCountryList()
        domainList = DomainList.getDomainList()
        geographyLevelList = GeographyLevelList.getCountryWiseList()
        industryList = IndustryList.getList()
        geographyList = GeographyAPI.getList()

        clientIds = User.getClientIds(sessionUser)
        if clientIds ==  None:
            print "Error : User is not responsible for any client"
        else:
            groupCompanyList = GroupCompany.getClientList(clientIds)
            businessGroupList = BusinessGroup.getList(clientIds)
            legalEntityList = LegalEntity.getList(clientIds)
            divisionList = Division.getList(clientIds)
            unitList = Unit.getDetailedList(clientIds)
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
        self.sessionUser = int(sessionUser)

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.legalEntityId = JSONHelper.getInt(requestData, "legal_entity_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        try:
            self.divisionId = JSONHelper.getInt(requestData, "division_id")
        except:
            self.divisionId = None

        client = Client()
        if client.changeClientStatus(self.clientId, self.legalEntityId, self.divisionId, 
            self.isActive, self.sessionUser):
            return commonResponseStructure("ChangeClientStatusSuccess",{})
        else:
            print "Error: Failed to change status of unit"

    def reactivateUnit(self, requestData, sessionUser):
        print "inside reactivate unit"
        self.sessionUser = int(sessionUser)

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.unitId = JSONHelper.getInt(requestData, "unit_id")
        self.password = JSONHelper.getString(requestData, "password")
        self.isActive = 1
        if self.verifyPassword():
            client = Client()
            if client.changeClientStatus(self.clientId, self.divisionId, 
                self.isActive, self.sessionUser):
                return commonResponseStructure("ReactivateUnitSuccess", {})
            else:
                print "Error: Failed to activate unit"
        else:
            return commonResponseStructure("InvalidPassword", {})

    def verifyPassword(self):
        encryptedPassword = encrypt(self.password)
        return DatabaseHandler.instance().verifyPassword(
            encryptedPassword, self.sessionUser, self.clientId)

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

        