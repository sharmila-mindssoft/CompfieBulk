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
    Following opterations will be performed in this class.
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
        logger.logKnowledge("info", "Database creation process", "begin")
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

    def process_error(self, message):
        logger.logKnowledge("error", "ClientDDBase", message)
        raise ValueError(str(message))

    def db_create_name(self, db_id):
        return "%s_%s_%s" % (
            self._db_prefix, self._short_name.lower(), db_id
        )

    def db_create_username(self):
        return generate_random()

    def db_create_password(self):
        return generate_special_random()

    def get_db_constrains(self):
        self._db_username = self.db_create_username()
        self._db_password = self.db_create_password()
        return True

    def _mysql_server_connect(self, host, username, password, port):
        try :
            return mysql.connect(
                host=host, user=username, passwd=password, port=port
            )
        except Exception, e :
            logger.logKnowledge("error", "mysql server connect", "%s, %s, %s" % (host, port, username))
            logger.logKnowledge("error", "mysql server connect", str(e))
            raise RuntimeError("server connection failed")

    def _db_connect(self, host, username, password, database, port):
        try :
            return mysql.connect(
                host=host, user=username, passwd=password, db=database,
                port=port
            )
        except Exception, e:
            logger.logKnowledge("error", "db connect", "%s, %s, %s, %s" % (host, port, username, database))
            logger.logKnowledge("error", "db connect", str(e))
            raise RuntimeError("server connection failed")

    def delete_database(self):
        con = self._mysql_server_connect(
            self._host, self._username, self._password, self._port
        )
        try:
            cursor = con.cursor()
            query = "DROP DATABASE IF EXISTS %s" % self._db_name
            cursor.execute(query)
            con.commit()
            logger.logKnowledge("info", "dropping database", "query:%s" % (query))

        except Exception, e:
            logger.logKnowledge("error", "drop", query)
            logger.logKnowledge("error", "drop", str(e))
            con.rollback()
            raise RuntimeError(str(e))

    def _create_db(self, cursor):
        query = "CREATE DATABASE %s" % self._db_name
        try:
            cursor.execute("DROP DATABASE IF EXISTS %s" % (self._db_name))
            cursor.execute(query)
            logger.logKnowledge("info", "creating database", "query:%s" % (query))

        except Exception, ex:
            self._is_db_failed = True
            logger.logKnowledge("error", "create", query)
            logger.logKnowledge("error", "create", str(ex))
            e = "client db creation failed"
            raise RuntimeError(str(e))

    def _grant_privileges(self, cursor):
        try:
            q = "CREATE USER %s@%s IDENTIFIED BY %s;"

            cursor.execute(q, [self._db_username, str('%'), self._db_password])
            logger.logKnowledge("info", "create user", "query:%s, param:%s" % (q, [self._db_username, str('%'), self._db_password]))

            query = "GRANT SELECT, INSERT, UPDATE, " + \
                " DELETE ON %s.* to '%s'@'%s' ;"

            param = (
                self._db_name, self._db_username, str('%')
            )

            cursor.execute(query % param)
            cursor.execute("FLUSH PRIVILEGES;")
            logger.logKnowledge("info", "grant privileges", "query:%s, param:%s" % (query, param))

        except Exception, ex:
            logger.logKnowledge("error", "create user", "query:%s, param:%s" % (q, [self._db_username, str('%'), self._db_password]))
            logger.logKnowledge("error", "grant privileges", "query:%s, param:%s" % (query, param))
            logger.logKnowledge("error", "create", str(ex))
            e = "client database user grant_privileges failed"
            raise RuntimeError(str(e))

    def _create_admin_user(self, cursor):
        try:
            query = "insert into tbl_users (user_category_id, client_id, employee_name, " + \
                " email_id " + \
                " )" + \
                " values (1, %s, 'Administrator', %s)"
            cursor.execute(query, [self._client_id, self._email_id])
            logger.logKnowledge("query", "create admin user", "query:%s, param:%s" % (query, [self._client_id, self._email_id]))

        except Exception, e:
            logger.logKnowledge("error", "create admin user", "query:%s, param:%s" % (query, [self._client_id, self._email_id]))
            logger.logKnowledge("error", "create admin user", str(e))
            raise RuntimeError("admin user creation failed")

    def _create_tables(self, cursor):
        # "scripts/mirror-client-group.sql"
        try:
            cmd = None
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
                        cmd = command
                        cursor.execute(command)
                    else:
                        break
        except Exception, e:
            logger.logKnowledge("error", "create table", "query:%s" % (cmd))
            logger.logKnowledge("error", "create table", str(e))
            raise RuntimeError("table creation failed")

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

    def bulk_insert(self, cursor, table, columns, valueList):
        stringValue = []
        for i in range(len(columns)):
            stringValue.append('%s')

        if type(columns) is list:
            columns = ", ".join(columns)
        query = "INSERT INTO %s (%s) " % (table, columns)
        query += " VALUES (%s) " % (",".join(stringValue))

        try:
            assert cursor is not None
            cursor.executemany(query, valueList)
            logger.logKnowledge("query", "insert data to client db", "query:%s, param:%s" % (query, valueList))
            cursor.nextset()
            return True
        except Exception, e:
            logger.logKnowledge("error", "insert data", "query:%s, param:%s" % (query, valueList))
            logger.logKnowledge("error", "insert data", str(e))
            return False

    def save_country(self, db_cur, data):
        columns = ["country_id", "country_name"]
        values = []
        for d in data :
            values.append(
                (d.get("country_id"), d.get("country_name"))
            )

        if values :
            self.bulk_insert(db_cur, 'tbl_countries', columns, values)

    def save_domain(self, db_cur, data):
        columns = ["domain_id", "domain_name"]
        values = []
        for d in data :
            values.append(
                (d.get("domain_id"), d.get("domain_name"))
            )

        if values :
            self.bulk_insert(db_cur, 'tbl_domains', columns, values)

    def save_domain_country(self, db_cur, data):

        columns = ["domain_id", "country_id"]
        values = []
        for d in data :
            values.append(
                (d.get("domain_id"), d.get("country_id"))
            )

        if values :
            self.bulk_insert(db_cur, 'tbl_domain_countries', columns, values)

    def save_organisation(self, db_cur, data):
        columns = ["organisation_id", "organisation_name", "country_id", "domain_id", "is_active"]
        values = []
        for d in data :
            values.append(
                (d.get("organisation_id"), d.get("organisation_name"), d.get("country_id"), d.get("domain_id"), d.get("is_active"))
            )

        if values :
            self.bulk_insert(db_cur, 'tbl_organisation', columns, values)

    def save_client_group(self, db_cur, data):
        columns = ["client_id", "group_name", "short_name", "email_id", "total_view_licence"]
        values = []
        for d in data :
            values.append((
                d.get("client_id"), d.get("group_name"), d.get("short_name"),
                d.get("email_id"), d.get("total_view_licence")
            ))
        if values :
            self.bulk_insert(db_cur, "tbl_client_groups", columns, values)

    def save_client_configuration(self, db_cur, data):
        columns = ["client_id", "country_id", "domain_id", "month_from", "month_to"]
        values = []
        for d in data :
            values.append((
                d.get("client_id"), d.get("country_id"), d.get("domain_id"),
                d.get("month_from"), d.get("month_to")
            ))
        if values :
            self.bulk_insert(db_cur, "tbl_client_configuration", columns, values)

    def save_legal_entity(self, db_cur, data):
        columns = [
            "legal_entity_id", "country_id", "business_group_id",
            "legal_entity_name", "contract_from", "contract_to",
            "logo", "logo_size", "file_space_limit", "total_licence"
        ]
        values = []
        for d in data :
            values.append((
                d.get("legal_entity_id"), d.get("country_id"),
                d.get("business_group_id"), d.get("legal_entity_name"),
                d.get("contract_from"), d.get("contract_to"), d.get("logo"),
                d.get("logo_size"), d.get("file_space_limit"), d.get("total_licence")
            ))
        if values :
            self.bulk_insert(db_cur, "tbl_legal_entities", columns, values)

    def save_legal_entity_domains(self, db_cur, data):
        columns = [
            "legal_entity_id", "domain_id", "activation_date",
            "organisation_id", "count"
        ]
        values = []
        for d in data :
            values.append((
                d.get("legal_entity_id"), d.get("domain_id"), d.get("activation_date"),
                d.get("organisation_id"), d.get("count")
            ))

        if values :
            self.bulk_insert(db_cur, "tbl_legal_entity_domains", columns, values)

    def save_business_group(self, db_cur, data):
        columns = ["business_group_id", "business_group_name"]
        values = []
        for d in data :
            values.append(
                (d.get("business_group_id"), d.get("business_group_name"))
            )

        if values :
            self.bulk_insert(db_cur, 'tbl_business_groups', columns, values)

    def save_reminder_settings(self, db_cur, le_id, client_id):
        columns = ["client_id", "legal_entity_id"]
        values = [(client_id, le_id)]
        if values :
            self.bulk_insert(db_cur, 'tbl_reminder_settings', columns, values)


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
        self._db_name = self.db_create_name(client_id)
        self.db_con = None

    def _create_database(self):
        db_con = None
        main_con = None
        try:
            temp_var = "%s, %s, %s" % (self._host, self._username, self._db_name)
            logger.logKnowledge("info", "create database - begin", temp_var)

            main_con = self._mysql_server_connect(
                self._host, self._username, self._password, self._port
            )
            main_cursor = main_con.cursor()
            self._create_db(main_cursor)

            self._grant_privileges(main_cursor)
            main_con.commit()

            db_con = self._db_connect(
                self._host, self._username, self._password, self._db_name,
                self._port
            )
            self.db_con = db_con
            db_cursor = db_con.cursor()

            self._create_tables(db_cursor)

            self._create_trigger(db_cursor)
            self._create_admin_user(db_cursor)

            db_con.commit()
            logger.logKnowledge("info", "create database - end", temp_var)

            return (True, self._db_name, self._db_username, self._db_password)
        except Exception, e:

            logger.logKnowledge("error", "create_database", str(e))
            if db_con is not None:
                db_con.rollback()
            if main_con is not None:
                main_con.rollback()
            if self._is_db_failed :
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
            logger.logKnowledge("info", "_create_procedure", p1)
        except Exception, e:
            logger.logKnowledge("error", "_create_procedure", p1)
            logger.logKnowledge("error", "_create_procedure", str(e))
            raise self.process_error(
                "procedure creation failed in client database"
            )

    def _create_trigger(self, cursor):
        try:

            t1 = "CREATE TRIGGER `after_tbl_legal_entity_insert` AFTER INSERT ON `tbl_legal_entities` " + \
                " FOR EACH ROW BEGIN " + \
                "  INSERT INTO tbl_le_replication_status(legal_entity_id) values(new.legal_entity_id); " + \
                " INSERT INTO tbl_reminder_settings(client_id, legal_entity_id) select client_id, new.legal_entity_id from " + \
                " tbl_client_groups ;" + \
                " END; "
            cursor.execute(t1)
            logger.logKnowledge("info", "create trigger", t1)

            t2 = " CREATE TRIGGER `after_tbl_user_legal_entities_insert` AFTER INSERT ON `tbl_user_legal_entities` " + \
                " FOR EACH ROW BEGIN " + \
                " INSERT INTO tbl_le_user_replication_status(legal_entity_id, user_id, s_action) " + \
                " values(new.legal_entity_id, new.user_id, 1) on duplicate key update s_action = 1; " + \
                " UPDATE tbl_le_replication_status set user_data = 1 where legal_entity_id = new.legal_entity_id; " + \
                " END; "
            cursor.execute(t2)
            logger.logKnowledge("info", "create trigger", t2)

            t3 = "CREATE TRIGGER `after_tbl_user_legal_entities_delete` AFTER DELETE ON `tbl_user_legal_entities` " + \
                " FOR EACH ROW BEGIN " + \
                " if old.user_id is not null then " + \
                " INSERT INTO tbl_le_user_replication_status(legal_entity_id, user_id, s_action) " + \
                " values(old.legal_entity_id, old.user_id, 3) on duplicate key update s_action = 3; " + \
                " UPDATE tbl_le_replication_status set user_data = 1 where legal_entity_id = old.legal_entity_id; " + \
                " end if; " + \
                " END; "
            cursor.execute(t3)
            logger.logKnowledge("info", "create trigger", t3)

            t4 = "CREATE TRIGGER `after_tbl_service_providers_insert` AFTER INSERT ON `tbl_service_providers` " + \
                " FOR EACH ROW BEGIN " + \
                " insert into tbl_le_provider_replication_status(legal_entity_id, provider_id, s_action) " + \
                " select legal_entity_id, new.service_provider_id, 1 from tbl_legal_entities on duplicate key update s_action = 1; " + \
                " UPDATE tbl_le_replication_status set provider_data = 1 ; " + \
                " END ;"
            cursor.execute(t4)
            logger.logKnowledge("info", "create trigger", t4)

            t5 = "CREATE TRIGGER `after_tbl_service_providers_update` AFTER UPDATE ON `tbl_service_providers` " + \
                " FOR EACH ROW BEGIN " + \
                " insert into tbl_le_provider_replication_status(legal_entity_id, provider_id, s_action) " + \
                " select legal_entity_id, new.service_provider_id, 1 from tbl_legal_entities on duplicate key update s_action = 1; " + \
                " UPDATE tbl_le_replication_status set provider_data = 1 ; " + \
                " END ;"
            cursor.execute(t5)
            logger.logKnowledge("info", "create trigger", t5)

            t6 = "CREATE TRIGGER `after_tbl_reminder_settings_update` AFTER UPDATE ON `tbl_reminder_settings` " + \
                " FOR EACH ROW BEGIN " + \
                " insert into tbl_le_settings_replication_status(legal_entity_id, s_action) " + \
                " values(new.legal_entity_id, 1) on duplicate key update s_action = 1; " + \
                " UPDATE tbl_le_replication_status set settings_data = 1 where legal_entity_id = new.legal_entity_id ; " + \
                " END ;"
            cursor.execute(t6)
            logger.logKnowledge("info", "create trigger", t6)

            t7 = "CREATE TRIGGER `after_tbl_users_status_update` AFTER UPDATE ON `tbl_users` " + \
                " FOR EACH ROW BEGIN " + \
                " if ((old.is_active <> new.is_active) or (old.is_disable <> new.is_disable)) then " + \
                " INSERT INTO tbl_le_user_replication_status(legal_entity_id, user_id, s_action) " + \
                " select legal_entity_id, new.user_id, 1 from tbl_user_legal_entities where user_id = new.user_id " + \
                " on duplicate key update s_action = 1; " + \
                " UPDATE tbl_le_replication_status set user_data = 1 " + \
                " where legal_entity_id in (select legal_entity_id from tbl_user_legal_entities where user_id = new.user_id); " + \
                " end if; " + \
                " END ; "

            cursor.execute(t7)
            logger.logKnowledge("info", "create trigger", t7)

        except Exception, e:
            logger.logGroup("error", "_create_trigger", str(e))
            raise self.process_error(
                "trigger creation failed in client database "
            )

    def _save_master_info(self):
        args = [self._client_id, None]
        m_info = self._db.call_proc_with_multiresult_set("sp_get_le_master_info", args, 4)
        country = m_info[0]
        domain = m_info[1]
        domain_country = m_info[2]
        org_data = m_info[3]
        db_cur = self.db_con.cursor()
        self.save_country(db_cur, country)
        self.save_domain(db_cur, domain)
        self.save_domain_country(db_cur, domain_country)
        self.save_organisation(db_cur, org_data)
        self.db_con.commit()

