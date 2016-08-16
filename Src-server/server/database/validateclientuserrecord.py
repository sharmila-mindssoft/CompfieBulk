from server.dbase import Database
from server.exceptionmessage import not_found_error


class ClientdbConnect(object):
    def __init__(self, db):
        self._db = db
        self._c_db = None
        self._conn = None
        self._cursor = None

    def get_client_database(self):
        columns = [
            "database_ip", "database_port", "database_username",
            "database_password", "database_name"
        ]
        condition = "client_id = %s"
        rows = self._db.get_data(
            "tbl_client_database", columns, condition, [self._client_id]
        )
        if len(rows) == 0:
            raise not_found_error("E061")
        else:
            return rows[0]

    def get_client_connect(self):
        rows = self.get_client_database()
        host = rows["database_ip"]
        port = rows["database_port"]
        username = rows["database_username"]
        password = rows["database_password"]
        database = rows["database_name"]
        self._c_db = Database(
            host, port,
            username, password,
            database
        )
        self._c_db.connect()


class ClientAdmin(ClientdbConnect):
    def __init__(self, db, new_admin_id, old_admin_id, client_id):
        super(ClientAdmin, self).__init__(db)

        self._new_admin_id = new_admin_id
        self._client_id = client_id
        # Assigned to 1 if received old_admin_id is 0
        # because the corresponding admin id in client database is 1
        self._old_admin_id = 1 if old_admin_id == 0 else old_admin_id
        print "init"

    def get_admin_compliances(self):
        q = "select count(compliance_id) from tbl_assigned_compliances " + \
            " WHERE assignee = %s or " + \
            " concurrence_person = %s or " + \
            " approval_person = %s"
        row = self._c_db.select_one(q, [
            self._old_admin_id, self._old_admin_id, self._old_admin_id
        ])
        if int(row[0]) > 0:
            return True
        else:
            return False

    def update_new_admin_records(self):
        q = "update tbl_users set is_primary_admin = 1 where user_id = %s"
        self._c_db.execute(q, [self._new_admin_id])

        q1 = "insert into tbl_user_countries(user_id, country_id) " + \
            " select %s, c.country_id from tbl_countries c " + \
            " on duplicate key update country_id = c.country_id"

        self._c_db.execute(q1, [self._new_admin_id])

        q2 = "insert into tbl_user_domains(user_id, domain_id) " + \
            " select %s, c.domain_id from tbl_domains c " + \
            " on duplicate key update domain_id = c.domain_id"

        self._c_db.execute(q2, [self._new_admin_id])

        q3 = "insert into tbl_user_units(user_id, unit_id) " + \
            " select %s, c.unit_id from tbl_units c " + \
            " on duplicate key update unit_id = c.unit_id"

        self._c_db.execute(q3, [self._new_admin_id])

        q4 = "update tbl_assigned_compliances set " + \
            " concurrence_person = null, approval_person = %s " + \
            " where assignee = %s"
        self._c_db.execute(q4, [self._new_admin_id, self._new_admin_id])

        # updating on going compliances are under discussion.
        # as of now concurrence and approvar paerson will not be
        # changed for inprogress compliances.

    def remove_old_admin(self):
        q2 = "update tbl_users set is_active = 0 " + \
            " where user_id = %s " % (self._old_admin_id)
        self._c_db.execute(q2)

        q3 = " DELETE FROM tbl_user_sessions " + \
            " WHERE user_id = %s " % (self._old_admin_id)
        self._c_db.execute(q3)
        # q1 = "update tbl_admin t1, (select user_id, email_id, password \
        #     from tbl_users) t2 set t1.admin_id = t2.user_id, \
        #     t1.username = t2.email_id, t1.password = t2.password \
        #     where t2.user_id = %s"
        # self._c_db.execute(q1, [self._new_admin_id])

    def perform_promote_admin(self):
        try:
            self.get_client_connect()
            self._c_db.begin()
            is_active_compliance = self.get_admin_compliances()
            if is_active_compliance:
                return "Reassign"
            else:
                self.remove_old_admin()
                self.update_new_admin_records()
                self._c_db.commit()
                self._c_db.close()
                return True
        except Exception, e:
            print e
            self._c_db.rollback()
            return False
