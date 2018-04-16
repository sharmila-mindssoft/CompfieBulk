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

    def __init__(self, bu_client_id, bu_group_name, csv_name, csv_data,
                 csv_size):

        self.bu_client_id = bu_client_id
        self.bu_group_name = bu_group_name
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, [
            "bu_client_id", "bu_group_name", "csv_name", "csv_data", "csv_size"
        ])

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
            "csv_id": self.c_id,
            "bu_client_id": self.d_id
        }


class GetClientUnitBulkReportData(Request):
    def __init__(self, bu_client_id, from_date, to_date, r_count, p_count,
                 child_ids, user_category_id):
        self.bu_client_id = bu_client_id
        self.from_date = from_date
        self.to_date = to_date
        self.r_count = r_count
        self.p_count = p_count
        self.child_ids = child_ids
        self.user_category_id = user_category_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "bu_client_id", "from_date", "to_date", "r_count", "p_count",
            "child_ids", "user_category_id"])
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
            "child_ids": self.child_ids,
            "user_category_id": self.user_category_id
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

        data = parse_dictionary(data, [
            "csv_id", "bu_action", "bu_remarks", "password", "bu_client_id"
        ])
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


class GetBulkClientUnitApproveRejectList(Request):
    def __init__(self, csv_id, f_count, r_range):

        self.csv_id = csv_id
        self.f_count = f_count
        self.r_range = r_range

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, ["csv_id", "f_count", "r_range"])
        return GetBulkClientUnitApproveRejectList(
            data.get("csv_id"), data.get("f_count"), data.get("r_range")
        )

    def to_inner_structure(self):

        return {
            "csv_id": self.csv_id,
            "f_count": self.f_count,
            "r_range": self.r_range
        }


class ConfirmClientUnitDeclination(Request):
    def __init__(self, csv_id, bu_client_id):
        self.csv_id = csv_id
        self.bu_client_id = bu_client_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "bu_client_id"])
        return ConfirmClientUnitDeclination(
            data.get("csv_id"), data.get("bu_client_id"),
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "bu_client_id": self.bu_client_id,
        }


class SaveBulkClientUnitListFromView(Request):

    def __init__(self, bulk_unit_id, csv_id, bu_action, bu_remarks):

        self.bulk_unit_id = bulk_unit_id
        self.csv_id = csv_id
        self.bu_action = bu_action
        self.bu_remarks = bu_remarks

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, [
            "bulk_unit_id", "csv_id", "bu_action", "bu_remarks"
        ])
        return SaveBulkClientUnitListFromView(
            data.get("bulk_unit_id"), data.get("csv_id"),
            data.get("bu_action"), data.get("bu_remarks")
        )

    def to_inner_structure(self):

        return {
            "bulk_unit_id": self.bulk_unit_id,
            "csv_id": self.csv_id,
            "bu_action": self.bu_action,
            "bu_remarks": self.bu_remarks
        }


class SubmitBulkClientUnitListFromView(Request):

    def __init__(self, csv_id, bu_action, bu_remarks, password, bu_client_id):
        self.csv_id = csv_id
        self.bu_action = bu_action
        self.bu_remarks = bu_remarks
        self.password = password
        self.bu_client_id = bu_client_id

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, [
            "csv_id", "bu_action", "bu_remarks", "password", "bu_client_id"
        ])
        return SubmitBulkClientUnitListFromView(
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


class ConfirmSubmitClientUnitFromView(Request):

    def __init__(self, csv_id, bu_client_id):
        self.csv_id = csv_id
        self.bu_client_id = bu_client_id

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, ["csv_id", "bu_client_id"])
        return SubmitBulkClientUnitListFromView(
            data.get("csv_id"), data.get("bu_client_id")
        )

    def to_inner_structure(self):

        return {
            "csv_id": self.csv_id,
            "bu_client_id": self.bu_client_id
        }


