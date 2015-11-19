from types import *
from databasehandler import DatabaseHandler 
import json
from aparajitha.server.common import *

__all__ = [
    "GroupCompany",
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit"
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

    def __init__(self, requestData, sessionUser) :
        self.requestData = requestData
        assertType(requestData, DictType)
        self.sessionUser = sessionUser
        assertType(sessionUser, IntType)

    def processRequest():
        groupCompany = JSONHelper.getString(requestData, "group_company")
        businessGroup = JSONHelper.getString(requestData, "business_group")
        legalEntity = JSONHelper.getString(requestData, "legal_entity")
        division = JSONHelper.getString(requestData, "division")
        logo = JSONHelper.getString(requestData, "logo")
        domainIds = JSONHelper.getString(requestData, "domain_ids")
        username = JSONHelper.getString(requestData, "username")
        noOfLicence = JSONHelper.getString(requestData, "no_of_licence")
        contractFrom = JSONHelper.getString(requestData, "contract_from")
        contractTo = JSONHelper.getString(requestData, "contract_to")
        totalDiskSpace = JSONHelper.getString(requestData, "total_disk_space")
        isSmsSubscribed = JSONHelper.getString(requestData, "is_sms_subscribed")
        countryWiseUnits = JSONHelper.getString(requestData, "country_wise_units")

        assertType(groupCompany, DictType)
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




