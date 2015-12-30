import datetime
import MySQLdb as mysql

__all__ = [
    "KnowledgeDatabase", "ClientDatabase"
]


class Database(object) :
    def __init__(
        self, 
        mysqlHost, mysqlUser, 
        mysqlPassword, mysqlDatabase
    ):
        self._mysqlHost = mysqlHost
        self._mysqlUser = mysqlUser
        self._mysqlPassword = mysqlPassword
        self._mysqlDatabase = mysqlDatabase
        self._connection = None
        self._cursor = None 

    def cursor(self):
        return self._cursor
 
    def connect(self):
        assert self._connection is None
        connection = mysql.connect(
            self._mysqlHost, self._mysqlUser, 
            self._mysqlPassword, self._mysqlDatabase
        )
        connection.autocommit(False)
        self._connection = connection

    def close(self):
        assert self._connection is not None
        self._connection.close()
        self._connection = None

    def begin(self):
        self.connect()
        assert self._connection is not None
        assert self._cursor is None
        self._cursor = self._connection.cursor()
        return self._cursor

    def commit(self):
        assert self._connection is not None
        assert self._cursor is not None
        self._cursor.close()
        self._connection.commit()
        self._cursor = None
        self.close()

    def rollback(self):
        assert self._connection is not None
        assert self._cursor is not None
        self._cursor.close()
        self._connection.rollback()
        self._cursor = None
        self.close()

    def select_all(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query)
        return cursor.fetchall()

    def select_one(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    def execute(self, query) :
        cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query)


    def call_proc(self, procedure_name, args):
        # args is tuple e.g, (parm1, parm2)
        cursor = self.cursor()
        assert cursor is not None
        print "calling proc", procedure_name, args
        cursor.callproc(procedure_name, args)
        print "end proc", procedure_name
        result = cursor.fetchall()
        return result

