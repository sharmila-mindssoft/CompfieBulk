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


class UploadClientUnitsBulkCSV(Request):
    def __init__(self, bu_client_id, bu_group_name, csv_name, csv_data, csv_size):
        self.bu_client_id = bu_client_id
        self.bu_group_name = bu_group_name
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_client_id", "bu_group_name", "csv_name", "csv_data", "csv_size"])
        return UploadClientUnitsBulkCSV(
            data.get("bu_client_id"), data.get("bu_group_name"),
            data.get("csv_name"), data.get("csv_data"),
            data.get("csv_size")
        )

    def to_inner_structure(self):
        return {
            "bu_client_id": self.bu_client_id,
            "bu_group_name": self.bu_group_name,
            "csv_name": self.csv_name,
            "csv_data": self.csv_data,
            "csv_size": self.csv_size
        }

class GetClientUnitsUploadedCSVFiles(Request):
    def __init__(self, bu_client_id, bu_group_name):
        self.bu_client_id = bu_client_id
        self.bu_group_name = bu_group_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_client_id", "bu_group_name"])
        return GetClientUnitsUploadedCSVFiles(
            data.get("bu_client_id"),
            data.get("bu_group_name")
        )

    def to_inner_structure(self):
        return {
            "bu_client_id": self.bu_client_id,
            "bu_group_name": self.bu_group_name
        }

class GetClientUnitRejectedData(Request):
    def __init__(self, bu_client_id):
        self.bu_client_id = bu_client_id
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_client_id"])
        return GetClientUnitRejectedData(
            data.get("bu_client_id")
        )

    def to_inner_structure(self):
        return {
            "bu_client_id": self.bu_client_id
            }

class UpdateUnitClickCount(Request):
    def __init__(self, csv_id):
        self.csv_id = csv_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id"])
        return UpdateUnitClickCount(
            data.get("csv_id")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id
        }

class DeleteRejectedUnitDataByCsvID(Request):
    def __init__(self, csv_id, bu_client_id):
        self.bu_client_id = bu_client_id
        self.csv_id = csv_id
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "bu_client_id"])
        return DeleteRejectedUnitDataByCsvID(
            data.get("csv_id"),
            data.get("bu_client_id")
            )

    def to_inner_structure(self):
        return {
            "csv_id":self.c_id,
            "bu_client_id":self.d_id
            }


class GetClientUnitBulkReportData(Request):
    def __init__(self, bu_client_id, from_date, to_date,
        r_count, p_count, child_ids, user_category_id):
        self.bu_client_id = bu_client_id
        self.from_date = from_date
        self.to_date = to_date
        self.r_count = r_count
        self.p_count = p_count
        self.child_ids = child_ids
        self.user_category_id = user_category_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_client_id", "from_date", "to_date",
        "r_count", "p_count", "child_ids", "user_category_id"])
        return GetClientUnitBulkReportData(
            data.get("bu_client_id"),
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
            "from_date": self.from_date,
            "to_date": self.to_date,
            "r_count": self.r_count,
            "p_count": self.p_count,
            "child_ids":self.child_ids,
            "user_category_id":self.user_category_id
        }
# SM - Statutory Mapping

class DownloadRejectedClientUnitReport(Request):
    def __init__(self, csv_id, cg_id, download_format):
        self.csv_id = csv_id
        self.cg_id = cg_id
        self.download_format = download_format

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "cg_id", "download_format"])
        return DownloadRejectedClientUnitReport(
            data.get("csv_id"), data.get("cg_id"),
            data.get("download_format")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "cg_id": self.cg_id,
            "download_format": self.download_format
        }



class ExportCUBulkReportData(Request):
    def __init__(self, bu_client_id, bu_group_name, from_date, to_date,
                 child_ids, user_category_id, csv):
        self.bu_client_id = bu_client_id
        self.bu_group_name = bu_group_name
        self.from_date = from_date
        self.to_date = to_date
        self.child_ids = child_ids
        self.user_category_id = user_category_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_client_id", "bu_group_name",
                                       "from_date", "to_date",
                                       "child_ids", "user_category_id", "csv"])
        return ExportCUBulkReportData(
            data.get("bu_client_id"),
            data.get("bu_group_name"),
            data.get("from_date"),
            data.get("to_date"),
            data.get("child_ids"),
            data.get("user_category_id"),
            data.get("csv")
        )

    def to_inner_structure(self):
        return {
            "bu_client_id": self.bu_client_id,
            "bu_group_name": self.bu_group_name,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "child_ids": self.child_ids,
            "user_category_id": self.user_category_id,
            "csv": self.csv
        }


