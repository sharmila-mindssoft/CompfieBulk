import json
from types import *

from databasehandler import DatabaseHandler

__all__ = [
    "JSONHelper", "PossibleError", "Domain", "DomainList", 
    "SaveDomain", "UpdateDomain", "ChangeDomainStatus",
    "Country", "CountryList", "SaveCountry",
    "UpdateCountry", "ChangeCountryStatus",
    "Industry", "IndustryList", "SaveIndustry",
    "UpdateIndustry", "ChangeIndustryStatus",
    "StatutoryNature", "StatutoryNatureList", "SaveStatutoryNature",
    "UpdateStatutoryNature", "ChangeStatutoryNatureStatus",
    "Level", "StatutoryLevelsList", "SaveStatutoryLevel", "GeographyLevelList",
    "SaveGeographyLevel", "Geography", "GeographyAPI", "Statutory", "StatutoryApi", "Compliance",
    "StatutoryMapping", "StatutoryMappingApi"
]

def assertType (x, typeObject) :
    if type(x) is not typeObject :
        msg = "%s- expected type %s, received invalid type  %s" % (x, typeObject, type(x))
        raise TypeError(msg)

class JSONHelper(object) :
    
    @staticmethod
    def string(x) :
        assertType(x, UnicodeType)
        return str(x)

    @staticmethod
    def getString(data, name) :
        return JSONHelper.string(data.get(name))

    @staticmethod
    def int(x):
        assertType(x, IntType)
        return x

    @staticmethod
    def getInt(data, name) :
        return JSONHelper.int(data.get(name))

    @staticmethod
    def getOptionalInt(data, name) :
        x = data.get(name)
        if x is None :
            return x
        return JSONHelper.int(x)

    @staticmethod
    def float(x) :
        assertType(x, FloatType)
        return x

    @staticmethod
    def getFloat(data, name) :
        return JSONHelper.float(data.get(name))

    @staticmethod
    def list(x) :
        assertType(x, ListType)
        return x

    @staticmethod
    def getList(data, name) :
        return JSONHelper.list(data.get(name))

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

    def __repr__(self) :
        return str(self.toStructure())

class DomainList(object) :
    def __init__(self) :
        self.domainList = []
        self.processData()

    def processData(self) :
        _domains = DatabaseHandler.instance().getDomains()
        for row in _domains :
            domain = Domain(int(row[0]), row[1], row[2])
            self.domainList.append(domain.toStructure())

    def toList(self) :
        return self.domainList

    def getDomains(self) :
        return self.domainList

    def toStructure(self) :
        return [
            "success",
            {"domains": self.domainList}
        ]

    @classmethod
    def getDomainList(self) :
        domain = DomainList()
        return domain.domainList

    def __repr__(self) :
        return str(self.toStructure())

