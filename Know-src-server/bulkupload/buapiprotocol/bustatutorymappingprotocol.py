from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, parse_VariantType,
    to_VariantType, to_structure_dictionary_values
)

#
# Request
#
class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        if type(inner) is dict:
            inner = to_structure_dictionary_values(inner)
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Request_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Request_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class GetStatutoryMappingCsvUploadedList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryMappingCsvUploadedList()

    def to_inner_structure(self):
        return {
        }

class UploadStatutoryMappingCSV(Request):
    def __init__(self, c_id, c_name, d_id, d_name, csv_name, csv_data, csv_size):
        self.c_id = c_id
        self.c_name = c_name
        self.d_id = d_id
        self.d_name = d_name
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "c_name", "d_id", "d_name", "csv_name", "csv_data", "csv_size"])
        return UploadStatutoryMappingCSV(
            data.get("c_id"), data.get("c_name"), data.get("d_id"),
            data.get("d_name"), data.get("csv_name"), data.get("csv_data"),
            data.get("csv_size")
        )

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "c_name": self.c_name,
            "d_id": self.d_id,
            "d_name": self.d_name,
            "csv_name": self.csv_name,
            "csv_data": self.csv_data,
            "csv_size": self.csv_size,
        }


class GetBulkReportData(Request):
    def __init__(self, c_ids, d_ids, from_date, to_date, r_count, p_count, child_ids, user_category_id):
        self.c_ids = c_ids
        self.d_ids = d_ids
        self.from_date = from_date
        self.to_date = to_date
        self.r_count = r_count
        self.p_count = p_count
        self.child_ids = child_ids
        self.user_category_id = user_category_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "d_ids", "from_date", "to_date", "r_count", "p_count", "child_ids", "user_category_id"])
        return GetBulkReportData(
            data.get("c_ids"), 
            data.get("d_ids"), 
            data.get("from_date"),
            data.get("to_date"), 
            data.get("r_count"),
            data.get("p_count"),
            data.get("child_ids"),
            data.get("user_category_id")
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.c_ids,
            "d_ids": self.d_ids,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "r_count": self.r_count,
            "p_count": self.p_count,
            "child_ids":self.child_ids,
            "user_category_id":self.user_category_id
            }        

class ExportStatutoryMappingBulkReportData(Request):
    def __init__(self, c_ids, d_ids, from_date, to_date, r_count, p_count):
        self.c_ids = c_ids
        self.d_ids = d_ids
        self.from_date = from_date
        self.to_date = to_date
        self.r_count = r_count
        self.p_count = p_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "d_ids", "from_date", "to_date", "r_count", "p_count"])
        return ExportStatutoryMappingBulkReportData(
            data.get("c_ids"), 
            data.get("d_ids"), 
            data.get("from_date"),
            data.get("to_date"), 
            data.get("r_count"),
            data.get("p_count")
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.c_ids,
            "d_ids": self.d_ids,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "r_count": self.r_count,
            "p_count": self.p_count
            }   


class GetAssignedStatutoryBulkReportData(Request):
    def __init__(self, bu_client_id, bu_legal_entity_id, bu_unit_id, from_date, to_date, 
        r_count, p_count, child_ids, user_category_id):
        self.bu_client_id = bu_client_id
        self.bu_legal_entity_id = bu_legal_entity_id
        self.bu_unit_id = bu_unit_id
        self.from_date = from_date
        self.to_date = to_date
        self.r_count = r_count
        self.p_count = p_count
        self.child_ids = child_ids
        self.user_category_id = user_category_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_client_id", "bu_legal_entity_id", "bu_unit_id", "from_date", "to_date", 
        "r_count", "p_count", "child_ids", "user_category_id"])
        return GetAssignedStatutoryBulkReportData(
            data.get("bu_client_id"), 
            data.get("bu_legal_entity_id"), 
            data.get("bu_unit_id"), 
            data.get("from_date"),
            data.get("to_date"), 
            data.get("r_count"),
            data.get("p_count"),
            data.get("child_ids"),
            data.get("user_category_id")
        )

    def to_inner_structure(self):
        return {
            "bu_client_id": self.bu_client_id,
            "bu_legal_entity_id": self.bu_legal_entity_id,
            "bu_unit_id": self.bu_unit_id,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "r_count": self.r_count,
            "p_count": self.p_count,
            "child_ids":self.child_ids,
            "user_category_id":self.user_category_id
            }        