class PerformClientUnitApproveReject(Request):
    def __init__(self, csv_id, bu_action, bu_remarks, password, bu_client_id):
        self.csv_id = csv_id
        self.bu_action = bu_action
        self.bu_remarks = bu_remarks
        self.password = password
        self.bu_client_id = bu_client_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "bu_action", "bu_remarks", "password", "bu_client_id"])
        return PerformClientUnitApproveReject(
            data.get("csv_id"), data.get("bu_action"), data.get("bu_remarks"),
            data.get("password"), data.get("bu_client_id")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "bu_action": self.bu_action,
            "bu_remarks": self.bu_remarks,
            "password": self.password,
            "bu_client_id": self.bu_client_id
        }

def _init_Request_class_map():
    classes = [
        UploadClientUnitsBulkCSV,
        GetClientUnitsUploadedCSVFiles,
        GetClientUnitRejectedData,
        UpdateUnitClickCount,
        DeleteRejectedUnitDataByCsvID,
        GetClientUnitBulkReportData,
        ExportCUBulkReportData,
        DownloadRejectedClientUnitReport,
        PerformClientUnitApproveReject
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()

#
# Object
#

class ClientUnitCSVList(object):
    def __init__(
        self, csv_id, csv_name, uploaded_by, uploaded_on, no_of_records,
        approved_count, rej_count
    ):
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.no_of_records = no_of_records
        self.approved_count = approved_count
        self.rej_count = rej_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "csv_name", "uploaded_by", "uploaded_on",
            "no_of_records", "approved_count", "rej_count"
        ])
        return ClientUnitCSVList(
            data.get("csv_id"), data.get("csv_name"), data.get("uploaded_by"),
            data.get("uploaded_on"), data.get("no_of_records"), data.get("approved_count"),
            data.get("rej_count")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "csv_name": self.csv_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "no_of_records": self.no_of_records,
            "approved_count": self.approved_count,
            "rej_count": self.rej_count,
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


class UploadClientUnitBulkCSVSuccess(Response):
    def __init__(self, total, valid, invalid):
        self.total = total
        self.valid = valid
        self.invalid = invalid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total", "valid", "invalid"])
        return UploadClientUnitBulkCSVSuccess(
            data.get("total"), data.get("valid"), data.get("invalid")
        )

    def to_inner_structure(self):
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid
        }


class UploadClientUnitBulkCSVFailed(Response):
    def __init__(
        self, invalid_file, mandatory_error, max_length_error, duplicate_error,
        invalid_char_error, invalid_data_error, inactive_error,
        max_unit_count_error, total, invalid

    ):
        self.invalid_file = invalid_file
        self.mandatory_error = mandatory_error
        self.max_length_error = max_length_error
        self.duplicate_error = duplicate_error
        self.invalid_char_error = invalid_char_error
        self.invalid_data_error = invalid_data_error
        self.inactive_error = inactive_error
        self.max_unit_count_error = max_unit_count_error
        self.total = total
        self.invalid = invalid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "invalid_file", "mandatory_error", "max_length_error", "duplicate_error",
            "invalid_char_error", "invalid_data_error", "inactive_error",
            "max_unit_count_error", "total", "invalid"
        ])
        return UploadClientUnitBulkCSVFailed(
            data.get("invalid_file"), data.get("mandatory_error"),
            data.get("max_length_error"), data.get("duplicate_error"),
            data.get("invalid_char_error"), data.get("invalid_data_error"),
            data.get("inactive_error"), data.get("max_unit_count_error"),
            data.get("total"), data.get("invalid")
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
            "max_unit_count_error": self.max_unit_count_error,
            "total": self.total,
            "invalid": self.invalid
        }

