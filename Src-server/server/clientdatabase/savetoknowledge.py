from server.dbase import Database
from server.exceptionmessage import client_process_error
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)

class KnowledgedbConnect(object):
    def __init__(self):
        self._k_db = None

    def get_knowledge_connect(self):
        self._k_db = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT,
            KNOWLEDGE_DB_USERNAME, KNOWLEDGE_DB_PASSWORD,
            KNOWLEDGE_DATABASE_NAME
        )
        self._k_db.connect()

class UpdateFileSpace(KnowledgedbConnect):
    def __init__(self, space_used, client_id):
        super(UpdateFileSpace, self).__init__()
        self._space_used = space_used
        self._client_id = client_id
        self.procee_update_space()

    def _update_space(self):
        q = "Update tbl_client_groups set total_disk_space_used = %s \
            where client_id = %s "
        res = self._k_db.execute(q, [self._space_used, self._client_id])
        if res is False :
            raise client_process_error("E021")

    def procee_update_space(self):
        try:
            self.get_knowledge_connect()
            self._k_db.begin()
            self._update_space()
            self._k_db.commit()
            self._k_db.close()
            return True
        except Exception, e:
            print e
            self._k_db.rollback()
            raise client_process_error("E021")
