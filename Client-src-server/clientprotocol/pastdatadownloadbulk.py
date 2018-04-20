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
from server.clientdatabase.general import (
    calculate_due_date, filter_out_due_dates)
from clientprotocol import (
    clienttransactions, clientcore
)
from server.common import datetime_to_string

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CSV_PATH = os.path.join(ROOT_PATH, "exported_reports")
FILE_DOWNLOAD_BASE_PATH = "/download/csv"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"


class PastDataJsonToCSV(object):
    def __init__(self, db, request, session_user, report_type):
        s = str(uuid.uuid4())
        file_name = "%s.csv" % s.replace("-", "")
        self.FILE_DOWNLOAD_PATH = "%s/%s" % (
            CSV_DOWNLOAD_URL, file_name)
        print "File Download Path", self.FILE_DOWNLOAD_PATH
        self.FILE_PATH = "%s/%s" % (CSV_PATH, file_name)
        self.documents_list = []
        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)
        with io.FileIO(self.FILE_PATH, "wb+") as f:
            self.writer = csv.writer(f)
            # self.header, quoting=csv.QUOTE_ALL)
            # self.convert_json_to_csv(jsonObj)
            if report_type == "DownloadPastData":
                self.download_past_data(
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

    def download_past_data(self, db, request, session_user):
        is_header = False

        unit_id = request.unit_id
        domain_id = request.domain_id
        compliance_frequency = request.compliance_frequency
        le_name = request.le_name
        domain_name = request.d_name
        unit_name = request.u_name
        unit_code = request.u_code

        # country_id = request.country_id
        start_count = request.start_count
        statutory_wise_compliances = []
        # To Do - Loop for complaince frequency
        statutory_wise_compliances = get_download_bulk_compliance_data(
                db, unit_id, domain_id, "", compliance_frequency, session_user,
                start_count, 100
        )
        sno = 0
        print "statutory_wise_compliances", statutory_wise_compliances
        if len(statutory_wise_compliances) > 0:
            for swc in statutory_wise_compliances[0]:
                print "swc ->> ", swc
                # print "level 1 -->>>", swc.level_1_statutory_name
                print "pr_compliances-->>>", swc.compliances[0]

                level_statu_name = swc.level_1_statutory_name
                compliances = swc.compliances

                if not is_header:
                    # csv_headers = [
                    #     "SNO", "Legal_Entity", "Domain", "Unit_Code",
                    #     "Unit_Name", "Primary_Legislation",
                    #     "Secondary_Legislation", "Compliance_Task",
                    #     "Compliance_Description", "Compliance_Frequency",
                    #     "Statutory_Date", "Due_Date", "Assignee",
                    #     "Completion_Date*", "Document_Name"
                    # ]
                    csv_headers = [
                        "Legal_Entity", "Domain", "Unit_Code",
                        "Unit_Name", "Primary_Legislation",
                        "Secondary_Legislation", "Compliance_Task",
                        "Compliance_Description", "Compliance_Frequency",
                        "Statutory_Date", "Due_Date", "Assignee",
                        "Completion_Date*", "Document_Name"
                    ]
                    self.write_csv(csv_headers, None)

                    for comp in compliances:
                        description = comp.description
                        print "pastdatadownloadbulk>due_date>>", comp.due_date
                        due_date = comp.due_date
                        compliance_name = comp.compliance_name
                        compliance_task_frequency = comp.frequency.to_structure()
                        statutory_date = comp.statutory_date
                        assignee_name = comp.assignee_name
                        is_header = True
                        csv_values = [
                            le_name, domain_name, unit_code, unit_name,
                            level_statu_name, "",
                            compliance_name, description,
                            compliance_task_frequency, statutory_date,
                            due_date, assignee_name, "", ""
                        ]
                        self.write_csv(None, csv_values)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)
                self.FILE_DOWNLOAD_PATH = None

