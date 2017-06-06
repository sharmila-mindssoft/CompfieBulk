import os
import io
import json
import csv
import uuid
import shutil
import zipfile
import datetime
from clientprotocol import (clientcore)
from server.common import (
    string_to_datetime, datetime_to_string,
    convert_to_dict, datetime_to_string_time, datetime_to_moth_year, get_current_date
)
from server.clientdatabase.common import (
    get_country_domain_timelines
)
from server.clientdatabase.general import (calculate_ageing)
from server.clientdatabase.tables import *
from server.clientdatabase.clientreport import *
from server.clientdatabase.dashboard import (
    get_assigneewise_compliances_drilldown_data_count,
    fetch_assigneewise_compliances_drilldown_data,
    fetch_assigneewise_reassigned_compliances

)
from server.clientdatabase.general import (
    get_user_unit_ids, get_date_time_in_date,
    get_user_domains, get_from_and_to_date_for_domain
)


ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CSV_PATH = os.path.join(ROOT_PATH, "exported_reports")
FILE_DOWNLOAD_BASE_PATH = "/download/csv"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"
CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"
CLIENT_LOGO_PATH = os.path.join(ROOT_PATH, "clientlogo")

class ConvertJsonToCSV(object):
    def __init__(self, db, request, session_user, report_type, session_category=None):
        s = str(uuid.uuid4())
        self.session_category = session_category
        file_name = "%s.csv" % s.replace("-", "")
        self.FILE_DOWNLOAD_PATH = "%s/%s" % (
            FILE_DOWNLOAD_BASE_PATH, file_name)
        self.FILE_PATH = "%s/%s" % (CSV_PATH, file_name)
        self.documents_list = []
        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)
        if report_type == "AssigneeWise":
            print report_type
            print self.session_category
            self.generate_assignee_wise_report_and_zip(
                    db, request, session_user
                )
        else:
            with io.FileIO(self.FILE_PATH, "wb+") as f:
                self.writer = csv.writer(f)
                if report_type == "ClientDetails":
                    self.generate_client_details_report(db, request, session_user)
                elif report_type == "Reassign":
                    self.generate_reassign_history_report(db, request, session_user)
                elif report_type == "LegalEntityWiseReport":
                    self.generate_legal_entity_wise_report(db, request, session_user, report_type)
                elif report_type == "DomainWiseReport":
                    self.generate_legal_entity_wise_report(db, request, session_user, report_type)
                elif report_type == "UnitWiseReport":
                    self.generate_unit_wise_report(db, request, session_user)
                elif report_type == "ServiceProviderWiseReport":
                    self.generate_service_provider_wise_compliance_report(db, request, session_user)
                elif report_type == "UserWiseReport":
                    self.generate_user_wise_compliance_report(db, request, session_user)
                elif report_type == "UnitListReport":
                    self.generate_unit_list_report(db, request, session_user)
                elif report_type == "StatutoryNotificationListReport":
                    self.generate_stat_notf_list_report(db, request, session_user)
                elif report_type == "AuditTrailReport":
                    self.generate_audit_trail_report(db, request, session_user)
                elif report_type == "LoginTraceReport":
                    self.generate_login_trace_report(db, request, session_user)
                elif report_type == "RiskReport":
                    self.generate_risk_report(db, request, session_user)
                elif report_type == "StatusReportConsolidated":
                    self.generate_status_report_consolidated(db, request, session_user)
                elif report_type == "StatutorySettingsUnitWise":
                    self.generate_statutory_settings_unit_wise(db, request, session_user)

    def generate_assignee_wise_report_and_zip(
        self, db, request, session_user
    ):
        s = str(uuid.uuid4())
        docs_path = "%s/%s" % (CSV_PATH, s)
        print docs_path
        self.temp_path = "%s/%s" % (CSV_PATH, s)
        self.create_a_csv("Assigneewise compliance count")
        print self.documents_list
        print "==============================="
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

    def generate_client_details_report(
        self, db, request, session_user
    ):
        is_header = False
        country_id = request.country_id
        business_group_id = request.business_group_id
        legal_entity_id = request.legal_entity_id
        division_id = request.division_id
        unit_id = request.unit_id
        domain_ids = request.domain_ids

        condition, condition_val = get_client_details_condition(
            db, country_id,  business_group_id, legal_entity_id, division_id,
            unit_id, domain_ids, session_user
        )
        total_count = get_client_details_count(
            db, country_id,  business_group_id, legal_entity_id, division_id,
            unit_id, domain_ids, session_user
        )
        query = "SELECT unit_id, unit_code, unit_name, geography, " + \
            " address, domain_ids, postal_code, " + \
            " business_group_name, " + \
            " legal_entity_name, division_name " + \
            " FROM tbl_units u " + \
            " LEFT JOIN tbl_business_groups b ON ( " + \
            " b.business_group_id = u.business_group_id) " + \
            " INNER JOIN tbl_legal_entities l ON ( " + \
            " l.legal_entity_id = u.legal_entity_id) " + \
            " LEFT JOIN tbl_divisions d " + \
            " ON (d.division_id = u.division_id) " + \
            " WHERE %s " + \
            " ORDER BY u.business_group_id, " + \
            " u.legal_entity_id, u.division_id, " + \
            " u.unit_id DESC LIMIT %s, %s "

        query = query % (condition, 0, total_count)
        print query
        rows = db.select_all(query, condition_val)
        columns_list = [
            "unit_id", "unit_code", "unit_name", "geography",
            "address", "domain_ids", "postal_code",
            "business_group_name", "legal_entity_name", "division_name"
        ]
        unit_rows = convert_to_dict(rows, columns_list)

        if not is_header:
            csv_headers = [
                "Business Group", "Legal Entity",
                "Division", "Unit Code", "Unit Name", "Geography",
                "Address", "Domains", "Postal Code"
            ]
            self.write_csv(csv_headers, None)
            is_header = True
        for result_row in unit_rows:
            domain_names = db.get_data(
                tblDomains,
                ["group_concat(domain_name) as domains"],
                "domain_id in (%s)" % result_row["domain_ids"]
            )[0]["domains"]
            csv_values = [
                result_row["business_group_name"],
                result_row["legal_entity_name"],
                result_row["division_name"],
                result_row["unit_code"],
                result_row["unit_name"],
                result_row["geography"],
                result_row["address"], domain_names,
                result_row["postal_code"]
            ]
            self.write_csv(None, csv_values)

    def generate_reassign_history_report(
        self, db, request, session_user
    ):
        is_header = False
        country_id = request.country_id
        domain_id = request.domain_id
        level_1_statutory_name = request.level_1_statutory_id
        unit_id = request.unit_id
        compliance_id = request.compliance_id
        user_id = request.user_id
        from_date = request.from_date
        to_date = request.to_date
        qry_where, qry_val = get_where_query_for_reassigned_history_report(
            db, country_id, domain_id, level_1_statutory_name,
            unit_id, compliance_id, user_id, from_date, to_date, session_user
        )
        to_count = get_reassigned_history_report_count(
            db, country_id, domain_id, qry_where, qry_val
        )
        rows = get_reassigned_history_report_data(
            db, country_id, domain_id, qry_where, qry_val,
            0, to_count
        )

        if not is_header:
            csv_headers = [
                "Unit Code", "Unit Name", "Address", "Level 1 statutory",
                "Compliance Name", "Due date", "Assignee", "Reassigned to",
                "Reassigned date", "Remarks"
            ]
            self.write_csv(csv_headers, None)
            is_header = True
        for history in rows:
            # columns = [
            #     "compliance_id", "assignee",
            #     "reassigned_from", "reassigned_date",
            #     "remarks", "due_date", "compliance_task",
            #     "document_name", "unit_code", "unit_name", "address",
            #     "assigneename", "oldassignee", "unit_id", "statutory_mapping"
            # ]
            mappings = history["statutory_mapping"].split('>>')
            statutory_name = mappings[0].strip()
            statutory_name = statutory_name.strip()
            if history["document_name"] is not None:
                compliance_name = " %s - %s" % (
                    history["document_name"], history["compliance_task"]
                )
            else:
                compliance_name = history["compliance_task"]
            csv_values = [
                history["unit_code"], history["unit_name"], history["address"],
                statutory_name, compliance_name, history["due_date"],
                history["reassigned_from"], history["assigneename"],
                datetime_to_string(history["reassigned_date"]),
                history["remarks"]
            ]
            self.write_csv(None, csv_values)

    def generate_statutory_notification_report(
        self, db, request_data, session_user
    ):
        country_name = request_data.country_name
        domain_name = request_data.domain_name
        business_group_id = request_data.business_group_id
        legal_entity_id = request_data.legal_entity_id
        division_id = request_data.division_id
        unit_id = request_data.unit_id
        level_1_statutory_name = request_data.level_1_statutory_name
        from_date = request_data.from_date
        to_date = request_data.to_date
        is_header = False
        if from_date is None:
            from_date = ''
        else:
            from_date = string_to_datetime(from_date)
        if to_date is None:
            to_date = ''
        else:
            to_date = string_to_datetime(to_date)
        condition = "1"
        condition_val = []
        if business_group_id is not None:
            condition += " AND business_group_id = %s "
            condition_val.append(business_group_id)

        if legal_entity_id is not None:
            condition += " AND legal_entity_id = %s "
            condition_val.append(legal_entity_id)

        if division_id is not None:
            condition += " AND division_id = %s "
            condition_val.append(division_id)

        if unit_id is not None:
            condition += " AND unit_id = %s "
            condition_val.append(unit_id)

        # Gettings distinct sets of bg_id, le_id, div_id, unit_id
        columns = [
            "business_group_id", "legal_entity_id", "division_id",
            "unit_id"
        ]
        condition += " group by business_group_id, " + \
            " legal_entity_id, division_id, unit_id"
        rows = db.get_data(tblStatutoryNotificationsUnits, columns, condition)
        conditiondate = None
        for row in rows:
            business_group_id = row["business_group_id"]
            legal_entity_id = row["legal_entity_id"]
            division_id = row["division_id"]
            unit_id = row["unit_id"]
            query = "SELECT bg.business_group_name, le.legal_entity_name, " + \
                " d.division_name, u.unit_code, u.unit_name, u.address, " + \
                " snl.statutory_provision, snl.notification_text, " + \
                " snl.updated_on from " + \
                " tbl_statutory_notifications_log snl " + \
                " INNER JOIN " + \
                " tbl_statutory_notifications_units snu  ON " + \
                " snl.statutory_notification_id = " + \
                " snu.statutory_notification_id " + \
                " INNER JOIN " + \
                " tbl_business_groups bg ON " + \
                " snu.business_group_id = bg.business_group_id " + \
                " INNER JOIN " + \
                " tbl_legal_entities le ON " + \
                " snu.legal_entity_id = le.legal_entity_id " + \
                " INNER JOIN " + \
                " tbl_divisions d ON " + \
                " snu.division_id = d.division_id " + \
                " INNER JOIN " + \
                " tbl_units u ON " + \
                " snu.unit_id = u.unit_id " + \
                " where " + \
                " snl.country_name = %s " + \
                " and " + \
                " snl.domain_name = %s " + \
                " and " + \
                " bg.business_group_id = %s " + \
                " and " + \
                " le.legal_entity_id = %s " + \
                " and " + \
                " d.division_id = %s " + \
                " and " + \
                " u.unit_id = %s " % (
                    country_name, domain_name, business_group_id,
                    legal_entity_id, division_id, unit_id
                )
            if from_date != '' and to_date != '':
                conditiondate = " AND  snl.updated_on between %s and %s " % (
                    from_date, to_date)
                query = query + conditiondate
            if level_1_statutory_name is not None:
                conditionlevel1 = "AND statutory_provision like %s " % (
                    str(level_1_statutory_name + "%"))
                query = query + conditionlevel1
            result_rows = db.select_all(query)
            columns = [
                "business_group_name", "legal_entity_name", "division_name",
                "unit_code", "unit_name", "address",
                "statutory_provision", "notification_text", "updated_on"
            ]
            statutory_notifications = convert_to_dict(result_rows, columns)
            level_1_statutory_wise_notifications = {}
            if len(result_rows) > 0:
                business_group_name = result_rows[0][0]
                legal_entity_name = result_rows[0][1]
                division_name = result_rows[0][2]
                for notification in statutory_notifications:
                    unit_name = "%s - %s" % (
                        notification["unit_code"], notification["unit_name"])
                    statutories = notification[
                        "statutory_provision"].split(">>")
                    level_1_statutory_name = statutories[0]
                    if(
                        level_1_statutory_name not in
                        level_1_statutory_wise_notifications
                    ):
                        level_1_statutory_wise_notifications[
                            level_1_statutory_name] = []

                    if not is_header:
                        csv_headers = [
                            "Business group name", "Legal Entity Name",
                            "Division Name", "Unit Name",
                            "Level 1 statutory mame", "Statutory provision",
                            "Notification Text", "Date and Time"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True
                    csv_values = [
                        business_group_name, legal_entity_name,
                        division_name, unit_name,
                        level_1_statutory_name,
                        notification["statutory_provision"],
                        notification["notification_text"],
                        datetime_to_string(notification["updated_on"])
                    ]
                    self.write_csv(None, csv_values)

    def generate_service_provider_wise_report(
        self, db, request, session_user
    ):
        is_header = False
        country_id = request.country_id
        domain_id = request.domain_id
        statutory_id = request.statutory_id
        unit_id = request.unit_id
        service_provider_id = request.service_provider_id

        if service_provider_id is None:
            service_provider_id = '%'

        query = "SELECT service_provider_id, service_provider_name, " + \
            " address, contract_from, contract_to, " + \
            " contact_person, contact_no  " + \
            " FROM tbl_service_providers " + \
            " WHERE service_provider_id like %s and is_active = 1"
        rows = db.select_all(query, [service_provider_id])

        for row in rows:
            service_provider_name = row[1]
            address = row[2]
            contract_from = datetime_to_string(row[3])
            contract_to = datetime_to_string(row[4])
            contact_person = row[5]
            contact_no = row[6]

            user_ids = get_service_provider_user_ids(db, row[0])
            if unit_id is None:
                unit_ids = get_service_provider_user_unit_ids(
                    db, user_ids)
            else:
                unit_ids = unit_id

            q = "SELECT unit_id, unit_code, unit_name, address " + \
                " FROM tbl_units " + \
                " WHERE country_id = %s and unit_id in (%s)"

            unit_rows = db.select_all(q, [country_id, unit_ids])

            for unit in unit_rows:
                unit_id = unit[0]
                unit_name = "%s - %s " % (unit[1], unit[2])
                unit_address = unit[3]

                query = "SELECT c.compliance_task, " + \
                    " c.compliance_description, " + \
                    " ac.statutory_dates, ac.validity_date, ac.due_date, " + \
                    " ac.assignee, cf.frequency, c.frequency_id, " + \
                    " c.duration, c.repeats_every, " + \
                    " (select duration_type " + \
                    " from tbl_compliance_duration_type " + \
                    " where duration_type_id = c.duration_type_id) " + \
                    " AS duration_type, " + \
                    " (select repeat_type from tbl_compliance_repeat_type " + \
                    " where repeat_type_id = c.repeats_type_id) " + \
                    " AS repeat_type " + \
                    " FROM tbl_client_statutories cs, " + \
                    " tbl_client_compliances cc, tbl_compliances c, " + \
                    " tbl_assign_compliances ac, " + \
                    " tbl_compliance_frequency cf " + \
                    " where  cs.country_id = %s and cs.domain_id = %s " + \
                    " and cs.unit_id = %s and cc.statutory_opted = 1 " + \
                    " and ac.is_active = 1 " + \
                    " and cs.client_statutory_id = cc.client_statutory_id " + \
                    " and c.compliance_id = cc.compliance_id " + \
                    " and c.compliance_id = ac.compliance_id " + \
                    " and ac.unit_id = cs.unit_id " + \
                    " and cf.frequency_id = c.frequency_id " + \
                    " and ac.assignee in (%s) and " + \
                    " c.statutory_mapping like '%s'"
                query = query % (
                        country_id, domain_id,
                        unit_id, user_ids, str(statutory_id+"%")
                    )
                compliance_rows = db.select_all(query)

                for compliance in compliance_rows:
                    statutory_dates = compliance[2]
                    statutory_dates = json.loads(statutory_dates)
                    date_list = []
                    for date in statutory_dates:
                        s_date = clientcore.StatutoryDate(
                            date["statutory_date"],
                            date["statutory_month"],
                            date["trigger_before_days"],
                            date.get("repeat_by")
                        )
                        date_list.append(s_date)

                    compliance_name = compliance[0]
                    description = compliance[1]
                    statutory_date = date_list
                    compliance_frequency = clientcore.COMPLIANCE_FREQUENCY(
                        compliance[6])

                    due_date = None
                    if(compliance[4] is not None):
                        due_date = datetime_to_string(compliance[4])

                    validity_date = None
                    if(compliance[3] is not None):
                        validity_date = datetime_to_string(compliance[3])

                    if compliance[7] in (2, 3):
                        summary = "Repeats every %s - %s" % (
                            compliance[9], compliance[11])
                        for statutory_date in statutory_dates:
                            summary += " (%s %s)" % (
                                statutory_date["statutory_date"],
                                db.string_months[
                                    statutory_date["statutory_month"]
                                ]
                            )
                    elif compliance[7] == 4:
                        summary = "To complete within %s - %s" % (
                            compliance[8], compliance[10])
                    else:
                        summary = None

                    if not is_header:
                        csv_headers = [
                            "Service provider name", "Address",
                            "Contract From", "Contract To",
                            "Contact Person", "Contact No",
                            "Compliance name", "Unit Name", "Unit Address",
                            "Frequency", "Description", "Statutory Date",
                            "Due date", "Validity Date"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True
                    frequence_json = compliance_frequency.to_structure()
                    csv_values = [
                        service_provider_name, address, contract_from,
                        contract_to, contact_person,
                        contact_no, compliance_name, unit_name, unit_address,
                        frequence_json, description, summary,
                        due_date, validity_date
                    ]
                    self.write_csv(None, csv_values)

    def generate_assignee_wise_report_data(
        self, db, request, session_user
    ):
        is_header = False
        country_id = request.country_id
        business_group_id = request.business_group_id
        legal_entity_ids = request.legal_entity_ids
        division_id = request.division_id
        unit_id = request.unit_id
        assignee_id = request.user_id
        condition = "tu.country_id =  %s"
        condition_val = [country_id]
        if business_group_id is not None:
            condition += " AND tu.business_group_id = %s"
            condition_val.append(business_group_id)
        if legal_entity_ids is not None:
            condition += " AND find_in_set(tu.legal_entity_id, %s)"
            condition_val.append(",".join([str(x) for x in legal_entity_ids]))
        if division_id is not None:
            condition += " AND tu.division_id = %s"
            condition_val.append(division_id)
        if unit_id is not None:
            condition += " AND tu.unit_id = %s"
            condition_val.append(unit_id)
        else:
            units = get_user_unit_ids(db, session_user, self.session_category)
            condition += " AND find_in_set(tu.unit_id, %s)"
            condition_val.append(",".join([str(x) for x in units]))

        if assignee_id is not None:
            condition += " AND tch.completed_by = %s"
            condition_val.append(assignee_id)
        domain_ids_list = get_user_domains(db, session_user, self.session_category)
        current_date = get_date_time_in_date()
        print domain_ids_list
        for domain_id in domain_ids_list:
            timelines = get_country_domain_timelines(
                db, [country_id], [domain_id], [current_date.year]
            )
            if len(timelines[0][1]) == 0 :
                continue
            from_date = timelines[0][1][0][1][0]["start_date"].date()
            to_date = timelines[0][1][0][1][0]["end_date"].date()
            query = " SELECT " + \
                " concat(IFNULL(employee_code, " + \
                " 'Administrator'), '-', employee_name) " + \
                " as assignee, tch.completed_by, tch.unit_id, " + \
                " concat(unit_code, '-', unit_name) as unit_name, " + \
                " address, tc.domain_id, " + \
                " (SELECT domain_name FROM tbl_domains td " + \
                " WHERE tc.domain_id = td.domain_id) as domain_name, " + \
                "  sum(IF(ifnull(tc.duration_type_id,0) = 2,IF(tch.due_date >= tch.completion_date and ifnull(tch.approve_status,0) = 1,1,0), " + \
                " IF(date(tch.due_date) >= date(tch.completion_date) and ifnull(tch.approve_status,0) = 1,1,0))) as complied_count, " + \
                " sum(IF(ifnull(tc.duration_type_id,0) = 2,IF(tch.due_date < tch.completion_date and ifnull(tch.approve_status,0) = 1,1,0),  " + \
                " IF(date(tch.due_date) < date(tch.completion_date) and ifnull(tch.approve_status,0) = 1,1,0))) as delayed_count,  " + \
                "  sum(IF(IF(ifnull(tc.duration_type_id,0) = 2, tch.due_date >= now(), date(tch.due_date) >= curdate()) and tch.current_status < 3, 1, 0)) " + \
                " as inprogress_count,  " + \
                "  sum(IF(ifnull(tc.duration_type_id,0) = 2,IF(tch.due_date < now() and ifnull(tch.approve_status,0) <> 1 and ifnull(tch.approve_status,0) <> 3 ,1,0),  " + \
                "  IF(date(tch.due_date) < curdate() and ifnull(tch.approve_status,0) <> 1 and ifnull(tch.approve_status,0) <> 3 ,1,0))) as overdue_count, " + \
                " sum(iF(tch.current_status = 3 and tch.completion_date > tch.due_date and ifnull(tac.is_reassigned, 0) = 1, 1, 0)) as reassigned, " + \
                "  sum(iF(tch.current_status = 3 and ifnull(tch.approve_status, 0) = 3, 1, 0)) as rejected " + \
                " FROM tbl_compliance_history tch " + \
                " INNER JOIN tbl_assign_compliances tac ON ( " + \
                " tch.compliance_id = tac.compliance_id " + \
                " AND tch.unit_id = tac.unit_id) " + \
                " INNER JOIN tbl_units tu ON (tac.unit_id = tu.unit_id) " + \
                " INNER JOIN tbl_users tus ON " + \
                " (tus.user_id = tch.completed_by) " + \
                " INNER JOIN tbl_compliances tc " + \
                " ON (tac.compliance_id = tc.compliance_id) " + \
                " WHERE " + condition + " AND tac.domain_id = %s " + \
                " AND tch.due_date " + \
                " BETWEEN DATE_SUB(%s, INTERVAL 1 DAY) AND " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) " + \
                " group by completed_by, tch.unit_id; "
            param = [domain_id, from_date, to_date]
            parameter_list = condition_val + param
            assignee_wise_compliances = db.select_all(query, parameter_list)
            # columns = [
            #     "assignee", "completed_by", "unit_id", "unit_name",
            #     "address", "domain_id", "domain_name", "complied",
            #     "inprogress", "not_complied", "delayed", "delayed_reassigned",
            # ]
            # assignee_wise_compliances = convert_to_dict(rows, columns)

            with io.FileIO(self.FILE_PATH, "wb+") as f:
                self.writer = csv.writer(f)
                if not is_header:
                    csv_headers = [
                        "Assignee", "Unit Name", "Address", "Domain",
                        "Total", "Complied", "Delayed",
                        "Delayed Reassigned", "Inprogress", "Not Complied",
                        "Rejected"
                    ]
                    self.write_csv(csv_headers, None)
                    is_header = True

                print assignee_wise_compliances
                for compliance in assignee_wise_compliances:
                    unit_name = compliance["unit_name"]
                    assignee = compliance["assignee"]
                    domain_name = compliance["domain_name"]
                    address = compliance["address"]
                    total_compliances = (
                        compliance["complied_count"] + (int(compliance["delayed_count"]) - int(compliance["reassigned"])) +
                        compliance["inprogress_count"] + compliance["overdue_count"] +
                        compliance["rejected"] + compliance["reassigned"]
                    )

                    complied_count = int(compliance["complied_count"])

                    delayed_reassigned_count = int(
                        compliance["reassigned"])
                    inprogress_count = int(compliance["inprogress_count"])
                    not_complied_count = int(compliance["overdue_count"])
                    rejected = int(compliance["rejected"])
                    delay = int(compliance["delayed_count"]) - int(compliance["reassigned"])
                    if delay < 0 :
                        delay = 0

                    csv_values = [
                        assignee, unit_name, address, domain_name,
                        str(total_compliances),
                        str(complied_count), str(delay),
                        str(delayed_reassigned_count),
                        str(inprogress_count), str(not_complied_count),
                        str(rejected)
                    ]
                    self.write_csv(None, csv_values)
            drill_down_path = "%s/%s" % (
                    self.temp_path, "Drilldown Data"
                )
            seven_years_path = "%s/%s" % (
                    self.temp_path, "Assigneewise 7 yearwise Count"
                )
            reassigned = "%s/%s" % (
                    self.temp_path, "Reassigned Compliance Details"
                )
            for compliance in assignee_wise_compliances:
                self.temp_path = drill_down_path
                file_name = "%s-%s-%s" % (
                    compliance["unit_name"], compliance["assignee"],
                    compliance["domain_name"]
                )
                self.create_a_csv(file_name)
                with io.FileIO(self.FILE_PATH, "wb+") as f:
                    self.writer = csv.writer(f)
                    self.generate_assignee_wise_report_drill_down(
                        db, country_id, compliance["completed_by"],
                        compliance["domain_id"], compliance["unit_id"],
                        session_user, compliance["domain_name"]
                    )
            for compliance in assignee_wise_compliances:
                self.temp_path = seven_years_path
                file_name = "%s-%s-%s" % (
                    compliance["unit_name"], compliance["assignee"],
                    compliance["domain_name"]
                )
                self.create_a_csv(file_name)
                with io.FileIO(self.FILE_PATH, "wb+") as f:
                    self.writer = csv.writer(f)
                    self.get_assigneewise_yearwise_compliances(
                        db, country_id, compliance["unit_id"],
                        compliance["completed_by"], domain_id
                    )
            for compliance in assignee_wise_compliances:
                self.temp_path = reassigned
                file_name = "%s-%s-%s" % (
                    compliance["unit_name"], compliance["assignee"],
                    compliance["domain_name"]
                )
                self.create_a_csv(file_name)
                print self.FILE_PATH
                with io.FileIO(self.FILE_PATH, "wb+") as f:
                    self.writer = csv.writer(f)
                    self.get_reassigned_details(
                        db, country_id, compliance["unit_id"],
                        compliance["completed_by"], compliance["domain_id"]
                    )

    def generate_assignee_wise_report_drill_down(
        self, db, country_id, assignee_id, domain_id, unit_id,
        session_user, domain_name, year=None
    ):
        is_header = False
        count = get_assigneewise_compliances_drilldown_data_count(
            db, country_id=country_id, assignee_id=assignee_id,
            domain_ids=[domain_id], year=year,
            unit_id=unit_id, session_user=session_user,
            session_category=self.session_category
        )
        result = fetch_assigneewise_compliances_drilldown_data(
            db, country_id=country_id, assignee_id=assignee_id,
            domain_ids=[domain_id],
            year=year, unit_id=unit_id, start_count=0, to_count=count,
            session_user=session_user, session_category=self.session_category
        )
        complied_compliances = {}
        inprogress_compliances = {}
        delayed_compliances = {}
        not_complied_compliances = {}

        if not is_header:
            csv_headers = [
                "Assignee", "Domain", "Status", "Leve 1 Statutory",
                "Compliance", "Start Date", "Actual Due date",
                "Date of Completion", "Year"
            ]
            self.write_csv(csv_headers, None)
            is_header = True

        for compliance in result:
            compliance_name = compliance["compliance_task"]
            compliance_status = compliance["compliance_status"]
            if compliance["document_name"] is not None:
                compliance_name = "%s - %s" % (
                    compliance["document_name"], compliance_name
                )
            level_1_statutory = compliance["statutory_mapping"].split(">>")[0]
            current_list = not_complied_compliances
            if compliance_status == "Complied":
                current_list = complied_compliances
            elif compliance_status == "Delayed":
                current_list = delayed_compliances
            elif compliance_status == "Inprogress":
                current_list = inprogress_compliances
            if level_1_statutory not in current_list:
                current_list[level_1_statutory] = []

            csv_values = [
                compliance["assignee"], domain_name, compliance_status,
                level_1_statutory, compliance_name, "Nil" if(
                    compliance["start_date"] is None
                ) else datetime_to_string(compliance["start_date"]),
                datetime_to_string(compliance["due_date"]),
                "Nil" if(
                    compliance["completion_date"] is None
                ) else datetime_to_string(compliance["completion_date"]),
                year
            ]
            self.write_csv(None, csv_values)

    def get_reassigned_details(
        self, db, country_id, unit_id, user_id, domain_id
    ):
        is_header = False
        results = fetch_assigneewise_reassigned_compliances(
            db, country_id, unit_id, user_id, domain_id
        )

        for compliance in results:
            if not is_header:
                csv_headers = [
                    "Compliance", "Reassigned From", "Start Date", "Due Date",
                    "Reassigned Date", "Completed Date"
                ]
                self.write_csv(csv_headers, None)
                is_header = True

            compliance_name = compliance["compliance_task"]
            if compliance["document_name"] is not None:
                compliance_name = "%s - %s" % (
                    compliance["document_name"], compliance_name
                )
            csv_values = [
                compliance_name, compliance["reassigned_from"],
                compliance["start_date"], compliance["due_date"],
                compliance["reassigned_date"], compliance["completion_date"]
            ]
            self.write_csv(None, csv_values)

    def get_assigneewise_yearwise_compliances(
        self, db, country_id, unit_id, user_id, domain_id
    ):
        is_header = False
        current_year = get_date_time_in_date().year
        # domain_ids_list = get_user_domains(db, user_id)
        start_year = current_year - 5
        iter_year = start_year
        if not is_header:
            csv_headers = [
                "Year", "Total", "Complied", "Delayed",
                "In progress", "Not complied"
            ]
            self.write_csv(csv_headers, None)
            is_header = True
        while iter_year <= current_year:
            domainwise_complied = 0
            domainwise_inprogress = 0
            domainwise_notcomplied = 0
            domainwise_total = 0
            domainwise_delayed = 0
            for domain_id in [domain_id]:
                result = get_country_domain_timelines(
                    db, [country_id], [domain_id], [iter_year]
                )
                if len(result[0][1]) == 0 :
                    continue
                from_date = result[0][1][0][1][0]["start_date"].date()
                to_date = result[0][1][0][1][0]["end_date"].date()
                query = " SELECT tc.domain_id, " + \
                    " sum(IF(IF(ifnull(tc.duration_type_id, 0) = 2, tch.due_date >= tch.completion_date, date(tch.due_date) >= date(tch.completion_date)) " + \
                    " and ifnull(tch.approve_status,0) = 1, 1, 0)) as complied, " + \
                    " sum(IF(IF(ifnull(tc.duration_type_id, 0) = 2, tch.due_date < tch.completion_date, date(tch.due_date) < date(tch.completion_date)) and " + \
                    " ifnull(tch.approve_status,0) = 1, 1, 0)) as delayed_comp, " + \
                    " sum(IF(IF(ifnull(tc.duration_type_id, 0) = 2, tch.due_date >= now(), date(tch.due_date) >= curdate()) and ifnull(tch.approve_status, 0) <> 1  " + \
                    " and ifnull(tch.approve_status,0) <> 3, 1, 0)) as inprogress, " + \
                    " sum(IF((IF(ifnull(tc.duration_type_id, 0) = 2, tch.due_date < now(), tch.due_date < curdate())  " + \
                    " and ifnull(tch.approve_status,0) <> 1) or ifnull(tch.approve_status,0) = 3, 1, 0)) as not_complied, " + \
                    " sum(case when (approve_status = 1 and " + \
                    " completion_date > tch.due_date and (is_reassigned = 1)) " + \
                    " then 1 else 0 end) as delayed_reassigned " + \
                    " FROM tbl_compliance_history tch " + \
                    " INNER JOIN tbl_assign_compliances tac ON ( " + \
                    " tch.compliance_id = tac.compliance_id " + \
                    " AND tch.unit_id = tac.unit_id " + \
                    " AND tch.completed_by = %s) " + \
                    " INNER JOIN tbl_units tu ON (tac.unit_id = tu.unit_id) " + \
                    " INNER JOIN tbl_users tus " + \
                    " ON (tus.user_id = tac.assignee) " + \
                    " INNER JOIN tbl_compliances tc " + \
                    " ON (tac.compliance_id = tc.compliance_id) " + \
                    " INNER JOIN tbl_domains td " + \
                    " ON (td.domain_id = tc.domain_id) " + \
                    " WHERE tch.unit_id =%s " + \
                    " AND tc.domain_id = %s "
                date_condition = " AND tch.due_date between '%s' AND '%s';"
                date_condition = date_condition % (from_date, to_date)
                query = query + date_condition
                count_rows = db.select_all(query, [
                    user_id, unit_id, int(domain_id)
                ])
                if count_rows:
                    # convert_columns = [
                    #     "domain_id", "complied", "inprogress", "not_complied",
                    #     "delayed", "delayed_reassigned"
                    # ]
                    # count_rows = convert_to_dict(rows, convert_columns)
                    for row in count_rows:
                        domainwise_complied += 0 if(
                            row["complied"] is None) else int(row["complied"])
                        domainwise_inprogress += 0 if(
                            row["inprogress"] is None) else int(
                            row["inprogress"])
                        domainwise_notcomplied += 0 if(
                            row["not_complied"] is None
                        ) else int(row["not_complied"])
                        domainwise_delayed += 0 if(
                            row["delayed_comp"] is None) else int(row["delayed_comp"])
                        domainwise_delayed += 0 if(
                                row["delayed_reassigned"] is None
                            ) else int(row["delayed_reassigned"])
            domainwise_total += (
                domainwise_complied + domainwise_inprogress)
            domainwise_total += (
                domainwise_notcomplied + domainwise_delayed)
            csv_values = [
                str(iter_year), domainwise_total, domainwise_complied,
                domainwise_delayed, domainwise_inprogress,
                domainwise_notcomplied
            ]
            self.write_csv(None, csv_values)
            iter_year += 1

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
        page_count = 100000

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
        page_count = 100000

        if contract_from is not None:
            contract_from = string_to_datetime(contract_from).date()
        if contract_to is not None:
            contract_to = string_to_datetime(contract_to).date()


        client_agreement_list = db.call_proc(
            "sp_domainwise_agreement_details", (country_id, client_id, business_group_id,
        legal_entity_id, domain_id, contract_from, contract_to, from_count, page_count)
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

    def generate_legal_entity_wise_report(
        self, db, request, session_user, rpt_type
    ):
        where_clause = None
        condition_val = []
        select_qry = None
        from_clause = None
        u_type_val = 0
        country_id = request.country_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.domain_id

        stat_map = request.statutory_mapping

        user_type = request.user_type
        if user_type == 'All':
            user_type = '%'
        if user_type == "Assignee":
            u_type_val = 1
        elif user_type == "Concurrence":
            u_type_val = 2
        elif user_type == "Approval":
            u_type_val = 3
        user_id = request.user_id
        if user_id == 0:
            user_id = None
        else:
            user_id = str(user_id)

        due_from = request.due_from_date
        due_to = request.due_to_date
        task_status = request.task_status
        if task_status == '':
            task_status = "All"
        unit_id = request.unit_id
        if unit_id == 0:
            unit_id = None

        compliance_task = request.compliance_task
        if compliance_task is None:
            compliance_task = None

        frequency_id = request.frequency_id

        if due_from is not None and due_to is not None:
            due_from = string_to_datetime(due_from).date()
            due_to = string_to_datetime(due_to).date()

        query = "select (select country_name from tbl_countries where country_id = com.country_id) as country_name, " + \
                "(select domain_name from tbl_domains where domain_id = com.domain_id) as domain_name, " + \
                "(select legal_entity_name from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as legal_entity_name, " + \
                "%s as fromdate, %s as todate, " + \
                "unt.unit_code, concat(unt.unit_name,' - ',SUBSTRING_INDEX(unt.geography_name,'>>',-1),' - ',unt.address) unitname, " + \
                "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
                "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
                "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
                "(select employee_name from tbl_users where user_id = ac.assigned_by) as assigned_by, " + \
                "ac.assigned_on as assigned_date, (select user_category_name from " + \
                "tbl_user_category where user_category_id = (select user_category_id from tbl_users where user_id = " + \
                "ch.completed_by)) as assigned_to, " + \
                "IF(acl.activity_by = ch.completed_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.assignee))as assignee, " + \
                "ch.completed_on, " + \
                "IF(acl.activity_by = ch.concurred_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.concurrence_person)) as concur, " + \
                "ch.concurred_on, " + \
                "IF(acl.activity_by = ch.approved_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.approval_person)) as approver , " + \
                "ch.approved_on, " + \
                "ch.start_date,ch.due_date, ch.due_date as activity_month, " + \
                "ch.validity_date, " + \
                "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                "ELSE 'In Progress' END) as compliance_task_status, " + \
                "(CASE WHEN (ch.due_date >= ch.completion_date and ch.current_status = 3) THEN 'On Time' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN concat('Delayed by ',abs(TIMESTAMPDIFF(day,ch.completion_date,ch.due_date)),' Days') " + \
                "WHEN (ch.due_date >= current_timestamp() and ch.current_status < 3) THEN concat('',abs(TIMESTAMPDIFF(day,ch.due_date,current_timestamp())),' Days Left') " + \
                "WHEN (ch.due_date < current_timestamp() and ch.current_status < 3) THEN concat('Overdue by ',abs(TIMESTAMPDIFF(day,current_timestamp(),ch.due_date)),' Days') " + \
                "ELSE 0 END) as duration " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                "inner join tbl_assign_compliances as ac on acl.compliance_id = ac.compliance_id and acl.unit_id = ac.unit_id " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "where com.country_id = %s and ch.legal_entity_id = %s " + \
                "and com.domain_id = %s " + \
                "and IF(%s IS NOT NULL, acl.unit_id = %s,1) " + \
                "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
                "and IF(%s IS NOT NULL, com.compliance_task like concat('%',%s,'%'),1) " + \
                "and IF(%s > 0, com.frequency_id = %s,1) " + \
                "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
                "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
                "ELSE 1 END) " + \
                "and IF(%s IS NOT NULL, (ch.completed_by = %s OR ch.concurred_by = %s OR ch.approved_by = %s),1) " + \
                "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
                "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                "ELSE 'In Progress' END) = %s,1) " + \
                "order by ch.compliance_history_id asc,acl.compliance_activity_id desc; "

        result = db.select_all(query, [
                due_from, due_to, country_id, legal_entity_id, domain_id,
                unit_id, unit_id, stat_map, stat_map, compliance_task, compliance_task, frequency_id, frequency_id,
                u_type_val, user_id, user_id, user_id, user_id, due_from, due_to, task_status, task_status
            ])
        is_header = False
        j = 1
        if int(len(result)) > 0:
            for row in result:
                if not is_header:
                    if rpt_type == "LegalEntityWiseReport":
                        text = "Legal Entity Wise Report - (" + row["country_name"] + "-" + row["domain_name"] + "-" + row["legal_entity_name"] + ")"
                    else:
                        text = "Domain Wise Report - (" + row["country_name"] + "-" + row["domain_name"] + "-" + row["legal_entity_name"] + ")"
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", "as on " + datetime_to_string(get_current_date()), "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "SNO", "Unit Code", "Unit Name", "Act / Rules", "Compliance Task", "Frequency", "Assigned By",
                        "Assigned To", "Assigned Date", "Assignee", "DOC", "Concurrer", "DOC", "Approver",
                        "DOC", "Start Date", "Due Date", "Month", "Validity Date", "Statutory Status",
                        "Duration"
                    ]

                    self.write_csv(csv_headers, None)
                    is_header = True

                if row["due_date"] is not None:
                    month_names = datetime_to_string(row["due_date"]).split("-")[1]+" "+datetime_to_string(row["due_date"]).split("-")[2]
                else:
                    month_names = None

                csv_values = [
                    j, row["unit_code"], row["unitname"], row["act_name"], row["compliance_name"], row["frequency_name"],
                    row["assigned_by"], row["assigned_to"], row["assigned_date"], row["assignee"],
                    datetime_to_string(row["completed_on"]), row["concur"], datetime_to_string(row["concurred_on"]),
                    row["approver"], datetime_to_string(row["approved_on"]), datetime_to_string(row["start_date"]),
                    datetime_to_string(row["due_date"]), month_names, datetime_to_string(row["validity_date"]),
                    row["compliance_task_status"], row["duration"]
                ]
                j = j + 1
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_unit_wise_report(
        self, db, request, session_user
    ):
        where_clause = None
        condition_val = []
        select_qry = None
        from_clause = None
        u_type_val = 0
        country_id = request.country_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id_optional
        if domain_id == 0:
            domain_id = None

        stat_map = request.statutory_mapping

        user_type = request.user_type
        if user_type == 'All':
            user_type = '%'
        if user_type == "Assignee":
            u_type_val = 1
        elif user_type == "Concurrence":
            u_type_val = 2
        elif user_type == "Approval":
            u_type_val = 3
        user_id = request.user_id
        if user_id == 0:
            user_id = None
        else:
            user_id = str(user_id)

        due_from = request.due_from_date
        due_to = request.due_to_date
        task_status = request.task_status
        unit_id = request.unit_id
        if unit_id == 0:
            unit_id = None

        compliance_task = request.compliance_task
        if compliance_task is None:
            compliance_task = None

        frequency_id = request.frequency_id

        if due_from is not None and due_to is not None:
            due_from = string_to_datetime(due_from).date()
            due_to = string_to_datetime(due_to).date()

        query = "select (select country_name from tbl_countries where country_id = com.country_id) as country_name, " + \
                "(select domain_name from tbl_domains where domain_id = com.domain_id) as domain_name, " + \
                "(select legal_entity_name from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as legal_entity_name, " + \
                "%s as fromdate, %s as todate, " + \
                "unt.unit_code, concat(unt.unit_name,' - ',SUBSTRING_INDEX(unt.geography_name,'>>',-1),' - ',unt.address) unit_name, " + \
                "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
                "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
                "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
                "(select employee_name from tbl_users where user_id = ac.assigned_by) as assigned_by, " + \
                "ac.assigned_on as assigned_date, (select user_category_name from " + \
                "tbl_user_category where user_category_id = (select user_category_id from tbl_users where user_id = " + \
                "ch.completed_by)) as assigned_to, " + \
                "IF(acl.activity_by = ch.completed_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.assignee))as assignee, " + \
                "ch.completed_on, " + \
                "IF(acl.activity_by = ch.concurred_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.concurrence_person)) as concur, " + \
                "ch.concurred_on, " + \
                "IF(acl.activity_by = ch.approved_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.approval_person)) as approver , " + \
                "ch.approved_on, " + \
                "ch.start_date,ch.due_date, ch.due_date as activity_month, " + \
                "ch.validity_date, " + \
                "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                "ELSE 'In Progress' END) as compliance_task_status, " + \
                "(CASE WHEN (ch.due_date >= ch.completion_date and ch.current_status = 3) THEN 'On Time' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN concat('Delayed by ',abs(TIMESTAMPDIFF(day,ch.completion_date,ch.due_date)),' Days') " + \
                "WHEN (ch.due_date >= current_timestamp() and ch.current_status < 3) THEN concat('',abs(TIMESTAMPDIFF(day,ch.due_date,current_timestamp())),' Days Left') " + \
                "WHEN (ch.due_date < current_timestamp() and ch.current_status < 3) THEN concat('Overdue by ',abs(TIMESTAMPDIFF(day,current_timestamp(),ch.due_date)),' Days') " + \
                "ELSE 0 END) as duration " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                "inner join tbl_assign_compliances as ac on acl.compliance_id = ac.compliance_id and acl.unit_id = ac.unit_id " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "where com.country_id = %s and ch.legal_entity_id = %s and ch.unit_id = %s " + \
                "and IF(%s IS NOT NULL, com.domain_id = %s,1) " + \
                "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
                "and IF(%s IS NOT NULL, com.compliance_task like concat('%',%s,'%'),1) " + \
                "and IF(%s > 0, com.frequency_id = %s,1) " + \
                "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
                "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
                "ELSE 1 END) " + \
                "and IF(%s IS NOT NULL, (ch.completed_by = %s OR ch.concurred_by = %s OR ch.approved_by = %s),1) " + \
                "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
                "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                "ELSE 'In Progress' END) = %s,1) " + \
                "order by ch.compliance_history_id asc,acl.compliance_activity_id desc; "

        result = db.select_all(query, [
                due_from, due_to, country_id, legal_entity_id, unit_id, domain_id, domain_id,
                stat_map, stat_map, compliance_task, compliance_task, frequency_id, frequency_id,
                u_type_val, user_id, user_id, user_id, user_id, due_from, due_to, task_status, task_status
            ])
        is_header = False

        j = 1
        if len(result) > 0:
            for row in result:
                if not is_header:
                    text = "Unit Wise Report - (" + row["country_name"] + "-" + row["legal_entity_name"] + "-" + row["unit_name"] + ")"
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", "as on " + datetime_to_string(get_current_date()), "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "SNO", "Domain Name", "Act / Rules", "Compliance Task", "Frequency", "Assigned By",
                        "Assigned To", "Assigned Date", "Assignee", "DOC", "Concurrer", "DOC", "Approver",
                        "DOC", "Start Date", "Due Date", "Month", "Validity Date", "Statutory Status",
                        "Duration"
                    ]
                    self.write_csv(csv_headers, None)
                    is_header = True

                if row["due_date"] is not None:
                    month_names = datetime_to_string(row["due_date"]).split("-")[1]+" "+datetime_to_string(row["due_date"]).split("-")[2]
                else:
                    month_names = None
                csv_values = [
                    j, row["domain_name"], row["act_name"], row["compliance_name"], row["frequency_name"],
                    row["assigned_by"], row["assigned_to"], row["assigned_date"], row["assignee"],
                    datetime_to_string(row["completed_on"]), row["concur"], datetime_to_string(row["concurred_on"]),
                    row["approver"], datetime_to_string(row["approved_on"]), datetime_to_string(row["start_date"]),
                    datetime_to_string(row["due_date"]), month_names, datetime_to_string(row["validity_date"]),
                    row["compliance_task_status"], row["duration"]
                ]
                j = j + 1
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_service_provider_wise_compliance_report(
        self, db, request, session_user
    ):
        where_clause = None
        condition_val = []
        select_qry = None
        from_clause = None
        country_id = request.country_id
        legal_entity_id = request.legal_entity_id
        sp_id = request.sp_id
        domain_id = request.domain_id
        stat_map = request.statutory_mapping
        due_from = request.due_from_date
        due_to = request.due_to_date
        task_status = request.task_status
        if task_status == "All":
            task_status = '%'
        user_id = request.user_id
        if user_id == 0:
            user_id = None
        else:
            user_id = str(user_id)
        select_qry = "select (select legal_entity_name from tbl_legal_entities where legal_entity_id = " + \
            "t1.legal_entity_id) as legal_entity_name, (select unit_code from tbl_units where unit_id = " + \
            "t1.unit_id) as unit_code, t3.statutory_mapping, t3.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as frequency_name, " + \
            "(select employee_name from tbl_users where user_id in (select assigned_by from tbl_assign_compliances " + \
            "where compliance_id = t1.compliance_id and unit_id = t1.unit_id)) as assigned_by, (select assigned_on from tbl_assign_" + \
            "compliances where compliance_id = t1.compliance_id limit 1) as assigned_date, (select user_category_name from " + \
            "tbl_user_category where user_category_id = (select user_category_id from tbl_users where user_id = " + \
            "t1.completed_by)) as assigned_to, (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users " + \
            "where user_id = t1.completed_by) as assignee, t1.completed_on, t1.concurred_on, (select " + \
            "IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = t1.concurred_by) as " + \
            "concurred_by, (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = t1.approved_by) as approver, " + \
            "t1.approved_on, t1.start_date, t1.due_date, t1.validity_date, t1.approve_status, " + \
            "(select duration_type from tbl_compliance_duration_type where duration_type_id = t3.duration_type_id) " + \
            "as duration_type, t1.current_status, (select country_name from tbl_countries where country_id =  " + \
            "t3.country_id) as country_name, (select domain_name from tbl_domains where domain_id = " + \
            "t3.domain_id) as domain_name, (select service_provider_name from tbl_service_providers where " + \
            "service_provider_id = t4.service_provider_id) as service_provider_name,t1.completion_date, t1.approved_by, " + \
            "abs(TIMESTAMPDIFF(day,now(),t1.due_date)) as dura_1, abs(TIMESTAMPDIFF(day,t1.due_date,now())) as dura_2, " + \
            "(CASE WHEN (t1.due_date >= t1.completion_date and t1.current_status = 3) THEN 'On Time' " + \
            "WHEN (t1.due_date < t1.completion_date and t1.current_status = 3) THEN concat('Delayed by ',abs(TIMESTAMPDIFF(day,t1.completion_date,t1.due_date)),' Days') " + \
            "WHEN (t1.due_date >= current_timestamp() and t1.current_status < 3) THEN concat('',abs(TIMESTAMPDIFF(day,t1.due_date,current_timestamp())),' Days Left') " + \
            "WHEN (t1.due_date < current_timestamp() and t1.current_status < 3) THEN concat('Overdue by ',abs(TIMESTAMPDIFF(day,current_timestamp(),t1.due_date)),' Days') " + \
            "ELSE 0 END) as duration, " + \
            "(CASE WHEN (t1.due_date < t1.completion_date and t1.current_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (t1.due_date >= t1.completion_date and t1.approve_status <> 3 and t1.current_status = 3) THEN 'Complied' " + \
            "WHEN (t1.due_date >= t1.completion_date and t1.current_status < 3) THEN 'In Progress' " + \
            "WHEN (t1.due_date < t1.completion_date and t1.current_status < 3) THEN 'Not Complied' " + \
            "WHEN (t1.current_status = 3 and t1.approve_status = 3) THEN 'Not Complied' " + \
            "WHEN (t1.completion_date IS NULL and IFNULL(t1.current_status,0) = 0) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) as task_status "
        from_clause = "from tbl_users as t4 inner join tbl_compliance_history as t1 " + \
            "on t1.completed_by = t4.user_id and t4.is_service_provider = 1 " + \
            "inner join tbl_legal_entity_domains as t5 on t5.legal_entity_id = t1.legal_entity_id inner join " + \
            "tbl_compliances as t3 on t3.compliance_id = t1.compliance_id and t3.domain_id = t5.domain_id " + \
            "left join tbl_compliance_activity_log as t2 on t2.compliance_history_id = t1.compliance_history_id " + \
            "inner join tbl_assign_compliances as ac on ac.compliance_id = t1.compliance_id where "
        where_clause = "t3.country_id = %s and t3.domain_id = %s "
        condition_val.extend([country_id, domain_id])
        if request.statutory_mapping is not None:
            stat_map = '%' + stat_map + '%'
            where_clause = where_clause + "and t3.statutory_mapping like %s "
            condition_val.append(stat_map)

        # where_clause = where_clause + "and IF(%s IS NOT NULL, (t1.completed_by = %s),1) "
        # condition_val.extend([user_id, user_id, user_id, user_id])

        if task_status == "Complied":
            where_clause = where_clause + \
                "and t1.due_date >= t1.completion_date and t1.current_status = 3 and t1.approve_status <> 3 "
        elif task_status == "Delayed Compliance":
            where_clause = where_clause + \
                "and t1.due_date < t1.completion_date and t1.current_status = 3 "
        elif task_status == "Inprogress":
            where_clause = where_clause + "and ((t1.completion_date is NULL and IFNULL(t1.current_status,0) = 0) or " + \
                "(t1.due_date >= t1.completion_date and t1.current_status < 3)) "
        elif task_status == "Not Complied":
            where_clause = where_clause + "and ((t1.due_date < t1.completion_date and t1.current_status < 3) or " + \
                "(t1.current_status = 3 and t1.approve_status = 3)) "

        if due_from is not None and due_to is not None:
            due_from = string_to_datetime(due_from).date()
            due_to = string_to_datetime(due_to).date()
            where_clause = where_clause + " and t1.due_date >= " + \
                " date(%s)  and t1.due_date < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.extend([due_from, due_to])
        elif due_from is not None and due_to is None:
            due_from = string_to_datetime(due_from).date()
            where_clause = where_clause + " and t1.due_date >= " + \
                " date(%s)  and t1.due_date < " + \
                " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
            condition_val.append(due_from)
        elif due_from is None and due_to is not None:
            due_to = string_to_datetime(due_to).date()
            where_clause = where_clause + " and t1.due_date < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.append(due_to)

        compliance_task = request.compliance_task
        if compliance_task is not None:
            where_clause = where_clause + "and t3.compliance_task like concat('%',%s, '%') "
            condition_val.append(compliance_task)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        if user_id is not None:
            where_clause = where_clause + "and t4.user_id = %s "
            condition_val.append(user_id)

        where_clause = where_clause + "and t4.service_provider_id = %s and " + \
            "t1.legal_entity_id = %s group by t2.compliance_activity_id " + \
            "order by t1.due_date,t1.compliance_history_id, t2.compliance_activity_id desc;"
        condition_val.extend([sp_id, legal_entity_id])

        query = select_qry + from_clause + where_clause
        print "qry"
        print query
        result = db.select_all(query, condition_val)
        print "length"
        print len(result)
        is_header = False

        j = 1
        if len(result) > 0:
            for row in result:
                if not is_header:
                    text = "Service Provider Wise Report - (" + row["country_name"] + "-" + row["domain_name"] + "-" + row["service_provider_name"] + ")"
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "", "", "as on " + datetime_to_string(get_current_date()), "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "SNO", "Legal Entity", "Unit Code", "Act / Rules", "Compliance Task", "Frequency", "Assigned By",
                        "Assigned To", "Assigned Date", "Assignee", "DOC", "Concurrer", "DOC", "Approver",
                        "DOC", "Start Date", "Due Date", "Month", "Validity Date", "Statutory Status",
                        "Duration"
                    ]
                    self.write_csv(csv_headers, None)
                    is_header = True

                task_status = None
                statutory_mapping = json.loads(row["statutory_mapping"])
                if statutory_mapping[0].find(">>") >= 0:
                    statutory_mapping = statutory_mapping[0].split(">>")[0]
                else:
                    statutory_mapping = str(statutory_mapping)[3:-2]

                if row["due_date"] is not None:
                    month_names = datetime_to_string(row["due_date"]).split("-")[1]+" "+datetime_to_string(row["due_date"]).split("-")[2]
                else:
                    month_names = None
                csv_values = [
                    j, row["legal_entity_name"], row["unit_code"], statutory_mapping, row["compliance_task"], row["frequency_name"],
                    row["assigned_by"], row["assigned_to"], row["assigned_date"], row["assignee"],
                    datetime_to_string(row["completed_on"]), row["concurred_by"], datetime_to_string(row["concurred_on"]),
                    row["approver"], datetime_to_string(row["approved_on"]), datetime_to_string(row["start_date"]),
                    datetime_to_string(row["due_date"]), month_names, datetime_to_string(row["validity_date"]),
                    row["task_status"], row["duration"]
                ]
                j = j + 1
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_user_wise_compliance_report(
        self, db, request, session_user
    ):
        where_clause = None
        count_clause = None
        condition_val = []
        select_qry = None
        from_clause = None
        u_type_val = 0
        country_id = request.country_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.domain_id
        if domain_id == 0:
            domain_id = None
        stat_map = request.statutory_mapping

        user_type = request.user_type
        if user_type == 'All':
            user_type = '%'
        if user_type == "Assignee":
            u_type_val = 1
        elif user_type == "Concurrence":
            u_type_val = 2
        elif user_type == "Approval":
            u_type_val = 3
        user_id = request.user_id
        if user_id == 0:
            user_id = None
        else:
            user_id = str(user_id)

        due_from = request.due_from_date
        due_to = request.due_to_date
        task_status = request.task_status
        unit_id = request.unit_id
        if unit_id == 0:
            unit_id = None

        compliance_task = request.compliance_task
        if compliance_task is None:
            compliance_task = None

        frequency_id = request.frequency_id

        if due_from is not None and due_to is not None:
            due_from = string_to_datetime(due_from).date()
            due_to = string_to_datetime(due_to).date()
        query = "select count(0) as user_cnt " + \
            "from tbl_assign_compliances as t1 " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s and " + \
            "(CASE %s WHEN 1 THEN t1.assignee = %s WHEN 2 THEN t1.concurrence_person = %s " + \
            "WHEN 3 THEN t1.approval_person = %s ELSE 1 END) "

        result = db.select_one(query, [legal_entity_id, country_id, u_type_val, user_id, user_id, user_id])
        print "user result"
        print result

        if result["user_cnt"] > 0 :
            query = "select (select country_name from tbl_countries where country_id = com.country_id) as country_name, " + \
                    "(select domain_name from tbl_domains where domain_id = com.domain_id) as domain_name, " + \
                    "(select legal_entity_name from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as legal_entity_name, " + \
                    "%s as fromdate, %s as todate, " + \
                    "unt.unit_code, concat(unt.unit_name,' - ',SUBSTRING_INDEX(unt.geography_name,'>>',-1),' - ',unt.address) unitname, " + \
                    "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
                    "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
                    "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
                    "(select employee_name from tbl_users where user_id = ac.assigned_by) as assigned_by, " + \
                    "ac.assigned_on as assigned_date, (select user_category_name from " + \
                    "tbl_user_category where user_category_id = (select user_category_id from tbl_users where user_id = " + \
                    "ch.completed_by)) as assigned_to, " + \
                    "IF(acl.activity_by = ch.completed_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                    "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.assignee))as assignee, " + \
                    "ch.completed_on, " + \
                    "IF(acl.activity_by = ch.concurred_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                    "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.concurrence_person)) as concur, " + \
                    "ch.concurred_on, " + \
                    "IF(acl.activity_by = ch.approved_by,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = acl.activity_by), " + \
                    "(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.approval_person)) as approver , " + \
                    "ch.approved_on, " + \
                    "ch.start_date,ch.due_date, ch.due_date as activity_month, " + \
                    "ch.validity_date, " + \
                    "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                    "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                    "WHEN (ch.due_date >= ch.completion_date and ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                    "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                    "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                    "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
                    "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                    "ELSE 'In Progress' END) as compliance_task_status, " + \
                    "(CASE WHEN (ch.due_date >= ch.completion_date and ch.current_status = 3) THEN 'On Time' " + \
                    "WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN concat('Delayed by ',abs(TIMESTAMPDIFF(day,ch.completion_date,ch.due_date)),' Days') " + \
                    "WHEN (ch.due_date >= current_timestamp() and ch.current_status < 3) THEN concat('',abs(TIMESTAMPDIFF(day,ch.due_date,current_timestamp())),' Days Left') " + \
                    "WHEN (ch.due_date < current_timestamp() and ch.current_status < 3) THEN concat('Overdue by ',abs(TIMESTAMPDIFF(day,current_timestamp(),ch.due_date)),' Days') " + \
                    "ELSE 0 END) as duration " + \
                    "from tbl_users as t4 inner join tbl_compliance_history as ch on (ch.completed_by = t4.user_id or " + \
                    "ch.approved_by = t4.user_id or ch.concurred_by = t4.user_id) " + \
                    "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                    "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                    "inner join tbl_assign_compliances as ac on acl.compliance_id = ac.compliance_id and acl.unit_id = ac.unit_id " + \
                    "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                    "where t4.user_id = %s and com.country_id = %s and ch.legal_entity_id = %s " + \
                    "and IF(%s IS NOT NULL, com.domain_id = %s,1) " + \
                    "and IF(%s IS NOT NULL, acl.unit_id = %s,1) " + \
                    "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
                    "and IF(%s IS NOT NULL, com.compliance_task like concat('%',%s,'%'),1) " + \
                    "and IF(%s > 0, com.frequency_id = %s,1) " + \
                    "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
                    "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
                    "ELSE 1 END) " + \
                    "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
                    "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                    "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                    "WHEN (ch.due_date >= ch.completion_date and ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                    "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                    "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                    "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
                    "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                    "ELSE 'In Progress' END) = %s,1) " + \
                    "order by ch.compliance_history_id asc,acl.compliance_activity_id desc; "

            result = db.select_all(query, [
                    due_from, due_to, user_id, country_id, legal_entity_id, domain_id, domain_id,
                    unit_id, unit_id, stat_map, stat_map, compliance_task, compliance_task, frequency_id, frequency_id,
                    u_type_val, due_from, due_to, task_status, task_status
                ])

            is_header = False
            j = 1
            if len(result) > 0:
                for row in result:
                    if not is_header:
                        text = "User Wise Report - (" + row["country_name"] + ")"
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", "as on " + datetime_to_string(get_current_date()), "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "SNO", "Legal Entity", "Unit Code", "Domain", "Act / Rules", "Compliance Task", "Frequency", "Assigned By",
                            "Assigned To", "Assigned Date", "Assignee", "DOC", "Concurrer", "DOC", "Approver",
                            "DOC", "Start Date", "Due Date", "Month", "Validity Date", "Statutory Status",
                            "Duration"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True

                    if row["due_date"] is not None:
                        month_names = datetime_to_string(row["due_date"]).split("-")[1]+" "+datetime_to_string(row["due_date"]).split("-")[2]
                    else:
                        month_names = None

                    csv_values = [
                        j, row["legal_entity_name"], row["unit_code"], row["domain_name"], row["act_name"], row["compliance_name"], row["frequency_name"],
                        row["assigned_by"], row["assigned_to"], row["assigned_date"], row["assignee"],
                        datetime_to_string(row["completed_on"]), row["concur"], datetime_to_string(row["concurred_on"]),
                        row["approver"], datetime_to_string(row["approved_on"]), datetime_to_string(row["start_date"]),
                        datetime_to_string(row["due_date"]), month_names, datetime_to_string(row["validity_date"]),
                        row["compliance_task_status"], row["duration"]
                    ]
                    j = j + 1
                    self.write_csv(None, csv_values)
            else:
                if os.path.exists(self.FILE_PATH):
                    os.remove(self.FILE_PATH)
                    self.FILE_DOWNLOAD_PATH = None
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_unit_list_report(
        self, db, request, session_user
    ):
        where_clause = None
        condition_val = []
        select_qry = None
        country_id = request.country_id
        business_group_id = request.business_group_id
        legal_entity_id = request.legal_entity_id
        division_id = request.division_id
        category_id = request.category_id
        unit_id = request.unit_id
        domain_id = request.domain_id
        organisation_id = request.organisation_id

        unit_status = request.unit_status

        select_qry = "select t1.unit_id, (select business_group_name from tbl_business_groups where business_group_id = " + \
            "t1.business_group_id) as business_group_name, (select legal_entity_name from tbl_legal_entities " + \
            "where legal_entity_id = t1.legal_entity_id) as legal_entity_name, t1.unit_code, t1.unit_name, " + \
            "t1.address, t1.postal_code, (select country_name " + \
            "from tbl_countries where country_id = t1.country_id) as country_name, " + \
            "t1.geography_name, t1.is_closed, t1.closed_on, t1.division_id, t1.category_id, (select  " + \
            "division_name from tbl_divisions where division_id = t1.division_id) as division_name, " + \
            "(select category_name from tbl_categories where category_id = t1.category_id) as " + \
            "category_name, (select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "DATEDIFF(now(),t1.closed_on) as closed_days from tbl_units as t1 where "
        where_clause = "t1.legal_entity_id = %s and t1.country_id = %s "
        condition_val.extend([legal_entity_id, country_id])

        if business_group_id is not None and int(business_group_id) > 0:
            where_clause = where_clause + "and t1.business_group_id = %s "
            condition_val.append(business_group_id)

        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        if int(division_id) > 0:
            where_clause = where_clause + "and t1.division_id = %s "
            condition_val.append(division_id)

        if int(category_id) > 0:
            where_clause = where_clause + "and t1.category_id = %s "
            condition_val.append(category_id)

        if unit_status == "Active":
            where_clause = where_clause + "and t1.is_closed = %s "
            condition_val.append(0)
        elif unit_status == "Closed":
            where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) > 30 "
            condition_val.append(1)
        elif unit_status == "Inactive":
            where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) <= 30 "
            condition_val.append(1)

        where_clause = where_clause + "order by t1.closed_on desc"
        # condition_val.extend([int(request.from_count), int(request.page_count)])
        query = select_qry + where_clause
        print "qry"
        print query
        result = db.select_all(query, condition_val)

        # domains & organisations
        select_qry = None
        where_clause = None
        condition_val = []
        select_qry = "select t1.unit_id, t2.domain_id, t2.organisation_id, (select domain_name " + \
            "from tbl_domains where domain_id = t2.domain_id) as domain_name, (select " + \
            "organisation_name from tbl_organisation where organisation_id = t2.organisation_id) as " + \
            "organisation_name, DATEDIFF(now(),t1.closed_on) as closed_days from tbl_units as t1 inner join tbl_units_organizations as t2 on " + \
            "t2.unit_id = t1.unit_id inner join tbl_legal_entity_domains as t3 on t3.legal_entity_id = " + \
            "t1.legal_entity_id and t3.domain_id = t2.domain_id where "
        where_clause = "t1.legal_entity_id = %s and t1.country_id = %s "
        condition_val.extend([legal_entity_id, country_id])

        if business_group_id is not None and int(business_group_id) > 0:
            where_clause = where_clause + "and t1.business_group_id = %s "
            condition_val.append(business_group_id)

        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        if int(division_id) > 0:
            where_clause = where_clause + "and t1.division_id = %s "
            condition_val.append(division_id)

        if int(category_id) > 0:
            where_clause = where_clause + "and t1.category_id = %s "
            condition_val.append(category_id)

        if int(domain_id) > 0:
            where_clause = where_clause + "and t2.domain_id = %s "
            condition_val.append(domain_id)

        if int(organisation_id) > 0:
            where_clause = where_clause + "and t2.organisation_id = %s "
            condition_val.append(organisation_id)

        if unit_status == "Active":
            where_clause = where_clause + "and t1.is_closed = %s "
            condition_val.append(0)
        elif unit_status == "Closed":
            where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) > 30 "
            condition_val.append(1)
        elif unit_status == "Inactive":
            where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) <= 30 "
            condition_val.append(1)
        where_clause = where_clause + "order by t1.closed_on desc;"
        # condition_val.extend([int(request.from_count), int(request.page_count)])
        query = select_qry + where_clause
        print "qry"
        print query
        result_1 = db.select_all(query, condition_val)

        is_header = False

        j = 1
        if len(result) > 0:
            for row in result:
                if not is_header:
                    text = "Unit Details - (" + row["country_name"] + ")"
                    csv_headers = [
                        "", "", "", "", text, "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "Aparajitha Group", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "as on " + datetime_to_string(get_current_date()), "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "SNO", "Business Group", "Legal Entity", "Division Name", "Unit Code", "Unit Name", "Domain",
                        "Organization Type", "Address", "Postal Code",  "Status", "Date"
                    ]
                    self.write_csv(csv_headers, None)
                    is_header = True

                unit_id = row["unit_id"]
                unit_code = row["unit_code"]
                unit_name = row["unit_name"]
                geography_name = row["geography_name"]
                address = row["address"]
                postal_code = row["postal_code"]
                division_name = row["division_name"]
                if row["is_closed"] == 0:
                    unit_status = "Active"
                    closed_date = None
                elif int(row["closed_days"]) <= 30:
                    unit_status = "Inactive"
                    closed_date = datetime_to_string(row["closed_on"])
                else:
                    unit_status = "Closed"
                    closed_date = datetime_to_string(row["closed_on"])
                d_names = []
                i_names = []

                # if geography_name.find(">>") >= 0:
                #     val = geography_name.split(">>")
                #     split_len = len(geography_name.split(">>"))
                #     state = val[split_len-1]
                #     city = val[split_len-1]
                # else:
                #     state = None
                #     city = None

                last = object()
                last_1 = object()
                for row_1 in result_1:
                    if unit_id == row_1["unit_id"]:
                        if last != row_1["domain_name"]:
                            last = row_1["domain_name"]
                            d_names.append(row_1["domain_name"])
                        if last_1 != row_1["organisation_name"]:
                            last_1 = row_1["organisation_name"]
                            i_names.append(row_1["organisation_name"])
                csv_values = [
                    j, row["business_group_name"], row["legal_entity_name"], division_name, unit_code, unit_name,
                    (",").join(d_names), (",").join(i_names), address, postal_code, unit_status, closed_date
                ]
                j = j + 1
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_stat_notf_list_report(
        self, db, request, session_user
    ):
        where_clause = None
        condition_val = []
        select_qry = None
        country_id = request.country_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.domain_id
        statutory_mapping = request.statutory_mapping
        due_from = request.due_from_date
        due_to = request.due_to_date

        select_qry = "select t1.compliance_id, t2.statutory_mapping, t2.compliance_description, " + \
            "t2.compliance_task, SUBSTRING_INDEX(t3.notification_text,'remarks',-1) as notification_text, t3.created_on from tbl_client_compliances as t1 " + \
            "inner join tbl_compliances as t2 on t2.compliance_id = t1.compliance_id inner join " + \
            "tbl_statutory_notifications as t3 on t3.compliance_id = t2.compliance_id where "
        where_clause = "t1.legal_entity_id = %s and t1.domain_id = %s and t2.country_id = %s "
        condition_val.extend([legal_entity_id, domain_id, country_id])

        if statutory_mapping is not None:
            statutory_mapping = '%'+statutory_mapping+'%'
            where_clause = where_clause + "and t2.statutory_mapping like %s "
            condition_val.append(statutory_mapping)

        if due_from is not None and due_to is not None:
            due_from = string_to_datetime(due_from).date()
            due_to = string_to_datetime(due_to).date()
            where_clause = where_clause + " and t3.created_on >= " + \
                " date(%s)  and t3.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.extend([due_from, due_to])
        elif due_from is not None and due_to is None:
            due_from = string_to_datetime(due_from).date()
            where_clause = where_clause + " and t3.created_on >= " + \
                " date(%s)  and t3.created_on < " + \
                " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
            condition_val.append(due_from)
        elif due_from is None and due_to is not None:
            due_to = string_to_datetime(due_to).date()
            where_clause = where_clause + " and t3.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.append(due_to)

        where_clause = where_clause + "group by t1.compliance_id order by t3.created_on desc;"
        # condition_val.extend([int(request.from_count), int(request.page_count)])
        query = select_qry + where_clause
        print "qry"
        print query
        result = db.select_all(query, condition_val)
        if len(result) > 0:
            is_header = False
            if not is_header:
                csv_headers = [
                    "", "", "Statutory Notifications List", "", "", ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "", "", "Aparajitha Group", "", "", ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "", "", "as on " + datetime_to_string(get_current_date()), "", "", ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "Compliance ID", "Act", "Compliance Task", "Compliance Description",
                    "Date", "Notification Content"
                ]
                self.write_csv(csv_headers, None)
                is_header = True
            for row in result:
                stat_map = json.loads(row["statutory_mapping"])
                if stat_map[0].find(">>") >= 0:
                    stat_map = stat_map[0].split(">>")[0]
                else:
                    stat_map = str(stat_map)[3:-2]
                csv_values = [
                    row["compliance_id"], stat_map, row["compliance_task"], row["compliance_description"],
                    datetime_to_string(row["created_on"]), row["notification_text"]
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_audit_trail_report(
        self, db, request, session_user
    ):
        where_clause = None
        condition_val = []
        select_qry = None
        legal_entity_id = request.legal_entity_id
        user_id = request.user_id
        form_id = request.form_id_optional
        due_from = request.due_from_date
        due_to = request.due_to_date

        select_qry = "select t1.user_id, t1.form_id, t1.action, t1.created_on, (select  " + \
            "employee_code from tbl_users where user_id " + \
            "= t1.user_id) as emp_code, (select  " + \
            "employee_name from tbl_users where user_id " + \
            "= t1.user_id) as user_name, " + \
            "(select form_name from tbl_forms where form_id = t1.form_id) as form_name " + \
            "from tbl_activity_log as t1 where "
        where_clause = "t1.form_id <> 0 and t1.legal_entity_id = %s "
        condition_val.append(legal_entity_id)

        if int(user_id) > 0:
            where_clause = where_clause + "and t1.user_id = %s "
            condition_val.append(user_id)
        if int(form_id) > 0:
            where_clause = where_clause + "and t1.form_id = %s "
            condition_val.append(form_id)
        if due_from is not None and due_to is not None:
            due_from = string_to_datetime(due_from).date()
            due_to = string_to_datetime(due_to).date()
            where_clause = where_clause + " and t1.created_on >= " + \
                " date(%s)  and t1.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.extend([due_from, due_to])
        elif due_from is not None and due_to is None:
            due_from = string_to_datetime(due_from).date()
            where_clause = where_clause + " and t1.created_on >= " + \
                " date(%s)  and t1.created_on < " + \
                " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
            condition_val.append(due_from)
        elif due_from is None and due_to is not None:
            due_to = string_to_datetime(due_to).date()
            where_clause = where_clause + " and t1.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.append(due_to)

        where_clause = where_clause + "order by t1.created_on desc;"
        # condition_val.extend([int(request.from_count), int(request.page_count)])
        query = select_qry + where_clause
        print "qry"
        print query
        result = db.select_all(query, condition_val)
        if len(result) > 0:
            is_header = False
            if not is_header:
                csv_headers = [
                    "", "Audit Trail Report", ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "", "Aparajitha Group", ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "", "as on " + datetime_to_string(get_current_date()), ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "User Name", "Form Name", "Action", "Created On"
                ]
                self.write_csv(csv_headers, None)
                is_header = True
            for row in result:
                user_name = None
                if row["emp_code"] is not None:
                    user_name = row["emp_code"] + " - " + row["user_name"]
                else:
                    user_name = row["user_name"]
                csv_values = [
                    user_name, row["form_name"], row["action"], datetime_to_string_time(row["created_on"])
                ]
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_login_trace_report(
        self, db, request, session_user
    ):
        where_clause = None
        condition_val = []
        select_qry = None
        user_id = request.user_id
        due_from = request.due_from_date
        due_to = request.due_to_date

        select_qry = "select t1.form_id, t1.action, t1.created_on, (select  " + \
            "concat(employee_code,' - ',employee_name) from tbl_users where user_id " + \
            "= t1.user_id) as user_name from tbl_activity_log as t1 where "
        where_clause = "t1.form_id = 0 "

        if int(user_id) > 0:
            where_clause = where_clause + "and t1.user_id = %s "
            condition_val.append(user_id)
        if due_from is not None and due_to is not None:
            due_from = string_to_datetime(due_from).date()
            due_to = string_to_datetime(due_to).date()
            where_clause = where_clause + " and t1.created_on >= " + \
                " date(%s)  and t1.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.extend([due_from, due_to])
        elif due_from is not None and due_to is None:
            due_from = string_to_datetime(due_from).date()
            where_clause = where_clause + " and t1.created_on >= " + \
                " date(%s)  and t1.created_on < " + \
                " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
            condition_val.append(due_from)
        elif due_from is None and due_to is not None:
            due_to = string_to_datetime(due_to).date()
            where_clause = where_clause + " and t1.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.append(due_to)

        where_clause = where_clause + "order by t1.created_on desc;"
        # condition_val.extend([int(request.from_count), int(request.page_count)])
        query = select_qry + where_clause
        print "qry"
        print query
        result = db.select_all(query, condition_val)
        print "login length"
        print result
        j = 1
        if len(result) > 0:
            is_header = False
            if not is_header:
                csv_headers = [
                    "", "Login Trace Report", ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "", "Aparajitha Group", ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "", "as on " + datetime_to_string(get_current_date()), ""
                ]
                self.write_csv(csv_headers, None)
                csv_headers = [
                    "S.No.", "Action", "Info", "Created On"
                ]
                self.write_csv(csv_headers, None)
                is_header = True
            for row in result:
                if row["action"].find("Login") >= 0:
                    csv_values = [
                        j, "Login",
                        row["action"], datetime_to_string_time(row["created_on"])
                    ]
                    self.write_csv(None, csv_values)
                elif row["action"].find("Logout") >= 0:
                    csv_values = [
                        j, "Logout",
                        row["action"], datetime_to_string_time(row["created_on"])
                    ]
                    self.write_csv(None, csv_values)
                j = j + 1
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_risk_report(
        self, db, request, session_user
    ):
        # u_type = ("Assignee", "Concurrence", "Approval")
        # status = ("Complied", "Delayed Compliance", "Inprogress", "Not Complied")
        where_clause = None
        condition_val = []
        select_qry = None
        union_qry = None
        from_clause = None
        union_from_clause = None
        union_where_clause = None
        country_id = request.country_id
        # business_group_id = request.business_group_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.domain_id
        division_id = request.division_id
        category_id = request.category_id
        unit_id = request.unit_id
        stat_map = request.statutory_mapping
        # compliance_id = request.compliance_id
        u_type_val = 0
        task_status = request.task_status
        if task_status == "Not Opted":
            u_type_val = 1
        elif task_status == "Delayed Compliance":
            u_type_val = 2
        elif task_status == "Not Complied":
            u_type_val = 3
        condition_val = []
        print "other"
        if task_status == "All":
            print task_status
            # All or unassigned compliance
            union_qry = "(select (select legal_entity_name from tbl_legal_entities where legal_entity_id= " + \
                "t1.legal_entity_id) as legal_entity_name, t2.statutory_mapping, (select concat(unit_code,'-',unit_name, " + \
                "',',address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, " + \
                "t2.compliance_task,(select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as " + \
                "frequency_name,null as admin_incharge, null as assignee_name, null as assigned_to, null as assigned_date, " + \
                "t2.penal_consequences, null as completion_date, null as due_date, null as approve_status, " + \
                "null as completion_date, null as due_date, null as current_status, null as compliance_opted_status, null as start_date, " + \
                "null as due_date, null as concurrer_name, null as approver_name, null as remarks, null as documents, " + \
                "null as assigned_on, null as concurred_on, null as approved_on, null as validity_date, null as duration, " + \
                "null as approve_status, (select country_name from tbl_countries where country_id = t2.country_id) as country_name, " + \
                "(select domain_name from tbl_domains where domain_id = t2.domain_id) as domain_name, " + \
                "null as approved_by, null as dura_1, null as dura_2, 'Unassigned Compliance' as compliance_task_status, " + \
                "null as duration, t2.frequency_id, t2.duration_type_id "
            union_from_clause = "from tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
                "on t2.compliance_id = t1.compliance_id inner join tbl_units as t3 on t3.unit_id = t1.unit_id where "
            union_where_clause = "t2.country_id = %s and t2.domain_id = %s "
            condition_val.extend([country_id, domain_id])

            if int(division_id) > 0:
                union_where_clause = union_where_clause + "and t3.division_id = %s "
                condition_val.append(division_id)

            if int(category_id) > 0:
                union_where_clause = union_where_clause + "and t3.category_id = %s "
                condition_val.append(category_id)

            if request.statutory_mapping is not None:
                stat_map = '%'+stat_map+'%'
                union_where_clause = union_where_clause + "and t2.statutory_mapping like %s "
                condition_val.append(stat_map)

            compliance_task = request.compliance_task
            if compliance_task is not None:
                where_clause = where_clause + "and t2.compliance_task like concat('%',%s, '%') "
                condition_val.append(compliance_task)

            unit_id = request.unit_id
            if int(unit_id) > 0:
                union_where_clause = union_where_clause + "and t1.unit_id = %s "
                condition_val.append(unit_id)

            union_where_clause = union_where_clause + "and t1.legal_entity_id = %s and t1.compliance_opted_status = 1 and t1.compliance_id not in " + \
                "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc)"
            condition_val.extend([legal_entity_id])

            # other compliance
            select_qry = "(select (select legal_entity_name from tbl_legal_entities where legal_entity_id= " + \
                "t1.legal_entity_id) as legal_entity_name, t3.statutory_mapping, (select concat(unit_code,'-',unit_name, " + \
                "',',address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, " + \
                "t3.compliance_task,(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as " + \
                "frequency_name,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = " + \
                "t6.assigned_by) as admin_incharge, (select employee_name from tbl_users " + \
                "where user_id = t1.completed_by) as assignee_name, (select user_category_name from tbl_user_category " + \
                "where user_category_id = (select user_category_id from tbl_users where user_id = t1.completed_by)) as " + \
                "assigned_to, t6.assigned_on as assigned_date, t3.penal_consequences, t1.completion_date, t1.due_date, t1.approve_status, " + \
                "t1.completion_date, t1.due_date, t1.current_status, t5.compliance_opted_status, t1.start_date, " + \
                "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
                "t1.concurred_by) as concurrer_name, (select (case when employee_code is not null then " + \
                "concat(employee_code,'-',employee_name) else employee_name end) from tbl_users " + \
                "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
                "assigned_on, t1.concurred_on, t1.approved_on, t6.validity_date, (select duration_type from tbl_" + \
                "compliance_duration_type where duration_type_id = (select duration_type_id from tbl_compliances where " + \
                "compliance_id = t3.compliance_id)) as duration, t1.approve_status, (select country_name from tbl_countries " + \
                "where country_id = t3.country_id) as country_name, (select domain_name from tbl_domains " + \
                "where domain_id = t3.domain_id) as domain_name, t1.approved_by, " + \
                "abs(TIMESTAMPDIFF(day,now(),t1.due_date)) as dura_1, abs(TIMESTAMPDIFF(day,t1.due_date,now())) as dura_2, " + \
                "(CASE WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3) THEN 'Delayed Compliance' " + \
                "WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) then 'Not Complied' " + \
                "when (ifnull(t1.current_status,0) =3 and ifnull(t1.approve_status,0) = 3) THEN 'Not Complied - Rejected' " + \
                "WHEN t5.compliance_opted_status = 0 THEN 'Not Opted' END) as compliance_task_status, " + \
                "(CASE WHEN (t1.due_date >= t1.completion_date and t1.current_status = 3) THEN 'On Time' " + \
                "WHEN (t1.due_date < t1.completion_date and t1.current_status = 3) THEN concat('Delayed by ',abs(TIMESTAMPDIFF(day,t1.completion_date,t1.due_date)),' Days') " + \
                "WHEN (t1.due_date >= current_timestamp() and t1.current_status < 3) THEN concat('',abs(TIMESTAMPDIFF(day,t1.due_date,current_timestamp())),' Days Left') " + \
                "WHEN (t1.due_date < current_timestamp() and t1.current_status < 3) THEN concat('Overdue by ',abs(TIMESTAMPDIFF(day,current_timestamp(),t1.due_date)),' Days') " + \
                "ELSE 0 END) as duration, t3.frequency_id, t3.duration_type_id  "
            from_clause = "from tbl_compliance_history as t1 inner join tbl_compliances as t3 on " + \
                "t3.compliance_id = t1.compliance_id inner join tbl_client_compliances as t5 " + \
                "on t5.compliance_id = t1.compliance_id left join tbl_compliance_activity_log as t2 " + \
                "on t2.compliance_history_id = t1.compliance_history_id inner join tbl_assign_compliances as t6 on t6.compliance_id = " + \
                "t1.compliance_id and t6.unit_id = t1.unit_id inner join tbl_units as t4 on t4.unit_id = t1.unit_id where "
            where_clause = "t3.country_id = %s and t3.domain_id = %s "
            condition_val.extend([country_id, domain_id])

            where_clause = where_clause + "and (CASE %s WHEN 1 THEN (t5.compliance_opted_status = 0) " + \
                "WHEN 2 THEN t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3 " + \
                "WHEN 3 THEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3) " + \
                "else ((t5.compliance_opted_status = 0) or (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3) " + \
                "or (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3)" + \
                ") end)"
            condition_val.append(u_type_val)

            if int(division_id) > 0:
                where_clause = where_clause + "and t4.division_id = %s "
                condition_val.append(division_id)

            if int(category_id) > 0:
                where_clause = where_clause + "and t4.category_id = %s "
                condition_val.append(category_id)

            if request.statutory_mapping is not None:
                stat_map = '%'+stat_map+'%'
                where_clause = where_clause + "and t3.statutory_mapping like %s "
                condition_val.append(stat_map)

            compliance_task = request.compliance_task
            if compliance_task is not None:
                where_clause = where_clause + "and t3compliance_task like concat('%',%s, '%') "
                condition_val.append(compliance_task)

            unit_id = request.unit_id
            if int(unit_id) > 0:
                where_clause = where_clause + "and t1.unit_id = %s "
                condition_val.append(unit_id)

            where_clause = where_clause + "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t3.compliance_task asc)"
            condition_val.extend([legal_entity_id])

            query = union_qry + union_from_clause + union_where_clause + " union " + select_qry + from_clause + where_clause
            result_1 = db.select_all(query, condition_val)

            risk_report = []
            is_header = False

            j = 1
            if len(result_1) > 0:
                for row in result_1:
                    if not is_header:
                        text = "Risk Report - (" + row["country_name"] + "-" + row["domain_name"] + ")"
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", "as on " + datetime_to_string(get_current_date()), "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "SNO", "Legal Entity", "Unit Code", "Unit Name", "Act / Rules", "Compliance Task",
                            "Frequency", "Assigned By", "Assigned To", "Assigned Date", "Assignee", "DOC",
                            "Concurrer", "DOC", "Approver", "DOC", "Start Date", "Due Date", "Validity Date",
                            "Compliance Task Status", "Remarks", "Duration", "Penal Consequences"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True
                    task_status = None
                    duration = ""
                    print row["statutory_mapping"]
                    print json.loads(row["statutory_mapping"])
                    statutory_mapping = json.loads(row["statutory_mapping"])
                    if statutory_mapping[0].find(">>") >= 0:
                        statutory_mapping = statutory_mapping[0].split(">>")[0]
                    else:
                        statutory_mapping = str(statutory_mapping)[3:-2]
                    start_date = datetime_to_string(row["start_date"])
                    due_date = datetime_to_string(row["due_date"])
                    if row["frequency_id"] == 5 and row["duration_type_id"] == 2:
                        start_date = datetime_to_string_time(row["start_date"])
                        due_date = datetime_to_string_time(row["due_date"])
                    csv_values = [
                        j, row["legal_entity_name"], row["unit_name"].split("-")[0], row["unit_name"].split("-")[1],
                        statutory_mapping, row["compliance_task"],
                        row["frequency_name"], row["admin_incharge"], row["assigned_to"], row["assigned_date"], row["assignee_name"],
                        datetime_to_string_time(row["assigned_on"]), row["concurrer_name"],
                        datetime_to_string_time(row["concurred_on"]), row["approver_name"],
                        datetime_to_string_time(row["approved_on"]), start_date, due_date,
                        datetime_to_string_time(row["validity_date"]),
                        row["compliance_task_status"], row["remarks"], row["duration"], row["penal_consequences"]
                    ]
                    j = j + 1
                    self.write_csv(None, csv_values)
            else:
                if os.path.exists(self.FILE_PATH):
                    os.remove(self.FILE_PATH)
                    self.FILE_DOWNLOAD_PATH = None

        elif task_status == "Unassigned Compliance":
            print task_status
            # All or unassigned compliance
            union_qry = "select (select legal_entity_name from tbl_legal_entities where legal_entity_id=t1.legal_entity_id) " + \
                "as legal_entity_name, (select concat(unit_code,'-',unit_name,',',address,',', " + \
                "postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t2.statutory_mapping, " + \
                "t2.compliance_task, (select frequency from tbl_compliance_frequency where frequency_id = " + \
                "t2.frequency_id) as frequency_name, t2.penal_consequences, (select country_name from tbl_countries " + \
                "where country_id = t2.country_id) as country_name, (select domain_name from tbl_domains " + \
                "where domain_id = t2.domain_id) as domain_name "
            union_from_clause = "from tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
                "on t2.compliance_id = t1.compliance_id inner join tbl_units as t3 on t3.unit_id = t1.unit_id where "
            union_where_clause = "t2.country_id = %s and t2.domain_id = %s "
            condition_val.extend([country_id, domain_id])

            if int(division_id) > 0:
                union_where_clause = union_where_clause + "and t3.division_id = %s "
                condition_val.append(division_id)

            if int(category_id) > 0:
                union_where_clause = union_where_clause + "and t3.category_id = %s "
                condition_val.append(category_id)

            if request.statutory_mapping is not None:
                stat_map = '%'+stat_map+'%'
                union_where_clause = union_where_clause + "and t2.statutory_mapping like %s "
                condition_val.append(stat_map)

            compliance_task = request.compliance_task
            if compliance_task is not None:
                where_clause = where_clause + "and t2.compliance_task like concat('%',%s, '%') "
                condition_val.append(compliance_task)

            unit_id = request.unit_id
            if int(unit_id) > 0:
                union_where_clause = union_where_clause + "and t1.unit_id = %s "
                condition_val.append(unit_id)

            union_where_clause = union_where_clause + "and t1.compliance_opted_status =1 and t1.legal_entity_id = %s and t1.compliance_id not in " + \
                "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc;"
            condition_val.extend([legal_entity_id])

            query = union_qry + union_from_clause + union_where_clause
            print "qry1"
            print query
            result_1 = db.select_all(query, condition_val)

            risk_report = []
            is_header = False

            j = 1
            if len(result_1) > 0:
                for row in result_1:
                    if not is_header:
                        text = "Risk Report - (" + row["country_name"] + "-" + row["domain_name"] + ")"
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", "as on " + datetime_to_string(get_current_date()), "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "SNO", "Legal Entity", "Unit Code", "Unit Name", "Act / Rules", "Compliance Task",
                            "Frequency", "Assigned By", "Assigned To", "Assigned Date", "Assignee", "DOC",
                            "Concurrer", "DOC", "Approver", "DOC", "Start Date", "Due Date", "Validity Date",
                            "Compliance Task Status", "Remarks", "Duration", "Penal Consequences"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True

                    task_status = "Unassigned Compliance"
                    statutory_mapping = json.loads(row["statutory_mapping"])
                    if statutory_mapping[0].find(">>") >= 0:
                        statutory_mapping = statutory_mapping[0].split(">>")[0]
                    else:
                        statutory_mapping = str(statutory_mapping)[3:-2]

                    csv_values = [
                        j, row["legal_entity_name"], row["unit_name"].split("-")[0], row["unit_name"].split("-")[1],
                        statutory_mapping, row["compliance_task"],
                        row["frequency_name"], None, None, None, None, None, None, None, None, None, None,
                        None, task_status, None, None, row["penal_consequences"]
                    ]
                    j = j + 1
                    self.write_csv(None, csv_values)
            else:
                if os.path.exists(self.FILE_PATH):
                    os.remove(self.FILE_PATH)
                    self.FILE_DOWNLOAD_PATH = None

            condition_val = []
            print len(risk_report)
        elif (task_status != "All" or task_status != "Unassigned Compliance"):
            print "a"
            condition_val = []
            # other compliance
            select_qry = "select (select legal_entity_name from tbl_legal_entities where legal_entity_id= " + \
                "t1.legal_entity_id) as legal_entity_name, t3.statutory_mapping, (select concat(unit_code,'-',unit_name, " + \
                "',',address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, " + \
                "t3.compliance_task,(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as " + \
                "frequency_name,(select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = " + \
                "t6.assigned_by) as admin_incharge, (select employee_name from tbl_users " + \
                "where user_id = t1.completed_by) as assignee_name, (select user_category_name from tbl_user_category " + \
                "where user_category_id = (select user_category_id from tbl_users where user_id = t1.completed_by)) as " + \
                "assigned_to, t6.assigned_on as assigned_date, t3.penal_consequences, t1.completion_date, t1.due_date, t1.approve_status, " + \
                "t1.completion_date, t1.due_date, t1.current_status, t5.compliance_opted_status, t1.start_date, " + \
                "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
                "t1.concurred_by) as concurrer_name, (select (case when employee_code is not null then " + \
                "concat(employee_code,'-',employee_name) else employee_name end) from tbl_users " + \
                "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
                "assigned_on, t1.concurred_on, t1.approved_on, t6.validity_date, (select duration_type from tbl_" + \
                "compliance_duration_type where duration_type_id = (select duration_type_id from tbl_compliances where " + \
                "compliance_id = t3.compliance_id)) as duration, t1.approve_status, (select country_name from tbl_countries " + \
                "where country_id = t3.country_id) as country_name, (select domain_name from tbl_domains " + \
                "where domain_id = t3.domain_id) as domain_name, t1.approved_by, " + \
                "abs(TIMESTAMPDIFF(day,now(),t1.due_date)) as dura_1, abs(TIMESTAMPDIFF(day,t1.due_date,now())) as dura_2, " + \
                "(CASE WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3) THEN 'Delayed Compliance' " + \
                "WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) then 'Not Complied' " + \
                "when (ifnull(t1.current_status,0) =3 and ifnull(t1.approve_status,0) = 3) THEN 'Not Complied - Rejected' " + \
                "WHEN t5.compliance_opted_status = 0 THEN 'Not Opted' END) as compliance_task_status, " + \
                "(CASE WHEN (t1.due_date >= t1.completion_date and t1.current_status = 3) THEN 'On Time' " + \
                "WHEN (t1.due_date < t1.completion_date and t1.current_status = 3) THEN concat('Delayed by ',abs(TIMESTAMPDIFF(day,t1.completion_date,t1.due_date)),' Days') " + \
                "WHEN (t1.due_date >= current_timestamp() and t1.current_status < 3) THEN concat('',abs(TIMESTAMPDIFF(day,t1.due_date,current_timestamp())),' Days Left') " + \
                "WHEN (t1.due_date < current_timestamp() and t1.current_status < 3) THEN concat('Overdue by ',abs(TIMESTAMPDIFF(day,current_timestamp(),t1.due_date)),' Days') " + \
                "ELSE 0 END) as duration, t3.frequency_id, t3.duration_type_id  "
            from_clause = "from tbl_compliance_history as t1 inner join tbl_compliances as t3 on " + \
                "t3.compliance_id = t1.compliance_id inner join tbl_client_compliances as t5 " + \
                "on t5.compliance_id = t1.compliance_id left join tbl_compliance_activity_log as t2 " + \
                "on t2.compliance_history_id = t1.compliance_history_id inner join tbl_assign_compliances as t6 on t6.compliance_id = " + \
                "t1.compliance_id and t6.unit_id = t1.unit_id inner join tbl_units as t4 on t4.unit_id = t1.unit_id where "
            where_clause = "t3.country_id = %s and t3.domain_id = %s "
            condition_val.extend([country_id, domain_id])

            if int(division_id) > 0:
                where_clause = where_clause + "and t4.division_id = %s "
                condition_val.append(division_id)

            if int(category_id) > 0:
                where_clause = where_clause + "and t4.category_id = %s "
                condition_val.append(category_id)

            if request.statutory_mapping is not None:
                stat_map = '%'+stat_map+'%'
                where_clause = where_clause + "and t3.statutory_mapping like %s "
                condition_val.append(stat_map)

            if task_status == "Not Opted":
                where_clause = where_clause + "and t5.compliance_opted_status = 0 "
            elif task_status == "Delayed Compliance":
                where_clause = where_clause + "and t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3 "
            elif task_status == "Not Complied":
                where_clause = where_clause + "and ((t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3)) "

            compliance_task = request.compliance_task
            if compliance_task is not None:
                where_clause = where_clause + "and t3.compliance_task like concat('%',%s, '%') "
                condition_val.append(compliance_task)

            unit_id = request.unit_id
            if int(unit_id) > 0:
                where_clause = where_clause + "and t1.unit_id = %s "
                condition_val.append(unit_id)

            where_clause = where_clause + "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t3.compliance_task asc;"
            condition_val.extend([legal_entity_id])

            query = select_qry + from_clause + where_clause
            print "qry"
            print query

            result = db.select_all(query, condition_val)
            is_header = False

            j = 1
            if len(result) > 0:
                for row in result:
                    if not is_header:
                        text = "Risk Report - (" + row["country_name"] + "-" + row["domain_name"] + ")"
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "", "", "", "", "", "", "", "", "", "", "as on " + datetime_to_string(get_current_date()), "", "", "", "", "", "", "", "", "", "", ""
                        ]
                        self.write_csv(csv_headers, None)
                        csv_headers = [
                            "SNO", "Legal Entity", "Unit Code", "Unit Name", "Act / Rules", "Compliance Task",
                            "Frequency", "Assigned By", "Assigned To", "Assigned Date", "Assignee", "DOC",
                            "Concurrer", "DOC", "Approver", "DOC", "Start Date", "Due Date", "Validity Date",
                            "Compliance Task Status", "Remarks", "Duration", "Penal Consequences"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True

                    task_status = None
                    statutory_mapping = json.loads(row["statutory_mapping"])
                    if statutory_mapping[0].find(">>") >= 0:
                        statutory_mapping = statutory_mapping[0].split(">>")[0]
                    else:
                        statutory_mapping = str(statutory_mapping)[3:-2]
                    start_date = datetime_to_string(row["start_date"])
                    due_date = datetime_to_string(row["due_date"])
                    if row["frequency_id"] == 5 and row["duration_type_id"] == 2:
                        start_date = datetime_to_string_time(row["start_date"])
                        due_date = datetime_to_string_time(row["due_date"])
                    csv_values = [
                        j, row["legal_entity_name"], row["unit_name"].split("-")[0], row["unit_name"].split("-")[1],
                        statutory_mapping, row["compliance_task"], row["frequency_name"],
                        row["admin_incharge"], row["assigned_to"], row["assigned_date"], row["assignee_name"],
                        datetime_to_string_time(row["assigned_on"]), row["concurrer_name"],
                        datetime_to_string_time(row["concurred_on"]), row["approver_name"],
                        datetime_to_string_time(row["approved_on"]), start_date, due_date,
                        datetime_to_string_time(row["validity_date"]),
                        row["compliance_task_status"], row["remarks"], row["duration"], row["penal_consequences"]
                    ]
                    j = j + 1
                    self.write_csv(None, csv_values)
            else:
                if os.path.exists(self.FILE_PATH):
                    os.remove(self.FILE_PATH)
                    self.FILE_DOWNLOAD_PATH = None

    def generate_status_report_consolidated(
        self, db, request, session_user
    ):
        country_id = request.c_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        unit_id = request.unit_id
        act = request.act
        compliance_id = request.compliance_id
        frequency_id = request.frequency_id
        user_type_id = request.user_type_id
        status_name = request.status_name
        usr_id = request.usr_id
        csv = request.csv
        f_count = request.f_count
        t_count = request.t_count

        from_date = string_to_datetime(request.from_date)
        to_date = string_to_datetime(request.to_date)

        query = "select (select country_name from tbl_countries where country_id = com.country_id) as countryname, " + \
                "(select domain_name from tbl_domains where domain_id = com.domain_id) as domainname, " + \
                "(select legal_entity_name from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as legal_entity_name, " + \
                "%s as fromdate, %s as todate, " + \
                "unt.unit_code, concat(unt.unit_name,' - ',SUBSTRING_INDEX(unt.geography_name,'>>',-1),' - ',unt.address) unitname, " + \
                "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
                "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
                "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
                "(select concat(IFNULL(employee_code,''),' - ',employee_name) from tbl_users where user_id = ac.assigned_by) as assigned_by, " + \
                "ac.assigned_on as assigned_date, " + \
                "IF(acl.activity_by = ch.completed_by,(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = acl.activity_by), " + \
                "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee))as assignee, " + \
                "ch.completed_on, " + \
                "IF(acl.activity_by = ch.concurred_by,(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = acl.activity_by), " + \
                "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.concurrence_person)) as concur, " + \
                "ch.concurred_on, " + \
                "IF(acl.activity_by = ch.approved_by,(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = acl.activity_by), " + \
                "(select concat(IFNULL(employee_code,''),' - ',employee_name) from tbl_users where user_id = ac.approval_person)) as approver , " + \
                "ch.approved_on, " + \
                "ch.start_date,ch.due_date, ch.due_date as activity_month, " + \
                "ch.validity_date, " + \
                "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                "ELSE 'In Progress' END) as compliance_task_status, " + \
                "(CASE WHEN (ch.due_date >= ch.completion_date and ch.current_status = 3) THEN 'On Time' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN concat('Delayed by ',abs(TIMESTAMPDIFF(day,ch.completion_date,ch.due_date)),' Days') " + \
                "WHEN (ch.due_date >= current_timestamp() and ch.current_status < 3) THEN concat('',abs(TIMESTAMPDIFF(day,ch.due_date,current_timestamp())),' Days Left') " + \
                "WHEN (ch.due_date < current_timestamp() and ch.current_status < 3) THEN concat('Overdue by ',abs(TIMESTAMPDIFF(day,current_timestamp(),ch.due_date)),' Days') " + \
                "ELSE 0 END) as duration, com.duration as duration_type " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                "inner join tbl_assign_compliances as ac on acl.compliance_id = ac.compliance_id and acl.unit_id = ac.unit_id " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "where com.country_id = %s and ch.legal_entity_id = %s " + \
                "and com.domain_id = %s " + \
                "and IF(%s IS NOT NULL, acl.unit_id = %s,1) " + \
                "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
                "and IF(%s IS NOT NULL, ch.compliance_id = %s,1) " + \
                "and IF(%s > 0, com.frequency_id = %s,1) " + \
                "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
                "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
                "ELSE 1 END) " + \
                "and IF(%s IS NOT NULL, ((ch.completion_date is not null and ch.completed_by = %s)  OR (ch.concurrence_status is not null and ch.concurred_by = %s) OR (ch.approve_status is not null and ch.approved_by = %s)),1) " + \
                "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
                "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                "ELSE 'In Progress' END) = %s,1) " + \
                "order by ch.compliance_history_id asc,acl.compliance_activity_id desc; "

        rows = db.select_all(query, [ from_date, to_date, country_id, legal_entity_id, domain_id,
                    unit_id, unit_id, act, act, compliance_id, compliance_id, frequency_id, frequency_id,
                    user_type_id, usr_id, usr_id, usr_id, usr_id, from_date, to_date, status_name, status_name])

        is_header = False
        j = 1
        is_header = False
        # datetime_to_string(get_current_date())
        if int(len(rows)) > 0:

            for row in rows:
                if not is_header:
                    text = "Status Report - Consolidated - (" + row["countryname"] + " - " + row["legal_entity_name"] + " - " + row["domainname"] + ")"
                    csv_headers = [
                        "", "", "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "("+ request.from_date +" - "+ request.to_date +")", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "", "","as on " + datetime_to_string_time(get_date_time_in_date()) + " (Report generated date)", "", "", "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    # "S.No", "Unit Code",  "Unit Name", "Act / Rules", "Compliance Task", "Frequency", "Assigned By", "Assigned To", "Assigned Date",
                    # "Assignee", "DOC", "Concurer", "DOC", "Approver", "DOC", "Start Date", "Due Date", "Month", "Validity Date", "Compliance Task Status", "Duration"
                    csv_headers = [
                        "SNO", "Unit Code", "Unit Name", "Act / Rules", "Compliance Task",
                        "Frequency", "Assigned by", "Assigned Date", "Assignee", "Completed on", "Concur",
                        "Concurred on", "Approver", "Approved on", "Start Date", "Due Date", "Month", "Validity Date", "Compliance Task Status", "Duration"
                    ]
                    # "From Date", "To Date",
                    self.write_csv(csv_headers, None)
                    is_header = True
                if row["duration_type"] == 2 and row["frequency_name"] == "On Occurrence":
                    start_date = datetime_to_string_time(row["start_date"])
                    due_date = datetime_to_string_time(row["due_date"])
                    validity_date = datetime_to_string_time(row["validity_date"])
                else:
                    start_date = datetime_to_string(row["start_date"])
                    due_date = datetime_to_string(row["due_date"])
                    validity_date = datetime_to_string(row["validity_date"])
                csv_values = [
                    j, row["unit_code"], row["unitname"], row["act_name"], row["compliance_name"], row["frequency_name"],
                    row["assigned_by"],row["assigned_date"], row["assignee"],row["completed_on"], row["concur"],
                    row["concurred_on"], row["approver"], row["approved_on"], start_date, due_date,
                    datetime_to_moth_year(row["activity_month"]), validity_date, row["compliance_task_status"], row["duration"]
                ]
                # row["fromdate"], row["todate"],
                j = j + 1
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                # os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

    def generate_statutory_settings_unit_wise(
        self, db, request, session_user
    ):
        country_id = request.c_id
        bg_id = request.bg_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        unit_id = request.unit_id
        div_id = request.div_id
        cat_id = request.cat_id
        act = request.act
        compliance_id = request.compliance_id
        frequency_id = request.frequency_id
        status_name = request.status_name
        csv = request.csv
        f_date, t_date = get_from_and_to_date_for_domain(db, country_id, domain_id)


        query = "select (select country_name from tbl_countries where country_id = com.country_id) as countryname, " + \
                "(select domain_name from tbl_domains where domain_id = cc.domain_id) as domainname, " + \
                "concat(unt.unit_code,' - ',unt.unit_name,' - ',unt.address) as unit_name, " + \
                "(select business_group_name from tbl_business_groups where business_group_id = lg.business_group_id) as business_group_name,lg.legal_entity_name, " + \
                "(select division_name from tbl_divisions where division_id = unt.division_id) as division_name, " + \
                "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
                "(CASE cc.compliance_opted_status WHEN 1 THEN " + \
                "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL THEN 'Un-Assigned' ELSE 'Assigned' END) ELSE 'Not Opted' END) as task_status, " + \
                "concat(IFNULL(com.document_name,''),' - ',com.compliance_task) as compliance_name,cf.frequency, " + \
                "aclh.start_date, aclh.due_date, " + \
                "aclh.due_date as activity_month, " + \
                "aclh.completion_date, com.duration " + \
                "from tbl_client_compliances as cc " + \
                "inner join tbl_compliances as com on cc.compliance_id = com.compliance_id " + \
                "inner join tbl_legal_entities as lg on cc.legal_entity_id = lg.legal_entity_id " + \
                "inner join tbl_units as unt on cc.unit_id = unt.unit_id " + \
                "inner join tbl_compliance_frequency as cf on com.frequency_id = cf.frequency_id " + \
                "left join tbl_assign_compliances ac on cc.unit_id = ac.unit_id and cc.compliance_id = ac.compliance_id " + \
                "left join (select ch.compliance_id,ch.unit_id,acl.activity_by,ch.due_date,ch.start_date,ch.completion_date from tbl_compliance_history as ch  " + \
                "inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id and ch.completed_by = acl.activity_by " + \
                "and ch.due_date >= %s and ch.due_date <= %s) as aclh " + \
                "on cc.compliance_id = aclh.compliance_id and cc.unit_id = aclh.unit_id " + \
                "WHERE com.country_id = %s " + \
                "and IF(%s IS NOT NULL,lg.business_group_id = %s,1) " + \
                "and cc.legal_entity_id = %s and cc.domain_id = %s " + \
                "and IF(%s IS NOT NULL,unt.division_id = %s,1) " + \
                "and IF(%s IS NOT NULL,unt.category_id = %s,1) " + \
                "and IF(%s IS NOT NULL,unt.unit_id = %s,1) " + \
                "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
                "and IF(%s > 0,cf.frequency_id = %s,1) " + \
                "and IF(%s IS NOT NULL,com.compliance_id = %s,1) " + \
                "and IF(%s <> 'All', (CASE cc.compliance_opted_status WHEN 1 THEN " + \
                "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL THEN 'Un-Assigned' " + \
                "ELSE 'Assigned' END) ELSE 'Not Opted' END) = %s,1) " + \
                "and cc.compliance_opted_status is not null "

        rows = db.select_all(query, [
                f_date, t_date, country_id, bg_id, bg_id, legal_entity_id, domain_id, div_id,
                div_id, cat_id, cat_id, unit_id, unit_id, act, act, frequency_id, frequency_id,
                compliance_id, compliance_id, status_name, status_name])
        # print "============>", f_date, t_date, get_current_date()
        is_header = False
        j = 1
        if int(len(rows)) > 0:
            s_date = None
            d_date = None
            t_c_date = None
            for row in rows:
                if not is_header:
                    text = "Statutory Settings - Unit Wise Report - (" + row["countryname"] + " - " + row["legal_entity_name"] + " - " + row["domainname"] + ")"
                    csv_headers = [
                        "", "", "", "", "", "", text, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "("+ str(f_date) +" - "+ str(t_date) +")", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "Aparajitha Group", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "", "", "", "", "", "", "as on " + datetime_to_string_time(get_date_time_in_date()) + " (Report generated date)", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                    ]
                    self.write_csv(csv_headers, None)
                    csv_headers = [
                        "SNO", "Business Group", "Legal Entity", "Division Name", "Act", "Status", "Compliance Task",
                        "Frequency", "Start Date", "Due Date", "Month", "Task Completion date"
                    ]
                    self.write_csv(csv_headers, None)
                    is_header = True

                if row["duration"] == 2 and row["frequency"] == "On Occurrence":
                    s_date = datetime_to_string_time(row["due_date"])
                    d_date = datetime_to_string_time(row["completion_date"])
                    t_c_date = datetime_to_string_time(row["start_date"])
                else:
                    s_date = datetime_to_string(row["due_date"])
                    d_date = datetime_to_string(row["completion_date"])
                    t_c_date = datetime_to_string(row["start_date"])
                csv_values = [
                    j, row["business_group_name"], row["legal_entity_name"], row["division_name"],
                    row["act_name"], row["task_status"], row["compliance_name"],row["frequency"],
                    s_date, d_date, datetime_to_moth_year(row["activity_month"]), t_c_date
                ]
                j = j + 1
                self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                # os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

