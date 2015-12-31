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
    "ClientConfiguration",
    "Client"
]
clientDatabaseMappingFilePath = os.path.join(ROOT_PATH, 
    "Src-client/files/desktop/common/clientdatabase/clientdatabasemapping.txt")
class Unit(object):
    unitTblName = "tbl_units"
    divisionTblName = "tbl_divisions"
    legalEntityTblName = "tbl_legal_entities"
    businessGroupTblName = "tbl_business_groups"

    def __init__(self, unitId, divisionId, legalEntityId, businessGroupId, clientId, 
                countryId, geographyId, unitCode, unitName, industryId, address, 
                postalCode, domainIds, isActive, industryName, geography):
        self.clientId = int(clientId)
        self.unitId = unitId
        self.divisionId = int(divisionId) if divisionId != None else None
        self.legalEntityId = int(legalEntityId)
        self.businessGroupId = int(businessGroupId) if businessGroupId != None else None
        self.countryId = int(countryId)
        self.geographyId = int(geographyId) if isActive != None else None
        self.unitCode = str(unitCode)
        self.unitName = str(unitName)
        self.industryId = int(industryId) if isActive != None else None
        self.address = str(address)
        self.postalCode = str(postalCode)
        self.domainIds = domainIds
        self.isActive = int(isActive) if isActive != None else 1
        self.industryName = str(industryName)
        self.geography = str(geography)

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

    @classmethod
    def generateNewUnitId(self, clientId):
        return ClientDatabaseHandler.instance(
                getClientDatabase(clientId)).generateNewId(
                self.unitTblName, "unit_id")

    def isIdInvalid(self):
        condition = "unit_id = '%d'" % self.unitId
        return not ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.unitTblName, condition)

    def isDuplicateUnitName(self):
        condition = "unit_name= '%s'" % self.unitName
        if self.unitId != None:
            condition += " and unit_id != '%d'" % self.unitId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.unitTblName, condition)

    def isDuplicateUnitCode(self):
        condition = "unit_code= '%s' " % self.unitCode
        if self.unitId != None:
            condition += " and unit_id != '%d'" % self.unitId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).isAlreadyExists(self.unitTblName, condition)

    def save(self, sessionUser):
        knowledgeValueslist = []
        clientValuesList = []
        if (self.unitId == None or not self.isIdInvalid()):
            self.unitId = self.generateNewUnitId(self.clientId)
            print "generating new id for unit {unitId}".format(unitId = self.unitId)
        clientDbColumns = "unit_id, legal_entity_id, "+\
                        " country_id, geography, unit_code, unit_name, industry_name,"+\
                        " address, postal_code, domain_ids"
        knowledgeDbColumns = "client_id, unit_id, country_id, geography_id, unit_code,"+\
                            " unit_name, industry_id, created_by, created_on,"+\
                            " updated_by, updated_on"
        knowledgeValuesList = [self.clientId, self.unitId, self.countryId, self.geographyId,
                                self.unitCode, self.unitName, self.industryId, 
                                int(sessionUser), getCurrentTimeStamp(), 
                                int(sessionUser), getCurrentTimeStamp()]
        clientValuesList = [self.unitId, self.legalEntityId,
                            self.countryId, self.geography, 
                            self.unitCode, self.unitName, self.industryName, 
                            self.address, self.postalCode, 
                            ",".join(str(x) for x in self.domainIds)]

        if self.businessGroupId != None:
            columns += ", business_group_id"
            valuesList.append(self.businessGroupId)
        if self.divisionId != None:
            columns += ", division_id"
            valuesList.append(self.divisionId)
        knowledgeValues = listToString(knowledgeValuesList)
        clientValues = listToString(clientValuesList)
        if ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).insert(
                self.unitTblName, clientDbColumns, clientValues):
            return DatabaseHandler.instance().insert(
                        self.unitTblName, knowledgeDbColumns, knowledgeValues) 

    def update(self, sessionUser):
        knowledgeValueslist = []
        clientValuesList = []
        clientDbColumns = [ "legal_entity_id",
                        "country_id", "geography", "unit_code", "unit_name", "industry_name",
                        "address", "postal_code", "domain_ids"]
        knowledgeDbColumns = [ "country_id", "geography_id", "unit_code",
                            "unit_name", "industry_id", "updated_by", "updated_on"]
        knowledgeValuesList = [self.countryId, self.geographyId,
                                self.unitCode, self.unitName, self.industryId, 
                                int(sessionUser), getCurrentTimeStamp()]
        clientValuesList = [self.legalEntityId,
                             self.countryId, self.geography, 
                            self.unitCode, self.unitName, self.industryName, 
                            self.address, self.postalCode, ",".join(str(x) for x in self.domainIds)]
        knowledgeCondition = " client_id = '%d' and unit_id= '%d'" % (self.clientId, self.unitId)
        clientCondition = " unit_id= '%d'" % self.unitId
        
        if self.businessGroupId != None:
            clientDbColumns.append("business_group_id")
            clientValuesList.append(self.businessGroupId)
        if self.divisionId != None:
            clientDbColumns.append("division_id")
            clientValuesList.append(self.divisionId)

        if DatabaseHandler.instance().update(
                        self.unitTblName, knowledgeDbColumns, knowledgeValuesList, knowledgeCondition):
            print "knowledge updated"
            return ClientDatabaseHandler.instance(
                getClientDatabase(self.clientId)).update(
                self.unitTblName, clientDbColumns, clientValuesList, clientCondition) 

    @classmethod
    def getList(self,clientIds):
        unitList = []
        print clientIds
        for index, clientId in enumerate(clientIds.split(",")):
                print clientId
            # try:
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

            # except:
            #     print "Error: While fetching Unit of client id %s" % clientId

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
        unitList , sessionUser, type):
        self.businessGroup = businessGroup
        self.legalEntity = legalEntity
        self.division = division
        self.unitList = unitList
        self.sessionUser = sessionUser
        if type == "save":
            if self.businessGroup.businessGroupId != None:
                self.businessGroup.save(self.sessionUser)
                if self.legalEntity.legalEntityId != None:
                    self.legalEntity.save(self.sessionUser)
                    if self.division.divisionId != None:
                        self.division.save(self.sessionUser)
                        for unitObj in self.unitList:
                            print "going to save unit %s" % unitObj.unitName
                            if unitObj.save(self.sessionUser):
                                print "saved unit %s" % unitObj.unitName
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
        elif type == "update":
            if self.businessGroup.update(self.sessionUser):
                if self.legalEntity.update(self.sessionUser):
                    if self.division.update(self.sessionUser):
                        for unitObj in self.unitList:
                            print "going to update unit %s" % unitObj.unitName
                            if unitObj.update(self.sessionUser):
                                print "saved unit %s" % unitObj.unitName
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

    def changeClientStatus(self, clientId,  legalEntityId, divisionId, 
        isActive, sessionUser):
        self.clientId = clientId
        self.legalEntityId = legalEntityId
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
        condition = " legal_entity_id='%d'" % self.legalEntityId
        if self.divisionId != None:
            condition += " AND division_id='%d'" % self.divisionId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.unitTblName, columns, values, condition)

    def getUnitsOfDivision(self):
        unitIdsList = []
        columns = "unit_id"
        condition = " legal_entity_id='%d'" % self.legalEntityId
        if self.divisionId != None:
            condition += " AND division_id='%d'" % self.divisionId
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