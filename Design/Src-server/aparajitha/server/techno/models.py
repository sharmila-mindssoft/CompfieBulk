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
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit",
    "SaveClientGroup",
    "SaveClient",
    "GetClientGroups",
    "ChangeClientGroupStatus",
    "UpdateClientGroup",
    "GetClients",
    "ChangeClientStatus",
    "ReactivateUnit"
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
            print "Error : Database Not exists for the client %d" % clientId
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
            # try:
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
        self.businessGroupId = businessGroupId
        self.businessGroupName = businessGroupName
        self.clientId = clientId

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

    @classmethod
    def getClienDatabaseName(self, clientId):
        clientDBName = getClientDatabase(clientId)
        if clientDBName == None:
            print "Error : Database Not exists for the client %d" % clientId
        return clientDBName

    @classmethod
    def getList(self, clientIds):
        businessGroupList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = self.getClienDatabaseName(clientId)
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
        self.legalEntityId = legalEntityId
        self.legalEntityName = legalEntityName
        self.businessGroupId = businessGroupId
        self.clientId = clientId

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

    @classmethod
    def getClienDatabaseName(self, clientId):
        clientDBName = getClientDatabase(clientId)
        if clientDBName == None:
            print "Error : Database Not exists for the client %d" % clientId
        return clientDBName

    @classmethod
    def getList(self, clientIds):
        legalEntitiesList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = self.getClienDatabaseName(clientId)
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
        self.divisionId = divisionId
        self.divisionName = divisionName
        self.legalEntityId = legalEntityId
        self.businessGroupId = businessGroupId
        self.clientId = clientId

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

    @classmethod
    def getClienDatabaseName(self, clientId):
        clientDBName = getClientDatabase(clientId)
        if clientDBName == None:
            print "Error : Database Not exists for the client %d" % clientId
        return clientDBName

    @classmethod
    def getList(self, clientIds):
        divisionsList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = self.getClienDatabaseName(clientId)
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
        return{
            "unit_id": self.unitId,
            "division_id": self.divisionId,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId,
            "client_id"  : self.clientId,
            "unit_name": self.unitName,
            "unit_address": self.address
        }

    @classmethod
    def getClienDatabaseName(self, clientId):
        clientDBName = getClientDatabase(clientId)
        if clientDBName == None:
            print "Error : Database Not exists for the client %d" % clientId
        return clientDBName

    @classmethod
    def getDetailedList(self, clientIds):
        unitList = []

        for index, clientId in enumerate(clientIds.split(",")):
            try:
                clientDBName = self.getClienDatabaseName(clientId)
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
                            industryId, address, postalCode, domainIds, isActive)
                    unitList.append(unit.toDetailedStructure())

            except:
                print "Error: While fetching Division of client id %s" % clientId

        return unitList