class GetRejectedClientUnitDataSuccess(Response):
    def __init__(self, rejected_unit_data):
        self.rejected_unit_data = rejected_unit_data
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["rejected_unit_data"])
        return GetRejectedStatutoryMappingBulkUploadDataSuccess(
            data.get("rejected_unit_data")
        )

    def to_inner_structure(self):
        return {
            "rejected_unit_data": self.rejected_unit_data
        }

class ClientUnitRejectData(object):
    def __init__(self, csv_id, uploaded_by,
        uploaded_on, csv_name, total_records, total_rejected_records,
        approved_by, rejected_by, approved_on, rejected_on,
        is_fully_rejected, approve_status, file_download_count, remarks,
        statutory_action, declined_count
        ):
        self.csv_id = csv_id
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
        self.file_download_count = file_download_count
        self.remarks = remarks
        self.statutory_action = statutory_action
        self.declined_count = declined_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id","uploaded_by","uploaded_on", "csv_name", "total_records",
            "total_rejected_records", "approved_by", "rejected_by", "approved_on",
            "rejected_on", "is_fully_rejected", "approve_status", "file_download_count",
            "remarks", "statutory_action", "declined_count"
        ])
        return ClientUnitRejectData(
            data.get("csv_id"),
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
            data.get("approve_status"),
            data.get("file_download_count"),
            data.get("remarks"),
            data.get("statutory_action"),
            data.get("declined_count")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "uploaded_by": self.uploaded_by,
            "uploaded_on" : self.uploaded_on,
            "csv_name" : self.csv_name,
            "total_records" : self.total_records,
            "total_rejected_records" : self.total_rejected_records,
            "rejected_by" : self.rejected_by,
            "approved_on" : self.approved_on,
            "approved_by" : self.approved_by,
            "rejected_on" : self.rejected_on,
            "is_fully_rejected" : self.is_fully_rejected,
            "approve_status"    : self.approve_status,
            "file_download_count"    : self.file_download_count,
            "remarks"    : self.remarks,
            "statutory_action"    : self.statutory_action,
            "declined_count"    : self.declined_count
            }

class UpdateUnitDownloadCount(object):
    def __init__(self, csv_id, download_count
        ):
        self.csv_id = csv_id
        self.download_count = download_count
    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id","download_count"
        ])
        return UpdateUnitDownloadCount(
            data.get("csv_id"),
            data.get("download_count")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "download_count": self.download_count
            }

class UpdateUnitDownloadCountSuccess(Response):
    def __init__(self, updated_unit_count):
        self.updated_unit_count = updated_unit_count
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["updated_unit_count"])
        return UpdateUnitDownloadCountSuccess(
            data.get("updated_unit_count")
        )
    def to_inner_structure(self):
        return {
            "updated_unit_count": self.updated_unit_count
        }

class GetClientUnitReportDataSuccess(Response):
    def __init__(self, clientdata, total):
        self.clientdata = clientdata
        self.total = total
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["clientdata"], ["total"])

        return GetClientUnitReportDataSuccess(
            data.get("clientdata"),
            data.get("total")
        )

    def to_inner_structure(self):
        return {
            "clientdata": self.clientdata,
            "total": self.total
        }

class ClientUnitsUploadedCSVFilesListSuccess(Response):
    def __init__(self, bu_cu_csvFilesList):
        self.bu_cu_csvFilesList = bu_cu_csvFilesList

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_cu_csvFilesList"])
        return ClientUnitsUploadedCSVFilesListSuccess(
            data.get("bu_cu_csvFilesList")
        )

    def to_inner_structure(self):
        return {
            "bu_cu_csvFilesList": self.bu_cu_csvFilesList,
        }


def _init_Response_class_map():
    classes = [
        UploadClientUnitBulkCSVSuccess,
        UploadClientUnitBulkCSVFailed,
        ClientUnitsUploadedCSVFilesListSuccess,
        UpdateUnitDownloadCountSuccess,
        GetClientUnitReportDataSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


#
# RequestFormat
#

client_units = "bulkupload.buapiprotocol.buclientunitsprotocol"

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
            request, client_units, "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, client_units, "Response"
            ),
        }
