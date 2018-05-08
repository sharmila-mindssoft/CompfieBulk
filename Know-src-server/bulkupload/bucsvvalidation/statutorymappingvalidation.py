import os
import json
import traceback
import collections
import mysql.connector
import urllib
import threading
import requests
import calendar
from zipfile import ZipFile
from itertools import groupby
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    KNOWLEDGE_FORMAT_PATH
)

from ..bulkconstants import (
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH, TEMP_FILE_SERVER,
    BULK_UPLOAD_DB_HOST, BULK_UPLOAD_DB_PORT, BULK_UPLOAD_DB_USERNAME,
    BULK_UPLOAD_DB_PASSWORD, BULK_UPLOAD_DATABASE_NAME
)
from server.common import (
    get_date_time
)
from server.database.forms import (
    frmStatutoryMappingBulkUpload,
    frmApproveStatutoryMappingBulkUpload
)

from server.exceptionmessage import process_error
from server.database.knowledgetransaction import save_messages
from keyvalidationsettings import (
    csv_params, parse_csv_dictionary_values, is_numeric
)
from ..bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)

__all__ = [
    "ValidateStatutoryMappingCsvData",
    "ValidateStatutoryMappingForApprove"
]

################################
'''
    SourceDB: This class methods executed with main db connection
    also check csv data validation
'''
################################