class GetRejectedStatutoryMappingList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetRejectedStatutoryMappingList()

    def to_inner_structure(self):
        return {
        }

class RemoveRejectedData(Request):
    def __init__(self, csv_id, pwd):
        self.csv_id = csv_id
        self.pwd = pwd

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "pwd"])
        return RemoveRejectedData(
            data.get("csv_id"), data.get("pwd")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "pwd": self.pwd
        }

class GetApproveStatutoryMappingList(Request):
    def __init__(self, c_id, d_id):
        self.c_id = c_id
        self.d_id = d_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "d_id"])
        return GetApproveStatutoryMappingList(
            data.get("c_id"), data.get("d_id")
        )

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "d_id": self.d_id
        }

class GetApproveMappingFilter(Request):
    def __init__(self, csv_id):
        self.csv_id = csv_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id"])
        return GetApproveMappingFilter(data.get("csv_id"))

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id
        }

class GetApproveStatutoryMappingViewFilter(Request):
    def __init__(
        self, csv_id, orga_name, s_nature, frequency, statutory, geo_location,
        c_task_name, c_desc, c_doc, f_count, f_range
    ):
        self.csv_id = csv_id
        self.orga_name = orga_name
        self.s_nature = s_nature
        self.frequency = frequency
        self.statutory = statutory
        self.geo_location = geo_location
        self.c_task_name = c_task_name
        self.c_desc = c_desc
        self.c_doc = c_doc
        self.f_count = f_count
        self.f_range = f_range

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "orga_name", "s_nature", "frequency", "statutory",
            "geo_location", "c_task_name", "c_desc", "c_doc",
            "f_count", "f_range"
        ])
        return GetApproveStatutoryMappingViewFilter(
            data.get("csv_id"), data.get("orga_name"), data.get("s_nature"),
            data.get("frequency"), data.get("statutory"), data.get("geo_location"),
            data.get("c_task_name"), data.get("c_desc"), data.get("c_doc"),
            data.get("f_count"), data.get("f_range")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "orga_name": self.orga_name,
            "s_nature": self.s_nature,
            "frequency": self.frequency,
            "statutory": self.statutory,
            "geo_location": self.geo_location,
            "c_task_name": self.c_task_name,
            "c_desc": self.c_desc,
            "c_doc": self.c_doc,
            "f_count": self.f_count,
            "f_range": self.f_range
        }


class GetApproveStatutoryMappingView(Request):
    def __init__(self, csv_id, f_count, r_range):
        self.csv_id = csv_id
        self.f_count = f_count
        self.r_range = r_range

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "f_count", "r_range"])
        return GetApproveStatutoryMappingView(
            data.get("csv_id"), data.get("f_count"), data.get("r_range")
        )

    def to_inner_structure(self):
        return {
            "csv_id" : self.csv_id,
            "f_count" : self.f_count,
            "r_range" : self.r_range,
        }


class UpdateApproveActionFromList(Request):
    def __init__(self, csv_id, action, remarks):
        self.csv_id = csv_id
        self.action = action
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "action", "remarks"])
        return UpdateApproveActionFromList(
            data.get("csv_id"), data.get("action"), data.get("remarks")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "action": self.action,
            "remarks": self.remarks,
        }


class SubmitStatutoryMapping(Request):
    def __init__(self, csv_id, pwd):
        self.csv_id = csv_id
        self.pwd = pwd

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "pwd"])
        return SubmitStatutoryMapping(
            data.get("csv_id"), data.get("pwd")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "pwd": self.pwd
        }

