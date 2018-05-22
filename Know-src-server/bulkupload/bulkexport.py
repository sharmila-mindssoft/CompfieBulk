import os
import io
import csv
import uuid
import datetime
import mysql.connector
from .budatabase.buassignstatutorydb import (
    get_country_name_by_legal_entity_id
)
from server.constants import (
    CSV_DOWNLOAD_URL, KNOWLEDGE_DB_HOST,
    KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME, KNOWLEDGE_DB_PASSWORD,
    KNOWLEDGE_DATABASE_NAME
)

from bulkconstants import (
    CSV_DELIMITER, SYSTEM_REJECTED_BY
)

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
        except Exception:
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
        country_id, country_name = get_country_name_by_legal_entity_id(
            request.le_id
        )

        download_assign_compliance_list = db.call_proc(
            'sp_download_assign_statutory_template',
            [
                client_group_name, country_name, le_name,
                domain_names, unit_names
            ]
        )

        sno = 0
        if len(download_assign_compliance_list) > 0:
            for ac in download_assign_compliance_list:
                sno = sno + 1
                client_group = ac["client_group"]
                country = ac["country"]
                legal_entity = ac["legal_entity"]
                domain = ac["domain"]
                organization = ac["organization"].replace(",", CSV_DELIMITER)
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
                        "S.No", "Client_Group", "Country", "Legal_Entity",
                        "Domain", "Organization", "Unit_Code", "Unit_Name",
                        "Unit_Location", "Primary_Legislation",
                        "Secondary_Legislation", "Statutory_Provision",
                        "Compliance_Task", "Compliance_Description",
                        "Statutory_Applicable_Status*", "Statutory_remarks",
                        "Compliance_Applicable_Status*"
                    ]

                    self.write_csv(csv_headers, None)
                    is_header = True
                csv_values = [
                    sno, client_group, country, legal_entity, domain,
                    organization, unit_code, unit_name, unit_location,
                    perimary_legislation, secondary_legislation,
                    statutory_provision, compliance_task_name,
                    compliance_description, "", "", ""
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
        country_id_list = ",".join(str(e) for e in request.c_ids)
        domain_id_list = ",".join(str(e) for e in request.d_ids)
        child_ids = request.child_ids
        if(child_ids is not None):
            user_ids = ",".join(str(e) for e in child_ids)
        else:
            user_ids = session_user.user_id()
        user_name_list = ",".join(
            getUserNameAndCode(cnx_pool, e) for e in child_ids)
        from_date = datetime.datetime.strptime(request.from_date, '%d-%b-%Y')
        to_date = datetime.datetime.strptime(request.to_date, '%d-%b-%Y')

        export_bu_statutory_list = db.call_proc(
            'sp_export_statutory_mappings_bulk_reportdata',
            [user_ids, country_id_list, domain_id_list, from_date, to_date])
        sno = 0

        exported_time = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')
        if len(export_bu_statutory_list) > 0:
            for ac in export_bu_statutory_list:
                sno = sno + 1
                country_name = ac["country_name"]
                domain_name = ac["domain_name"]
                uploaded_by = ac["uploaded_by"]
                uploaded_by_name = getUserNameAndCode(cnx_pool, uploaded_by)
                uploaded_on = datetime.datetime.strftime(ac["uploaded_on"],
                                                         '%d-%b-%Y %H:%M')
                domain_name = ac["domain_name"]
                csv_name = ac["csv_name"]
                total_records = ac["total_records"]
                total_rejected_records = ac["total_rejected_records"]
                if total_rejected_records is None:
                    total_rejected_records = 0
                rejected_by_name = ""
                approved_by_name = ""
                if(
                    ac["declined_count"] is not None and ac["declined_count"]
                ) >= 1:
                    rejected_by_name = SYSTEM_REJECTED_BY
                    approved_by_name = SYSTEM_REJECTED_BY
                else:
                    rejected_by = ac["rejected_by"]
                    rejected_by_name = getUserNameAndCode(cnx_pool,
                                                          rejected_by)
                    approved_by = ac["approved_by"]
                    approved_by_name = getUserNameAndCode(cnx_pool,
                                                          approved_by)
                rejected_on = ac["rejected_on"]
                approved_on = ac["approved_on"]
                approvedRejectedOn = ""
                approvedRejectedBy = ""
                if rejected_on is not None:
                    approvedRejectedOn = datetime.datetime.strftime(
                        ac["rejected_on"], '%d-%b-%Y %H:%M')
                    approvedRejectedBy = rejected_by_name
                if approved_on is not None:
                    approvedRejectedOn = datetime.datetime.strftime(
                        ac["approved_on"], '%d-%b-%Y %H:%M')
                    approvedRejectedBy = approved_by_name
                approve_status = ac["total_approve_records"]
                approve_reject_task = str(approve_status) + " / " + str(
                    total_rejected_records)
                reason_for_rejection = ""
                if (ac["is_fully_rejected"] == 1):
                    approve_reject_task = "-"
                    reason_for_rejection = ac["rejected_reason"]
                if not is_header:
                    # {'1': ['1', '3', '2'], '3': ['4'], '2': ['1', '3', '2']}
                    self.write_to_csv_statumapping(
                        request, user_name_list, exported_time, cnx_pool
                    )
                    is_header = True
                csv_values = [
                    sno, country_name, domain_name, uploaded_by_name,
                    uploaded_on, csv_name, total_records, approve_reject_task,
                    approvedRejectedOn, approvedRejectedBy,
                    reason_for_rejection
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None
        cnx_pool.close()


    def write_to_csv_statumapping(
        self, request, user_name_list, exported_time, cnx_pool
    ):

        c_d_ids = convert_array_map(request.c_d_ids)
        print "c_d_id->>>>>>>> ", c_d_ids
        # c_d_ids = {'1': ['1', '3', '2'], '2': ['1', '3', '2']}

        c_d_names = ''
        for cntry_id, dom_ids in c_d_ids.iteritems():
            cntry_name = getCountryName(cnx_pool, cntry_id)
            print "cntry_name->> ", cntry_name
            c_d_names += cntry_name + " - "

            c_d_names += ",".join(getDomainName(cnx_pool, d) for d in dom_ids)
            c_d_names += " "
        print "c_d_names->> ", c_d_names

        text = "Statutory Mapping - Bulk Upload Report"
        csv_header_line1 = [
            "", "", "", "", "", text, "", "", "", "", ""
        ]
        self.write_csv(csv_header_line1, None)
        csv_header_line2 = [
            "", "", "", "Country", request.c_names, "", "Domain",
            c_d_names, "", "", ""
        ]
        self.write_csv(csv_header_line2, None)
        csv_header_line3 = [
            "", "", "", "From Date", request.from_date, "",
            "To Date", request.to_date, "", "", ""
        ]
        self.write_csv(csv_header_line3, None)
        csv_header_line4 = [
            "", "", "", "KE Name", user_name_list, "",
            "Exported Date and Time", exported_time, "", "", ""
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


    def generate_export_client_unit_bulk(self, db, request, session_user):
        is_header = False
        # try:
        cnx_pool = connectKnowledgeDB()
        clientGroupId = request.bu_client_id
        clientGroupName = request.bu_group_name
        from_date = datetime.datetime.strptime(request.from_date, '%d-%b-%Y')
        to_date = datetime.datetime.strptime(request.to_date, '%d-%b-%Y')
        child_ids = request.child_ids
        if(child_ids is not None):
            user_ids = ",".join(str(e) for e in child_ids)
        else:
            user_ids = session_user.user_id()
        user_name_list = ",".join(
            getUserNameAndCode(cnx_pool, e) for e in child_ids)
        export_bu_client_unit_report = db.call_proc(
            'sp_export_client_unit_bulk_reportdata',
            [clientGroupId, from_date, to_date, str(user_ids)]
        )
        sno = 0
        exported_time = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')
        if len(export_bu_client_unit_report) > 0:
            for cu in export_bu_client_unit_report:
                sno = sno + 1
                uploaded_by = cu["uploaded_by"]
                uploaded_by_name = getUserNameAndCode(cnx_pool, uploaded_by)
                uploaded_on = datetime.datetime.strftime(cu["uploaded_on"],
                                                         '%d-%b-%Y %H:%M')
                csv_name = cu["csv_name"]
                total_records = cu["total_records"]
                total_rejected_records = cu["total_rejected_records"]
                if total_rejected_records is None:
                    total_rejected_records = 0
                rejected_by_name = ""
                approved_by_name = ""
                if(
                    cu["declined_count"] is not None and
                    cu["declined_count"]
                ) >= 1:
                    rejected_by_name = SYSTEM_REJECTED_BY
                    approved_by_name = SYSTEM_REJECTED_BY
                else:
                    rejected_by = cu["rejected_by"]
                    rejected_by_name = getUserNameAndCode(cnx_pool,
                                                          rejected_by)
                    approved_by = cu["approved_by"]
                    approved_by_name = getUserNameAndCode(cnx_pool,
                                                          approved_by)
                rejected_on = cu["rejected_on"]
                approved_on = cu["approved_on"]
                approvedRejectedOn = ""
                approvedRejectedBy = ""
                if rejected_on is not None:
                    approvedRejectedOn = datetime.datetime.strftime(
                        cu["rejected_on"], '%d-%b-%Y %H:%M')
                    approvedRejectedBy = rejected_by_name
                if approved_on is not None:
                    approvedRejectedOn = datetime.datetime.strftime(
                        cu["approved_on"], '%d-%b-%Y %H:%M')
                    approvedRejectedBy = approved_by_name
                approve_status = cu["total_approve_records"]
                approve_reject_task = str(approve_status) + " / " + str(
                    total_rejected_records)
                reason_for_rejection = ""
                if (cu["is_fully_rejected"] == 1):
                    approve_reject_task = "-"
                    reason_for_rejection = cu["rejected_reason"]
                if not is_header:
                    self.write_to_csv_clientunit(
                        request, user_name_list, exported_time, clientGroupName
                    )
                    is_header = True
                csv_values = [
                    sno, uploaded_by_name, uploaded_on,
                    csv_name, total_records, approve_reject_task,
                    approvedRejectedOn, approvedRejectedBy,
                    reason_for_rejection
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None
        cnx_pool.close()

    def write_to_csv_clientunit(
        self, request, user_name_list, exported_time, clientGroupName
    ):
        text = "Client Unit - Bulk Upload Report"
        csv_header_line1 = [
            "", "", "", "", "", text, "", "", "", "", ""
        ]
        self.write_csv(csv_header_line1, None)
        csv_header_line2 = [
            "", "", "", "Client Group", clientGroupName, "",
            "TE Name ", user_name_list, "", "", ""
        ]
        self.write_csv(csv_header_line2, None)
        csv_header_line3 = [
            "", "", "", "From Date", request.from_date, "",
            "To Date", request.to_date, "", "", ""
        ]
        self.write_csv(csv_header_line3, None)
        csv_header_line4 = [
            "", "", "", "Exported Date and Time ", exported_time,
            "", "", "", "", "", ""
        ]
        self.write_csv(csv_header_line4, None)
        csv_header_line5 = ["S.No", "Uploaded By", "Uploaded On",
                            "Uploaded File Name", "No. Of Units",
                            "Approved / Rejected Units",
                            "Approved / Rejected On",
                            "Approved / Rejected By",
                            "Reason for Rejection"]
        self.write_csv(csv_header_line5, None)


    def generate_export_assigned_statutory_bulk(
        self, db, request, session_user
    ):
        is_header = False
        cnx_pool = connectKnowledgeDB()
        domainIds = request.domain_ids
        from_date = datetime.datetime.strptime(request.from_date, '%d-%b-%Y')
        to_date = datetime.datetime.strptime(request.to_date, '%d-%b-%Y')
        child_ids = request.child_ids
        if(child_ids is not None):
            user_ids = ",".join(str(e) for e in child_ids)
        else:
            user_ids = session_user.user_id()
        if(domainIds is not None):
            domain_ids = ",".join(map(str, domainIds))

        user_name_list = ",".join(
            getUserNameAndCode(cnx_pool, e) for e in child_ids)
        export_bu_assigned_statutory_report = db.call_proc(
            'sp_export_assigned_statutory_bulk_reportdata',
            [request.bu_client_id, request.bu_legal_entity_id,
             request.bu_unit_id, from_date, to_date,
                str(user_ids), domain_ids])
        sno = 0
        exported_time = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')
        if len(export_bu_assigned_statutory_report) > 0:
            for asr in export_bu_assigned_statutory_report:
                sno = sno + 1
                uploaded_by = asr["uploaded_by"]
                uploaded_by_name = getUserNameAndCode(cnx_pool, uploaded_by)
                uploaded_on = datetime.datetime.strftime(asr["uploaded_on"],
                                                         '%d-%b-%Y %H:%M')
                csv_name = asr["csv_name"]
                total_records = asr["total_records"]
                total_rejected_records = asr["total_rejected_records"]
                print "total_rejected_records >>> ", total_rejected_records
                if total_rejected_records is None:
                    total_rejected_records = 0
                result_domain = asr["domain_names"]
                rejected_by_name = ""
                approved_by_name = ""
                if (
                    asr["declined_count"] is not None and
                    asr["declined_count"]
                ) >= 1:
                    rejected_by_name = SYSTEM_REJECTED_BY
                    approved_by_name = SYSTEM_REJECTED_BY
                else:
                    rejected_by = asr["rejected_by"]
                    rejected_by_name = getUserNameAndCode(cnx_pool,
                                                          rejected_by)
                    approved_by = asr["approved_by"]
                    approved_by_name = getUserNameAndCode(cnx_pool,
                                                          approved_by)
                rejected_on = asr["rejected_on"]
                approved_on = asr["approved_on"]
                approvedRejectedOn = ""
                approvedRejectedBy = ""
                if rejected_on is not None:
                    approvedRejectedOn = datetime.datetime.strftime(
                        asr["rejected_on"], '%d-%b-%Y %H:%M')
                    approvedRejectedBy = rejected_by_name
                if approved_on is not None:
                    approvedRejectedOn = datetime.datetime.strftime(
                        asr["approved_on"], '%d-%b-%Y %H:%M')
                    approvedRejectedBy = approved_by_name
                approve_status = asr["total_approve_records"]
                approve_reject_task = str(approve_status) + " / " + str(
                    total_rejected_records)
                reason_for_rejection = ""
                if (asr["is_fully_rejected"] == 1):
                    approve_reject_task = "-"
                    reason_for_rejection = asr["rejected_reason"]
                if not is_header:
                    self.write_to_csv_assignstatu(
                        request, user_name_list, exported_time
                    )
                    is_header = True
                csv_values = [
                    sno, result_domain, uploaded_by_name, uploaded_on,
                    csv_name, total_records, approve_reject_task,
                    approvedRejectedOn, approvedRejectedBy,
                    reason_for_rejection
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None
        cnx_pool.close()

    def write_to_csv_assignstatu(
        self, request, user_name_list, exported_time
    ):
        text = "Assigned Statutory - Bulk Upload Report"
        csv_header_line1 = [
            "", "", "", "", "", text, "", "", "", "", "", ""]
        self.write_csv(csv_header_line1, None)
        csv_header_line2 = [
            "", "", "", "Client Group", request.bu_group_name, "",
            "Legal Entity ", request.legal_entity_name,
            "", "", "", ""
        ]
        self.write_csv(csv_header_line2, None)
        csv_header_line3 = [
            "", "", "", "Domain", request.d_names, "",
            "Unit", request.unit_name, "", "", "", ""
        ]
        self.write_csv(csv_header_line3, None)
        csv_header_line4 = [
            "", "", "", "From Date", request.from_date, "",
            "To Date", request.to_date, "", "", "", ""
        ]
        self.write_csv(csv_header_line4, None)
        csv_header_line5 = [
            "", "", "", "Exported Date and Time", exported_time,
            "", "DE Name", user_name_list, "", "", ""
        ]
        self.write_csv(csv_header_line5, None)
        csv_header_line6 = ["S.No", "Domain", "Uploaded By",
                            "Uploaded On", "Uploaded File Name",
                            "No. Of Tasks",
                            "Approved / Rejected Tasks",
                            "Approved / Rejected On",
                            "Approved / Rejected By",
                            "Reason for Rejection"]
        self.write_csv(csv_header_line6, None)


def connectKnowledgeDB():
    try:
        cnx = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME,
            password=KNOWLEDGE_DB_PASSWORD,
            host=KNOWLEDGE_DB_HOST,
            database=KNOWLEDGE_DATABASE_NAME,
            port=KNOWLEDGE_DB_PORT,
            autocommit=False,
        )
        return cnx
    except Exception, e:
        print "Connection Exception Caught"
        print e


def getUserNameAndCode(cnx_pool, userId):
    query = "select employee_code, employee_name " + \
            "from tbl_users  as t1 where t1.user_id = %s ;"
    condition_val = []
    user_name_res = ''
    condition_val.append(userId)
    c = cnx_pool.cursor(dictionary=True, buffered=True)
    result = c.execute(query, condition_val)
    result = c.fetchall()
    user_name_res = ""
    for row in result:
        if row["employee_code"] is not None:
            user_name_res = row["employee_code"] + " - " + row["employee_name"]
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

def convert_array_map(c_d_ids_list):
    keymap = []
    dom_map = {}
    for i in c_d_ids_list:
        c = i.split('-')[0]
        if c not in keymap:
            keymap.append(c)

    for k in keymap:
        dom_map[k] = []

    for i in c_d_ids_list:
        c = i.split('-')[0]
        d = i.split('-')[1]
        dom_map[c].append(str(d))

    print dom_map
    return dom_map
