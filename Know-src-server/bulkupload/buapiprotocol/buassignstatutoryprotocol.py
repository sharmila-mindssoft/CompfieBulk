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


class GetClientInfo(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientInfo()

    def to_inner_structure(self):
        return {
        }

# class UploadStatutoryMappingCSV(Request):
#     def __init__(self, c_id, c_name, d_id, d_name, csv_name, csv_data, csv_size, uploadby_name):
#         self.c_id = c_id
#         self.c_name = c_name
#         self.d_id = d_id
#         self.d_name = d_name
#         self.csv_name = csv_name
#         self.csv_data = csv_data
#         self.csv_size = csv_size
#         self.uploadby_name = uploadby_name

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["c_id", "c_name", "d_id", "d_name", "csv_name", "csv_data", "csv_size", "uploadby_name"])
#         return UploadStatutoryMappingCSV(
#             data.get("c_id"), data.get("c_name"), data.get("d_id"),
#             data.get("d_name"), data.get("csv_name"), data.get("csv_data"),
#             data.get("csv_size"), data.get("uploadby_name")
#         )

#     def to_inner_structure(self):
#         return {
#             "c_id": self.c_id,
#             "c_name": self.c_name,
#             "d_id": self.d_id,
#             "d_name": self.d_name,
#             "csv_name": self.csv_name,
#             "csv_data": self.csv_data,
#             "csv_size": self.csv_size,
#             "uploadby_name": self.uploadby_name
#         }

# class GetRejectedStatutoryMappingList(Request):
#     def __init__(self):
#         pass

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data)
#         return GetRejectedStatutoryMappingList()

#     def to_inner_structure(self):
#         return {
#         }

# class RemoveRejectedData(Request):
#     def __init__(self, csv_id, pwd):
#         self.csv_id = csv_id
#         self.pwd = pwd

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["csv_id", "pwd"])
#         return RemoveRejectedData(
#             data.get("csv_id"), data.get("pwd")
#         )

#     def to_inner_structure(self):
#         return {
#             "csv_id": self.csv_id,
#             "pwd": self.pwd
#         }

# class GetApproveStatutoryMappingList(Request):
#     def __init__(self, c_id, d_id):
#         self.c_id = c_id
#         self.d_id = d_id

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["c_id", "d_id"])
#         return GetApproveStatutoryMappingList(
#             data.get("c_id"), data.get("d_id")
#         )

#     def to_inner_structure(self):
#         return {
#             "c_id": self.c_id,
#             "d_id": self.d_id
#         }


# class GetApproveStatutoryMappingViewFilter(Request):
#     def __init__(
#         self, csv_id, orga_name, s_nature, frequency, statutory, geo_location,
#         c_task_name, c_desc, c_doc
#     ):
#         self.csv_id = csv_id
#         self.orga_name = orga_name
#         self.s_nature = s_nature
#         self.frequency = frequency
#         self.statutory = statutory
#         self.geo_location = geo_location
#         self.c_task_name = c_task_name
#         self.c_desc = c_desc

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, [
#             "csv_id", "orga_name", "s_nature", "frequency", "statutory",
#             "geo_location", "c_task_name", "c_desc", "c_doc"
#         ])
#         return GetApproveStatutoryMappingViewFilter(
#             data.get("csv_id"), data.get("orga_name"), data.get("s_nature"),
#             data.get("frequency"), data.get("statutory"), data.get("geo_location"),
#             data.get("c_task_name"), data.get("c_desc"), data.get("c_doc")
#         )

#     def to_inner_structure(self):
#         return {
#             "csv_id": self.csv_id,
#             "orga_name": self.orga_name,
#             "s_nature": self.s_nature,
#             "frequency": self.frequency,
#             "statutory": self.statutory,
#             "geo_location": self.geo_location,
#             "c_task_name": self.c_task_name,
#             "c_desc": self.c_desc,
#             "c_doc": self.c_doc
#         }


# class GetApproveStatutoryMappingView(Request):
#     def __init__(self, csv_id, f_count, r_range):
#         self.csv_id = csv_id
#         self.f_count = f_count
#         self.r_range = r_range

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["csv_id", "f_count", "r_range"])
#         return GetApproveStatutoryMappingView(
#             data.get("csv_id"), data.get("f_count"), data.get("r_range")
#         )