class ClientLEDBCreate(ClientDBBase):
    def __init__(
        self, db, client_id, short_name, email_id, database_ip, database_port,
        database_username, database_password, legal_entity_id
    ):
        super(ClientLEDBCreate, self).__init__(
            db, client_id, short_name, email_id, database_ip, database_port,
            database_username, database_password
        )
        self._db = db
        self._db_prefix = CLIENT_LE_DB_PREFIX
        self._db_file_path = "scripts/mirror-client-new.sql"
        self._legal_entity_id = legal_entity_id
        self._db_name = self.db_create_name(legal_entity_id)
        self.db_con = None

    def _create_database(self):
        db_con = None
        main_con = None
        try:
            temp_var = "%s, %s, %s" % (self._host, self._username, self._db_name)
            logger.logKnowledge("info", "create le database - begin", temp_var)
            main_con = self._mysql_server_connect(
                self._host, self._username, self._password, self._port
            )

            main_cursor = main_con.cursor()
            self._create_db(main_cursor)
            self._grant_privileges(main_cursor)

            main_con.commit()

            db_con = self._db_connect(
                self._host, self._username, self._password, self._db_name,
                self._port
            )
            self.db_con = db_con
            db_cursor = db_con.cursor()

            self._create_tables(db_cursor)
            self._create_admin_user(db_cursor)
            self._create_le_trigger(db_cursor)
            self.save_reminder_settings(db_cursor, self._legal_entity_id, self._client_id)
            db_con.commit()
            logger.logKnowledge("info", "create le database - end", temp_var)

            return (True, self._db_name, self._db_username, self._db_password)
        except Exception, e:
            logger.logKnowledge("error", "create le database", str(e))

            if db_con is not None:
                db_con.rollback()
            if main_con is not None:
                main_con.rollback()
            if self._is_db_failed :
                self.delete_database()
            raise RuntimeError(str(e))

    def _create_le_trigger(self, cursor):
        t6 = "CREATE TRIGGER `tbl_statutory_notifications_insert` AFTER INSERT ON `tbl_statutory_notifications` " + \
                " FOR EACH ROW BEGIN " + \
                "   SET @notificationid = NEW.notification_id; " + \
                " INSERT INTO tbl_statutory_notifications_users ( " + \
                " notification_id, user_id, is_read) " + \
                " select distinct @notificationid, t1.user_id, 0 from tbl_users as t1 " + \
                " left join tbl_user_domains as t3 on t1.user_id = t3.user_id " + \
                " left join tbl_legal_entities as t4 on t3.legal_entity_id = t4.legal_entity_id " + \
                " left join tbl_compliances as t2 " + \
                " on t3.domain_id = t2.domain_id and t4.country_id = t2.country_id and" + \
                " t2.compliance_id = new.compliance_id;" + \
                " END ;"
        cursor.execute(t6)
        logger.logKnowledge("query", "create le trigger", t6)

    def _save_master_info(self):
        args = [self._client_id, self._legal_entity_id]
        m_info = self._db.call_proc_with_multiresult_set("sp_get_le_master_info", args, 9)
        country = m_info[0]

        self._db.call_proc(
            "sp_audit_trail_country_for_group", [self._legal_entity_id, self._client_id]
        )

        domain = m_info[1]
        domain_country = m_info[2]
        org_data = m_info[3]
        client_data = m_info[4]
        client_conf_data = m_info[5]
        le_data = m_info[6]
        le_domain_data = m_info[7]
        bg_info = m_info[8]
        db_cur = self.db_con.cursor()
        self.save_country(db_cur, country)
        self.save_domain(db_cur, domain)
        self.save_domain_country(db_cur, domain_country)
        self.save_organisation(db_cur, org_data)
        self.save_client_group(db_cur, client_data)
        self.save_client_configuration(db_cur, client_conf_data)
        self.save_legal_entity(db_cur, le_data)
        self.save_legal_entity_domains(db_cur, le_domain_data)
        self.save_business_group(db_cur, bg_info)
        self.db_con.commit()