class SaveClientGroup(object) :
    clientTblName = "tbl_client_groups"
    clientSettingsTblName = "tbl_client_settings"
    clietConfigurationTblName = "tbl_client_configurations"
    userDetailsTblName = "tbl_user_details"
    clientUserDetailsTblName = "tbl_client_user_details"
    countryTblName = "tbl_countries"
    domainTblName = "tbl_domains"
    userTblName = "tbl_users"
    clientDBName = None

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = int(sessionUser)
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def processRequest(self):
        requestData = self.requestData

        self.groupName = JSONHelper.getString(requestData, "group_name")
        self.countryIds = JSONHelper.getList(requestData, "country_ids")
        self.domainIds = JSONHelper.getList(requestData, "domain_ids")
        self.logo = JSONHelper.getString(requestData, "logo")
        self.contractFrom = JSONHelper.getString(requestData, "contract_from")
        self.contractTo = JSONHelper.getString(requestData, "contract_to")
        self.inchargePersons = JSONHelper.getList(requestData, "incharge_persons")
        self.noOfLicence = JSONHelper.getInt(requestData, "no_of_user_licence")
        self.fileSpace = JSONHelper.getFloat(requestData, "file_space")
        self.isSmsSubscribed = JSONHelper.getInt(requestData, "is_sms_subscribed")
        self.username = JSONHelper.getString(requestData, "email_id")     
        self.dateConfigurations = JSONHelper.getList(requestData, "date_configurations")

        self.clientId = self.generateNewId()

        if self.isDuplicateGroupName():
            self.response = "GroupNameAlreadyExists"
        elif self.saveCredentials() and self.saveGroupCompany() :
            if self.createClientDatabase():
                if self.saveClientDetails():
                    if self.copyBasicData():
                        if self.saveDateConfigurations():
                            if self.saveClientAdminUserDetails():
                                self.response = "SaveClientGroupSuccess"
                            else:
                                print "Error : Saving Client admin user details failed"
                        else:
                            print "Error : Saving date configurations Failed"
                    else:
                        print "Error : Copying Data Failed"
                else:
                    print "Error : Saving client settings failed"
            else:
                print "Error : Creating client database failed"
        else:
            print "Error : Save Group company failed"

        return commonResponseStructure(self.response,{})

    def generateNewId(self) :
        print "inside generateNewId"
        return DatabaseHandler.instance().generateNewId(self.clientTblName, "client_id")

    def isDuplicateGroupName(self):
        print "inside isDuplicateGroupName"
        condition = "group_name ='"+self.groupName+\
                "' AND client_id != '"+str(self.clientId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.clientTblName, condition)     

    def copyBasicData(self):
        print "inside copyBasicData"
        if self.insertCountries() and self.insertDomains():
            return True
    
    def insertCountries(self):
        print "inside insertCountries"
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
        return ClientDatabaseHandler.instance(self.getDatabaseName()).bulkInsert(self.countryTblName,columns,valuesList)

    def insertDomains(self):
        print "inside insertDomains"
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
        return ClientDatabaseHandler.instance(self.getDatabaseName()).bulkInsert(self.domainTblName,columns,valuesList)

    def saveGroupCompany(self):
        print "inside saveGroupCompany"
        columns = "client_id, group_name, incharge_persons,created_on, created_by, updated_on, updated_by"
        valuesList =  [self.clientId, self.groupName, 
                        ",".join(str(x) for x in self.inchargePersons),
                        getCurrentTimeStamp(), self.sessionUser,
                        getCurrentTimeStamp(), self.sessionUser]
        values = listToString(valuesList)

        userColumns = "client_ids"
        userValues = str(self.clientId)
        for inchargePerson in self.inchargePersons:
            condition = " user_id='%d'" % inchargePerson 
            print condition
            DatabaseHandler.instance().append(self.userDetailsTblName,userColumns, userValues, condition)
        print "returning from saveGroupCompany"
        return DatabaseHandler.instance().insert(self.clientTblName,columns,values)

    def saveClientDatabaseMapping(self, clientId, databaseName):
        print "inside saveClientDatabaseMapping"
        clientDatabaseMappingJson = json.load(open(clientDatabaseMappingFilePath))
        try:
            del clientDatabaseMappingJson[str(clientId)]
        except:
            print "Key not exists"
        clientDatabaseMappingJson[str(clientId)] = databaseName
        json.dump(clientDatabaseMappingJson, 
            open(clientDatabaseMappingFilePath,'w'))

    def createClientDatabase(self):
        print "inside createClientDatabase"
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
        print "inside getDatabaseName"
        if self.clientDBName == None:
            self.clientDBName = getClientDatabase(self.clientId)
        return self.clientDBName

    def saveClientDetails(self):
        print "inside saveClientDetails"
        columns = "country_ids ,domain_ids, logo_url, contract_from, contract_to,"+\
                  "no_of_user_licence,total_disk_space, is_sms_subscribed,"+\
                  "  updated_on, updated_by"
        print "before converting "+self.contractFrom
        dt = stringToDatetime(self.contractFrom)
        print "stringToDatetime(self.contractFrom):{dt}".format(dt= dt)
        ts = datetimeToTimestamp(stringToDatetime(self.contractFrom))
        print "datetimeToTimestamp(stringToDatetime(self.contractFrom)):{ts}".format(ts= ts)
        self.contractFrom = datetimeToTimestamp(stringToDatetime(self.contractFrom))
        self.contractTo = datetimeToTimestamp(stringToDatetime(self.contractTo))
        valuesList =  [ ",".join(str(x) for x in self.countryIds),
                         ",".join(str(x) for x in self.countryIds),
                        self.logo, self.contractFrom, self.contractTo, self.noOfLicence, 
                        self.fileSpace, self.isSmsSubscribed, getCurrentTimeStamp(), 
                        self.sessionUser]
        values = listToString(valuesList)
        return ClientDatabaseHandler.instance(self.getDatabaseName()).insert(self.clientSettingsTblName,columns,values)

    def saveDateConfigurations(self):
        print "inside saveDateConfigurations"
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
        print "inside saveCredentials"
        password = generatePassword()
        user = User(None, self.username, None, self.groupName+" Admin", "",None,
             " ", "Admin", self.countryIds,self.domainIds, self.clientId, None)

        if user.isDuplicateEmail():
            self.response = "UsernameAlreadyExists"
        elif user.saveAdmin(self.sessionUser):
            return True
        else:
            return False

    def getUserId(self):
        print "inside getUserId"
        columns = "user_id"
        condition = " username='%s'" % self.username
        rows = DatabaseHandler.instance().getData(self.userTblName, columns, condition)
        return rows[0][0]

    def saveClientAdminUserDetails(self):
        print "inside saveClientAdminUserDetails"
        columns = "user_id, email_id, employee_name, country_ids, domain_ids, is_admin, "+\
                    "is_service_provider, created_by, created_on, updated_by, updated_on"
        self.userId = self.getUserId()
        valuesList = [self.userId, self.username, "Admin" , ",".join(str(x) for x in self.countryIds), 
                    ",".join(str(x) for x in self.domainIds),1,0, self.sessionUser, 
                    getCurrentTimeStamp(), self.sessionUser, getCurrentTimeStamp()]
        values = listToString(valuesList)
        return ClientDatabaseHandler.instance(self.getDatabaseName()).insert(self.clientUserDetailsTblName, columns, values)