class GetBulkClientUnitListForFilterView(Request):

    def __init__(
        self, csv_id, f_count, r_range, bu_le_name, bu_division_name,
        bu_category_name, bu_unit_location, bu_unit_code, bu_domain,
        bu_orgn, bu_action
    ):
        self.csv_id = csv_id
        self.f_count = f_count
        self.r_range = r_range
        self.bu_le_name = bu_le_name
        self.bu_division_name = bu_division_name
        self.bu_category_name = bu_category_name
        self.bu_unit_location = bu_unit_location
        self.bu_unit_code = bu_unit_code
        self.bu_domain = bu_domain
        self.bu_orgn = bu_orgn
        self.bu_action = bu_action

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, [
            "csv_id", "f_count", "r_range", "bu_le_name", "bu_division_name",
            "bu_category_name", "bu_unit_location",
            "bu_unit_code", "bu_domain",
            "bu_orgn", "bu_action"
        ])
        return GetBulkClientUnitListForFilterView(
            data.get("csv_id"), data.get("f_count"), data.get("r_range"),
            data.get("bu_le_name"), data.get("bu_division_name"),
            data.get("bu_category_name"), data.get("bu_unit_location"),
            data.get("bu_unit_code"), data.get("bu_domain"),
            data.get("bu_orgn"), data.get("bu_action")
        )

    def to_inner_structure(self):

        return {
            "csv_id": self.csv_id,
            "f_count": self.f_count,
            "r_range": self.r_range,
            "bu_le_name": self.bu_le_name,
            "bu_division_name": self.bu_division_name,
            "bu_category_name": self.bu_category_name,
            "bu_unit_location": self.bu_unit_location,
            "bu_unit_code": self.bu_unit_code,
            "bu_domain": self.bu_domain,
            "bu_orgn": self.bu_orgn,
            "bu_action": self.bu_action
        }


def _init_Request_class_map():
    classes = [
        UploadClientUnitsBulkCSV,
        GetClientUnitsUploadedCSVFiles,
        GetClientUnitRejectedData,
        UpdateUnitClickCount,
        DeleteRejectedUnitDataByCsvID,
        GetClientUnitBulkReportData,
        PerformClientUnitApproveReject,
        DownloadRejectedClientUnitReport,
        GetBulkClientUnitApproveRejectList,
        ExportCUBulkReportData,
        ConfirmClientUnitDeclination,
        SaveBulkClientUnitListFromView,
        SubmitBulkClientUnitListFromView,
        ConfirmSubmitClientUnitFromView,
        GetBulkClientUnitListForFilterView
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
        approved_count, rej_count, declined_count
    ):
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.no_of_records = no_of_records
        self.approved_count = approved_count
        self.rej_count = rej_count
        self.declined_count = declined_count

    @staticmethod
    def parse_structure(data):

        data = parse_dictionary(data, [
            "csv_id", "csv_name", "uploaded_by", "uploaded_on",
            "no_of_records", "approved_count", "rej_count",
            "declined_count"
        ])

        return ClientUnitCSVList(
            data.get("csv_id"), data.get("csv_name"), data.get("uploaded_by"),
            data.get("uploaded_on"), data.get("no_of_records"),
            data.get("approved_count"),
            data.get("rej_count"), data.get("declined_count")
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
            "declined_count": self.declined_count
        }


