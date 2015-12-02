from types import *
import json
import re
import os

from aparajitha.server.constants import ROOT_PATH
from aparajitha.server.databasehandler import DatabaseHandler 
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler 
from aparajitha.server.admin.models import User
from aparajitha.server.knowledge.models import DomainList, CountryList, GeographyLevelList
from aparajitha.server.knowledge.models import IndustryList, Geography
from aparajitha.server.common import *

__all__ = [
    "GroupCompany",
    "ClientConfiguration",
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit",
    "Client"
]
clientDatabaseMappingFilePath = os.path.join(ROOT_PATH, 
    "Src-client/files/desktop/common/clientdatabase/clientdatabasemapping.txt")

class GroupCompany(object):
    clientTblName = "tbl_client_groups"
    clientSettingsTblName = "tbl_client_settings"
    clietConfigurationTblName = "tbl_client_configurations"
    userDetailsTblName = "tbl_user_details"
    clientUserDetailsTblName = "tbl_client_user_details"
    userTblName = "tbl_users"

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

    @classmethod
    def getClientAdminUsername(self, clientId):
        username = ""
        columns = "user_id"
        condition = " is_admin = 1"
        rows = []

        try : 
            clientDBName = self.getClienDatabaseName(clientId)
            rows = ClientDatabaseHandler.instance(clientDBName).getData(self.clientUserDetailsTblName,
                    columns, condition)
        except:
            print "Error : Client Database Not exists for the client %d" % clientId

        if len(rows) < 1:
            print "Error :User details not found for client admin"

        for row in rows:
            userId = int(row[0])
            columns = "username"
            condition = "user_id='%d'" % userId
            rows = DatabaseHandler.instance().getData(self.userTblName, columns, condition)
            try :
                username += rows[0][0]
            except:
                print "Error: No Credentials exist for admin user "+str(userId)+" for client %d" % clientId

        return username

    @classmethod
    def getClienDatabaseName(self, clientId):
        clientDBName = getClientDatabase(clientId)
        if clientDBName == None:
            print "Error : Database Not exists for the client %d" % int(clientId)
        return clientDBName

    @classmethod
    def getSettings(self, clientId):
        clientSettingsColumns = "country_ids,domain_ids,logo_url,contract_from,"+\
                    "contract_to,no_of_user_licence,total_disk_space,is_sms_subscribed"
        settingsRows = []
        settingsDataList = []
       
        clientDBName = self.getClienDatabaseName(clientId)
        settingsRows = ClientDatabaseHandler.instance(clientDBName).getData(self.clientSettingsTblName,
                clientSettingsColumns, "1")

        countryIds = settingsRows[0][0].split(",")
        domainIds = settingsRows[0][1].split(",")
        logo = settingsRows[0][2]
        contractFrom = datetimeToString(timestampToDatetime(settingsRows[0][3]))
        contractTo = datetimeToString(timestampToDatetime(settingsRows[0][4]))
        noOfUserLicence = int(settingsRows[0][5])
        fileSpace = settingsRows[0][6]
        isSmsSubscribed = int(settingsRows[0][7])  
        settingsDataList = [countryIds, domainIds, logo, contractFrom, contractTo, noOfUserLicence,
                            fileSpace, isSmsSubscribed]

        return settingsDataList    

    @classmethod
    def getDateConfigurations(self, clientId):
        clientConfigurationColums = "country_id, domain_id, period_from, period_to"
        try:
            clientDBName = self.getClienDatabaseName(clientId)
            configurationRows = ClientDatabaseHandler.instance(clientDBName).getData(self.clietConfigurationTblName,
                    clientConfigurationColums, "1")
        except:
            print "Error : Client Database Not exists for the client %d" % clientId

        dateConfigurations = []

        for configuraion in configurationRows:
            country_id = int(configuraion[0])
            domain_id = int(configuraion[1])
            period_from = int(configuraion[2])
            period_to = int(configuraion[3])
            clientConfiguration = ClientConfiguration(country_id, domain_id,
                period_from, period_to)
            dateConfigurations.append(clientConfiguration.toStructure())

        return dateConfigurations

    @classmethod
    def getClientGroups(self):
        clientGroupColumns = "client_id, group_name,incharge_persons,is_active"
        rows = DatabaseHandler.instance().getData(self.clientTblName, clientGroupColumns, "1")
        return rows

    @classmethod
    def getDetailedClientList(self):
        clientList = []

        clientGroupRows = self.getClientGroups()

        for row in clientGroupRows:
                clientId = int(row[0])
                groupName = row[1]
                inchargePersons = row[2].split(",")
                isActive = row[3]

                username = self.getClientAdminUsername(clientId)
                settingsDataList = self.getSettings(clientId)
                countryIds = settingsDataList[0]
                domainIds = settingsDataList[1]
                logo = settingsDataList[2]
                contractFrom = settingsDataList[3]
                contractTo = settingsDataList[4]
                noOfUserLicence = settingsDataList[5]
                fileSpace = settingsDataList[6]
                isSmsSubscribed = settingsDataList[7]
                dateConfigurations = self.getDateConfigurations(clientId)

                groupCompany = GroupCompany(int(clientId), groupName, inchargePersons, countryIds ,domainIds, 
                                            logo, contractFrom, contractTo, noOfUserLicence, fileSpace, 
                                            isSmsSubscribed, dateConfigurations, username, isActive)
                groupCompany.verify()

                clientList.append(groupCompany.toDetailedStructure())

        return clientList

    @classmethod
    def getClientList(self, clientIds):
        clientList = []
        clientDetails = {}
        column = "client_id, group_name, is_active"
        condition = "client_id in (%s)" % clientIds
        clientRows = DatabaseHandler.instance().getData(self.clientTblName, column, condition)

        for row in clientRows:
            clientDetails[str(row[0])] = [row[1], row[2]]

        for index, clientId in enumerate(clientIds.split(",")):
            clientDBName = self.getClienDatabaseName(clientId)
            columns = "country_ids, domain_ids"
            settingsRows = ClientDatabaseHandler.instance(clientDBName).getData(self.clientSettingsTblName,
                columns, "1")

            clientDetail = clientDetails[clientId]
            groupName = clientDetail[0]
            countryIds = settingsRows[0][0]
            domainIds = settingsRows[0][1]
            isActive = clientDetail[1]
                
            groupCompany = GroupCompany(int(clientId), groupName, None, countryIds ,domainIds, None, 
                                        None, None, None, None, None,None, None, isActive)
            clientList.append(groupCompany.toStructure())
            

        return clientList

