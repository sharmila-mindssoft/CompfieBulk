from types import *
import json
import re
import os

from aparajitha.server.constants import ROOT_PATH
from aparajitha.server.databasehandler import DatabaseHandler 
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler 
from aparajitha.server.admin.models import User
from aparajitha.server.knowledge.models import DomainList, CountryList
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
    "UpdateClientGroup"
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
        assertType(self.contractFrom, LongType)
        assertType(self.contractTo, LongType)
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

    @classmethod
    def getClientUsername(self, clientId):
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
        try : 
            clientDBName = self.getClienDatabaseName(clientId)
            settingsRows = ClientDatabaseHandler.instance(clientDBName).getData(self.clientSettingsTblName,
                clientSettingsColumns, "1")
        except:
            print "Error : Client Database Not exists for client %d" % clientId

        try :
            countryIds = settingsRows[0][0].split(",")
            domainIds = settingsRows[0][1].split(",")
            logo = settingsRows[0][2]
            contractFrom = settingsRows[0][3]
            contractTo = settingsRows[0][4]
            noOfUserLicence = int(settingsRows[0][5])
            fileSpace = settingsRows[0][6]
            isSmsSubscribed = int(settingsRows[0][7])  
            settingsDataList = [countryIds, domainIds, logo, contractFrom, contractTo, noOfUserLicence,
        fileSpace, isSmsSubscribed]
        except:
            print "Settings Not exists for client %d" % clientId

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
    def getClientList(self):
        clientList = []

        clientGroupRows = self.getClientGroups()

        for row in clientGroupRows:
            try:
                clientId = int(row[0])
                groupName = row[1]
                inchargePersons = row[2].split(",")
                isActive = row[3]

                username = self.getClientUsername(clientId)

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

                groupCompany = GroupCompany(clientId, groupName, inchargePersons, countryIds ,domainIds, 
                                            logo, contractFrom, contractTo, noOfUserLicence, fileSpace, 
                                            isSmsSubscribed, dateConfigurations, username, isActive)
                groupCompany.verify()

                clientList.append(groupCompany.toDetailedStructure())
            except:
                print "Error : Settings not exist for client : %d" %clientId
                continue

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
    userDetailsTblName = "tbl_user_details"
    clientUserDetailsTblName = "tbl_client_user_details"
    countryTblName = "tbl_countries"
    domainTblName = "tbl_domains"
    userTblName = "tbl_users"
    clientDBName = None

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = sessionUser
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def processRequest(self):
        requestData = self.requestData

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
            self.response = "GroupNameAlreadyExists"
        elif self.saveCredentials() and self.saveGroupCompany() :
            if self.createClientDatabase():
                if self.saveClientDetails():
                    if self.copyBasicData():
                        if self.saveDateConfigurations():
                            if self.saveClientAdminUserDetails():
                                self.response = "SaveClientGroupSuccess"
                            else:
                                print "Saving Client admin user details failed"
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
            condition = " user_id='"+str(inchargePerson)+"'"
            DatabaseHandler.instance().append(self.userDetailsTblName,userColumns, userValues, condition)

        return DatabaseHandler.instance().insert(self.clientTblName,columns,values)

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
            self.clientDBName = getClientDatabase(self.clientId)
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
        return ClientDatabaseHandler.instance(self.getDatabaseName()).insert(self.clientUserDetailsTblName, columns, values)

