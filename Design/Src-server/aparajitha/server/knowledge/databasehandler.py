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

    def checkDuplicateDomain(self, domainName, domainId) :
        domainNames = []
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

    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
        return _databaseHandlerInstance