def _init_Request_class_map():
    classes = [
        GetStatutoryMappingCsvUploadedList,
        UploadStatutoryMappingCSV,
        GetRejectedStatutoryMappingList,
        RemoveRejectedData,
        GetApproveStatutoryMappingList,
        GetApproveMappingFilter,
        GetApproveStatutoryMappingViewFilter,
        GetApproveStatutoryMappingView,
        UpdateApproveActionFromList,
        SubmitStatutoryMapping,
        GetBulkReportData,
        GetAssignedStatutoryBulkReportData

    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()

class CsvList(object):
    def __init__(self, c_id, c_name, d_id, d_name, csv_id, csv_name, no_of_records, no_of_documents, uploaded_document):
        self.c_id = c_id
        self.c_name = c_name
        self.d_id = d_id
        self.d_name = d_name
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.no_of_records = no_of_records
        self.no_of_documents = no_of_documents
        self.uploaded_document = uploaded_document

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_id", "c_name", "d_id", "d_name", "csv_id", "csv_name",
            "no_of_records", "no_of_documents", "uploaded_documents"
        ])
        return CsvList(
            data.get("c_id"), data.get("c_name"), data.get("d_id"),
            data.get("d_name"), data.get("csv_id"), data.get("csv_name"),
            data.get("no_of_records"), data.get("no_of_documents"),
            data.get("uploaded_documents")
        )

    def to_structure(self):
        return {
            "c_id": self.c_id,
            "c_name": self.c_name,
            "d_id": self.d_id,
            "d_name": self.d_name,
            "csv_id": self.csv_id,
            "csv_name": self.csv_name,
            "no_of_records": self.no_of_records,
            "no_of_documents": self.no_of_documents,
            "uploaded_documents": self.uploaded_document
        }


class ReportData(object):

    def __init__(self, country_name, domain_name, uploaded_by,
        uploaded_on, csv_name, total_records, total_rejected_records,
        approved_by, rejected_by, approved_on, rejected_on,
        is_fully_rejected, approve_status
        ):
        self.country_name = country_name
        self.domain_name = domain_name
        self.uploaded_by = uploaded_by

        self.uploaded_on = uploaded_on
        self.csv_name = csv_name
        self.total_records = total_records
        self.total_rejected_records = total_rejected_records
        self.approved_by = approved_by
        self.rejected_by = rejected_by
        self.approved_on = approved_on
        self.rejected_on = rejected_on
        self.is_fully_rejected = is_fully_rejected
        self.approve_status = approve_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_name", "domain_name", "uploaded_by",
        "uploaded_on", "csv_name", "total_records", "total_rejected_records",
        "approved_by", "rejected_by", "approved_on", "rejected_on",
        "is_fully_rejected", "approve_status"
        ])
        return ReportData(
            data.get("country_name"), 
            data.get("domain_name"), 
            data.get("uploaded_by"),
            data.get("uploaded_on"),
            data.get("csv_name"),
            data.get("total_records"),
            data.get("total_rejected_records"),
            data.get("approved_by"),
            data.get("rejected_by"),
            data.get("approved_on"),
            data.get("rejected_on"),
            data.get("is_fully_rejected"),
            data.get("approve_status")
        )

    def to_structure(self):
        return {
            "country_name": self.country_name,
            "domain_name": self.domain_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on" : self.uploaded_on,
            "csv_name" : self.csv_name,
            "total_records" : self.total_records,
            "total_rejected_records" : self.total_rejected_records,
            "rejected_by" : self.rejected_by,
            "approved_on" : self.approved_on,
            "rejected_on" : self.rejected_on,
            "is_fully_rejected" : self.is_fully_rejected,
            "approve_status"    : self.approve_status
            }

