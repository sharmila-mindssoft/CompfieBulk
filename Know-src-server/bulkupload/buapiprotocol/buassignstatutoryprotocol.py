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

class DownloadAssignStatutory(Request):
    def __init__( self, cl_id, le_id, d_ids, u_ids, cl_name, le_name, d_names, u_names):
        self.cl_id = cl_id
        self.le_id = le_id
        self.d_ids = d_ids
        self.u_ids = u_ids
        self.cl_name = cl_name
        self.le_name = le_name
        self.d_names = d_names
        self.u_names = u_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["cl_id", "le_id", "d_ids", "u_ids", "cl_name", "le_name", "d_names", "u_names"])
        return DownloadAssignStatutory(
            data.get("cl_id"), data.get("le_id"), data.get("d_ids"), data.get("u_ids"),
            data.get("cl_name"), data.get("le_name"), data.get("d_names"), data.get("u_names")
        )

    def to_inner_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "d_ids": self.d_ids,
            "u_ids": self.u_ids,
            "cl_name": self.cl_name,
            "le_name": self.le_name,
            "d_names": self.d_names,
            "u_names": self.u_names,
        }

class UploadAssignStatutoryCSV(Request):
    def __init__(self, csv_name, csv_data, csv_size, cl_id, le_id, d_ids, le_name, d_names):
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size
        self.cl_id = cl_id
        self.le_id = le_id
        self.d_ids = d_ids
        self.le_name = le_name
        self.d_names = d_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_name", "csv_data", "csv_size", "cl_id", "le_id", "d_ids", "le_name", "d_names"])
        return UploadAssignStatutoryCSV(
            data.get("csv_name"), data.get("csv_data"), data.get("csv_size"), data.get("cl_id"), data.get("le_id"), data.get("d_ids"),
            data.get("le_name"), data.get("d_names")
        )

    def to_inner_structure(self):
        return {
            "csv_name": self.csv_name,
            "csv_data": self.csv_data,
            "csv_size": self.csv_size,
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "d_ids": self.d_ids,
            "le_name": self.le_name,
            "d_names": self.d_names
        }

class GetAssignStatutoryForApprove(Request):
    def __init__(self, cl_id, le_id):
        self.cl_id = cl_id
        self.le_id = le_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["cl_id", "le_id"])
        return GetAssignStatutoryForApprove(
            data.get("cl_id"), data.get("le_id")
        )

    def to_inner_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id
        }

class GetRejectedAssignSMData(Request):
    def __init__(self, client_id, le_id, domain_ids, asm_unit_code):
        self.client_id = client_id
        self.le_id = le_id
        self.domain_ids = domain_ids
        self.asm_unit_code = asm_unit_code

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "le_id", "domain_ids", "asm_unit_code"])
        return GetRejectedAssignSMData(
            data.get("client_id"),
            data.get("le_id"),
            data.get("domain_ids"),
            data.get("asm_unit_code")
        )
    def to_inner_structure(self):
        return {
            "client_id": self.c_id,
            "le_id": self.d_id,
            "domain_ids": self.domain_ids,
            "asm_unit_code": self.asm_unit_code
        }
class UpdateASMClickCount(Request):
    def __init__(self, csv_id):
        self.csv_id = csv_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id"])
        return UpdateASMClickCount(
            data.get("csv_id")
        )

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id
        }

class DeleteRejectedASMByCsvID(Request):
    def __init__(self, client_id, le_id, domain_ids, asm_unit_code, csv_id):
        self.client_id = client_id
        self.le_id = le_id
        self.domain_ids = domain_ids
        self.asm_unit_code = asm_unit_code
        self.csv_id = csv_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "le_id", "domain_ids", "asm_unit_code", "csv_id"])
        return DeleteRejectedASMByCsvID(
            data.get("client_id"),
            data.get("le_id"),
            data.get("domain_ids"),
            data.get("asm_unit_code"),
            data.get("csv_id")
            )

    def to_inner_structure(self):
        return {
            "client_id":self.client_id,
            "le_id":self.le_id,
            "domain_ids":self.domain_ids,
            "asm_unit_code":self.asm_unit_code,
            "csv_id":self.csv_id
            }