class StatutorySource(object):

    def __init__(self):
        self._source_db = None
        self._source_db_con = None
        self.Compliance_Frequency = {}
        self.Repeats_Type = {}
        self.Duration_Type = {}
        self.Organization = {}
        self.Statutory_Nature = {}
        self.Geographies = {}
        self.Statutories = {}
        self.Statu_dic = {}
        self.Task_Type = []
        self.Statu_level = {}
        self.StatuLevelPosition = {}
        self.connect_source_db()
        self._check_method_maps = {}
        self.statusCheckMethods()
        self._csv_column_name = []
        self._csv_column_name_with_mandatory = []
        self.csv_column_fields()

    def csv_column_fields(self):
        self._csv_column_name = [
            "Organization", "Applicable_Location",
            "Statutory_Nature", "Statutory", "Statutory_Provision",
            "Compliance_Task", "Compliance_Document", "Task_ID",
            "Compliance_Description", "Penal_Consequences",
            "Task_Type", "Reference_Link",
            "Compliance_Frequency", "Statutory_Month",
            "Statutory_Date", "Trigger_Days", "Repeats_Every",
            "Repeats_Type", "Repeats_By (DOM/EOM)", "Duration",
            "Duration_Type",
            "Multiple_Input_Section", "Format"
        ]
        self._csv_column_name_with_mandatory = [
            "Organization*", "Applicable_Location*",
            "Statutory_Nature*", "Statutory*", "Statutory_Provision*",
            "Compliance_Task*", "Compliance_Document", "Task_ID*",
            "Compliance_Description*", "Penal_Consequences",
            "Task_Type*", "Reference_Link",
            "Compliance_Frequency*", "Statutory_Month",
            "Statutory_Date", "Trigger_Days", "Repeats_Every",
            "Repeats_Type", "Repeats_By (DOM/EOM)", "Duration",
            "Duration_Type",
            "Multiple_Input_Section", "Format"
        ]

    def connect_source_db(self):
        self._source_db_con = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME,
            password=KNOWLEDGE_DB_PASSWORD,
            host=KNOWLEDGE_DB_HOST,
            database=KNOWLEDGE_DATABASE_NAME,
            port=KNOWLEDGE_DB_PORT,
            autocommit=False,
        )
        self._source_db = Database(self._source_db_con)
        self._source_db.begin()

    def close_source_db(self):
        self._source_db.close()
        self.__source_db_con.close()

    def init_values(self, country_id, domain_id):
        self.get_compliance_frequency()
        self.get_compliance_repeat_type()
        self.get_compliance_duration_type()
        self.get_organization(country_id, domain_id)
        self.get_statutory_nature(country_id)
        self.get_grographies(country_id)
        self.get_statutories(country_id, domain_id)
        self.get_task_type()
        self.get_statutory_levels(country_id, domain_id)
        self.get_level_position(country_id, domain_id)

    def get_compliance_frequency(self):
        data = self._source_db.call_proc("sp_bu_compliance_frequency")
        for d in data:
            self.Compliance_Frequency[d["frequency"]] = d["frequency_id"]

    def get_compliance_repeat_type(self):
        data = self._source_db.call_proc("sp_bu_compliance_repeat_type")
        for d in data:
            self.Repeats_Type[d["repeat_type"]] = d["repeat_type_id"]

    def get_compliance_duration_type(self):
        data = self._source_db.call_proc("sp_bu_compliance_duration_type")
        for d in data:
            self.Duration_Type[d["duration_type"]] = d["duration_type_id"]

    def get_organization(self, country_id, domain_id):
        data = self._source_db.call_proc("sp_bu_organization", [
            country_id, domain_id
        ])
        for d in data:
            self.Organization[d["organisation_name"]] = d

    def get_statutory_nature(self, country_id):
        data = self._source_db.call_proc("sp_bu_statutory_nature", [
            country_id
        ])
        for d in data:
            self.Statutory_Nature[d["statutory_nature_name"]] = d

    def get_grographies(self, country_id):
        data = self._source_db.call_proc("sp_bu_geographies", [country_id])
        for d in data:
            self.Geographies[d["parent_names"]] = d

    def get_statutories(self, country_id, domain_id):
        data = self._source_db.call_proc("sp_bu_statutories", [
            country_id, domain_id
        ])
        for d in data:
            if d["parent_names"] != "":
                self.Statutories[
                    d["parent_names"] + '>>' + d["statutory_name"]
                ] = d
            else:
                self.Statutories[d["statutory_name"]] = d

    def get_statutory_levels(self, country_id, domain_id):
        data = self._source_db.call_proc("sp_bu_statutory_level", [
            country_id, domain_id
        ])
        for d in data:
            self.Statu_level[d["statu_level"]] = d

    def get_task_type(self):
        self.Task_Type = ["Register", "Notice"]

    def get_level_position(self, country_id, domain_id):
        data = self._source_db.call_proc("sp_bu_get_levelposition", [
            country_id, domain_id
        ])
        for d in data:
            self.StatuLevelPosition[d["statu_level"]] = d["level_id"]

    def check_base(self, check_status, store, key_name):
        data = None
        key_name = key_name.strip()
        if type(store) is list:
            if key_name in store:
                data = key_name
        else:
            data = store.get(key_name)

        if data is None:
            return "Not found"

        if check_status is True:
            if data.get("is_active") == 0:
                return "Status Inactive"

        return True

    def check_organization(self, organization_name):
        return self.check_base(True, self.Organization, organization_name)

    def check_statutory_nature(self, nature):
        return self.check_base(True, self.Statutory_Nature, nature)

    def check_geography(self, geo_names):
        return self.check_base(True, self.Geographies, geo_names)

    def check_frequency(self, frequency):
        return self.check_base(False, self.Compliance_Frequency, frequency)

    def check_repeat_type(self, rType):
        return self.check_base(False, self.Repeats_Type, rType)

    def check_duration_type(self, dType):
        return self.check_base(False, self.Duration_Type, dType)

    def check_statutory(self, statutory):
        return self.check_base(False, self.Statutories, statutory)

    def check_statutory_level(self, statu_level):
        for k in self.Statu_level.keys():
            if k < len(statu_level.split(" >> ")):
                print "Statutory level not found"
                return "Invalid Level"
        return True

    def check_task_type(self, tType):
        return self.check_base(False, self.Task_Type, tType)

    def check_single_input(self, d):
        msg = []
        keys = ["Statutory_Month", "Statutory_Date", "Trigger_Days"]
        for k in keys:
            if CSV_DELIMITER in d[k]:
                msg.append("%s - %s" % (k, "Invalid data"))
        return msg

    def check_multiple_input(self, d, keys):
        msg = []

        diff = 12 / int(d["Repeats_Every"])
        for k in keys:
            if len(d[k].strip().split(CSV_DELIMITER)) != diff:
                msg.append("%s - %s" % (
                    k, "Invalid data for multiple input section"
                ))
        return msg

    def check_empty_for_compliance_frequency(self, d, keys):
        msg = []
        for k in keys:
            if d[k] != "":
                msg.append(
                    "%s - Invalid Data" % (k)
                    # "%s - Invalid Compliance Frequency" % (k)
                )
        return msg

    def check_one_time(self, d):
        msg = self.check_single_input(d)

        keys = [
            "Repeats_Type", "Repeats_Every", "Repeats_By (DOM/EOM)",
            "Duration", "Duration_Type", "Multiple_Input_Section"
        ]
        invalid = self.check_empty_for_compliance_frequency(d, keys)
        msg.extend(invalid)

        return msg

    def check_on_occurrence(self, d):
        msg = []
        if (
            d["Compliance_Frequency"] == "On Occurrence" and
            d["Duration"] == ""
        ):
            msg.append("Duration - Field is blank")
        else:
            if not is_numeric(d["Duration"]):
                return msg

        if (
            d["Compliance_Frequency"] == "On Occurrence" and
            d["Duration_Type"] == ""
        ):
            msg.append("Duration_Type - Field is blank")

        if d["Duration"] != '' and int(d["Duration"]) > 999:
            msg.append("Duration - cannot exceed maximum 3 digits")

        keys = [
            "Statutory_Month", "Statutory_Date", "Trigger_Days",
            "Repeats_Type", "Repeats_Every", "Repeats_By (DOM/EOM)",
            "Multiple_Input_Section"
        ]
        msg.extend(self.check_empty_for_compliance_frequency(d, keys))
        return msg

    def check_periodical_and_Review(self, d):
        msg = []
        keys = [
            "Duration_Type", "Duration"
        ]
        msg.extend(self.check_empty_for_compliance_frequency(d, keys))

        if d["Repeats_Every"] == "":
            msg.append("Repeats_Every - Field is blank")
        else:
            print "isnumber ----> ", is_numeric(d["Repeats_Every"])
            if not is_numeric(d["Repeats_Every"]):
                return msg

        if d["Repeats_Type"] == "":
            msg.append("Repeats_Type - Field is blank")

        if (
            d["Multiple_Input_Section"] == "No" or
            d["Multiple_Input_Section"] == ""
        ):
            msg.extend(self.check_single_input(d))
            if d["Repeats_Type"] == "Month(s)":
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 99:
                    msg.append(
                        "Repeats_Every - Cannot exceed maximum 2 digits")
                if d["Repeats_By (DOM/EOM)"] == "":
                    msg.append("Repeats_By (DOM/EOM) - Field is blank")
                if d["Statutory_Month"] != "":
                    if "Statutory_Month - Invalid data" not in msg:
                        msg.append("Statutory_Month - Invalid data")
                if (
                    d["Repeats_By (DOM/EOM)"] == "EOM" and
                    d["Statutory_Date"] != ""
                ):
                    msg.append("Statutory_Date - Invalid data")

            elif d["Repeats_Type"] == "Year(s)":
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 9:
                    msg.append("Repeats_Every - Cannot exceed maximum 1 digit")
                if d["Repeats_By (DOM/EOM)"] == "":
                    msg.append("Repeats_By (DOM/EOM) - Field is blank")
                # if (
                #     d["Multiple_Input_Section"] == "No"
                # ):
                #     msg.append("Statutory_Date - Invalid data")
                if (
                    d["Repeats_By (DOM/EOM)"] == "EOM" and
                    d["Statutory_Date"] != ""
                ):
                    msg.append("Statutory_Date - Invalid data")

            elif d["Repeats_Type"] == "Day(s)":
                if d["Multiple_Input_Section"] != "":
                    msg.append("Multiple_Input_Section - Invalid data")
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 999:
                    msg.append(
                        "Repeats_Every - Cannot exceed maximum 3 digits")
                if d["Repeats_By (DOM/EOM)"] != "":
                    msg.append("Repeats_By (DOM/EOM) - Invalid data")
                if d["Statutory_Month"] != "":
                    msg.append("Statutory_Month - Invalid data")
                if d["Statutory_Date"] != "":
                    msg.append("Statutory_Date - Invalid data")
                if d["Repeats_Every"] < d["Trigger_Days"]:
                    msg.append(
                        "Trigger_Days - cannot be greater than Repeat"
                        " every days")

        elif (
            d["Multiple_Input_Section"] == "Yes" and
            d["Repeats_Type"] == "Month(s)"
        ):

            if d["Repeats_Every"] == "":
                msg.append("Repeats_Every - Field is blank")
            elif d["Repeats_Every"] != "" and int(d["Repeats_Every"]) not in [
                1, 2, 3, 4, 6
            ]:
                msg.append(
                    "Repeats_Every - Invalid data for multiple input section"
                )

            if d["Repeats_By (DOM/EOM)"] == "DOM" and d["Repeats_Every"] != "":
                keys = ["Statutory_Month", "Statutory_Date", "Trigger_Days"]
                msg.extend(self.check_multiple_input(d, keys))

            if d["Repeats_By (DOM/EOM)"] == "EOM" and d["Repeats_Every"] != "":
                keys = ["Statutory_Month", "Trigger_Days"]
                msg.extend(self.check_multiple_input(d, keys))
                if d["Statutory_Date"] != "":
                    msg.append("Statutory_Date - Invalid data")

        else:
            msg.append("Multiple_Input_Section - Invalid data")

        return msg

    def check_flexi_review(self, d):
        msg = []
        keys = [
            "Duration_Type", "Duration"
        ]
        msg.extend(self.check_empty_for_compliance_frequency(d, keys))
        if d["Repeats_Every"] != "":
            print "isnumber Flexi review----> ", is_numeric(d["Repeats_Every"])
            if not is_numeric(d["Repeats_Every"]):
                return msg
        if (
            d["Multiple_Input_Section"] == "No" or
            d["Multiple_Input_Section"] == ""
        ):
            # msg.extend(self.check_single_input(d))

            if d["Repeats_Type"] == "Month(s)":
                if d["Repeats_Every"] == '':
                    msg.append("Repeats_Every - Field is blank")
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 99:
                    msg.append("Repeats_Every - Cannot exceed maximum "
                               "2 digits")
                if d["Repeats_By (DOM/EOM)"] == "":
                    msg.append("Repeats_By (DOM/EOM)- Field is blank")
                if d["Statutory_Month"] != "":
                    msg.append("Statutory_Month - Invalid data")
                if (
                    d["Repeats_By (DOM/EOM)"] == "EOM" and
                    d["Statutory_Date"] != ""
                ):
                    msg.append("Statutory_Date - Invalid data")

            elif d["Repeats_Type"] == "Year(s)":
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 9:
                    msg.append("Repeats_Every - Cannot exceed "
                               "maximum 1 digits")
                if d["Repeats_By (DOM/EOM)"] == "":
                    msg.append("Repeats_By (DOM/EOM)- Field is blank")
                if (
                    d["Repeats_By (DOM/EOM)"] == "EOM" and
                    d["Statutory_Date"] != ""
                ):
                    msg.append("Statutory_Date - Invalid data")

            elif d["Repeats_Type"] == "Day(s)":
                if d["Multiple_Input_Section"] != "":
                    msg.append("Multiple_Input_Section - Invalid data")
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 999:
                    msg.append(
                        "Repeats_Every - Cannot exceed maximum 2 digits"
                    )
                if d["Repeats_By (DOM/EOM)"] != "":
                    msg.append("Repeats_By (DOM/EOM)- Invalid data")
                if d["Statutory_Month"] != "":
                    msg.append("Statutory_Month - Invalid data")
                if d["Statutory_Date"] != "":
                    msg.append("Statutory_Date - Invalid data")
                if d["Repeats_Every"] < d["Trigger_Days"]:
                    msg.append("Trigger_Days - cannot be greater than "
                               "Repeat every days")

            # Added for BUC588
            if (
                d["Repeats_Type"] == "" and
                d["Repeats_Every"] == "" and
                d["Repeats_By (DOM/EOM)"] == ""
            ):
                if(d["Statutory_Date"] != ""):
                    msg.append("Statutory_Date - Invalid data")
                if d["Statutory_Month"] != "":
                    msg.append("Statutory_Month - Invalid data")
                if d["Trigger_Days"] != "":
                    msg.append("Trigger_Days - Invalid data")

        elif (
            d["Multiple_Input_Section"] == "Yes" and
            d["Repeats_Type"] == "Month(s)"
        ):

            if d["Repeats_Every"] == "":
                msg.append("Repeats_Every - Field is blank")
            if (
                d["Repeats_Every"] != '' and
                int(d["Repeats_Every"]) not in [1, 2, 3, 4, 6]
            ):
                msg.append(
                    "Repeats_Every - Invalid data for multiple input section"
                )

            if d["Repeats_By (DOM/EOM)"] == "DOM" and d["Repeats_Every"] != "":
                keys = ["Statutory_Month", "Statutory_Date", "Trigger_Days"]
                msg.extend(self.check_multiple_input(d, keys))

            if d["Repeats_By (DOM/EOM)"] == "EOM" and d["Repeats_Every"] != "":
                keys = ["Statutory_Month", "Trigger_Days"]
                msg.extend(self.check_multiple_input(d, keys))
                if d["Statutory_Date"] != "":
                    msg.append("Statutory_Date - Invalid data")

        else:
            msg.append("Multiple_Input_Section - Invalid data")

        return msg

    def check_format_file_name(self, d):
        msg = []
        if (d["Compliance_Document"] != "" and d["Format"] == ""):
            msg.append(
                "Format - Field is blank when Compliance_Document available"
            )
        return msg

    def check_compliance_doc_name(self, d):
        msg = []
        if (d["Compliance_Document"] == "" and d["Format"] != ""):
            msg.append(
                "Compliance_Document - Field is blank when Format available"
            )
        return msg

    def check_primary_legislation_value(self, value):
        msg = []
        values = value.strip().split(CSV_DELIMITER)
        pri_leg_list = []
        for v in [v.strip() for v in values]:
            if v.find(">>") > 0:
                e = [e.strip() for e in v.split(">>")]
                pri_leg_list.append(e[0])
        print "pri_leg_list--->> ", pri_leg_list
        print all(pri_leg_list[0] == item for item in pri_leg_list)
        is_pl_equal = all(pri_leg_list[0] == item for item in pri_leg_list)
        if is_pl_equal is False:
            msg.append(
                "Statutory - Invalid Level One Data"
            )
        return msg

    # main db related validation mapped with field name
    def statusCheckMethods(self):
        self._check_method_maps = {
            "Organization": self.check_organization,
            "Applicable_Location": self.check_geography,
            "Statutory_Nature": self.check_statutory_nature,
            # "Statutory": self.check_statutory,
            "Statutory": self.check_statutory_level,
            "Compliance_Frequency": self.check_frequency,
            "Repeats_Type": self.check_repeat_type,
            "Duration_Type": self.check_duration_type,
            # "Task_Type": self.check_task_type,
        }

    def check_compliance_task_name_duplicate(
        self, country_id, domain_id, statutory,
        statutory_provision, task_name
    ):
        statutories = statutory.split(CSV_DELIMITER)
        statutory_string = str("[\"" + (',').join(statutories) + "\"]")

        data = self._source_db.call_proc(
            "sp_bu_check_duplicate_compliance", [
                country_id, domain_id, statutory_provision, task_name,
                statutory_string
            ]
        )
        if len(data) > 0:
            return False
        else:
            return True

    def check_task_id_duplicate(
        self, country_id, domain_id, statutory,
        statutory_provision, task_name, task_id
    ):
        statutories = statutory.split(CSV_DELIMITER)
        statutory_string = str("[\"" + (',').join(statutories) + "\"]")

        data = self._source_db.call_proc(
            "sp_bu_check_duplicate_task_id", [
                country_id, domain_id, statutory_provision, task_name,
                statutory_string, task_id
            ]
        )
        if len(data) > 0:
            return False
        else:
            return True

    def save_mapping_data(self, c_id, d_id, n_id, uploadedby, mapping):
        created_on = get_date_time()
        mapping = mapping.replace("u'", '"')
        mapping = mapping.replace("'", '"')
        mapping_value = [
            int(c_id), int(d_id),
            int(n_id), 1, 2,
            int(uploadedby), str(created_on), mapping
        ]
        q = "INSERT INTO tbl_statutory_mappings (country_id, domain_id, " + \
            " statutory_nature_id, is_active, is_approved, created_by, " + \
            " created_on, statutory_mapping) values " + \
            " (%s, %s, %s, %s, %s, %s, %s, %s)"
        statutory_mapping_id = self._source_db.execute_insert(
            q, mapping_value
        )
        if statutory_mapping_id is False:
            raise process_error("E018")
        return statutory_mapping_id

    def map_statutory_date(self, s_date, s_month, t_days, r_by):
        if r_by == "EOM":
            r_by = 2
        elif r_by == "DOM":
            r_by = 1
        else:
            r_by = None

        multi_len = 0
        if len(s_date.split(CSV_DELIMITER)) > 1:
            multi_len = len(s_date.split(CSV_DELIMITER))

        if (len(s_date.split(CSV_DELIMITER)) <= 1 and
                len(s_month.split(CSV_DELIMITER)) > 1):
            multi_len = len(s_month.split(CSV_DELIMITER))

        if(len(s_date.split(CSV_DELIMITER)) <= 1 and
            len(s_month.split(CSV_DELIMITER)) <= 1 and
                len(t_days.split(CSV_DELIMITER)) > 1):
            multi_len = len(t_days.split(CSV_DELIMITER))

        sdate = []
        if multi_len == 0:
            if(s_date is not None and s_date != ''):
                s_date = int(s_date)
            else:
                s_date = None

            if(s_month is not None and s_month != ''):
                s_month = int(s_month)
            else:
                s_month = None

            if(t_days is not None and t_days != ''):
                t_days = int(t_days)
            else:
                t_days = None

            if(r_by is not None and r_by == 2 and s_month is not None):
                end_of_month = calendar.mdays[s_month]
                s_date = int(end_of_month)

            sdate.append({
                "statutory_date": s_date,
                "statutory_month": s_month,
                "trigger_before_days": t_days,
                "repeat_by": r_by
            })
        else:
            s_date = s_date.split(CSV_DELIMITER)
            s_month = s_month.split(CSV_DELIMITER)
            t_days = t_days.split(CSV_DELIMITER)
            for i in range(multi_len):
                s_date_i = None
                s_month_i = None
                t_days_i = None

                if(type(s_date) != int or type(s_date) != float):
                    if(len(s_date) > 1):
                        s_date_i = int(s_date[i])

                if(type(s_month) != int or type(s_month) != float):
                    if(len(s_month) > 1):
                        s_month_i = int(s_month[i])

                if(type(t_days) != int or type(t_days) != float):
                    if(len(t_days) > 1):
                        t_days_i = int(t_days[i])
                if(r_by is not None and r_by == 2):
                    end_of_month = calendar.mdays[s_month_i]
                    s_date_i = int(end_of_month)

                sdate.append({
                    "statutory_date": s_date_i,
                    "statutory_month": s_month_i,
                    "trigger_before_days": t_days_i,
                    "repeat_by": r_by
                })
        return json.dumps(sdate)

    # write update query
    def save_compliance_data(self, c_id, d_id, mapping_id, data):
        created_on = get_date_time()
        approved_on = get_date_time()
        approved_by = self._session_user_obj.user_id()
        columns = [
            "statutory_provision",
            "compliance_task", "compliance_description",
            "document_name", "format_file", "format_file_size",
            "penal_consequences", "reference_link", "frequency_id",
            "statutory_dates", "statutory_mapping_id",
            "is_active", "created_by", "created_on",
            "domain_id", "country_id", "is_approved",
            "duration", "duration_type_id", "repeats_every", "repeats_type_id",
            "task_id", "task_type", "approved_by", "approved_on", "remarks"
        ]
        values = []

        for idx, d in enumerate(data):

            freq_id = self.Compliance_Frequency.get(d["Compliance_Frequency"])
            duration_type_id = None
            if d["Duration_Type"] != '':
                duration_type_id = self.Duration_Type.get(d["Duration_Type"])

            repeat_type_id = None
            if d["Repeats_Type"] != '':
                repeat_type_id = self.Repeats_Type.get(d["Repeats_Type"])

            Statutory_Date = d["Statutory_Date"] if d["Statutory_Date"] is not None else None
            Statutory_Month = d["Statutory_Month"] if d["Statutory_Month"] is not None else None
            Trigger_Days = d["Trigger_Days"] if d["Trigger_Days"] is not None else None
            Repeats_By = d["Repeats_By (DOM/EOM)"] if d["Repeats_By (DOM/EOM)"] is not None else None

            mapped_date = self.map_statutory_date(Statutory_Date,
                                                  Statutory_Month,
                                                  Trigger_Days,
                                                  Repeats_By)

            values.append((
                d["Statutory_Provision"], d["Compliance_Task"],
                d["Compliance_Description"], d["Compliance_Document"],
                d["Format"], d["format_file_size"],
                d["Penal_Consequences"], d["Reference_Link"], freq_id,
                mapped_date, int(mapping_id), 1, d["uploaded_by"],
                created_on, d_id, c_id, 2,
                None if d["Duration"] == '' else d["Duration"],
                duration_type_id,
                None if d["Repeats_Every"] == '' else d["Repeats_Every"],
                repeat_type_id,
                d["Task_ID"], d["Task_Type"], approved_by,
                approved_on, d["remarks"]
            ))

        if values:
            self._source_db.bulk_insert("tbl_compliances", columns, values)
            return True
        else:
            return False

    def save_industries(self, mapping_id, uploaded_by, orgids):
        columns = ["statutory_mapping_id", "organisation_id", "assigned_by"]
        values = []
        for d in orgids:
            values.append((mapping_id, d, uploaded_by))
        if values:
            self._source_db.bulk_insert(
                "tbl_mapped_industries", columns, values
            )

    def save_statutories(self, mapping_id, uploaded_by, statu_ids):
        columns = ["statutory_mapping_id", "statutory_id", "assigned_by"]
        values = []
        for d in statu_ids:
            values.append((mapping_id, d, uploaded_by))
        if values:
            self._source_db.bulk_insert(
                "tbl_mapped_statutories", columns, values
            )

    def save_statutories_data(self, statu_name, statu_level,
                              parent_id, parent_names, created_by):
        created_on = get_date_time()
        mapping_value = [
            statu_name, int(statu_level), parent_id, parent_names, created_on,
            created_by
        ]
        q = "INSERT INTO tbl_statutories (statutory_name, level_id, " + \
            " parent_ids, parent_names, created_on, created_by)" + \
            "values " + \
            " (%s, %s, %s, %s, %s, %s)"
        statutory_mapping_id = self._source_db.execute_insert(
            q, mapping_value
        )
        return statutory_mapping_id
        # if values:
        #     statu_id = self._source_db.execute_insert(
        #         "tbl_statutories", columns, values
        #     )
        #     return statu_id

    def save_geograhy_location(self, mapping_id, uploaded_by, geo_ids):
        columns = ["statutory_mapping_id", "geography_id", "assigned_by"]
        values = []
        for d in geo_ids:
            values.append((mapping_id, d, uploaded_by))
        if values:
            self._source_db.bulk_insert(
                "tbl_mapped_locations", columns, values
            )

    def save_executive_message(
        self, actual_csv_name, countryname, domainname, createdby
    ):
        csv_name = actual_csv_name.split('_')
        csv_name = "_".join(csv_name[:-1])
        text = "Statutory mapping file %s of %s - %s uploaded for your %s" % (
            csv_name, countryname, domainname, 'approval'
        )
        link = "/knowledge/approve-statutory-mapping-bu"
        save_messages(
            self._source_db, 3, "Statutory Mapping Bulk Upload",
            text, link, createdby
        )

        action = "Statutory mapping csv file uploaded %s of %s - %s" % (
            csv_name, countryname, domainname
        )
        if csv_name and countryname and domainname:
            self._source_db.save_activity(
                createdby, frmStatutoryMappingBulkUpload, action
            )

    def save_manager_message(
        self, a_type, actual_csv_name, countryname, domainname,
        createdby, rejected_reason, sys_declined_count
    ):
        print "QQQQQQQQQQQQQQQQQQQQQQQQQQQ"
        print "sys_declined_count-->> ", sys_declined_count
        print "rejected_reason-> ", rejected_reason
        csv_name = actual_csv_name.split('_')
        csv_name = "_".join(csv_name[:-1])
        if a_type == 1:
            action_type = "approved"

        else:
            action_type = "rejected"

        if a_type == 1:
            text = "Statutory mapping file %s of %s - %s has been %s" % (
                csv_name, countryname, domainname, action_type
            )
            if sys_declined_count > 0:
                text = "Statutory mapping file %s of %s - %s %s "\
                    "records has been declined by COMPFIE" % \
                    (csv_name, countryname, domainname, sys_declined_count)
                print "In system reject ", text
        else:
            text = "Statutory mapping file %s of %s - %s "\
                "has been %s with Reason '%s'" % \
                (csv_name, countryname, domainname, action_type,
                 rejected_reason)

        link = "/knowledge/statutory-mapping-bu"
        save_messages(
            self._source_db, 4, "Approve Statutory Mapping Bulk Upload",
            text, link, createdby
        )

        action = "Statutory mapping file  %s of %s - %s has been %s" % (
            csv_name, countryname, domainname, action_type
        )
        if csv_name and countryname and domainname:
            self._source_db.save_activity(
                createdby, frmApproveStatutoryMappingBulkUpload, action
            )

    def source_commit(self):
        self._source_db.commit()


