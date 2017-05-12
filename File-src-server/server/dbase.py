import os
import uuid
import zipfile
import xlsxwriter
import traceback
import mysql.connector

from server.constants import CLIENT_DOCS_BASE_PATH, EXPORT_PATH

class Database(object):
    def __init__(
        self,
        mysqlConnection
    ):
        self._connection = mysqlConnection
        self._cursor = None
        self._for_client = False

        self.string_months = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }

    def get_unique_id(self):
        s = str(uuid.uuid4())
        return s

    def datetime_to_string_time(self, datetime_val):
        datetime_in_string = datetime_val
        if datetime_val is not None:
            datetime_in_string = datetime_val.strftime("%d-%b-%Y %H:%M")
        return datetime_in_string

    def cursor(self):
        return self._cursor

    @classmethod
    def make_connection(self, username, password, db_name, ip_address, ip_port):
        try:

            return mysql.connector.connect(
                autocommit=False,
                user=username,
                password=password,
                host=ip_address,
                database=db_name,
                port=ip_port
            )
        except Exception, e:
            raise ValueError(str(e))

    ########################################################
    # To Close database connection
    ########################################################
    def close(self):
        assert self._connection is not None
        if self._cursor is not None :
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

    ########################################################
    # To execute a query
    ########################################################
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
            print e
            return False

    ########################################################
    # To execute select query
    # Used to fetch multiple rows
    # select_all: query is string and param is tuple which return result in tuple of tuples
    # select_one: query is string and param is typle which return result in tuple
    ########################################################
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
            print e
            raise RuntimeError("process failed")

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
            print e
            raise RuntimeError("process failed")

    def reconnect(self):
        self.close()
        self.connect()

    def fetch_data_to_export(self):
        q = "select distinct group_concat(t3.unit_code, ' - ', t3.unit_name) as unitname, " + \
            " t1.compliance_task, t1.document_name, t1.statutory_provision, t1.compliance_description, " + \
            " t1.penal_consequences,t2.start_date, t2.due_date, t2.completion_date, t2.validity_date, " + \
            " t2.remarks, (select group_concat(employee_code, ' - ', employee_name) from tbl_users where user_id = t2.completed_by) as assignee, " + \
            " t2.completed_on, " + \
            " (select group_concat(employee_code,' - ', employee_name) from tbl_users where user_id = t2.concurred_by) as concur, " + \
            " t2.concurred_on,  " + \
            " (select group_concat(ifnull(employee_code, 'Administrator'), ' - ', employee_name) from tbl_users where user_id = t2.approved_by) as approver, " + \
            " t2.approved_on, t2.documents, " + \
            " t3.country_id, t3.client_id, t3.legal_entity_id, t3.unit_id, t1.domain_id " + \
            " from tbl_compliances as t1 " + \
            " inner join tbl_compliance_history as t2 on t1.compliance_id = t2.compliance_id " + \
            " inner join tbl_units as t3 on t2.unit_id = t3.unit_id  " + \
            " order by t2.unit_id, t2.start_date, t2.due_date"

        rows = self.select_all(q, None)

        data = []
        for r in rows :
            if r["due_date"] is None :
                continue

            url_column = ""
            if r["documents"] is not None :
                year = r["start_date"].year
                month = "%s%s" % (self.string_months[r["start_date"].month], str(year))
                file_path = "%s/%s/%s/%s" % (
                    r["unit_id"], r["domain_id"], year, month
                )
                url_column = "%s/%s" % (file_path, r["documents"])

            data.append([
                r.get("unitname"),
                r.get("compliance_task"), r.get("document_name"),
                r.get("statutory_provision"), r.get("compliance_description"),
                r.get("penal_consequences"), self.datetime_to_string_time(r.get("start_date")),
                self.datetime_to_string_time(r.get("due_date")),
                "" if r.get("completion_date") is None else self.datetime_to_string_time(r.get("completion_date")),
                "" if r.get("validity_date") is None else self.datetime_to_string_time(r.get("validity_date")),
                "" if r.get("remarks") is None else r.get("remarks"),
                r.get("assignee"),
                "" if r.get("completed_on") is None else self.datetime_to_string_time(r.get("completed_on")),
                r.get("concur"),
                "" if r.get("concurred_on") is None else self.datetime_to_string_time(r.get("concurred_on")),
                r.get("approver"),
                "" if r.get("approved_on") is None else self.datetime_to_string_time(r.get("approved_on")),
                url_column,
                "" if r.get("documents") is None else r.get("documents")
            ])
        return data

    def get_le_name(self, le_id):
        q = "select legal_entity_name from tbl_legal_entities where legal_entity_id = %s"
        row = self.select_one(q, [le_id])
        return row["legal_entity_name"]

    def perform_export(self, le_id):
        try :
            le_name = self.get_le_name(le_id)
            le_name = le_name.replace(' ', '_')
            print le_name
            data = self.fetch_data_to_export()
            print data
            headers = [
                "Unit name",
                "Compliance task", "Document name", "Statutory provision", "Compliance description",
                "Penal consequences", "Start date", "Due date", "Completion date", "Validity date",
                "Remarks", "Assignee name", "Completed on", "Concurrence name", "Concurred on",
                "Approver name", "Approved on", "Documents"
            ]
            source_path = self.fetch_le_path(le_id)
            # print source_path
            csv_filename = "%s_%s.xlsx" % ("unitwise_compliances", self.get_unique_id())
            self.export_to_excel(headers, data, csv_filename, url_column=16)

            zip_filename = "%s-data" % (le_name)

            zip_file_link = self.generate_to_zip(
                zip_filename, EXPORT_PATH, csv_filename, source_path
            )
            print zip_file_link
            return True

        except Exception, e :
            print e
            print(traceback.format_exc())
            return False

    def get_unit_name(self, legal_entity_id):
        q = "select unit_id, client_id, country_id, legal_entity_id, business_group_id, division_id, category_id, " + \
            " unit_code, unit_name, address from tbl_units where legal_entity_id = %s "
        row = self.select_one(q, [legal_entity_id])
        unitname = None
        print row
        print "----------------------------"
        if row :
            unitname = "%s-%s-%s" % (row.get("unit_code"), row.get("unit_name"), row.get("address"))
        self.unitname = unitname
        return unitname, row

    def fetch_le_path(self, le_id):
        nfo = self.get_unit_name(le_id)[1]
        client_path = os.path.join(CLIENT_DOCS_BASE_PATH, str(nfo.get("client_id")))
        country_id = os.path.join(client_path, str(nfo.get("country_id")))
        legal_entity_path = os.path.join(country_id, str(nfo.get("legal_entity_id")))

        return legal_entity_path

    def generate_to_zip(self, zip_file_name, csv_source_path, csv_file_name, soruce_dir_path):
        zip_file_name = zip_file_name + '.zip'
        zip_path = os.path.join(EXPORT_PATH, zip_file_name)
        zfw = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
        csv_absname = os.path.join(csv_source_path, csv_file_name)
        csv_arcname = csv_absname[len(csv_source_path) + 0:]
        zfw.write(csv_absname, csv_arcname)
        os.remove(csv_absname)
        print "Excel added in zip"

        for dirname, subdirs, files in os.walk(soruce_dir_path):
            for file in files :
                absname = os.path.join(dirname, file)
                arcname = absname[len(soruce_dir_path) + 0:]

                zfw.write(absname, arcname)

        zfw.close()
        return zip_file_name

    def export_to_excel(self, headers, data, file_name, url_column):
        file_path = os.path.join(EXPORT_PATH, file_name)
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet('ComplianceDetails')
        worksheet.set_column('A:A', 30)
        bold = workbook.add_format({'bold': 1})
        url_format = workbook.add_format({
            'font_color': 'blue',
            'underline':  1
        })
        cells = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for idx, h in enumerate(headers):
            if idx < 26 :
                x = idx
            else :
                x = idx - 26

            c = "%s%s" % (cells[x], 1)
            worksheet.write(c, h, bold)

        row = 1
        col = 0
        for idx, dat in enumerate(data):
            for i, d in enumerate(dat[:-1]):
                if d is None :
                    d = ""
                if i == url_column and d != "":
                    worksheet.write_url(row, col+i, d, url_format, dat[i + 1])
                else :
                    worksheet.write_string(row, col+i, d)
            row += 1
