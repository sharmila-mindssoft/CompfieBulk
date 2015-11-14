import datetime
import MySQLdb as mysql

from models import *

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


    def checkDuplicateDomain(self, domainName, domainId) :
        con = None
        cursor = None
        domainNames = []
        isDuplicate = False
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            query = "SELECT count(*) FROM tbl_domains WHERE LOWER(domain_name) = LOWER('%s') " % domainName
            if domainId is not None :
                query = query + " AND domain_id != %s" % domainId
            cursor.execute(query)
            row = cursor.fetchone()
            if row[0] > 0 :
                isDuplicate = True

        except mysql.Error, e:
            print ("error while checking duplicate domain: %s", e)
        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()
        return isDuplicate

    def getDomainId(self) :
        con = None
        cursor = None
        domainId = 1
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            query = "SELECT max(domain_id) FROM tbl_domains "
            cursor.execute(query)
            row = cursor.fetchone()
            if row[0] is not None:
                domainId = row[0] + 1 

        except mysql.Error, e:
            print ("error while getting domain_id: %s", e)
        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()
        return domainId
            
    def getDomains(self) :
        con = None
        cursor = None
        domainList = []
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            query = "SELECT domain_id, domain_name, is_active FROM tbl_domains "
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows :
                domain = Domain(int(row[0]), row[1], row[2])
                domainList.append(domain)

        except  mysql.Error, e :
            print ("error loading domain lists: %s", e)
        
        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()
        return domainList

    def saveDomain(self, domainName, createdBy) :
        con = None
        cursor = None
        createdOn = datetime.datetime.now()
        domainId = self.getDomainId()
        isActive = 1
        isSaved = True
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, created_by, created_on)" + \
            " VALUES (%s, '%s', %s, %s, '%s') " % (domainId, domainName, isActive, createdBy, createdOn)
            cursor.execute(query)
            con.commit()

        except mysql.Error, e:
            print ("error, while saving domain: %s ", e)
            isSaved = False
        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()
        return isSaved

    def updateDomain(self, domainId, domainName, updatedBy) :
        con = None
        cursor = None
        isUpdated = True
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            q = "SELECT count(*) FROM tbl_domains WHERE domain_id=%s" % domainId
            cursor.execute(q)
            row = cursor.fetchone()
            if row[0] > 0 :
                query = "UPDATE tbl_domains SET domain_name = '%s', updated_by = %s WHERE domain_id = %s" % (
                    domainName, updatedBy, domainId
                )
                cursor.execute(query)
                con.commit()
            else :
                isUpdated = False

        except mysql.Error, e:
            print ("error while updating domain: %s ", e)
            isUpdated = False
        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()
        return isUpdated

    def updateDomainStatus(self, domainId, isActive, updatedBy) :
        con = None
        cursor = None
        isUpdated = True
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            q = "SELECT count(*) FROM tbl_domains WHERE domain_id=%s" % domainId
            cursor.execute(q)
            row = cursor.fetchone()
            if row[0] > 0 :
                query = "UPDATE tbl_domains SET is_active = %s, updated_by = %s WHERE domain_id = %s" % (
                    isActive, updatedBy, domainId
                )
                cursor.execute(query)
                con.commit()
            else :
                isUpdated = False

        except mysql.Error, e:
            print ("error while updating domain status: %s ", e)
            isUpdated = False
        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()
        return isUpdated


    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
        return _databaseHandlerInstance