class StatutoryReportData(object):

    def __init__(self, uploaded_by,
        uploaded_on, csv_name, total_records, total_rejected_records,
        approved_by, rejected_by, approved_on, rejected_on,
        is_fully_rejected, approve_status
        ):
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.csv_name = csv_name
        self.total_records = total_records
        self.total_rejected_records = total_rejected_records
        self.approved_by = approved_by
        self.rejected_by = rejected_by
        self.approved_on = approved_on
        self.rejected_on = rejected_on
        self.is_fully_rejected = is_fully_rejected
        self.approve_status = approve_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "uploaded_by",
        "uploaded_on", "csv_name", "total_records", "total_rejected_records",
        "approved_by", "rejected_by", "approved_on", "rejected_on",
        "is_fully_rejected", "approve_status"
        ])
        return ReportData(
            data.get("uploaded_by"),
            data.get("uploaded_on"),
            data.get("csv_name"),
            data.get("total_records"),
            data.get("total_rejected_records"),
            data.get("approved_by"),
            data.get("rejected_by"),
            data.get("approved_on"),
            data.get("rejected_on"),
            data.get("is_fully_rejected"),
            data.get("approve_status")
        )

    def to_structure(self):
        return {
            "uploaded_by": self.uploaded_by,
            "uploaded_on" : self.uploaded_on,
            "csv_name" : self.csv_name,
            "total_records" : self.total_records,
            "total_rejected_records" : self.total_rejected_records,
            "rejected_by" : self.rejected_by,
            "approved_on" : self.approved_on,
            "rejected_on" : self.rejected_on,
            "is_fully_rejected" : self.is_fully_rejected,
            "approve_status"    : self.approve_status
            }

class RejectedList(object):
    def __init__(
        self, c_id, c_name, d_id, d_name, csv_id, csv_name, no_of_records,
        rej_by, rej_on, rej_count, rej_file, rej_reason, remove
    ):
        self.c_id = c_id
        self.c_name = c_name
        self.d_id = d_id
        self.d_name = d_name
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.no_of_records = no_of_records
        self.rej_by = rej_by
        self.rej_on = rej_on
        self.rej_count = rej_count
        self.rej_file = rej_file
        self.rej_reason = rej_reason
        self.remove = remove

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_id", "c_name", "d_id", "d_name", "csv_id", "csv_name",
            "no_of_records", "rej_by", "rej_on", "rej_count", "rej_file",
            "rej_reason", "remove"
        ])
        return CsvList(
            data.get("c_id"), data.get("c_name"), data.get("d_id"),
            data.get("d_name"), data.get("csv_id"), data.get("csv_name"),
            data.get("no_of_records"), data.get("rej_by"), data.get("rej_on"),
            data.get("rej_count"), data.get("rej_file"),
            data.get("rej_reason"), data.get("remove")
        )

    def to_structure(self):
        return {
            "c_id": self.c_id,
            "c_name": self.c_name,
            "d_id": self.d_id,
            "d_name": self.d_name,
            "csv_id": self.csv_id,
            "csv_name": self.csv_name,
            "no_of_records": self.no_of_records,
            "rej_by": self.rej_by,
            "rej_on": self.rej_on,
            "rej_count": self.rej_count,
            "rej_file": self.rej_file,
            "rej_reason": self.rej_reason,
            "remove": self.remove
        }

class PendingCsvList(object):
    def __init__(
        self, csv_id, csv_name, uploaded_by,
        uploaded_on, no_of_records, action_count, download_file
    ):
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.no_of_records = no_of_records
        self.action_count = action_count
        self.download_file = download_file

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "csv_name", "uploaded_by", "uploaded_on",
            "no_of_records", "action_count", "download_file"

        ])
        return PendingCsvList(
            data.get("csv_id"), data.get("csv_name"), data.get("uploaded_by"),
            data.get("uploaded_on"), data.get("no_of_records"), data.get("download_file")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "csv_name": self.csv_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "no_of_records": self.no_of_records,
            "action_count": self.action_count,
            "download_file": self.download_file
        }

