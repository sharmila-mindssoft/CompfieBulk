from types import *
import json
import re
import os

from aparajitha.server.constants import ROOT_PATH
from aparajitha.server.databasehandler import DatabaseHandler 
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler 
from aparajitha.server.admin.models import User
from aparajitha.server.knowledge.models import DomainList, CountryList, GeographyLevelList
from aparajitha.server.knowledge.models import IndustryList, Geography, GeographyAPI
from aparajitha.server.common import *
from models import *

__all__ = [
    "ClientGroupController",
    "ClientController",
    "ClientProfile"
]
clientDatabaseMappingFilePath = os.path.join(ROOT_PATH, 
    "Src-client/files/desktop/common/clientdatabase/clientdatabasemapping.txt")

class ClientGroupController(object) :
    clientTblName = "tbl_client_groups"
    clientSettingsTblName = "tbl_client_settings"
    clietConfigurationTblName = "tbl_client_configurations"
    userDetailsTblName = "tbl_user_details"
    clientUserDetailsTblName = "tbl_client_user_details"
    countryTblName = "tbl_countries"
    domainTblName = "tbl_domains"
    userTblName = "tbl_users"
    clientDBName = None

    def getClientGroups(self):
        responseData = {}
        domainList = DomainList.getDomainList()
        countryList = CountryList.getCountryList()
        userList = User.getList()
        clientList = GroupCompany.getDetailedClientList()

        responseData["domains"] = domainList
        responseData["countries"] = countryList
        responseData["users"] = userList
        responseData["client_list"] = clientList

        return commonResponseStructure("GetClientGroupsSuccess",responseData)

    def saveClientGroup(self, requestData, sessionUser):
        self.sessionUser = int(sessionUser)
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

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

    def updateClientGroup(self, requestData, sessionUser):   
        self.sessionUser = sessionUser
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

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
                    if self.saveDateConfigurations():
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

    def changeClientGroupStatus(self, requestData, sessionUser):
        self.sessionUser = sessionUser
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")

        if self.isClientExists():
            columns = ["is_active","updated_on", "updated_by"]
            values = [self.isActive, getCurrentTimeStamp(), self.sessionUser]
            condition = " client_id='%d'" % self.clientId
            if DatabaseHandler.instance().update(self.clientTblName, columns, values, condition):
                return commonResponseStructure("ChangeClientGroupStatusSuccess",{})
            else:
                print "Error :  Updating Status Failed"
        else:
            return commonResponseStructure("InvalidClientId",{})

    def generateNewId(self) :
        return DatabaseHandler.instance().generateNewId(self.clientTblName, "client_id")

    def isDuplicateGroupName(self):
        condition = "group_name ='%s' AND client_id != '%d'" % (self.groupName, self.clientId)
        return DatabaseHandler.instance().isAlreadyExists(self.clientTblName, condition)     
    
    def copyBasicData(self):
        for countryId in self.countryIds:
            condition = "country_id='%d'" % countryId
            if DatabaseHandler.instance().isAlreadyExists(self.countryTblName, condition):
                continue
            else:
                self.response = "InvalidCountryId"
                return False
        for domainId in self.domainIds:
            condition = "domain_id ='%d'" % domainId
            if DatabaseHandler.instance().isAlreadyExists(self.domainTblName, condition):
                continue
            else:
                self.response = "InvalidDomainId"
                return False
        if self.insertCountries() and self.insertDomains():
            return True

    def insertCountries(self):
        valuesList = []
        countryIdsStrVal = ",".join(str(x) for x in self.countryIds)
        condition = "country_id in (%s)" % countryIdsStrVal
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
        condition = "domain_id in (%s)" % domainIdsStrVal
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

    def saveGroupCompany(self):
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
            DatabaseHandler.instance().append(self.userDetailsTblName,userColumns, userValues, condition)
        return DatabaseHandler.instance().insert(self.clientTblName,columns,values)

    def saveClientDatabaseMapping(self, clientId, databaseName):
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
        if self.clientDBName == None:
            self.clientDBName = getClientDatabase(self.clientId)
        return self.clientDBName

    def saveClientDetails(self):
        columns = "country_ids ,domain_ids, logo_url, contract_from, contract_to,"+\
                  "no_of_user_licence,total_disk_space, is_sms_subscribed,"+\
                  "  updated_on, updated_by"
        dt = stringToDatetime(self.contractFrom)
        ts = datetimeToTimestamp(stringToDatetime(self.contractFrom))
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
        columns = "user_id"
        condition = " username='%s'" % self.username
        rows = DatabaseHandler.instance().getData(self.userTblName, columns, condition)
        return rows[0][0]

    def saveClientAdminUserDetails(self):
        columns = "user_id, email_id, employee_name, country_ids, domain_ids, is_admin, "+\
                    "is_service_provider, created_by, created_on, updated_by, updated_on"
        self.userId = self.getUserId()
        valuesList = [self.userId, self.username, "Admin" , ",".join(str(x) for x in self.countryIds), 
                    ",".join(str(x) for x in self.domainIds),1,0, self.sessionUser, 
                    getCurrentTimeStamp(), self.sessionUser, getCurrentTimeStamp()]
        values = listToString(valuesList)

        return ClientDatabaseHandler.instance(self.getDatabaseName()).insert(
            self.clientUserDetailsTblName, columns, values)

    def isClientExists(self):
        condition = " client_id = '%d'" % self.clientId
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

    def updateGroupCompany(self):
        oldInchargePersons = self.getOldInchargePersons()
        
        existingInchargePersons = []
        newInchargePersons = []
        removedInchargePersons = []
        for inchargePerson in self.inchargePersons:
            if str(inchargePerson) in oldInchargePersons:
                existingInchargePersons.append(inchargePerson)
            else:
                newInchargePersons.append(inchargePerson)

        for oldInchargePerson in oldInchargePersons:
            if int(oldInchargePerson) not in self.inchargePersons:
                removedInchargePersons.append(int(oldInchargePerson))

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

    def saveClient(self, requestData, sessionUser):
        self.sessionUser = int(sessionUser)

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

        self.clientId = JSONHelper.getInt(requestData, "client_id")
        self.businessGroup = JSONHelper.getDict(requestData, "business_group")
        self.legalEntity = JSONHelper.getDict(requestData, "legal_entity")
        self.division = JSONHelper.getDict(requestData, "division")
        self.countryWiseUnits = JSONHelper.getList(requestData, "country_wise_units")


        assertType(self.businessGroup, DictType)
        assertType(self.legalEntity, DictType)
        assertType(self.division, DictType)
        assertType(self.countryWiseUnits, ListType)

        if self.processRequest():
            client = Client()
            if client.save(self.businessGroupObj, self.legalEntityObj,
                self.divisionObj, self.unitObjList, self.sessionUser):
               self.responseData = commonResponseStructure("SaveClientSuccess", {}) 
            else:
                print "Error: Failed to save client"
        else:
            print "Error : Save Client request validation failed"

        return self.responseData

    def processRequest(self):
        try:
            self.businessGroupId = JSONHelper.getInt(
                                    self.businessGroup, "business_group_id")
        except:
            self.businessGroupId = None
        try:
            self.legalEntityId = JSONHelper.getInt(
                                    self.legalEntity, "legal_entity_id")
        except:
            self.legalEntityId = None
        try:
            self.divisionId = JSONHelper.getInt(self.division, "division_id")
        except:
            self.divisionId = None

        self.businessGroupName = JSONHelper.getString(
                                    self.businessGroup, "business_group_name")
        self.legalEntityName = JSONHelper.getString(
                                    self.legalEntity, "legal_entity_name")
        self.divisionName = JSONHelper.getString(self.division, "division_name")

        
        self.businessGroupObj = BusinessGroup(self.businessGroupId,
                                    self.businessGroupName, self.clientId)  
        self.legalEntityObj = LegalEntity(self.legalEntityId, 
                                self.legalEntityName, 
                                self.businessGroupObj.businessGroupId, 
                                self.clientId)
        self.divisionObj = Division(self.divisionId, self.divisionName, 
                                self.legalEntityObj.legalEntityId, 
                                self.businessGroupObj.businessGroupId, 
                                self.clientId)

        if self.businessGroupObj.isDuplicate():
            self.responseData = commonResponseStructure("BusinessGroupNameAlreadyExists", {})
            return False
        elif self.legalEntityObj.isDuplicate():
            self.responseData = commonResponseStructure("LegalEntityNameAlreadyExists", {})
            return False
        elif self.divisionObj.isDuplicate():
            self.responseData = commonResponseStructure("DivisionNameAlreadyExists", {})
            return False

        if self.businessGroupId != None:
            if self.businessGroupObj.isIdInvalid():
                self.responseData = commonResponseStructure("InvalidBusinessGroupId",{})
                return False
        elif self.legalEntityId != None:
            if self.legalEntityObj.isIdInvalid():
                self.responseData = commonResponseStructure("InvalidLegalEntityId",{})
                return False
        elif self.divisionId != None:
            if self.divisionObj.isIdInvalid():
                self.responseData = commonResponseStructure("InvalidDivisionId",{})
                return False

        for country in self.countryWiseUnits:
                
            countryId = JSONHelper.getInt(country,"country_id")
            units = JSONHelper.getList(country, "units")
            print units
            for unit in units:
                try:
                    self.unitId = JSONHelper.getInt(unit, "unit_id")
                except:
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
                               self.divisionObj.divisionId,
                               self.legalEntityObj.legalEntityId, 
                                self.businessGroupObj.businessGroupId, 
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

        