class ClientConfiguration(object):

    def __init__(self, countryId, domainId, periodFrom, periodTo):
        self.countryId = countryId
        self.domainId = domainId
        self.periodFrom = periodFrom
        self.periodTo = periodTo

        self.verify()

    def verify(self):
        assertType(self.countryId, IntType)
        assertType(self.domainId, IntType)
        assertType(self.periodFrom, IntType)
        assertType(self.periodTo, IntType)

    def toStructure(self):
        return {
            "country_id": self.countryId,
            "domain_id": self.domainId,
            "period_from": self.periodFrom,
            "period_to": self.periodTo
        }

class BusinessGroup(object):
    businessGroupTblName = "tbl_business_groups"

    def __init__(self, businessGroupId, businessGroupName, clientId):
        self.clientId = clientId
        self.businessGroupId = businessGroupId if businessGroupId != None else self.generateNewBusinessGroupId()
        self.businessGroupName = businessGroupName

    def verify(self) :
        assertType(self.businessGroupId, IntType)
        assertType(self.businessGroupName, StringType)
        assertType(self.clientId, IntType)

    def toStructure(self) :
        return {
            "business_group_id": self.businessGroupId,
            "business_group_name": self.businessGroupName,
            "client_id": self.clientId
        }

    def generateNewBusinessGroupId(self):
        return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).generateNewId(
                self.businessGroupTblName, "business_group_id")

    def isIdInvalid(self):
        condition = "business_group_id = '%d'" % self.businessGroupId
        return not ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).isAlreadyExists(
                self.businessGroupTblName, condition)

    def isDuplicate(self):
        condition = "business_group_name= '%s' and business_group_id != '%d'" % (
                    self.businessGroupName, self.businessGroupId)
        return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).isAlreadyExists(
                self.businessGroupTblName, condition)

    def save(self, sessionUser):
        print "inside businessGroup save"
        valuesList = []
        columns = "business_group_id, business_group_name, created_on, created_by,"+\
                "updated_on, updated_by"
        valuesTuple = (self.businessGroupId, self.businessGroupName, getCurrentTimeStamp(), 
                        sessionUser, getCurrentTimeStamp(), sessionUser)
        valuesList.append(valuesTuple)
        updateColumnsList = ["business_group_name", "updated_on", "updated_by"]
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).onDuplicateKeyUpdate(
            self.businessGroupTblName, columns, valuesList, updateColumnsList)

    @classmethod
    def getList(self, clientIds):
        businessGroupList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = getClientDatabase(clientId)
                columns = "business_group_id, business_group_name"
                rows = ClientDatabaseHandler.instance(clientDBName).getData(
                    self.businessGroupTblName,columns, "1")

                for row in rows:
                    businessGroupId = row[0]
                    businessGroupName = row[1]
                    businessGroup = BusinessGroup(businessGroupId, businessGroupName, 
                        int(clientId))
                    businessGroupList.append(businessGroup.toStructure())
            except:
                print "Error: While fetching Business Groups of client id %s" % clientId

        return businessGroupList

