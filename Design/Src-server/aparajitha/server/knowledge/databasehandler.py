import datetime
import MySQLdb as mysql


__all__ = [
    "DatabaseHandler"
]

_databaseHandlerInstance = None

class DatabaseHandler(object) :
    def __init__(self) :
        self.mysqlHost = "localhost"
        self.mysqlUser = "root"
        self.mysqlPassword = "123456"
        self.mysqlDatabase = "aparajitha_knowledge"

    def dbConnect(self) :
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword, self.mysqlDatabase
        )

    def dataInsertUpdate(self, query) :
        con = None
        cursor = None
        isComplete = True
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()

        except mysql.Error, e:
            print ("Error:%s - %s" % (query, e))
            isComplete = False

        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()

        return isComplete

    def dataSelect(self, query) :
        con = None
        cursor = None
        result = None
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        except mysql.Error, e:
            print ("Error:%s - %s" % (query, e))

        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()

        return result

    def validateSessionToken(self, sessionToken) :
        query = "SELECT user_id FROM tbl_user_sessions \
        WHERE session_id = '%s'" % sessionToken
        rows = self.dataSelect(query)
        row = rows[0]
        return row[0]

    ### Domain ###

    def checkDuplicateDomain(self, domainName, domainId) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_domains \
        WHERE LOWER(domain_name) = LOWER('%s') " % domainName
        if domainId is not None :
            query = query + " AND domain_id != %s" % domainId
        rows = self.dataSelect(query)
        row = rows[0]

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def getDomainId(self) :
        domainId = 1
        query = "SELECT max(domain_id) FROM tbl_domains "
        rows = self.dataSelect(query)

        for row in rows :
            if row[0] is not None :
                domainId = row[0] + 1

        return domainId
            
    def getDomains(self) :
        query = "SELECT domain_id, domain_name, is_active FROM tbl_domains "
        return self.dataSelect(query)

    def saveDomain(self, domainName, createdBy) :
        createdOn = datetime.datetime.now()
        domainId = self.getDomainId()
        isActive = 1

        query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, \
            created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            domainId, domainName, isActive, createdBy, createdOn
        )

        return self.dataInsertUpdate(query)

    def getDomainByDomainId(self, domainId) :
        q = "SELECT domain_name FROM tbl_domains WHERE domain_id=%s" % domainId
        rows = self.dataSelect(q)
        domainName = rows[0][0]
        return domainName

    def updateDomain(self, domainId, domainName, updatedBy) :
        
        oldData = self.getDomainByDomainId(domainId)
        if oldData is not None :
            query = "UPDATE tbl_domains SET domain_name = '%s', \
            updated_by = %s WHERE domain_id = %s" % (
                domainName, updatedBy, domainId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    def updateDomainStatus(self, domainId, isActive, updatedBy) :
        oldData = self.getDomainByDomainId(domainId)
        if oldData is not None :
            query = "UPDATE tbl_domains SET is_active = %s, \
            updated_by = %s WHERE domain_id = %s" % (
                isActive, updatedBy, domainId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    ### Country ###

    def getCountries(self) :
        query = "SELECT country_id, country_name, is_active FROM tbl_countries "
        return self.dataSelect(query)

    def checkDuplicateCountry(self, countryName, countryId) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_countries \
        WHERE LOWER(country_name) = LOWER('%s') " % countryName
        if countryId is not None :
            query = query + " AND country_id != %s" % countryId
        rows = self.dataSelect(query)
        row = rows[0]

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def getCountryId(self) :
        countryId = 1
        query = "SELECT max(country_id) FROM tbl_countries "
        rows = self.dataSelect(query)
        for row in rows :
            if row[0] is not None :
                countryId = int(row[0]) + 1
        return countryId

    def saveCountry(self, countryName, createdBy) :
        createdOn = datetime.datetime.now()
        countryId = self.getCountryId()
        isActive = 1

        query = "INSERT INTO tbl_countries(country_id, country_name, \
            is_active, created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            countryId, countryName, isActive, createdBy, createdOn
        )

        return self.dataInsertUpdate(query)

    def getCountryByCountryId(self, countryId) :
        q = "SELECT country_name FROM tbl_countries WHERE country_id=%s" % countryId
        rows = self.dataSelect(q)
        countryName = rows[0][0]
        return countryName

    def updateCountry(self, countryId, countryName, updatedBy) :
        oldData = self.getCountryByCountryId(countryId)
        if oldData is not None :
            query = "UPDATE tbl_countries SET country_name = '%s', \
            updated_by = %s WHERE country_id = %s" % (
                countryName, updatedBy, countryId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    def updateCountryStatus(self, countryId, isActive, updatedBy) :
        oldData = self.getCountryByCountryId(countryId)
        if oldData is not None :
            query = "UPDATE tbl_countries SET is_active = %s, \
            updated_by = %s WHERE country_id = %s" % (
                isActive, updatedBy, countryId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    ### Industry ###

    def getIndustries(self) :
        query = "SELECT industry_id, industry_name, is_active FROM tbl_industries "
        return self.dataSelect(query)

    def checkDuplicateIndustry(self, industryName, industryId) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_industries \
        WHERE LOWER(industry_name) = LOWER('%s') " % industryName
        if industryId is not None :
            query = query + " AND industry_id != %s" % industryId
        rows = self.dataSelect(query)
        row = rows[0]

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def getIndustryId(self) :
        industryId = 1
        query = "SELECT max(industry_id) FROM tbl_industries "
        rows = self.dataSelect(query)
        for row in rows :
            if row[0] is not None :
                industryId = int(row[0]) + 1
        return industryId

    def saveIndustry(self, industryName, createdBy) :
        createdOn = datetime.datetime.now()
        industryId = self.getIndustryId()
        isActive = 1

        query = "INSERT INTO tbl_industries(industry_id, industry_name, is_active, \
            created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            industryId, industryName, isActive, createdBy, createdOn
        )

        return self.dataInsertUpdate(query)

    def getIndustryByIndustryId(self, industryId) :
        q = "SELECT industry_name FROM tbl_industries WHERE industry_id=%s" % industryId
        rows = self.dataSelect(q)
        industryName = rows[0][0]
        return industryName

    def updateIndustry(self, industryId, industryName, updatedBy) :
        oldData = self.getIndustryByIndustryId(industryId)
        if oldData is not None :
            query = "UPDATE tbl_industries SET industry_name = '%s', \
            updated_by = %s WHERE industry_id = %s" % (
                industryName, updatedBy, industryId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    def updateIndustryStatus(self, industryId, isActive, updatedBy) :
        oldData = self.getIndustryByIndustryId(industryId)
        if oldData is not None :
            query = "UPDATE tbl_industries SET is_active = %s, updated_by = %s \
            WHERE industry_id = %s" % (
                isActive, updatedBy, industryId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    ### StatutoryNature ###

    def getStatutoryNatures(self) :
        query = "SELECT statutory_nature_id, statutory_nature_name, is_active \
            FROM tbl_statutory_natures "
        return self.dataSelect(query)

    def checkDuplicateStatutoryNature(self, statutoryNatureName, statutoryNatureId) :
        isDuplicate = False

        query = "SELECT count(*) FROM tbl_statutory_natures \
            WHERE LOWER(statutory_nature_name) = LOWER('%s') " % statutoryNatureName

        if statutoryNatureId is not None :
            query = query + " AND statutory_nature_id != %s" % statutoryNatureId
        rows = self.dataSelect(query)
        row = rows[0]

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def getStatutoryNatureId(self) :
        statutoryNatureId = 1
        query = "SELECT max(statutory_nature_id) FROM tbl_statutory_natures "

        rows = self.dataSelect(query)
        for row in rows :
            if row[0] is not None :
                statutoryNatureId = int(row[0]) + 1
        return statutoryNatureId

    def saveStatutoryNature(self, statutoryNatureName, createdBy) :
        createdOn = datetime.datetime.now()
        statutoryNatureId = self.getStatutoryNatureId()
        isActive = 1

        query = "INSERT INTO tbl_statutory_natures(statutory_nature_id, statutory_nature_name, \
            is_active, created_by, created_on)  VALUES (%s, '%s', %s, %s, '%s') " % (
                statutoryNatureId, statutoryNatureName, isActive, createdBy, createdOn
            )

        return self.dataInsertUpdate(query)

    def getStatutoryNatureById(self, statutoryNatureId) :
        q = "SELECT statutory_nature_name FROM tbl_statutory_natures \
            WHERE statutory_nature_id=%s" % statutoryNatureId
        rows = self.dataSelect(q)
        statutoryNatureName = rows[0][0]
        return statutoryNatureName

    def updateStatutoryNature(self, statutoryNatureId, statutoryNatureName, updatedBy) :
        oldData = self.getStatutoryNatureById(statutoryNatureId)
        if oldData is not None :
            query = "UPDATE tbl_statutory_natures SET statutory_nature_name = \'%s\', \
            updated_by = %s WHERE statutory_nature_id = %s" % (
                statutoryNatureName, updatedBy, statutoryNatureId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    def updateStatutoryNatureStatus(self, statutoryNatureId, isActive, updatedBy) :
        oldData = self.getStatutoryNatureById(statutoryNatureId)
        if oldData is not None :
            query = "UPDATE tbl_statutory_natures SET is_active = %s, \
            updated_by = %s WHERE statutory_nature_id = %s" % (
                isActive, updatedBy, statutoryNatureId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    ### StatutoryLevels ###

    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
        return _databaseHandlerInstance
