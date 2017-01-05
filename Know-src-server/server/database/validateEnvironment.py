import MySQLdb as mysql
import requests
__all__ = [
    "ServerValidation"
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
            connection.open()
            connection.close()
            return True
        except mysql.Error, e :
            print e
            return "Database server connection failed"

    def validate_application_server(self):
        port = self.machine_info.get("port")
        ip = self.machine_info.get("ip")
        r = requests.post("http://%s:%s/api/isalive") % (ip, port)
        if r.status_code != 200 :
            return "Application server connection failed"
        else :
            return True

    def validate_file_server(self):
        pass
        return True
        # file server connection goes here

    def perform_validation(self):
        machine_result = self.validate_application_server()
        db_result = self.validate_database_server()
        file_result = self.validate_file_server()
        return (machine_result, db_result, file_result)