class GetClientGroups(object):
    responseData = {}
    def __init__(self):
        domainList = DomainList.getDomainList()
        print "Got Domain List"
        countryList = CountryList.getCountryList()
        print "Got Country List"
        userList = User.getList()
        print "Got User List"
        clientList = GroupCompany.getDetailedClientList()
        print "Got Client List"

        self.responseData["domains"] = domainList
        self.responseData["countries"] = countryList
        self.responseData["users"] = userList
        self.responseData["client_list"] = clientList

    def getList(self):
        return commonResponseStructure("GetClientGroupsSuccess",self.responseData)

class ChangeClientGroupStatus(object):
    clientTblName = "tbl_client_groups"

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = sessionUser
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def updateStatus(self):
        requestData = self.requestData

        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")

        if self.isValidClientId():
            columns = ["is_active","updated_on", "updated_by"]
            values = [self.isActive, getCurrentTimeStamp(), self.sessionUser]
            condition = " client_id='%d'" % self.clientId
            if DatabaseHandler.instance().update(self.clientTblName, columns, values, condition):
                return commonResponseStructure("ChangeClientGroupStatusSuccess",{})
            else:
                print "Error :  Updating Status Failed"
        else:
            return commonResponseStructure("InvalidClientId",{})

    def isValidClientId(self):
        columns = "count(*)"
        condition = "client_id='%d'" % self.clientId
        rows = DatabaseHandler.instance().getData(self.clientTblName, columns, condition)
        if rows[0][0] == 1:
            return True
        else:
            return False

