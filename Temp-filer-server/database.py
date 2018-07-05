import traceback
import logger


class Database(object):
    def __init__(self, mysql_connection):
        self._connection = mysql_connection
        self._cursor = None

    ########################################################
    # To Redirect Requests to Functions
    ########################################################
    def cursor(self):
        return self._cursor

    def _db_connect(self, host, username, password, database):
        pass
        # return mysql.connect(host, username, password, database)

    ########################################################
    # To Close database connection
    ########################################################
    def close(self):
        assert self._connection is not None
        if self._cursor is not None:
            self._cursor.close()
        self._connection.close()
        self._connection = None

    ########################################################
    # To begin a database transaction
    ########################################################
    def begin(self):
        assert self._connection is not None
        assert self._cursor is None
        self._cursor = self._connection.cursor(dictionary=True, buffered=True)
        return self._cursor

    ########################################################
    # To commit a database transaction
    ########################################################
    def commit(self):
        assert self._connection is not None
        assert self._cursor is not None
        self._cursor.close()
        self._connection.commit()
        self._cursor = None

    ########################################################
    # To rollback a connection
    ########################################################
    def rollback(self):
        assert self._connection is not None
        assert self._cursor is not None
        self._cursor.close()
        self._connection.rollback()
        self._cursor = None

    def validate_session_token(self, session_token):
        query = "SELECT t01.user_id FROM tbl_user_sessions t01 " + \
            " inner JOIN tbl_user_login_details t02 ON t01.user_id = t02.user_id " + \
            " and is_active = 1 " + \
            " WHERE  session_token=%s"
        param = [session_token]
        row = self.select_one(query, param)
        logger.logTempFiler(
            "query", "validate_session_token",
            "query:%s, param:%s" % (query, param)
        )
        user_id = None
        if row:
            user_id = row["user_id"]
            self.update_session_time(session_token)
        return user_id

    def update_session_time(self, session_token):
        q = "update tbl_user_sessions set last_accessed_time = current_ist_datetime() " + \
            "where session_token = %s "
        self.execute(q, [str(session_token)])
        logger.logTempFiler(
            "query", "update_session_time",
            "query:%s, param:%s" % (q, [str(session_token)])
        )

    def select_one(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None

        try:
            if param is None:
                cursor.execute(query)
            else:
                if type(param) is tuple:

                    cursor.execute(query, param)
                elif type(param) is list:
                    cursor.execute(query, param)
                else:
                    cursor.execute(query)
            cursor.nextset()
            res = cursor.fetchone()
            cursor.nextset()
            return res

        except Exception, e:
            logger.logTempFiler(
                "error", "database.py > select_one()", str(e)
            )
            logger.logTempFiler(
                "error", "database.py > select_one()",
                str(traceback.format_exc())
            )
            raise RuntimeError(str(e))

    def select_all(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if param is None:
                cursor.execute(query)
            else:
                if type(param) is tuple:
                    cursor.execute(query, param)

                elif type(param) is list:
                    cursor.execute(query, param)

                else:
                    cursor.execute(query)
            cursor.nextset()
            res = cursor.fetchall()
            cursor.nextset()
            return res

        except Exception, e:
            logger.logTempFiler(
                "error", "database.py > select_all()", str(e)
            )
            logger.logTempFiler(
                "error", "database.py > select_all()",
                str(traceback.format_exc())
            )
            raise RuntimeError(str(e))

    def execute(self, query, param=None):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if type(param) is tuple:
                cursor.execute(query, param)

            elif type(param) is list:
                cursor.execute(query, param)

            else:
                cursor.execute(query)

            cursor.nextset()
            return True

        except Exception, e:
            logger.logTempFiler(
                "error", "database.py > execute()", str(e)
            )
            logger.logTempFiler(
                "error", "database.py > execute()",
                str(traceback.format_exc())
            )
            raise RuntimeError(str(e))

    def call_update_proc(self, procedure_name, args):
        cursor = self.cursor()
        assert cursor is not None
        try:
            if args is None:
                cursor.callproc(procedure_name)
            else:
                cursor.callproc(procedure_name, args)

            cursor.nextset()
        except Exception, e:
            logger.logTempFiler(
                "error", "database.py > call_update_proc()", str(e)
            )
            logger.logTempFiler(
                "error", "database.py > call_update_proc()",
                str(traceback.format_exc())
            )
            raise RuntimeError(str(e))
        return True

    def update_file_status(self, old_file_name, csv_id, file_name, file_size):
        param = [old_file_name, csv_id, file_name, file_size]
        return self.call_update_proc(
            "sp_sm_format_file_status_update", param
        )

    def update_format_file_status(self, csv_id, status):
        res_update_stats = self.call_update_proc(
            "sp_sm_file_download_status_update", [csv_id, status]
        )
        return res_update_stats

    def update_file_status_client(
            self, old_file_name, csv_id, file_name, file_size
    ):
        param = [old_file_name, csv_id, file_name, file_size]
        return self.call_update_proc(
            "sp_ct_format_file_status_update", param
        )

    def update_past_data_document_status(
        self, csv_id, status
    ):
        res_update_stats = self.call_update_proc(
            "sp_pastdata_doc_download_status_update", [csv_id, status]
        )
        return res_update_stats

    def get_declined_docs(self, csv_id):

        query = "SELECT distinct format_file FROM tbl_bulk_statutory_mapping" \
                " WHERE csv_id=%s and action = 3 and format_file not in" \
                " (SELECT format_file FROM tbl_bulk_statutory_mapping" \
                " WHERE csv_id=%s and" \
                " (action !=3 or action IS NULL or action =''))"

        param = [int(csv_id), int(csv_id)]
        row = self.select_all(query, param)
        logger.logTempFiler(
            "query", "get_declined_docs",
            "query:%s, param:%s" % (query, param))
        dec_doc_list = []
        for r in row:
            print "r-> ", r
            if r["format_file"] is not None:
                dec_doc_list.append(r["format_file"].encode('ascii', 'ignore'))

        print "dec_doc_list ", dec_doc_list
        return dec_doc_list
