import os
import io
import MySQLdb as mysql
from server import logger
from server.common import (
    generate_random, generate_special_random
)


CLIENT_LE_DB_PREFIX = "compfie_le"
CLIENT_GROUP_PREFIX = "compfie_group"

'''
    these are the process will be performed in this class
    create database user,
    grand privileges,
    database creation,
    creation of tables, procedures and trigger
    and client specific knowledge data to created db
'''
class ClientDBBase(object):
    def __init__(
        self, db, client_id, short_name, email_id, database_ip, database_port,
        database_username, database_password
    ):
        logger.logGroup("ClientDBCreate", "inside client db create init")
        self._db = db
        self._client_id = client_id
        self._short_name = short_name
        self._email_id = email_id
        self._host = database_ip
        self._port = database_port
        self._username = database_username
        self._password = database_password

        self._db_name = None
        self._db_username = None
        self._db_password = None
        self._is_db_failed = False

        self._db_file_path = None
        self._db_prefix = None
        logger.logGroup("ClientDBCreate", "ClientDBCreate Begin")

    def process_error(self, message):
        logger.logGroup("process_error", message)
        return str(message)
        # raise ValueError(message)

    def db_create_name(self):
        return "%s_%s_%s" % (
            self._db_prefix, self._short_name.lower(), self._client_id
        )

    def db_create_username(self):
        return generate_random()

    def db_create_password(self):
        return generate_special_random()

    def get_db_constrains(self):
        self._db_name = self.db_create_name()
        self._db_username = self.db_create_username()
        self._db_password = self.db_create_password()
        return True

    def _mysql_server_connect(self, host, username, password, port):
        return mysql.connect(
            host=host, user=username, passwd=password, port=port
        )

    def _db_connect(self, host, username, password, database, port):
        return mysql.connect(
            host=host, user=username, passwd=password, db=database,
            port=port
        )

    def delete_database(self):
        con = self._mysql_server_connect(
            self._host, self._username, self._password, self._port
        )
        try:
            print con
            logger.logGroup("delete_database", "begin")
            cursor = con.cursor()
            print cursor
            query = "DROP DATABASE IF EXISTS %s" % self._db_name
            print query
            cursor.execute(query)
            print 'after drop'
            # drop created user here.
            con.commit()
            logger.logGroup("delete_database", "end")
        except mysql.Error, e:
            logger.logGroup("delete_database", str(e))
            print e
            con.rollback()
            raise Exception(e)

    def _create_db(self, cursor):
        try:
            query = "CREATE DATABASE %s" % self._db_name
            print query
            cursor.execute(query)
        except mysql.Error, ex:
            self._is_db_failed = True
            print ex
            logger.logGroup("_create_db", str(ex))
            e = "client db creation failed"
            print e
            logger.logGroup("_create_db", "failed")
            raise Exception(ex)

    def _grant_privileges(self, cursor):
        try:
            query = "GRANT SELECT, INSERT, UPDATE, " + \
                " DELETE ON %s.* to '%s'@'%s' IDENTIFIED BY '%s';"
            print query
            param = (
                self._db_name, self._db_username, str('%'), self._db_password
            )
            print param
            cursor.execute(query % param)
            cursor.execute("FLUSH PRIVILEGES;")
        except mysql.Error, ex:
            print ex
            logger.logGroup("_grant_privileges", str(ex))
            logger.logGroup("_grant_privileges", "failed")
            e = "client database user grant_privileges failed"
            print e
            raise Exception(ex)

    def _create_admin_user(self, cursor):
        try:
            query = "insert into tbl_users (user_category_id, client_id, employee_name, " + \
                " email_id " + \
                " )" + \
                " values (1, %s, 'Administrator', %s)"
            cursor.execute(query, [self._client_id, self._email_id])

        except mysql.Error, e:
            logger.logGroup("_create_admin_user", str(e))
            logger.logGroup("_create_admin_user", "failed")
            #  self.process_error(
            #     "admin user creation failed in client database"
            # )
            raise Exception(e)

    def _create_tables(self, cursor):
        # "scripts/mirror-client-group.sql"
        try:
            sql_script_path = os.path.join(
                os.path.join(os.path.split(__file__)[0], ".."),
                self._db_file_path
            )
            with io.FileIO(sql_script_path, "r") as file_obj:
                sql_file = file_obj.read()
                sql_commands = sql_file.split(';')
                size = len(sql_commands)
                for index, command in enumerate(sql_commands):
                    if (index < size-1):
                        # print command
                        cursor.execute(command)
                    else:
                        break
        except mysql.Error, e:
            print e
            logger.logGroup("_create_tables", str(e))
            logger.logGroup("_create_tables", "failed")
            # raise self.process_error(
            #     "table creation failed in client database"
            # )

    def prepare_db_constrains(self):
        result = self.get_db_constrains()
        if result is False:
            raise self.process_error("Prepare db_constrains failed")
        elif result is True:
            res = self._create_database()
            return res

    def begin_process(self):
        print "inside process begin"
        return self.prepare_db_constrains()

