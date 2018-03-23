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
    def __init__(
        self, c_id, c_name, d_id, d_name, csv_name, csv_data, csv_size
    ):
        self.c_id = c_id
        self.c_name = c_name
        self.d_id = d_id
        self.d_name = d_name
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "c_name", "d_id", "d_name", "csv_name",
            "csv_data", "csv_size"
        ])
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


class GetSMBulkReportData(Request):
    def __init__(self, c_ids, d_ids, from_date, to_date, r_count, p_count,
                 child_ids, user_category_id):
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
        data = parse_dictionary(data, ["c_ids", "d_ids", "from_date",
                                       "to_date", "r_count", "p_count",
                                       "child_ids", "user_category_id"])
        return GetSMBulkReportData(
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
            "c_ids": self.c_ids, "d_ids": self.d_ids,
            "from_date": self.from_date, "to_date": self.to_date,
            "r_count": self.r_count, "p_count": self.p_count,
            "child_ids": self.child_ids,
            "user_category_id": self.user_category_id
            }


class ExportSMBulkReportData(Request):
    def __init__(self, c_ids, c_names, d_ids, d_names, from_date, to_date,
                 child_ids, user_category_id, csv):
        self.c_ids = c_ids
        self.c_names = c_names
        self.d_ids = d_ids
        self.d_names = d_names
        self.from_date = from_date
        self.to_date = to_date
        self.child_ids = child_ids
        self.user_category_id = user_category_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "c_names", "d_ids", "d_names",
                                       "from_date", "to_date", "child_ids",
                                       "user_category_id", "csv"])
        return ExportSMBulkReportData(
            data.get("c_ids"),
            data.get("c_names"),
            data.get("d_ids"),
            data.get("d_names"),
            data.get("from_date"),
            data.get("to_date"),
            data.get("child_ids"),
            data.get("user_category_id"),
            data.get("csv")
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.c_ids,
            "c_names": self.c_names,
            "d_ids": self.d_ids,
            "d_names": self.d_names,
            "from_date": self.from_date, "to_date": self.to_date,
            "child_ids": self.child_ids,
            "user_category_id": self.user_category_id,
            "csv": self.csv
            }


class UpdateDownloadCountToRejectedStatutory(Request):
    def __init__(self, csv_id):
        self.csv_id = csv_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id"])
        return UpdateDownloadCountToRejectedStatutory(
            data.get("csv_id")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id
        }


class GetRejectedStatutoryMappingBulkUploadData(Request):
    def __init__(self, c_id, d_id):
        self.c_id = c_id
        self.d_id = d_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "d_id"])
        return GetRejectedStatutoryMappingBulkUploadData(
            data.get("c_id"),
            data.get("d_id")
        )

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "d_id": self.d_id
        }


class DeleteRejectedSMCsvId(Request):
    def __init__(self, c_id, d_id, csv_id):
        self.c_id = c_id
        self.d_id = d_id
        self.csv_id = csv_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "d_id", "csv_id"])
        return DeleteRejectedSMCsvId(
            data.get("c_id"),
            data.get("d_id"),
            data.get("csv_id")
            )

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "d_id": self.d_id,
            "csv_id": self.csv_id
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
    def __init__(self, c_id, d_id, uploaded_by):
        self.c_id = c_id
        self.d_id = d_id
        self.uploaded_by = uploaded_by

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "d_id", "uploaded_by"])
        return GetApproveStatutoryMappingList(
            data.get("c_id"), data.get("d_id"),
            data.get("uploaded_by")
        )

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "d_id": self.d_id,
            "uploaded_by": self.uploaded_by
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
        self, csv_id, orga_name, s_nature, f_types, statutory, geo_location,
        c_task_name, c_desc, c_doc, f_count, r_range
    ):
        self.csv_id = csv_id
        self.orga_name = orga_name
        self.s_nature = s_nature
        self.f_types = f_types
        self.statutory = statutory
        self.geo_location = geo_location
        self.c_task_name = c_task_name
        self.c_desc = c_desc
        self.c_doc = c_doc
        self.f_count = f_count
        self.r_range = r_range

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "orga_name", "s_nature", "f_types", "statutory",
            "geo_location", "c_task_name", "c_desc", "c_doc",
            "f_count", "r_range"
        ])
        return GetApproveStatutoryMappingViewFilter(
            data.get("csv_id"), data.get("orga_name"), data.get("s_nature"),
            data.get("f_types"), data.get("statutory"),
            data.get("geo_location"),
            data.get("c_task_name"), data.get("c_desc"), data.get("c_doc"),
            data.get("f_count"), data.get("r_range")

        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "orga_name": self.orga_name,
            "s_nature": self.s_nature,
            "f_types": self.f_types,
            "statutory": self.statutory,
            "geo_location": self.geo_location,
            "c_task_name": self.c_task_name,
            "c_desc": self.c_desc,
            "c_doc": self.c_doc,
            "f_count": self.f_count,
            "r_range": self.r_range
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
            "csv_id": self.csv_id, "f_count": self.f_count,
            "r_range": self.r_range
        }