#     def to_inner_structure(self):
#         return {
#             "csv_id" : self.csv_id,
#             "f_count" : self.f_count,
#             "r_range" : self.r_range,
#         }


# class UpdateApproveActionFromList(Request):
#     def __init__(self, csv_id, action, remarks):
#         self.csv_id = csv_id
#         self.action = action
#         self.remarks = remarks

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["csv_id", "action", "remarks"])
#         return UpdateApproveActionFromList(
#             data.get("csv_id"), data.get("action"), data.get("remarks")
#         )

#     def to_inner_structure(self):
#         return {
#             "csv_id": self.csv_id,
#             "action": self.action,
#             "remarks": self.remarks,
#         }


# class SubmitStatutoryMapping(Request):
#     def __init__(self, csv_id, pwd):
#         self.csv_id = csv_id
#         self.pwd = pwd

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["csv_id", "pwd"])
#         return SubmitStatutoryMapping(
#             data.get("csv_id"), data.get("pwd")
#         )

#     def to_inner_structure(self):
#         return {
#             "csv_id": self.csv_id,
#             "pwd": self.pwd
#         }

def _init_Request_class_map():
    classes = [
        GetClientInfo
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()

# class CsvList(object):
#     def __init__(self, c_id, c_name, d_id, d_name, csv_id, csv_name, no_of_records, no_of_documents, uploaded_document):
#         self.c_id = c_id
#         self.c_name = c_name
#         self.d_id = d_id
#         self.d_name = d_name
#         self.csv_id = csv_id
#         self.csv_name = csv_name
#         self.no_of_records = no_of_records
#         self.no_of_documents = no_of_documents
#         self.uploaded_document = uploaded_document

#     @staticmethod
#     def parse_structure(data):
#         data = parse_dictionary(data, [
#             "c_id", "c_name", "d_id", "d_name", "csv_id", "csv_name",
#             "no_of_records", "no_of_documents", "uploaded_documents"
#         ])
#         return CsvList(
#             data.get("c_id"), data.get("c_name"), data.get("d_id"),
#             data.get("d_name"), data.get("csv_id"), data.get("csv_name"),
#             data.get("no_of_records"), data.get("no_of_documents"),
#             data.get("uploaded_documents")
#         )

#     def to_structure(self):
#         return {
#             "c_id": self.c_id,
#             "c_name": self.c_name,
#             "d_id": self.d_id,
#             "d_name": self.d_name,
#             "csv_id": self.csv_id,
#             "csv_name": self.csv_name,
#             "no_of_records": self.no_of_records,
#             "no_of_documents": self.no_of_documents,
#             "uploaded_documents": self.uploaded_document
#         }

# class RejectedList(object):
#     def __init__(
#         self, c_id, c_name, d_id, d_name, csv_id, csv_name, no_of_records,
#         rej_by, rej_on, rej_count, rej_file, rej_reason, remove
#     ):
#         self.c_id = c_id
#         self.c_name = c_name
#         self.d_id = d_id
#         self.d_name = d_name
#         self.csv_id = csv_id
#         self.csv_name = csv_name
#         self.no_of_records = no_of_records
#         self.rej_by = rej_by
#         self.rej_on = rej_on
#         self.rej_count = rej_count
#         self.rej_file = rej_file
#         self.rej_reason = rej_reason
#         self.remove = remove

#     @staticmethod
#     def parse_structure(data):
#         data = parse_dictionary(data, [
#             "c_id", "c_name", "d_id", "d_name", "csv_id", "csv_name",
#             "no_of_records", "rej_by", "rej_on", "rej_count", "rej_file",
#             "rej_reason", "remove"
#         ])
#         return CsvList(
#             data.get("c_id"), data.get("c_name"), data.get("d_id"),
#             data.get("d_name"), data.get("csv_id"), data.get("csv_name"),
#             data.get("no_of_records"), data.get("rej_by"), data.get("rej_on"),
#             data.get("rej_count"), data.get("rej_file"),
#             data.get("rej_reason"), data.get("remove")
#         )

#     def to_structure(self):
#         return {
#             "c_id": self.c_id,
#             "c_name": self.c_name,
#             "d_id": self.d_id,
#             "d_name": self.d_name,
#             "csv_id": self.csv_id,
#             "csv_name": self.csv_name,
#             "no_of_records": self.no_of_records,
#             "rej_by": self.rej_by,
#             "rej_on": self.rej_on,
#             "rej_count": self.rej_count,
#             "rej_file": self.rej_file,
#             "rej_reason": self.rej_reason,
#             "remove": self.remove
#         }

# class PendingCsvList(object):
#     def __init__(
#         self, csv_id, csv_name, uploaded_by,
#         uploaded_on, no_of_records, action_count, download_file
#     ):
#         self.csv_id = csv_id
#         self.csv_name = csv_name
#         self.uploaded_by = uploaded_by
#         self.uploaded_on = uploaded_on
#         self.no_of_records = no_of_records
#         self.action_count = action_count
#         self.download_file = download_file

#     @staticmethod
#     def parse_structure(data):
#         data = parse_dictionary(data, [
#             "csv_id", "csv_name", "uploaded_by", "uploaded_on",
#             "no_of_records", "action_count", "download_file"

#         ])
#         return PendingCsvList(
#             data.get("csv_id"), data.get("csv_name"), data.get("uploaded_by"),
#             data.get("uploaded_on"), data.get("no_of_records"), data.get("download_file")
#         )

#     def to_structure(self):
#         return {
#             "csv_id": self.csv_id,
#             "csv_name": self.csv_name,
#             "uploaded_by": self.uploaded_by,
#             "uploaded_on": self.uploaded_on,
#             "no_of_records": self.no_of_records,
#             "action_count": self.action_count,
#             "download_file": self.download_file
#         }

# class MappingData(object):
#     def __init__(
#         self, sm_id, orga_name, geo_location, s_nature, statutory, s_provsion,
#         c_task_name, c_doc, c_desc, p_cons, refer, frequency, statu_month,
#         statu_date, trigger_before, r_every, r_type, r_by,
#         dur, dur_type, multiple_input, format_file, bu_action, bu_remarks
#     ):
#         self.sm_id = sm_id
#         self.orga_name = orga_name
#         self.geo_location = geo_location
#         self.s_nature = s_nature
#         self.statutory = statutory
#         self.s_provsion = s_provsion
#         self.c_atsk_name = c_task_name
#         self.c_doc = c_doc
#         self.c_desc = c_desc
#         self.p_cons = p_cons
#         self.refer = refer
#         self.frequency = frequency
#         self.statu_month = statu_month
#         self.statu_date = statu_date
#         self.trigger_before = trigger_before
#         self.r_every = r_every
#         self.r_type = r_type
#         self.r_by = r_by
#         self.dur = dur
#         self.dur_type = dur_type
#         self.multiple_input = multiple_input
#         self.format_file = format_file
#         self.bu_action = bu_action
#         self.bu_remarks = bu_remarks

#     @staticmethod
#     def parse_structure(data):
#         data = parse_dictionary(data, [
#             "sm_id",
#             "orga_name",
#             "geo_location",
#             "s_nature",
#             "statutory",
#             "s_provsion",
#             "c_task_name",
#             "c_doc",
#             "c_desc",
#             "p_cons",
#             "refer",
#             "frequency",
#             "statu_month",
#             "statu_date",
#             "trigger_before",
#             "r_every",
#             "r_type",
#             "r_by",
#             "dur",
#             "dur_type",
#             "multiple_input",
#             "format_file",
#             "bu_action",
#             "bu_remarks",

#         ])
#         return MappingData(
#             data.get("sm_id"),
#             data.get("orga_name"),
#             data.get("geo_location"),
#             data.get("s_nature"),
#             data.get("statutory"),
#             data.get("s_provsion"),
#             data.get("c_task_name"),
#             data.get("c_doc"),
#             data.get("c_desc"),
#             data.get("p_cons"),
#             data.get("refer"),
#             data.get("frequency"),
#             data.get("statu_month"),
#             data.get("statu_date"),
#             data.get("trigger_before"),
#             data.get("r_every"),
#             data.get("r_type"),
#             data.get("r_by"),
#             data.get("dur"),
#             data.get("dur_type"),
#             data.get("multiple_input"),
#             data.get("format_file"),
#             data.get("bu_action"),
#             data.get("bu_remarks"),
#         )

#     def to_structure(self):
#         return {
#             "sm_id": self.sm_id,
#             "orga_name": self.orga_name,
#             "geo_location": self.geo_location,
#             "s_nature": self.s_nature,
#             "statutory": self.statutory,
#             "s_provsion": self.s_provsion,
#             "c_task_name": self.c_task_name,
#             "c_doc": self.c_doc,
#             "c_desc": self.c_desc,
#             "p_cons": self.p_cons,
#             "refer": self.refer,
#             "frequency": self.frequency,
#             "statu_month": self.statu_month,
#             "statu_date": self.statu_date,
#             "trigger_before": self.trigger_before,
#             "r_every": self.r_every,
#             "r_type": self.r_type,
#             "r_by": self.r_by,
#             "dur": self.dur,
#             "dur_type": self.dur_type,
#             "multiple_input": self.multiple_input,
#             "format_file": self.format_file,
#             "bu_action": self.bu_action,
#             "bu_remarks": self.bu_remarks,
#         }




class Clients(object):
    def __init__(
        self, cl_id, cl_name
    ):
        self.cl_id = cl_id
        self.cl_name = cl_name
        
    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "cl_name"
        ])
        return Clients(
            data.get("cl_id"), data.get("cl_name")
        )

    def to_structure(self):
        return {
            "cl_id": self.cl_id,
            "cl_name": self.cl_name
        }

