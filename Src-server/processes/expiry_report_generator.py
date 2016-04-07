import os
import xlsxwriter
import zipfile
import datetime
import shutil

__all__ =[

    "ExpiryReportGenerator"
]

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CLIENT_DOCS_BASE_PATH = os.path.join(ROOT_PATH, "clientdocuments")
# CLIENT_URL = "http://45.118.182.47:8082/"
CLIENT_URL = "http://localhost:8080/"
docment_path = "documents/"

class ExpiryReportGenerator(object):

    def __init__(self, client_id, db):
        self.client_id = client_id
        self.db = db

    def datetime_to_string(self, datetime_val):
        if datetime_val is not None:
            date_in_string = datetime_val.strftime("%d-%b-%Y")
        else:
            date_in_string = ""
        return date_in_string

    def convert_to_dict(self, data_list, columns) :
        assert type(data_list) in (list, tuple)
        if len(data_list) > 0:
            if type(data_list[0]) is tuple :
                result_list = []
                if len(data_list[0]) == len(columns) :
                    for data in data_list:
                        result = {}
                        for i, d in enumerate(data):
                            result[columns[i]] = d
                        result_list.append(result)
                return result_list
            else :
                result = {}
                if len(data_list) == len(columns) :
                    for i, d in enumerate(data_list):
                        result[columns[i]] = d
                return result
        else:
            return []

    def generate_report(self):
        # Getting Data
        query_columns = "c.compliance_task, c.document_name, c.compliance_description, ch.start_date, ch.due_date,\
        ch.completion_date, ch.validity_date, ch.remarks, ch.completed_on, ch.concurred_on, ch.approved_on,\
        (SELECT concat(unit_code, '-', unit_name) FROM tbl_units un WHERE un.unit_id = ch.unit_id),\
        (SELECT concat(employee_code, '-', employee_name) FROM tbl_users us WHERE us.user_id = ch.completed_by), \
        (SELECT concat(employee_code, '-', employee_name) FROM tbl_users us WHERE us.user_id = ch.concurred_by), \
        (SELECT concat(employee_code, '-', employee_name) FROM tbl_users us WHERE us.user_id = ch.approved_by), \
        ch.documents"
        query = "SELECT %s FROM tbl_compliance_history ch INNER JOIN tbl_compliances c ON \
        (c.compliance_id = ch.compliance_id) " % query_columns
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [
            "compliance_name", "document_name", "description", "start_date", "due_date", 
            "completion_date", "validity_date", "remarks", "completed_on", "concurred_on", 
            "approved_on", "unit_name", "assignee", "concurrence_person", "approval_person",
            "documents"
        ]
        results = self.convert_to_dict(rows, columns)
 
        # Paths
        self.folder_path = "./expired/%s/" % str(self.client_id)
        self.excel_file_path = "%s/ComplianceDetails.xlsx" % (self.folder_path) 

        # Create Directory
        os.makedirs(self.folder_path)
        os.chmod(self.folder_path, 0777)

        # Creating Work Sheet
        workbook = xlsxwriter.Workbook(self.excel_file_path )
        worksheet = workbook.add_worksheet('ComplianceDetails')
        worksheet.set_column('A:A', 30)

        # Formats
        bold = workbook.add_format({'bold': 1})
        url_format = workbook.add_format({
            'font_color': 'blue',
            'underline':  1
        })

        # Writing Headers
        worksheet.write('A1', 'Unit Name', bold)
        worksheet.write('B1', 'Compliance Name', bold)
        worksheet.write('C1', 'Description', bold)
        worksheet.write('D1', 'Start Date', bold)
        worksheet.write('E1', 'Due Date', bold)
        worksheet.write('F1', 'Completion Date', bold)
        worksheet.write('G1', 'Validity Date', bold)
        worksheet.write('H1', 'Remarks', bold)
        worksheet.write('I1', 'Assignee', bold)
        worksheet.write('J1', 'Completed On', bold)
        worksheet.write('K1', 'Concurrence Person', bold)
        worksheet.write('L1', 'Concurred On', bold)
        worksheet.write('M1', 'Approval Person', bold)
        worksheet.write('N1', 'Approved On', bold)
        worksheet.write('O1', 'Documents', bold)


        # Starting from the row below header
        row = 1
        col = 0
        for index, result in enumerate(results):
            compliance_name = result["compliance_name"]
            if result["document_name"] not in [None, "None"]:
                compliance_name = "%s - %s" % (
                    result["document_name"], result["compliance_name"]
                )

            worksheet.write_string(row, col, result["unit_name"])
            worksheet.write_string(row, col+1, compliance_name)
            worksheet.write_string(row, col+2, result["description"])
            worksheet.write_string(row, col+3, self.datetime_to_string(result["start_date"]))
            worksheet.write_string(row, col+4, self.datetime_to_string(result["due_date"]))
            worksheet.write_string(row, col+5, self.datetime_to_string(result["completion_date"]))
            worksheet.write_string(row, col+6, self.datetime_to_string(result["validity_date"]))
            worksheet.write_string(row, col+7, "" if result["remarks"] is None else result["remarks"])
            worksheet.write_string(row, col+8, result["assignee"])
            worksheet.write_string(row, col+9, self.datetime_to_string(result["completed_on"]))
            worksheet.write_string(row, col+10, "" if result["concurrence_person"] is None else result["concurrence_person"])
            worksheet.write_string(row, col+11, self.datetime_to_string(result["concurred_on"]))
            worksheet.write_string(row, col+12, "Administrator" if result["approval_person"] is None else result["approval_person"])
            worksheet.write_string(row, col+13, self.datetime_to_string(result["approved_on"]))

            # writing document links
            docs = [] if result["documents"] is None else result["documents"].split(",")
            if len(docs) > 0:
                col_index = 14
                for doc in docs:
                    if doc in [None, "None", ""]:
                        continue
                    file_name_parts = doc.split("-")
                    file_name = file_name_parts[0]
                    unique_id_with_extention = file_name_parts[1]
                    unique_id_parts = unique_id_with_extention.split(".")
                    extention = unique_id_parts[1]
                    file_name_with_extention = "%s.%s" % (file_name, extention)
                    original_path = "%s%s" % (docment_path, doc)
                    worksheet.write_url(row, col+col_index, original_path, url_format, file_name_with_extention)
                    col_index += 1
            row += 1        
        workbook.close()
        zip_file_name = self.generateZipFile()
        download_link = "%sdownload/bkup/%s/%s" % (
            CLIENT_URL, self.client_id, zip_file_name
        )
        return download_link

    def generateZipFile(self):
        temp_path = "./expired/%s/documents" % str(self.client_id)
        os.makedirs(temp_path)
        os.chmod(temp_path, 0777)

        abs_src = "%s/%s" % (CLIENT_DOCS_BASE_PATH, self.client_id)
        for dirname, subdirs, files in os.walk(abs_src):
            for filename in files:
                shutil.copy(abs_src+"/"+filename, temp_path)

        timestamp = datetime.datetime.utcnow()
        report_generated_date = self.datetime_to_string(timestamp)
        zip_file_name = "ComplianceDetails-%s.zip" % (report_generated_date)
        zip_file_path = "./expired/%s/%s" % (str(self.client_id), zip_file_name)
        zf = zipfile.ZipFile( zip_file_path, "w", zipfile.ZIP_DEFLATED)

        abs_src = "./expired/%s" % str(self.client_id)
        for dirname, subdirs, files in os.walk(abs_src):
            for filename in files:
                if filename == zip_file_name:
                    continue
                absname = os.path.join(dirname, filename)
                arcname = absname[len(abs_src) + 0:]
                zf.write(absname, arcname)
        shutil.rmtree(temp_path, ignore_errors=True)
        os.remove(self.excel_file_path)
        zf.close()
        return zip_file_name