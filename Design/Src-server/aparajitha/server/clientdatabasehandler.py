import datetime
import os
import MySQLdb as mysql
from aparajitha.server.constants import ROOT_PATH

__all__ = [
    "ClientDatabaseHandler"
]

_databaseHandlerInstance = None 
sqlScriptPath = os.path.join(ROOT_PATH, "Src-client/files/desktop/common/clientdatabase/client-tables.sql")

class ClientDatabaseHandler(object) :
    def __init__(self,  databaseName) :
        self.mysqlHost = "localhost"
        self.mysqlUser = "root"
        self.mysqlPassword = "123456"
        self.mysqlDatabase = databaseName

    def dbConnect(self) :
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword, self.mysqlDatabase
        )

    def createClientDatabaseTables(self):
        fileObj = open(sqlScriptPath, 'r')
        sqlFile = fileObj.read()
        fileObj.close()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            if command != "":
                self.execute(command)
            else:
                continue


    def execute(self, query):
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

    def executeAndReturn(self, query) :
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

    def insert(self, table, columns, values) :
        query = "INSERT INTO "+table+" ("+columns+")" + \
            " VALUES ("+values+")"     
        return self.execute(query)

    def bulkInsert(self, table, columns, valueList) :
        query = "INSERT INTO %s (%s) VALUES" % (table, columns)

        for index, value in enumerate(valueList):
            if index < len(valueList)-1:
                query += +"%s," % str(value)
            else:
                query += str(value)
        return self.execute(query)

    def update(self, table, columns, values, condition) :
        query = "UPDATE "+table+" set "
        for index,column in enumerate(columns):
            if index < len(columns)-1:
                query += column+" = '"+str(values[index])+"', "
            else:
                query += column+" = '"+str(values[index])+"' "

        query += " WHERE "+condition

        return self.execute(query)

    def onDuplicateKeyUpdate(self, table, columns, valueList, updateColumnsList):
        query = "INSERT INTO %s (%s) VALUES " % (table, columns)

        for index, value in enumerate(valueList):
            if index < len(valueList)-1:
                query += "%s," % str(value)
            else:
                query += "%s" % str(value)

        query += " ON DUPLICATE KEY UPDATE "

        for index, updateColumn in enumerate(updateColumnsList):

            if index < len(updateColumnsList)-1:
                query += "%s = VALUES(%s)," % (updateColumn, updateColumn)
            else:
                query += "%s = VALUES(%s)" % (updateColumn, updateColumn)

        return self.execute(query)

    def generateNewId(self, table, column):
        query = "SELECT max("+column+") FROM "+table
        rows = self.executeAndReturn(query)

        for row in rows :
            newId = row[0] + 1 if row[0] != None else 1

        return int(newId)

    def isAlreadyExists(self, table, condition) :
        query = "SELECT count(*) FROM "+table+" WHERE "+condition
        rows = self.executeAndReturn(query)     
        if rows[0][0] > 0:
            return True
        else : 
            return False

    def getData(self, table, columns, condition):
        query = "SELECT "+columns+" FROM "+table+" WHERE "+condition
        return self.executeAndReturn(query)

    def validateSessionToken(self, sessionToken) :
        query = "SELECT user_id FROM tbl_user_sessions \
        WHERE session_id = '%s'" % sessionToken
        rows = self.executeAndReturn(query)
        row = rows[0]
        return row[0]

    def delete(self, table, condition):
        query = "DELETE from "+table+" WHERE "+condition
        return self.execute(query)        

    def append(self, table, column, value, condition):
        rows = self.getData(table, column, condition)
        currentValue = rows[0][0]
        if currentValue != None:
            newValue = currentValue+","+str(value)
        else:
            newValue = str(value)
        columns = [column]
        values = [newValue]
        return self.update(table, columns, values, condition)

    def truncate(self, table):
        query = "TRUNCATE TABLE  %s;" % table
        return self.execute(query)

    @staticmethod
    def instance(databaseName) :
        global _databaseHandlerInstance
        _databaseHandlerInstance = None 
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = ClientDatabaseHandler(databaseName)
        return _databaseHandlerInstance
