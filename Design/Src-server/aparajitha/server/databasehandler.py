import datetime
import os
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
        self.mysqlDatabase = "mirror_knowledge"

    def mysqlServerConnect(self):
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword
        )

    def dbConnect(self) :
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword, self.mysqlDatabase
        )

    def createDatabase(self, databaseName):
        con = None
        cursor = None
        isComplete = True
        try:
            con = self.mysqlServerConnect()
            cursor = con.cursor()
            query = "CREATE DATABASE "+databaseName
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
        query = "INSERT INTO %s (%s)  VALUES" % (table, columns)

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
        # query = "SELECT "+columns+" FROM "+table+" WHERE "+condition 
        query = "SELECT %s FROM %s WHERE %s "  % (table, columns, condition)
        return self.executeAndReturn(query)

    def getDataFromMultipleTables(self, columns, tables, conditions, joinType):

        query = "SELECT %s FROM " % columns

        for index,table in enumerate(tables):
            if index == 0:
                query += "%s alias%d  %s" % (table, index, joinType)
            elif index <= len(tables) -2:
                query += " %s alias%d on (alias%d.%s = alias%d.%s) %s " % (table, 
                    index, index-1, conditions[index-1][0], index, 
                    conditions[index-1][1], joinType)
            else:
                query += " %s alias%d on (alias%d.%s = alias%d.%s)" % (table, index,
                    index-1, conditions[index-1][0], index, conditions[index-1][1])

        return self.executeAndReturn(query)

    def validateSessionToken(self, sessionToken) :
        query = "SELECT user_id FROM tbl_user_sessions \
        WHERE session_id = '%s'" % sessionToken
        rows = self.executeAndReturn(query)
        row = rows[0]
        return row[0]

    def verifyPassword(self, password, userId, clientId):
        columns = "count(*)"
        condition = "password='%s' and user_id='%d'" % (password, userId)
        if clientId != None:
            condition += " and client_id='%d'" % clientId
        rows = self.getData("tbl_users", columns, condition)
        if(int(rows[0][0]) <= 0):
            return False
        else:
            return True

    def add_session(self, user_id) :
        session_id = self.new_uuid()
        query = "insert into tbl_user_sessions values ('%s', '%s', '%d');"
        query = query % (session_id, user_id, current_timestamp())
        self._db.execute(query)
        return session_id

    def verifyLogin(self, userName, password):
        tblAdminCondition = "password='%s' and user_name='%s'" % (password, userName)
        adminDetails = self.getData("tbl_admin", "*", tblAdminCondition)
        if (len(adminDetails) == 0) :
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, t1.address, t1.designation \
                t2.user_group_name, t2.form_ids \
                FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
                ON t1.user_group_id = t2.user_group_id \
                WHERE t1.password='%s' and t1.email_id='%s'" % (password, userName)
            return userDetails = self.executeAndReturn(query)
        else :
            return True

    def getForms(self, form_category_id, form_ids):
        query = "SELECT t1.form_id, t1.form_category_id, t1.form_type_id, t1.form_name, \
            t1.form_url, t1.form_order, t1.parent_menu, t2.form_category_name, t3.form_type_name \
            FROM tbl_forms t1 INNER JOIN tbl_form_category t2 ON t1.form_category_id = t2.form_category_id \
            INNER JOIN tbl_form_types t3 ON t1.form_type_id = t3.form_type_id "
        qry = ""

        if (form_category_id is not None) :
            qry = " WHERE t1.form_category_id = %s" % (form_category_id)
        if (form_ids is not None):
            ids = [int(x) for x in form_ids.split(',')]
            qry = " WHERE t1.form_id in '%s' " str(tuple(ids))

        return self.executeAndReturn(query + qry)

    def truncate(self, table):
        query = "TRUNCATE TABLE  %s;" % table
        return self.execute(query)

    @staticmethod
    def instance() :
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
        return _databaseHandlerInstance