class SaveAction(Request):
    def __init__(self, sm_id, csv_id, bu_action, remarks):
        self.sm_id = sm_id
        self.csv_id = csv_id
        self.bu_action = bu_action
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "sm_id", "csv_id", "bu_action", "remarks"
        ])
        return SaveAction(
            data.get("sm_id"), data.get("csv_id"),
            data.get("bu_action"), data.get("remarks")
        )

    def to_inner_structure(self):
        return {
            "sm_id": self.sm_id,
            "csv_id": self.csv_id,
            "bu_action": self.bu_action,
            "remarks": self.remarks
        }


class UpdateApproveActionFromList(Request):
    def __init__(self, c_id, d_id, csv_id, bu_action, remarks, password):
        self.c_id = c_id
        self.d_id = d_id
        self.csv_id = csv_id
        self.bu_action = bu_action
        self.remarks = remarks
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "d_id",
            "csv_id", "bu_action", "remarks", "password"
        ])
        return UpdateApproveActionFromList(
            data.get("c_id"), data.get("d_id"),
            data.get("csv_id"), data.get("bu_action"), data.get("remarks"),
            data.get("password")
        )

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "d_id": self.d_id,
            "csv_id": self.csv_id,
            "bu_action": self.bu_action,
            "remarks": self.remarks,
            "password": self.password
        }


class ConfirmStatutoryMappingSubmit(Request):
    def __init__(self, csv_id, c_id, d_id):
        self.csv_id = csv_id
        self.c_id = c_id
        self.d_id = d_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "c_id", "d_id"])
        return ConfirmStatutoryMappingSubmit(
            data.get("csv_id"), data.get("c_id"), data.get("d_id"),
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "c_id": self.c_id,
            "d_id": self.d_id,
        }


class SubmitStatutoryMapping(Request):
    def __init__(self, csv_id, c_id, d_id, password):
        self.csv_id = csv_id
        self.c_id = c_id
        self.d_id = d_id
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "c_id", "d_id", "password"])
        return SubmitStatutoryMapping(
            data.get("csv_id"), data.get("c_id"), data.get("d_id"),
            data.get("password")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "c_id": self.c_id,
            "d_id": self.d_id,
            "password": self.password
        }


# SM - Statutory Mapping