class ClientReportData(object):
    def __init__(self, uploaded_by,
                 uploaded_on, csv_name, total_records, total_rejected_records,
                 approved_by, rejected_by, approved_on, rejected_on,
                 is_fully_rejected, total_approve_records,
                 rejected_reason, declined_count
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
        self.total_approve_records = total_approve_records
        self.rejected_reason = rejected_reason
        self.declined_count = declined_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "uploaded_by", "uploaded_on", "csv_name", "total_records",
            "total_rejected_records", "approved_by", "rejected_by",
            "approved_on", "rejected_on", "is_fully_rejected",
            "total_approve_records", "rejected_reason", "declined_count"
        ])
        return ClientReportData(
                          data.get("uploaded_by"),
                          data.get("uploaded_on"),
                          data.get("csv_name"), data.get("total_records"),
                          data.get("total_rejected_records"),
                          data.get("approved_by"), data.get("rejected_by"),
                          data.get("approved_on"), data.get("rejected_on"),
                          data.get("is_fully_rejected"),
                          data.get("total_approve_records"),
                          data.get("rejected_reason"),
                          data.get("declined_count")
                          )

    def to_structure(self):
        return {
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "csv_name": self.csv_name,
            "total_records": self.total_records,
            "total_rejected_records": self.total_rejected_records,
            "approved_by": self.approved_by,
            "rejected_by": self.rejected_by,
            "approved_on": self.approved_on,
            "rejected_on": self.rejected_on,
            "is_fully_rejected": self.is_fully_rejected,
            "total_approve_records": self.total_approve_records,
            "rejected_reason": self.rejected_reason,
            "declined_count": self.declined_count
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
            "invalid_file", "mandatory_error", "max_length_error",
            "duplicate_error", "invalid_char_error", "invalid_data_error",
            "inactive_error", "max_unit_count_error", "total", "invalid"
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
            "invalid_file": self.invalid_file,
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
        return GetRejectedClientUnitDataSuccess(
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
                 is_fully_rejected, total_approve_records, file_download_count,
                 remarks, statutory_action, declined_count, rejected_file,
                 rejected_reason
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
        self.total_approve_records = total_approve_records
        self.file_download_count = file_download_count
        self.remarks = remarks
        self.statutory_action = statutory_action
        self.declined_count = declined_count
        self.rejected_file = rejected_file
        self.rejected_reason = rejected_reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "uploaded_by", "uploaded_on", "csv_name",
            "total_records", "total_rejected_records", "approved_by",
            "rejected_by", "approved_on", "rejected_on", "is_fully_rejected",
            "total_approve_records", "file_download_count", "remarks",
            "statutory_action", "declined_count", "rejected_file",
            "rejected_reason"
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
            data.get("total_approve_records"),
            data.get("file_download_count"),
            data.get("remarks"),
            data.get("statutory_action"),
            data.get("declined_count"),
            data.get("rejected_file"),
            data.get("rejected_reason")
            )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "csv_name": self.csv_name,
            "total_records": self.total_records,
            "total_rejected_records": self.total_rejected_records,
            "rejected_by": self.rejected_by,
            "approved_on": self.approved_on,
            "approved_by": self.approved_by,
            "rejected_on": self.rejected_on,
            "is_fully_rejected": self.is_fully_rejected,
            "total_approve_records": self.total_approve_records,
            "file_download_count": self.file_download_count,
            "remarks": self.remarks,
            "statutory_action": self.statutory_action,
            "declined_count": self.declined_count,
            "rejected_file": self.rejected_file,
            "rejected_reason": self.rejected_reason
        }


class UpdateUnitDownloadCount(object):
    def __init__(self, csv_id, download_count):
        self.csv_id = csv_id
        self.download_count = download_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["csv_id", "download_count"])
        return UpdateUnitDownloadCount(
            data.get("csv_id"),
            data.get("download_count")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "download_count": self.download_count
        }