class UpdateClientGroup(object):
    clientTblName = "tbl_client_groups"
    clientSettingsTblName = "tbl_client_settings"
    clietConfigurationTblName = "tbl_client_configurations"
    userDetailsTblName = "tbl_user_details"
    clientUserDetailsTblName = "tbl_client_user_details"
    countryTblName = "tbl_countries"
    domainTblName = "tbl_domains"
    userTblName = "tbl_users"
    clientDBName = None

    def __init__(self, requestData, sessionUser) :
        print "initializing updateClientGroup"
        self.requestData = requestData
        self.sessionUser = sessionUser
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def processRequest(self):   
        print "Processing updateClientGroup request"
        requestData = self.requestData

        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.groupName = JSONHelper.getString(requestData, "group_name")
        self.countryIds = JSONHelper.getList(requestData, "country_ids")
        self.domainIds = JSONHelper.getList(requestData, "domain_ids")
        self.logo = JSONHelper.getString(requestData, "logo")
        self.contractFrom = JSONHelper.getString(requestData, "contract_from")
        self.contractTo = JSONHelper.getString(requestData, "contract_to")
        self.inchargePersons = JSONHelper.getList(requestData, "incharge_persons")
        self.noOfLicence = JSONHelper.getInt(requestData, "no_of_user_licence")
        self.fileSpace = JSONHelper.getFloat(requestData, "file_space")
        self.isSmsSubscribed = JSONHelper.getInt(requestData, "is_sms_subscribed")
        self.dateConfigurations = JSONHelper.getList(requestData, "date_configurations")

        if not self.isClientExists():
            self.response = "InvalidClientId"
        elif self.isDuplicateGroupName():
            self.response = "GroupNameAlreadyExists"
        elif self.updateGroupCompany() :
            if self.copyBasicData():
                if self.updateClientDetails():
                    if self.updateDateConfigurations():
                        if self.updateClientAdminUserDetails():
                                self.response = "UpdateClientGroupSuccess"
                        else:
                            print "Error : Saving Client admin user details failed"
                    else:
                        print "Error : Saving date configurations Failed"
                else:
                    print "Error : Saving client settings failed"
            else:
                print "Error : Copying Data Failed"
        else:
            print "Error : Save Group company failed"

        return commonResponseStructure(self.response,{})

    def isClientExists(self):
        condition = " client_id = '%d'" % self.clientId
        return DatabaseHandler.instance().isAlreadyExists(self.clientTblName, condition) 

    def isDuplicateGroupName(self):
        condition = "group_name ='"+self.groupName+\
                "' AND client_id != '"+str(self.clientId)+"'"
        return DatabaseHandler.instance().isAlreadyExists(self.clientTblName, condition) 

    def getOldInchargePersons(self):
        columns = "incharge_persons"
        condition = "client_id='%d'" % self.clientId
        rows = []
        try:
            rows = DatabaseHandler.instance().getData(self.clientTblName, columns, condition)
            return rows[0][0].split(",")
        except:
            print "Error : Incharge Persons not exists for client id %d " % self.clientId

    def getDatabaseName(self):
        if self.clientDBName == None:
            self.clientDBName = getClientDatabase(self.clientId)
        return self.clientDBName

    def updateGroupCompany(self):
        oldInchargePersons = self.getOldInchargePersons()
        
        existingInchargePersons = []
        newInchargePersons = []
        removedInchargePersons = []
        print "oldInchargePersons: {oldInchargePersons}".format(
            oldInchargePersons =oldInchargePersons)
        for inchargePerson in self.inchargePersons:
            if str(inchargePerson) in oldInchargePersons:
                existingInchargePersons.append(inchargePerson)
            else:
                newInchargePersons.append(inchargePerson)

        for oldInchargePerson in oldInchargePersons:
            if int(oldInchargePerson) not in self.inchargePersons:
                removedInchargePersons.append(int(oldInchargePerson))

        print "existingInchargePersons: {existingInchargePersons}".format(
            existingInchargePersons =existingInchargePersons)
        print "newInchargePersons: {newInchargePersons}".format(
            newInchargePersons =newInchargePersons)
        print "removedInchargePersons:{removedInchargePersons}".format(
            removedInchargePersons =removedInchargePersons)
        for newInchargePerson in newInchargePersons:
            try:
                condition = " user_id='%d'" % newInchargePerson 
                columns = "client_ids"
                values = str(self.clientId)
                DatabaseHandler.instance().append(self.userDetailsTblName, columns, values, condition)
            except:
                self.response = "InvalidInchargePersonId"
                return False

        for removedInchargePerson in removedInchargePersons:
            columns = "client_ids"
            condition = "user_id='%s'" % removedInchargePerson
            rows = DatabaseHandler.instance().getData(self.userDetailsTblName, columns, condition)
            clientIds = rows[0][0].split(",")
            print "clientIds:{clientIds}".format(clientIds =clientIds)
            if str(self.clientId) in clientIds:
                clientIds.remove(str(self.clientId))
            updateColumns = ["client_ids"]
            updateValues = [",".join(str(x) for x in clientIds)]
            DatabaseHandler.instance().update(self.userDetailsTblName, updateColumns, 
                                            updateValues, condition)

        columnsList = ["group_name", "incharge_persons", "updated_on", "updated_by"]
        valuesList =  [ self.groupName, ",".join(str(x) for x in self.inchargePersons),
                        getCurrentTimeStamp(), self.sessionUser]
        condition = "client_id='%d'" % self.clientId
        return DatabaseHandler.instance().update(self.clientTblName, columnsList, valuesList, condition)

    def updateClientDetails(self):
        columnsList = ["country_ids", "domain_ids", "logo_url", "contract_from", "contract_to",
        "no_of_user_licence","total_disk_space", "is_sms_subscribed","updated_on", "updated_by"]
        self.contractFrom = datetimeToTimestamp(stringToDatetime(self.contractFrom))
        self.contractTo = datetimeToTimestamp(stringToDatetime(self.contractTo))
        valuesList =  [ ",".join(str(x) for x in self.countryIds),
                         ",".join(str(x) for x in self.domainIds),
                        self.logo, self.contractFrom, self.contractTo, self.noOfLicence, 
                        self.fileSpace, self.isSmsSubscribed, getCurrentTimeStamp(), 
                        self.sessionUser]
        clientDBName = self.getDatabaseName()
        return ClientDatabaseHandler.instance(clientDBName).update(self.clientSettingsTblName,
            columnsList, valuesList, "1")

    def copyBasicData(self):
        for countryId in self.countryIds:
            condition = "country_id='%d'" % countryId
            if DatabaseHandler.instance().isAlreadyExists(self.countryTblName, condition):
                continue
            else:
                self.response = "InvalidCountryId"
                return
        for domainId in self.domainIds:
            condition = "domain_id ='%d'" % domainId
            if DatabaseHandler.instance().isAlreadyExists(self.domainTblName, condition):
                continue
            else:
                self.response = "InvalidDomainId"
                return
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
        updateColumns = ["country_name"]
        return ClientDatabaseHandler.instance(self.getDatabaseName()).onDuplicateKeyUpdate(
                self.countryTblName,columns,valuesList, updateColumns)

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

        updateColumns = ["domain_name"]
        return ClientDatabaseHandler.instance(
                        self.getDatabaseName()).onDuplicateKeyUpdate(
                        self.domainTblName,columns,valuesList, updateColumns)

    def updateDateConfigurations(self):
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

        updateColums = ["period_from", "period_to"]
        return ClientDatabaseHandler.instance(
                            self.getDatabaseName()).onDuplicateKeyUpdate(
                            self.clietConfigurationTblName,columns,valuesList, updateColums)

    def getClientAdminUserId(self):
        userId = None
        columns = "user_id"
        condition = " is_admin = 1"
        rows = []

        try : 
            clientDBName = self.getDatabaseName()
            rows = ClientDatabaseHandler.instance(clientDBName).getData(self.clientUserDetailsTblName,
                    columns, condition)
        except:
            print "Error : Client Database Not exists for the client %d" % self.clientId

        if len(rows) < 1:
            print "Error :User details not found for client admin"
        else:
            userId = int(rows[0][0])
        
        return userId


    def updateClientAdminUserDetails(self):
        columnsList = [  "country_ids", "domain_ids", "updated_by", "updated_on"]
        valuesList = [ ",".join(str(x) for x in self.countryIds), 
                    ",".join(str(x) for x in self.domainIds),1,0, 
                    self.sessionUser, getCurrentTimeStamp()]

        condition = "user_id= '%d'" % self.getClientAdminUserId()

        return ClientDatabaseHandler.instance(
                        self.getDatabaseName()).update( 
                        self.clientUserDetailsTblName, columnsList, valuesList, condition)   

