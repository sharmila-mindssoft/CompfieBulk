import MySQLdb as mysql
import requests
__all__ = [
    "ServerValidation", "UpdateServerValidation"
]
class ServerValidation(object):
    def __init__(self, db, machine_id, database_server_id, file_server_id):
        self._db = db
        self._db_server_id = database_server_id
        self._machine_id = machine_id
        self._f_server_id = file_server_id
        self.dbase_info = None
        self.machine_info = None
        self.fileserver_info = None
        self.get_server_info()

    def get_server_info(self):
        result = self._db.call_proc_with_multiresult_set(
            "sp_get_environment_byid", [self._db_server_id, self._machine_id, self._f_server_id], 3
        )
        self.dbase_info = result[0][0]
        self.machine_info = result[1][0]
        self.fileserver_info = result[2][0]

    def validate_database_server(self):
        dhost = self.dbase_info.get("database_ip")
        uname = self.dbase_info.get("database_username")
        pwd = self.dbase_info.get("database_password")
        port = self.dbase_info.get("database_port")
        try :
            connection = mysql.connect(host=dhost, user=uname, passwd=pwd, port=port)
            c = connection.cursor()
            c.close()
            connection.close()
            return True
        except mysql.Error, e :
            print e
            return "Database server connection failed"

    def validate_application_server(self):
        port = self.machine_info.get("port")
        ip = self.machine_info.get("ip")
        try :
            r = requests.post("http://%s:%s/api/isalive" % (ip, port))
            print r
            print "-" * 50
            if r.status_code != 200 :
                return "Application server connection failed"
            else :
                return True

        except :
            raise RuntimeError("Application server connection failed")

    def validate_file_server(self):
        port = self.fileserver_info.get("port")
        ip = self.fileserver_info.get("ip")
        try :
            r = requests.post("http://%s:%s/api/isfilealive" % (ip, port))
            print r
            print "-" * 50
            if r.status_code != 200 :
                return "File server connection failed"
            else :
                return True

        except :
            raise RuntimeError("File server connection failed")

    def perform_validation(self):
        machine_result = self.validate_application_server()
        db_result = self.validate_database_server()
        file_result = self.validate_file_server()
        return (machine_result, db_result, file_result)

class UpdateServerValidation(object):
    def __init__(
        self, db, client_db_id, legal_entity_id, client_id, machine_id, database_server_id,
        le_database_server_id, file_server_id
    ):
        self._db = db
        self._client_db_id = client_db_id
        self._cl_id = client_id
        self._le_id = legal_entity_id
        self._db_server_id = database_server_id
        self._machine_id = machine_id
        self._f_server_id = file_server_id
        self._le_db_server_id = le_database_server_id
        self.dbase_info = None
        self.le_dbase_info = None
        self.machine_info = None
        self.fileserver_info = None
        self.get_update_server_info()

    def get_update_server_info(self):
        print self._machine_id, self._db_server_id, self._le_db_server_id, self._f_server_id, self._cl_id, self._le_id
        result = self._db.call_proc_with_multiresult_set(
            "sp_get_created_server_details_byid", [
                self._machine_id, self._db_server_id, self._le_db_server_id, self._f_server_id, self._cl_id, self._le_id], 4
        )
        print result[0][0]
        print result[1][0]
        self.dbase_info = result[0][0]
        self.le_dbase_info = result[1][0]
        self.machine_info = result[2][0]
        self.fileserver_info = result[3][0]

    def validate_update_database_server(self):
        dhost = self.dbase_info.get("database_ip")
        uname = self.dbase_info.get("database_username")
        pwd = self.dbase_info.get("database_password")
        port = self.dbase_info.get("database_port")
        try :
            print uname, pwd
            if (uname is None or pwd is None):
                return "Group Database server Not Exists"
            else:
                connection = mysql.connect(host=dhost, user=uname, passwd=pwd, port=port)
                c = connection.cursor()
                c.close()
                connection.close()
                return True
        except mysql.Error, e :
            print e
            return "Group Database server connection failed"

    def validate_update_le_database_server(self):
        dhost = self.le_dbase_info.get("database_ip")
        uname = self.le_dbase_info.get("database_username")
        pwd = self.le_dbase_info.get("database_password")
        port = self.le_dbase_info.get("database_port")
        try :
            if (uname is None or pwd is None):
                return "Group Database server connection failed"
            else:
                connection = mysql.connect(host=dhost, user=uname, passwd=pwd, port=port)
                c = connection.cursor()
                c.close()
                connection.close()
                return True
        except mysql.Error, e :
            print e
            return "Legal Entity Database server connection failed"

    def validate_update_application_server(self):
        port = self.machine_info.get("port")
        ip = self.machine_info.get("ip")
        try :
            r = requests.post("http://%s:%s/api/isalive" % (ip, port))
            print r
            print "-" * 50
            if r.status_code != 200 :
                return "Application server connection failed"
            else :
                return True

        except :
            raise RuntimeError("Application server connection failed")

    def validate_update_file_server(self):
        port = self.fileserver_info.get("port")
        ip = self.fileserver_info.get("ip")
        try :
            r = requests.post("http://%s:%s/api/isfilealive" % (ip, port))
            print r
            print "-" * 50
            if r.status_code != 200 :
                return "File server connection failed"
            else :
                return True

        except :
            raise RuntimeError("File server connection failed")

    def perform_update_validation(self):
        machine_result = self.validate_update_application_server()
        db_result = self.validate_update_database_server()
        le_db_result = self.validate_update_le_database_server()
        file_result = self.validate_update_file_server()
        return (machine_result, db_result, le_db_result, file_result)