class MappingData(object):
    def __init__(
        self, sm_id, orga_name, geo_location, s_nature, statutory, s_provsion,
        c_task_name, c_doc, c_desc, p_cons, refer, frequency, statu_month,
        statu_date, trigger_before, r_every, r_type, r_by,
        dur, dur_type, multiple_input, format_file, bu_action, bu_remarks
    ):
        self.sm_id = sm_id
        self.orga_name = orga_name
        self.geo_location = geo_location
        self.s_nature = s_nature
        self.statutory = statutory
        self.s_provsion = s_provsion
        self.c_atsk_name = c_task_name
        self.c_doc = c_doc
        self.c_desc = c_desc
        self.p_cons = p_cons
        self.refer = refer
        self.frequency = frequency
        self.statu_month = statu_month
        self.statu_date = statu_date
        self.trigger_before = trigger_before
        self.r_every = r_every
        self.r_type = r_type
        self.r_by = r_by
        self.dur = dur
        self.dur_type = dur_type
        self.multiple_input = multiple_input
        self.format_file = format_file
        self.bu_action = bu_action
        self.bu_remarks = bu_remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "sm_id",
            "orga_name",
            "geo_location",
            "s_nature",
            "statutory",
            "s_provsion",
            "c_task_name",
            "c_doc",
            "c_desc",
            "p_cons",
            "refer",
            "frequency",
            "statu_month",
            "statu_date",
            "trigger_before",
            "r_every",
            "r_type",
            "r_by",
            "dur",
            "dur_type",
            "multiple_input",
            "format_file",
            "bu_action",
            "bu_remarks",

        ])
        return MappingData(
            data.get("sm_id"),
            data.get("orga_name"),
            data.get("geo_location"),
            data.get("s_nature"),
            data.get("statutory"),
            data.get("s_provsion"),
            data.get("c_task_name"),
            data.get("c_doc"),
            data.get("c_desc"),
            data.get("p_cons"),
            data.get("refer"),
            data.get("frequency"),
            data.get("statu_month"),
            data.get("statu_date"),
            data.get("trigger_before"),
            data.get("r_every"),
            data.get("r_type"),
            data.get("r_by"),
            data.get("dur"),
            data.get("dur_type"),
            data.get("multiple_input"),
            data.get("format_file"),
            data.get("bu_action"),
            data.get("bu_remarks"),
        )

    def to_structure(self):
        return {
            "sm_id": self.sm_id,
            "orga_name": self.orga_name,
            "geo_location": self.geo_location,
            "s_nature": self.s_nature,
            "statutory": self.statutory,
            "s_provsion": self.s_provsion,
            "c_task_name": self.c_task_name,
            "c_doc": self.c_doc,
            "c_desc": self.c_desc,
            "p_cons": self.p_cons,
            "refer": self.refer,
            "frequency": self.frequency,
            "statu_month": self.statu_month,
            "statu_date": self.statu_date,
            "trigger_before": self.trigger_before,
            "r_every": self.r_every,
            "r_type": self.r_type,
            "r_by": self.r_by,
            "dur": self.dur,
            "dur_type": self.dur_type,
            "multiple_input": self.multiple_input,
            "format_file": self.format_file,
            "bu_action": self.bu_action,
            "bu_remarks": self.bu_remarks,
        }


#
# Response
#
class Response(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        if type(inner) is dict:
            inner = to_structure_dictionary_values(inner)
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Response_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Response_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class GetStatutoryMappingCsvUploadedListSuccess(Response):
    def __init__(self, upload_more, csv_list):
        self.upload_more = upload_more
        self.csv_list = csv_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["upload_more", "csv_list"])
        upload_more = data.get("upload_more")
        csv_list = data.get("csv_list")
        return GetStatutoryMappingCsvUploadedListSuccess(
            upload_more, csv_list
        )

    def to_inner_structure(self):
        return {
            "upload_more": self.upload_more,
            "csv_list": self.csv_list
        }

class UploadStatutoryMappingCSVSuccess(Response):
    def __init__(self, total, valid, invalid, doc_count, doc_names):
        self.total = total
        self.valid = valid
        self.invalid = invalid
        self.doc_count = doc_count
        self.doc_names = doc_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total", "valid", "invalid", "doc_count", "doc_names"])
        return UploadStatutoryMappingCSVSuccess(
            data.get("total"), data.get("valid"), data.get("invalid"),
            data.get("doc_count"), data.get("doc_names")
        )

    def to_inner_structure(self):
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid,
            "doc_count": self.doc_count,
            "doc_names": self.doc_names
        }

class GetBulkReportDataSuccess(Response):
    def __init__(self, reportdata, total):
        self.reportdata = reportdata
        self.total = total
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["reportdata"], ["total"])

        return GetBulkReportDataSuccess(
            data.get("reportdata"),
            data.get("total")
        )

    def to_inner_structure(self):
        return {
            "reportdata": self.reportdata,
            "total": self.total
        }