class GetClients(object):
    userDetailsTblName = "tbl_user_details"

    responseData = {}

    def __init__(self,  sessionUser) :
        self.sessionUser = sessionUser
        countryList = []
        groupCompanyList = []
        businessGroupList = []
        legalEntityList = []
        divisionList = []
        unitList = []
        geographyLevelList = []
        industryList = []
        geographyList = []

        countryList = CountryList.getCountryList()
        domainList = DomainList.getDomainList()
        geographyLevelList = GeographyLevelList.getCountryWiseList()
        industryList = IndustryList.getList()
        geographyList = Geography.getCountryWiseList()

        clientIds = self.getClientIdsOfUser()
        
        if clientIds ==  None:
            print "Error : User is not responsible for any client"
        else:
            groupCompanyList = GroupCompany.getClientList(clientIds)
            businessGroupList = BusinessGroup.getList(clientIds)
            legalEntityList = LegalEntity.getList(clientIds)
            divisionList = Division.getList(clientIds)
            unitList = Unit.getDetailedList(clientIds)
            
        self.responseData["countries"] = countryList
        self.responseData["domains"] = domainList
        self.responseData["geography_levels"] = geographyLevelList
        self.responseData["geographies"] =geographyList
        self.responseData["industries"] = industryList
        self.responseData["group_companies"] = groupCompanyList
        self.responseData["business_groups"] = businessGroupList
        self.responseData["legal_entities"] = legalEntityList
        self.responseData["divisions"] = divisionList
        self.responseData["units"] = unitList

        

    def getClientIdsOfUser(self):
        columns = "client_ids"
        condition = "user_id = '%d'" % self.sessionUser
        rows = DatabaseHandler.instance().getData(self.userDetailsTblName, columns, condition)
        return rows[0][0]

    def getList(self):
        return commonResponseStructure("GetClientsSuccess",self.responseData)

