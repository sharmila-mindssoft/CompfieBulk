__all__ = [
    "Country",
    "Domain"
]

class Country(object) :
    def __init__(self, countryId, countryName, isActive) :
        self.countryId = countryId
        self.countryName = countryName
        self.isActive = isActive

    def toStructure(self) :
        return {
            "country_id": self.countryId,
            "country_name": self.countryName,
            "is_active": self.isActive
        }

    @classmethod
    def getList(self, db):
        countryList = []
        # try:
        rows = db.getCountries()
        for row in rows:
            countryId = int(row[0])
            countryName = row[1]
            isActive = row[2]
            country = Country(countryId, countryName, isActive)
            countryList.append(country.toStructure())
        # except:
        #     print "Error: While fetching Countries"
        return countryList

class Domain(object) :
    def __init__(self, domainId, domainName, isActive) :
        self.domainId = domainId
        self.domainName = domainName
        self.isActive = isActive

    def toStructure(self) :
        return {
            "domain_id": self.domainId,
            "domain_name": self.domainName,
            "is_active": self.isActive
        }

    @classmethod
    def getList(self, db):
        domainList = []
        # try:
        rows = db.getDomains()
        for row in rows:
            domainId = int(row[0])
            domainName = row[1]
            isActive = row[2]
            domain = Domain(domainId, domainName, isActive)
            domainList.append(domain.toStructure())
        # except:
        #     print "Error: While fetching Countries"
        return domainList