class LegalEntity(object):
    legalEntityTblName = "tbl_legal_entities"

    def __init__(self, legalEntityId, legalEntityName, businessGroupId, clientId):
        self.clientId = clientId
        self.legalEntityId = legalEntityId if legalEntityId != None else self.generateNewLegalEntityId()
        self.legalEntityName = legalEntityName
        self.businessGroupId = businessGroupId
        

    def verify(self) :
        assertType(self.legalEntityId, IntType)
        assertType(self.legalEntityName, StringType)
        assertType(self.businessGroupId, IntType)
        assertType(self.clientId, IntType)

    def toStructure(self) :
        return {
            "legal_entity_id": self.legalEntityId,
            "legal_entity_name": self.legalEntityName,
            "business_group_id": self.businessGroupId,
            "client_id": self.clientId
        }

    def generateNewLegalEntityId(self):
        return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).generateNewId(
                self.legalEntityTblName, "legal_entity_id")

    def isIdInvalid(self):
        condition = "legal_entity_id = '%d'" % self.legalEntityId
        return not ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).isAlreadyExists(
                self.legalEntityTblName, condition)

    def isDuplicate(self):
        condition = "legal_entity_name= '%s' and legal_entity_id != '%d'" % (
                    self.legalEntityName, self.legalEntityId)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(
            self.legalEntityTblName, condition)

    def save(self, sessionUser):
        print "inside legalEntity save"
        columns = "legal_entity_id, legal_entity_name, business_group_id,"+\
                  "created_on, created_by, updated_on, updated_by"
        valuesTuple = (self.legalEntityId, self.legalEntityName, self.businessGroupId, 
                        getCurrentTimeStamp(), sessionUser, 
                        getCurrentTimeStamp(), sessionUser)
        valuesList =  []
        valuesList.append(valuesTuple)
        updateColumnsList = ["legal_entity_name", "updated_on", "updated_by"]
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).onDuplicateKeyUpdate(
            self.legalEntityTblName, columns, valuesList, updateColumnsList)

    @classmethod
    def getList(self, clientIds):
        legalEntitiesList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = getClientDatabase(clientId)
                columns = "legal_entity_id, legal_entity_name, business_group_id"
                rows = ClientDatabaseHandler.instance(clientDBName).getData(
                    self.legalEntityTblName,columns, "1")

                for row in rows:
                    legalEntityId = row[0]
                    legalEntityName = row[1]
                    businessGroupId = row[2]
                    legalEntity = LegalEntity(legalEntityId, legalEntityName, 
                        businessGroupId, int(clientId))
                    legalEntitiesList.append(legalEntity.toStructure())
            except:
                print "Error: While fetching Legal Entities of client id %s" % clientId

        return legalEntitiesList