class SaveClient(object):
    businessGroupTblName = "tbl_business_groups"
    legalEntityTblName = "tbl_legal_entities"
    divisionTblName = "tbl_divisions"
    unitTblName = "tbl_units"
    clientDBName = None
    responseData = None

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = int(sessionUser)

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def processRequest(self):
        requestData = self.requestData
        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.businessGroup = JSONHelper.getDict(requestData, "business_group")
        self.legalEntity = JSONHelper.getDict(requestData, "legal_entity")
        self.division = JSONHelper.getDict(requestData, "division")
        self.countryWiseUnits = JSONHelper.getList(requestData, "country_wise_units")


        assertType(self.businessGroup, DictType)
        assertType(self.legalEntity, DictType)
        assertType(self.division, DictType)
        assertType(self.countryWiseUnits, ListType)

        if self.processBusinessGroup():
            if self.processLegalEntity():
                if self.processDivision():
                    if self.processUnit():
                        if self.saveBusinessGroup(self.businessGroupId,
                             self.businessGroupName) and self.saveLegalEntity(
                            self.legalEntityId, self.legalEntityName) and self.saveDivision(
                            self.divisionId, self.divisionName) and self.saveUnit():
                            self.responseData = commonResponseStructure("SaveClientSuccess", {})
                    else:
                         print "Unit name already Exists"
                else:
                    print "Division name already Exists"
            else:
                print "Legal Entity name already Exists"
        else:
            print "Business group name already Exists"

        return self.responseData

    def getDatabaseName(self):
        if self.clientDBName == None:
            self.clientDBName = getClientDatabase(self.clientId)
        return self.clientDBName

    def generateNewId(self, idType) :
        if idType == "businessGroup":
            return ClientDatabaseHandler.instance(self.getDatabaseName()).generateNewId(
                self.businessGroupTblName, "business_group_id")
        elif idType == "legalEntity":
            return ClientDatabaseHandler.instance(self.getDatabaseName()).generateNewId(
                self.legalEntityTblName, "legal_entity_id")
        elif idType == "division":
            return ClientDatabaseHandler.instance(self.getDatabaseName()).generateNewId(
                self.divisionTblName, "division_id")
        elif idType == "unit":
            return ClientDatabaseHandler.instance(self.getDatabaseName()).generateNewId(
                self.unitTblName, "unit_id")

    def isDuplicate(self, value, valueType):
        tableName = None
        condition = None
        if valueType == "businessGroup":
            tableName = self.businessGroupTblName
            condition = "business_group_name= '%s' and business_group_id != '%d'" % (value, 
                self.businessGroupId)
        elif valueType == "legalEntity":
            tableName = self.legalEntityTblName
            condition = "legal_entity_name= '%s' and legal_entity_id != '%d'" % (value, 
                self.legalEntityId)
        elif valueType == "division":
            tableName = self.divisionTblName
            condition = "division_name= '%s'  and division_id != '%d'" % (value, 
                self.divisionId)
        elif valueType == "unitName":
            tableName = self.unitTblName
            condition = "unit_name= '%s' and unit_id != '%d'" % (value, 
                self.unitId)
        elif valueType == "unitCode":
            tableName = self.unitTblName
            condition = "unit_code= '%s' and unit_id != '%d'" % (value, 
                self.unitId)

        return ClientDatabaseHandler.instance(self.getDatabaseName()).isAlreadyExists(
                tableName, condition)

    def processBusinessGroup(self):
        print "Entered into Process Business group"
        try:
            self.businessGroupId = JSONHelper.getInt(self.businessGroup, "business_group_id")
        except:
            self.businessGroupId = self.generateNewId("businessGroup")
        self.businessGroupName = JSONHelper.getString(self.businessGroup, "business_group_name")

        assertType(self.businessGroupName, StringType)

        if self.isDuplicate(self.businessGroupName, "businessGroup"):
            self.responseData = commonResponseStructure("BusinessGroupNameAlreadyExists", {})
            return False
        else:
            return True

    def saveBusinessGroup(self, businessGroupId, businessGroupName):
        print "Entered into Save Business group"
        valuesList = []
        columns = "business_group_id, business_group_name, created_on, created_by,"+\
                "updated_on, updated_by"
        valuesTuple = (self.businessGroupId, businessGroupName, getCurrentTimeStamp(), 
                        self.sessionUser, getCurrentTimeStamp(), self.sessionUser)
        valuesList.append(valuesTuple)
        updateColumnsList = ["business_group_name", "updated_on", "updated_by"]
        return ClientDatabaseHandler.instance(self.getDatabaseName()).onDuplicateKeyUpdate(
            self.businessGroupTblName, columns, valuesList, updateColumnsList)

    def processLegalEntity(self):
        print "Entered into processLegalEntity"
        try:
            self.legalEntityId = JSONHelper.getInt(self.legalEntity, "legal_entity_id")
        except:
            self.legalEntityId = self.generateNewId("legalEntity")
        self.legalEntityName = JSONHelper.getString(self.legalEntity, "legal_entity_name")

        assertType(self.legalEntityName, StringType)

        if self.isDuplicate(self.legalEntityName, "legalEntity"):
            self.responseData = commonResponseStructure("LegalEntityNameAlreadyExists", {})
            return False
        else:
            return True

    def saveLegalEntity(self, legalEntityId, legalEntityName):
        print "Entered into saveLegalEntity"
        columns = "legal_entity_id, legal_entity_name, business_group_id,"+\
                  "created_on, created_by, updated_on, updated_by"
        valuesTuple = (legalEntityId, legalEntityName, self.businessGroupId, 
                        getCurrentTimeStamp(), self.sessionUser, 
                        getCurrentTimeStamp(), self.sessionUser)
        valuesList =  []
        valuesList.append(valuesTuple)
        updateColumnsList = ["legal_entity_name", "updated_on", "updated_by"]
        # values = listToString(valuesList)
        return ClientDatabaseHandler.instance(self.getDatabaseName()).onDuplicateKeyUpdate(
            self.legalEntityTblName, columns, valuesList, updateColumnsList)

    def processDivision(self):
        print "Entered into processDivision"
        try:
            self.divisionId = JSONHelper.getInt(self.division, "division_id")
        except:
            self.divisionId = self.generateNewId("division")
        self.divisionName = JSONHelper.getString(self.division, "division_name")

        assertType(self.divisionName, StringType)

        if self.isDuplicate(self.divisionName, "division"):
            self.responseData = commonResponseStructure("DivisionNameAlreadyExists", {})
            return False
        else:
            return True

    def saveDivision(self, divisionId, divisionName):
        print "Entered into saveDivision"
        columns = "division_id, division_name, legal_entity_id, business_group_id,"+\
                  "created_on, created_by, updated_on, updated_by"
        valuesTuple = (self.divisionId, divisionName, self.legalEntityId, 
                        self.businessGroupId, getCurrentTimeStamp(), self.sessionUser, 
                        getCurrentTimeStamp(), self.sessionUser)          
        valuesList =  []
        valuesList.append(valuesTuple)
        updateColumnsList = ["division_name", "updated_on", "updated_by"]
        # values = listToString(valuesList)
        return ClientDatabaseHandler.instance(self.getDatabaseName()).onDuplicateKeyUpdate(
            self.divisionTblName, columns, valuesList, updateColumnsList)

    def processUnit(self):
        print "Entered into process Unit"
        self.clientValuesList = []
        self.knowledgeValueslist = []

        for country in self.countryWiseUnits:
            countryId = JSONHelper.getInt(country,"country_id")
            units = JSONHelper.getList(country, "units")
            for unit in units:
                try:
                    self.unitId = JSONHelper.getInt(unit, "unit_id")
                except:
                    self.unitId = self.generateNewId("unit")
                unitCode = JSONHelper.getString(unit, "unit_code")
                unitName = JSONHelper.getString(unit, "unit_name")
                address = JSONHelper.getString(unit, "unit_address")
                postalCode = JSONHelper.getString(unit, "postal_code")
                geographyId = JSONHelper.getInt(unit, "geography_id")
                geography = JSONHelper.getString(unit, "unit_location")
                industryId = JSONHelper.getInt(unit, "industry_id")
                industryName = JSONHelper.getString(unit, "industry_name")
                domainIds = JSONHelper.getList(unit, "domain_ids")
                if self.isDuplicate( unitCode, "unitCode"):
                    self.responseData = commonResponseStructure("UnitCodeAlreadyExists", {})
                    return False
                elif self.isDuplicate( unitName, "unitName"):
                    self.responseData = commonResponseStructure("UnitNameAlreadyExists", {})
                    return False
                else:
                    knowledgeValuesTuple = (self.clientId, self.unitId, countryId, geographyId,
                                            unitCode, unitName, industryId, 
                                            int(self.sessionUser), getCurrentTimeStamp(), 
                                            int(self.sessionUser), getCurrentTimeStamp())
                    self.knowledgeValueslist.append(knowledgeValuesTuple)
                    clientValuesTuple = ( self.unitId, self.divisionId, self.legalEntityId,
                                        self.businessGroupId, countryId, geography, unitCode,
                                        unitName, industryName, address, postalCode, 
                                        ",".join(str(x) for x in domainIds))
                    self.clientValuesList.append(clientValuesTuple)
        
        return True

    def saveUnit(self):
        print "Entering into save Unit"
        clientDbColumns = "unit_id, division_id, legal_entity_id, business_group_id,"+\
                        " country_id, geography, unit_code, unit_name, industry_name,"+\
                        " address, postal_code, domain_ids"
        knowledgeDbColumns = "client_id, unit_id, country_id, geography_id, unit_code,"+\
                            " unit_name, industry_id, created_by, created_on,"+\
                            " updated_by, updated_on"
        knowledgeUpdateColumnsList = ["geography_id", "unit_code", "unit_name", "industry_id",
        "updated_by", "updated_on"]
        clientUpdateColumnsList = ["geography", "unit_code", "unit_name", "industry_name",
        "address", "postal_code", "domain_ids"]
        if DatabaseHandler.instance().onDuplicateKeyUpdate(
                        self.unitTblName, knowledgeDbColumns, self.knowledgeValueslist, 
                        knowledgeUpdateColumnsList):
            print "Inserted in Knowledge Database"
            return ClientDatabaseHandler.instance(self.getDatabaseName()).onDuplicateKeyUpdate(
                self.unitTblName, clientDbColumns, self.clientValuesList, clientUpdateColumnsList)