class GetAssignedStatutoryBulkReportData(Request):
    def __init__(self, bu_client_id, bu_legal_entity_id, bu_unit_id, domain_ids,
     from_date, to_date, r_count, p_count, child_ids, user_category_id):
        self.bu_client_id = bu_client_id
        self.bu_legal_entity_id = bu_legal_entity_id
        self.bu_unit_id = bu_unit_id
        self.domain_ids = domain_ids
        self.from_date = from_date
        self.to_date = to_date
        self.r_count = r_count
        self.p_count = p_count
        self.child_ids = child_ids
        self.user_category_id = user_category_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_client_id", "bu_legal_entity_id",
            "bu_unit_id", "domain_ids", "from_date", "to_date", "r_count", "p_count",
            "child_ids", "user_category_id"])
        return GetAssignedStatutoryBulkReportData(
            data.get("bu_client_id"),
            data.get("bu_legal_entity_id"),
            data.get("bu_unit_id"),
            data.get("domain_ids"),
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
            "domain_ids":self.domain_ids,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "r_count": self.r_count,
            "p_count": self.p_count,
            "child_ids":self.child_ids,
            "user_category_id":self.user_category_id
        }


class ExportASBulkReportData(Request):
    def __init__(self, bu_client_id, bu_group_name, bu_legal_entity_id,
                 legal_entity_name, bu_unit_id, unit_name,
                 domain_ids, d_names, from_date, to_date, child_ids,
                 user_category_id, csv):
        self.bu_client_id = bu_client_id
        self.bu_group_name = bu_group_name
        self.bu_legal_entity_id = bu_legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.bu_unit_id = bu_unit_id
        self.unit_name = unit_name
        self.domain_ids = domain_ids
        self.d_names = d_names
        self.from_date = from_date
        self.to_date = to_date
        self.child_ids = child_ids
        self.user_category_id = user_category_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
                data, ["bu_client_id", "bu_group_name", "bu_legal_entity_id",
                       "legal_entity_name", "bu_unit_id", "unit_name",
                       "domain_ids", "d_names", "from_date", "to_date",
                       "child_ids", "user_category_id", "csv"])
        return ExportASBulkReportData(
            data.get("bu_client_id"),
            data.get("bu_group_name"),
            data.get("bu_legal_entity_id"),
            data.get("legal_entity_name"),
            data.get("bu_unit_id"),
            data.get("unit_name"),
            data.get("domain_ids"),
            data.get("d_names"),
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
            "bu_legal_entity_id": self.bu_legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "bu_unit_id": self.bu_unit_id,
            "unit_name": self.unit_name,
            "domain_ids": self.domain_ids,
            "d_names": self.d_names,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "child_ids": self.child_ids,
            "user_category_id": self.user_category_id,
            "csv": self.csv
        }


class DownloadRejectedASMReport(Request):
    def __init__(self, client_id, le_id, domain_ids,
                 asm_unit_code, csv_id, download_format):
        self.client_id = client_id
        self.le_id = le_id
        self.domain_ids = domain_ids
        self.asm_unit_code = asm_unit_code
        self.csv_id = csv_id
        self.download_format = download_format

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "le_id", "domain_ids",
            "asm_unit_code", "csv_id", "download_format"])
        return DownloadRejectedASMReport(
            data.get("client_id"), data.get("le_id"),
            data.get("domain_ids"), data.get("asm_unit_code"),
            data.get("csv_id"), data.get("download_format"))

    def to_inner_structure(self):
        return {
            "client_id": self.client_id,
            "le_id": self.le_id,
            "domain_ids": self.domain_ids,
            "asm_unit_code": self.asm_unit_code,
            "csv_id": self.csv_id,
            "download_format": self.download_format
        }


class GetAssignStatutoryFilters(Request):
    def __init__(self, csv_id):
        self.csv_id = csv_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id"])
        return GetAssignStatutoryFilters(data.get("csv_id"))

    def to_inner_structure(self):
        return {
            "csv_id": self.csv_id
        }

class ViewAssignStatutoryData(Request):
    def __init__(self, csv_id, f_count, r_range):
        self.csv_id = csv_id
        self.f_count = f_count
        self.r_range = r_range

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "f_count", "r_range"])
        return ViewAssignStatutoryData(
            data.get("csv_id"), data.get("f_count"), data.get("r_range")
        )

    def to_inner_structure(self):
        return {
            "csv_id" : self.csv_id,
            "f_count" : self.f_count,
            "r_range" : self.r_range,
        }

