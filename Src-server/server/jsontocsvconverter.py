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

    def __init__(self, db, request, session_user, client_id):
        s = str(uuid.uuid4())
        file_name = "%s.csv" % s.replace("-", "")
        self.FILE_DOWNLOAD_PATH = "%s/%s" % (FILE_DOWNLOAD_BASE_PATH, file_name)
        self.FILE_PATH = "%s/%s" % (CSV_PATH, file_name)

        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)
        with open(self.FILE_PATH, 'wb+') as f:
            self.writer = csv.writer(f)#self.header, quoting=csv.QUOTE_ALL) 
            # self.convert_json_to_csv(jsonObj)
            self.generate_compliance_activity_report(db, request, session_user, client_id)

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
