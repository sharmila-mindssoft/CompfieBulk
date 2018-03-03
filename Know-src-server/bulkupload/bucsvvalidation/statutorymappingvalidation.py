import os
import collections
import mysql.connector
from itertools import groupby
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH
)
from server.common import (
    get_date_time
)
from server.exceptionmessage import process_error
from keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)

__all__ = [
    "ValidateStatutoryMappingCsvData",
    "ValidateStatutoryMappingForApprove"
]
################################
'''
    SourceDB : This class methods executed with main db connection
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
        self.Task_Type = []
        self.connect_source_db()
        self._validation_method_maps = {}
        self.statusCheckMethods()
        self._csv_column_name = []
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
            "Repeats_Type",  "Repeats_By (DOM/EOM)", "Duration", "Duration_Type",
            "Multiple_Input_Section",  "Format"
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

    def get_compliance_frequency(self):
        data = self._source_db.call_proc("sp_bu_compliance_frequency")
        for d in data :
            self.Compliance_Frequency[d["frequency"]] = d["frequency_id"]

    def get_compliance_repeat_type(self):
        data = self._source_db.call_proc("sp_bu_compliance_repeat_type")
        for d in data :
            self.Repeats_Type[d["repeat_type"]] = d["repeat_type_id"]

    def get_compliance_duration_type(self):
        data = self._source_db.call_proc("sp_bu_compliance_duration_type")
        for d in data :
            self.Duration_Type[d["duration_type"]] = d["duration_type_id"]

    def get_organization(self, country_id, domain_id):
        data = self._source_db.call_proc("sp_bu_organization", [country_id, domain_id])
        for d in data :
            self.Organization[d["organisation_name"]] = d

    def get_statutory_nature(self, country_id):
        data = self._source_db.call_proc("sp_bu_statutory_nature", [country_id])
        for d in data :
            self.Statutory_Nature[d["statutory_nature_name"]] = d

    def get_grographies(self, country_id):
        data = self._source_db.call_proc("sp_bu_geographies", [country_id])
        for d in data :
            self.Geographies[d["parent_names"]] = d

    def get_statutories(self, country_id, domain_id):
        data = self._source_db.call_proc("sp_bu_statutories", [country_id, domain_id])
        for d in data :
            if d["parent_names"] != "" :
                self.Statutories[d["parent_names"] + '>>' + d["statutory_name"]] = d
            else :
                self.Statutories[d["statutory_name"]] = d

    def get_task_type(self):
        self.Task_Type = ["Register", "Notice"]

    def check_base(self, check_status, store, key_name):
        data = None
        print key_name
        print store
        print check_status
        if type(store) is list :
            if key_name in store :
                data = key_name
        else :
            data = store.get(key_name)

        print data
        if data is None:
            return "Not found"

        if check_status is True :
            if data.get("is_active") == 0 :
                return "Status Inactive"

        return True

    def check_organization(self, organization_name):
        return self.check_base(True,  self.Organization, organization_name)

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

    def check_task_type(self, tType):
        return self.check_base(False, self.Task_Type, tType)

    def check_single_input(self, d):
        msg = []
        keys = ["Statutory_Month", "Statutory_Date", "Trigger_Days"]
        for k in keys :
            if CSV_DELIMITER in d[k]:
                msg.append("%s-%s" % (k, "Invalid data"))

        return msg

    def check_multiple_input(self, d, keys):
        msg = []

        diff = 12 / int(d["Repeats_Every"])
        print diff
        for k in keys :
            print d[k]
            if len(d[k].strip().split(CSV_DELIMITER)) != diff :
                msg.append("%s-%s" % (k, "Invalid data for multiple input section"))
        return msg

    def check_empty_for_compliance_frequency(self, d, keys):
        msg = []
        for k in keys :
            if d[k] != "":
                msg.append(
                    "Invalid  %s for compliance frequency %s" %
                    (k, d["Compliance_Frequency"])
                )
        return msg

    def check_one_time(self, d):
        msg = self.check_single_input(d)

        keys = [
            "Repeats_Type", "Repeats_Every", "Repeats_By (DOM/EOM)", "Duration",
            "Duration_Type", "Multiple_Input_Section"
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

        if (
            d["Compliance_Frequency"] == "On Occurrence" and
            d["Duration_Type"] == ""
        ):
            msg.append("Duration_Type - Field is blank")

        keys = [
            "Statutory_Month", "Statutory_Date", "Trigger_Days",
            "Repeats_Type", "Repeats_Every", "Repeats_By (DOM/EOM)", "Multiple_Input_Section"
        ]
        msg.extend(self.check_empty_for_compliance_frequency(d, keys))
        return msg

    def check_periodical_and_Review(self, d):
        msg = []
        keys = [
            "Duration_Type", "Duration"
        ]
        msg.extend(self.check_empty_for_compliance_frequency(d, keys))

        if d["Repeats_Every"] == "" :
            msg.append("Repeats_Every - Field is blank")

        if d["Repeats_Type"] == "" :
            msg.append("Repeats_Type - Field is blank")

        if d["Multiple_Input_Section"] == "No" or d["Multiple_Input_Section"] == "":
            msg.extend(self.check_single_input(d))

            if d["Repeats_Type"] == "Month(s)" :
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 99 :
                    msg.append("Repeats_Every - Invalid data")
                if d["Repeats_By (DOM/EOM)"] == "" :
                    msg.append("Repeats_By - Field is blank")
                if d["Statutory_Month"] != "":
                    msg.append("Statutory_Month - Invalid data")
                if d["Repeats_By (DOM/EOM)"] == "EOM" and d["Statutory_Date"] != "" :
                    msg.append("Statutory_Date - Invalid data")

            elif d["Repeats_Type"] == "Year(s)" :
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 9 :
                    msg.append("Repeats_Every - Invalid data")
                if d["Repeats_By (DOM/EOM)"] == "" :
                    msg.append("Repeats_By - Field is blank")
                if d["Repeats_By (DOM/EOM)"] == "EOM" and d["Statutory_Date"] != "" :
                    msg.append("Statutory_Date - Invalid data")

            elif d["Repeats_Type"] == "Day(s)" :
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 999 :
                    msg.append("Repeats_Every - Invalid data")
                if d["Repeats_By (DOM/EOM)"] != "" :
                    msg.append("Repeats_By - Invalid data")
                if d["Statutory_Month"] != "":
                    msg.append("Statutory_Month - Invalid data")
                if d["Statutory_Date"] != "" :
                    msg.append("Statutory_Date - Invalid data")
                if d["Repeats_Every"] < d["Trigger_Days"] :
                    msg.append("Trigger_Days - Invalid data")

        elif d["Multiple_Input_Section"] == "Yes" and d["Repeats_Type"] == "Month(s)" :

            if d["Repeats_Every"] == "" :
                msg.append("Repeats_Every - Field is blank")
            elif d["Repeats_Every"] != "" and int(d["Repeats_Every"]) not in [1, 2, 3, 4, 6] :
                msg.append("Repeats_Every - Invalid data for multiple input section")

            if d["Repeats_By (DOM/EOM)"] == "DOM" and d["Repeats_Every"] != "" :
                keys = ["Statutory_Month", "Statutory_Date", "Trigger_Days"]
                msg.extend(self.check_multiple_input(d, keys))

            if d["Repeats_By (DOM/EOM)"] == "EOM" and d["Repeats_Every"] != "" :
                keys = ["Statutory_Month", "Trigger_Days"]
                msg.extend(self.check_multiple_input(d, keys))
                if d["Statutory_Date"] != "" :
                    msg.append("Statutory_Date - Invalid data")

        else :
            msg.append("Multiple_Input_Section - Invalid data")

        return msg

    def check_flexi_review(self, d):
        msg = []
        keys = [
            "Duration_Type", "Duration"
        ]
        msg.extend(self.check_empty_for_compliance_frequency(d, keys))

        if d["Multiple_Input_Section"] == "No" or d["Multiple_Input_Section"] == "":
            msg.extend(self.check_single_input(d))

            if d["Repeats_Type"] == "Month(s)" :
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 99 :
                    msg.append("Repeats_Every - Invalid data")
                if d["Repeats_By (DOM/EOM)"] == "" :
                    msg.append("Repeats_By - Field is blank")
                if d["Statutory_Month"] != "":
                    msg.append("Statutory_Month - Invalid data")
                if d["Repeats_By (DOM/EOM)"] == "EOM" and d["Statutory_Date"] != "" :
                    msg.append("Statutory_Date - Invalid data")

            elif d["Repeats_Type"] == "Year(s)" :
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 9 :
                    msg.append("Repeats_Every - Invalid data")
                if d["Repeats_By (DOM/EOM)"] == "" :
                    msg.append("Repeats_By - Field is blank")
                if d["Repeats_By (DOM/EOM)"] == "EOM" and d["Statutory_Date"] != "" :
                    msg.append("Statutory_Date - Invalid data")

            elif d["Repeats_Type"] == "Day(s)" :
                if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) > 999 :
                    msg.append("Repeats_Every - Invalid data")
                if d["Repeats_By (DOM/EOM)"] != "" :
                    msg.append("Repeats_By - Invalid data")
                if d["Statutory_Month"] != "":
                    msg.append("Statutory_Month - Invalid data")
                if d["Statutory_Date"] != "" :
                    msg.append("Statutory_Date - Invalid data")
                if d["Repeats_Every"] < d["Trigger_Days"] :
                    msg.append("Trigger_Days - Invalid data")

        elif d["Multiple_Input_Section"] == "Yes" and d["Repeats_Type"] == "Month(s)" :

            if d["Repeats_Every"] == "" :
                msg.append("Repeats_Every - Field is blank")
            if d["Repeats_Every"] != '' and int(d["Repeats_Every"]) not in [1, 2, 3, 4, 6] :
                msg.append("Repeats_Every - Invalid data for multiple input section")

            if d["Repeats_By (DOM/EOM)"] == "DOM" and d["Repeats_Every"] != "" :
                keys = ["Statutory_Month", "Statutory_Date", "Trigger_Days"]
                msg.extend(self.check_multiple_input(d, keys))

            if d["Repeats_By (DOM/EOM)"] == "EOM" and d["Repeats_Every"] != "" :
                keys = ["Statutory_Month", "Trigger_Days"]
                msg.extend(self.check_multiple_input(d, keys))
                if d["Statutory_Date"] != "" :
                    msg.append("Statutory_Date - Invalid data")

        else :
            msg.append("Multiple_Input_Section - Invalid data")

        return msg

    # main db related validation mapped with field name
    def statusCheckMethods(self):
        self._validation_method_maps = {
            "Organization": self.check_organization,
            "Applicable_Location": self.check_geography,
            "Statutory_Nature" : self.check_statutory_nature,
            "Statutory" : self.check_statutory,
            "Compliance_Frequency" : self.check_frequency,
            "Repeats_Type" : self.check_repeat_type,
            "Duration_Type" : self.check_duration_type,
            "Task_Type": self.check_task_type,
        }

    def check_compliance_task_name_duplicate(self, country_id, domain_id, statutory, statutory_provision, task_name):
        statutories = statutory.split(CSV_DELIMITER)
        statutory_string = str("[\"" + (',').join(statutories) + "\"]")

        data = self._source_db.call_proc("sp_bu_check_duplicate_compliance", [country_id, domain_id, statutory_provision, task_name, statutory_string])
        if len(data) > 0 :
            return False
        else:
            return True

    def check_task_id_duplicate(self, country_id, domain_id, statutory, statutory_provision, task_name, task_id):
        statutories = statutory.split(CSV_DELIMITER)
        statutory_string = str("[\"" + (',').join(statutories) + "\"]")

        data = self._source_db.call_proc("sp_bu_check_duplicate_task_id", [country_id, domain_id, statutory_provision, task_name, statutory_string, task_id])
        if len(data) > 0 :
            return False
        else:
            return True

    def save_mapping_data(self, c_id, d_id, n_id, uploadedby, mapping):
        created_on = get_date_time()
        mapping_value = [
            int(c_id), int(d_id),
            int(n_id), 1, 1,
            int(uploadedby), str(created_on), mapping
        ]
        q = "INSERT INTO tbl_statutory_mappings (country_id, domain_id, " + \
            " statutory_nature_id, is_active, is_approved, created_by, created_on, statutory_mapping) values " + \
            " (%s, %s, %s, %s, %s, %s, %s, %s)"
        statutory_mapping_id = self._source_db.execute_insert(
            q, mapping_value
        )
        if statutory_mapping_id is False:
            raise process_error("E018")
        return statutory_mapping_id

    def save_compliance_data(self, c_id, d_id, mapping_id, data):
        created_on = get_date_time()
        columns = [
            "statutory_provision",
            "compliance_task", "compliance_description",
            "document_name", "format_file", "format_file_size",
            "penal_consequences", "reference_link", "frequency_id",
            "statutory_dates", "statutory_mapping_id",
            "is_active", "created_by", "created_on",
            "domain_id", "country_id", "is_approved",
            "duration", "duration_type_id", "repeats_every", "repeats_type_id",
            "task_id", "task_type",

        ]
        values = []

        for idx, d in enumerate(data) :
            freq_id = self.Compliance_Frequency.get(d["Compliance_Frequency"]).get("frequency_id")
            duration_type_id = None
            if d["Duration_Type"] != '':
                duration_type_id = self.Duration_Type.get(d["Duration_Type"]).get("duration_type_id")

            repeat_type_id = None
            if d["Repeats_Type"] != '':
                repeat_type_id = self.Repeats_Type.get(d["Repeats_Type"]).get("repeat_type_id")

            values.append((
                d["Statutory_Provision"], d["Compliance_Task"],
                d["Compliance_Description"], d["Compliance_Document"], d["Format"], 0,
                d["Penal_Consequences"], d["Reference_Link"], freq_id,
                d["mapped_statutory_date"], int(mapping_id), 1, d["uploaded_by"],
                created_on, c_id, d_id, 1,
                None if d["Duration"] == '' else d["Duration"],
                duration_type_id,
                None if d["Repeats_Every"] == '' else d["Repeats_Every"],
                repeat_type_id,
                d["Task_ID"], d["Task_Type"],
            ))

        if values :
            self._source_db.bulk_insert("tbl_compliances", columns, values)
            return True
        else :
            return False

    def save_industries(self, mapping_id, uploaded_by, orgids):
        columns = ["statutory_mapping_id", "organisation_id", "assined_by"]
        values = []
        for d in orgids :
            values.append((mapping_id, d, uploaded_by))
        if values :
            self._source_db.bulk_insert("tbl_mapped_industries", columns, values)

    def save_statutories(self, mapping_id, uploaded_by, statu_ids):
        columns = ["statutory_mapping_id", "statutory_id", "assined_by"]
        values = []
        for d in statu_ids :
            values.append((mapping_id, d, uploaded_by))
        if values :
            self._source_db.bulk_insert("tbl_mapped_statutories", columns, values)

    def save_geograhy_location(self, mapping_id, uploaded_by, geo_ids):
        columns = ["statutory_mapping_id", "geography_id", "assined_by"]
        values = []
        for d in geo_ids :
            values.append((mapping_id, d, uploaded_by))
        if values :
            self._source_db.bulk_insert("tbl_mapped_locations", columns, values)


class ValidateStatutoryMappingCsvData(StatutorySource):
    def __init__(self, db, source_data, session_user, country_id, domain_id, csv_name, csv_header):
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
            "duplicate_error" : 0,
            "invalid_char_error": 0,
            "invalid_data_error": 0,
            "inactive_error": 0,
        }

    def compare_csv_columns(self):
        res = collections.Counter(self._csv_column_name) == collections.Counter(self._csv_header)
        if res is False :
            raise ValueError("Csv column mismatched")

    def check_duplicate_in_csv(self):
        seen = set()
        for d in self._source_data:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)

        if len(seen) != len(self._source_data):
            raise ValueError("Csv duplicate row found")

    def check_duplicate_task_name_in_csv(self):
        self._source_data.sort(key=lambda x: (
            x["Statutory"], x["Statutory_Provision"], x["Compliance_Task"]
        ))
        msg = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Statutory"], s["Statutory_Provision"], s["Compliance_Task"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1 :
                msg.append(grouped_list[0].get("Compliance_Task"))

        if len(msg) > 0 :
            error_msg = "Duplicate compliance task found in csv %s" % (
                ','.join(msg)
            )
            raise ValueError(str(error_msg))

    def check_duplicate_task_id_in_csv(self):
        self._source_data.sort(key=lambda x: (
            x["Statutory"], x["Statutory_Provision"], x["Compliance_Task"], x["Task_ID"]
        ))
        msg = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Statutory"], s["Statutory_Provision"], s["Compliance_Task"], s["Task_ID"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1 :
                msg.append(grouped_list[0].get("Task_ID"))

        if len(msg) > 0 :
            error_msg = "Duplicate task id found in csv %s" % (
                ','.join(msg)
            )
            raise ValueError(str(error_msg))

    '''
        looped csv data to perform corresponding validation
        returns : valid and invalid return format
        rType: dictionary
    '''
    def perform_validation(self):
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        self.compare_csv_columns()
        self.check_duplicate_in_csv()
        self.check_duplicate_task_name_in_csv()
        self.check_duplicate_task_id_in_csv()

        self.init_values(self._country_id, self._domain_id)

        def make_error_desc(res, msg):
            if res is True :
                res = []
            if res is not True :
                if type(msg) is list:
                    res.extend(msg)
                else :
                    res.append(msg)
            return res

        for row_idx, data in enumerate(self._source_data):
            print "\n"
            res = True
            print data
            error_count = {"mandatory": 0, "max_length": 0, "invalid_char": 0}
            for key in self._csv_column_name:
                value = data.get(key)
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)

                if (key == "Format" and value != ''):
                    self._doc_names.append(value)
                for v in [v.strip() for v in values] :

                    if v != "" :
                        valid_failed, error_cnt = parse_csv_dictionary_values(key, v)
                        if valid_failed is not True :
                            if res is True :
                                res = valid_failed
                                error_count = error_cnt
                            else :
                                res.extend(valid_failed)
                                error_count["mandatory"] += error_cnt["mandatory"]
                                error_count["max_length"] += error_cnt["max_length"]
                                error_count["invalid_char"] += error_cnt["invalid_char"]

                        if csvParam.get("check_is_exists") is True or csvParam.get("check_is_active") is True :
                            unboundMethod = self._validation_method_maps.get(key)
                            if unboundMethod is not None :
                                isFound = unboundMethod(v)

                            if isFound is not True and isFound != "" :
                                msg = "%s - %s" % (key, isFound)
                                if res is not True :
                                    res.append(msg)
                                else :
                                    res = [msg]
                                print res
                                if "Status" in isFound :
                                    self._error_summary["inactive_error"] += 1
                                else :
                                    self._error_summary["invalid_data_error"] += 1

                if key == "Compliance_Frequency":
                    msg = []
                    if value == "One time":
                        msg = self.check_one_time(data)

                    elif value == "On Occurrence":
                        msg = self.check_on_occurrence(data)

                    elif value in ["Periodical", "Review"]:
                        msg = self.check_periodical_and_Review(data)

                    else :
                        msg = self.check_flexi_review(data)

                    self._error_summary["invalid_data_error"] += len(msg)
                    if len(msg) > 0 :
                        res = make_error_desc(res, msg)
                        print res
                        print key

            if not self.check_compliance_task_name_duplicate(
                self._country_id, self._domain_id, data.get("Statutory"),
                data.get("Statutory_Provision"), data.get("Compliance_Task")
            ) :
                self._error_summary["duplicate_error"] += 1
                dup_error = "Compliance_Task - Duplicate data"
                res = make_error_desc(res, dup_error)

            if not self.check_task_id_duplicate(
                self._country_id, self._domain_id, data.get("Statutory"),
                data.get("Statutory_Provision"), data.get("Compliance_Task"),
                data.get("Task_ID")
            ):
                self._error_summary["duplicate_error"] += 1
                dup_error = "Task_ID - Duplicate data"
                res = make_error_desc(res, dup_error)

            print "final"
            print res

            if res is not True :
                error_list = mapped_error_dict.get(row_idx)
                if error_list is None:
                    error_list = res
                else :
                    error_list.extend(res)
                res = True

                mapped_error_dict[row_idx] = error_list

                head_idx = mapped_header_dict.get(key)
                if head_idx is None :
                    head_idx = [row_idx]
                else :
                    head_idx.append(row_idx)

                mapped_header_dict[key] = head_idx
                invalid += 1
                self._error_summary["mandatory_error"] += error_count["mandatory"]
                self._error_summary["max_length_error"] += error_count["max_length"]
                self._error_summary["invalid_char_error"] += error_count["invalid_char"]

        print invalid
        if invalid > 0 :
            return self.make_invalid_return(mapped_error_dict, mapped_header_dict)
        else :
            return self.make_valid_return(mapped_error_dict, mapped_header_dict)

    def make_invalid_return(self, mapped_error_dict, mapped_header_dict):
        fileString = self._csv_name.split('.')
        file_name = "%s_%s.%s" % (
            fileString[0], "invalid", "xlsx"
        )
        final_hearder = self._csv_header
        final_hearder.append("Error Description")
        write_data_to_excel(
            os.path.join(BULKUPLOAD_INVALID_PATH, "xlsx"), file_name, final_hearder,
            self._source_data, mapped_error_dict, mapped_header_dict, self._sheet_name
        )
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)
        # make csv file
        rename_file_type(file_name, "csv")
        # make ods file
        rename_file_type(file_name, "ods")
        # make text file
        # rename_file_type(file_name, "txt")
        return {
            "return_status": False,
            "invalid_file": file_name,
            "mandatory_error": self._error_summary["mandatory_error"],
            "max_length_error": self._error_summary["max_length_error"],
            "duplicate_error" : self._error_summary["duplicate_error"],
            "invalid_char_error": self._error_summary["invalid_char_error"],
            "invalid_data_error": self._error_summary["invalid_data_error"],
            "inactive_error": self._error_summary["inactive_error"],
            "total": total,
            "invalid": invalid,
            "doc_count": len(set(self._doc_names))
        }

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
            "doc_names": list(set(self._doc_names))
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
        self._declined_row_idx = []
        self.get_source_data()

    def get_source_data(self):
        self._source_data = self._db.call_proc("sp_statutory_mapping_by_csvid", [self._csv_id])

    def perform_validation_before_submit(self):
        declined_count = 0
        self._declined_row_idx = []
        self.init_values(self._country_id, self._domain_id)

        for row_idx, data in enumerate(self._source_data):
            print row_idx, data
            for key in self._csv_column_name:
                value = data.get(key)
                isFound = ""
                if value is None :
                    continue
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)
                if csvParam is None :
                    continue

                for v in values :
                    v = v.strip()

                    if v != "" :
                        if csvParam.get("check_is_exists") is True or csvParam.get("check_is_active") is True :
                            unboundMethod = self._validation_method_maps.get(key)
                            if unboundMethod is not None :
                                isFound = unboundMethod(v)

                        if isFound is not True and isFound != "" :
                            declined_count += 1

            if not self.check_compliance_task_name_duplicate(
                self._country_id, self._domain_id, data.get("Statutory"),
                data.get("Statutory_Provision"), data.get("Compliance_Task")
            ) :
                print "compliance task name dulicate"
                declined_count += 1

            if not self.check_task_id_duplicate(
                self._country_id, self._domain_id, data.get("Statutory"),
                data.get("Statutory_Provision"), data.get("Compliance_Task"),
                data.get("Task_ID")
            ):
                print "Task id duplicate"
                declined_count += 1

            if declined_count > 0 :
                self._declined_row_idx.append(data.get("bulk_statutory_mapping_id"))
        return self._declined_row_idx

    def frame_data_for_main_db_insert(self):
        self._source_data.sort(key=lambda x: (
             x["Organization"], x["Statutory_Nature"], x["Statutory"], x["Applicable_Location"]
        ))
        msg = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Organization"], s["Statutory_Nature"], s["Statutory"], s["Applicable_Location"]
        )):
            grouped_list = list(v)
            if len(grouped_list) == 0:
                continue
            print k
            org_ids = []
            statu_ids = []
            geo_ids = []
            nature_id = None
            statu_mapping = None
            value = grouped_list[0]
            for org in value.get("Organization").strip().split(CSV_DELIMITER):
                org_ids.append(self.Organization.get(org).get("organisation_id"))
            print org_ids

            for nature in value.get("Statutory_Nature"):
                nature_id = self.Statutory_Nature.get(nature).get("statutory_nature_id")
            print nature_id

            for geo_maps in value.get("Applicable_Location").split(CSV_DELIMITER):
                print geo_maps
                geo_ids.append(self.Geographies.get(geo_maps).get("geography_id"))
            print geo_ids

            statu_mapping = value.get("Statutory").split(CSV_DELIMITER)
            for statu_maps in statu_mapping:
                print statu_maps
                statu_ids.append(self.Statutories.get(statu_maps).get("statutory_id"))
            print statu_ids
            if len(grouped_list) > 1 :
                msg.append(grouped_list[0].get("Compliance_Task"))
            uploaded_by = value.get("uploaded_by")

            mapping_id = self.save_mapping_data(self._country_id, self._domain_id, nature_id, uploaded_by, str(statu_mapping))

            self.save_compliance_data(self._country_id, self._domain_id, mapping_id, grouped_list)

            self.save_industries(mapping_id, uploaded_by, org_ids)

            self.save_statutories(mapping_id, uploaded_by, statu_ids)

            self.save_geograhy_location(mapping_id, uploaded_by, geo_ids)

    def make_rejection(self, declined_info):
        q = "update tbl_bulk_statutory_mapping set action = 3 where bulk_statutory_mapping_id in %s"
        self._source_db.execute_insert(q, [",".join(declined_info)])
