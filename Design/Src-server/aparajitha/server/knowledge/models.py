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
    "Level", "StatutoryLevelList", "SaveStatutoryLevel", "GeographyLevelList",
    "SaveGeographyLevel"
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
        return {
            str(self.possibleError),
            {}
        }

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

    def toList(self) :
        return self.countryList

    def toStructure(self) :
        return [
            "success",
            {"countries": self.countryList}
        ]

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

    def toStructure(self) :
        return [
            "success",
            {"industries": self.industryList}
        ]

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

    def toStructure(self) :
        return [
            "success",
            {"industries": self.statutoryNatureList}
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

class StatutoryLevelList(object) :
    def __init__(self) :
        self.statutoryLevels = {}
        self. countryList = []
        self.processData()

    def processData(self) :
        self.countryList = CountryList().toList()
        _statutoryLevels = DatabaseHandler.instance().getStatutoryLevels()
        for row in _statutoryLevels :
            statutoryLevel = Level(int(row[0]), int(row[1]), row[2])
            countryId = int(row[3])
            _list = self.statutoryLevels.get(countryId)
            if _list is None :
                _list = []
            _list.append(statutoryLevel.toStructure())
            self.statutoryLevels[countryId] = _list

    def toStructure(self) :
        return [
            "success",
            {
                "countries": self.countryList,
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
        levels = JSONHelper.getList(requestData, "levels")
        savedNames = [row[2] for row in DH.getGeographyLevelsByCountry(countryId)]
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

                if (DH.saveStatutoryLevel(countryId, levelId, name, position, self.userId)) :
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
        self.countryList = CountryList().toList()
        _geographyLevels = DatabaseHandler.instance().getGeographyLevels()
        for row in _geographyLevels :
            geographyLevel = Level(int(row[0]), int(row[1]), row[2])
            countryId = int(row[3])
            _list = self.geographyLevels.get(countryId)
            if _list is None :
                _list = []
            _list.append(geographyLevel.toStructure())
            self.geographyLevels[countryId] = _list

    def toStructure(self) :
        return [
            "success",
            {
                "countries": self.countryList,
                "geography_levels": self.geographyLevels
            }
        ]

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
    def __init__(self, request) :
        self.request = request
        self.statutoryNatureList = []
        self.possibleError = None
        self.processData()

    def processData(self) :
        _statutoryNatures = DatabaseHandler.instance().getStatutoryNatures()
        for row in _statutoryNatures :
            statutoryNature = StatutoryNature(int(row[0]), row[1], row[2])
            self.statutoryNatureList.append(statutoryNature)

    def toStructure(self) :
        if self.possibleError is not None :
            return [
                str(self.possibleError),
                {}
            ]
        else :
            return [
                "success",
                {"industries": self.statutoryNatureList}
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