class ViewAssignStatutoryDataFromFilter(Request):
    def __init__(self, csv_id, f_count, r_range, filter_d_name, filter_u_name, filter_p_leg,
        s_leg, s_prov, c_task, c_desc, filter_view_data, s_status, c_status):
        self.csv_id = csv_id
        self.f_count = f_count
        self.r_range = r_range
        self.filter_d_name = filter_d_name
        self.filter_u_name = filter_u_name
        self.filter_p_leg = filter_p_leg
        self.s_leg = s_leg
        self.s_prov = s_prov
        self.c_task = c_task
        self.c_desc = c_desc
        self.filter_view_data = filter_view_data
        self.s_status = s_status
        self.c_status = c_status


    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_id", "f_count", "r_range", "filter_d_name",
        "filter_u_name", "filter_p_leg", "s_leg", "s_prov", "c_task", "c_desc",
        "filter_view_data", "s_status", "c_status"])
        return ViewAssignStatutoryDataFromFilter(
            data.get("csv_id"),
            data.get("f_count"),
            data.get("r_range"),
            data.get("filter_d_name"),
            data.get("filter_u_name"),
            data.get("filter_p_leg"),
            data.get("s_leg"),
            data.get("s_prov"),
            data.get("c_task"),
            data.get("c_desc"),
            data.get("filter_view_data"),
            data.get("s_status"),
            data.get("c_status")


        )

    def to_inner_structure(self):
        return {
            "csv_id" : self.csv_id,
            "f_count" : self.f_count,
            "r_range" : self.r_range,
            "filter_d_name" : self.filter_d_name,
            "filter_u_name" : self.filter_u_name,
            "filter_p_leg" : self.filter_p_leg,
            "s_leg" : self.s_leg,
            "s_prov" : self.s_prov,
            "c_task" : self.c_task,
            "c_desc" : self.c_desc,
            "filter_view_data" : self.filter_view_data,
            "s_status" : self.s_status,
            "c_status" : self.c_status,

        }

class AssignStatutoryApproveActionInList(Request):
    def __init__(self, cl_id, le_id, csv_id, bu_action, remarks, password):
        self.cl_id = cl_id
        self.le_id = le_id
        self.csv_id = csv_id
        self.bu_action = bu_action
        self.remarks = remarks
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "le_id",
            "csv_id", "bu_action", "remarks", "password"
        ])
        return AssignStatutoryApproveActionInList(
            data.get("cl_id"), data.get("le_id"),
            data.get("csv_id"), data.get("bu_action"), data.get("remarks"),
            data.get("password")
        )

    def to_inner_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "csv_id": self.csv_id,
            "bu_action": self.bu_action,
            "remarks": self.remarks,
            "password": self.password
        }

def _init_Request_class_map():
    classes = [

        GetClientInfo, DownloadAssignStatutory, UploadAssignStatutoryCSV,
        GetAssignStatutoryForApprove, GetAssignStatutoryFilters,
        ViewAssignStatutoryData, ViewAssignStatutoryDataFromFilter,
        AssignStatutoryApproveActionInList,
        GetAssignStatutoryForApprove, GetRejectedAssignSMData,
        UpdateASMClickCount, DeleteRejectedASMByCsvID,
        GetAssignedStatutoryBulkReportData, DownloadRejectedASMReport,
        ExportASBulkReportData
    ]

    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()




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
        self, cl_id, le_id, le_name, bu_domains
    ):
        self.cl_id = cl_id
        self.le_id = le_id
        self.le_name = le_name
        self.bu_domains = bu_domains

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "le_id", "le_name", "bu_domains"
        ])
        return LegalEntites(
            data.get("cl_id"), data.get("le_id"), data.get("le_name"), data.get("bu_domains")
        )

    def to_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "le_name": self.le_name,
            "bu_domains": self.bu_domains
        }

class Units(object):
    def __init__(
        self, cl_id, le_id, u_id, u_name, d_ids
    ):
        self.cl_id = cl_id
        self.le_id = le_id
        self.u_id = u_id
        self.u_name = u_name
        self.d_ids = d_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "le_id", "u_id", "u_name", "d_ids"
        ])
        return Units(
            data.get("cl_id"), data.get("le_id"), data.get("u_id"), data.get("u_name"), data.get("d_ids")
        )

    def to_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "u_id": self.u_id,
            "u_name": self.u_name,
            "d_ids": self.d_ids
        }

class Domains(object):
    def __init__(
        self, d_id, d_name
    ):
        self.d_id = d_id
        self.d_name = d_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "d_id", "d_name"
        ])
        return Units(
            data.get("d_id"), data.get("d_name")
        )

    def to_structure(self):
        return {
            "d_id": self.d_id,
            "d_name": self.d_name
        }