class ValidateStatutoryMappingCsvData(StatutorySource):

    def __init__(
        self, db, source_data, session_user,
        country_id, domain_id, csv_name, csv_header
    ):
        # super(SourceDB, self).__init__()
        StatutorySource.__init__(self)
        self._db = db
        self._source_data = source_data
        self._session_user_obj = session_user
        self._country_id = country_id
        self._domain_id = domain_id
        self._csv_name = csv_name
        self._csv_header = csv_header

        self._error_summary = {}
        self.errorSummary()

        self._doc_names = []
        self._sheet_name = "Statutory Mapping"

    # error summary mapped with initial count
    def errorSummary(self):
        self._error_summary = {
            "mandatory_error": 0,
            "max_length_error": 0,
            "duplicate_error": 0,
            "invalid_char_error": 0,
            "invalid_data_error": 0,
            "inactive_error": 0,
            "invalid_frequency_error": 0
        }

    def compare_csv_columns(self):
        print "self._csv_column_name->> ", self._csv_column_name
        print "self._csv_header--->", self._csv_header
        res = collections.Counter(
            self._csv_column_name
        ) == collections.Counter(self._csv_header)
        if res is False:
            return "InvalidCsvFile"
        return True

    def check_duplicate_in_csv(self):
        seen = set()
        duplicate_count = 0
        for d in self._source_data:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
            else:
                duplicate_count += 1
        return duplicate_count

        # if len(seen) != len(self._source_data):
        #     raise ValueError("Duplicate or empty data found in CSV")

    def check_duplicate_task_name_in_csv(self):
        self._source_data.sort(key=lambda x: (
            x["Statutory"], x["Statutory_Provision"], x["Compliance_Task"]
        ))
        duplicate_compliance = 0
        duplicate_compliance_row = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Statutory"], s["Statutory_Provision"], s["Compliance_Task"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1:
                # msg.append(grouped_list[0].get("Compliance_Task"))
                duplicate_compliance += len(grouped_list)
                duplicate_compliance_row.append([
                    grouped_list[0].get("Compliance_Task"),
                    grouped_list[0].get("Statutory"),
                    grouped_list[0].get("Statutory_Provision"),
                ])

        return duplicate_compliance, duplicate_compliance_row

        # if len(msg) > 0:
        #     error_msg = "Duplicate compliance task found in csv %s" % (
        #         ','.join(msg)
        #     )
        #     raise ValueError(str(error_msg))

    def check_duplicate_task_id_in_csv(self):
        self._source_data.sort(key=lambda x: (
            x["Statutory"], x["Statutory_Provision"],
            x["Compliance_Task"], x["Task_ID"]
        ))
        duplicate_task_ids = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Statutory"], s["Statutory_Provision"],
            s["Compliance_Task"], s["Task_ID"]
        )):
            print "K-->>> ", k
            print "V-->>> ", v
            grouped_list = list(v)
            print "grouped_list-> ", grouped_list[0].get("Task_ID")
            print "len(grouped_list)> ", len(grouped_list)
            if len(grouped_list) > 1:
                duplicate_task_ids.append(grouped_list[0].get("Task_ID"))

        return duplicate_task_ids
        # if len(msg) > 0:
        #     error_msg = "Duplicate task id found in csv %s" % (
        #         ','.join(msg)
        #     )
        #     raise ValueError(str(error_msg))

    def check_compliance_duplicate_in_tempDB(
        self, country_id, domain_id, statutory, statutory_provision,
        compliance_task
    ):
        data = self._db.call_proc("sp_check_duplicate_statu_mapping", [
            country_id, domain_id, statutory, statutory_provision,
            compliance_task
        ])
        if len(data) > 0:
            return False
        else:
            return True

    def check_duplicate_taskid_in_tempDB(
        self, country_id, domain_id, task_id
    ):
        data = self._db.call_proc("sp_check_duplicate_task_id", [
            country_id, domain_id, task_id
        ])
        if len(data) > 0:
            return False
        else:
            return True

    '''
        looped csv data to perform corresponding validation
        returns: valid and invalid return format
        rType: dictionary
    '''

    def perform_validation(self):
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        csv_compare = self.compare_csv_columns()
        if(csv_compare is not True):
            return "InvalidCSV"

        # duplicate_row_in_csv = self.check_duplicate_in_csv()
        # self._error_summary["duplicate_error"] += duplicate_row_in_csv
        duplicate = self.check_duplicate_task_name_in_csv()
        # duplicate_compliance_in_csv = duplicate[0]
        duplicate_compliance_row = duplicate[1]
        # self._error_summary["duplicate_error"] += duplicate_compliance_in_csv
        duplicate_task_ids = self.check_duplicate_task_id_in_csv()

        self.init_values(self._country_id, self._domain_id)

        def make_error_desc(res, msg):
            if res is True:
                res = []
            if res is not True:
                if type(msg) is list:
                    res.extend(msg)
                else:
                    res.append(msg)
            return res

        for row_idx, data in enumerate(self._source_data):
            res = True
            error_count = {"mandatory": 0, "max_length": 0, "invalid_char": 0}
            for key in self._csv_column_name:
                value = data.get(key)
                print "key->", key, " Values->", value
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)

                if (key == "Format" and value != ''):
                    self._doc_names.append(value)
                if key in ["Statutory_Nature", "Compliance_Frequency"]:
                    if CSV_DELIMITER in value:
                        msg = "%s - Invalid Data" % (key)
                        if res is not True:
                            res.append(msg)
                        else:
                            res = [msg]
                        error_count["invalid_char"] += 1

                for v in [v.strip() for v in values]:
                    valid_failed, error_cnt = parse_csv_dictionary_values(
                        key, v
                    )
                    # print "valid_failed----> ", valid_failed
                    if valid_failed is not True:
                        if res is True:
                            res = valid_failed
                            error_count = error_cnt
                        else:
                            res.extend(valid_failed)
                            error_count["mandatory"] += error_cnt[
                                "mandatory"
                            ]
                            error_count["max_length"] += error_cnt[
                                "max_length"
                            ]
                            error_count["invalid_char"] += error_cnt[
                                "invalid_char"
                            ]
                    if v != "":
                        if (
                            csvParam.get("check_is_exists") is True or
                            csvParam.get("check_is_active") is True
                        ):
                            unboundMethod = self._check_method_maps.get(
                                key
                            )
                            if key in ["Applicable_Location", "Statutory"]:
                                if v.find(">>") > 0:
                                    v = " >> ".join(
                                        e.strip() for e in v.split(">>")
                                    )

                            print "v-> ", v

                            if unboundMethod is not None:
                                isFound = unboundMethod(v)

                            # print "isFound-> ", isFound

                            if isFound is not True and isFound != "":
                                msg = "%s - %s %s" % (key, v, isFound)
                                # print msg
                                # print row_idx
                                if res is not True:
                                    res.append(msg)
                                else:
                                    res = [msg]
                                if "Status" in isFound:
                                    self._error_summary[
                                        "inactive_error"
                                    ] += 1
                                else:
                                    self._error_summary[
                                        "invalid_data_error"
                                    ] += 1
                            if (
                                isFound is not True and isFound != "" and
                                (key == "Compliance_Frequency" or
                                 key == "Repeats_Type" or
                                 key == "Duration_Type")
                            ):
                                self._error_summary[
                                    "invalid_frequency_error"] += 1

                if key == "Statutory":
                    msg = self.check_primary_legislation_value(value)
                    self._error_summary["invalid_data_error"] += len(msg)
                    if len(msg) > 0:
                        res = make_error_desc(res, msg)

                if key == "Task_ID":
                    if v in duplicate_task_ids:
                        dup_error = "Task_ID - Duplicate data"
                        self._error_summary["duplicate_error"] += 1
                        res = make_error_desc(res, dup_error)

                    if not self.check_duplicate_taskid_in_tempDB(
                        self._country_id, self._domain_id, data.get("Task_ID")
                    ):
                        self._error_summary["duplicate_error"] += 1
                        dup_error = "Task_ID - Duplicate in Temp DB"
                        res = make_error_desc(res, dup_error)

                    if not self.check_task_id_duplicate(
                        self._country_id, self._domain_id,
                        data.get("Statutory"),
                        data.get("Statutory_Provision"),
                        data.get("Compliance_Task"),
                        data.get("Task_ID")
                    ):
                        self._error_summary["duplicate_error"] += 1
                        dup_error = "Task_ID - Duplicate in Knowledge DB"
                        res = make_error_desc(res, dup_error)

                if key == "Compliance_Task":
                    for x in duplicate_compliance_row:
                        if (
                            x[0] == v and
                            x[1] == data.get("Statutory") and
                            x[2] == data.get("Statutory_Provision")
                        ):
                            dup_err = "Compliance_Task - Duplicate data"
                            self._error_summary["duplicate_error"] += 1
                            res = make_error_desc(res, dup_err)

                    if not self.check_compliance_duplicate_in_tempDB(
                        self._country_id, self._domain_id,
                        data.get("Statutory"), data.get("Statutory_Provision"),
                        data.get("Compliance_Task")
                    ):
                        self._error_summary["duplicate_error"] += 1
                        dup_error = "Compliance_Task - Duplicate " +\
                                    "Compliances in Temp DB"
                        res = make_error_desc(res, dup_error)

                    if not self.check_compliance_task_name_duplicate(
                        self._country_id, self._domain_id,
                        data.get("Statutory"),
                        data.get("Statutory_Provision"),
                        data.get("Compliance_Task")
                    ):
                        self._error_summary["duplicate_error"] += 1
                        dup_error = "Compliance_Task - Duplicate compliances in Knowledge DB"
                        res = make_error_desc(res, dup_error)

                if key == "Compliance_Frequency":
                    msg = []
                    if value == "One Time":
                        msg = self.check_one_time(data)

                    elif value == "On Occurrence":
                        msg = self.check_on_occurrence(data)

                    elif value in ["Periodical", "Review"]:
                        msg = self.check_periodical_and_Review(data)

                    else:
                        msg = self.check_flexi_review(data)

                    # print "Messge---> ", msg
                    self._error_summary["invalid_data_error"] += len(msg)
                    self._error_summary["invalid_frequency_error"] += len(msg)
                    if len(msg) > 0:
                        res = make_error_desc(res, msg)

                if key is "Compliance_Document":
                    msg = self.check_compliance_doc_name(data)
                    self._error_summary["mandatory_error"] += len(msg)
                    if len(msg) > 0:
                        res = make_error_desc(res, msg)
                if key is "Format":
                    msg = self.check_format_file_name(data)
                    self._error_summary["mandatory_error"] += len(msg)
                    if len(msg) > 0:
                        res = make_error_desc(res, msg)
                    if (
                        data["Compliance_Document"] != "" and
                        data["Format"] != ""
                    ):
                        file_extension = os.path.splitext(data["Format"])
                        allowed_file_formats = [".pdf", ".doc", ".docx",
                                                ".xls", ".xlsx"]
                        if file_extension[1] not in allowed_file_formats:
                            msg.append("Format - Invalid File Format")
                            self._error_summary["invalid_data_error"] += 1
                            res = make_error_desc(res, msg)
                print "RES ->> ", res
                if res is not True:
                    err_str = (',').join(res)
                    print "err_str--> ", err_str
                    if err_str.find(key + " - ") != -1:
                        head_idx = mapped_header_dict.get(key)
                        if head_idx is None:
                            head_idx = [row_idx]
                        else:
                            head_idx.append(row_idx)

                        mapped_header_dict[key] = head_idx
                # print "Header Dict-->", mapped_header_dict

                # if key == "Format" and res is True:
                    # if not self.check_compliance_task_name_duplicate(
                    #     self._country_id, self._domain_id,
                    #     data.get("Statutory"),
                    #     data.get("Statutory_Provision"),
                    #     data.get("Compliance_Task")
                    # ):
                    #     self._error_summary["duplicate_error"] += 1
                    #     dup_error = "Compliance_Task - Duplicate compliances in Knowledge DB"
                    #     res = make_error_desc(res, dup_error)

                    # if not self.check_task_id_duplicate(
                    #     self._country_id, self._domain_id,
                    #     data.get("Statutory"),
                    #     data.get("Statutory_Provision"),
                    #     data.get("Compliance_Task"),
                    #     data.get("Task_ID")
                    # ):
                    #     self._error_summary["duplicate_error"] += 1
                    #     dup_error = "Task_ID - Duplicate in Knowledge DB"
                    #     res = make_error_desc(res, dup_error)
            if res is not True:
                error_list = mapped_error_dict.get(row_idx)
                if error_list is None:
                    error_list = res
                else:
                    error_list.extend(res)

                mapped_error_dict[row_idx] = error_list
                invalid += 1
                self._error_summary["mandatory_error"] += error_count[
                    "mandatory"
                ]
                self._error_summary["max_length_error"] += error_count[
                    "max_length"
                ]
                self._error_summary["invalid_char_error"] += error_count[
                    "invalid_char"
                ]
                res = True

        print "Error dict-> ", mapped_error_dict
        print "\n"
        print "Header Dict-->", mapped_header_dict
        if invalid > 0:
            return self.make_invalid_return(
                mapped_error_dict, mapped_header_dict
            )
        else:
            return self.make_valid_return(
                mapped_error_dict, mapped_header_dict
            )

    def make_invalid_return(self, mapped_error_dict, mapped_header_dict):
        try:
            fileString = self._csv_name.split('.')
            file_name = "%s_%s.%s" % (
                fileString[0], "invalid", "xlsx"
            )
            final_hearder = self._csv_column_name_with_mandatory
            final_hearder.append("Error Description")
            write_data_to_excel(
                os.path.join(BULKUPLOAD_INVALID_PATH, "xlsx"),
                file_name, final_hearder,
                self._source_data, mapped_error_dict,
                mapped_header_dict, self._sheet_name
            )
            invalid = len(mapped_error_dict.keys())
            total = len(self._source_data)
            # make csv file
            rename_file_type(file_name, "csv")
            # make ods file
            rename_file_type(file_name, "ods")
            # make text file
            rename_file_type(file_name, "txt")
            return {
                "return_status": False,
                "invalid_file": file_name,
                "mandatory_error": self._error_summary["mandatory_error"],
                "max_length_error": self._error_summary["max_length_error"],
                "duplicate_error": self._error_summary["duplicate_error"],
                "invalid_char_error": self._error_summary[
                    "invalid_char_error"],
                "invalid_data_error": self._error_summary[
                    "invalid_data_error"],
                "inactive_error": self._error_summary["inactive_error"],
                "invalid_frequency_error": self._error_summary["invalid_frequency_error"],
                "total": total,
                "invalid": invalid,
                "doc_count": len(set(self._doc_names))
            }
        except Exception, e:
            print e
            print str(traceback.format_exc())

    def make_valid_return(self, mapped_error_dict, mapped_header_dict):
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)
        return {
            "return_status": True,
            "data": self._source_data,
            "total": total,
            "valid": total - invalid,
            "invalid": invalid,
            "doc_count": len(set(self._doc_names)),
            "doc_names": list(set(self._doc_names)),
            "csv_name": self._csv_name
        }