def get_download_bulk_compliance_data(
    db, unit_id, domain_id, level_1_statutory_name, frequency_name,
    session_user, start_count, to_count
):
    condition = ""
    condition_val = []

    condition += "AND c.frequency_id in (2,3)"

    if level_1_statutory_name is not None:
        condition += " AND statutory_mapping like %s"
        condition_val.append("%" + str(level_1_statutory_name + "%"))

    query = "SELECT ac.compliance_id, ac.statutory_dates, ac.due_date, " + \
        " assignee, employee_code, employee_name, " + \
        " SUBSTRING_INDEX(substring(substring(statutory_mapping,3),1, " + \
        " char_length(statutory_mapping) -4), '>>', 1) as statutory_mapping, " + \
        " document_name, compliance_task, compliance_description, " + \
        " c.repeats_type_id, rt.repeat_type, c.repeats_every, frequency, " + \
        " c.frequency_id FROM tbl_assign_compliances ac " + \
        " INNER JOIN tbl_users u ON (ac.assignee = u.user_id) " + \
        " INNER JOIN tbl_compliances c ON " + \
        " (ac.compliance_id = c.compliance_id) " + \
        " INNER JOIN tbl_compliance_frequency f " + \
        " ON (c.frequency_id = f.frequency_id) " + \
        " INNER JOIN tbl_compliance_repeat_type rt " + \
        " ON (c.repeats_type_id = rt.repeat_type_id) " + \
        " WHERE ac.is_active = 1 " + \
        " AND c.domain_id = %s AND ac.unit_id = %s "
    param = [
        domain_id, unit_id
    ]
    if condition != "":
        query += condition
        param.extend(condition_val)

    rows = db.select_all(query, param)

    level_1_statutory_wise_compliances = {}
    total_count = 0
    compliance_count = 0
    for compliance in rows:
        # statutories = compliance["statutory_mapping"].split(">>")

        # s_maps = json.loads(compliance["statutory_mapping"])
        # statutories = s_maps[0]
        s_maps = compliance["statutory_mapping"]
        statutories = s_maps

        # if level_1_statutory_name is None or level_1_statutory_name == "" :
        level_1 = statutories
        # else:
            # level_1 = level_1_statutory_name

        if level_1 not in level_1_statutory_wise_compliances:
            level_1_statutory_wise_compliances[level_1] = []

        compliance_name = compliance["compliance_task"]
        if compliance["document_name"] not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                compliance["document_name"], compliance_name
            )
        employee_code = compliance["employee_code"]
        if employee_code is None:
            employee_code = "Administrator"
        assingee_name = "%s - %s" % (
            employee_code, compliance["employee_name"]
        )
        due_dates = []
        summary = ""

        if compliance["repeats_type_id"] == 1:  # Days
            due_dates, summary = calculate_due_date(
                db,
                repeat_by=1,
                repeat_every=compliance["repeats_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id
            )
        elif compliance["repeats_type_id"] == 2:  # Months
            due_dates, summary = calculate_due_date(
                db,
                statutory_dates=compliance["statutory_dates"],
                repeat_by=2,
                repeat_every=compliance["repeats_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id
            )
        elif compliance["repeats_type_id"] == 3:  # years
            due_dates, summary = calculate_due_date(
                db,
                repeat_by=3,
                statutory_dates=compliance["statutory_dates"],
                repeat_every=compliance["repeats_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id
            )

        final_due_dates = filter_out_due_dates(
            db, unit_id, compliance["compliance_id"], due_dates
        )
        total_count += len(final_due_dates)

        for due_date in final_due_dates:
            if (
                int(start_count) <= compliance_count and
                compliance_count < (int(start_count)+to_count)
            ):
                due_date_parts = due_date.replace("'", "").split("-")
                year = due_date_parts[0]
                month = due_date_parts[1]
                day = due_date_parts[2]
                due_date = datetime.date(int(year), int(month), int(day))

                statutories_strip = statutories[0].strip()

                print "get_download_bulk_compliance_data>due_date>>", due_date
                print "datetime_to_string(due_date)>>", datetime_to_string(due_date)

                level_1_statutory_wise_compliances[level_1].append(
                    clienttransactions.UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(
                        compliance["compliance_id"], compliance_name,
                        compliance["compliance_description"],
                        clientcore.COMPLIANCE_FREQUENCY(compliance["frequency"]),
                        summary, datetime_to_string(due_date),
                        assingee_name, compliance["assignee"]
                    )
                )
                compliance_count += 1
            elif compliance_count > (int(start_count)+to_count):
                break
            else:
                compliance_count += 1
                continue

    statutory_wise_compliances = []
    for (level_1_statutory_name, compliances) in level_1_statutory_wise_compliances.iteritems():
        print "len(compliances)-->", len(compliances)
        if len(compliances) > 0:
            statutory_wise_compliances.append(
                clienttransactions.STATUTORY_WISE_COMPLIANCES_BU(
                    level_1_statutory_name, compliances
                )
            )
    # print [STATUTORY_WISE_COMPLIANCES.level_1_statutory_name for STATUTORY_WISE_COMPLIANCES in statutory_wise_compliances]
    # print [STATUTORY_WISE_COMPLIANCES.compliances for STATUTORY_WISE_COMPLIANCES in statutory_wise_compliances]
    print statutory_wise_compliances
    print "Total-> ", total_count
    return statutory_wise_compliances, total_count