class GetAssignedStatutoryReportDataSuccess(Response):
    def __init__(self, assign_statutory_data, total):
        self.assign_statutory_data = assign_statutory_data
        self.total = total
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["assign_statutory_data"], ["total"])

        return GetAssignedStatutoryReportDataSuccess(
            data.get("assign_statutory_data"),
            data.get("total")
        )

    def to_inner_structure(self):
        return {
            "assign_statutory_data": self.assign_statutory_data,
            "total": self.total
        }


class UploadStatutoryMappingCSVFailed(Response):
    def __init__(
        self, invalid_file, mandatory_error, max_length_error, duplicate_error,
        invalid_char_error, invalid_data_error, inactive_error,
        total, invalid

    ):
        self.invalid_file = invalid_file
        self.mandatory_error = mandatory_error
        self.max_length_error = max_length_error
        self.duplicate_error = duplicate_error
        self.invalid_char_error = invalid_char_error
        self.invalid_data_error = invalid_data_error
        self.inactive_error = inactive_error
        self.total = total
        self.invalid = invalid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "invalid_file", "mandatory_error", "max_length_error", "duplicate_error",
            "invalid_char_error", "invalid_data_error", "inactive_error",
            "total", "invalid"
        ])
        return UploadStatutoryMappingCSVFailed(
            data.get("invalid_file"), data.get("mandatory_error"),
            data.get("max_length_error"), data.get("duplicate_error"),
            data.get("invalid_char_error"), data.get("invalid_data_error"),
            data.get("inactive_error"),
            data.get("total"),
            data.get("invalid")
        )

    def to_inner_structure(self):
        return {
            "invalid_file" : self.invalid_file,
            "mandatory_error": self.mandatory_error,
            "max_length_error": self.max_length_error,
            "duplicate_error": self.duplicate_error,
            "invalid_char_error": self.invalid_char_error,
            "invalid_data_error": self.invalid_data_error,
            "inactive_error": self.inactive_error,
            "total": self.total,
            "invalid": self.invalid
        }


class GetRejectedStatutoryMappingListSuccess(Response):
    def __init__(self, rejected_list):
        self.rejected_list = rejected_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["rejected_list"])
        return GetRejectedStatutoryMappingListSuccess(data.get("rejected_list"))

    def to_inner_structure(self):
        return {
            "rejected_list": self.rejected_list
        }

class RemoveRejectedDataSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return RemoveRejectedDataSuccess()

    def to_inner_structure(self):
        return {}


class GetApproveStatutoryMappingListSuccess(Response):
    def __init__(self, pending_csv_list):
        self.pending_csv_list = pending_csv_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["pending_csv_list"])
        return GetApproveStatutoryMappingListSuccess(
            data.get("pending_csv_list")
        )

    def to_inner_structure(self):
        return {
            "pending_csv_list": self.pending_csv_list
        }

class GetApproveMappingFilterSuccess(Response):
    def __init__(
        self, orga_names, s_natures, statutories,
        frequencies, geo_locations, c_tasks, c_descs,
        c_docs
    ):
        self.orga_names = orga_names
        self.s_natures = s_natures
        self.statutories = statutories
        self.frequencies = frequencies
        self.geo_locations = geo_locations
        self.c_tasks = c_tasks
        self.c_descs = c_descs
        self.c_docs = c_docs

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "orga_names", "s_natures", "statutories",
            "frequencies", "geo_locations", "c_tasks",
            "c_descs", "c_docs"
        ])
        return {
            "orga_names": data.get("orga_names"),
            "s_natures": data.get("s_natures"),
            "statutories": data.get("statutories"),
            "frequencies": data.get("frequencies"),
            "geo_locations": data.get("geo_locations"),
            "c_tasks": data.get("c_tasks"),
            "c_descs": data.get("c_descs"),
            "c_docs": data.get("c_docs"),
        }

    def to_inner_structure(self):
        return {
            "orga_names": self.orga_names,
            "s_natures": self.s_natures,
            "bu_statutories": self.statutories,
            "frequencies": self.frequencies,
            "geo_locations": self.geo_locations,
            "c_tasks": self.c_tasks,
            "c_descs": self.c_descs,
            "c_docs": self.c_docs,
        }