class DownloadRejectedSMReportData(Request):
    def __init__(self, csv_id, c_id, d_id, download_format):
        self.csv_id = csv_id
        self.c_id = c_id
        self.d_id = d_id
        self.download_format = download_format

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "c_id", "d_id",
                                       "download_format"])
        return DownloadRejectedSMReportData(
            data.get("csv_id"), data.get("c_id"),
            data.get("d_id"), data.get("download_format")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "c_id": self.c_id,
            "d_id": self.d_id,
            "download_format": self.download_format
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
        ConfirmStatutoryMappingSubmit,
        GetSMBulkReportData,
        GetRejectedStatutoryMappingBulkUploadData,
        DeleteRejectedSMCsvId,
        UpdateDownloadCountToRejectedStatutory,
        ExportSMBulkReportData,
        DownloadRejectedSMReportData,
        SaveAction
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()


class CsvList(object):
    def __init__(
        self, c_id, c_name, d_id, d_name, csv_id, csv_name,
        no_of_records, no_of_documents, uploaded_documents,
        uploaded_on
    ):
        self.c_id = c_id
        self.c_name = c_name
        self.d_id = d_id
        self.d_name = d_name
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.no_of_records = no_of_records
        self.no_of_documents = no_of_documents
        self.uploaded_documents = uploaded_documents
        self.uploaded_on = uploaded_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_id", "c_name", "d_id", "d_name", "csv_id", "csv_name",
            "no_of_records", "no_of_documents", "uploaded_documents",
            "uploaded_on"
        ])
        return CsvList(
            data.get("c_id"), data.get("c_name"), data.get("d_id"),
            data.get("d_name"), data.get("csv_id"), data.get("csv_name"),
            data.get("no_of_records"), data.get("no_of_documents"),
            data.get("uploaded_documents"),
            data.get("uploaded_on")
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
            "uploaded_documents": self.uploaded_documents,
            "uploaded_on": self.uploaded_on
        }


class ReportData(object):

    def __init__(self, country_name, domain_name, uploaded_by,
                 uploaded_on, csv_name_text, total_records,
                 total_rejected_records, approved_by, rejected_by, approved_on,
                 rejected_on, is_fully_rejected, total_approve_records,
                 rejected_reason):

        self.country_name = country_name
        self.domain_name = domain_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.csv_name_text = csv_name_text
        self.total_records = total_records
        self.total_rejected_records = total_rejected_records
        self.approved_by = approved_by
        self.rejected_by = rejected_by
        self.approved_on = approved_on
        self.rejected_on = rejected_on
        self.is_fully_rejected = is_fully_rejected
        self.total_approve_records = total_approve_records
        self.rejected_reason = rejected_reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_name", "domain_name",
                                       "uploaded_by", "uploaded_on",
                                       "csv_name_text", "total_records",
                                       "total_rejected_records", "approved_by",
                                       "rejected_by", "approved_on",
                                       "rejected_on", "is_fully_rejected",
                                       "total_approve_records",
                                       "rejected_reason"])
        return ReportData(
            data.get("country_name"),
            data.get("domain_name"),
            data.get("uploaded_by"),
            data.get("uploaded_on"),
            data.get("csv_name_text"),
            data.get("total_records"),
            data.get("total_rejected_records"),
            data.get("approved_by"),
            data.get("rejected_by"),
            data.get("approved_on"),
            data.get("rejected_on"),
            data.get("is_fully_rejected"),
            data.get("total_approve_records"),
            data.get("rejected_reason")
        )

    def to_structure(self):
        return {
            "country_name": self.country_name,
            "domain_name": self.domain_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "csv_name_text": self.csv_name_text,
            "total_records": self.total_records,
            "total_rejected_records": self.total_rejected_records,
            "approved_by": self.approved_by,
            "rejected_by": self.rejected_by,
            "approved_on": self.approved_on,
            "rejected_on": self.rejected_on,
            "is_fully_rejected": self.is_fully_rejected,
            "total_approve_records": self.total_approve_records,
            "rejected_reason": self.rejected_reason
            }


class StatutoryMappingRejectData(object):
    def __init__(self, csv_id, uploaded_by, uploaded_on, csv_name_text,
                 total_records, total_rejected_records, approved_by,
                 rejected_by, approved_on, rejected_on, is_fully_rejected,
                 approve_status, file_download_count, remarks,
                 statutory_action, declined_count, rejected_reason):

        self.csv_id = csv_id
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.csv_name_text = csv_name_text
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
        self.rejected_reason = rejected_reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["csv_id", "uploaded_by", "uploaded_on",
                                       "csv_name_text", "total_records",
                                       "total_rejected_records",
                                       "approved_by", "rejected_by",
                                       "approved_on", "rejected_on",
                                       "is_fully_rejected", "approve_status",
                                       "file_download_count", "remarks",
                                       "statutory_action", "declined_count",
                                       "rejected_reason"])
        return StatutoryMappingRejectData(
            data.get("csv_id"),
            data.get("uploaded_by"),
            data.get("uploaded_on"),
            data.get("csv_name_text"),
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
            data.get("declined_count"),
            data.get("rejected_reason")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "csv_name_text": self.csv_name_text,
            "total_records": self.total_records,
            "total_rejected_records": self.total_rejected_records,
            "rejected_by": self.rejected_by,
            "approved_on": self.approved_on,
            "approved_by": self.approved_by,
            "rejected_on": self.rejected_on,
            "is_fully_rejected": self.is_fully_rejected,
            "approve_status": self.approve_status,
            "file_download_count": self.file_download_count,
            "remarks": self.remarks,
            "statutory_action": self.statutory_action,
            "declined_count": self.declined_count,
            "rejected_reason": self.rejected_reason
            }