class LegalEntites(object):
    def __init__(
        self, cl_id, le_id, le_name
    ):
        self.cl_id = cl_id
        self.le_id = le_id
        self.le_name = le_name
        
    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "le_id", "le_name"
        ])
        return LegalEntites(
            data.get("cl_id"), data.get("le_id"), data.get("le_name")
        )

    def to_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "le_name": self.le_name
        }

class Units(object):
    def __init__(
        self, cl_id, le_id, u_id, u_name
    ):
        self.cl_id = cl_id
        self.le_id = le_id
        self.u_id = u_id
        self.u_name = u_name
        
    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "le_id", "u_id", "u_name"
        ])
        return Units(
            data.get("cl_id"), data.get("le_id"), data.get("u_id"), data.get("u_name")
        )

    def to_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "u_id": self.u_id,
            "u_name": self.u_name
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


class GetClientInfoSuccess(Response):
    def __init__(self, clients, legalentites, units):
        self.clients = clients
        self.legalentites = legalentites
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["clients", "legalentites", "units"])
        clients = data.get("clients")
        legalentites = data.get("legalentites")
        units = data.get("units")
        return GetClientInfoSuccess(
            clients, legalentites, units
        )

    def to_inner_structure(self):
        return {
            "clients": self.clients,
            "legalentites": self.legalentites,
            "units": self.units

        }