class PendingCsvListAssignStatutory(object):
    def __init__(
        self, csv_id, csv_name, uploaded_by,
        uploaded_on, no_of_records, approved_count, rej_count, download_file
    ):
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.no_of_records = no_of_records
        self.approved_count = approved_count
        self.rej_count = rej_count
        self.download_file = download_file

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "csv_name", "uploaded_by", "uploaded_on",
            "no_of_records", "approved_count", "rej_count", "download_file"

        ])
        return PendingCsvListAssignStatutory(
            data.get("csv_id"), data.get("csv_name"), data.get("uploaded_by"),
            data.get("uploaded_on"), data.get("no_of_records"), data.get("approved_count"),
            data.get("rej_count"), data.get("download_file")
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
            "download_file": self.download_file
        }

class AssignStatutoryData(object):
    def __init__(
        self, as_id, u_location, u_code, u_name, d_name, org_name, p_leg,
        s_leg, s_prov, c_task, c_desc, s_status, s_remarks, c_status,
        bu_action, remarks
    ):
        self.as_id = as_id
        self.u_location = u_location
        self.u_code = u_code
        self.u_name = u_name
        self.d_name = d_name
        self.org_name = org_name
        self.p_leg = p_leg
        self.s_leg = s_leg
        self.s_prov = s_prov
        self.c_task = c_task
        self.c_desc = c_desc
        self.s_status = s_status
        self.s_remarks = s_remarks
        self.c_status = c_status
        self.bu_action = bu_action
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "as_id",
            "u_location",
            "u_code",
            "u_name",
            "d_name",
            "org_name",
            "p_leg",
            "s_leg",
            "s_prov",
            "c_task",
            "c_desc",
            "s_status",
            "s_remarks",
            "c_status",
            "bu_action",
            "remarks"

        ])
        return AssignStatutoryData(
            data.get("as_id"),
            data.get("u_location"),
            data.get("u_code"),
            data.get("u_name"),
            data.get("d_name"),
            data.get("org_name"),
            data.get("p_leg"),
            data.get("s_leg"),
            data.get("s_prov"),
            data.get("c_task"),
            data.get("c_desc"),
            data.get("s_status"),
            data.get("s_remarks"),
            data.get("c_status"),
            data.get("bu_action"),
            data.get("remarks")
        )

    def to_structure(self):
        return {
            "as_id": self.as_id,
            "u_location": self.u_location,
            "u_code": self.u_code,
            "u_name": self.u_name,
            "d_name": self.d_name,
            "org_name": self.org_name,
            "p_leg": self.p_leg,
            "s_leg": self.s_leg,
            "s_prov": self.s_prov,
            "c_task": self.c_task,
            "c_desc": self.c_desc,
            "s_status": self.s_status,
            "s_remarks": self.s_remarks,
            "c_status": self.c_status,
            "bu_action": self.bu_action,
            "remarks": self.remarks
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
    def __init__(self, bu_clients, bu_legalentites, bu_units):
        self.bu_clients = bu_clients
        self.bu_legalentites = bu_legalentites
        self.bu_units = bu_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["bu_clients", "bu_legalentites", "bu_units"])
        bu_clients = data.get("bu_clients")
        bu_legalentites = data.get("bu_legalentites")
        bu_units = data.get("bu_units")
        return GetClientInfoSuccess(
            bu_clients, bu_legalentites, bu_units
        )

    def to_inner_structure(self):
        return {
            "bu_clients": self.bu_clients,
            "bu_legalentites": self.bu_legalentites,
            "bu_units": self.bu_units

        }

class DownloadAssignStatutorySuccess(Response):
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["link"])
        link = data.get("link")

        return DownloadAssignStatutorySuccess(
            link
        )

    def to_inner_structure(self):
        return {
            "link": self.link
        }


class UploadAssignStatutoryCSVSuccess(Response):
    def __init__(self, total, valid, invalid):
        self.total = total
        self.valid = valid
        self.invalid = invalid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total", "valid", "invalid"])
        return UploadAssignStatutoryCSVSuccess(
            data.get("total"), data.get("valid"), data.get("invalid")
        )

    def to_inner_structure(self):
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid
        }


class UploadAssignStatutoryCSVFailed(Response):
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
        return UploadAssignStatutoryCSVFailed(
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

class GetAssignStatutoryForApproveSuccess(Response):
    def __init__(self, pending_csv_list_as):
        self.pending_csv_list_as = pending_csv_list_as

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["pending_csv_list_as"])
        return GetAssignStatutoryForApproveSuccess(
            data.get("pending_csv_list_as")
        )

    def to_inner_structure(self):
        return {
            "pending_csv_list_as": self.pending_csv_list_as
        }

