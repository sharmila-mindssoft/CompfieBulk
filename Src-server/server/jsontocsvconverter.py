import os
import json
import csv
import uuid
from protocol import (
    core, clientreport, 
)

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CSV_PATH = os.path.join(ROOT_PATH, "exported_reports")
FILE_DOWNLOAD_BASE_PATH = "/download/csv"

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
                self.generater_risk_report(db, request, session_user, client_id)

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

    def generater_risk_report(self, db, request, session_user, client_id):
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
        print
        print rows
        level_1_statutories_list = [level_1_statutory_name]
        if level_1_statutory_name is None:
            level_1_statutories_list = db.get_level_1_statutories_for_user(
                session_user, client_id, domain_id
            )
        print "level_1_statutories_list:{}".format(level_1_statutories_list)

        risk_report_Data = []
        for row in rows:
            unit_ids_list = [int(x) for x in row[0].split(",")]
            print
            print "unit_ids list : {}".format(unit_ids_list)
            business_group_name = row[2]
            legal_entity_name = row[4]
            division_name = row[6]
            level_1_statutory_wise_units = {}
            for level_1_statutory in level_1_statutories_list:
                unit_wise_compliances = []
                for unit_id in unit_ids_list:
                    compliance_history_columns = "compliance_id, (select statutory_mapping from \
                     %s c where ch.compliance_id = c.compliance_id and statutory_mapping like '%s%s') \
                    as statu" % (db.tblCompliances, level_1_statutory, "%")
                    compliance_history_condition = "unit_id = '%d'" % (
                        unit_id
                    )
                    if statutory_status == 1:
                        compliance_history_condition += " and completed_on > due_date and \
                        approve_status = 1"
                    elif statutory_status == 2:
                        compliance_history_condition += " and (approve_status = 0 or \
                        approve_status is null) and due_date < now()"
                    compliance_history_rows = db.get_data(
                        db.tblComplianceHistory+" ch", compliance_history_columns, compliance_history_condition
                    )
                    print "compliance_history_rows : {}".format(compliance_history_rows)
                    
                    compliances_list = []
                    if len(compliance_history_rows) > 0:
                        compliance_ids = compliance_history_rows[0][0]
                        statutory_mapping = compliance_history_rows[0][1]
                        if compliance_ids is not None and statutory_mapping is not None:
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
                                repeats = None
                                trigger = "Trigger :"
                                if compliance["frequency_id"] != 1 and compliance["frequency_id"] != 4: # checking not onetime and onoccrence
                                    if compliance["repeats_type_id"] == 1: # Days
                                        repeats = "Every %s Day/s" % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 2: # Month
                                        repeats = "Every %s Month/s" % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 3: # Year
                                        repeats = "Every %s Year/s" % (compliance["repeats_every"])
                                    if compliance["statutory_dates"] is not None:
                                        statutory_dates = json.loads(compliance["statutory_dates"])
                                        for index, statutory_date in enumerate(statutory_dates):
                                            if index  == 0:
                                                repeats += "%s %s, " % (
                                                    statutory_date["statutory_date"], statutory_date["statutory_month"]
                                                )
                                                trigger += "%s Days" % statutory_date["trigger_before_days"]
                                            else:
                                                trigger += " and %s Days" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 1:
                                    statutory_dates = json.loads(compliance["statutory_dates"])
                                    statutory_date = statutory_dates[0]
                                    repeats = "%s %s" % (
                                        statutory_date["statutory_date"], statutory_date["statutory_month"]
                                    )
                                    trigger += "%s Days" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 4:
                                    if compliance["duration_type_id"] == 1: # Days
                                        repeats = "Complete within %s Day/s" % (compliance["duration"])
                                    elif compliance["duration_type_id"] == 2: # Hours
                                        repeats = "Complete %s Hour/s" % (compliance["duration"])
                                
                                csv_headers = [
                                    "Business Group Name", "Legal Entity Name", 
                                    "Division Name", "Level 1 Statutory Name",
                                    "Unit Name", "Statutory Mapping", "Compliance Name",
                                    "Description", "Penal", "Frequency", "Repeats"
                                ]
                                if not is_header:
                                    self.write_csv(csv_headers, None)
                                unit_columns = "unit_code, unit_name"
                                unit_condition = "unit_id = '%d'" % unit_id
                                unit_rows = db.get_data(db.tblUnits, unit_columns, unit_condition)
                                unit_name = unit_rows[0][1]
                                if unit_rows[0][0] is not None:
                                    unit_name = "%s-%s"  % (unit_rows[0][0], unit_rows[0][1])

                                frequency_columns = "frequency"
                                frequency_condition = "frequency_id = '%d'" % compliance["frequency_id"]
                                frequency_rows = db.get_data(db.tblComplianceFrequency, frequency_columns, frequency_condition)

                                csv_values = [
                                    business_group_name, legal_entity_name,
                                    division_name, level_1_statutory_name, 
                                    unit_name, statutory_mapping, compliance_name,
                                    compliance["compliance_description"], compliance["penal"],
                                    frequency_rows[0][0], repeats
                                ]
                                self.write_csv(None, csv_values)