# class UploadStatutoryMappingCSVSuccess(Response):
#     def __init__(self, total, valid, invalid, doc_count, doc_names):
#         self.total = total
#         self.valid = valid
#         self.invalid = invalid
#         self.doc_count = doc_count
#         self.doc_names = doc_names

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["total", "valid", "invalid", "doc_count", "doc_names"])
#         return UploadStatutoryMappingCSVSuccess(
#             data.get("total"), data.get("valid"), data.get("invalid"),
#             data.get("doc_count"), data.get("doc_names")
#         )

#     def to_inner_structure(self):
#         return {
#             "total": self.total,
#             "valid": self.valid,
#             "invalid": self.invalid,
#             "doc_count": self.doc_count,
#             "doc_names": self.doc_names
#         }


# class UploadStatutoryMappingCSVFailed(Response):
#     def __init__(
#         self, invalid_file, mandatory_error, max_length_error, duplicate_error,
#         invalid_char_error, invalid_data_error, inactive_error,
#         total, invalid

#     ):
#         self.invalid_file = invalid_file
#         self.mandatory_error = mandatory_error
#         self.max_length_error = max_length_error
#         self.duplicate_error = duplicate_error
#         self.invalid_char_error = invalid_char_error
#         self.invalid_data_error = invalid_data_error
#         self.inactive_error = inactive_error
#         self.total = total
#         self.invalid = invalid

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, [
#             "invalid_file", "mandatory_error", "max_length_error", "duplicate_error",
#             "invalid_char_error", "invalid_data_error", "inactive_error",
#             "total", "invalid"
#         ])
#         return UploadStatutoryMappingCSVFailed(
#             data.get("invalid_file"), data.get("mandatory_error"),
#             data.get("max_length_error"), data.get("duplicate_error"),
#             data.get("invalid_char_error"), data.get("invalid_data_error"),
#             data.get("inactive_error"),
#             data.get("total"),
#             data.get("invalid")
#         )

#     def to_inner_structure(self):
#         return {
#             "invalid_file" : self.invalid_file,
#             "mandatory_error": self.mandatory_error,
#             "max_length_error": self.max_length_error,
#             "duplicate_error": self.duplicate_error,
#             "invalid_char_error": self.invalid_char_error,
#             "invalid_data_error": self.invalid_data_error,
#             "inactive_error": self.inactive_error,
#             "total": self.total,
#             "invalid": self.invalid
#         }


# class GetRejectedStatutoryMappingListSuccess(Response):
#     def __init__(self, rejected_list):
#         self.rejected_list = rejected_list

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["rejected_list"])
#         return GetRejectedStatutoryMappingListSuccess(data.get("rejected_list"))

