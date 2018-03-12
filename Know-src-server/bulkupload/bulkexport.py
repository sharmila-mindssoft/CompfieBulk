import os
import io
import csv
import uuid
import datetime
import mysql.connector
from server.constants import (
    CSV_DOWNLOAD_URL, KNOWLEDGE_DB_HOST,
    KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME, KNOWLEDGE_DB_PASSWORD,
    KNOWLEDGE_DATABASE_NAME)

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CSV_PATH = os.path.join(ROOT_PATH, "exported_reports")
FILE_DOWNLOAD_BASE_PATH = "/download/csv"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"


class ConvertJsonToCSV(object):
    def __init__(self, db, request, session_user, report_type):
        s = str(uuid.uuid4())
        file_name = "%s.csv" % s.replace("-", "")
        self.FILE_DOWNLOAD_PATH = "%s/%s" % (
            CSV_DOWNLOAD_URL, file_name)
        self.FILE_PATH = "%s/%s" % (CSV_PATH, file_name)
        self.documents_list = []
        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)
        if report_type == "AssigneeWise":
            self.generate_assignee_wise_report_and_zip(
                    db, request, session_user
                )
        else:
            with io.FileIO(self.FILE_PATH, "wb+") as f:
                self.writer = csv.writer(f)
                # self.header, quoting=csv.QUOTE_ALL)
                # self.convert_json_to_csv(jsonObj)
                if report_type == "DownloadAssignStatutory":
                    self.generate_download_assign_statutory(
                        db, request, session_user)
                elif report_type == "ExportSMBulkReport":
                    self.generate_export_statutory_mapping(
                        db, request, session_user)
                elif report_type == "ExportCUBulkReport":
                    self.generate_export_client_unit_bulk(
                        db, request, session_user)
                elif report_type == "ExportASBulkReport":
                    self.generate_export_assigned_statutory_bulk(
                        db, request, session_user)

    def to_string(self, s):
        try:
            return str(s)
        except:
            return s.encode('utf-8')

    def write_csv(self, header, values=None):
        if header:
            self.writer.writerow(header)
        if values:
            self.writer.writerow(values)

    def generate_download_assign_statutory(self, db, request, session_user):
        is_header = False

        client_group_name = request.cl_name
        le_name = request.le_name
        domain_names = ",".join(str(e) for e in request.d_names)
        unit_names = ",".join(str(e) for e in request.u_names)

        download_assign_compliance_list = db.call_proc(
            'sp_download_assign_statutory_template', [client_group_name , le_name,
            domain_names, unit_names]
            )

        sno = 0
        if len(download_assign_compliance_list) > 0:
            for ac in download_assign_compliance_list:
                sno = sno + 1
                client_group = ac["client_group"]
                legal_entity = ac["legal_entity"]
                domain = ac["domain"]
                organization = ac["organization"]
                unit_code = ac["unit_code"]
                unit_name = ac["unit_name"]
                unit_location = ac["unit_location"]
                perimary_legislation = ac["perimary_legislation"]
                secondary_legislation = ac["secondary_legislation"]
                statutory_provision = ac["statutory_provision"]
                compliance_task_name = ac["compliance_task_name"]
                compliance_description = ac["compliance_description"]

                if not is_header:
                    csv_headers = [
                        "S.No", "Client_Group", "Legal_Entity", "Domain",
                        "Organisation", "Unit_Code", "Unit_Name_",
                        "Unit_Location", "Primary_Legislation_",
                        "Secondary_Legislaion", "Statutory_Provision_",
                        "Compliance_Task_", "Compliance_Description_",
                        "Statutory_Applicable_Status*", "Statutory_remarks",
                        "Compliance_Applicable_Status*"
                    ]
                    
                    self.write_csv(csv_headers, None)
                    is_header = True
                csv_values = [
                    sno, client_group, legal_entity, domain, organization,
                    unit_code, unit_name, unit_location, perimary_legislation,
                    secondary_legislation, statutory_provision,
                    compliance_task_name, compliance_description,
                    "", "", ""
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_export_statutory_mapping(self, db, request, session_user):
        is_header = False
        # try:
        cnx_pool = connectKnowledgeDB()

        # c_ids = request.c_ids
        country_id_list = ",".join(str(e) for e in request.c_ids)
        print "country_id_list-> ", country_id_list
        # country_name_list = ",".join(
        #     getCountryName(cnx_pool, e) for e in request.c_ids)

        country_name_list = request.c_names
        print country_name_list
        # d_ids = request.c_ids
        domain_id_list = ",".join(str(e) for e in request.d_ids)
        print "domain_id_list-> ", domain_id_list
        # domain_name_list = ",".join(
        #     getDomainName(cnx_pool, e) for e in request.d_ids)
        domain_name_list = request.d_names
        child_ids = request.child_ids
        if(child_ids is not None):
            user_ids = ",".join(str(e) for e in request.child_ids)
        else:
            user_ids = session_user.user_id()

        print "user_ids->", user_ids
        user_name_list = ",".join(
            getUserNameAndCode(cnx_pool, e) for e in request.child_ids)

        from_date = request.from_date
        print from_date
        from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y')

        to_date = request.to_date
        to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y')

        export_bu_statutory_list = db.call_proc(
            'sp_export_statutory_mappings_bulk_reportdata',
            [user_ids, country_id_list, domain_id_list, from_date, to_date]
            )
        sno = 0
        if len(export_bu_statutory_list) > 0:
            for ac in export_bu_statutory_list:
                sno = sno + 1
                country_name = ac["country_name"]
                domain_name = ac["domain_name"]
                uploaded_by = ac["uploaded_by"]
                uploaded_by_name = getUserNameAndCode(cnx_pool, uploaded_by)
                print "uploaded_by_name-> ", uploaded_by_name

                uploaded_on = ac["uploaded_on"]
                domain_name = ac["domain_name"]
                csv_name = ac["csv_name"]
                total_records = ac["total_records"]
                total_rejected_records = ac["total_rejected_records"]
                # approved_by = ac["approved_by"]
                rejected_by = ac["rejected_by"]
                rejected_by_name = getUserNameAndCode(cnx_pool, rejected_by)
                # approved_on = ac["approved_on"]
                rejected_on = ac["rejected_on"]
                reason_for_rejection = ac["rejected_reason"]
                # is_fully_rejected = ac["is_fully_rejected"]
                approve_status = ac["approve_status"]
                approve_reject_task = str(approve_status) + " / " + str(
                                                    total_rejected_records)
                exported_time = datetime.datetime.now()

                if not is_header:
                    text = "Statutory Mapping - Bulk Report"
                    csv_header_line1 = [
                        "", "", "", "", "", text, "", "", "", "", ""
                    ]
                    self.write_csv(csv_header_line1, None)
                    csv_header_line2 = [
                        "", "", "", "Country", country_name_list, "", "Domain",
                        domain_name_list, "", "", ""
                    ]
                    self.write_csv(csv_header_line2, None)
                    csv_header_line3 = [
                        "", "", "", "From Date", from_date, "", "To Date",
                        to_date, "", "", ""
                    ]
                    self.write_csv(csv_header_line3, None)
                    csv_header_line4 = [
                        "", "", "", "User ", user_name_list, "",
                        "Exported Time", exported_time, "", "", ""
                    ]
                    self.write_csv(csv_header_line4, None)
                    csv_header_line5 = ["S.No", "Country", "Domain",
                                        "Uploaded By", "Uploaded On",
                                        "Uploaded File Name", "No. Of Tasks",
                                        "Approved / Rejected Tasks",
                                        "Approved / Rejected On",
                                        "Approved / Rejected By",
                                        "Reason for Rejection"]
                    self.write_csv(csv_header_line5, None)
                    is_header = True
                csv_values = [
                    sno, country_name, domain_name, uploaded_by_name,
                    uploaded_on, csv_name, total_records, approve_reject_task,
                    rejected_on, rejected_by_name, reason_for_rejection
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_export_client_unit_bulk(self, db, request, session_user):
        is_header = False

        cnx_pool = connectKnowledgeDB()

        clientGroupId = request.bu_client_id
        clientGroupName = request.bu_group_name
        child_ids = request.child_ids
        # user_category_id = request.user_category_id

        from_date = request.from_date
        print from_date
        from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y')

        to_date = request.to_date
        to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y')

        child_ids = request.child_ids
        if(child_ids is not None):
            user_ids = ",".join(str(e) for e in request.child_ids)
        else:
            user_ids = session_user.user_id()

        print "user_ids->", user_ids
        user_name_list = ",".join(
            getUserNameAndCode(cnx_pool, e) for e in request.child_ids)

        export_bu_client_unit_report = db.call_proc(
            'sp_export_client_unit_bulk_reportdata',
            [clientGroupId, from_date, to_date, str(user_ids)]
            )
        sno = 0
        if len(export_bu_client_unit_report) > 0:
            for cu in export_bu_client_unit_report:
                sno = sno + 1
                uploaded_by = cu["uploaded_by"]
                uploaded_by_name = getUserNameAndCode(cnx_pool, uploaded_by)
                uploaded_on = cu["uploaded_on"]
                csv_name = cu["csv_name"]
                total_records = cu["total_records"]
                total_rejected_records = cu["total_rejected_records"]
                # approved_by = cu["approved_by"]
                rejected_by = cu["rejected_by"]
                rejected_by_name = getUserNameAndCode(cnx_pool, rejected_by)
                # approved_on = cu["approved_on"]
                rejected_on = cu["rejected_on"]
                # is_fully_rejected = cu["is_fully_rejected"]
                approve_status = cu["approve_status"]
                reason_for_rejection = cu["rejected_reason"]
                approve_reject_task = str(approve_status) + " / " + str(
                                                    total_rejected_records)
                exported_time = datetime.datetime.now()
                if not is_header:
                    text = "Client Unit - Bulk Report"
                    csv_header_line1 = [
                        "", "", "", "", "", text, "", "", "", "", ""
                    ]
                    self.write_csv(csv_header_line1, None)
                    csv_header_line2 = [
                        "", "", "", "Client Group", clientGroupName, "",
                        "User ", user_name_list, "", "", ""
                    ]
                    self.write_csv(csv_header_line2, None)
                    csv_header_line3 = [
                        "", "", "", "From Date", from_date, "", "To Date",
                        to_date, "", "", ""
                    ]
                    self.write_csv(csv_header_line3, None)
                    csv_header_line4 = [
                        "", "", "", "Exported Time ", exported_time, "", "",
                        "", "", "", ""
                    ]
                    self.write_csv(csv_header_line4, None)
                    csv_header_line5 = ["S.No", "Uploaded By", "Uploaded On",
                                        "Uploaded File Name", "No. Of Units",
                                        "Approved / Rejected Units",
                                        "Approved / Rejected On",
                                        "Approved / Rejected By",
                                        "Reason for Rejection"]
                    self.write_csv(csv_header_line5, None)
                    is_header = True
                csv_values = [
                    sno, uploaded_by_name, uploaded_on,
                    csv_name, total_records, approve_reject_task,
                    rejected_on, rejected_by_name, reason_for_rejection
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_export_assigned_statutory_bulk(self, db, request, session_user):
        is_header = False
        cnx_pool = connectKnowledgeDB()
        clientGroupId = request.bu_client_id
        clientGroupName = request.bu_group_name
        legalEntityId = request.bu_legal_entity_id
        legalEntityName = request.legal_entity_name
        unitId = request.bu_unit_id
        unitName = request.unit_name
        domainIds = ",".join(str(e) for e in request.domain_ids)
        d_names = request.d_names
        from_date = request.from_date
        to_date = request.to_date
        child_ids = request.child_ids
        # user_category_id = request.user_category_id

        from_date = request.from_date
        print from_date
        from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y')

        to_date = request.to_date
        to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y')

        child_ids = request.child_ids
        if(child_ids is not None):
            user_ids = ",".join(str(e) for e in request.child_ids)
        else:
            user_ids = session_user.user_id()

        print "user_ids->", user_ids
        user_name_list = ",".join(
            getUserNameAndCode(cnx_pool, e) for e in request.child_ids)

        export_bu_assigned_statutory_report = db.call_proc(
            'sp_export_assigned_statutory_bulk_reportdata',
            [clientGroupId, legalEntityId, unitId, from_date, to_date,
                str(user_ids), domainIds]
            )
        sno = 0
        if len(export_bu_assigned_statutory_report) > 0:
            for asr in export_bu_assigned_statutory_report:
                sno = sno + 1
                uploaded_by = asr["uploaded_by"]
                uploaded_by_name = getUserNameAndCode(cnx_pool, uploaded_by)
                uploaded_on = asr["uploaded_on"]
                csv_name = asr["csv_name"]
                total_records = asr["total_records"]
                total_rejected_records = asr["total_rejected_records"]
                result_domain = asr["domain"]
                # approved_by = asr["approved_by"]
                rejected_by = asr["rejected_by"]
                rejected_by_name = getUserNameAndCode(cnx_pool, rejected_by)
                # approved_on = asr["approved_on"]
                rejected_on = asr["rejected_on"]
                # is_fully_rejected = asr["is_fully_rejected"]
                approve_status = asr["approve_status"]
                reason_for_rejection = asr["rejected_reason"]
                approve_reject_task = str(approve_status) + " / " + str(
                                                    total_rejected_records)
                exported_time = datetime.datetime.now()
                if not is_header:
                    text = "Assigned Statutory - Bulk Report"
                    csv_header_line1 = [
                        "", "", "", "", "", text, "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_header_line1, None)
                    csv_header_line2 = [
                        "", "", "", "Client Group", clientGroupName, "",
                        "Legal Entity ", legalEntityName, "", "", "", ""
                    ]
                    self.write_csv(csv_header_line2, None)
                    csv_header_line3 = [
                        "", "", "", "Domain", d_names, "",
                        "Unit", unitName, "", "", "", ""
                    ]
                    self.write_csv(csv_header_line3, None)
                    csv_header_line4 = [
                        "", "", "", "From Date", from_date, "", "To Date",
                        to_date, "", "", "", ""
                    ]
                    self.write_csv(csv_header_line4, None)
                    csv_header_line5 = [
                        "", "", "", "Exported Time ", exported_time, "",
                        "User", user_name_list, "", "", ""
                    ]
                    self.write_csv(csv_header_line5, None)
                    csv_header_line6 = ["S.No", "Domain", "Uploaded By",
                                        "Uploaded On", "Uploaded File Name",
                                        "No. Of Units",
                                        "Approved / Rejected Units",
                                        "Approved / Rejected On",
                                        "Approved / Rejected By",
                                        "Reason for Rejection"]
                    self.write_csv(csv_header_line6, None)
                    is_header = True
                csv_values = [
                    sno, result_domain, uploaded_by_name, uploaded_on,
                    csv_name, total_records, approve_reject_task,
                    rejected_on, rejected_by_name, reason_for_rejection
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None


def connectKnowledgeDB():
    cnx = mysql.connector.connect(
        user=KNOWLEDGE_DB_USERNAME,
        password=KNOWLEDGE_DB_PASSWORD,
        host=KNOWLEDGE_DB_HOST,
        database=KNOWLEDGE_DATABASE_NAME,
        port=KNOWLEDGE_DB_PORT,
        autocommit=False,
    )
    return cnx


def getUserNameAndCode(cnx_pool, userId):
    query = "select employee_code, employee_name " + \
           "from tbl_users  as t1 where t1.user_id = %s ;"
    condition_val = []
    condition_val.append(userId)
    c = cnx_pool.cursor(dictionary=True, buffered=True)
    result = c.execute(query, condition_val)
    result = c.fetchall()
    for row in result:
        if row["employee_code"] is not None:
            user_name_res = row["employee_code"] + " - "+row["employee_name"]
        else:
            user_name_res = row["employee_name"]
    return user_name_res


def getCountryName(cnx_pool, countryId):
    query = "select country_name " + \
           "from tbl_countries  as t1 where t1.country_id = %s ;"
    print query
    condition_val = []
    condition_val.append(countryId)
    c = cnx_pool.cursor(dictionary=True, buffered=True)
    result = c.execute(query, condition_val)
    result = c.fetchall()
    print "Res0", result[0]
    for row in result:
        countryName = row["country_name"]
    print "countryName ", countryName
    return countryName

def getDomainName(cnx_pool, domainId):
    query = "select domain_name " + \
           "from tbl_domains  as t1 where t1.domain_id = %s ;"
    condition_val = []
    condition_val.append(domainId)
    c = cnx_pool.cursor(dictionary=True, buffered=True)
    result = c.execute(query, condition_val)
    result = c.fetchall()
    print "Res0", result[0]
    for row in result:
        domainName = row["domain_name"]
    print "domName ", domainName
    return domainName
