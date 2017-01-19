import os
import io
import csv
import uuid
import shutil
import zipfile
import datetime
from server.constants import CSV_DOWNLOAD_URL
from server.common import (
    string_to_datetime, datetime_to_string
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
                elif report_type == "ClientDetails":
                    self.generate_client_details_report(
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
        from_count = 0
        page_count = 10000

        if contract_from is not None:
            contract_from = string_to_datetime(contract_from).date()
        if contract_to is not None:
            contract_to = string_to_datetime(contract_to).date()

        client_agreement_list = db.call_proc(
            "sp_client_agreement_details", (country_id, client_id, business_group_id,
        legal_entity_id, domain_id, contract_from, contract_to, from_count, page_count, session_user)
        )

        for client_agreement in client_agreement_list:
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

            if not is_header:
                csv_headers = [
                    "Group Name", "Business Group Name",
                    "Legal Entity Name", "Group Admin Email",
                    "Legal Entity Admin Email", "Legal Entity Admin Contact No",
                    "Used Licence", "Total Licence",
                    "Used File Space", "Total File Space",
                    "Contract From", "Contract To",
                    "Total Domin", "Domain Name", "Total Unit", "Used Unit", "Activation Date"
                ]
                self.write_csv(csv_headers, None)
                is_header = True
            csv_values = [
                group_name, business_group_name, legal_entity_name, group_admin_email,
                legal_entity_admin_email, legal_entity_admin_contactno, used_licence,
                total_licence, used_file_space, file_space, contract_from, contract_to,
                domain_count, d_name, domain_total_unit, domain_used_unit, activation_date
            ]

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
        from_count = 0
        page_count = 10000

        if contract_from is not None:
            contract_from = string_to_datetime(contract_from).date()
        if contract_to is not None:
            contract_to = string_to_datetime(contract_to).date()


        client_agreement_list = db.call_proc(
            "sp_domainwise_agreement_details", (country_id, client_id, business_group_id,
        legal_entity_id, domain_id, contract_from, contract_to, from_count, page_count, session_user)
        )

        for client_agreement in client_agreement_list:
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

            if not is_header:
                csv_headers = [
                    "Group Name", "Business Group Name",
                    "Legal Entity Name", "Group Admin Email",
                    "Legal Entity Admin Email", "Legal Entity Admin Contact No",
                    "Contract From", "Contract To",
                    "Total Unit", "Used Unit", "Activation Date"
                ]
                self.write_csv(csv_headers, None)
                is_header = True
            csv_values = [
                group_name, business_group_name, legal_entity_name, group_admin_email,
                legal_entity_admin_email, legal_entity_admin_contactno, contract_from,
                contract_to, domain_total_unit, domain_used_unit, activation_date
            ]
            self.write_csv(None, csv_values)