class KnowledgeDatabase(Database):
    def __init__(
        self, 
        mysqlHost, mysqlUser, 
        mysqlPassword, mysqlDatabase
    ):
        super(KnowledgeDatabase, self).__init__(
            mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase
        )

    # def get_user(self, user_id):
    #   query = "select * from users"
    #   return self.select_all(query)

    # def insert_user(self, username, user_id):
    #   query = "INSERT INTO USERS(username, user_id) VALUES (%s, %s)" % (
    #       username, user_id
    #   )
    #   self.execute(query)

    # def update_user(self, username, user_id):
    #   query = "UPDATE USERS SET username= %s WHERE user_id = %s" % (
    #       username, user_id
    #   )
    #   self.execute(query)

    def validate_session_token(self, session_token) :
        # query = "CALL sp_validate_session_token ('%s');" % (session_token)
        query = "SELECT user_id FROM tbl_user_sessions \
            WHERE session_token = '%s'" % (session_token)
        row = self.select_one(query)
        user_id = row[0]
        return user_id

    def get_data(self, table, columns, condition):
        # query = "SELECT "+columns+" FROM "+table+" WHERE "+condition 
        query = "SELECT %s FROM %s WHERE %s "  % (table, columns, condition)
        return self.select_all(query)

    def get_data_from_multiple_tables(self, columns, tables, aliases, joinType, joinConditions, whereCondition):
        query = "SELECT %s FROM " % columns

        for index,table in enumerate(tables):
            if index == 0:
                query += "%s  %s  %s" % (table, aliases[index], joinType)
            elif index <= len(tables) -2:
                query += " %s %s on (%s) %s " % (table, aliases[index], joinConditions[index-1], joinType)
            else:
                query += " %s %s on (%s)" % (table, aliases[index],joinConditions[index-1])

        query += " where %s" % whereCondition
        return self.select_all(query)


    def verify_login(self, username, password):
        tblAdminCondition = "password='%s' and user_name='%s'" % (password, username)
        admin_details = self.get_data("tbl_admin", "*", tblAdminCondition)
        if (len(admin_details) == 0) :
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, t1.address, t1.designation \
                t2.user_group_name, t2.form_ids \
                FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
                ON t1.user_group_id = t2.user_group_id \
                WHERE t1.password='%s' and t1.email_id='%s'" % (password, username)
            return self.select_one(query)
        else :
            return True

    def add_session(self, user_id) :
        session_id = self.new_uuid()
        query = "insert into tbl_user_sessions values ('%s', '%s', '%d');"
        query = query % (session_id, user_id, current_timestamp())
        self.execute(query)
        return session_id

    def get_new_id(self, field , table_name) :
        newId = 1
        query = "SELECT max(%s) from %s " % (field, table_name)

        row = self.select_one(query)
        if row[0] is not None :
            newId = int(row[0]) + 1
        return newId

    def get_date_time(self) :
        return datetime.datetime.now()

    def save_activity(self, user_id, form_id, action):
        createdOn = self.get_date_time()
        activityId = self.get_new_id("activity_log_id", "tbl_activity_log")
        query = "INSERT INTO tbl_activity_log(activity_log_id, user_id, form_id, \
            action, created_on) \
            VALUES (%s, %s, %s, '%s', '%s')" % (
                activityId, user_id, form_id, action, createdOn
            )
        self.execute(query)

  #
  # Domain
  #

    def get_domains_for_user(self, user_id) :
        # query = "CALL sp_get_domains_for_user (%s)" % (user_id)
        query = "SELECT distinct t1.domain_id, t1.domain_name, t1.is_active FROM tbl_domains t1 "
        if user_id > 0 :
            query = query + " INNER JOIN tbl_user_domains t2 ON t1.domain_id = t2.domain_id WHERE t2.user_id = %s" % (user_id)
        result = self.select_all(query)
        return result
    
    def save_domain(self, domain_name, user_id) :
        createdOn = self.get_date_time()
        domain_id = self.get_new_id("domain_id", "tbl_domains")
        is_active = 1

        query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, \
            created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            domain_id, domain_name, is_active, user_id, createdOn
        )
        self.execute(query)
        action = "Add Domain - \"%s\"" % domain_name
        self.save_activity(user_id, 4, action)
        return True

    def check_duplicate_domain(self, domain_name, domain_id) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_domains \
            WHERE LOWER(domain_name) = LOWER('%s') " % domain_name
        if domain_id is not None :
            query = query + " AND domain_id != %s" % domain_id
        row = self.select_one(query)
        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def get_domain_by_id(self, domain_id) :
        q = "SELECT domain_name FROM tbl_domains WHERE domain_id=%s" % domain_id
        row = self.select_one(q)
        domain_name = row[0]
        return domain_name

    def update_domain(self, domain_id, domain_name, updated_by) :
        oldData = self.get_domain_by_id(domain_id)
        if oldData is None :
            return False
        else :
            query = "UPDATE tbl_domains SET domain_name = '%s', \
            updated_by = %s WHERE domain_id = %s" % (
                domain_name, updated_by, domain_id
            )
            self.execute(query)
            action = "Edit Domain - \"%s\"" % domain_name
            self.save_activity(updated_by, 4, action)
            return True

    def update_domain_status(self, domain_id, is_active, updated_by) :
        oldData = self.get_domain_by_id(domain_id)
        if oldData is None :
            return False
        else :
            query = "UPDATE tbl_domains SET is_active = %s, \
            updated_by = %s WHERE domain_id = %s" % (
                is_active, updated_by, domain_id
            )
            self.execute(query)
            if is_active == 0 :
                status = "deactivated"
            else:
                status = "activated"
            action = "Domain %s status  - %s" % (oldData, status)
            self.save_activity(updated_by, 4, action)
            return True

    #
    # Country
    #

    def get_countries_for_user(self, user_id) :
        query = "SELECT distinct t1.country_id, t1.country_name, t1.is_active FROM tbl_domains t1 "
        if user_id > 0 :
            query = query + " INNER JOIN tbl_user_countries t2 ON t1.domain_id = t2.domain_id WHERE t2.user_id = %s" % (user_id)
        result = self.select_all(query)
        return result
    
    def get_country_by_id(self, country_id) :
        q = "SELECT country_name FROM tbl_countries WHERE country_id=%s" % country_id
        row = self.select_one(q)
        country_name = row[0]
        return country_name

    def check_duplicate_country(self, country_name, country_id) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_countries \
        WHERE LOWER(country_name) = LOWER('%s') " % country_name
        if country_id is not None :
            query = query + " AND country_id != %s" % country_id
        row = self.select_one(query)
        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate


    def save_country(self, country_name, created_by) :
        createdOn = self.get_date_time()
        country_id = self.get_new_id("country_id", "tbl_countries")
        is_active = 1

        query = "INSERT INTO tbl_countries(country_id, country_name, \
            is_active, created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            country_id, country_name, is_active, created_by, createdOn
        )
        self.execute(query)
        action = "Add Country - \"%s\"" % country_name
        self.save_activity(created_by, 4, action)
        return True

    def update_country(self, country_id, country_name, updated_by) :
        oldData = self.get_country_by_id(country_id)
        if oldData is None :
            return False
        else :
            query = "UPDATE tbl_countries SET country_name = '%s', \
            updated_by = %s WHERE country_id = %s" % (
                country_name, updated_by, country_id
            )
            self.execute(query)
            action = "Edit Country - \"%s\"" % country_name
            self.save_activity(updated_by, 3, action)
            return True

    def update_country_status(self, country_id, is_active, updated_by) :
        oldData = self.get_country_by_id(country_id)
        if oldData is None :
            return False
        else :
            query = "UPDATE tbl_countries SET is_active = %s, \
            updated_by = %s WHERE country_id = %s" % (
                is_active, updated_by, country_id
            )
            if is_active == 0:
                status = "deactivated"
            else:
                status = "activated"
            self.execute(query)
            action = "Country %s status  - %s" % (oldData, status)
            self.save_activity(updated_by, 3, action)
            return True



    def get_user_forms(self, form_ids):
        forms = []

        columns = "tf.form_id, tf.form_category_id, tfc.form_category, tf.form_type_id, tft.form_type,"+\
        "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormCategory, self.tblFormType]
        aliases = ["tf", "tfc", "tft"]
        joinConditions = ["tf.form_category_id = tfc.form_category_id", "tf.form_type_id = tft.form_type_id"]
        whereCondition = " tf.form_id in ('%s') order by tf.form_order" % (form_ids)
        joinType = "left join"

        rows = self.get_data_from_multiple_tables(columns, tables, aliases, joinType, 
            joinConditions, whereCondition)
        return rows 
