import os
import io
import Queue
import threading
import MySQLdb as mysql
from protocol import (technomaster)
from server import logger
from server.database.tables import *

from server.common import (
    generate_and_return_password,
    generate_random
)
from server.database.technomaster import (
    get_server_details
)


CLIENT_DB_PREFIX = "compfie"

class ClientDBCreate(object):
    def __init__(self, db, client_id, short_name, email_id, country_ids, domain_ids):
        self._db = db
        self._client_id = client_id
        self._short_name = short_name
        self._email_id = email_id
        self._country_ids = country_ids
        self._domain_ids = domain_ids
        self._host = None
        self._username = None
        self._password = None
        self._port = None
        self._db_name = None
        self._db_username = None
        self._db_password = None

    def process_error(self, message):
        raise ValueError(message)

    def prepare_db_constrains(self):
        result = self.get_server_machine_details()
        if result is False :
            raise self.process_error("Prepare db_constrsains failed")
        if result is True :
            self.process_db_creation()
        else :
            return result

    def db_name(self):
        return "%s_%s_%s" % (CLIENT_DB_PREFIX, self._short_name.lower(), self._client_id)

    def db_username(self):
        return generate_random()

    def db_password(self):
        return generate_random()

    def get_server_machine_details(self):
        data = get_server_details(self._db)
        if len(data) <= 0 :
            return technomaster.ServerIsFull()
        else :
            self._host = data[0]["ip"]
            self._username = data[0]["server_username"]
            self._password = data[0]["server_password"]
            self._port = data[0]["port"]
            self._db_name = self.db_name()
            self._db_username = self.db_username()
            self._db_password = self.db_password()
            return True

    def process_db_creation(self):
        def enthread():
            q = Queue.Queue()

            def wrapper():
                q.put(
                    self._create_database(
                        self._host, self._username,
                        self._password, self._db_username,
                        self._db_password, self._email_id,
                        self._client_id, self._short_name,
                        self._db, self._country_ids, self._domain_ids
                    )
                )
            create_database_thread = threading.Thread(target=wrapper)
            create_database_thread.start()
            return q

        result_q = enthread()
        result = result_q.get()
        return result

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
            self._host, self._username, self._password,
        )
        cursor = con.cursor()
        query = "DROP DATABASE IF EXISTS %s"
        cursor.execute(query, [self._db_name])
        # drop created user here.
        con.commit()

    def _create_database(self):
        try :
            main_con = self._mysql_server_connect(
                self._host, self._username, self._password, self._port
            )
            main_cursor = main_con.cursor()
            self._create_db(main_cursor)
            self._grant_privileges(main_cursor)
            main_cursor.commit()

            db_con = self._db_connect(
                self._host, self._username, self._password, self._db_name,
                self._port
            )
            self._create_tables(db_con)
            self._create_admin_user(db_con)
            self._create_procedure(db_con)
            self._create_trigger(db_con)
            self._save_client_domains(self._domain_ids, db_con)
            self._save_client_countries(self._country_ids, db_con)
            db_con.commit()
            return True
        except Exception :
            raise self.process_error("create_database failed")

    def _save_client_countries(self, country_ids, cursor):
        try :
            q = "SELECT country_id, country_name, is_active \
                    FROM tbl_countries\
                    WHERE country_id\
                    IN (%s) " % (country_ids)
            rows = self._db.select_all(q)
            for r in rows :
                q = " INSERT INTO tbl_countries VALUES (%s, %s, %s)"
                cursor.execute(q, [int(r[0]), r[1], int(r[2])])
        except Exception :
            raise self.process_error("save client countries failed")

    def _save_client_domains(self, domain_ids, cursor):
        try :
            q = "SELECT domain_id, domain_name, is_active \
                    FROM tbl_domains\
                    WHERE domain_id\
                    IN (%s)"
            rows = self._db.select_all(q, [domain_ids])
            for r in rows :
                q = " INSERT INTO tbl_domains VALUES (%s, %s, %s)"
                cursor.execute(q, [int(r[0]), r[1], int(r[2])])
        except Exception :
            raise self.process_error("save client domains failed")

    def _create_db(self, cursor):
        try :
            query = "CREATE DATABASE %s"
            cursor.execute(query, [self._db_name])
        except Exception :
            raise self.process_error("client db creation failed")

    def _grant_privileges(self, cursor):
        try :
            query = "GRANT SELECT, INSERT, UPDATE, DELETE ON %s.* to '%s'@'%s' IDENTIFIED BY '%s';"
            self.execute(query, [
                self._db_name, self._db_username, str('%'), self._db_password
            ])
            cursor.execute("FLUSH PRIVILEGES;")
        except Exception :
            raise self.process_error("client database user grant_privileges failed")

    def _create_admin_user(self, cursor):
        try :
            encrypted_password, password = generate_and_return_password()
            query = "insert into tbl_admin (username, password) values (%s, %s)"
            logger.logKnowledge("info", "create", "save user")
            cursor.execute(query, [self._email_id, encrypted_password])

            query = "insert into tbl_users (user_id, employee_name, email_id, password, user_level,\
            is_primary_admin, is_service_provider, is_admin)\
            values (0, 'Administrator', %s, %s, 1 , 1, 0, 0 )"
            cursor.execute(query, [self._email_id, encrypted_password])
        except Exception :
            raise self.process_error("admin user creation failed in client database")

    def _create_tables(self, cursor):
        try :
            sql_script_path = os.path.join(
                os.path.join(os.path.split(__file__)[0]),
                "scripts/mirror-client.sql"
            )
            with io.FileIO(sql_script_path, "r") as file_obj :
                sql_file = file_obj.read()
                sql_commands = sql_file.split(';')
                size = len(sql_commands)
                for index, command in enumerate(sql_commands):
                    if (index < size-1):
                        cursor.execute(command)
                    else:
                        break
        except Exception :
            raise self.process_error("table creation failed in client database")

    def _create_procedure(self, cursor):
        try :
            p1 = "CREATE PROCEDURE `procedure_to_update_version` (IN update_type VARCHAR(100))\
                BEGIN \
                    SET SQL_SAFE_UPDATES=0;\
                    case \
                        when update_type = 'unit' then \
                        SET @count = (SELECT unit_details_version+1 FROM tbl_mobile_sync_versions ); \
                        update tbl_mobile_sync_versions set unit_details_version = @count; \
                        when update_type = 'user' then \
                        SET @count = (SELECT user_details_version+1 FROM tbl_mobile_sync_versions ); \
                        update tbl_mobile_sync_versions set user_details_version = @count; \
                        when update_type = 'compliance' then \
                        SET @count = (SELECT compliance_applicability_version+1 FROM tbl_mobile_sync_versions ); \
                        update tbl_mobile_sync_versions set compliance_applicability_version = @count; \
                        when update_type = 'history' then \
                        SET @count = (SELECT compliance_history_version+1 FROM tbl_mobile_sync_versions ); \
                        update tbl_mobile_sync_versions set compliance_history_version = @count; \
                    end case; \
                    SET SQL_SAFE_UPDATES=1; \
                END "
            cursor.execute(p1)
        except Exception :
            raise self.process_error("procedure creation failed in client database")

    def _create_trigger(self, cursor):
        try :
            t1 = "CREATE TRIGGER `after_tbl_statutory_notifications_units_insert` AFTER INSERT ON `tbl_statutory_notifications_units` \
                FOR EACH ROW BEGIN \
                    INSERT INTO tbl_statutory_notification_status ( \
                    statutory_notification_id, \
                    user_id, read_status) \
                    SELECT NEW.statutory_notification_id, t1.user_id, 0 \
                    FROM tbl_user_units t1 where t1.unit_id = NEW.unit_id; \
                    \
                    INSERT INTO tbl_statutory_notification_status ( \
                        statutory_notification_id, \
                        user_id, read_status \
                    ) \
                    SELECT NEW.statutory_notification_id, t1.admin_id, 0 FROM \
                    tbl_admin t1 where t1.admin_id != 0; \
                END; "
            cursor.execute(t1)
            t2 = " CREATE TRIGGER `after_tbl_units_insert` AFTER INSERT ON `tbl_units` \
                FOR EACH ROW BEGIN \
                    CALL procedure_to_update_version('unit'); \
                END; "
            cursor.execute(t2)
            t3 = "CREATE TRIGGER `after_tbl_units_update` AFTER UPDATE ON `tbl_units` \
                FOR EACH ROW BEGIN \
                    CALL procedure_to_update_version('unit'); \
                END; "
            cursor.execute(t3)
            t4 = "CREATE TRIGGER `after_tbl_users_update` AFTER UPDATE ON `tbl_users` \
                FOR EACH ROW BEGIN \
                    CALL procedure_to_update_version('user'); \
                END; "
            cursor.execute(t4)
            t5 = "CREATE TRIGGER `after_tbl_users_insert` AFTER INSERT ON `tbl_users` \
                FOR EACH ROW BEGIN \
                    CALL procedure_to_update_version('user'); \
                END; "
            cursor.execute(t5)
            t6 = "CREATE TRIGGER `after_tbl_compliance_history_insert` AFTER INSERT ON `tbl_compliance_history` \
                FOR EACH ROW BEGIN \
                    CALL procedure_to_update_version('history'); \
                END; "
            cursor.execute(t6)
            t7 = "CREATE TRIGGER `after_tbl_compliance_history_update` AFTER UPDATE ON `tbl_compliance_history` \
                FOR EACH ROW BEGIN \
                    CALL procedure_to_update_version('history'); \
                END; "
            cursor.execute(t7)
            t8 = "CREATE TRIGGER `after_tbl_client_compliances_update` AFTER UPDATE ON `tbl_client_compliances` \
                FOR EACH ROW BEGIN \
                    CALL procedure_to_update_version('compliance'); \
                END; "
            cursor.execute(t8)
            t9 = "CREATE TRIGGER `after_tbl_client_compliances_insert` AFTER INSERT ON `tbl_client_compliances` \
                FOR EACH ROW BEGIN \
                    CALL procedure_to_update_version('compliance'); \
                END; "
            cursor.execute(t9)
        except Exception :
            raise self.process_error("trigger creation failed in client database ")

    def _get_machine_details(self):
        columns = "machine_id, ip, port"
        condition = "server_full = 0 ORDER BY length(client_ids) limit 1"
        rows = self._db.get_data(tblMachines, columns, condition)
        return rows

    def set_server_full(self, db_server_condition):
        columns = ["server_full"]
        values = [1]
        self._db.update(tblMachines, columns, values, db_server_condition)

    def update_client_db_details(self):
        db_server_column = "company_ids"
        db_server_value = self._client_id

        db_server_condition = "ip = '%s' and port = '%s'" % (str(host), str(db_port))
        print db_server_condition

        self._db.append(
            tblDatabaseServer, db_server_column, db_server_value,
            db_server_condition
        )
        db_server_column = "length"
        self._db.increment(
            tblDatabaseServer, db_server_column,
            db_server_condition
        )

        result = self._get_machine_details()
        machine_id = result[0]["machine_id"]
        server_ip = result[0]["ip"]
        server_port = result[0]["port"]
        machine_columns = "client_ids"
        machine_value = self._client_id
        machine_condition = "ip='%s' and port='%s'" % (server_ip, server_port)
        self._db.append(
            tblMachines, machine_columns, machine_value,
            machine_condition
        )

        client_db_columns = [
            "client_id", "machine_id", "database_ip",
            "database_port", "database_username", "database_password",
            "client_short_name", "database_name",
            "server_ip", "server_port"
        ]
        client_dB_values = [
            client_id, machine_id, host, db_port, db_username,
            db_password, short_name, database_name,
            server_ip, server_port
        ]
        length_rows = self._db.get_data(
            tblMachines, "client_ids",
            db_server_condition
        )
        if length_rows:
            print length_rows
            company_ids = length_rows[0][0].split(",")
            if company_ids >= 30:
                self.set_server_full(db_server_condition)
        return self._db.insert(
            tblClientDatabase, client_db_columns,
            client_dB_values
        )

    def begin_process(self):
        return self.prepare_db_constrains()