class ChangeClientStatus(object):
    unitTblName = "tbl_units"

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = int(sessionUser)

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def processRequest(self):
        requestData = self.requestData
        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.divisionId = JSONHelper.getInt(requestData, "division_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.deactivateUnitsInClientDB():
            if self.deactivateUnitsInKnowledgeDB():
                return commonResponseStructure("ChangeClientStatusSuccess",{})
            else:
                print "Error: Failed to deactivate units in knowledge database"
        else:
            print "Error: Failed to deactivate units in client database"


    def deactivateUnitsInClientDB(self):
        columns = ["is_active"]
        values = [self.isActive]
        condition = "division_id='%d'" % self.divisionId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.unitTblName, columns, values, condition)

    def getUnits(self):
        unitIdsList = []
        columns = "unit_id"
        condition = "division_id='%d'" % self.divisionId
        rows = ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).getData(self.unitTblName, columns, condition)
        for row in rows:
            unitIdsList.append(row[0])

        return unitIdsList

    def deactivateUnitsInKnowledgeDB(self):
        columns = ["is_active", "updated_by", "updated_on"]
        values = [self.isActive, self.sessionUser, getCurrentTimeStamp()]
        unitIdsList  = self.getUnits()
        condition = "unit_id in ({unitIdsList}) and client_id={clientId}".format(
            unitIdsList = ",".join(str(x) for x in unitIdsList), clientId = self.clientId)
        return DatabaseHandler.instance().update(
            self.unitTblName, columns, values, condition)

