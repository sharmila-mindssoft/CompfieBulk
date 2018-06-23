import datetime
import traceback
from processes.process_logger import logNotifyError, logNotifyInfo
from processes.process_dbase import Database
from processes.auto_start_task import KnowledgeConnect
from server.emailcontroller import EmailHandler
from server.common import (return_hour_minute, get_current_date)

class AutoNotify(Database):
    def __init__(
        self, c_db_ip, c_db_username, c_db_password, c_db_name,
        c_db_port, client_id, legal_entity_id, current_date
    ):
        super(AutoNotify, self).__init__(
            c_db_ip, c_db_port, c_db_username, c_db_password, c_db_name
        )
        self.connect()
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.current_date = current_date

    def audit_trail_auto_deletion(self):
        q = "DELETE FROM tbl_activity_log WHERE UNIX_TIMESTAMP(DATE(created_on)) < UNIX_TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL 31 DAY)); "
        # print "QUERY>>", q
        v = None
        # logNotifyInfo("save_notification_users", q % v)
        self.execute(q, v)
        # print "DELETESUCCESSFULLY"

    def start_process(self):
        try :
            self.begin()
            self.audit_trail_auto_deletion()
            self.commit()
            self.close()
        except Exception, e :
            print e
            print (traceback.format_exc())
            logNotifyError("start_process", (traceback.format_exc()))
            self.rollback()
            self.close()

class AuditTrailProcess(KnowledgeConnect):
    def __init__(self):
        super(AuditTrailProcess, self).__init__()

    def begin_process(self):
        current_date = datetime.datetime.now()
        logNotifyInfo("current_date", current_date)
        current_time = return_hour_minute(current_date)

        client_info = self.get_client_db_list()
        # print client_info
        for c in client_info:
            try :
                print "-------------------------------"
                print "DATABASE>>", c
                print "-------------------------------"
                task = AutoNotify(
                    c["database_ip"], c["database_username"],
                    c["database_password"], c["database_name"],
                    c["database_port"], c["client_id"], c["legal_entity_id"],
                    current_date
                )
                task.start_process()
            except Exception, e :
                print e
                logNotifyError("AuditTrailAutoDeleteion", e)
                logNotifyError("AuditTrailAutoDeleteion", (traceback.format_exc()))

def run_audit_trail_process():
    np = AuditTrailProcess()
    np.begin_process()