class SaveDomain(object) :
    def __init__ (self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.domainName = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.domainName = JSONHelper.getString(requestData, "domain_name")
        isDuplicate = DatabaseHandler.instance().checkDuplicateDomain(self.domainName, None)
        if isDuplicate :
            self.responseData = "DomainNameAlreadyExists"
        else :
            if DatabaseHandler.instance().saveDomain(self.domainName, self.userId) :
                self.responseData = "success"
            else :
                self.responseData = "saveFailed"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class UpdateDomain(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.domainId = None
        self.domainName = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.domainName = JSONHelper.getString(requestData, "domain_name")
        self.domainId = JSONHelper.getInt(requestData, "domain_id")
        isDuplicate = DatabaseHandler.instance().checkDuplicateDomain(self.domainName, self.domainId)
        if isDuplicate :
            self.responseData = "DomainNameAlreadyExists"
        else :
            if DatabaseHandler.instance().updateDomain(self.domainId, self.domainName, self.userId) :
                self.responseData = "success"
            else :
                self.responseData = "InvalidDomainId"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class ChangeDomainStatus(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.domainId = None
        self.isActive = None
        self.responseData = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        self.domainId = JSONHelper.getInt(requestData, "domain_id")
        if DatabaseHandler.instance().updateDomainStatus(self.domainId, self.isActive, self.userId) :
            self.responseData = "success"
        else :
            self.responseData = "InvalidDomainId"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

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

    def __repr__(self) :
        return str(self.toStructure())

class CountryList(object) :
    def __init__(self) :
        self.countryList = []
        self.processData()

    def processData(self) :
        _countries = DatabaseHandler.instance().getCountries()
        for row in _countries :
            country = Country(int(row[0]), row[1], row[2])
            self.countryList.append(country.toStructure())

    def getCountry(self) :
        return self.countryList

    def toStructure(self) :
        return [
            "success",
            {"countries": self.countryList}
        ]

    @classmethod
    def getCountryList(self) :
        country = CountryList()
        return country.countryList

    def __repr__(self) :
        return str(self.toStructure())

class SaveCountry(object) :
    def __init__ (self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.countryName = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.countryName = JSONHelper.getString(requestData, "country_name")
        isDuplicate = DatabaseHandler.instance().checkDuplicateCountry(self.countryName, None)
        if isDuplicate :
            self.responseData = "CountryNameAlreadyExists"
        else :
            if DatabaseHandler.instance().saveCountry(self.countryName, self.userId) :
                self.responseData = "success"
            else :
                self.responseData = "saveFailed"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class UpdateCountry(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.countryId = None
        self.countryName = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.countryName = JSONHelper.getString(requestData, "country_name")
        self.countryId = JSONHelper.getInt(requestData, "country_id")
        isDuplicate = DatabaseHandler.instance().checkDuplicateCountry(self.countryName, self.countryId)
        if isDuplicate :
            self.responseData = "CountryNameAlreadyExists"
        else :
            if DatabaseHandler.instance().updateCountry(self.countryId, self.countryName, self.userId) :
                self.responseData = "success"
            else :
                self.responseData = "InvalidCountryId"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class ChangeCountryStatus(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.countryId = None
        self.isActive = None
        self.responseData = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        self.countryId = JSONHelper.getInt(requestData, "country_id")
        if DatabaseHandler.instance().updateCountryStatus(self.countryId, self.isActive, self.userId) :
            self.responseData = "success"
        else :
            self.responseData = "InvalidCountryId"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

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

class IndustryList(object) :
    def __init__(self) :
        self.industryList = []
        self.processData()

    def processData(self) :
        _industries = DatabaseHandler.instance().getIndustries()
        for row in _industries :
            industry = Industry(int(row[0]), row[1], row[2])
            self.industryList.append(industry.toStructure())

    def getIndustries(self):
        return self.industryList

    def toStructure(self) :
        return [
            "success",
            {"industries": self.industryList}
        ]

    @classmethod
    def getList(self):
        industryListObj = IndustryList()
        return industryListObj.industryList

    def __repr__(self) :
        return str(self.toStructure())

class SaveIndustry(object) :
    def __init__ (self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.industryName = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.industryName = JSONHelper.getString(requestData, "industry_name")
        isDuplicate = DatabaseHandler.instance().checkDuplicateIndustry(self.industryName, None)
        if isDuplicate :
            self.responseData = "IndustryNameAlreadyExists"
        else :
            if DatabaseHandler.instance().saveIndustry(self.industryName, self.userId) :
                self.responseData = "success"
            else :
                self.responseData = "saveFailed"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class UpdateIndustry(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.industryId = None
        self.industryName = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.industryName = JSONHelper.getString(requestData, "industry_name")
        self.industryId = JSONHelper.getInt(requestData, "industry_id")
        isDuplicate = DatabaseHandler.instance().checkDuplicateIndustry(self.industryName, self.industryId)
        if isDuplicate :
            self.responseData = "IndustryNameAlreadyExists"
        else :
            if DatabaseHandler.instance().updateIndustry(self.industryId, self.industryName, self.userId) :
                self.responseData = "success"
            else :
                self.responseData = "InvalidIndustryId"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class ChangeIndustryStatus(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.industryId = None
        self.isActive = None
        self.responseData = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        self.industryId = JSONHelper.getInt(requestData, "industry_id")
        if DatabaseHandler.instance().updateIndustryStatus(self.industryId, self.isActive, self.userId) :
            self.responseData = "success"
        else :
            self.responseData = "InvalidIndustryId"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

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

class StatutoryNatureList(object) :
    def __init__(self) :
        self.statutoryNatureList = []
        self.processData()

    def processData(self) :
        _statutoryNatures = DatabaseHandler.instance().getStatutoryNatures()
        for row in _statutoryNatures :
            statutoryNature = StatutoryNature(int(row[0]), row[1], row[2])
            self.statutoryNatureList.append(statutoryNature.toStructure())

    def getStatutoryNatures(self):
        return self.statutoryNatureList

    def toStructure(self) :
        return [
            "success",
            {"statutory_natures": self.statutoryNatureList}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class SaveStatutoryNature(object) :
    def __init__ (self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.statutoryNatureName = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.statutoryNatureName = JSONHelper.getString(requestData, "statutory_nature_name")
        isDuplicate = DatabaseHandler.instance().checkDuplicateStatutoryNature(
            self.statutoryNatureName, None
        )
        if isDuplicate :
            self.responseData = "StatutoryNatureNameAlreadyExists"
        else :
            if DatabaseHandler.instance().saveStatutoryNature(self.statutoryNatureName, self.userId) :
                self.responseData = "success"
            else :
                self.responseData = "saveFailed"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class UpdateStatutoryNature(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.statutoryNatureId = None
        self.statutoryNatureName = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.statutoryNatureName = JSONHelper.getString(requestData, "statutory_nature_name")
        self.statutoryNatureId = JSONHelper.getInt(requestData, "statutory_nature_id")
        isDuplicate = DatabaseHandler.instance().checkDuplicateStatutoryNature(
            self.statutoryNatureName, self.statutoryNatureId
        )
        if isDuplicate :
            self.responseData = "StatutoryNatureNameAlreadyExists"
        else :
            if DatabaseHandler.instance().updateStatutoryNature(
                self.statutoryNatureId, self.statutoryNatureName, self.userId
            ) :
                self.responseData = "success"
            else :
                self.responseData = "InvalidStatutoryNatureId"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class ChangeStatutoryNatureStatus(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.statutoryNatureId = None
        self.isActive = None
        self.responseData = None
        self.processData()

    def processData(self) :
        requestData = self.request[1]
        assertType(requestData, DictType)
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        self.statutoryNatureId = JSONHelper.getInt(requestData, "statutory_nature_id")
        if DatabaseHandler.instance().updateStatutoryNatureStatus(
            self.statutoryNatureId, self.isActive, self.userId
        ) :
            self.responseData = "success"
        else :
            self.responseData = "InvalidStatutoryNatureId"

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

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

class StatutoryLevelsList(object) :
    def __init__(self) :
        self.statutoryLevels = {}
        self.countryList = []
        self.domainList = []
        self.processData()

    def processData(self) :
        self.countryList = CountryList().getCountry()
        self.domainList = DomainList().toList()
        _statutoryLevels = DatabaseHandler.instance().getStatutoryLevels()
        for row in _statutoryLevels :
            statutoryLevel = Level(int(row[0]), int(row[1]), row[2])
            countryId = int(row[3])
            domainId = int(row[4])
            _list = []
            countryWise = {}
            countryWise = self.statutoryLevels.get(countryId)
            if countryWise is None :
                countryWise = {}
            else :
                _list = countryWise.get(domainId)
                if _list is None :
                    _list = []
            _list.append(statutoryLevel.toStructure())
            countryWise[domainId] = _list
            self.statutoryLevels[countryId] = countryWise
    
    def getStatutoryLevels(self):
        return self.statutoryLevels

    def toStructure(self) :
        return [
            "success",
            {
                "countries": self.countryList,
                "domains": self.domainList,
                "statutory_levels": self.statutoryLevels
            }
        ]

    def __repr__(self) :
        return str(self.toStructure())

class SaveStatutoryLevel(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.processRequest()

    def processRequest(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        assertType(requestData, DictType)
        countryId = JSONHelper.getInt(requestData, "country_id")
        domainId = JSONHelper.getInt(requestData, "domain_id")
        levels = JSONHelper.getList(requestData, "levels")
        savedNames = [row[2] for row in DH.getStatutoryLevelsByID(countryId, domainId)]
        levelNames = []
        levelPositions = []

        for level in levels :
            levelId = JSONHelper.getOptionalInt(level, "level_id")
            name = JSONHelper.getString(level, "level_name")
            position = JSONHelper.getInt(level, "level_position")
            if levelId is None :
                if (savedNames.count(name) > 0) :
                    self.responseData = "LevelIdCannotNullFor '%s'" % name
                    break
            levelNames.append(name)
            levelPositions.append(position)

        duplicateNames = [x for i, x in enumerate(levelNames) if levelNames.count(x) > 1]
        duplicatePositions = [x for i, x in enumerate(levelPositions) if levelPositions.count(x) > 1]
        if len(duplicateNames) > 0 :
            self.responseData = "DuplicateStatutoryLevelNamesExists"
        elif len(duplicatePositions) > 0 :
            self.responseData = "DuplicateStatutoryLevelPositionsExists"
        if self.responseData is None :
            for level in levels :
                levelId = JSONHelper.getOptionalInt(level, "level_id")
                name = JSONHelper.getString(level, "level_name")
                position = JSONHelper.getInt(level, "level_position")

                if (DH.saveStatutoryLevel(countryId, domainId, levelId, name, position, self.userId)) :
                    self.responseData = "success"
                else :
                    self.responseData = "saveFailed: %s" % level
                    break

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

    def __repr__(self) :
        return str(self.toStructure())

class GeographyLevelList(object) :
    def __init__(self) :
        self.geographyLevels = {}
        self. countryList = []
        self.processData()

    def processData(self) :
        self.countryList = CountryList().getCountry()
        _geographyLevels = DatabaseHandler.instance().getGeographyLevels()
        for row in _geographyLevels :
            geographyLevel = Level(int(row[0]), int(row[1]), row[2])
            countryId = int(row[3])
            _list = self.geographyLevels.get(countryId)
            if _list is None :
                _list = []
            _list.append(geographyLevel.toStructure())
            self.geographyLevels[countryId] = _list

    def getGeographyLevels(self) :
        return self.geographyLevels

    def toStructure(self) :
        return [
            "success",
            {
                "countries": self.countryList,
                "geography_levels": self.geographyLevels
            }
        ]

    @classmethod
    def getCountryWiseList(self):
        geographyLevelList = GeographyLevelList()
        return geographyLevelList.geographyLevels

    def __repr__(self) :
        return str(self.toStructure())

class SaveGeographyLevel(object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.processRequest()

    def processRequest(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        assertType(requestData, DictType)
        countryId = JSONHelper.getInt(requestData, "country_id")
        levels = JSONHelper.getList(requestData, "levels")
        savedNames = [row[2] for row in DH.getGeographyLevelsByCountry(countryId)]
        levelNames = []
        levelPositions = []

        for level in levels :
            levelId = JSONHelper.getOptionalInt(level, "level_id")
            name = JSONHelper.getString(level, "level_name")
            levelNames.append(name)
            levelPositions.append(JSONHelper.getInt(level, "level_position"))
            if levelId is None :
                if (savedNames.count(name) > 0) :
                    self.responseData = "LevelIdCannotNullFor '%s'" % name
                    break

        duplicateNames = [x for i, x in enumerate(levelNames) if levelNames.count(x) > 1]
        duplicatePositions = [x for i, x in enumerate(levelPositions) if levelPositions.count(x) > 1]
        if len(duplicateNames) > 0 :
            self.responseData = "DuplicateGeographyLevelNamesExists"
        elif len(duplicatePositions) > 0 :
            self.responseData = "DuplicateGeographyLevelPositionsExists"

        if self.responseData is None :
            for level in levels :
                levelId = JSONHelper.getOptionalInt(level, "level_id")
                name = JSONHelper.getString(level, "level_name")
                position = JSONHelper.getInt(level, "level_position")

                if (DH.saveGeographyLevel(countryId, levelId, name, position, self.userId)) :
                    self.responseData = "success"
                else :
                    self.responseData = "saveFailed: %s" % level
                    break

    def toStructure(self) :
        return [
            str(self.responseData),
            {}
        ]

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

class GeographyAPI(object) :
    countryList = None
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.countryList = CountryList().getCountry()
        self.geographyLevelList = GeographyLevelList().getGeographyLevels()
        self.geographies = {}


    def getGeography(self) :
        DH = DatabaseHandler.instance()
        _geographyList = DH.getGeographies()
        for row in _geographyList :
            parentIds = [int(x) for x in row[3][:-1].split(',')]
            geography = Geography(int(row[0]), row[1], int(row[2]), parentIds[-1], int(row[4]))
            countryId = int(row[5])
            _list = self.geographies.get(countryId)
            if _list is None :
                _list = []
            _list.append(geography.toStructure())
            self.geographies[countryId] = _list
        return [
            "success",
            {
                "countries": self.countryList,
                "geography_levels": self.geographyLevelList,
                "geographies": self.geographies
            }
        ]

    def getGeographyList(self) :
        self.getGeography()
        return self.geographies

    @classmethod
    def toMappingStructure(self, geographyId, name, levelId, parentIds, mapping, isActive) :
        return {
            "geography_id": geographyId,
            "geography_name": name,
            "level_id": levelId,
            "parent_id": parentIds,
            "mapping": mapping,
            "is_active": isActive
        }    

    @classmethod
    def getList(self):
        geographies = {}
        DH = DatabaseHandler.instance()
        _geographyList = DH.getGeographies()
        geographyData = {}

        for row in _geographyList :
            geographyData[int(row[0])] = row[1]
        for row in _geographyList :
            parentIds = [int(x) for x in row[3][:-1].split(',')]
            geography = Geography(int(row[0]), row[1], int(row[2]), parentIds[-1], int(row[4]))
            countryId = int(row[5])
            names = []
            names.append(row[6])
            for id in parentIds :
                if id > 0 :
                    names.append(geographyData.get(id))
                names.append(row[1])

            mapping = ' >> '.join(str(x) for x in names)
            _list = geographies.get(countryId)
            if _list is None :
                _list = []
            _list.append(self.toMappingStructure(int(row[0]), row[1], int(row[2]), 
                parentIds[-1], mapping, int(row[4])))
            geographies[countryId] = _list
        return geographies

    def saveGeographies(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        assertType(requestData, DictType)
        levelId = JSONHelper.getInt(requestData, "geography_level_id")
        geographyName = JSONHelper.getString(requestData, "geography_name")
        parentIdsList = JSONHelper.getList(requestData, "parent_ids")
        parentIds = ','.join(str(x) for x in parentIdsList) + ","
        geographyNames = [row[1].lower() for row in DH.getDuplicateGeographies(parentIds, None)]
        if geographyNames.count(geographyName.lower()) > 0:
            self.responseData = "GeographyNameAlreadyExists"
        else :
            if (DH.saveGeographies(geographyName, levelId, parentIds, self.userId)) :
                self.responseData = "success"
            else :
                self.responseData = "saveFailed: %s" % requestData

        return [
            str(self.responseData),
            {}
        ]

    def updateGeographies(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        assertType(requestData, DictType)
        geographyId =  JSONHelper.getInt(requestData, "geography_id")
        levelId = JSONHelper.getInt(requestData, "geography_level_id")
        geographyName = JSONHelper.getString(requestData, "geography_name")
        parentIdsList = JSONHelper.getList(requestData, "parent_ids")
        parentIds = ','.join(str(x) for x in parentIdsList) + ","
        geographyNames = [row[1].lower() for row in DH.getDuplicateGeographies(parentIds, geographyId)]
        if geographyNames.count(geographyName.lower()) > 0:
            self.responseData = "GeographyNameAlreadyExists"
        else :
            if (DH.updateGeographyMaster(geographyId, geographyName, parentIds, self.userId)) :
                self.responseData = "success"
            else :
                self.responseData = "saveFailed: %s" % requestData

        return [
            str(self.responseData),
            {}
        ]

    def changeGeographyStatus(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        assertType(requestData, DictType)
        geographyId =  JSONHelper.getInt(requestData, "geography_id")
        isActive = JSONHelper.getInt(requestData, "is_active")

        if (DH.changeGeographyStatus(geographyId, isActive, self.userId)) :
            self.responseData = "success"
        else :
            self.responseData = "saveFailed: %s" % requestData

        return [
            str(self.responseData),
            {}
        ]

    @classmethod
    def geographyReport(self) :
        DH = DatabaseHandler.instance()
        _geographyList = DH.getGeographies()
        geoMappingList = []
        geoMappingDict = {}
        geographyData = {}

        for row in _geographyList :
            geographyData[int(row[0])] = row[1]
        for geo in _geographyList :
            countryId = int(row[5])
            parentIds = [int(x) for x in geo[3][:-1].split(',')]
            names = []
            names.append(geo[6])
            for id in parentIds :
                if id > 0 :
                    names.append(geographyData.get(id))
                names.append(geo[1])

            geographies = '>>'.join(str(x) for x in names)
            isActive = int(geo[4])
            geoMappingList.append(
                {
                    "geography": geographies,
                    "is_active": isActive
                }
            )
            geoMappingDict[countryId] = geoMappingList
            self.countryList = CountryList().getCountry()
        return [
            "success", 
            {
                "countries": self.countryList,
                "geographies": geoMappingDict
            }
            
        ]

class Statutory(object) :
    def __init__(self, statutoryId, name, levelId, parentIds, parentMappings) :
        self.statutoryId = statutoryId
        self.name = name
        self.levelId = levelId
        self.parentIds = parentIds
        self.parentMappings = parentMappings
        self.verify()
    
    def verify(self) :
        assertType(self.statutoryId, IntType)
        assertType(self.name, StringType)
        assertType(self.levelId, IntType)
        assertType(self.parentIds, ListType)
        assertType(self.parentMappings, StringType)

    def toStructure(self) :
        return {
            "statutory_id": self.statutoryId, 
            "statutory_name": self.name,
            "level_id": self.levelId,
            "parent_ids": self.parentIds,
            "parent_id": self.parentIds[-1],
            "parent_mappings": self.parentMappings
        }

    def __repr__(self) :
        return str(self.toStructure())

class StatutoryApi (object) :
    def __init__(self, request, userId) :
        self.request = request
        self.userId = userId
        self.responseData = None
        self.statutories = {}

    def getStatutories(self) :
        DH = DatabaseHandler.instance()
        _statutoryDict = DH.getAllStatutories()
        for key, value in _statutoryDict.iteritems() :
            # parentIds = [int(x) for x in row[3][:-1].split(',')]

            statutory = Statutory(key, value[0], value[1], value[2], value[3])
            countryId = int(value[4])
            domainId = int(value[5])
            _list = []
            _countryWise = self.statutories.get(countryId)
            if _countryWise is None :
                _countryWise = {}
            else :
                _list = _countryWise.get(domainId)
                if _list is None :
                    _list = []
            _list.append(statutory.toStructure())
            _countryWise[domainId] = _list
            self.statutories[countryId] = _countryWise
        return self.statutories

    def saveStatutory(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        assertType(requestData, DictType)
        statutoryName = JSONHelper.getString(requestData, "statutory_name")
        levelId = JSONHelper.getInt(requestData, "statutory_level_id")
        parentIdsList = JSONHelper.getList(requestData, "parent_ids")
        parentIds = ','.join(str(x) for x in parentIdsList) + ","
        statutoryNames = [row[1].lower() for row in DH.getDuplicateStatutories(parentIds, None)]
        if statutoryNames.count(statutoryName.lower()) > 0:
            self.responseData = "StatutoryNameAlreadyExists"
        else :
            if (DH.saveStatutories(statutoryName, levelId, parentIds, self.userId)) :
                self.responseData = "success"
            else :
                self.responseData = "saveFailed: %s" % requestData

        return [
            str(self.responseData),
            {}
        ]

    def updateStatutory(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        assertType(requestData, DictType)
        statutoryId = JSONHelper.getInt(requestData, "statutory_id")
        statutoryName = JSONHelper.getString(requestData, "statutory_name")
        levelId = JSONHelper.getInt(requestData, "statutory_level_id")
        parentIdsList = JSONHelper.getList(requestData, "parent_ids")
        parentIds = ','.join(str(x) for x in parentIdsList) + ","
        statutoryNames = [row[1].lower() for row in DH.getDuplicateStatutories(parentIds, statutoryId)]
        if statutoryNames.count(statutoryName.lower()) > 0:
            self.responseData = "StatutoryNameAlreadyExists"
        else :
            if (DH.updateStatutories(statutoryId, statutoryName, parentIds, self.userId)) :
                self.responseData = "success"
            else :
                self.responseData = "updateFailed: %s" % requestData

        return [
            str(self.responseData),
            {}
        ]

    def updateStatutoryMappingId(self, mappingId, statutoryIds) :
        pass
        
class Compliance(object) :
    def __init__(
            self, complianceId, statutoryProvition, complianceTask,
            description, documentName, formatFileName, penalDescription,
            complianceFrequency, statutoryDates,
            repeatsType, repeatsEvery, durationType, duration, isActive
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
        assertType(self.approvalStatus, StringType)
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


class StatutoryMappingApi(object):
    def __init__(self, request, userId) :
        self.request = request
        assertType(self.request[1], DictType)
        self.userId = userId
        self.responseData = None
        self.countryList = CountryList().getCountry()
        self.domainList = DomainList().getDomains()
        self.industryList = IndustryList().getIndustries()
        self.statutoryNatureList = StatutoryNatureList().getStatutoryNatures()
        self.statutoryLevelList = StatutoryLevelsList().getStatutoryLevels()
        self.statutories= StatutoryApi(request, userId).getStatutories()
        self.geographyLevelList = GeographyLevelList().getGeographyLevels()
        self.geographies= GeographyAPI(request, userId).getGeographyList()
        self.statutoryMappings = {}

    def getStatutoryMappings(self) :
        DH = DatabaseHandler.instance()
        _staturoyMapList = DH.getStautoryMappings()
        _statutoryMappings = DH.allStatutories
        for row in _staturoyMapList :
            mappingId = int(row[0])
            countryId = int(row[1])
            countryName = row[2]
            domainId = int(row[3])
            domainName = row[4]
            industryIds = [int(x) for x in row[5][:-1].split(',')]
            statutoryNatureId = int(row[6])
            statutoryNatureName = row[7]
            statutoryIds = [int(x) for x in row[8][:-1].split(',')]
            statutoryMappings = [_statutoryMappings.get(x)[1] for x in statutoryIds ]
            complianceIds = [int(x) for x in row[9][:-1].split(',')]
            geographyIds = [int(x) for x in row[10][:-1].split(',')]
            approvalStatus = row[11]
            isActive = row[12]
            mapping = StatutoryMapping (
                countryId, countryName, domainId, domainName, 
                industryIds, statutoryNatureId, statutoryNatureName, 
                statutoryIds, statutoryMappings, complianceIds, 
                geographyIds, approvalStatus, isActive
            )
            self.statutoryMappings[mappingId] = mapping.toStructure()
            
        return [
            "GetStatutoryMappingsSuccess",
            {
                "countries": self.countryList,
                "domains": self.domainList,
                "industries": self.industryList,
                "statutory_natures": self.statutoryNatureList,
                "statutory_levels": self.statutoryLevelList,
                "statutories": self.statutories,
                "geography_levels": self.geographyLevelList,
                "geographies": self.geographies,
                "statutory_mappings": self.statutoryMappings
            }
        ]

    def saveStatutoryMapping(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        assertType(requestData, DictType)
        if (DH.saveStatutoryMapping(requestData, self.userId)) :
            self.responseData = "success"
        else :
            self.responseData = "saveFailed"

        return [
            str(self.responseData),
            {}
        ]

    def updateStatutoryMapping(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        if (DH.updateStatutoryMapping(requestData, self.userId)) :
            self.responseData = "success"
        else :
            self.responseData = "updateFailed"

        return [
            str(self.responseData),
            {}
        ]

    def changeStatutoryMappingStatus(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        if (DH.changeStatutoryMappingStatus(requestData, self.userId)) :
            self.responseData = "success"
        else :
            self.responseData = "StatusUpdateFailed"
        return [
            str(self.responseData),
            {}
        ]

    def changeApprovalStatus(self) :
        DH = DatabaseHandler.instance()
        requestData = self.request[1]
        if (DH.changeApprovalStatus(requestData, self.userId)) :
            self.responseData = "success"
        else :
            self.responseData = "StatusUpdateFailed"
        return [
            str(self.responseData),
            {}
        ]

    def getLevel1Statutories(self) :
        DH = DatabaseHandler.instance()
        rows = DH.getCountryWiseLevel1Statutories()
        statutories = {}
        for row in rows :
            parentIds = [int(x) for x in row[3][:-1].split(',')]
            statutory = Statutory(int(row[0]), row[1], int(row[2]), parentIds)
            countryId = int(row[4])
            domainId = int(row[6])
            _list = []
            _countryWise = statutories.get(countryId)
            if _countryWise is None :
                _countryWise = {}
            else :
                _list = _countryWise.get(domainId)
                if _list is None :
                    _list = []
            _list.append(statutory.toStructure())
            _countryWise[domainId] = _list
            statutories[countryId] = _countryWise
        return statutories

    def getReportFilters(self) :
        DH = DatabaseHandler.instance()
        return [
            "GetStatutoryMappingReportFiltersSuccess",
            {
                "countries": self.countryList,
                "domains": self.domainList,
                "industries": self.industryList,
                "statutory_natures": self.statutoryNatureList,
                "geographies": self.geographies,
                "level_1_statutories": self.getLevel1Statutories()
            }
        ]

    def getReportData(self) :
        DH = DatabaseHandler.instance()
