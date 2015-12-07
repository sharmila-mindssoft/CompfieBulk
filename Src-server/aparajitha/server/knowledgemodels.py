import json
from types import *

__all__ = [
    "PossibleError", "Domain",
    "Country",
    "Industry",
    "StatutoryNature",
    "Level", "Geography", "Statutory", "Compliance",
    "StatutoryMapping",
    "UserGroup",
    "AdminUser"
]


def assertType (x, typeObject) :
    if type(x) is not typeObject :
        msg = "%s- expected type %s, received invalid type  %s" % (x, typeObject, type(x))
        raise TypeError(msg)

class PossibleError(object) :
    def __init__(self, possibleError) :
        self.possibleError = possibleError
        self.verify()

    def verify(self) :
        assertType(self.possibleError, StringType)

    def toStructure(self) :
        return [
            str(self.possibleError),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class Domain(object) :
    def __init__(self, domainId, domainName, isActive) :
        self.domainId = domainId
        self.domainName = domainName
        self.isActive = isActive
        self.verify()

    def verify(self) :
        assertType(self.domainId, IntType)
        assertType(self.domainName, StringType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        return {
            "domain_id": self.domainId,
            "domain_name": self.domainName,
            "is_active": self.isActive
        }

    @classmethod
    def fromStructure(klass, data) :
        domainId = data.get("domain_id")
        assertType(domainId, IntType)
        domainName = data.get("domain_name")
        assertType(domainName, StringType)
        isActive = data.get("is_active")
        assertType(isActive, IntType) 
        return klass(domainId, domainName, isActive)

    @classmethod
    def get_list(self, db):
        domain_list = []
        # try:
        rows = db.get_domains()
        for row in rows:
            domain_id = int(row[0])
            domain_name = row[1]
            is_active = row[2]
            domain = Domain(domain_id, domain_name, is_active)
            domain_list.append(domain.to_structure())
        # except:
        #     print "Error: While fetching Countries"
        return domain_list

    def __repr__(self) :
        return str(self.toStructure())

class Country(object) :
    def __init__(self, countryId, countryName, isActive) :
        self.countryId = countryId
        self.countryName = countryName
        self.isActive = isActive
        self.verify()

    def verify(self) :
        assertType(self.countryId, IntType)
        assertType(self.countryName, StringType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        return {
            "country_id": self.countryId,
            "country_name": self.countryName,
            "is_active": self.isActive
        }

    @classmethod
    def get_list(self, db):
        country_list = []
        # try:
        rows = db.get_countries()
        for row in rows:
            country_id = int(row[0])
            country_name = row[1]
            is_active = row[2]
            country = Country(country_id, country_name, is_active)
            country_list.append(country.to_structure())
        # except:
        #     print "Error: While fetching Countries"
        return country_list


    def __repr__(self) :
        return str(self.toStructure())

class Industry(object) :
    def __init__(self, industryId, industryName, isActive) :
        self.industryId = industryId
        self.industryName = industryName
        self.isActive = isActive
        self.verify()

    def verify(self) :
        assertType(self.industryId, IntType)
        assertType(self.industryName, StringType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        return {
            "industry_id": self.industryId,
            "industry_name": self.industryName,
            "is_active": self.isActive
        }

    def __repr__(self) :
        return str(self.toStructure())

class StatutoryNature(object) :
    def __init__(self, statutoryNatureId, statutoryNatureName, isActive) :
        self.statutoryNatureId = statutoryNatureId
        self.statutoryNatureName = statutoryNatureName
        self.isActive = isActive
        self.verify()

    def verify(self) :
        assertType(self.statutoryNatureId, IntType)
        assertType(self.statutoryNatureName, StringType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        return {
            "statutory_nature_id": self.statutoryNatureId,
            "statutory_nature_name": self.statutoryNatureName,
            "is_active": self.isActive
        }

    def __repr__(self) :
        return str(self.toStructure())

class Level(object) :
    def __init__ (self, levelId, levelPosition, levelName) :
        self.levelId = levelId
        self.levelPosition = levelPosition
        self.levelName = levelName
        self.verify()

    def verify(self) :
        assertType(self.levelId, IntType)
        assertType(self.levelPosition, IntType)
        assertType(self.levelName, StringType)

    def toStructure(self) :
        return {
            "level_id": self.levelId,
            "level_position": self.levelPosition,
            "level_name": self.levelName,
        }

    def __repr__(self) :
        return str(self.toStructure())

class Geography(object) :
    def __init__(self, geographyId, name, levelId, parentIds, isActive) :
        self.geographyId = geographyId
        self.name = name
        self.levelId = levelId
        self.parentIds = parentIds
        self.isActive = isActive
        self.verify()

    def verify(self) :
        assertType(self.geographyId, IntType)
        assertType(self.name, StringType)
        assertType(self.levelId, IntType)
        assertType(self.parentIds, IntType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        return {
            "geography_id": self.geographyId,
            "geography_name": self.name,
            "level_id": self.levelId,
            "parent_id": self.parentIds,
            "is_active": self.isActive
        }

    @classmethod
    def getCountryWiseList(self):
        geographies = {}
        DH = DatabaseHandler.instance()
        _geographyList = DH.instance().getGeographies()
        for row in _geographyList :
            parentIds = [int(x) for x in row[3][:-1].split(',')]
            geography = Geography(int(row[0]), row[1], int(row[2]), parentIds[-1], int(row[4]))
            countryId = int(row[5])
            _list = geographies.get(countryId)
            if _list is None :
                _list = []
            _list.append(geography.toStructure())
            geographies[countryId] = _list
        return geographies

    def __repr__(self) :
        return str(self.toStructure())

class Statutory(object) :
    def __init__(self, statutoryId, name, levelId, parentIds) :
        self.statutoryId = statutoryId
        self.name = name
        self.levelId = levelId
        self.parentIds = parentIds
        self.verify()
    
    def verify(self) :
        assertType(self.statutoryId, IntType)
        assertType(self.name, StringType)
        assertType(self.levelId, IntType)
        assertType(self.parentIds, ListType)

    def toStructure(self) :
        return {
            "statutory_id": self.statutoryId, 
            "statutory_name": self.name,
            "level_id": self.levelId,
            "parent_ids": self.parentIds,
            "parent_id": self.parentIds[-1]
        }

    def __repr__(self) :
        return str(self.toStructure())

class Compliance(object) :
    def __init__(
            self, complianceId, statutoryProvition, complianceTask,
            description, documentName, formatFileName, penalDescription,
            complianceFrequency, statutoryDates,
            repeatsType, 

            repeatsEvery, durationType, duration, isActive
        ):
        self.complianceId = complianceId
        self.statutoryProvition = statutoryProvition
        self. complianceTask = complianceTask
        self.description = description
        self.documentName = documentName
        self.formatFileName = formatFileName
        self.penalDescription = penalDescription
        self.complianceFrequency = complianceFrequency
        self.statutoryDates = statutoryDates
        self.repeatsType = repeatsType
        self.repeatsEvery = repeatsEvery
        self.durationType = durationType
        self.duration = duration
        self.isActive = isActive
        self.verify()
    
    def verify(self) :
        assertType(self.complianceId, IntType)
        assertType(self.statutoryProvition, StringType)
        assertType(self.complianceTask, StringType)
        assertType(self.description, StringType)
        assertType(self.documentName, StringType)
        assertType(self.formatFileName, ListType)
        assertType(self.penalDescription, StringType)
        assertType(self.complianceFrequency, StringType)
        assertType(self.statutoryDates, ListType)
        # assertType(self.repeatsType, StringType)
        # assertType(self.repeatsEvery, IntType)
        # assertType(self.durationType, StringType)
        # assertType(self.duration, IntType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        # "statutory_dates": [
        #         {
        #             "statutory_date": self.statutoryDate,
        #             "statutory_month": self.statutoryMonth,
        #             "trigger_before_days": self.triggerBefore
        #         },
        #     ],
        return {
            "compliance_id": self.complianceId,
            "statutory_provision" : self.statutoryProvition,
            "compliance_task": self.complianceTask,
            "description": self.description,
            "document_name": self.documentName,
            "format_file_name": self.formatFileName,
            "penal_description": self.penalDescription,
            "compliance_frequency": self.complianceFrequency,
            "statutory_dates": self.statutoryDates,
            "repeats_type": self.repeatsType,
            "repeats_every": self.repeatsEvery, 
            "duration_type": self.durationType,
            "duration": self.duration,
            "is_active": self.isActive
        }

    def __repr__(self) :
        return str(self.toStructure())

class StatutoryMapping(object) :
    def __init__(
        self, countryId, countryName, domainId, 
        domainName, industryIds,
        statutoryNatureId, statutoryNatureName,
        statutoryIds, statutoryMappings, complianceIds, 
        geographyIds, approvalStatus, isActive
    ) :
        self.countryId = countryId
        self.countryName = countryName 
        self.domainId = domainId
        self.domainName = domainName
        self.industryIds = industryIds
        self.industryNames = None
        self.statutoryNatureId = statutoryNatureId
        self.statutoryNatureName = statutoryNatureName
        self.statutoryIds = statutoryIds
        self.statutoryMappings = statutoryMappings
        self.complianceIds = complianceIds
        self.complianceNames = []
        self.compliances = []
        self.geographyIds = geographyIds
        self.approvalStatus = approvalStatus
        self.isActive = isActive
        self.verify()
    
    def verify(self) :
        assertType(self.countryId, IntType)
        assertType(self.countryName, StringType)
        assertType(self.domainId, IntType)
        assertType(self.domainName, StringType)
        assertType(self.industryIds, ListType)
        # assertType(self.industryNames, ListType)
        assertType(self.statutoryNatureId, IntType)
        assertType(self.statutoryNatureName, StringType)
        assertType(self.statutoryIds, ListType)
        assertType(self.statutoryMappings, ListType)
        assertType(self.complianceIds, ListType)
        # assertType(self.complianceNames, ListType)
        assertType(self.geographyIds, ListType)
        assertType(self.approvalStatus, IntType)
        assertType(self.isActive, IntType)
        self.getData()

    def getData(self) :
        DH = DatabaseHandler.instance()
        self.industryNames = DH.getIndustryByIndustryId(self.industryIds)
        _compliances = DH.getCompliancesByIds(self.complianceIds)
        for row in _compliances :
            formatFileName = []
            if len(row[5]) >1 :
                formatFileName = [int(x) for x in row[5].split(',')]
            compliance =  Compliance(
                    int(row[0]), row[1], row[2], row[3], row[4], 
                    formatFileName, row[6], row[7], 
                    json.loads(row[8]), row[9], 
                    row[10], row[11], row[12], row[13]
                )
            self.compliances.append(compliance.toStructure())
            self.complianceNames.append("%s-%s" % (row[4], row[2]))


    def toStructure(self) :
        return {
            "country_id": self.countryId,
            "country_name": self.countryName,
            "domain_id": self.domainId,
            "domain_name": self.domainName,
            "industry_ids": self.industryIds,
            "industry_names": self.industryNames,
            "statutory_nature_id": self.statutoryNatureId,
            "statutory_nature_name": self.statutoryNatureName,
            "statutory_ids": self.statutoryIds,
            "statutory_mappings": self.statutoryMappings,
            "compliances": self.compliances,
            "compliance_names": self.complianceNames,
            "geographies_ids": self.geographyIds,
            "approval_status": self.approvalStatus,
            "is_active": self.isActive
        }

    def __repr__(self) :
        return str(self.toStructure())

class UserGroup() :
    def __init__(self, user_group_id, user_group_name, form_type, form_ids, is_active) :
        self.user_group_id =  user_group_id 
        self.user_group_name = user_group_name
        self.form_type = form_type 
        self.form_ids = form_ids 
        self.is_active = is_active if is_active != None else 1

    @classmethod
    def initialize_with_request(self, request, user_group_id):
        user_group_name = str(request["user_group_name"])
        form_type = str(request["form_type"])
        form_ids =  request["form_ids"]
        user_group = UserGroup(user_group_id, user_group_name, form_type, form_ids, None)
        return user_group

    def to_detailed_structure(self) :
        return {
            "user_group_id": int(self.user_group_id),
            "user_group_name": str(self.user_group_name),
            "form_type": str(self.form_type),
            "form_ids": self.form_ids,
            "is_active": int(self.is_active)
        }

    def to_structure(self):
        return {
            "user_group_id": int(self.user_group_id),
            "user_group_name": str(self.user_group_name),
            "is_active": int(self.is_active)
        }

    @classmethod
    def get_detailed_list(self, db) :
        user_group_list = []
        rows = db.get_user_group_details_list()
        for row in rows:
            form_ids = [int(x) for x in row[3].split(",")]
            user_group = UserGroup(int(row[0]), row[1], row[2], form_ids, row[4])
            user_group_list.append(user_group.to_detailed_structure())
        return user_group_list

    @classmethod
    def get_list(self, db):
        user_group_list = []
        rows = db.get_user_group_list()
        for row in rows:
            user_group = UserGroup(int(row[0]), row[1], None, None, row[2])
            user_group_list.append(user_group.to_structure())
        return user_group_list

class AdminUser(object) :
    def __init__(self, user_id, email_id, user_group_id, form_type,employee_name, 
                employee_code, contact_no, address, designation, country_ids,
                domain_ids, client_id,is_active) :
        self.user_id =  int(user_id)
        self.email_id =  str(email_id)
        self.user_group_id =  int(user_group_id) if user_group_id != None else None
        self.form_type = str(form_type) if form_type != None else None
        self.employee_name =  str(employee_name)
        self.employee_code =  str(employee_code)
        self.contact_no =  str(contact_no)
        self.address =  str(address)
        self.designation =  str(designation)
        self.country_ids =  country_ids
        self.domain_ids =  domain_ids
        self.client_id = client_id 
        self.is_active = int(is_active) if is_active != None else 1

    @classmethod
    def initialize_with_request(self, request, user_id):
        email_id = None
        try:
            email_id = request["email_id"]
        except:
            email_id = None
        user_group_id = request["user_group_id"]
        employee_name = request["employee_name"]
        employee_code = request["employee_code"]
        contact_no = request["contact_no"]
        address =  request["address"]
        designation =  request["designation"]
        country_ids = request["country_ids"]
        domain_ids = request["domain_ids"]
        user = AdminUser(user_id, email_id, user_group_id, None,employee_name, employee_code, contact_no, 
                    address, designation, country_ids, domain_ids, None,None)
        return user

    def to_detailed_structure(self) :
        return {
            "user_id": self.user_id,
            "email_id": self.email_id,
            "user_group_id": self.user_group_id,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "contact_no": self.contact_no,
            "address": self.address, 
            "designation": self.designation,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids,
            "client_id": self.client_id,
            "is_active": self.is_active
        }

    def to_structure(self):
        employee_name = None
        if self.employee_code == None:
            employee_name = self.employee_name
        else:
            employee_name = "%s-%s" % (self.employee_code, self.employee_name)
        return {
            "user_id": self.user_id,
            "employee_name": employee_name,
        }

    @classmethod
    def get_detailed_list(self, db):
        userList = []
        rows = db.get_user_details_list()    
        for row in rows:
            country_ids = [int(x) for x in row[8].split(",")] if row[8] != None else None
            domain_ids = [int(x) for x in row[9].split(",")] if row[9] != None else None
            user = AdminUser(row[0],row[1], row[2], None,row[3], row[4],
                 row[5], row[6], row[7], country_ids, domain_ids, 
                 row[10], row[11])
            userList.append(user.to_detailed_structure())
        return userList

    @classmethod
    def get_list(self, db):
        userList = []
        rows = db.get_user_list()
        for row in rows:
            user = AdminUser(int(row[0]),None,None, None,row[1], row[2],
                 None, None, None, None, None, None, None)
            userList.append(user.toStructure())
        return userList    