class ReactivateUnit(object):
    unitTblName = "tbl_units"
    userTblName = "tbl_users"

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = int(sessionUser)

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def processRequest(self):
        requestData = self.requestData
        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.unitId = JSONHelper.getInt(requestData, "unit_id")
        self.password = JSONHelper.getString(requestData, "password")
        if self.verifyPassword():
            if self.activateUnit():
                return commonResponseStructure("ReactivateUnitSuccess", {})
            else:
                print "Error: Failed to activate unit"
        else:
            return commonResponseStructure("InvalidPassword", {})

    def verifyPassword(self):
        encryptedPassword = encrypt(self.password)
        columns = "count(*)"
        condition = "password='%s' and user_id='%d'" % (encryptedPassword, self.sessionUser)
        rows = DatabaseHandler.instance().getData(self.userTblName, columns, condition)
        
        if(int(rows[0][0]) <= 0):
            return False
        else:
            return True

    def activateUnit(self):
        if self.activateUnitInClientDB():
            if self.activateUnitInKnowledgeDB():
                return True
            else:
                return False
        else:
            return False

    def activateUnitInClientDB(self):
        columns = ["is_active"]
        values = [1]
        condition = "unit_id ='%d'" % self.unitId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.unitTblName, columns, values, condition)

    def activateUnitInKnowledgeDB(self):    
        columns = ["is_active", "updated_by", "updated_on"]
        values = [1, self.sessionUser, getCurrentTimeStamp()]
        condition = "unit_id = {unitId} and client_id={clientId}".format(
            unitId = self.unitId, clientId = self.clientId)
        return DatabaseHandler.instance().update(
            self.unitTblName, columns, values, condition)





        