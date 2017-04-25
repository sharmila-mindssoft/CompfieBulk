import os
import io
import csv
import uuid
import shutil
import zipfile
import datetime
import json
from server.constants import CSV_DOWNLOAD_URL
from server.common import (
    string_to_datetime, datetime_to_string
)

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CSV_PATH = os.path.join(ROOT_PATH, "exported_reports")
FILE_DOWNLOAD_BASE_PATH = "/download/csv"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"

def generate_organization_map(organizations):
    org_map = {}
    header_list = []
    for organization in organizations:
        legal_entity_id = organization["legal_entity_id"]
        organization_name = organization["organization_name"]
        if organization_name not in header_list:
            header_list.append(organization_name)
        if legal_entity_id not in org_map:
            org_map[legal_entity_id] = []
        org_map[legal_entity_id].append(
            {
                'organization_name': organization_name,
                'count': organization["count"]
            }
        )
    return org_map, header_list

def generate_organization_domain_map(organizations):
    org_map = {}
    header_list = []
    for organization in organizations:
        legal_entity_id = organization["legal_entity_id"]
        organization_name = organization["organization_name"]
        domain_id = organization["domain_id"]
        combine_id = str(legal_entity_id) + '-' + str(domain_id);
        if organization_name not in header_list:
            header_list.append(organization_name)
        if combine_id not in org_map:
            org_map[combine_id] = []
        org_map[combine_id].append(
            {
                'organization_name': organization_name,
                'count': organization["count"]
            }
        )
    return org_map, header_list

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
                if report_type == "ActivityReport":
                    self.generate_compliance_activity_report(
                        db, request, session_user)
                elif report_type == "RiskReport":
                    self.generate_risk_report(db, request, session_user)
                elif report_type == "ComplianceDetails":
                    self.generate_compliance_details_report(
                        db, request, session_user)
                elif report_type == "TaskApplicability":
                    self.generate_task_applicability_report(
                        db, request, session_user)
                elif report_type == "Reassign":
                    self.generate_reassign_history_report(
                        db, request, session_user)
                elif report_type == "StatutoryNotification":
                    self.generate_statutory_notification_report(
                        db, request, session_user)
                elif report_type == "ServiceProviderWise":
                    self.generate_service_provider_wise_report(
                        db, request, session_user)
                elif report_type == "ClientAgreementReport":
                    self.generate_client_agreement_report(
                        db, request, session_user)
                elif report_type == "DomainwiseAgreementReport":
                    self.generate_domainwise_agreement_report(
                        db, request, session_user)
                elif report_type == "UserMappingReport":
                    self.generate_user_mapping_report(
                        db, request, session_user)
                elif report_type == "ClientUnitDetailsReport":
                    self.generate_client_details_report(
                        db, request, session_user)
                elif report_type == "ReassignUserReport":
                    self.generate_reassign_user_report(
                        db, request, session_user)
                elif report_type == "AuditTraiReport":
                    self.generate_audit_trail_report(
                        db, request, session_user)
                elif report_type == "AllocateServerReport":
                    self.generate_allocate_server_report(
                        db, request, session_user)
                elif report_type == "IPSettingReport":
                    self.generate_ip_setting_report(
                        db, request, session_user)
                elif report_type == "GroupAdminRegistrationEMail":
                    self.generate_group_admin_email_report(
                        db, request, session_user)
                elif report_type == "StatutorySettingsReport":
                    self.generate_statutory_setting_report(
                        db, request, session_user)

    def generate_assignee_wise_report_and_zip(
        self, db, request, session_user
    ):
        s = str(uuid.uuid4())
        docs_path = "%s/%s" % (CSV_PATH, s)
        self.temp_path = "%s/%s" % (CSV_PATH, s)
        self.create_a_csv("Assigneewise compliance count")
        self.generate_assignee_wise_report_data(
            db, request, session_user
        )
        self.generateZipFile(
            docs_path, self.documents_list
        )

    def create_a_csv(self, file_name=None):
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)
        if file_name is None:
            s = str(uuid.uuid4())
            file_name = "%s.csv" % s.replace("-", "")
        else:
            s = file_name
            file_name = "%s.csv" % s
        self.documents_list.append(file_name)
        self.FILE_PATH = "%s/%s" % (self.temp_path, file_name)

    def generateZipFile(self, abs_src, documents):
        # abs_src = "%s/%s" % (FILE_DOWNLOAD_BASE_PATH, self.client_id)
        # for dirname, subdirs, files in os.walk(temp_path):
        #     for filename in files:
        #         if filename in documents:
        #             shutil.copy(abs_src+"/"+filename, temp_path)

        timestamp = datetime.datetime.utcnow()
        # report_generated_date = self.datetime_to_string(timestamp)
        zip_file_name = "AssigneewiseComplianceDetails%s.zip" % (
            timestamp)
        zip_file_path = "%s/%s" % (
            CSV_PATH, zip_file_name
        )
        self.FILE_DOWNLOAD_PATH = "%s/%s" % (
            FILE_DOWNLOAD_BASE_PATH, zip_file_name
        )
        print "zip_file_path :=====================> %s" % zip_file_path
        zf = zipfile.ZipFile(
            zip_file_path, "w", zipfile.ZIP_DEFLATED
        )
        print "created zip file: %s" % zf
        # abs_src = "./%s/%s" % (
        #     type_of_report, str(self.client_id)
        # )
        for dirname, subdirs, files in os.walk(abs_src):
            for filename in files:
                if filename == zip_file_name:
                    continue
                absname = os.path.join(dirname, filename)
                arcname = absname[len(abs_src) + 0:]
                zf.write(absname, arcname)
        shutil.rmtree(abs_src, ignore_errors=True)
        # os.remove(self.excel_file_path)
        zf.close()
        return zip_file_name

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

    def generate_audit_trail_report(
        self, db, request, session_user
    ):
        from_date = request.from_date
        to_date = request.to_date
        user_id = request.user_id_search
        form_id = request.form_id_search
        category_id = request.category_id
        unit_id = request.unit_id
        client_id = request.client_id
        legal_entity_id = request.legal_entity_id
        if user_id is None:
            user_id = '%'
        if form_id is None :
            form_id = '%'
        if category_id is None :
            category_id = '%'
        if unit_id is None :
            unit_id = '%'
        from_date = string_to_datetime(from_date).date()
        to_date = string_to_datetime(to_date).date()

        if client_id is None:
            args = [from_date, to_date, user_id, form_id, category_id]
            result = db.call_proc('sp_export_audit_trails', args)
        else:
            args = [from_date, to_date, user_id, form_id, category_id, client_id, legal_entity_id, unit_id]
            result = db.call_proc('sp_export_client_audit_trails', args)

        is_header = False
        if not is_header:
            csv_headers = [
                "User Name", "User Type", "Form Name", "Action",
                "Date & Time"
            ]
            self.write_csv(csv_headers, None)
            is_header = True

        for row in result:
            u_id = row["user_id"]
            form_id = row["form_id"]
            action = row["action"]
            date = row["created_on"].strftime("%d-%b-%Y %H:%M")
            user_name = row["employee_name"]
            user_category_name = row["user_category_name"]
            if user_name is None:
                user_name = "Administrator"
            form_name = "Login"
            if form_name.find("password") >= 0:
                form_name = "Change Password"
            elif form_id != 0:
                form_name = row["form_name"]
            csv_values = [
                user_name, user_category_name, form_name, action, date
            ]
            self.write_csv(None, csv_values)

    def generate_allocate_server_report(
        self, db, request, session_user
    ):
        client_id = request.client_id
        legal_entity_id = request.legal_entity_id

        if (client_id == 0):
            client_id = '%'
        if (legal_entity_id == 0):
            legal_entity_id = '%'
        args = [client_id, legal_entity_id]
        result = db.call_proc('sp_allocate_db_environment_report_export', args)
        is_header = False
        if not is_header:
            csv_headers = [
                "SNO", "Group Name", "Legal Entity Name",
                "Group Application Server Name", "Group Application Server IP/Port",
                "Group Database Server Name", "Group Database Server IP/Port",
                "LE Database Server Name", "LE Database Server IP/Port",
                "LE File Server Name", "LE File Server IP/Port"
            ]
            self.write_csv(csv_headers, None)
            is_header = True
        j = 1
        for row in result:
            csv_values = [
                j, row["group_name"], row["legal_entity_name"], row["machine_name"], row["machine_ip_port"],
                row["client_db_server_name"], row["client_db_s_ip_port"],
                row["db_server_name"], row["db_s_ip_port"], row["file_server_name"],
                row["file_s_ip_port"]
            ]
            j = j + 1
            self.write_csv(None, csv_values)

    def generate_reassign_user_report(
        self, db, request, session_user
    ):
        user_category_id = request.user_category_id
        user_id = request.user_id
        group_id = request.group_id_none
        if user_category_id == 5 or user_category_id == 6:
            if group_id is None or group_id == 0:
                args = [user_id, user_category_id, '%']
            else:
                args = [user_id, user_category_id, group_id]
            result = db.call_proc_with_multiresult_set("sp_reassign_user_report_getdata", args, 2)

            if len(result) > 0:
                is_header = False
                if not is_header:
                    csv_headers = [
                        "Country", "Group", "No. of Legal Entity", "Assign Date",
                        "Assigned", "Remarks"
                    ]
                    self.write_csv(csv_headers, None)
                    is_header = True

                for cl in result[0]:
                    c_names = []
                    client_id = int(cl.get("client_id"))
                    group_name = cl.get("group_name")
                    assigned_on = cl.get("assigned_on")
                    emp_code_name = cl.get("emp_code_name")
                    remarks = cl.get("remarks")
                    le_count = int(cl.get("le_count"))
                    last = object()
                    for country in result[1]:
                        if client_id == country.get("client_id"):
                            if last != country.get("country_name"):
                                last = country.get("country_name")
                                c_names.append(country.get("country_name"))
                    c_names = ",".join(c_names)
                    csv_values = [
                        c_names, group_name, le_count, assigned_on, emp_code_name, remarks
                    ]
                    self.write_csv(None, csv_values)
        else:
            if(user_category_id == 7 or user_category_id == 8):
                all_none = request.u_m_none
                bg_id = all_none.split(",")[0]
                le_id = all_none.split(",")[1]
                d_id = all_none.split(",")[2]
                if bg_id is None:
                    bg_id = '%'
                    args = [user_id, user_category_id, int(group_id), bg_id, int(le_id), int(d_id)]
                else:
                    args = [user_id, user_category_id, int(group_id), bg_id, int(le_id), int(d_id)]
                result = db.call_proc("sp_reassign_user_report_domain_user_getdata", args)
                if len(result) > 0:
                    is_header = False
                    if not is_header:
                        csv_headers = [
                            "Unit Code", "Unit Name", "Unit Location", "Assign Date",
                            "Assigned", "Remarks"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True

                    for d in result:
                        unit_code = d["unit_code"]
                        unit_name = d["unit_name"]
                        unit_location = d["geography_name"]+","+d["address"]+","+d["postal_code"]
                        assign_date = d["unit_email_date"]
                        assign_by = d["emp_code_name"]
                        remarks = d["remarks"]
                        csv_values = [
                            unit_code, unit_name, unit_location, assign_date, assign_by, remarks
                        ]
                        self.write_csv(None, csv_values)

    def generate_client_details_report(
        self, db, request, session_user
    ):
        country_id = request.country_id
        client_id = request.client_id
        legal_entity_id = request.legal_entity_id
        client_details_none_values = request.u_m_none
        bgrp_id = domain_id = org_id = unit_id = from_date = to_date = unit_status = None
        if client_details_none_values.find(",") > 0:
            bgrp_id = client_details_none_values.split(",")[0]
            domain_id = client_details_none_values.split(",")[2]
            org_id = client_details_none_values.split(",")[3]
            unit_id = client_details_none_values.split(",")[1]
            from_date = client_details_none_values.split(",")[4]
            # if (from_date is not None or from_date != 'null'):
            #     print "a"
            #     from_date = string_to_datetime(from_date).date()
            to_date = client_details_none_values.split(",")[5]
            # if to_date is not None or from_date != 'null':
            #     print "b"
            #     to_date = string_to_datetime(from_date).date()
            unit_status = client_details_none_values.split(",")[6]

        args = [session_user, country_id, client_id, legal_entity_id, bgrp_id, domain_id, org_id,
                unit_id, from_date, to_date, unit_status]

        client_details_dataset = []
        expected_result = 3
        client_details_dataset = db.call_proc_with_multiresult_set("sp_client_details_report_export_unitlist", (
            session_user, country_id, client_id, legal_entity_id, bgrp_id, domain_id, org_id,
            unit_id, from_date, to_date, unit_status), expected_result)
        unit_details = unit_domains = {}
        if(len(client_details_dataset) > 0):
            if(len(client_details_dataset[1]) > 0):
                unit_details = client_details_dataset[1]

            if(len(client_details_dataset[2]) > 0):
                unit_domains = client_details_dataset[2]

            is_header = False
            if not is_header:
                csv_headers = [
                    "Unit Code", "Unit Name", "Division", "Category",
                    "domain", "Unit Address", "Created By", "Created_on", "Status"
                ]
                self.write_csv(csv_headers, None)
                is_header = True


            for units in unit_details:
                unit_code = units.get("unit_code")
                unit_name = units.get("unit_name")
                division_name = units.get("division_name")
                if units.get("division_name") is None:
                    division_name = "-Nil-"
                category_name = units.get("category_name")
                if units.get("category_name") is None:
                    category_name = "-Nil-"

                unit_address = units.get("address")+","+str(units.get("postal_code"))
                created_by = units.get("emp_code_name")
                created_on = units.get("created_on")
                if units.get("is_active") == 0:
                    status = "Active"
                else:
                    closed_on = units.get("closed_on")
                    if closed_on is None:
                        closed_on = "-Nil-"
                    status = "Closed - "+closed_on
                domain_names = []
                for domain in unit_domains:
                    if (units.get("unit_id") == domain.get("unit_id")):
                        domain_names.append(domain.get("domain_name")+"-"+domain.get("organisation_name"))
                domain_names = ",".join(domain_names)
                csv_values = [
                    unit_code, unit_name, division_name, category_name, domain_names,
                    unit_address, created_by, created_on, status
                ]
                self.write_csv(None, csv_values)

    def generate_user_mapping_report(
        self, db, request, session_user
    ):
        country_id = request.country_id
        client_id = request.client_id
        legal_entity_id = request.legal_entity_id
        user_mapping_none_values = request.u_m_none
        bgrp_id = division_id = category_id = unit_id = 0
        if user_mapping_none_values.find(",") > 0:
            bgrp_id = user_mapping_none_values.split(",")[0]
            if bgrp_id == "0":
                bgrp_id = '%'
            division_id = user_mapping_none_values.split(",")[1]
            if division_id == "0":
                division_id = '%'
            category_id = user_mapping_none_values.split(",")[2]
            if category_id == "0":
                category_id = '%'
            unit_id = user_mapping_none_values.split(",")[3]
            if unit_id == "0":
                unit_id = '%'
        usermapping_report_dataset = []

        args = [session_user, client_id, legal_entity_id, country_id, bgrp_id, division_id, category_id, unit_id]
        expected_result = 4
        print args
        usermapping_report_dataset = db.call_proc_with_multiresult_set("sp_usermapping_report_details_for_export", (
            session_user, client_id, legal_entity_id, country_id, bgrp_id, division_id, category_id, unit_id),
            expected_result)
        print usermapping_report_dataset
        techno_details = unit_domains = domains = {}

        if(len(usermapping_report_dataset) > 0):
            if(len(usermapping_report_dataset[1]) > 0):
                techno_details = usermapping_report_dataset[1]

            if(len(usermapping_report_dataset[2]) > 0):
                unit_domains = usermapping_report_dataset[2]

            if(len(usermapping_report_dataset[3]) > 0):
                domains = usermapping_report_dataset[3]

            is_header = False
            if not is_header:
                csv_headers = ["Unit", "Techno Manager", "Techno User"]
                for domain in domains:
                    csv_headers.append("Domain Manager "+domain.get("domain_name"))
                    csv_headers.append("Domain User "+domain.get("domain_name"))
                self.write_csv(csv_headers, None)
                is_header = True

            for techs in techno_details:
                unitName = techs.get("unit_name")
                tech_mgr = techs.get("techno_manager")
                tech_user = techs.get("techno_user")
                csv_values = [unitName, tech_mgr, tech_user]
                columnCount = int(len(csv_headers))
                i = 3
                while (i < columnCount):
                    domain_user = "NA"
                    for unit in unit_domains:
                        if (unit.get("unit_id") == techs.get("unit_id")):
                            for domain in domains:
                                if(domain.get("domain_id") == unit.get("domain_id")):
                                    print "domain hdr"
                                    print csv_headers[i]
                                    temp_header = None
                                    if(csv_headers[i].find("Domain User") >= 0):
                                        print csv_headers[i].split(" ")[2]
                                        temp_header = "Domain Executive"+" "+csv_headers[i].split(" ")[2]+" "+csv_headers[i].split(" ")[3]
                                    else:
                                        temp_header = csv_headers[i]

                                    if(temp_header == (unit.get("user_category_name")+" "+domain.get("domain_name"))):
                                        domain_user = unit.get("employee_name")
                                        csv_values.append(domain_user)
                                        break
                                    else:
                                        continue
                    i = i + 1
                self.write_csv(None, csv_values)

    def generate_client_agreement_report(
        self, db, request, session_user
    ):
        is_header = False

        country_id = request.country_id
        client_id = request.client_id
        business_group_id = request.business_group_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.domain_id
        contract_from = request.contract_from
        contract_to = request.contract_to
        country_name = request.country_name

        if contract_from is not None:
            contract_from = string_to_datetime(contract_from).date()
        if contract_to is not None:
            contract_to = string_to_datetime(contract_to).date()

        client_agreement_list = db.call_proc_with_multiresult_set(
            "sp_client_agreement_details_export", [country_id, client_id, business_group_id,
        legal_entity_id, domain_id, contract_from, contract_to, session_user], 2
        )

        organization_map, header_lists = generate_organization_domain_map(client_agreement_list[1])

        sno = 0
        for client_agreement in client_agreement_list[0]:
            sno = sno + 1
            le_admin_contactno = 'Not Available'
            if client_agreement["le_admin_contactno"] is not None:
                le_admin_contactno = client_agreement["le_admin_contactno"]

            le_admin_email = 'Not Available'
            if client_agreement["le_admin_email"] is not None:
                le_admin_email = client_agreement["le_admin_email"]

            legal_entity_name = client_agreement["legal_entity_name"]
            total_licence = int(client_agreement["total_licence"])
            used_licence = int(client_agreement["used_licence"])
            file_space = int(client_agreement["file_space_limit"])
            used_file_space = int(client_agreement["used_file_space"])
            contract_from = datetime_to_string(client_agreement["contract_from"])
            contract_to = datetime_to_string(client_agreement["contract_to"])
            group_name=client_agreement["group_name"]
            group_admin_email=client_agreement["groupadmin_email"]
            is_active=bool(client_agreement["is_closed"])
            domain_count=int(client_agreement["domaincount"])
            d_name=client_agreement["domain_name"]
            domain_total_unit=int(client_agreement["domain_total_unit"])
            activation_date=datetime_to_string(client_agreement["activation_date"])
            domain_used_unit=int(client_agreement["domain_used_unit"])
            legal_entity_admin_contactno = le_admin_contactno
            legal_entity_admin_email = le_admin_email
            business_group_name=client_agreement["business_group_name"]
            status = 'Active'
            if(client_agreement["is_closed"] == 1):
                status = 'Closed'

            if not is_header:
                csv_headers = [
                    "S.No", "Country", "Group Name", "Business Group",
                    "Legal Entity", "License Allotted", "License Used",
                    "File Space Alloted in GB", "File Space Used in GB", "Group Admin Email",
                    "Legal Entity Admin Email", "Legal Entity Admin Contact No", "Domain Name",
                    "Total No. of Unit per Domain",  "No. of Units Used", "Date of Agmt Inception",
                    "Contract From", "Contract To"
                ]

                for header_list in header_lists:
                    csv_headers.append(header_list)

                csv_headers.append("Status")

                self.write_csv(csv_headers, None)
                is_header = True
            csv_values = [
                sno, country_name, group_name, business_group_name, legal_entity_name, 
                total_licence, used_licence, file_space, used_file_space, group_admin_email,
                legal_entity_admin_email, legal_entity_admin_contactno, d_name,
                domain_total_unit, domain_used_unit, activation_date, 
                contract_from, contract_to
            ]

            for header_list in header_lists:
                if domain_used_unit > 0:
                    count = ''
                    for org in organization_map[str(client_agreement["legal_entity_id"]) + '-' + str(client_agreement["domain_id"])]:
                        if header_list == org['organization_name']:
                            count = org['count']
                    csv_values.append(count)
                else:
                    csv_values.append('')

            csv_values.append(status)

            self.write_csv(None, csv_values)

    def generate_domainwise_agreement_report(
        self, db, request, session_user
    ):
        is_header = False
        country_id = request.country_id
        client_id = request.client_id
        business_group_id = request.business_group_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.domain_id
        contract_from = request.contract_from
        contract_to = request.contract_to
        country_name = request.country_name
        domain_name = request.domain_name
       
        if contract_from is not None:
            contract_from = string_to_datetime(contract_from).date()
        if contract_to is not None:
            contract_to = string_to_datetime(contract_to).date()

        client_agreement_list = db.call_proc_with_multiresult_set(
            "sp_domainwise_agreement_details_export", [country_id, client_id, business_group_id,
        legal_entity_id, domain_id, contract_from, contract_to, session_user], 2
        )

        organization_map, header_lists = generate_organization_map(client_agreement_list[1])
        
        sno = 0
        for client_agreement in client_agreement_list[0]:
            sno = sno + 1
            le_admin_contactno = 'Not Available'
            if client_agreement["le_admin_contactno"] is not None:
                le_admin_contactno = client_agreement["le_admin_contactno"]

            le_admin_email = 'Not Available'
            if client_agreement["le_admin_email"] is not None:
                le_admin_email = client_agreement["le_admin_email"]

            legal_entity_name = client_agreement["legal_entity_name"]
            contract_from = datetime_to_string(client_agreement["contract_from"])
            contract_to = datetime_to_string(client_agreement["contract_to"])
            group_name=client_agreement["group_name"]
            group_admin_email=client_agreement["groupadmin_email"]
            domain_total_unit=int(client_agreement["domain_total_unit"])
            activation_date=datetime_to_string(client_agreement["activation_date"])
            domain_used_unit=int(client_agreement["domain_used_unit"])
            legal_entity_admin_contactno = le_admin_contactno
            legal_entity_admin_email = le_admin_email
            business_group_name=client_agreement["business_group_name"]
            total_licence = int(client_agreement["total_licence"])
            used_licence = int(client_agreement["used_licence"])
            file_space = int(client_agreement["file_space_limit"])
            used_file_space = int(client_agreement["used_file_space"])

            if not is_header:
                csv_headers = [
                    "S.No", "Country" ,"Group Name", "Business Group",
                    "Legal Entity", "License Allotted", "License Used",
                    "File Space Alloted in GB", "File Space Used in GB", "Domain", "Group Admin Email",
                    "Legal Entity Admin Email", "Legal Entity Admin Contact No",
                    "Date of Agmt Inception", "Contract From", "Contract To",
                    "Total Unit", "Used Unit"
                ]
                for header_list in header_lists:
                    csv_headers.append(header_list)

                self.write_csv(csv_headers, None)
                is_header = True
            csv_values = [
                sno, country_name, group_name, business_group_name, legal_entity_name, 
                total_licence, used_licence, file_space, used_file_space, domain_name, group_admin_email,
                legal_entity_admin_email, legal_entity_admin_contactno, activation_date, contract_from,
                contract_to, domain_total_unit, domain_used_unit
            ]

            for header_list in header_lists:
                if domain_used_unit > 0:
                    count = ''
                    for org in organization_map[client_agreement["legal_entity_id"]]:
                        if header_list == org['organization_name']:
                            count = org['count']
                    csv_values.append(count)
                else:
                    csv_values.append('')

            self.write_csv(None, csv_values)

    def generate_ip_setting_report(
        self, db, request, session_user
    ):
        is_header = False

        client_id = request.client_id
        ip = request.ip

        ip_setting_details_list = db.call_proc(
            "sp_ip_setting_details_report_export", (client_id, ip)
        )

        for ip_setting_details in ip_setting_details_list:

            form_name = ip_setting_details["form_name"]
            ips=ip_setting_details["ips"]
            group_name=ip_setting_details["group_name"]

            if not is_header:
                csv_headers = [
                    "Group Name", "Form Name", "IP Details"
                ]
                self.write_csv(csv_headers, None)
                is_header = True
            csv_values = [
                group_name, form_name, ips
            ]
            self.write_csv(None, csv_values)

    def generate_group_admin_email_report(
        self, db, request, session_user
    ):
        cl_id = request.client_id
        c_id = request.country_id
        if c_id == 0:
            c_id = '%'

        result = db.call_proc_with_multiresult_set("sp_group_admin_registration_email_export_report_data", (session_user, cl_id, c_id), 2)
        is_header = False
        if not is_header:
            csv_headers = [
                "SNO", "Group Name", "Registration Email Date", "Country", "Legal Entity",
                "No. of Units", "Unit Email Date", "Statutory Email Date"
            ]
            self.write_csv(csv_headers, None)
            is_header = True
        j = 1

        for row in result[1]:
            print "a"
            print row.get("client_name")
            client_name = row.get("client_name")
            csv_values = [
                j, client_name, row.get("registration_email_date"), row.get("country_name"),
                row.get("legal_entity_name"), row.get("unit_count"), row.get("unit_email_date"),
                row.get("statutory_email_date")
            ]
            self.write_csv(None, csv_values)

    def generate_statutory_setting_report(
        self, db, request_data, session_user
    ):
        country_id = request_data.country_id
        group_id = request_data.group_id
        business_group_id = request_data.business_group_id
        if business_group_id == 0:
            business_group_id = '%'
        legal_entity_id = request_data.legal_entity_id
        unit_id = request_data.unit_id
        if unit_id == 0:
            unit_id = '%'
        domain_id = request_data.domain_id_optional
        if domain_id is None:
            domain_id = '%'
        statutory_id = request_data.statutory_id
        if statutory_id == 0:
            statutory_id = '%'
        compliance_id = request_data.compliance_id
        if compliance_id == 0:
            compliance_id = '%'
        param_list = [
            country_id, domain_id, business_group_id, legal_entity_id,
            unit_id, group_id, statutory_id, compliance_id
        ]
        print param_list
        result = db.call_proc("sp_export_statutory_setting_report_recordset", param_list)
        is_header = False
        if not is_header:
            csv_headers = [
                "SNO", "Group Name", "Legal Entity", "Country", "Domain", "Unit Name",
                "Statutory Name", "Statutory Provision", "Compliance Task",
                "Document Name", "Remarks", "Statutory Applicability", "Statutory Opted",
                "Compfie Admin", "Admin Update", "Client Admin", "Client Update",
                "Statutory Nature"
            ]
            self.write_csv(csv_headers, None)
            is_header = True
        j = 1
        for row in result:
            stat_map = json.loads(row.get("s_m_name"))
            print stat_map[0]
            if stat_map[0].find(">>") >= 0:
                k = 0
                for i in stat_map[0].split(">>"):
                    if k == 0:
                        stat_map = i + "-"
                        k = k + 1
                    else:
                        stat_map = stat_map + i + " >> "
                        k = k + 1
                    print stat_map
                stat_map = str(stat_map)[0:-3]
                s_map_name = stat_map.split("-")[0]
                s_provision = stat_map.split("-")[1]+" - "+row.get("statutory_provision")
            else:
                s_map_name = str(stat_map)[3:-2]
                s_provision = row.get("statutory_provision")

            stat_app_status = "No"
            if row.get("statutory_applicability_status") == 1:
                stat_app_status = "Yes"
            stat_opt_status = "No"
            if row.get("statutory_opted_status") == 1:
                stat_opt_status = "Yes"
            csv_values = [
                j, row.get("group_name"), row.get("legal_entity_name"), row.get("country_name"),
                row.get("domain_name"), row.get("unit_name"), s_map_name, s_provision,
                row.get("c_task"), row.get("document_name"), row.get("remarks"),
                stat_app_status, stat_opt_status, row.get("compfie_admin"), row.get("admin_update"),
                row.get("client_admin"), row.get("client_update"), row.get("statutory_nature_name")
            ]
            j = j + 1
            self.write_csv(None, csv_values)