import os
import json
import csv
import uuid
import datetime
from protocol import (
    core, clientreport, 
)

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
        with open(self.FILE_PATH, 'wb+') as f:
            self.writer = csv.writer(f)#self.header, quoting=csv.QUOTE_ALL) 
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

        unit_ids = unit_id
        unit_ids_list = []

        unit_ids = db.get_user_unit_ids(session_user)
        session_unit_ids = [int(x) for x in unit_ids.split(",")]
        if user_id is not None:
            user_unit_condition = "user_id = '%d'" % user_id
            user_unit_columns = "group_concat(unit_id)"
            rows = db.get_data(db.tblUserUnits, user_unit_columns, user_unit_condition)
            if rows:
                user_unit_ids = rows[0][0]
            user_unit_ids = [int(x) for x in user_unit_ids.split(",")]
            unit_ids_list = list(set(user_unit_ids).intersection(session_unit_ids))
        else:
            unit_ids_list = session_unit_ids
        level_1_statutories_list = []
        if level_1_statutory_name is not None:
            level_1_statutories_list = [level_1_statutory_name]
        else:
            level_1_statutories_list = db.get_level_1_statutories_for_user(
                session_user, client_id, domain_id
            )
        unit_wise_compliances = []
        for unit_id in unit_ids_list:
            unit_columns = "unit_name, unit_code, address"
            unit_condition = "unit_id = '%d'" % unit_id
            unit_rows = db.get_data(
                db.tblUnits, unit_columns, unit_condition
            )
            unit_name = "%s-%s" % (unit_rows[0][1], unit_rows[0][0])
            address = unit_rows[0][2]
            compliance_ids_list = []
            if compliance_id is not None:
                compliance_ids_list = [compliance_id]
            else:
                client_statutory_columns = "group_concat(client_statutory_id)"
                client_statutory_conditions = "country_id = '%d' and domain_id = '%d' and unit_id='%d'" % (
                    country_id, domain_id, unit_id
                )
                client_statutory_rows = db.get_data(
                    db.tblClientStatutories, client_statutory_columns, client_statutory_conditions
                )
                if client_statutory_rows:
                    client_statutory_ids = client_statutory_rows[0][0]
                    client_compliance_columns = "group_concat(compliance_id)"
                    client_compliance_conditions = "client_statutory_id in (%s)" % client_statutory_ids
                    client_compliance_rows = db.get_data(
                        db.tblClientCompliances, client_compliance_columns, client_compliance_conditions
                    )
                    if client_compliance_rows:
                        compliance_ids = client_compliance_rows[0][0]
                        compliance_ids_list = compliance_ids.split(",")
            level_1_statutory_wise_activities = {}
            for level_1_statutory in level_1_statutories_list:
                compliance_wise_activities = {}
                for compliance_id in compliance_ids_list:
                    compliance_columns = "statutory_mapping, document_name, compliance_task, compliance_description"
                    compliance_condition = "statutory_mapping like '%s%s' and compliance_id = '%d'" % (
                        level_1_statutory, "%", int(compliance_id))
                    compliance_rows = db.get_data(
                        db.tblCompliances, compliance_columns, compliance_condition
                    )
                    if compliance_rows:
                        compliance_name = compliance_rows[0][2]
                        if compliance_rows[0][1] not in (None, "None", "") :
                            compliance_name = "%s - %s" % (compliance_rows[0][1], compliance_rows[0][2])

                        compliance_activity_columns = "activity_date, activity_status, compliance_status," \
                        "remarks"
                        compliance_activity_condition = "compliance_id = '%d' and unit_id = '%d'" % (
                            int(compliance_id), int(unit_id)
                        )
                        if from_date is not None and to_date is not None:
                            from_date_in_datetime = db.string_to_datetime(from_date)
                            to_date_in_datetime = db.string_to_datetime(to_date)
                            compliance_activity_condition += " and activity_date between '{}' and '{}'".format(
                                from_date_in_datetime, to_date_in_datetime
                            )
                        else:
                            if from_date is not None:
                                from_date_in_datetime = db.string_to_datetime(from_date)
                                compliance_activity_condition += " and activity_date > '{}' ".format(
                                    from_date_in_datetime
                                )
                            if to_date is not None:
                                to_date_in_datetime = db.string_to_datetime(to_date)
                                compliance_activity_condition += " and activity_date < '{}' ".format(
                                    to_date_in_datetime
                                )
                        compliance_activity_rows = db.get_data(
                            db.tblComplianceActivityLog, compliance_activity_columns, compliance_activity_condition
                        )
                        if compliance_activity_rows:
                            columns = ["activity_date", "activity_status", "compliance_status", "remarks"]
                            compliance_activity_rows = db.convert_to_dict(compliance_activity_rows, columns)
                            activity_data = []
                            csv_header = [
                                "Unit Name", "Address", "Level 1 Statutory Name", 
                                "Compliance Name", "Activity Date", "Activity Status", 
                                "Compliance Status", "Remarks"
                            ]
                            if not is_header:
                                self.write_csv(csv_header, None)
                                is_header = True
                            for compliance_activity in compliance_activity_rows:
                                csv_values = [
                                    unit_name, address, level_1_statutory, compliance_name, 
                                    db.datetime_to_string(compliance_activity["activity_date"]),
                                    compliance_activity["activity_status"],
                                    compliance_activity["compliance_status"],
                                    compliance_activity["remarks"]
                                ]
                                self.write_csv(None, csv_values)

    def generate_risk_report(self, db, request, session_user, client_id):
        country_id = request.country_id
        domain_id = request.domain_id
        business_group_id = request.business_group_id
        legal_entity_id = request.division_id
        division_id = request.division_id
        unit_id = request.unit_id
        level_1_statutory_name = request.level_1_statutory_name
        statutory_status = request.statutory_status
        delayed_compliance = [] #1
        not_complied = [] # 2
        not_opted = [] # 3
        unassigned = [] # 4
        is_header = False
        columns = "group_concat(unit_id), business_group_id, (select business_group_name from \
            %s b where b.business_group_id = u.business_group_id) as business_group_name, \
            legal_entity_id, (select legal_entity_name from  %s l where l.legal_entity_id = \
            u.legal_entity_id) as legal_entity_name, division_id, (select division_name from \
            %s d where d.division_id = u.division_id) as division_name" % (
                db.tblBusinessGroups, db.tblLegalEntities, db.tblDivisions
            )
        condition = "1 "
        if business_group_id is not None:
            condition += " and u.business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " and u.legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " and u.division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " and u.unit_id = '%d'" % unit_id
        condition += " group by business_group_id, legal_entity_id, division_id"
        rows = db.get_data(db.tblUnits+" u", columns, condition)
        
        level_1_statutories_list = [level_1_statutory_name]
        if level_1_statutory_name is None:
            level_1_statutories_list = db.get_level_1_statutories_for_user(
                session_user, client_id, domain_id
            )

        risk_report_Data = []
        for row in rows:
            unit_ids_list = [int(x) for x in row[0].split(",")]
            business_group_name = row[2]
            legal_entity_name = row[4]
            division_name = row[6]
            level_1_statutory_wise_units = {}
            for level_1_statutory in level_1_statutories_list:
                unit_wise_compliances = []
                for unit_id in unit_ids_list:
                    compliance_ids_list = [""] * 4
                    if statutory_status in [1, 2, None, "None", "", 0]:
                        if statutory_status in [1,None, "None", "", 0]: # Delayed compliance
                            query = "SELECT group_concat(distinct compliance_id) FROM tbl_compliance_history \
                                WHERE unit_id = '%d' AND completed_on > due_date AND \
                                approve_status = 1" % unit_id
                            compliance_history_rows = db.select_all(query)
                            if len(compliance_history_rows) > 0:
                                compliance_ids_list[0] = compliance_history_rows[0][0]
                        if statutory_status in [2, None, "None", "", 0]: # Not complied 
                            query = "SELECT group_concat(distinct compliance_id) FROM tbl_compliance_history \
                                WHERE unit_id = '%d' AND (approve_status = 0 or \
                                approve_status is null) AND due_date < now()" % unit_id
                            compliance_history_rows = db.select_all(query)
                            if len(compliance_history_rows) > 0:
                                compliance_ids_list[1] = compliance_history_rows[0][0]
                    if statutory_status in [4, None, "None", "", 0]:# Unassigned compliances
                        query = "SELECT GROUP_CONCAT(distinct compliance_id) FROM tbl_client_compliances WHERE \
                            client_statutory_id IN (SELECT client_statutory_id FROM \
                            tbl_client_statutories WHERE unit_id = '%d') and compliance_id \
                            NOT IN (SELECT compliance_id FROM tbl_assigned_compliances \
                            WHERE unit_id = '%d') AND compliance_opted = 1" % (unit_id, unit_id)
                        result = db.select_all(query)
                        if len(result) > 0:
                            compliance_ids_list[3] = result[0][0]
                    if statutory_status in [3, None, "None", "", 0]: # Not Opted
                        query = "SELECT GROUP_CONCAT(distinct compliance_id) FROM tbl_client_compliances where \
                            client_statutory_id IN (SELECT client_statutory_id FROM \
                            tbl_client_statutories WHERE unit_id = '%d') AND \
                            compliance_opted = 0" % (unit_id)
                        result = db.select_all(query)
                        if len(result) > 0:
                            compliance_ids_list[2] = result[0][0]
                    compliances_list = []
                    for index, compliance_ids in enumerate(compliance_ids_list): 
                        status = None
                        if index == 0:
                            status = "Delayed Compliance"
                        elif index == 1:
                            status = "Not Complied"
                        elif index == 2:
                            status = "Not Opted"
                        else:
                            status = "Unassigned"
                        if compliance_ids not in ["", None, "None"]:
                            compliance_columns = "document_name, compliance_task, compliance_description, \
                            penal_consequences, (select frequency from %s f where c.frequency_id = \
                            f.frequency_id) as frequency, c.frequency_id, repeats_type_id, repeats_every, \
                            duration_type_id, duration, statutory_dates, statutory_mapping, \
                            statutory_provision" % (
                                db.tblComplianceFrequency
                            )
                            compliance_condition = "statutory_mapping like '%s%s' and compliance_id \
                            in (%s)" % (level_1_statutory, "%" , compliance_ids)
                            compliance_rows = db.get_data(
                                db.tblCompliances+" c", compliance_columns, compliance_condition
                            )
                            compliance_columns = [
                                "document_name", "compliance_task", "compliance_description",
                                "penal", "frequency", "frequency_id", "repeats_type_id", "repeats_every",
                                "duration_type_id", "duration", "statutory_dates", "statutory_mapping",
                                "statutory_provision"
                            ]
                            compliance_rows = db.convert_to_dict(
                                compliance_rows, compliance_columns
                            )
                            for compliance in compliance_rows:
                                compliance_name =  compliance["compliance_task"]
                                if compliance["document_name"] not in (None, "None", "") :
                                    compliance_name = "%s - %s" % (
                                        compliance["document_name"], compliance["compliance_task"]
                                    )
                                statutory_mapping = "%s >> %s" % (
                                    compliance["statutory_mapping"], compliance["statutory_provision"]
                                )
                                repeats = ""
                                trigger = "Trigger :"
                                if compliance["frequency_id"] != 1 and compliance["frequency_id"] != 4: # checking not onetime and onoccrence
                                    if compliance["repeats_type_id"] == 1: # Days
                                        repeats = "Every %s Day/s " % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 2: # Month
                                        repeats = "Every %s Month/s " % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 3: # Year
                                        repeats = "Every %s Year/s " % (compliance["repeats_every"])
                                    if compliance["statutory_dates"] is not None:
                                        statutory_dates = json.loads(compliance["statutory_dates"])
                                        for index, statutory_date in enumerate(statutory_dates):
                                            if index  == 0:
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
                                elif compliance["frequency_id"] == 1:
                                    statutory_dates = json.loads(compliance["statutory_dates"])
                                    statutory_date = statutory_dates[0]
                                    if statutory_date["statutory_date"] is not None and statutory_date["statutory_month"] is not None:
                                        repeats = "%s %s " % (
                                            statutory_date["statutory_date"], db.string_months[statutory_date["statutory_month"]]
                                        )
                                    if statutory_date["trigger_before_days"] is not None:
                                        trigger += " %s Day/s" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 4:
                                    if compliance["duration_type_id"] == 1: # Days
                                        if compliance["duration"] is not None:
                                            repeats = "Complete within %s Day/s" % (compliance["duration"])
                                    elif compliance["duration_type_id"] == 2: # Hours
                                        if compliance["duration"] is not None:
                                            repeats = "Complete with in %s Hour/s" % (compliance["duration"])
                                
                                csv_headers = [
                                    "Status", "Business Group Name", "Legal Entity Name", 
                                    "Division Name", "Level 1 Statutory Name",
                                    "Unit Name", "Statutory Mapping", "Compliance Name",
                                    "Description", "Penal", "Frequency", "Repeats"
                                ]
                                if not is_header:
                                    self.write_csv(csv_headers, None)
                                    is_header = True
                                unit_columns = "unit_code, unit_name"
                                unit_condition = "unit_id = '%d'" % unit_id
                                unit_rows = db.get_data(db.tblUnits, unit_columns, unit_condition)
                                unit_name = unit_rows[0][1]
                                if unit_rows[0][0] is not None:
                                    unit_name = "%s-%s"  % (unit_rows[0][0], unit_rows[0][1])

                                csv_values = [
                                    status, business_group_name, legal_entity_name,
                                    division_name, level_1_statutory, unit_name, 
                                    statutory_mapping, compliance_name,
                                    compliance["compliance_description"], compliance["penal"],
                                    compliance["frequency"], repeats
                                ]
                                self.write_csv(None, csv_values)

    def generate_compliance_details_report(
        self, db, request, session_user, client_id):
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

        if compliance_id is None :
            compliance_id = '%'
        if assignee_id is None :
            assignee_id = '%'
        if request.compliance_status is None :
            compliance_status = '%'
        # else :
        #     compliance_status = core.COMPLIANCE_STATUS(request.compliance_status)

        if unit_id is None :
            unit_ids = db.get_user_unit_ids(session_user, client_id)
        else :
            unit_ids = unit_id

        if from_date is None :
            query = "SELECT period_from, period_to FROM tbl_client_configurations where country_id = %s AND domain_id = %s " % (country_id, domain_id)
            daterow = db.select_all(query, client_id)

            period_from = daterow[0][0]
            period_to = daterow[0][1]

            current_year = datetime.date.today().year

            if period_from == 1 :
                year_from = current_year
                year_to = current_year
            else :
                current_month = datetime.date.today().month
                if current_month < period_from :
                    year_from = datetime.date.today().year - 1
                    year_to = datetime.date.today().year
                else :
                    year_from = datetime.date.today().year
                    year_to = datetime.date.today().year + 1

            start_date = db.string_to_datetime('01-' + db.string_months[period_from] + '-' + str(year_from))
            day = "30-"
            if period_to == 2:
                day = "28-"
            elif period_to in [1, 3, 5, 7, 8, 10, 12]:
                day = "31-"
            end_date = db.string_to_datetime(
                day + db.string_months[period_to] + '-' + str(year_to))

        else :
            start_date = db.string_to_datetime(from_date)
            end_date = db.string_to_datetime(to_date)

        unit_columns = "unit_id, unit_code, unit_name, address"
        detail_condition = "country_id = '%d' and unit_id in (%s) " % (country_id, unit_ids)
        unit_rows = db.get_data(db.tblUnits, unit_columns, detail_condition)

        unit_wise_compliances = []
        for unit in unit_rows:
            unit_id = unit[0]
            unit_name = "%s - %s " % (unit[1], unit[2])
            unit_address = unit[3]

            query = "SELECT ch.compliance_history_id, c.document_name, c.compliance_description, ch.validity_date, ch.due_date, \
                    (SELECT concat( u.employee_code, '-' ,u.employee_name ) FROM tbl_users u WHERE u.user_id = ch.completed_by) AS assigneename, \
                    ch.documents, ch.completion_date, c.compliance_task, c.frequency_id \
                    from tbl_compliances c,tbl_compliance_history ch, \
                    tbl_units ut where \
                    ch.unit_id = %s \
                    AND ut.country_id = %s and c.domain_id = %s and ch.unit_id = ut.unit_id\
                    AND c.compliance_id = ch.compliance_id \
                    AND ch.completed_by like '%s'  AND c.statutory_mapping like '%s'  AND c.compliance_id like '%s' and ch.due_date BETWEEN '%s' AND '%s'" % (
                    unit_id, country_id, domain_id,
                    assignee_id, str(statutory_id+"%"), compliance_id, start_date, end_date
                )
            compliance_rows = db.select_all(query, client_id)

            compliances_list = []
            for compliance in compliance_rows:

                if compliance[1] == "None" :
                    compliance_name = compliance[8]
                else :
                    compliance_name = compliance[1]+' - '+compliance[8]

                if compliance[5] is None :
                    assignee = 'Administrator'
                else :
                    assignee = compliance[5]

                due_date = None
                if(compliance[4] != None):
                    due_date = db.datetime_to_string(compliance[4])

                validity_date = None
                if(compliance[3] != None):
                    validity_date = db.datetime_to_string(compliance[3])

                documents = compliance[6]
                # no_of_days, compliance_status = db.calculate_ageing(due_date=compliance[4], completion_date=compliance[7])
                completion_date = None
                if(compliance[7] != None):
                    completion_date = db.datetime_to_string(compliance[7])

                remarks = db.calculate_ageing(compliance[4], compliance[8], compliance[7])

                if(compliance_status == 'Complied'):
                    c_status = 'On Time'
                elif(compliance_status == 'Delayed Compliance'):
                    c_status = 'Delayed'
                elif(compliance_status == 'Inprogress'):
                    c_status = 'days left'
                elif(compliance_status == 'Not Complied'):
                    c_status = 'Overdue'
                else:
                    c_status = ''

                if not is_header:
                    csv_headers = [
                        "Unit Name", "Address", "Compliance Name", "Assignee", "Due date",
                        "Completion date", "Validity date", "Documents", "Remarks"
                    ]
                    self.write_csv(csv_headers, None)
                    is_header = True
                if (c_status in remarks[1] or c_status == '') :
                    csv_values = [
                        unit_name, unit_address, compliance_name, assignee, due_date, completion_date,
                        validity_date, documents, remarks[1]
                    ]
                    self.write_csv(None, csv_values)

    def generate_task_applicability_report(self, db, request, session_user, client_id):
        is_header = False
        business_group = request.business_group_id
        legal_entity = request.legal_entity_id
        division_id = request.division_id
        unit = request.unit_id
        where_qry = ""
        if business_group is not None :
            where_qry = " AND T4.business_group_id = %s" % (business_group)

        if legal_entity is not None :
            where_qry += " AND T4.legal_entity_id = %s" % (legal_entity)

        if division_id is not None :
            where_qry += " AND T4.division_id = %s" % (division_id)

        if unit is not None :
            where_qry += " AND T3.unit_id = %s" % (unit)

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
            " % (
                request.country_id,
                request.domain_id,
                where_qry
            )
        rows = db.select_all(query)
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
        result = db.convert_to_dict(rows, columns)

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
            unit_id = r["unit_id"]
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
        condition = "country_id = '%d' "%(country_id)
        if business_group_id is not None:
            condition += " AND business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " AND legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " AND division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " AND unit_id = '%d'" % unit_id
        else:
            condition += " AND unit_id in (%s)" % db.get_user_unit_ids(session_user)
        if domain_ids is not None:
            for domain_id in domain_ids:
                condition += " AND  ( domain_ids LIKE  '%,"+str(domain_id)+",%' "+\
                            "or domain_ids LIKE  '%,"+str(domain_id)+"' "+\
                            "or domain_ids LIKE  '"+str(domain_id)+",%'"+\
                            " or domain_ids LIKE '"+str(domain_id)+"') "

        group_by_columns = "business_group_id, legal_entity_id, division_id"
        group_by_condition = condition+" group by business_group_id, legal_entity_id, division_id"
        group_by_rows = db.get_data(db.tblUnits, group_by_columns, group_by_condition)
        for row in group_by_rows:
            business_group_row = db.get_data(
                db.tblBusinessGroups, "business_group_name", "business_group_id = '%d'" % row[0]
            )
            business_group_name = business_group_row[0][0] if len(business_group_row) > 0 else ""

            legal_entity_row = db.get_data(
                db.tblLegalEntities, "legal_entity_name", "legal_entity_id = '%d'" % row[1]
            )
            legal_entity_name = legal_entity_row[0][0]

            division_row = db.get_data(
                db.tblDivisions, "division_name", "division_id = '%d'" % row[2]
            )
            division_name = division_row[0][0] if len(division_row) > 0 else ""

            columns = "unit_id, unit_code, unit_name, geography, "\
            "address, domain_ids, postal_code"
            where_condition = "legal_entity_id = '%d' "% row[1]
            if row[0] == None:
                where_condition += " And business_group_id is NULL"
            else:
                where_condition += " And business_group_id = '%d'" % row[0]
            if row[2] == None:
                where_condition += " And division_id is NULL"
            else:
                where_condition += " And division_id = '%d'" % row[2]
            if unit_id is not None:
                where_condition += " AND unit_id = '%d'" % unit_id
            else:
                where_condition += " AND unit_id in (%s)" % db.get_user_unit_ids(session_user)
            if domain_ids is not None:
                for domain_id in domain_ids:
                    where_condition += " AND  ( domain_ids LIKE  '%,"+str(domain_id)+",%' "+\
                                "or domain_ids LIKE  '%,"+str(domain_id)+"' "+\
                                "or domain_ids LIKE  '"+str(domain_id)+",%'"+\
                                " or domain_ids LIKE '"+str(domain_id)+"') "
            where_condition += " AND country_id = '%d' " % country_id
            result_rows = db.get_data(db.tblUnits, columns,  where_condition)
            units = []
            if not is_header:
                csv_headers = [
                    "Business Group", "Legal Entity", "Division", "Unit Code", "Unit Name", "Geography", 
                    "Address", "Domains", "Postal Code"
                ]
                self.write_csv(csv_headers, None)
                is_header = True
            for result_row in result_rows:
                domain_names = db.get_data(
                    db.tblDomains, "group_concat(domain_name)", "domain_id in (%s)" % result_row[5]
                )[0][0]
                csv_values = [
                    business_group_name, legal_entity_name, division_name, result_row[1],
                    result_row[2], result_row[3], result_row[4], domain_names, result_row[6]
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
        level_1_statutories_list = db.get_level_1_statutories_for_user(
            session_user, client_id, domain_id
        )
        if level_1_statutory_name is not None:
            level_1_statutories_list = [level_1_statutory_name]

        unit_ids = db.get_user_unit_ids(session_user, client_id)
        unit_ids_list = [int(x) for x in unit_ids.split(",")]
        if unit_id is not None:
            unit_ids_list = [unit_id]

        level_1_statutory_wise_compliance = []
        for level_1_statutory in level_1_statutories_list:
            unit_wise_compliances = []
            for unit_id in unit_ids_list:
                columns = "compliance_id, document_name, compliance_task, compliance_description, "\
                "statutory_mapping"
                condition = "select compliance_id from %s where \
                    unit_id = '%d' group by compliance_id" % (
                        db.tblReassignedCompliancesHistory, unit_id
                    )
                if compliance_id is not None:
                    condition = compliance_id
                whereCondition = " compliance_id in (%s) and statutory_mapping like '%s%s'" % (
                        condition, level_1_statutory, "%"
                )

                compliance_rows = db.get_data(
                    db.tblCompliances, columns, whereCondition
                )

                compliance_wise_history = []
                if len(compliance_rows) > 0:
                    compliance_columns = [
                        "compliance_id", "document_name", "compliance_task", "compliance_description",
                        "tc.statutory_mapping"
                    ]
                    compliance_rows = db.convert_to_dict(
                        compliance_rows, compliance_columns
                    )

                    for compliance in compliance_rows:
                        compliance_name = compliance["compliance_task"]
                        if compliance["document_name"] not in (None, "None", "") :
                            compliance_name = "%s - %s" % (
                                compliance["document_name"], compliance["compliance_task"]
                            )
                        reassign_columns = "assignee, reassigned_from, reassigned_date, remarks"
                        condition = "1"
                        if user_id is not None:
                            condition = "reassigned_from = '%d' or assignee = '%d'" % (
                                user_id, user_id
                            )
                        if from_date is not None and to_date is not None:
                            condition += " and reassigned_date between '{}' and '{}'".format(
                                from_date, to_date
                            )
                        elif from_date is None and to_date is None:
                            current_year = db.get_date_time().year
                            result = db.get_country_domain_timelines(
                                [country_id], [domain_id], [current_year], client_id
                            )
                            calculated_from_date = result[0][1][0][1][0]["start_date"]
                            calculated_to_date = result[0][1][0][1][0]["end_date"]
                            condition += " and reassigned_date between '{}' and '{}'".format(
                                calculated_from_date, calculated_to_date
                            )
                        else:
                            if from_date is not None:
                                condition += " and reassigned_date > '{}'".format(from_date)
                            elif to_date is not None:
                                condition += " and reassigned_date < '{}'".format(to_date)

                        reassign_condition = "compliance_id = '%d' and unit_id = '%d' \
                        and %s" % (
                            compliance["compliance_id"], unit_id, condition
                        )
                        reassign_rows = db.get_data(
                            db.tblReassignedCompliancesHistory, reassign_columns, reassign_condition
                        )
                        
                        current_due_date_column = "due_date"
                        current_due_date_condition = " next_due_date = (select due_date from %s where \
                            compliance_id = '%d' and unit_id = '%d')" % (
                            db.tblAssignedCompliances, compliance["compliance_id"], unit_id
                        )
                        current_due_date_rows = db.get_data(
                            db.tblComplianceHistory, current_due_date_column, current_due_date_condition
                        )
                        current_due_date = db.datetime_to_string(current_due_date_rows[0][0])
                        if not is_header:
                            csv_headers = [
                                "Unit Code", "Unit Name", "Address", "Level 1 statutory",
                                "Compliance Name", "Due date","Assignee", "Reassigned to",
                                "Reassigned date", "Remarks"
                            ]
                            self.write_csv(csv_headers, None)
                            is_header = True

                        unit_column = "unit_code, unit_name, address"
                        condition = "unit_id = '%d'" % unit_id
                        unit_rows = db.get_data(
                            db.tblUnits, unit_column, condition
                        )
                        history_list = []
                        if reassign_rows:
                            for history in reassign_rows:
                                reassigned_from = db.get_user_name_by_id(history[1], client_id)
                                reassigned_to = db.get_user_name_by_id(history[0], client_id)
                                csv_values = [
                                    unit_rows[0][0], unit_rows[0][1], unit_rows[0][2],
                                    level_1_statutory, compliance_name, current_due_date,
                                    reassigned_from, reassigned_to, db.datetime_to_string(history[2]),
                                    history[3]
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
            from_date = self.string_to_datetime(from_date)
        if to_date is None:
            to_date = ''
        else:
            to_date = self.string_to_datetime(to_date)
        condition = "1"
        if business_group_id is not None:
            condition += " AND business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " AND legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " AND division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " AND unit_id = '%d'" % unit_id

        # Gettings distinct sets of bg_id, le_id, div_id, unit_id
        columns = "business_group_id, legal_entity_id, division_id, unit_id"
        where_condition = "1 AND %s" % condition
        where_condition += " group by business_group_id, legal_entity_id, division_id, unit_id"
        rows = db.get_data(db.tblStatutoryNotificationsUnits, columns, where_condition)
        columns = ["business_group_id", "legal_entity_id", "division_id", "unit_id"]
        rows = db.convert_to_dict(rows, columns)
        notifications = []
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
                snl.country_name = '%s' \
                and \
                snl.domain_name = '%s' \
                and \
                bg.business_group_id = '%d' \
                and \
                le.legal_entity_id = '%d' \
                and \
                d.division_id = '%d' \
                and \
                u.unit_id = '%d' " % (
                    country_name, domain_name, business_group_id, legal_entity_id, division_id, unit_id
                )
            if from_date != '' and to_date != '':
                conditiondate = " AND  snl.updated_on between '%s' and '%s' " % (from_date, to_date)
                query = query + conditiondate
            if level_1_statutory_name is not None:
                conditionlevel1 = "AND statutory_provision like '%s'" % str(level_1_statutory_name + "%")
                query = query + conditionlevel1
            result_rows = db.select_all(query)
            columns = [
                "business_group_name", "legal_entity_name", "division_name", "unit_code", "unit_name", "address",
                "statutory_provision", "notification_text", "updated_on"
            ]
            statutory_notifications = db.convert_to_dict(result_rows, columns)
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
                            "Level 1 statutory mame","Statutory provision", "Notification Text",
                            "Date and Time"
                        ]
                        self.write_csv(csv_headers, None)
                        is_header = True
                    csv_values = [
                        business_group_name, legal_entity_name, division_name, unit_name,
                        level_1_statutory_name, notification["statutory_provision"], 
                        notification["notification_text"],db.datetime_to_string(notification["updated_on"])
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
                WHERE service_provider_id like '%s' and is_active = 1" % (service_provider_id)
        rows = db.select_all(query, client_id)

        service_provider_wise_compliances_list = []
        for row in rows:
            service_provider_name = row[1]
            address = row[2]
            contract_from = db.datetime_to_string(row[3])
            contract_to = db.datetime_to_string(row[4])
            contact_person = row[5]
            contact_no = row[6]

            user_ids = db.get_service_provider_user_ids(row[0], client_id)
            if unit_id is None :
                unit_ids = db.get_service_provider_user_unit_ids(user_ids, client_id)
            else:
                unit_ids = unit_id

            q = "SELECT unit_id, unit_code, unit_name, address  \
                FROM tbl_units \
                WHERE country_id = '%d' and unit_id in (%s)" % (country_id, unit_ids)

            unit_rows = db.select_all(q, client_id)

            unit_wise_compliances = {}
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

                compliances_list = []
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
                        due_date = db.datetime_to_string(compliance[4])

                    validity_date = None
                    if(compliance[3] is not None):
                        validity_date = db.datetime_to_string(compliance[3])

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
                        csv_headers =[ 
                            "Service provider name", "Address", "Contract From", "Contract To",
                            "Contact Person", "Contact No", "Compliance name","Unit Name", "Unit Address",
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