class SMRejectUpdateDownloadCount(object):
    def __init__(self, csv_id, download_count):
        self.csv_id = csv_id
        self.download_count = download_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["csv_id", "download_count"])
        return SMRejectUpdateDownloadCount(
            data.get("csv_id"),
            data.get("download_count")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "download_count": self.download_count
            }


class StatutoryReportData(object):

    def __init__(self, uploaded_by, uploaded_on, csv_name_text, total_records,
                 total_rejected_records, approved_by, rejected_by, approved_on,
                 rejected_on, is_fully_rejected, approve_status):
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.csv_name_text = csv_name_text
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
            "uploaded_by", "uploaded_on", "csv_name_text", "total_records",
            "total_rejected_records", "approved_by", "rejected_by",
            "approved_on", "rejected_on", "is_fully_rejected",
            "approve_status"])
        return StatutoryReportData(
            data.get("uploaded_by"),
            data.get("uploaded_on"),
            data.get("csv_name_text"),
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
            "uploaded_on": self.uploaded_on,
            "csv_name_text": self.csv_name_text,
            "total_records": self.total_records,
            "total_rejected_records": self.total_rejected_records,
            "rejected_by": self.rejected_by,
            "approved_on": self.approved_on,
            "rejected_on": self.rejected_on,
            "is_fully_rejected": self.is_fully_rejected,
            "approve_status": self.approve_status
            }


class SMRejectedDownload(object):
    def __init__(self, xlsx_link, csv_link, ods_link, txt_link):
        self.xlsx_link = xlsx_link
        self.csv_link = csv_link
        self.ods_link = ods_link
        self.txt_link = txt_link

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "xlsx_link", "csv_link", "ods_link", "txt_link"
        ])
        return SMRejectedDownload(
            data.get("xlsx_link"),
            data.get("csv_link"),
            data.get("ods_link"),
            data.get("txt_link")
        )

    def to_structure(self):
        return {
            "xlsx_link": self.xlsx_link,
            "csv_link": self.csv_link,
            "ods_link": self.ods_link,
            "txt_link": self.txt_link
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
        uploaded_on, no_of_records, approve_count, rej_count, download_file
    ):
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.no_of_records = no_of_records
        self.approve_count = approve_count
        self.rej_count = rej_count
        self.download_file = download_file

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "csv_name", "uploaded_by", "uploaded_on",
            "no_of_records", "approve_count", "rej_count", "download_file"

        ])
        return PendingCsvList(
            data.get("csv_id"), data.get("csv_name"),
            data.get("csv_id"), data.get("csv_name"), data.get("uploaded_by"),
            data.get("uploaded_on"), data.get("no_of_records"),
            data.get("approve_count"),
            data.get("rej_count"),
            data.get("download_file")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "csv_name": self.csv_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "no_of_records": self.no_of_records,
            "approve_count": self.approve_count,
            "rej_count": self.rej_count,
            "download_file": self.download_file
        }