#     def to_inner_structure(self):
#         return {
#             "rejected_list": self.rejected_list
#         }

# class RemoveRejectedDataSuccess(Response):
#     def __init__(self):
#         pass

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data)
#         return RemoveRejectedDataSuccess()

#     def to_inner_structure(self):
#         return {}


# class GetApproveStatutoryMappingListSuccess(Response):
#     def __init__(self, pending_csv_list):
#         self.pending_csv_list = pending_csv_list

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["pending_csv_list"])
#         return GetApproveStatutoryMappingListSuccess(
#             data.get("pending_csv_list")
#         )

#     def to_inner_structure(self):
#         return {
#             "pending_csv_list": self.pending_csv_list
#         }

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


# class GetApproveStatutoryMappingViewSuccess(Response):
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
#         return GetApproveStatutoryMappingViewSuccess(
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


# class UpdateApproveActionFromListSuccess(Response):
#     def __init__(self, csv_id, sm_id, action, remarks):
#         self.csv_id = csv_id
#         self.sm_id = sm_id
#         self.action = action
#         self.remarks = remarks

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data, ["csv_id", "sm_id", "action", "remarks"])
#         return UpdateApproveActionFromListSuccess(
#             data.get("csv_id"), data.get("sm_id"), data.get("action"), data.get("remarks")
#         )

#     def to_inner_structure(self):
#         return {
#             "csv_id" : self.csv_id,
#             "sm_id" : self.sm_id,
#             "action" : self.action,
#             "remarks" : self.remarks,
#         }

# class SubmitStatutoryMappingSuccess(Response):
#     def __init__(self):
#         pass

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data)
#         return SubmitStatutoryMappingSuccess()

#     def to_inner_structure(self):
#         return {}

# class ApproveActionPendingForSomeCompliances(Response):
#     def __init__(self):
#         pass

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data)
#         return ApproveActionPendingForSomeCompliances()

#     def to_inner_structure(self):
#         return {}


# class ValidationFailedForSomeCompliances(Response):
#     def __init__(self):
#         pass

#     @staticmethod
#     def parse_inner_structure(data):
#         data = parse_dictionary(data)
#         return ValidationFailedForSomeCompliances()

#     def to_inner_structure(self):
#         return {}

def _init_Response_class_map():
    classes = [
        GetClientInfoSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


#
# RequestFormat
#
assign_statutory = "bulkupload.buapiprotocol.buassignstatutoryprotocol"
class RequestFormat(object):
    def __init__(self, session_token, request):
        self.session_token = session_token
        self.request = request

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["session_token", "request"])
        session_token = data.get("session_token")
        request = data.get("request")
        request = parse_VariantType(
            request, assign_statutory, "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, assign_statutory, "Response"
            ),
        }