class GetClientGroups(object):
    responseData = {}
    def __init__(self):
        domainList = DomainList.getDomainList()
        countryList = CountryList.getCountryList()
        userList = User.getList()
        clientList = GroupCompany.getClientList()

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
                print "Updating Status Failed"
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

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        self.sessionUser = sessionUser
        self.response = ""

        assertType(requestData, DictType)
        assertType(sessionUser, LongType)

    def processRequest(self):
        requestData = self.requestData

        self.clientId = JSONHelper.getInt(requestData, "client_id")
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
        self.dateConfigurations = JSONHelper.getList(requestData, "date_configurations")

        if self.isDuplicateGroupName():
            self.response = "GroupNameAlreadyExists"
        elif self.updateGroupCompany() :
            if self.updateClientDetails():
                if self.copyBasicData():
                    if self.updateDateConfigurations():
                        if self.updateClientAdminUserDetails():
                                self.response = "UpdateClientGroupSuccess"
                        else:
                            print "Saving Client admin user details failed"
                    else:
                        print "Saving date configurations Failed"
                else:
                    print "Copying Data Failed"
            else:
                print "Saving client settings failed"
        else:
            print "Save Group company failed"

        return commonResponseStructure(self.response,{})

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


    def updateGroupCompany(self):
        columnsList = ["client_id", "group_name", "incharge_persons", "updated_on", 
                        "updated_by"]
        valuesList =  [self.clientId, self.groupName, 
                        ",".join(str(x) for x in self.inchargePersons),
                        getCurrentTimeStamp(), self.sessionUser]
        oldInchargePersons = self.getOldInchargePersons()
        
        existingInchargePersons = []
        newInchargePersons = []
        removedInchargePersons = []
        for inchargePerson in inchargePersons:
            if inchargePerson in oldInchargePersons:
                existingInchargePersons.append(inchargePerson)
            else:
                newInchargePersons.append(inchargePerson)

        for oldInchargePerson in oldInchargePersons:
            if oldInchargePerson not in inchargePersons:
                removedInchargePersons.append(oldInchargePerson)

        for newInchargePerson in newInchargePersons:
            condition = " user_id='%d'" % newInchargePerson 
            columns = "client_ids"
            values = str(self.clientId)
            DatabaseHandler.instance().append(self.userDetailsTblName, columns, values, condition)

        for removedInchargePerson in removedInchargePersons:
            columns = "client_ids"
            condition = "user_id='%d'" % removedInchargePerson
            rows = DatabaseHandler.instance().getData(self.userDetailsTblName, columns, condition)
            clientIds = rows[0][0].split(",")
            clientIds.remove(self.clientId)
            updateColumns = ["client_ids"]
            updateValues = [clientIds]
            DatabaseHandler.instance().update(self.userDetailsTblName, updateColumns, 
                                            updateValues, condition)

        return DatabaseHandler.instance().update(self.clientTblName,columns,valuesList)

    def updateClientDetails(self):
        columns = ["country_ids", "domain_ids", "logo_url", "contract_from", "contract_to",
        "no_of_user_licence","total_disk_space", "is_sms_subscribed","updated_on", "updated_by"]
        valuesList =  [ ",".join(str(x) for x in self.countryIds),
                         ",".join(str(x) for x in self.domainIds),
                        self.logo, self.contractFrom, self.contractTo, self.noOfLicence, 
                        self.fileSpace, self.isSmsSubscribed, getCurrentTimeStamp(), 
                        self.sessionUser]
        return ClientDatabaseHandler.instance(self.getDatabaseName()).insert(self.clientSettingsTblName,columns,values)

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
        ClientDatabaseHandler.instance(self.getDatabaseName()).truncate(self.countryTblName)
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
        ClientDatabaseHandler.instance(self.getDatabaseName()).truncate(self.domainTblName)
        return ClientDatabaseHandler.instance(
                        self.getDatabaseName()).bulkInsert(
                        self.domainTblName,columns,valuesList)

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

        return ClientDatabaseHandler.instance(
                            self.getDatabaseName()).onDuplicateKeyUpdate(
                            self.clietConfigurationTblName,columns,valuesList)

    def updateClientAdminUserDetails(self):
        columnsList = [  "country_ids", "domain_ids", "updated_by", "updated_on"]
        valuesList = [ ",".join(str(x) for x in self.countryIds), 
                    ",".join(str(x) for x in self.domainIds),1,0, 
                    self.sessionUser, getCurrentTimeStamp()]
        return ClientDatabaseHandler.instance(
                        self.getDatabaseName()).update( 
                        self.clientUserDetailsTblName, columnsList, valuesList, condition)   


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