class MappingData(object):
    def __init__(
        self, sm_id, orga_name, geo_location, s_nature, statutory, s_provision,
        c_task_name, c_doc, c_desc, p_cons, refer, frequency, statu_month,
        statu_date, trigger_before, r_every, r_type, r_by,
        dur, dur_type, multiple_input, format_file, bu_action, bu_remarks,
        task_id, task_type
    ):
        self.sm_id = sm_id
        self.orga_name = orga_name
        self.geo_location = geo_location
        self.s_nature = s_nature
        self.statutory = statutory
        self.s_provision = s_provision
        self.c_task_name = c_task_name
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
        self.task_id = task_id
        self.task_type = task_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "sm_id",
            "orga_name",
            "geo_location",
            "s_nature",
            "statutory",
            "s_provision",
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
            "task_id", "task_type"

        ])
        return MappingData(
            data.get("sm_id"),
            data.get("orga_name"),
            data.get("geo_location"),
            data.get("s_nature"),
            data.get("statutory"),
            data.get("s_provision"),
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
            data.get("task_id"), data.get("task_type")
        )

    def to_structure(self):
        return {
            "sm_id": self.sm_id,
            "orga_name": self.orga_name,
            "geo_location": self.geo_location,
            "s_nature": self.s_nature,
            "statutory": self.statutory,
            "s_provision": self.s_provision,
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
            "task_id": self.task_id,
            "task_type": self.task_type
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


class UploadStatutoryMappingCSVValidSuccess(Response):
    def __init__(self, csv_id, total, valid, invalid, doc_count, doc_names):
        self.csv_id = csv_id
        self.total = total
        self.valid = valid
        self.invalid = invalid
        self.doc_count = doc_count
        self.doc_names = doc_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "csv_id",
            "total", "valid", "invalid", "doc_count", "doc_names"
        ])

        return UploadStatutoryMappingCSVValidSuccess(
            data.get("csv_id"),
            data.get("total"), data.get("valid"), data.get("invalid"),
            data.get("doc_count"), data.get("doc_names")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id,
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid,
            "doc_count": self.doc_count,
            "doc_names": self.doc_names
        }


class GetSMBulkReportDataSuccess(Response):
    def __init__(self, reportdata, total):
        self.reportdata = reportdata
        self.total = total

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["reportdata"], ["total"])

        return GetSMBulkReportDataSuccess(
            data.get("reportdata"),
            data.get("total")
        )

    def to_inner_structure(self):
        return {
            "reportdata": self.reportdata,
            "total": self.total
        }


class RejectedSMBulkDataSuccess(Response):
    def __init__(self, rejected_data):
        self.rejected_data = rejected_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["rejected_data"])
        return RejectedSMBulkDataSuccess(
            data.get("rejected_data")
        )

    def to_inner_structure(self):
        return {
            "rejected_data": self.rejected_data
        }


class SMRejecteUpdatedDownloadCountSuccess(Response):
    def __init__(self, updated_count):
        self.updated_count = updated_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["updated_count"])
        return SMRejecteUpdatedDownloadCountSuccess(
            data.get("updated_count")
        )

    def to_inner_structure(self):
        return {
            "updated_count": self.updated_count
        }


class DeleteRejectedStatutoryMappingSuccess(Response):
    def __init__(self, rejected_data):
        self.rejected_data = rejected_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["rejected_data"])
        return DeleteRejectedStatutoryMappingSuccess(
            data.get("rejected_data")
        )

    def to_inner_structure(self):
        return {
            "rejected_data": self.rejected_data
        }


class UploadStatutoryMappingCSVInvalidSuccess(Response):
    def __init__(
        self, invalid_file, mandatory_error, max_length_error, duplicate_error,
        invalid_char_error, invalid_data_error, inactive_error,
        total, invalid, valid

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
        self.valid = valid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "invalid_file", "mandatory_error", "max_length_error",
            "duplicate_error",
            "invalid_char_error", "invalid_data_error", "inactive_error",
            "total", "invalid", "valid"
        ])
        return UploadStatutoryMappingCSVInvalidSuccess(
            data.get("invalid_file"), data.get("mandatory_error"),
            data.get("max_length_error"), data.get("duplicate_error"),
            data.get("invalid_char_error"), data.get("invalid_data_error"),
            data.get("inactive_error"),
            data.get("total"),
            data.get("invalid"), data.get("valid")
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
            "total": self.total,
            "invalid": self.invalid,
            "valid": self.valid
        }


