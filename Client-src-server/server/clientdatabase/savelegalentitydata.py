from server.dbase import Database

__all__ = [
    "LegalEntityReplicationManager",
]

class LegalEntityReplicationManager(object):
    def __init__(
        self, group_db_info, time_out_seconds, callback
    ):
        self._group_db_info = group_db_info
        self._time_out_seconds = time_out_seconds
        self._callback = callback
        self._first_time = True

    def _start(self):
        self._poll()

    def _initiate_connction(self):
        con = Database.make_connection(self._group_db_info)
        _db = Database(con)
        return _db

    def _poll(self):
        def on_timeout():
            rows = []
            _db = self._initiate_connction()
            q = "select legal_entity_id, user_data, settings_data, provider_data " + \
                " from tbl_le_replication_status where user_data = 1 or settings_data = 1 " + \
                " provider_data = 1 "
            try :
                _db.begin()
                rows = _db.select_all(q)
            except Exception, e :
                print e
                _db.rollback()

            finally :
                _db.close()
                self._poll_response(rows)

        if self._first_time :
            self._first_time = False
            on_timeout()

    def _poll_response(self, response):
        self._callback(response)