class Division(object):
    divisionTblName = "tbl_divisions"

    def __init__(self, divisionId, divisionName,legalEntityId, businessGroupId, clientId):
        self.clientId = clientId
        self.divisionId = divisionId if divisionId != None else self.generateNewDivisionId()
        self.divisionName = divisionName
        self.legalEntityId = legalEntityId
        self.businessGroupId = businessGroupId

    def verify(self) :
        assertType(self.divisionId, IntType)
        assertType(self.divisionName, StringType)
        assertType(self.legalEntityId, IntType)
        assertType(self.businessGroupId, IntType)
        assertType(self.clientId, IntType)

    def toStructure(self) :
        return {
            "division_id": self.divisionId,
            "division_name": self.divisionName,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId,
            "client_id": self.clientId
        }

    def generateNewDivisionId(self):
        return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).generateNewId(
                self.divisionTblName, "division_id")

    def isIdInvalid(self):
        condition = "division_id = '%d'" % self.divisionId
        return not ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.divisionTblName, condition)
    
    def isDuplicate(self):
        condition = "division_name= '%s'  and division_id != '%d'" % (
                    self.divisionName, self.divisionId)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(
            self.divisionTblName, condition)

    def save(self, sessionUser):
        print "Entered into saveDivision"
        columns = "division_id, division_name, legal_entity_id, business_group_id,"+\
                  "created_on, created_by, updated_on, updated_by"
        valuesTuple = (self.divisionId, self.divisionName, self.legalEntityId, 
                        self.businessGroupId, getCurrentTimeStamp(), sessionUser, 
                        getCurrentTimeStamp(), sessionUser)          
        valuesList =  []
        valuesList.append(valuesTuple)
        updateColumnsList = ["division_name", "updated_on", "updated_by"]
        return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).onDuplicateKeyUpdate(
                self.divisionTblName, columns, valuesList, updateColumnsList)

    @classmethod
    def getList(self, clientIds):
        divisionsList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = getClientDatabase(clientId)
                columns = "division_id, division_name, legal_entity_id, business_group_id"
                rows = ClientDatabaseHandler.instance(clientDBName).getData(
                    self.divisionTblName,columns, "1")

                for row in rows:
                    divisionId = row[0]
                    divisionName = row[1]
                    legalEntityId = row[2]
                    businessGroupId = row[2]
                    division = Division(divisionId, divisionName, legalEntityId, 
                        businessGroupId, int(clientId))
                    divisionsList.append(division.toStructure())
            except:
                print "Error: While fetching Division of client id %s" % clientId

        return divisionsList