class ClientGroupDBCreate(ClientDBBase):
    def __init__(
        self, db, client_id, short_name, email_id, database_ip, database_port,
        database_username, database_password
    ):
        super(ClientGroupDBCreate, self).__init__(
            db, client_id, short_name, email_id, database_ip, database_port,
            database_username, database_password
        )
        self._db_prefix = CLIENT_GROUP_PREFIX
        self._db_file_path = "scripts/mirror-client-group.sql"

    def _create_database(self):
        db_con = None
        main_con = None
        try:
            temp_var = "%s, %s, %s" % (self._host, self._username, self._password)
            logger.logGroup("_create_database", temp_var)
            main_con = self._mysql_server_connect(
                self._host, self._username, self._password, self._port
            )
            print "main_con success"
            logger.logGroup("_create_database", "main connection success")
            main_cursor = main_con.cursor()
            self._create_db(main_cursor)
            logger.logGroup("_create_database", "create DB success")
            self._grant_privileges(main_cursor)
            logger.logGroup("_create_database", "create DB user success")
            main_con.commit()

            db_con = self._db_connect(
                self._host, self._username, self._password, self._db_name,
                self._port
            )
            db_cursor = db_con.cursor()
            logger.logGroup("_create_database", "client connection success")

            self._create_tables(db_cursor)
            logger.logGroup("_create_database", "table create success")

            self._create_admin_user(db_cursor)
            logger.logGroup("_create_database", "admin create success")
            # self._create_procedure(db_cursor)
            logger.logGroup("_create_database", "procedure create success")
            # self._create_trigger(db_cursor)
            logger.logGroup("_create_database", "trigger create success")

            db_con.commit()
            return (True, self._db_name, self._db_username, self._db_password)
        except Exception, e:
            print e
            print "main Exception"
            logger.logGroup("_create_database", str(e))
            if db_con is not None:
                db_con.rollback()
            if main_con is not None:
                main_con.rollback()
            if not self._is_db_failed :
                self.delete_database()
            raise Exception(e)

    def _create_procedure(self, cursor):
        try:
            p1 = "CREATE PROCEDURE `procedure_to_update_version` " + \
                " (IN update_type VARCHAR(100)) " + \
                " BEGIN " + \
                " SET SQL_SAFE_UPDATES=0; " + \
                " case  " + \
                " when update_type = 'unit' then " + \
                " SET @count = (SELECT unit_details_version+1 " + \
                " FROM tbl_mobile_sync_versions ); " + \
                " update tbl_mobile_sync_versions set " + \
                " unit_details_version = @count; " + \
                " when update_type = 'user' then " + \
                " SET @count = (SELECT user_details_version+1 " + \
                " FROM tbl_mobile_sync_versions ); " + \
                " update tbl_mobile_sync_versions set " + \
                " user_details_version = @count; " + \
                " when update_type = 'compliance' then " + \
                " SET @count = (SELECT compliance_applicability_version+1 " + \
                " FROM tbl_mobile_sync_versions ); " + \
                " update tbl_mobile_sync_versions set " + \
                " compliance_applicability_version = @count; " + \
                " when update_type = 'history' then " + \
                " SET @count = (SELECT compliance_history_version+1 " + \
                " FROM tbl_mobile_sync_versions ); " + \
                " update tbl_mobile_sync_versions set " + \
                " compliance_history_version = @count; " + \
                " end case; " + \
                " SET SQL_SAFE_UPDATES=1; " + \
                " END "
            cursor.execute(p1)
        except Exception, e:
            logger.logGroup("_create_procedure", str(e))
            logger.logGroup("_create_procedure", "failed")
            raise self.process_error(
                "procedure creation failed in client database"
            )

    def _create_trigger(self, cursor):
        try:
            t1 = "CREATE TRIGGER " + \
                " `after_tbl_statutory_notifications_units_insert` " + \
                " AFTER INSERT ON `tbl_statutory_notifications_units` " + \
                " FOR EACH ROW BEGIN " + \
                " INSERT INTO tbl_statutory_notification_status ( " + \
                " statutory_notification_id, " + \
                " user_id, read_status) " + \
                " SELECT NEW.statutory_notification_id, t1.user_id, 0 " + \
                " FROM tbl_user_units t1 where t1.unit_id = NEW.unit_id; " + \
                " INSERT INTO tbl_statutory_notification_status ( " + \
                " statutory_notification_id, " + \
                " user_id, read_status) " + \
                " SELECT NEW.statutory_notification_id, t1.user_id, 0  " + \
                " FROM tbl_users t1 where t1.is_active = 1 " + \
                " and t1.is_primary_admin = 1;" + \
                " END; "
            cursor.execute(t1)
            t2 = " CREATE TRIGGER `after_tbl_units_insert` AFTER " + \
                " INSERT ON `tbl_units` " + \
                " FOR EACH ROW BEGIN " + \
                " CALL procedure_to_update_version('unit'); " + \
                " END; "
            cursor.execute(t2)
            t3 = "CREATE TRIGGER `after_tbl_units_update` " + \
                " AFTER UPDATE ON `tbl_units` " + \
                " FOR EACH ROW BEGIN " + \
                " CALL procedure_to_update_version('unit'); " + \
                " END; "
            cursor.execute(t3)
            t4 = "CREATE TRIGGER `after_tbl_users_update` " + \
                " AFTER UPDATE ON `tbl_users` " + \
                " FOR EACH ROW BEGIN " + \
                " CALL procedure_to_update_version('user'); " + \
                " END; "
            cursor.execute(t4)
            t5 = "CREATE TRIGGER `after_tbl_users_insert` " + \
                " AFTER INSERT ON `tbl_users` " + \
                " FOR EACH ROW BEGIN " + \
                " CALL procedure_to_update_version('user'); " + \
                " END; "
            cursor.execute(t5)
            t6 = "CREATE TRIGGER `after_tbl_compliance_history_insert` " + \
                " AFTER INSERT ON `tbl_compliance_history` " + \
                " FOR EACH ROW BEGIN " + \
                " CALL procedure_to_update_version('history'); " + \
                " END; "
            cursor.execute(t6)
            t7 = "CREATE TRIGGER `after_tbl_compliance_history_update` " + \
                " AFTER UPDATE ON `tbl_compliance_history` " + \
                " FOR EACH ROW BEGIN " + \
                " CALL procedure_to_update_version('history'); " + \
                " END; "
            cursor.execute(t7)
            t8 = "CREATE TRIGGER `after_tbl_client_compliances_update` " + \
                " AFTER UPDATE ON `tbl_client_compliances` " + \
                " FOR EACH ROW BEGIN " + \
                " CALL procedure_to_update_version('compliance'); " + \
                " END; "
            cursor.execute(t8)
            t9 = "CREATE TRIGGER `after_tbl_client_compliances_insert` " + \
                " AFTER INSERT ON `tbl_client_compliances` " + \
                " FOR EACH ROW BEGIN " + \
                " CALL procedure_to_update_version('compliance'); " + \
                " END; "
            cursor.execute(t9)
        except Exception, e:
            logger.logGroup("_create_trigger", str(e))
            logger.logGroup("_create_trigger", "failed")
            raise self.process_error(
                "trigger creation failed in client database "
            )