class BulkClientUnitList(object):

    def __init__(
        self, bulk_unit_id, bu_le_name, bu_division_name, bu_category_name,
        bu_geography_level, bu_unit_location, bu_unit_code,
        bu_unit_name, bu_address, bu_city, bu_state, bu_postal_code,
        bu_domain, bu_orgn, bu_action, bu_remarks
    ):
        self.bulk_unit_id = bulk_unit_id
        self.bu_le_name = bu_le_name
        self.bu_division_name = bu_division_name
        self.bu_category_name = bu_category_name
        self.bu_geography_level = bu_geography_level
        self.bu_unit_location = bu_unit_location
        self.bu_unit_code = bu_unit_code
        self.bu_unit_name = bu_unit_name
        self.bu_address = bu_address
        self.bu_city = bu_city
        self.bu_state = bu_state
        self.bu_postal_code = bu_postal_code
        self.bu_domain = bu_domain
        self.bu_orgn = bu_orgn
        self.bu_action = bu_action
        self.bu_remarks = bu_remarks

    @staticmethod
    def parse_structure(data):

        data = parse_dictionary(data, [
            "bulk_unit_id", "bu_le_name", "bu_division_name",
            "bu_category_name", "bu_geography_level", "bu_unit_location",
            "bu_unit_code", "bu_unit_name",
            "bu_address", "bu_city", "bu_state", "bu_postal_code", "bu_domain",
            "bu_orgn", "bu_action", "bu_remarks"
        ])

        return BulkClientUnitList(
            data.get("bulk_unit_id"), data.get("bu_le_name"),
            data.get("bu_division_name"), data.get("bu_category_name"),
            data.get("bu_geography_level"), data.get("bu_unit_location"),
            data.get("bu_unit_code"), data.get("bu_unit_name"),
            data.get("bu_address"), data.get("bu_city"),
            data.get("bu_state"), data.get("bu_postal_code"),
            data.get("bu_domain"), data.get("bu_orgn"),
            data.get("bu_action"), data.get("bu_remarks")
        )

    def to_structure(self):

        return {
            "bulk_unit_id": self.bulk_unit_id,
            "bu_le_name": self.bu_le_name,
            "bu_division_name": self.bu_division_name,
            "bu_category_name": self.bu_category_name,
            "bu_geography_level": self.bu_geography_level,
            "bu_unit_location": self.bu_unit_location,
            "bu_unit_code": self.bu_unit_code,
            "bu_unit_name": self.bu_unit_name,
            "bu_address": self.bu_address,
            "bu_city": self.bu_city,
            "bu_state": self.bu_state,
            "bu_postal_code": self.bu_postal_code,
            "bu_domain": self.bu_domain,
            "bu_orgn": self.bu_orgn,
            "bu_action": self.bu_action,
            "bu_remarks": self.bu_remarks
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


class ReturnDeclinedCount(Response):
    def __init__(self, declined_count, rejected_count):
        self.declined_count = declined_count
        self.rejected_count = rejected_count

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, ["declined_count", "rejected_count"])
        return ReturnDeclinedCount(
            data.get("declined_count"), data.get("rejected_count")
        )

    def to_inner_structure(self):

        return {
            "declined_count": self.declined_count,
            "rejected_count": self.rejected_count
        }


class UpdateApproveRejectActionFromListSuccess(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return UpdateApproveRejectActionFromListSuccess()

    def to_inner_structure(self):

        return {}


class SubmitClientUnitDeclinationSuccess(Response):

    def __init__(self):

        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return SubmitClientUnitDeclinationSuccess()

    def to_inner_structure(self):

        return {}


class GetBulkClientUnitViewAndFilterDataSuccess(Response):
    def __init__(
        self, bu_group_name, csv_name, uploaded_by, uploaded_on,
        csv_id, total_records, le_names, div_names, cg_names,
        unit_locations, unit_codes, bu_domain_names,
        orga_names, client_unit_data
    ):
        self.bu_group_name = bu_group_name
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.csv_id = csv_id
        self.total_records = total_records
        self.le_names = le_names
        self.div_names = div_names
        self.cg_names = cg_names
        self.unit_locations = unit_locations
        self.unit_codes = unit_codes
        self.bu_domain_names = bu_domain_names
        self.orga_names = orga_names
        self.client_unit_data = client_unit_data

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, [
            "bu_group_name", "csv_name", "uploaded_by",
            "uploaded_on", "csv_id", "total_records", "le_names",
            "div_names", "cg_names", "unit_locations",
            "unit_codes", "bu_domain_names", "orga_names", "client_unit_data"
        ])

        return GetBulkClientUnitViewAndFilterDataSuccess(
            data.get("bu_group_name"), data.get("csv_name"),
            data.get("uploaded_by"), data.get("uploaded_on"),
            data.get("csv_id"), data.get("total_records"),
            data.get("le_names"), data.get("div_names"), data.get("cg_names"),
            data.get("unit_locations"), data.get("unit_codes"),
            data.get("bu_domain_names"), data.get("orga_names"),
            data.get("client_unit_data")
        )

    def to_inner_structure(self):

        return {
            "bu_group_name": self.bu_group_name,
            "csv_name": self.csv_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "csv_id": self.csv_id,
            "total_records": self.total_records,
            "le_names": self.le_names,
            "div_names": self.div_names,
            "cg_names": self.cg_names,
            "unit_locations": self.unit_locations,
            "unit_codes": self.unit_codes,
            "bu_domain_names": self.bu_domain_names,
            "orga_names": self.orga_names,
            "client_unit_data": self.client_unit_data
        }