class Unit(object):
    unitTblName = "tbl_units"
    divisionTblName = "tbl_divisions"
    legalEntityTblName = "tbl_legal_entities"
    businessGroupTblName = "tbl_business_groups"

    def __init__(self, unitId, divisionId, legalEntityId, businessGroupId, clientId, 
                countryId, geographyId, unitCode, unitName, industryId, address, 
                postalCode, domainIds, isActive, industryName, geography):
        self.clientId = clientId
        self.unitId = unitId if unitId != None else self.generateNewUnitId()
        self.divisionId = divisionId
        self.legalEntityId = legalEntityId
        self.businessGroupId = businessGroupId
        self.countryId = countryId
        self.geographyId = geographyId
        self.unitCode = unitCode
        self.unitName = unitName
        self.industryId = industryId
        self.address = address
        self.postalCode = postalCode
        self.domainIds = domainIds
        self.isActive = isActive if isActive != None else 1
        self.industryName = industryName
        self.geography = geography

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
            "country_id": self.countryId,
            "domain_ids": self.domainIds,
            "unit_name": unitName,
            "unit_address": self.address
        }

    def generateNewUnitId(self):
        return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).generateNewId(
                self.unitTblName, "unit_id")

    def isIdInvalid(self):
        condition = "unit_id = '%d'" % self.unitId
        return not ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.unitTblName, condition)

    def isDuplicateUnitName(self):
        condition = "unit_name= '%s' and unit_id != '%d'" % (
                    self.unitName, self.unitId)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.unitTblName, condition)

    def isDuplicateUnitCode(self):
        condition = "unit_code= '%s' and unit_id != '%d'" % (
                    self.unitCode, self.unitId)
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.unitTblName, condition)

    def save(self, sessionUser):
        print "inside unit save"
        knowledgeValueslist = []
        clientValuesList = []
        clientDbColumns = "unit_id, division_id, legal_entity_id, business_group_id,"+\
                        " country_id, geography, unit_code, unit_name, industry_name,"+\
                        " address, postal_code, domain_ids"
        knowledgeDbColumns = "client_id, unit_id, country_id, geography_id, unit_code,"+\
                            " unit_name, industry_id, created_by, created_on,"+\
                            " updated_by, updated_on"
        
        knowledgeValuesTuple = (self.clientId, self.unitId, self.countryId, self.geographyId,
                                self.unitCode, self.unitName, self.industryId, 
                                int(sessionUser), getCurrentTimeStamp(), 
                                int(sessionUser), getCurrentTimeStamp())
        knowledgeValueslist.append(knowledgeValuesTuple)
        clientValuesTuple = ( self.unitId, self.divisionId, self.legalEntityId,
                            self.businessGroupId, self.countryId, self.geography, 
                            self.unitCode, self.unitName, self.industryName, 
                            self.address, self.postalCode, 
                            ",".join(str(x) for x in self.domainIds))
        clientValuesList.append(clientValuesTuple)


        knowledgeUpdateColumnsList = ["geography_id", "unit_code", "unit_name", "industry_id",
        "updated_by", "updated_on"]
        clientUpdateColumnsList = ["geography", "unit_code", "unit_name", "industry_name",
        "address", "postal_code", "domain_ids"]
        
        if DatabaseHandler.instance().onDuplicateKeyUpdate(
                        self.unitTblName, knowledgeDbColumns, knowledgeValueslist, 
                        knowledgeUpdateColumnsList):
            return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).onDuplicateKeyUpdate(
                self.unitTblName, clientDbColumns, clientValuesList, clientUpdateColumnsList)

    @classmethod
    def getList(self,clientIds):
        unitList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = getClientDatabase(clientId)
                clientColumns = "unit_id, division_id, legal_entity_id, "+\
                                "business_group_id, unit_code, unit_name,"+\
                                " country_id, address, domain_ids"

                rows = ClientDatabaseHandler.instance(clientDBName).getData(
                    self.unitTblName, clientColumns, "1")

                for row in rows:
                    unitId = row[0]
                    divisionId = row[1]
                    legalEntityId = row[2]
                    businessGroupId = row[3]
                    unitCode = row[4]
                    unitName = row[5]
                    countryId = row[6]
                    address = row[7]
                    domainIds = row[8]
                    unit = Unit(unitId, divisionId, legalEntityId, businessGroupId, 
                            int(clientId), countryId, None, unitCode, unitName,
                            None, address, None, domainIds, None, None, None)
                    unitList.append(unit.toStructure())

            except:
                print "Error: While fetching Unit of client id %s" % clientId

        return unitList

    @classmethod
    def getUnitListForClosure(self, clientId):
        unitList = []

        columns = "business_group_name,legal_entity_name,division_name,unit_id,"+\
                    "unit_code, unit_name, address,is_active"
        tables = [self.unitTblName, self.divisionTblName, self.legalEntityTblName,
                self.businessGroupTblName]
        conditionColumns = [("division_id","division_id"), 
                            ("legal_entity_id","legal_entity_id"),
                            ("business_group_id","business_group_id")]

        clientDBName = self.getClientDatabaseName(clientId)
        rows = ClientDatabaseHandler.instance(clientDBName).getDataFromMultipleTables(
            columns, tables, conditionColumns, "left join")
        
        for row in rows:
            unitStructure = {}
            unitStructure["business_group_name"] = row[0]
            unitStructure["legal_entity_name"] = row[1]
            unitStructure["division_name"] = row[2]
            unitStructure["unit_id"] = row[3]
            unitStructure["unit_name"] = "%s - %s" % (row[4], row[5])
            unitStructure["address"] = row[6]
            unitStructure["is_active"] = row[7]
            unitList.append(unitStructure)

        return unitList

    @classmethod
    def getDetailedList(self, clientIds):
        unitList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = getClientDatabase(clientId)
                clientColumns = "unit_id, division_id, legal_entity_id, business_group_id, "+\
                                "unit_code, unit_name, country_id,  address,"+\
                                "postal_code, domain_ids, is_active"

                rows = ClientDatabaseHandler.instance(clientDBName).getData(
                    self.unitTblName, clientColumns, "1")

                knowledgeColumns = "geography_id, industry_id"

                for row in rows:
                    unitId = row[0]
                    divisionId = row[1]
                    legalEntityId = row[2]
                    businessGroupId = row[3]
                    unitCode = row[4]
                    unitName = row[5]
                    countryId = row[6]
                    address = row[7]
                    postalCode = row[8]
                    domainIds = row[9]
                    isActive = row[10]
                    knowledgeRows = DatabaseHandler.instance().getData(self.unitTblName, 
                        knowledgeColumns, "1")
                    for knowledgeRow in knowledgeRows:
                        geographyId = knowledgeRow[0]
                        industryId = knowledgeRow[1]
                    unit = Unit(unitId, divisionId, legalEntityId, businessGroupId, 
                            int(clientId), countryId, geographyId, unitCode, unitName,
                            industryId, address, postalCode, domainIds, isActive, None, None)
                    unitList.append(unit.toDetailedStructure())

            except:
                print "Error: While fetching Unit of client id %s" % clientId

        return unitList