class GetRejectedStatutoryMappingListSuccess(Response):
    def __init__(self, rejected_list):
        self.rejected_list = rejected_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["rejected_list"])
        return GetRejectedStatutoryMappingListSuccess(
                                                      data.get("rejected_list")
                                                      )

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
        c_docs, task_ids, task_types
    ):
        self.orga_names = orga_names
        self.s_natures = s_natures
        self.statutories = statutories
        self.frequencies = frequencies
        self.geo_locations = geo_locations
        self.c_tasks = c_tasks
        self.c_descs = c_descs
        self.c_docs = c_docs
        self.task_ids = task_ids
        self.task_types = task_types

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "orga_names", "s_natures", "statutories",
            "frequencies", "geo_locations", "c_tasks",
            "c_descs", "c_docs", "task_ids", "task_types"
        ])
        return GetApproveMappingFilterSuccess(
            data.get("orga_names"),
            data.get("s_natures"),
            data.get("statutories"),
            data.get("frequencies"),
            data.get("geo_locations"),
            data.get("c_tasks"),
            data.get("c_descs"),
            data.get("c_docs"),
            data.get("task_ids"),
            data.get("task_types")
        )

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
            "task_ids": self.task_ids,
            "task_types": self.task_types
        }


class GetApproveStatutoryMappingViewSuccess(Response):
    def __init__(
        self, c_name, d_name, csv_name, uploaded_by, uploaded_on,
        csv_id, mapping_data, total
    ):
        self.c_name = c_name
        self.d_name = d_name
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.csv_id = csv_id
        self.mapping_data = mapping_data
        self.total = total

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_name", "d_name", "csv_name",
            "uploaded_by", "uploaded_on", "csv_id", "mapping_data",
            "total"
        ])
        return GetApproveStatutoryMappingViewSuccess(
            data.get("c_name"),
            data.get("d_name"),
            data.get("csv_name"),
            data.get("uploaded_by"),
            data.get("uploaded_on"),
            data.get("csv_id"),
            data.get("mapping_data"),
            data.get("total")
        )

    def to_inner_structure(self):
        return {
            "c_name": self.c_name,
            "d_name": self.d_name,
            "csv_name": self.csv_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "csv_id": self.csv_id,
            "mapping_data": self.mapping_data,
            "total": self.total
        }


class SaveActionSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveActionSuccess()

    def to_inner_structure(self):
        return {}


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


class ValidationSuccess(Response):
    def __init__(self, rej_count):
        self.rej_count = rej_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["rej_count"])
        return ValidationSuccess(data.get("rej_count"))

    def to_inner_structure(self):
        return {
            "rej_count": self.rej_count
        }


class DownloadActionSuccess(Response):
    def __init__(self, xlsx_link, csv_link, ods_link, txt_link):
        self.xlsx_link = xlsx_link
        self.csv_link = csv_link
        self.ods_link = ods_link
        self.txt_link = txt_link

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["xlsx_link", "csv_link", "ods_link",
                                       "txt_link"])
        return ValidationSuccess(data.get("xlsx_link"), data.get("csv_link"),
                                 data.get("ods_link"), data.get("txt_link"))

    def to_inner_structure(self):
        return {
            "xlsx_link": self.xlsx_link,
            "csv_link": self.csv_link,
            "ods_link": self.ods_link,
            "txt_link": self.txt_link
            }


def _init_Response_class_map():
    classes = [
        GetStatutoryMappingCsvUploadedListSuccess,
        UploadStatutoryMappingCSVValidSuccess,
        UploadStatutoryMappingCSVInvalidSuccess,
        GetRejectedStatutoryMappingListSuccess,
        RemoveRejectedDataSuccess,
        GetApproveStatutoryMappingListSuccess,
        GetApproveMappingFilterSuccess,
        GetApproveStatutoryMappingViewSuccess,
        UpdateApproveActionFromListSuccess,
        SubmitStatutoryMappingSuccess,
        ValidationSuccess,
        GetSMBulkReportDataSuccess,
        RejectedSMBulkDataSuccess,
        DeleteRejectedStatutoryMappingSuccess,
        SMRejecteUpdatedDownloadCountSuccess,
        DownloadActionSuccess,
        SaveActionSuccess
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