class GetBulkClientUnitFilterDataSuccess(Response):

    def __init__(
        self, bu_group_name, csv_name, uploaded_by, uploaded_on, csv_id,
        total_records, client_unit_data
    ):
        self.bu_group_name = bu_group_name
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.csv_id = csv_id
        self.client_unit_data = client_unit_data
        self.total_records = total_records

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, [
            "bu_group_name", "csv_name", "uploaded_by",
            "uploaded_on", "csv_id",
            "total_records", "client_unit_data"
        ])

        return GetBulkClientUnitFilterDataSuccess(
            data.get("bu_group_name"), data.get("csv_name"),
            data.get("uploaded_by"), data.get("uploaded_on"),
            data.get("csv_id"), data.get("total_records"),
            data.get("client_unit_data")
        )

    def to_inner_structure(self):

        return {
            "bu_group_name": self.bu_group_name,
            "csv_name": self.csv_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "csv_id": self.csv_id,
            "total_records": self.total_records,
            "client_unit_data": self.client_unit_data
        }


class SubmitClientUnitActionFromListSuccess(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return SubmitClientUnitActionFromListSuccess()

    def to_inner_structure(self):

        return {}


class SaveClientUnitActionSuccess(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return SaveClientUnitActionSuccess()

    def to_inner_structure(self):

        return {}


class SubmitClientUnitActionFromListFailure(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return SubmitClientUnitActionFromListFailure()

    def to_inner_structure(self):
        return {}


class EmptyCSVUploaded(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return EmptyCSVUploaded()

    def to_inner_structure(self):
        return {}


class InvalidCSVUploaded(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return InvalidCSVUploaded()

    def to_inner_structure(self):
        return {}


class ClientUnitUploadMaxReached(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return ClientUnitUploadMaxReached()

    def to_inner_structure(self):
        return {}


class EmptyFilteredData(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return EmptyFilteredData()

    def to_inner_structure(self):
        return {}


class CSVColumnMisMatched(Response):

    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data)
        return CSVColumnMisMatched()

    def to_inner_structure(self):
        return {}


class CSVFileLinesMaxREached(Response):

    def __init__(self, csv_max_lines):
        self.csv_max_lines = csv_max_lines

    @staticmethod
    def parse_inner_structure(data):

        data = parse_dictionary(data, ["csv_max_lines"])
        return CSVFileLinesMaxREached(data.get("csv_max_lines"))

    def to_inner_structure(self):
        return {
            "csv_max_lines": self.csv_max_lines
        }


def _init_Response_class_map():

    classes = [
        UploadClientUnitBulkCSVSuccess,
        UploadClientUnitBulkCSVFailed,
        ClientUnitsUploadedCSVFilesListSuccess,
        UpdateUnitDownloadCountSuccess,
        GetClientUnitReportDataSuccess,
        ReturnDeclinedCount,
        UpdateApproveRejectActionFromListSuccess,
        SubmitClientUnitDeclinationSuccess,
        GetBulkClientUnitViewAndFilterDataSuccess,
        GetBulkClientUnitFilterDataSuccess,
        SubmitClientUnitActionFromListSuccess,
        SaveClientUnitActionSuccess,
        SubmitClientUnitActionFromListFailure,
        EmptyCSVUploaded, ClientUnitUploadMaxReached,
        InvalidCSVUploaded, EmptyFilteredData,
        CSVFileLinesMaxREached, CSVColumnMisMatched
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
