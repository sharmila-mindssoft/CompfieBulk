# import datetime
import csv
import os
import io
import zipfile
# import shutil
import uuid
import traceback
import xlsxwriter
from server.common import datetime_to_string_time, string_months
__all__ = [
    "ExportData", "UnitClosureExport"
]


ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..", "..")
CLIENT_DOCS_BASE_PATH = os.path.join(ROOT_PATH, "clientdocuments")

EXPORT_PATH = os.path.join(ROOT_PATH, "exported_reports")
FILE_DOWNLOAD_BASE_PATH = "/download/csv"

class ExportData(object):
    def __init__(self):
        pass

    def get_unique_id(self):
        s = str(uuid.uuid4())
        return s

    def export_to_csv(self, headers, data, file_name):
        file_path = os.path.join(EXPORT_PATH, file_name)
        with io.FileIO(file_path, "wb+") as f :
            writer = csv.writer(f)
            writer.writerow(headers)
            for d in data :
                writer.writerow(d)

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
                if i == url_column and d != "":
                    worksheet.write_url(row, col+i, d, url_format, dat[i + 1])
                else :
                    worksheet.write_string(row, col+i, d)
            row += 1

    def generate_to_zip(self, zip_file_name, csv_source_path, csv_file_name, soruce_dir_path):
        # print soruce_dir_path
        # print os.path.exists(soruce_dir_path)
        zip_file_name = zip_file_name + '.zip'
        zip_path = os.path.join(EXPORT_PATH, zip_file_name)
        zfw = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
        csv_absname = os.path.join(csv_source_path, csv_file_name)
        csv_arcname = csv_absname[len(csv_source_path) + 0:]
        zfw.write(csv_absname, csv_arcname)
        # remove excel file after added in zi
        # shutil.rmtree("%s/%s" % (csv_absname, csv_arcname), ignore_errors=True)
        os.remove(csv_absname)
        print "Excel added in zip"

        for dirname, subdirs, files in os.walk(soruce_dir_path):
            for file in files :
                absname = os.path.join(dirname, file)
                arcname = absname[len(soruce_dir_path) + 0:]

                zfw.write(absname, arcname)

        zfw.close()
        return zip_file_name


class UnitClosureExport(ExportData):
    def __init__(self, db, unit_id, closed_on):
        super(UnitClosureExport, self).__init__()
        self.unit_id = unit_id
        self.db = db
        self.closed_on = closed_on
        self.unitname = None

    def get_unit_name(self):
        q = "select unit_id, client_id, country_id, legal_entity_id, business_group_id, division_id, category_id, " + \
            " unit_code, unit_name, address from tbl_units where unit_id = %s"
        row = self.db.select_one(q, [self.unit_id])
        unitname = None

        if row :
            unitname = "%s-%s-%s" % (row.get("unit_code"), row.get("unit_name"), row.get("address"))
        self.unitname = unitname
        return unitname, row

    def fetch_data_to_export(self):
        q = "select distinct t1.compliance_task, t1.document_name, t1.statutory_provision, t1.compliance_description, " + \
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
            " inner join tbl_units as t3 on t2.unit_id = t3.unit_id where t2.unit_id = %s " + \
            " order by t2.start_date, t2.due_date"
        rows = self.db.select_all(q, [self.unit_id])
        print self.unit_id
        data = []
        for r in rows :
            if r["due_date"] is None :
                continue

            url_column = ""
            if r["documents"] is not None :
                year = r["start_date"].year
                month = "%s%s" % (string_months[r["start_date"].month], str(year))
                file_path = "%s/%s/%s" % (
                    r["domain_id"], year, month
                )
                url_column = "%s/%s" % (file_path, r["documents"])

            data.append([
                r.get("compliance_task"), r.get("document_name"),
                r.get("statutory_provision"), r.get("compliance_description"),
                r.get("penal_consequences"), datetime_to_string_time(r.get("start_date")),
                datetime_to_string_time(r.get("due_date")),
                "" if r.get("completion_date") is None else datetime_to_string_time(r.get("completion_date")),
                "" if r.get("validity_date") is None else datetime_to_string_time(r.get("validity_date")),
                "" if r.get("remarks") is None else r.get("remarks"),
                r.get("assignee"),
                "" if r.get("completed_on") is None else datetime_to_string_time(r.get("completed_on")),
                r.get("concur"),
                "" if r.get("concurred_on") is None else datetime_to_string_time(r.get("concurred_on")),
                r.get("approver"),
                "" if r.get("approved_on") is None else datetime_to_string_time(r.get("approved_on")),
                url_column,
                "" if r.get("documents") is None else r.get("documents")
            ])
        return data

    def notify_to_admin(self, export_link):
        unitname, unit_data = self.get_unit_name()
        extra_datail = "/closure/%s" % (export_link)
        if unitname :
            bg_id = unit_data.get("business_group_id")

            div_id = unit_data.get("division_id")
            action = "%s has been closed " % (unitname)
            column = [
                    "country_id",
                    "legal_entity_id", "unit_id",
                    "notification_type_id",
                    "notification_text", "extra_details", "created_on"
                ]
            values = [
                unit_data.get("country_id"),
                unit_data.get("legal_entity_id"), self.unit_id, 2,
                action, extra_datail, self.closed_on
            ]
            if bg_id is not None :
                column.append("business_group_id")
                values.append(bg_id)
            if div_id is not None :
                column.append("division_id")
                values.append(div_id)

            notification_id = self.db.insert("tbl_notifications_log", column, values)

            if notification_id is False :
                return False
            q = "select t1.user_id from tbl_users as t1 left join tbl_user_units t2 on t1.user_id = t2.user_id " + \
                " and t2.unit_id = %s  where t1.user_category_id != 2 and t1.user_category_id <= 4 "
            users = self.db.select_all(q, [self.unit_id])

            for u in users :
                self.db.save_notification_users(notification_id, u["user_id"])

    def save_download_session(self, _db, expiry_date, export_session):
        q = "insert into tbl_email_verification (user_id, verification_code, verification_type_id, expiry_date) " + \
            "values(%s, %s, %s, %s)"
        _db.execute(q, [1, export_session, 3, expiry_date])

    def fetch_unit_path(self):
        nfo = self.get_unit_name()[1]
        client_path = os.path.join(CLIENT_DOCS_BASE_PATH, str(nfo.get("client_id")))
        country_id = os.path.join(client_path, str(nfo.get("country_id")))
        legal_entity_path = os.path.join(country_id, str(nfo.get("legal_entity_id")))
        unit_path = os.path.join(legal_entity_path, str(nfo.get("unit_id")))

        return unit_path

    def perform_export(self):
        try :
            data = self.fetch_data_to_export()
            headers = [
                "Compliance task", "Document name", "Statutory provision", "Compliance description",
                "Penal consequences", "Start date", "Due date", "Completion date", "Validity date",
                "Remarks", "Assignee name", "Completed on", "Concurrence name", "Concurred on",
                "Approver name", "Approved on", "Documents"
            ]
            source_path = self.fetch_unit_path()
            # print source_path
            csv_filename = "%s_%s_%s.xlsx" % (self.unitname, "compliances", self.get_unique_id())
            # self.export_to_csv(headers, data, csv_filename)
            self.export_to_excel(headers, data, csv_filename, url_column=16)

            zip_filename = "%s_%s" % (self.unitname, self.get_unique_id())

            zip_file_link = self.generate_to_zip(zip_filename, EXPORT_PATH, csv_filename, source_path)
            self.notify_to_admin(zip_file_link)
            return zip_file_link

        except Exception, e :
            print e
            print(traceback.format_exc())
            return None
