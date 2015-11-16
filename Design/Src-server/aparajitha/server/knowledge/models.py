import json
from types import *

from databasehandler import DatabaseHandler


__all__ = [
    "JSONHelper", "Domain", "DomainList", 
    "SaveDomain", "UpdateDomain", "ChangeDomainStatus",
    "Country", "CountryList", "SaveCountry",
    "UpdateCountry", "ChangeCountryStatus"
]

def assertType (x, typeObject) :
    if type(x) is not typeObject :
        msg = "expected type %s, received invalid type  %s" % (typeObject, type(x))
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
    def __init__(self, sessionToken, request) :
        self.sessionToken = sessionToken
        self.request = request
        self.domainList = []
        self.userId = None
        self.possibleError = None
        self.processData()

    def processData(self) :
        self.userId = DatabaseHandler.instance().validateSessionToken(self.sessionToken)
        if self.userId is None :
            self.possibleError = "InvalidSessionToken"
        elif self.request[0] != "GetDomains" :
            self.possibleError = "InvalidRequest"
        else :
            _domains = DatabaseHandler.instance().getDomains()
            for row in _domains :
                domain = Domain(int(row[0]), row[1], row[2])
                self.domainList.append(domain)

    def toStructure(self) :
        if self.possibleError is not None :
            return [
                str(self.possibleError),
                {}
            ]
        else :
            return [
                "success",
                {"domains": self.domainList}
            ]


    def __repr__(self) :
        return str(self.toStructure())

class SaveDomain(object) :
    def __init__ (self, sessionToken, request) :
        self.sessionToken = sessionToken
        self.request = request
        self.responseData = None
        self.userId = None
        self.domainName = None
        self.processData()

    def processData(self) :
        self.userId = DatabaseHandler.instance().validateSessionToken(self.sessionToken)
        if self.userId is None :
            self.responseData = "InvalidSessionToken"
        elif self.request[0] != "SaveDomain" :
            self.responseData = "InvalidRequest"
        else :
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
    def __init__(self, sessionToken, request) :
        self.sessionToken = sessionToken
        self.request = request
        self.responseData = None
        self.userId = None
        self.domainId = None
        self.domainName = None
        self.processData()

    def processData(self) :
        self.userId = DatabaseHandler.instance().validateSessionToken(self.sessionToken)
        if self.userId is None :
            self.responseData = "InvalidSessionToken"
        elif self.request[0] != "UpdateDomain" :
            self.responseData = "InvalidRequest"
        else :
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
    def __init__(self, sessionToken, request) :
        self.sessionToken = sessionToken
        self.request = request
        self.userId = None
        self.domainId = None
        self.isActive = None
        self.responseData = None
        self.processData()

    def processData(self) :
        self.userId = DatabaseHandler.instance().validateSessionToken(self.sessionToken)
        if self.userId is None :
            self.responseData = "InvalidSessionToken"
        elif self.request[0] != "ChangeDomainStatus" :
            self.responseData = "InvalidRequest"
        else :
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
    def __init__(self, sessionToken, request) :
        self.sessionToken = sessionToken
        self.request = request
        self.countryList = []
        self.userId = None
        self.possibleError = None
        self.processData()

    def processData(self) :
        self.userId = DatabaseHandler.instance().validateSessionToken(self.sessionToken)
        if self.userId is None :
            self.possibleError = "InvalidSessionToken"
        elif self.request[0] != "GetCountries" :
            self.possibleError = "InvalidRequest"
        else :
            _countries = DatabaseHandler.instance().getCountries()
            for row in _countries :
                country = Country(int(row[0]), row[1], row[2])
                self.countryList.append(country)

    def toStructure(self) :
        if self.possibleError is not None :
            return [
                str(self.possibleError),
                {}
            ]
        else :
            return [
                "success",
                {"countries": self.countryList}
            ]

    def __repr__(self) :
        return str(self.toStructure())

class SaveCountry(object) :
    def __init__ (self, sessionToken, request) :
        self.sessionToken = sessionToken
        self.request = request
        self.responseData = None
        self.userId = None
        self.countryName = None
        self.processData()

    def processData(self) :
        self.userId = DatabaseHandler.instance().validateSessionToken(self.sessionToken)
        if self.userId is None :
            self.responseData = "InvalidSessionToken"
        elif self.request[0] != "SaveCountry" :
            self.responseData = "InvalidRequest"
        else :
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
    def __init__(self, sessionToken, request) :
        self.sessionToken = sessionToken
        self.request = request
        self.responseData = None
        self.userId = None
        self.countryId = None
        self.countryName = None
        self.processData()

    def processData(self) :
        self.userId = DatabaseHandler.instance().validateSessionToken(self.sessionToken)
        if self.userId is None :
            self.responseData = "InvalidSessionToken"
        elif self.request[0] != "UpdateCountry" :
            self.responseData = "InvalidRequest"
        else :
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
    def __init__(self, sessionToken, request) :
        self.sessionToken = sessionToken
        self.request = request
        self.userId = None
        self.countryId = None
        self.isActive = None
        self.responseData = None
        self.processData()

    def processData(self) :
        self.userId = DatabaseHandler.instance().validateSessionToken(self.sessionToken)
        if self.userId is None :
            self.responseData = "InvalidSessionToken"
        elif self.request[0] != "ChangeCountryStatus" :
            self.responseData = "InvalidRequest"
        else :
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