class ValidateStatutoryMappingForApprove(StatutorySource):

    def __init__(self, db, csv_id, country_id, domain_id, session_user):
        StatutorySource.__init__(self)
        self._db = db
        self._csv_id = csv_id
        self._country_id = country_id
        self._domain_id = domain_id
        self._session_user_obj = session_user
        self._source_data = None
        self._declined_row_idx = {}
        self._country_name = None
        self._domain_name = None
        self._csv_name = None
        self._doc_count = 0
        self.get_source_data()
        self.get_file_count()

    def connect_bulk_database(self):
        c_db_con = bulkupload_db_connect()
        self._db = Database(c_db_con)
        self._db.begin()

    def source_bulkdb_commit(self):
        self._db.commit()

    def get_source_data(self):
        print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.connect_bulk_database()
        self._source_data = self._db.call_proc(
            "sp_statutory_mapping_by_csvid", [self._csv_id]
        )
        print "len(self._source_data)->>>>>>>> ", len(self._source_data)
        if len(self._source_data) > 0:
            self._csv_name = self._source_data[0].get("csv_name")
            self._country_name = self._source_data[0].get("country_name")
            self._domain_name = self._source_data[0].get("domain_name")

    def get_file_count(self):
        data = self._db.call_proc("sp_sm_get_total_file_count", [self._csv_id])
        if len(data) > 0:
            self._doc_count = data[0].get("total_documents")

    def perform_validation_before_submit(self):
        try:
            declined_count = 0
            self._declined_row_idx = {}
            self.init_values(self._country_id, self._domain_id)

            for row_idx, data in enumerate(self._source_data):
                res = True
                declined_count = 0
                if row_idx == 0:
                    self._country_name = data.get("country_name")
                    self._domain_name = data.get("domain_name")
                    self._csv_name = data.get("csv_name")

                for key in self._csv_column_name:
                    value = data.get(key)
                    isFound = ""
                    if value is None:
                        continue

                    csvParam = csv_params.get(key)
                    if csvParam is None:
                        continue

                    if type(value) is not int:
                        values = value.strip().split(CSV_DELIMITER)

                        for v in [v.strip() for v in values]:
                            if type(v) is str:
                                v = v.strip()

                            if v != "":
                                if (
                                    csvParam.get("check_is_exists") is True or
                                    csvParam.get("check_is_active") is True
                                ):
                                    unboundMethod = self._check_method_maps.get(
                                        key
                                    )

                                    if key in ["Applicable_Location", "Statutory"]:
                                        if v.find(">>") > 0:
                                            v = " >> ".join(e.strip() for e in v.split(">>"))

                                    if unboundMethod is not None:
                                        isFound = unboundMethod(v)

                                if isFound is not True and isFound != "":
                                    declined_count += 1
                                    msg = "%s - %s %s" % (key, v, isFound)
                                    print "msg->>>", msg
                                    if res is not True:
                                        res.append(msg)
                                    else:
                                        print "msg-> in else -> ", msg
                                        res = [msg]
                                        print "RES in else-> ", res

                if not self.check_compliance_task_name_duplicate(
                    self._country_id, self._domain_id,
                    data.get("Statutory"),
                    data.get("Statutory_Provision"),
                    data.get("Compliance_Task")
                ):
                    declined_count += 1
                    dup_error = "Compliance_Task - Duplicate data"
                    if res is not True:
                        res.append(dup_error)
                    else:
                        res = [dup_error]

                if not self.check_task_id_duplicate(
                    self._country_id, self._domain_id,
                    data.get("Statutory"), data.get("Statutory_Provision"),
                    data.get("Compliance_Task"), data.get("Task_ID")
                ):
                    declined_count += 1
                    dup_error = "Task_ID - Duplicate data"
                    if res is not True:
                        res.append(dup_error)
                    else:
                        res = [dup_error]

                if declined_count > 0:
                    self._declined_row_idx[
                        data.get("bulk_statutory_mapping_id")
                    ] = res
                print "REsSULT In perform validation before submit-", res

            return self._declined_row_idx
        except Exception, e:
            print e
            print str(traceback.format_exc())

    def frame_data_for_main_db_insert(self):
        try:
            self.get_source_data()
            self._source_data.sort(key=lambda x: (
                 x["Organization"], x["Statutory_Nature"],
                 x["Statutory"], x["Applicable_Location"]
            ))
            msg = []
            statu_exists_id = []
            for k, v in groupby(self._source_data, key=lambda s: (
                s["Organization"], s["Statutory_Nature"],
                s["Statutory"], s["Applicable_Location"]
            )):
                grouped_list = list(v)
                if len(grouped_list) == 0:
                    continue
                org_ids = []
                statu_ids = []
                geo_ids = []
                nature_id = None
                statu_mapping = None
                value = grouped_list[0]
                for org in value.get(
                    "Organization"
                ).strip().split(CSV_DELIMITER):
                    org = org.strip()
                    org_info = self.Organization.get(org)
                    if org_info is not None:
                        org_ids.append(
                            org_info.get("organisation_id")
                        )

                nature = value.get("Statutory_Nature")
                nature_id = self.Statutory_Nature.get(
                    nature
                ).get("statutory_nature_id")

                for geo_maps in value.get("Applicable_Location").split(
                        CSV_DELIMITER):
                    geo_maps = geo_maps.lstrip()
                    geo_maps = geo_maps.rstrip()
                    if geo_maps.find(">>") > 0:
                        geo_maps = " >> ".join(
                            e.strip() for e in geo_maps.split(">>"))

                    if self.Geographies.get(geo_maps) is not None:
                        geo_ids.append(
                            self.Geographies.get(geo_maps).get(
                                "geography_id"
                            )
                        )

                if len(grouped_list) > 1:
                    msg.append(grouped_list[0].get("Compliance_Task"))
                uploaded_by = grouped_list[0].get("uploaded_by")
                statu_mapping = value.get("Statutory").split(CSV_DELIMITER)
                for statu_maps in statu_mapping:
                    statu_limit = [i for i in self.Statu_level]
                    statu_level_limit = statu_limit[0]

                    statu_maps = statu_maps.lstrip()
                    statu_maps = statu_maps.rstrip()
                    if statu_maps.find(">>") > 0:
                        statu_maps = ">>".join(
                            e.strip() for e in statu_maps.split(">>"))
                    legis_data = statu_maps.split(">>")
                    if self.Statutories.get(statu_maps) is not None:
                        if(len(legis_data) <= statu_level_limit):
                            statu_ids.append(
                                self.Statutories.get(statu_maps).get(
                                    "statutory_id"
                                )
                            )
                        statu_exists_id.append(statu_maps)
                    else:
                        if self.Statu_dic.get(statu_maps) is not None:
                            if(len(legis_data) <= statu_level_limit):
                                statu_ids.append(
                                    self.Statu_dic.get(statu_maps)
                                )
                                statu_exists_id.append(statu_maps)

                        if(len(legis_data) <= statu_level_limit):
                            parent_names = ''
                            parent_id = ''
                            for statu_level, data in enumerate(legis_data, 1):
                                strip_data = data.lstrip()
                                strip_data = strip_data.rstrip()
                                if strip_data.find(">>") > 0:
                                    strip_data = ">>".join(
                                        e.strip() for e in strip_data.split(
                                            ">>"))
                                statu_position = self.StatuLevelPosition
                                level_id = statu_position.get(statu_level)

                                if(self.Statu_dic.get(strip_data) is not None):
                                    parent_id = self.Statu_dic.get(strip_data)
                                    parent_names = str(strip_data)

                                if(
                                   self.Statutories.get(strip_data) is not None
                                   ):
                                    parent_id = self.Statutories.get(
                                        strip_data).get("statutory_id")
                                    parent_names = str(strip_data)

                                if (int(statu_level) == 1 and
                                   self.Statutories.get(strip_data) is None):
                                    if(strip_data not in statu_exists_id):
                                        statu_id = self.save_statutories_data(
                                            str(strip_data), level_id,
                                            parent_id, parent_names,
                                            uploaded_by)
                                        if(len(legis_data) == 1):
                                            statu_ids.append(statu_id)
                                        statu_exists_id.append(strip_data)
                                        self.Statu_dic[strip_data] = statu_id
                                        parent_id = statu_id
                                        parent_names = str(strip_data)
                                else:
                                    if(int(statu_level) > 1 and
                                       self.Statutories.get(statu_maps) is None
                                       ):
                                        if(self.Statu_dic.get(statu_maps) is None
                                           ):
                                            statu_id = self.save_statutories_data(
                                                str(strip_data), level_id,
                                                parent_id, parent_names,
                                                uploaded_by)
                                            statu_ids.append(statu_id)
                                            statu_exists_id.append(statu_maps)
                                            self.Statu_dic[statu_maps] = statu_id
                                            parent_id = statu_id
                                            parent_names = str(strip_data)
                                        if(
                                           self.Statu_dic.get(statu_maps) is not None
                                           and statu_maps not in statu_exists_id
                                           ):
                                            statu_id = self.Statu_dic.get(statu_maps)
                                            statu_ids.append(statu_id)
                                            statu_exists_id.append(statu_maps)
                                            self.Statu_dic[statu_maps] = statu_id
                mapping_id = self.save_mapping_data(
                    self._country_id, self._domain_id, nature_id,
                    uploaded_by, str(statu_mapping)
                )
                self.save_compliance_data(
                    self._country_id, self._domain_id,
                    mapping_id, grouped_list
                )
                self.save_industries(mapping_id, uploaded_by, org_ids)

                self.save_statutories(mapping_id, uploaded_by, statu_ids)

                self.save_geograhy_location(mapping_id, uploaded_by, geo_ids)

        except Exception, e:
            print str(traceback.format_exc())
            raise e

    def make_rejection(self, declined_info, user_id):
        try:
            count = len(declined_info.keys())
            created_on = get_date_time()
            print "declined Coun info > ", declined_info
            for k, v in declined_info.items():
                print "k, ", k
                print "V > ", v
                remarks = ",".join(v)
                q = "update tbl_bulk_statutory_mapping set " + \
                    " action = 3, remarks = %s where " + \
                    " bulk_statutory_mapping_id  = %s"
                self._db.execute(q, [
                    remarks, k
                ])

            # q1 = "update tbl_bulk_statutory_mapping_csv set " + \
            #     " declined_count = %s,  approve_status = 1 " +\
            #     " approved_by = %s, approved_on = %s where csv_id = %s"

            q1 = "update tbl_bulk_statutory_mapping_csv set " + \
                " declined_count = %s, approve_status = 1, " + \
                " approved_by = %s, approved_on = %s, " + \
                " total_rejected_records = (select count(0) from " + \
                " tbl_bulk_statutory_mapping as t WHERE t.action = 2 and " + \
                " t.csv_id = %s) WHERE " + \
                " csv_id = %s"
            self._db.execute(q1, [count, user_id, created_on, self._csv_id,
                             self._csv_id])

            print "Rejection done"
            self._db.commit()
            return True
        except Exception, e:
            print str(traceback.format_exc())
            raise (e)

    def format_download_process_initiate(self, csvid):
        self.file_server_approve_call(csvid)
        self._stop = False

        def check_status():
            if self._stop:
                return

            file_status = get_file_stats(csvid)
            print " file Status -> ", file_status
            if file_status == "completed":
                self._stop = True
                self.file_server_download_call(csvid)

            if self._stop is False:
                t = threading.Timer(60, check_status)
                t.daemon = True
                t.start()

        def get_file_stats(csvid):
            file_status = None
            c_db_con = bulkupload_db_connect()
            _db_check = Database(c_db_con)
            try:
                _db_check.begin()
                data = _db_check.call_proc(
                    "sp_sm_get_file_download_status", [csvid]
                )
                print "DAta -> ", data
                if len(data) > 0:
                    file_status = data[0].get("file_download_status")

            except Exception, e:
                print e
                _db_check.rollback()

            finally:
                _db_check.close()
                c_db_con.close()
            return file_status

        check_status()

    def file_server_approve_call(self, csvid):
        print "Approve call done"
        caller_name = "%sapprove?csvid=%s" % (TEMP_FILE_SERVER, csvid)
        print "caller_name", caller_name
        response = requests.post(caller_name)
        print "response.text-> ", response.text

    def file_server_download_call(self, csvid):
        actual_zip_file = os.path.join(
            KNOWLEDGE_FORMAT_PATH, str(csvid) + ".zip"
        )
        caller_name = "%sdownloadfile?csvid=%s" % (TEMP_FILE_SERVER, csvid)
        print "Cller nameeeeee", caller_name
        urllib.urlretrieve(caller_name, actual_zip_file)
        zip_ref = ZipFile(actual_zip_file, 'r')
        zip_ref.extractall(KNOWLEDGE_FORMAT_PATH)
        zip_ref.close()
        os.remove(actual_zip_file)
        self.file_server_remove_call(csvid)
        return True

    def file_server_remove_call(self, csvid):
        caller_name = "%sremovefile?csvid=%s" % (TEMP_FILE_SERVER, csvid)
        response = requests.post(caller_name)
        print response.text


def bulkupload_db_connect():
    cnx_pool = mysql.connector.connect(
        user=BULK_UPLOAD_DB_USERNAME,
        password=BULK_UPLOAD_DB_PASSWORD,
        host=BULK_UPLOAD_DB_HOST,
        database=BULK_UPLOAD_DATABASE_NAME,
        port=BULK_UPLOAD_DB_PORT,
        autocommit=False,
    )
    return cnx_pool
