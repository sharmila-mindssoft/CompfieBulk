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

    def executeInsertUpdate(self, query):
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

    def insert(self, table, columns, values) :
        query = "INSERT INTO "+table+" ("+columns+")" + \
            " VALUES ("+values+")"
        return self.executeInsertUpdate(query)

    def generateNewId(self, table, column):
        query = "SELECT max("+column+") FROM "+table
        rows = self.dataSelect(query)

        for row in rows :
            newId = row[0] + 1 if row[0] != None else 1

        return int(newId)

    def isAlreadyExists(self, table, id_column_name, value_column_name,
        id, value) :
        query = "SELECT count(*) FROM "+table+" WHERE "+value_column_name+"='"+value+\
                "' AND "+id_column_name+" != '"+str(id)+"'"
        rows = self.dataSelect(query)        
        print rows[0][0]
        if rows[0][0] > 0:
            return True
        else : 
            return False

    def getData(self, table, columns):
        query = "SELECT "+columns+" FROM "+table
        return self.dataSelect(query)


    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
        return _databaseHandlerInstance
