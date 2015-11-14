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
        self.mysqlPassword = "minds"
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
        query = "SELECT user_id FROM tbl_user_sessions WHERE session_id = '%s'" % sessionToken
        rows = self.dataSelect(query)
        row = rows[0]
        return row[0]

    ### Domain ###

    def checkDuplicateDomain(self, domainName, domainId) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_domains WHERE LOWER(domain_name) = LOWER('%s') " % domainName
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

        query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, created_by, created_on)" + \
            " VALUES (%s, '%s', %s, %s, '%s') " % (domainId, domainName, isActive, createdBy, createdOn)

        return self.dataInsertUpdate(query)

    def getDomainByDomainId(self, domainId) :
        q = "SELECT domain_name FROM tbl_domains WHERE domain_id=%s" % domainId
        rows = self.dataSelect(q)
        domainName = rows[0][0]
        return domainName

    def updateDomain(self, domainId, domainName, updatedBy) :
        
        oldData = self.getDomainByDomainId(domainId)
        if oldData is not None :
            query = "UPDATE tbl_domains SET domain_name = '%s', updated_by = %s WHERE domain_id = %s" % (
                domainName, updatedBy, domainId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    def updateDomainStatus(self, domainId, isActive, updatedBy) :
        oldData = self.getDomainByDomainId(domainId)
        if oldData is not None :
            query = "UPDATE tbl_domains SET is_active = %s, updated_by = %s WHERE domain_id = %s" % (
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
        query = "SELECT count(*) FROM tbl_countries WHERE LOWER(country_name) = LOWER('%s') " % countryName
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

        query = "INSERT INTO tbl_countries(country_id, country_name, is_active, created_by, created_on)" + \
            " VALUES (%s, '%s', %s, %s, '%s') " % (countryId, countryName, isActive, createdBy, createdOn)

        return self.dataInsertUpdate(query)

    def getCountryByCountryId(self, countryId) :
        q = "SELECT country_name FROM tbl_countries WHERE country_id=%s" % countryId
        rows = self.dataSelect(q)
        countryName = rows[0][0]
        return countryName

    def updateCountry(self, countryId, countryName, updatedBy) :
        oldData = self.getCountryByCountryId(countryId)
        if oldData is not None :
            query = "UPDATE tbl_countries SET country_name = '%s', updated_by = %s WHERE country_id = %s" % (
                countryName, updatedBy, countryId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    def updateCountryStatus(self, countryId, isActive, updatedBy) :
        oldData = self.getCountryByCountryId(countryId)
        if oldData is not None :
            query = "UPDATE tbl_countries SET is_active = %s, updated_by = %s WHERE country_id = %s" % (
                isActive, updatedBy, countryId
            )
            return self.dataInsertUpdate(query)
        else :
            return False

    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
        return _databaseHandlerInstance