# class GetApproveStatutoryMappingViewFilterSuccess(Response):
#     def __init__(self, c_name, d_name, csv_name, uploaded_by, uploaded_on, csv_id, mapping_data):
#         self.c_name = c_name
#         self.d_name = d_name
#         self.csv_name = csv_name
#         self.uploaded_by = uploaded_by
#         self.uploaded_on = uploaded_on
#         self.csv_id = csv_id
#         self.mapping_data = mapping_data

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, [
#             "c_name", "d_name", "csv_name", "uploaded_by", "uploaded_on", "csv_id", "mapping_data"
#         ])
#         return GetApproveStatutoryMappingViewFilterSuccess(
#             data.get("c_name"),
#             data.get("d_name"),
#             data.get("csv_name"),
#             data.get("uploaded_by"),
#             data.get("uploaded_on"),
#             data.get("csv_id"),
#             data.get("mapping_data"),
#         )

#     def to_inner_structure(self):
#         return {
#             "c_name" : self.c_name,
#             "d_name" : self.d_name,
#             "csv_name" : self.csv_name,
#             "uploaded_by" : self.uploaded_by,
#             "uploaded_on" : self.uploaded_on,
#             "csv_id" : self.csv_id,
#             "mapping_data" : self.mapping_data,
#         }


class GetApproveStatutoryMappingViewSuccess(Response):
    def __init__(self, c_name, d_name, csv_name, uploaded_by, uploaded_on, csv_id, mapping_data):
        self.c_name = c_name
        self.d_name = d_name
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.csv_id = csv_id
        self.mapping_data = mapping_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_name", "d_name", "csv_name", "uploaded_by", "uploaded_on", "csv_id", "mapping_data"
        ])
        return GetApproveStatutoryMappingViewSuccess(
            data.get("c_name"),
            data.get("d_name"),
            data.get("csv_name"),
            data.get("uploaded_by"),
            data.get("uploaded_on"),
            data.get("csv_id"),
            data.get("mapping_data"),
        )

    def to_inner_structure(self):
        return {
            "c_name" : self.c_name,
            "d_name" : self.d_name,
            "csv_name" : self.csv_name,
            "uploaded_by" : self.uploaded_by,
            "uploaded_on" : self.uploaded_on,
            "csv_id" : self.csv_id,
            "mapping_data" : self.mapping_data,
        }


class UpdateApproveActionFromListSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateApproveActionFromListSuccess()

    def to_inner_structure(self):
        return {}

class SubmitStatutoryMappingSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SubmitStatutoryMappingSuccess()

    def to_inner_structure(self):
        return {}

class ApproveActionPendingForSomeCompliances(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ApproveActionPendingForSomeCompliances()

    def to_inner_structure(self):
        return {}


class ValidationFailedForSomeCompliances(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ValidationFailedForSomeCompliances()

    def to_inner_structure(self):
        return {}

def _init_Response_class_map():
    classes = [
        GetStatutoryMappingCsvUploadedListSuccess,
        UploadStatutoryMappingCSVSuccess,
        UploadStatutoryMappingCSVFailed,
        GetRejectedStatutoryMappingListSuccess,
        RemoveRejectedDataSuccess,
        GetApproveStatutoryMappingListSuccess,
        GetApproveMappingFilterSuccess,
        # GetApproveStatutoryMappingViewFilterSuccess,
        GetApproveStatutoryMappingViewSuccess,
        UpdateApproveActionFromListSuccess,
        SubmitStatutoryMappingSuccess,
        ApproveActionPendingForSomeCompliances,
        ValidationFailedForSomeCompliances,
        GetBulkReportDataSuccess,
        GetAssignedStatutoryReportDataSuccess,
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


#
# RequestFormat
#
statutory_mapping = "bulkupload.buapiprotocol.bustatutorymappingprotocol"
class RequestFormat(object):
    print "RequestFormat"
    def __init__(self, session_token, request):
        self.session_token = session_token
        self.request = request

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["session_token", "request"])
        session_token = data.get("session_token")
        request = data.get("request")
        request = parse_VariantType(
            request, statutory_mapping, "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, statutory_mapping, "Response"
            ),
        }
