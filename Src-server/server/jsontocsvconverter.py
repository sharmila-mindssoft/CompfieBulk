import os
import io
import json
import csv
import uuid
from protocol import (
    core
)
from server.common import (
    string_to_datetime, datetime_to_string,
    convert_to_dict
)
from server.clientdatabase.tables import *
from server.clientdatabase.clientreport import *


ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CSV_PATH = os.path.join(ROOT_PATH, "exported_reports")
FILE_DOWNLOAD_BASE_PATH = "/download/csv"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"

class ConvertJsonToCSV(object):

    def __init__(self, db, request, session_user, client_id, report_type):
        s = str(uuid.uuid4())
        file_name = "%s.csv" % s.replace("-", "")
        self.FILE_DOWNLOAD_PATH = "%s/%s" % (FILE_DOWNLOAD_BASE_PATH, file_name)
        self.FILE_PATH = "%s/%s" % (CSV_PATH, file_name)

        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)
        with io.FileIO(self.FILE_PATH, "wb+") as f :
            self.writer = csv.writer(f)  # self.header, quoting=csv.QUOTE_ALL)
            # self.convert_json_to_csv(jsonObj)
            if report_type == "ActivityReport":
                self.generate_compliance_activity_report(db, request, session_user, client_id)
            elif report_type == "RiskReport":
                self.generate_risk_report(db, request, session_user, client_id)
            elif report_type == "ComplianceDetails":
                self.generate_compliance_details_report(db, request, session_user, client_id)
            elif report_type == "TaskApplicability":
                self.generate_task_applicability_report(db, request, session_user, client_id)
            elif report_type == "ClientDetails":
                self.generate_client_details_report(db, request, session_user, client_id)
            elif report_type == "Reassign":
                self.generate_reassign_history_rpeort(db, request, session_user, client_id)
            elif report_type == "StatutoryNotification":
                self.generate_statutory_notification_report(db, request, session_user, client_id)
            elif report_type == "ServiceProviderWise":
                self.generate_service_provider_wise_report(db, request, session_user, client_id)

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

    def generate_compliance_activity_report(self, db, request, session_user, client_id):
        is_header = False
        country_id = request.country_id
        domain_id = request.domain_id
        unit_id = request.unit_id
        user_id = request.user_id
        user_type = request.user_type
        from_date = request.from_date
        to_date = request.to_date
        compliance_id = request.compliance_id
        level_1_statutory_name = request.level_1_statutory_name

        rows = get_compliance_activity_report(
            db, country_id, domain_id, user_type, user_id,
            unit_id, compliance_id,
            level_1_statutory_name, from_date, to_date,
            session_user, client_id
        )
        csv_header = [
            "Unit Name", "Address", "Level 1 Statutory Name",
            "Compliance Name", "Activity Date", "Activity Status",
            "Compliance Status", "Remarks", "Assignee"
        ]
        if not is_header:
            self.write_csv(csv_header, None)
            is_header = True
        for row in rows:
            statutories = row["statutory_mapping"].split(">>")
            level_1_statutory = statutories[0]

            compliance_name = row["compliance_name"]
            if row["document_name"] not in [None, "None", ""]:
                compliance_name = "%s - %s" % (row["document_name"], compliance_name)

            employee_name = row["employee_name"]
            if row["employee_code"] not in ["None", None, ""]:
                employee_name = "%s - %s" % (row["employee_code"], employee_name)
            csv_values = [
                row["unit_name"], row["address"], level_1_statutory,
                compliance_name,
                datetime_to_string(
                    row["activity_date"]
                ),
                core.COMPLIANCE_ACTIVITY_STATUS(row["activity_status"]),
                core.COMPLIANCE_STATUS(row["compliance_status"]),
                row["remarks"], employee_name
            ]
            self.write_csv(None, csv_values)

    def generate_risk_report(self, db, request, session_user, client_id):
        country_id = request.country_id
        domain_id = request.domain_id
        business_group_id = request.business_group_id
        legal_entity_id = request.legal_entity_id
        division_id = request.division_id
        unit_id = request.unit_id
        level_1_statutory_name = request.level_1_statutory_name
        statutory_status = request.statutory_status
        is_header = False
        compliance_list = []
        if statutory_status == 1 :  # Delayed compliance
            where_qry = get_delayed_compliances_where_qry(
                db, business_group_id, legal_entity_id, division_id, unit_id,
                level_1_statutory_name, session_user
            )
            total = get_delayed_compliances_count(
                db, country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id, level_1_statutory_name,
                session_user
            )
            compliance_list = get_delayed_compliances(
                db, domain_id, country_id, where_qry, 0, total
            )
            status = "Delayed Compliance"
        if statutory_status == 2 :  # Not complied
            where_qry = get_not_complied_where_qry(
                db, business_group_id, legal_entity_id, division_id, unit_id,
                level_1_statutory_name
            )
            total = get_not_complied_compliances_count(
                db, country_id, domain_id, where_qry
            )
            compliance_list = get_not_complied_compliances(
                db, domain_id, country_id, where_qry, 0, total
            )
            status = "Not Complied"
        if statutory_status == 3 :  # Not opted
            where_qry = get_not_opted_compliances_where_qry(
                db, business_group_id, legal_entity_id, division_id, unit_id,
                level_1_statutory_name,  session_user
            )
            total = get_not_opted_compliances_count(
                db, country_id, domain_id, where_qry
            )
            compliance_list = get_not_opted_compliances(
                db, domain_id, country_id, where_qry, 0, total
            )
            status = "Not Opted"
        if statutory_status == 4 :  # Unassigned
            where_qry = get_unassigned_compliances_where_qry(
                db, business_group_id, legal_entity_id, division_id, unit_id,
                level_1_statutory_name, session_user
            )
            total = get_unassigned_compliances_count(
                db, country_id, domain_id, where_qry
            )
            compliance_list = get_unassigned_compliances(
                db, domain_id, country_id, where_qry, 0, total
            )
            status = "Unassigned Compliance"
        csv_headers = [
            "Status", "Business Group Name", "Legal Entity Name",
            "Division Name", "Level 1 Statutory Name",
            "Unit Name", "Statutory Mapping", "Compliance Name",
            "Description", "Penal", "Frequency", "Repeats"
        ]
        if not is_header:
            self.write_csv(csv_headers, None)
            is_header = True
        for d in compliance_list:
            unit_name = "%s - %s" % (
                d["unit_code"], d["unit_name"]
            )
            compliance_name = d["compliance_task"]
            if d["document_name"] not in [None, "None", ""]:
                compliance_name = "%s - %s" % (d["document_name"], compliance_name)

            statutory_mapping = "%s >> %s" % (
                d["statutory_mapping"], d["statutory_provision"]
            )
            repeats = ""
            trigger = "Trigger :"
            if d["frequency_id"] != 1 and d["frequency_id"] != 4 :
                if d["repeats_type_id"] == 1 :
                    repeats = "Every %s Day/s " % (d["repeats_every"])
                elif d["repeats_type_id"] == 2 :
                    repeats = "Every %s Month/s " % (d["repeats_every"])
                elif d["repeats_type_id"] == 3 :
                    repeats = "Every %s Year/s " % (d["repeats_every"])
                if d["statutory_dates"] is not None:
                    statutory_dates = json.loads(d["statutory_dates"])
                    for index, statutory_date in enumerate(statutory_dates):
                        if index == 0:
                            if statutory_date["statutory_date"] is not None and statutory_date["statutory_month"] is not None:
                                repeats += "%s %s, " % (
                                    statutory_date["statutory_date"], statutory_date["statutory_month"]
                                )
                            if statutory_date["trigger_before_days"] is not None:
                                trigger += "%s Days" % statutory_date["trigger_before_days"]
                        else:
                            if statutory_date["trigger_before_days"] is not None:
                                trigger += " and %s Days" % statutory_date["trigger_before_days"]
                repeats += trigger
            elif d["frequency_id"] == 1:
                statutory_dates = json.loads(d["statutory_dates"])
                statutory_date = statutory_dates[0]
                if statutory_date["statutory_date"] is not None and statutory_date["statutory_month"] is not None:
                    repeats = "%s %s " % (
                        statutory_date["statutory_date"], db.string_months[statutory_date["statutory_month"]]
                    )
                if statutory_date["trigger_before_days"] is not None:
                    trigger += "%s Days " % statutory_date["trigger_before_days"]
                repeats += trigger
            elif d["frequency_id"] == 4:
                if d["duration_type_id"] == 1 :
                    if d["duration"] is not None:
                        repeats = "Complete within %s Day/s " % (d["duration"])
                elif d["duration_type_id"] == 2 :  # Hours
                    if d["duration"] is not None:
                        repeats = "Complete within %s Hour/s" % (d["duration"])

            csv_values = [
                status, d["business_group"], d["legal_entity"],
                d["division"], d["level_1"], unit_name,
                statutory_mapping, compliance_name,
                d["compliance_description"], d["penal_consequences"],
                d["frequency"], repeats
            ]
            self.write_csv(None, csv_values)

    def generate_compliance_details_report(
        self, db, request, session_user, client_id
    ):
        country_id = request.country_id
        domain_id = request.domain_id
        statutory_id = request.statutory_id
        unit_id = request.unit_id
        compliance_id = request.compliance_id
        assignee_id = request.assignee_id
        from_date = request.from_date
        to_date = request.to_date
        compliance_status = request.compliance_status
        is_header = False

        qry_where = get_where_query_for_compliance_details_report(
            db, country_id, domain_id, statutory_id,
            unit_id, compliance_id, assignee_id,
            from_date, to_date, compliance_status,
            session_user
        )

        total_count = get_compliance_details_total_count(
            db, country_id, domain_id, statutory_id, qry_where
        )
        rows = get_compliance_details(
            db, country_id, domain_id, statutory_id,
            qry_where, 0, total_count
        )

        if not is_header:
            csv_headers = [
                "Unit Name", "Address", "Compliance Name", "Assignee", "Due date",
                "Completion date", "Validity date", "Documents", "Remarks"
            ]
            self.write_csv(csv_headers, None)
            is_header = True
        for compliance in rows:
            unit_name = "%s - %s" % (
                compliance["unit_code"], compliance["unit_name"]
            )
            compliance_name = compliance["compliance_task"]
            if compliance["document_name"] not in [None, "None", ""]:
                compliance_name = "%s - %s" % (compliance["document_name"], compliance_name)
            csv_values = [
                unit_name, compliance["address"],
                compliance_name,  compliance["assigneename"],
                compliance["due_date"],
                compliance["completion_date"],
                compliance["validity_date"], compliance["documents"],
                compliance["status"]
            ]
            self.write_csv(None, csv_values)

    def generate_task_applicability_report(self, db, request, session_user, client_id):
        is_header = False
        business_group = request.business_group_id
        legal_entity = request.legal_entity_id
        division_id = request.division_id
        unit = request.unit_id
        where_qry = None
        where_qry_val = []

        query = "SELECT T2.statutory_provision, T2.statutory_mapping, \
            T2.compliance_task, T2.document_name, T2.format_file, \
            T2.penal_consequences, T2.compliance_description, \
            T2.statutory_dates, T3.unit_id, (select frequency \
                from tbl_compliance_frequency where \
                frequency_id = T2.frequency_id) as frequency,\
            (select business_group_name from tbl_business_groups where business_group_id = T4.business_group_id)business_group, \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = T4.legal_entity_id)legal_entity, \
            (select division_name from tbl_divisions where division_id = T4.division_id )division_name,\
            (select group_concat(unit_code, '-', unit_name) from tbl_units \
                where unit_id = T3.unit_id) as unit_name, \
            (select group_concat(address, '-', postal_code) from tbl_units \
                where unit_id = T3.unit_id) as unit_address, \
            T1.statutory_applicable, T1.statutory_opted, T1.compliance_opted, \
            (select repeat_type from tbl_compliance_repeat_type where \
                repeat_type_id = T2.repeats_type_id) repeat_type, \
            (select duration_type from tbl_compliance_duration_type where \
                duration_type_id = T2.duration_type_id) duration_type , \
            T2.repeats_every, T2.duration \
            FROM tbl_client_compliances T1 \
            INNER JOIN tbl_compliances T2 \
            ON T1.compliance_id = T2.compliance_id \
            INNER JOIN tbl_client_statutories T3 \
            ON T1.client_statutory_id = T3.client_statutory_id \
            INNER JOIN tbl_units T4 \
            ON T3.unit_id = T4.unit_id \
            WHERE T3.country_id = %s \
            AND T3.domain_id = %s \
            %s \
            "
        where_qry_val.extend([request.country_id, request.domain_id])
        if business_group is not None :
            where_qry = " AND T4.business_group_id = %s"
            where_qry_val.append(business_group)

        if legal_entity is not None :
            where_qry += " AND T4.legal_entity_id = %s"
            where_qry_val.append(legal_entity)

        if division_id is not None :
            where_qry += " AND T4.division_id = %s"
            where_qry_val.append(division_id)

        if unit is not None :
            where_qry += " AND T3.unit_id = %s"
            where_qry_val.append(unit)

        if where_qry is None :
            rows = db.select_all(query)
        else :
            rows = db.select_all(query + where_qry, where_qry_val)
        columns = [
            "statutory_provision", "statutory_mapping", "compliance_task",
            "document_name", "format_file", "penal_consequences",
            "compliance_description", "statutory_dates", "unit_id", "frequency",
            "business_group", "legal_entity", "division_name",
            "unit_name", "unit_address", "statutory_applicable",
            "statutory_opted", "compliance_opted",
            "repeat_type", "duration_type", "repeats_every",
            "duration"
        ]
        result = convert_to_dict(rows, columns)

        def statutory_repeat_text(statutory_dates, repeat, repeat_type) :
            trigger_days = ""
            repeats_text = ""
            for index, dat in enumerate(statutory_dates) :
                if dat["statutory_month"] is not None :
                    day = dat["statutory_date"]
                    if day == 1 :
                        day = "1st"
                    elif day == 2 :
                        day = "2nd"
                    else :
                        day = "%sth" % (day)
                    month = db.string_months[dat["statutory_month"]]
                    days = dat["trigger_before_days"]
                    if index == 0 :
                        repeats_text += " %s %s" % (day, month)
                        trigger_days += " %s days" % (days)
                    else :
                        repeats_text += " %s %s" % (day, month)
                        trigger_days += " and %s days" % (days)

            if repeats_text == "" :
                repeats_text = "Every %s %s" % (repeat, repeat_type)
            else :
                repeats_text = "Every %s" % (repeats_text)

            if trigger_days is not "" :
                trigger_days = "triggers (%s)" % (trigger_days)
            result = "%s %s" % (repeats_text, trigger_days)
            return result

        def statutory_duration_text(duration, duration_type):
            result = "To complete within %s %s" % (duration, duration_type)
            return result

        applicable_wise = {}
        for r in result :
            mapping = r["statutory_mapping"].split(">>")
            level_1_statutory = mapping[0]
            level_1_statutory = level_1_statutory.strip()

            if r["statutory_applicable"] == 1 :
                applicability_status = "applicable"
            else :
                applicability_status = "not applicable"

            if r["compliance_opted"] == 0:
                applicability_status = "not opted"

            act_wise = applicable_wise.get(applicability_status)
            if act_wise is None :
                act_wise = {}

            unit_wise = act_wise.get(level_1_statutory)

            document_name = r["document_name"]
            if document_name not in (None, "None", "") :
                compliance_name = "%s - %s" % (document_name, r["compliance_task"])
            else :
                compliance_name = r["compliance_task"]

            if unit_wise is None :
                unit_wise = {}

            statutory_dates = json.loads(r["statutory_dates"])
            repeat_text = ""
            repeats_every = r["repeats_every"]
            repeat_type = r["repeat_type"]
            if repeats_every :
                repeat_text = statutory_repeat_text(statutory_dates, repeats_every, repeat_type)

            duration = r["duration"]
            duration_type = r["duration_type"]
            if duration:
                repeat_text = statutory_duration_text(duration, duration_type)

            compliance_name_list = [compliance_name]
            format_file = r["format_file"]
            if format_file :
                compliance_name_list.append("%s/%s" % (FORMAT_DOWNLOAD_URL, format_file))

            if not is_header:
                csv_headers = [
                    "Unit Name", "Address", "Applicability Status", "Level 1 Statutory", "Statutory Provision",
                    "Statutory Mapping", "Compliance", "Description", "Penal Consequences", "Frequency",
                    "Repeats"
                ]
                self.write_csv(csv_headers, None)
                is_header = True
            for compliance in compliance_name_list:
                csv_values = [
                    r["unit_name"], r["unit_address"], applicability_status, level_1_statutory,
                    r["statutory_provision"], r["statutory_mapping"],
                    compliance, r["compliance_description"],
                    r["penal_consequences"], r["frequency"], repeat_text
                ]
                self.write_csv(None, csv_values)

    def generate_client_details_report(self, db, request, session_user, client_id):
        is_header = False
        country_id = request.country_id
        business_group_id = request.business_group_id
        legal_entity_id = request.legal_entity_id
        division_id = request.division_id
        unit_id = request.unit_id
        domain_ids = request.domain_ids

        condition = get_client_details_condition(
            db, country_id,  business_group_id, legal_entity_id, division_id,
            unit_id, domain_ids, session_user
        )
        columns = "unit_id, unit_code, unit_name, geography, \
                address, domain_ids, postal_code, business_group_name,\
                legal_entity_name, division_name"
        total_count = get_client_details_count(
            db, country_id,  business_group_id, legal_entity_id, division_id,
            unit_id, domain_ids, session_user
        )
        query = "SELECT %s \
                FROM %s u \
                LEFT JOIN %s b ON (b.business_group_id = u.business_group_id)\
                INNER JOIN %s l ON (l.legal_entity_id = u.legal_entity_id) \
                LEFT JOIN %s d ON (d.division_id = u.division_id) \
                WHERE %s \
                ORDER BY u.business_group_id, u.legal_entity_id, u.division_id, \
                u.unit_id DESC LIMIT %s, %s"

        rows = db.select_all(query, [
            columns, tblUnits, tblBusinessGroups,
            tblLegalEntities, tblDivisions, condition,
            0, total_count
        ])
        columns_list = columns.replace(" ", "").split(",")
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
                "group_concat(domain_name) domains",
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

    def generate_reassign_history_rpeort(self, db, request, session_user, client_id):
        is_header = False
        country_id = request.country_id
        domain_id = request.domain_id
        level_1_statutory_name = request.level_1_statutory_id
        unit_id = request.unit_id
        compliance_id = request.compliance_id
        user_id = request.user_id
        from_date = request.from_date
        to_date = request.to_date
        qry_where = get_where_query_for_reassigned_history_report(
            db, country_id, domain_id, level_1_statutory_name,
            unit_id, compliance_id, user_id, from_date, to_date, session_user
        )
        to_count = get_reassigned_history_report_count(
            db, country_id, domain_id, qry_where
        )
        rows = get_reassigned_history_report_data(
            db, country_id, domain_id, qry_where,
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
            #     "compliance_id", "assignee", "reassigned_from", "reassigned_date",
            #     "remarks", "due_date", "compliance_task",
            #     "document_name", "unit_code", "unit_name", "address",
            #     "assigneename", "oldassignee", "unit_id", "statutory_mapping"
            # ]
            mappings = history["statutory_mapping"].split('>>')
            statutory_name = mappings[0].strip()
            statutory_name = statutory_name.strip()
            if history["document_name"] is not None :
                compliance_name = " %s - %s" % (history["document_name"], history["compliance_task"])
            else :
                compliance_name = history["compliance_task"]
            csv_values = [
                history["unit_code"], history["unit_name"], history["address"],
                statutory_name, compliance_name, history["due_date"],
                history["reassigned_from"], history["assigneename"],
                datetime_to_string(history["reassigned_date"]),
                history["remarks"]
            ]
            self.write_csv(None, csv_values)

    def generate_statutory_notification_report(self, db, request_data, session_user, client_id):
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
        condition += " group by business_group_id, legal_entity_id, division_id, unit_id"
        rows = db.get_data(tblStatutoryNotificationsUnits, columns, condition)
        conditiondate = None
        for row in rows:
            business_group_id = row["business_group_id"]
            legal_entity_id = row["legal_entity_id"]
            division_id = row["division_id"]
            unit_id = row["unit_id"]
            query = "SELECT bg.business_group_name, le.legal_entity_name, d.division_name, u.unit_code, u.unit_name, u.address,\
                snl.statutory_provision, snl.notification_text, snl.updated_on \
                from \
                tbl_statutory_notifications_log snl \
                INNER JOIN \
                tbl_statutory_notifications_units snu  ON \
                snl.statutory_notification_id = snu.statutory_notification_id \
                INNER JOIN \
                tbl_business_groups bg ON \
                snu.business_group_id = bg.business_group_id \
                INNER JOIN \
                tbl_legal_entities le ON \
                snu.legal_entity_id = le.legal_entity_id \
                INNER JOIN \
                tbl_divisions d ON \
                snu.division_id = d.division_id \
                INNER JOIN \
                tbl_units u ON \
                snu.unit_id = u.unit_id \
                where \
                snl.country_name = %s \
                and \
                snl.domain_name = %s \
                and \
                bg.business_group_id = %s \
                and \
                le.legal_entity_id = %s \
                and \
                d.division_id = %s \
                and \
                u.unit_id = %s " % (
                    country_name, domain_name, business_group_id,
                    legal_entity_id, division_id, unit_id
                )
            if from_date != '' and to_date != '':
                conditiondate = " AND  snl.updated_on between %s and %s " % (from_date, to_date)
                query = query + conditiondate
            if level_1_statutory_name is not None:
                conditionlevel1 = "AND statutory_provision like %s " % str(level_1_statutory_name + "%")
                query = query + conditionlevel1
            result_rows = db.select_all(query)
            columns = [
                "business_group_name", "legal_entity_name", "division_name", "unit_code", "unit_name", "address",
                "statutory_provision", "notification_text", "updated_on"
            ]
            statutory_notifications = convert_to_dict(result_rows, columns)
            level_1_statutory_wise_notifications = {}
            if len(result_rows) > 0:
                business_group_name = result_rows[0][0]
                legal_entity_name = result_rows[0][1]
                division_name = result_rows[0][2]
                for notification in statutory_notifications:
                    unit_name = "%s - %s" % (notification["unit_code"], notification["unit_name"])
                    statutories = notification["statutory_provision"].split(">>")
                    level_1_statutory_name = statutories[0]
                    if level_1_statutory_name not in level_1_statutory_wise_notifications:
                        level_1_statutory_wise_notifications[level_1_statutory_name] = []

                    if not is_header:
                        csv_headers = [
                            "Business group name", "Legal Entity Name", "Division Name", "Unit Name",
                            "Level 1 statutory mame", "Statutory provision", "Notification Text",
                            "Date and Time"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True
                    csv_values = [
                        business_group_name, legal_entity_name, division_name, unit_name,
                        level_1_statutory_name, notification["statutory_provision"],
                        notification["notification_text"], datetime_to_string(notification["updated_on"])
                    ]
                    self.write_csv(None, csv_values)

    def generate_service_provider_wise_report(self, db, request, session_user, client_id):
        is_header = False
        country_id = request.country_id
        domain_id = request.domain_id
        statutory_id = request.statutory_id
        unit_id = request.unit_id
        service_provider_id = request.service_provider_id

        if service_provider_id is None :
            service_provider_id = '%'

        query = "SELECT service_provider_id, service_provider_name, address, contract_from, contract_to, contact_person, contact_no  \
                FROM tbl_service_providers \
                WHERE service_provider_id like %s and is_active = 1"
        rows = db.select_all(query, [service_provider_id])

        for row in rows:
            service_provider_name = row[1]
            address = row[2]
            contract_from = datetime_to_string(row[3])
            contract_to = datetime_to_string(row[4])
            contact_person = row[5]
            contact_no = row[6]

            user_ids = get_service_provider_user_ids(db, row[0], client_id)
            if unit_id is None :
                unit_ids = get_service_provider_user_unit_ids(db, user_ids, client_id)
            else:
                unit_ids = unit_id

            q = "SELECT unit_id, unit_code, unit_name, address  \
                FROM tbl_units \
                WHERE country_id = %s and unit_id in (%s)"

            unit_rows = db.select_all(q, [country_id, unit_ids])

            for unit in unit_rows:
                unit_id = unit[0]
                unit_name = "%s - %s " % (unit[1], unit[2])
                unit_address = unit[3]

                query = "SELECT c.compliance_task, c.compliance_description, ac.statutory_dates, ac.validity_date, ac.due_date, \
                        ac.assignee, cf.frequency, c.frequency_id, c.duration, c.repeats_every, \
                        (select duration_type from tbl_compliance_duration_type where duration_type_id = c.duration_type_id) AS duration_type, \
                        (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = c.repeats_type_id) AS repeat_type \
                        FROM tbl_client_statutories cs, tbl_client_compliances cc, tbl_compliances c, \
                        tbl_assigned_compliances ac, tbl_compliance_frequency cf where \
                        cs.country_id = %s and cs.domain_id = %s and cs.unit_id = %s and cc.statutory_opted = 1 and ac.is_active = 1 \
                        and cs.client_statutory_id = cc.client_statutory_id and c.compliance_id = cc.compliance_id \
                        and c.compliance_id = ac.compliance_id and ac.unit_id = cs.unit_id and cf.frequency_id = c.frequency_id and ac.assignee in (%s) and \
                        c.statutory_mapping like '%s'" % (
                        country_id, domain_id,
                        unit_id, user_ids, str(statutory_id+"%")
                    )
                compliance_rows = db.select_all(query)

                for compliance in compliance_rows:
                    statutory_dates = compliance[2]
                    statutory_dates = json.loads(statutory_dates)
                    date_list = []
                    for date in statutory_dates :
                        s_date = core.StatutoryDate(
                            date["statutory_date"],
                            date["statutory_month"],
                            date["trigger_before_days"],
                            date.get("repeat_by")
                        )
                        date_list.append(s_date)

                    compliance_name = compliance[0]
                    description = compliance[1]
                    statutory_date = date_list
                    compliance_frequency = core.COMPLIANCE_FREQUENCY(compliance[6])

                    due_date = None
                    if(compliance[4] is not None):
                        due_date = datetime_to_string(compliance[4])

                    validity_date = None
                    if(compliance[3] is not None):
                        validity_date = datetime_to_string(compliance[3])

                    if compliance[7] in (2, 3) :
                        summary = "Repeats every %s - %s" % (compliance[9], compliance[11])
                        for statutory_date in statutory_dates:
                            summary += " (%s %s)" % (
                                statutory_date["statutory_date"], db.string_months[statutory_date["statutory_month"]]
                            )
                    elif compliance[7] == 4 :
                        summary = "To complete within %s - %s" % (compliance[8], compliance[10])
                    else :
                        summary = None

                    if not is_header:
                        csv_headers = [
                            "Service provider name", "Address", "Contract From", "Contract To",
                            "Contact Person", "Contact No", "Compliance name", "Unit Name", "Unit Address",
                            "Frequency", "Description", "Statutory Date", "Due date", "Validity Date"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True
                    frequence_json = compliance_frequency.to_structure()
                    csv_values = [
                        service_provider_name, address, contract_from, contract_to, contact_person,
                        contact_no, compliance_name, unit_name, unit_address,
                        frequence_json, description, summary,
                        due_date, validity_date
                    ]
                    self.write_csv(None, csv_values)