class GetAssignStatutoryFiltersSuccess(Response):
    def __init__(
        self, d_names, u_names, p_legis,
        s_legis, s_provs, c_tasks, c_descs
    ):
        self.d_names = d_names
        self.u_names = u_names
        self.p_legis = p_legis
        self.s_legis = s_legis
        self.s_provs = s_provs
        self.c_tasks = c_tasks
        self.c_descs = c_descs

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "d_names", "u_names", "p_legis",
            "s_legis", "s_provs", "c_tasks",
            "c_descs"
        ])
        return {
            "d_names": data.get("d_names"),
            "u_names": data.get("u_names"),
            "p_legis": data.get("p_legis"),
            "s_legis": data.get("s_legis"),
            "s_provs": data.get("s_provs"),
            "c_tasks": data.get("c_tasks"),
            "c_descs": data.get("c_descs"),
        }

    def to_inner_structure(self):
        return {
            "d_names": self.d_names,
            "u_names": self.u_names,
            "p_legis": self.p_legis,
            "s_legis": self.s_legis,
            "s_provs": self.s_provs,
            "c_tasks": self.c_tasks,
            "c_descs": self.c_descs,
        }

class ViewAssignStatutoryDataSuccess(Response):
    def __init__(self, csv_id, csv_name, cl_name, le_name, uploaded_by, uploaded_on, assign_statutory_data_list, count):
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.cl_name = cl_name
        self.le_name = le_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.assign_statutory_data_list = assign_statutory_data_list
        self.count = count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "csv_name", "cl_name", "le_name", "uploaded_by", "uploaded_on", "assign_statutory_data_list", "count"
        ])
        return ViewAssignStatutoryDataSuccess(
            data.get("csv_id"),
            data.get("csv_name"),
            data.get("cl_name"),
            data.get("le_name"),
            data.get("uploaded_by"),
            data.get("uploaded_on"),
            data.get("assign_statutory_data_list"),
            data.get("count")
        )

    def to_inner_structure(self):
        return {
            "csv_id" : self.csv_id,
            "csv_name" : self.csv_name,
            "cl_name" : self.cl_name,
            "le_name" : self.le_name,
            "uploaded_by" : self.uploaded_by,
            "uploaded_on" : self.uploaded_on,
            "assign_statutory_data_list" : self.assign_statutory_data_list,
            "count": self.count

        }

class AssignStatutoryApproveActionInListSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return AssignStatutoryApproveActionInListSuccess()

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

class GetRejectedASMDataSuccess(Response):
    def __init__(self, asm_rejected_data):
        self.asm_rejected_data = asm_rejected_data
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["asm_rejected_data"])
        return GetRejectedASMDataSuccess(
            data.get("asm_rejected_data")
        )

    def to_inner_structure(self):
        return {
            "asm_rejected_data": self.asm_rejected_data
        }


class RejecteASMUpdatedDownloadCountSuccess(Response):
    def __init__(self, asm_updated_count):
        self.asm_updated_count = asm_updated_count
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["asm_updated_count"])
        return RejecteASMUpdatedDownloadCountSuccess(
            data.get("asm_updated_count")
        )
    def to_inner_structure(self):
        return {
            "asm_updated_count": self.asm_updated_count
        }


class GetRejectedASMBulkUploadDataSuccess(Response):
    def __init__(self, asm_rejected_data):
        self.asm_rejected_data = asm_rejected_data
    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["asm_rejected_data"])
        return GetRejectedASMBulkUploadDataSuccess(
            data.get("asm_rejected_data")
        )

    def to_inner_structure(self):
        return {
            "asm_rejected_data": self.asm_rejected_data
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


class ASMRejectUpdateDownloadCount(object):
    def __init__(self, csv_id, download_count
        ):
        self.csv_id = csv_id
        self.download_count = download_count
    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id","download_count"
        ])
        return SMRejectUpdateDownloadCount(
            data.get("csv_id"),
            data.get("download_count")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "download_count": self.download_count
            }

def _init_Response_class_map():
    classes = [
        GetClientInfoSuccess,
        DownloadAssignStatutorySuccess,
        UploadAssignStatutoryCSVSuccess,
        UploadAssignStatutoryCSVFailed,
        GetAssignStatutoryForApproveSuccess,
        GetRejectedASMDataSuccess,
        RejecteASMUpdatedDownloadCountSuccess,
        GetRejectedASMBulkUploadDataSuccess,
        GetAssignedStatutoryReportDataSuccess,
        ViewAssignStatutoryDataSuccess,
        GetAssignStatutoryFiltersSuccess,
        AssignStatutoryApproveActionInListSuccess,
        ValidationSuccess
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

class AssignStatutoryMappingRejectData(object):
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
        return AssignStatutoryMappingRejectData(
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
        return StatutoryReportData(
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