class Client(object):
    unitTblName = "tbl_units"
    clientSettingsTblName = "tbl_client_settings"
    clientUserDetails = "tbl_client_user_details"
    usersTblName = "tbl_users"

    def save(self, businessGroup, legalEntity, division, 
        unitList , sessionUser):
        self.businessGroup = businessGroup
        self.legalEntity = legalEntity
        self.division = division
        self.unitList = unitList
        self.sessionUser = sessionUser
        if self.businessGroup.save(self.sessionUser):
            if self.legalEntity.save(self.sessionUser):
                if self.division.save(self.sessionUser):
                    for unitObj in self.unitList:
                        if unitObj.save(self.sessionUser):
                            continue
                        else:
                            return False
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def changeClientStatus(self, clientId, divisionId, 
        isActive, sessionUser):
        self.clientId = clientId
        self.divisionId = divisionId
        self.isActive = isActive
        self.sessionUser = sessionUser
        if self.changeUnitStatusInClientDB():
            if self.changeUnitStatusInKnowledgeDB():
                return True
            else:
                return Faslse
        else:
            return False

    def changeUnitStatusInClientDB(self):
        columns = ["is_active"]
        values = [self.isActive]
        condition = "division_id='%d'" % self.divisionId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.unitTblName, columns, values, condition)

    def getUnitsOfDivision(self):
        unitIdsList = []
        columns = "unit_id"
        condition = "division_id='%d'" % self.divisionId
        rows = ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).getData(self.unitTblName, columns, condition)
        for row in rows:
            unitIdsList.append(row[0])

        return unitIdsList

    def changeUnitStatusInKnowledgeDB(self):
        columns = ["is_active", "updated_by", "updated_on"]
        values = [self.isActive, self.sessionUser, getCurrentTimeStamp()]
        unitIdsList  = self.getUnitsOfDivision()
        condition = "unit_id in ({unitIdsList}) and client_id={clientId}".format(
            unitIdsList = ",".join(str(x) for x in unitIdsList), clientId = self.clientId)
        return DatabaseHandler.instance().update(
            self.unitTblName, columns, values, condition)

    def getProfiles(self, clientIds):
        clientIdsList = clientIds.split(",")
        profiles = {}
        for clientId in clientIdsList:
            clientDBName = getClientDatabase(clientId)

            settingsColumns = "contract_from, contract_to, no_of_user_licence,"+\
                              " total_disk_space"

            settingsRows = ClientDatabaseHandler.instance(clientDBName).getData(
                self.clientSettingsTblName, settingsColumns, "1")

            
            userDetailsColumns = "user_id, email_id, employee_name, employee_code, "+\
                                "contact_no, is_admin, unit_code, unit_name,"+\
                                " address"
            userDetailsTables = [ self.clientUserDetails, self.unitTblName]
            userDetailsConditions = [("seating_unit_id","unit_id")]

            rows = ClientDatabaseHandler.instance(clientDBName).getDataFromMultipleTables(
            userDetailsColumns, userDetailsTables, userDetailsConditions, "left join")

            contractFrom = settingsRows[0][0]
            contractTo = settingsRows[0][1]
            noOfUserLicence = settingsRows[0][2]
            fileSpace = settingsRows[0][3]
            usedSpace = 34

            licenceHolders = []
            for row in rows:
                employeeName = None
                unitName = None
                if(row[3] == None):
                    employeeName = row[2]
                else:
                    employeeName = "%s - %s" % (row[3], row[2])

                if row[7] == None:
                    unitName = "-"
                else:
                    unitName =  "%s - %s" % (row[6], row[7])

                licenceHolderDetails = {}
                licenceHolderDetails["user_id"] = row[0]
                licenceHolderDetails["email_id"] = row[1]
                licenceHolderDetails["employee_name"] = employeeName
                licenceHolderDetails["contact_no"] = row[4]
                licenceHolderDetails["is_admin"] = row[5]
                licenceHolderDetails["unit_name"] =unitName
                licenceHolderDetails["address"] = row[8]

                columns = "is_active"
                condition = "user_id='%d'" % int(row[0])
                isActiveRows =DatabaseHandler.instance().getData(
                    self.usersTblName, columns, condition)
                licenceHolderDetails["is_active"] = isActiveRows[0][0]

                licenceHolders.append(licenceHolderDetails)

            profileDetails = {}
            profileDetails["contract_from"] = contractFrom
            profileDetails["contract_to"] = contractTo
            profileDetails["no_of_user_licence"] = noOfUserLicence
            profileDetails["remaining_licence"] = (noOfUserLicence) - len(rows)
            profileDetails["total_disk_space"] = fileSpace
            profileDetails["used_disk_space"] = usedSpace
            profileDetails["licence_holders"] = licenceHolders

            profiles[clientId] = profileDetails

        return profiles

    def getReport(self, countryId, clientId, businessGroupId, 
            legalEntityId, divisionId, unitId, domainIds):
        clientDBName = getClientDatabase(clientId)
        columns = "business_group_id, legal_entity_id, division_id,"+\
                "unit_code, unit_name, geography, address, domain_ids, postal_code"

        condition = "1 "

        if businessGroupId != None:
            condition += " AND business_group_id = '%d'" % businessGroupId
        if legalEntityId != None:
            condition += " AND legal_entity_id = '%d'" % legalEntityId
        if divisionId != None:
            condition += " AND division_id = '%d'" % divisionId
        if unitId != None:
            condition += " AND unit_id = '%d'" % unitId
        if domainIds != None:
            for domainId in domainIds:
                condition += " AND  ( domain_ids LIKE  '%,"+str(domainId)+",%' "+\
                            "or domain_ids LIKE  '%,"+str(domainId)+"' "+\
                            "or domain_ids LIKE  '"+str(domainId)+",%'"+\
                            " or domain_ids LIKE '"+str(domainId)+"') "

        rows = ClientDatabaseHandler.instance(clientDBName).getData(self.unitTblName,
            columns, condition)

        divisionWiseUnitDetails={}

        for row in rows:
            unitDetails = {}
            unitDetails["unit_name"] = "%s - %s" % (row[3], row[4])
            unitDetails["unit_location_and_address"] = "%s - %s" % (
                row[5], row[6])
            unitDetails["domain_ids"] = row[7]
            unitDetails["postal_code"] = row[8]
            divisionId = row[2]
            if divisionId in divisionWiseUnitDetails:
                divisionWiseUnitDetails[divisionId].append(unitDetails)
            else:
                divisionWiseUnitDetails[divisionId] = []
                divisionWiseUnitDetails[divisionId].append(unitDetails)

        return divisionWiseUnitDetails