class ClientLEDBCreate(ClientDBBase):
    def __init__(
        self, db, client_id, short_name, email_id, database_ip, database_port,
        database_username, database_password
    ):
        super(ClientLEDBCreate, self).__init__(
            db, client_id, short_name, email_id, database_ip, database_port,
            database_username, database_password
        )
        self._db_prefix = CLIENT_LE_DB_PREFIX
        self._db_file_path = "scripts/mirror-client-new.sql"

    def _create_database(self):
        db_con = None
        main_con = None
        try:
            temp_var = "%s, %s, %s" % (self._host, self._username, self._password)
            logger.logGroup("_create_database", temp_var)
            main_con = self._mysql_server_connect(
                self._host, self._username, self._password, self._port
            )
            print "main_con success"
            logger.logGroup("_create_database", "main connection success")
            main_cursor = main_con.cursor()
            self._create_db(main_cursor)
            logger.logGroup("_create_database", "create DB success")
            self._grant_privileges(main_cursor)
            logger.logGroup("_create_database", "create DB user success")
            main_con.commit()

            db_con = self._db_connect(
                self._host, self._username, self._password, self._db_name,
                self._port
            )
            db_cursor = db_con.cursor()
            logger.logGroup("_create_database", "client connection success")

            self._create_tables(db_cursor)
            logger.logGroup("_create_database", "table create success")

            db_con.commit()
            return (True, self._db_name, self._db_username, self._db_password)
        except Exception, e:
            print e
            print "main Exception"
            logger.logGroup("_create_database", str(e))
            if db_con is not None:
                db_con.rollback()
            if main_con is not None:
                main_con.rollback()
            if not self._is_db_failed :
                self.delete_database()
            raise Exception(e)
