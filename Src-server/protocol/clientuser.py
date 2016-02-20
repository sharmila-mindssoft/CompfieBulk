import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_core_UpcomingCompliance,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_RecordType_core_ActiveCompliance,
    parse_structure_CustomTextType_500,
    parse_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_CustomTextType_50,
    parse_structure_VectorType_RecordType_clientuser_ComplianceDetail,
    parse_structure_CustomTextType_20,
    parse_structure_VariantType_clientuser_Request,
    parse_structure_VectorType_CustomTextType_20,
    parse_structure_RecordType_clientuser_ComplianceDetail,
    parse_structure_OptionalType_VectorType_RecordType_core_FileList,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_OptionalType_CustomTextType_500
)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_core_UpcomingCompliance,
    to_structure_CustomTextType_100,
    to_structure_VectorType_RecordType_core_ActiveCompliance,
    to_structure_CustomTextType_500,
    to_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence,
    to_structure_SignedIntegerType_8, to_structure_CustomTextType_50,
    to_structure_VectorType_RecordType_clientuser_ComplianceDetail,
    to_structure_CustomTextType_20,
    to_structure_VariantType_clientuser_Request,
    to_structure_VectorType_CustomTextType_20,
    to_structure_RecordType_clientuser_ComplianceDetail,
    to_structure_OptionalType_VectorType_RecordType_core_FileList,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_OptionalType_CustomTextType_500
)

#
# Request
#

class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
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

class GetComplianceDetail(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetComplianceDetail()

    def to_inner_structure(self):
        return {
        }

class CheckDiskSpace(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CheckDiskSpace()

    def to_inner_structure(self):
        return {
        }

class UpdateComplianceDetail(Request):
    def __init__(self, compliance_history_id, documents, completion_date, validity_date, next_due_date, remarks):
        self.compliance_history_id = compliance_history_id
        self.documents = documents
        self.completion_date = completion_date
        self.validity_date = validity_date
        self.next_due_date = next_due_date
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_history_id", "documents", "completion_date", "validity_date", "next_due_date", "remarks"])
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        documents = data.get("documents")
        documents = parse_structure_OptionalType_VectorType_RecordType_core_FileList(documents)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_CustomTextType_20(completion_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        next_due_date = data.get("next_due_date")
        next_due_date = parse_structure_OptionalType_CustomTextType_20(next_due_date)
        remarks = data.get("remarks")
        remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        return UpdateComplianceDetail(compliance_history_id, documents, completion_date, validity_date, next_due_date, remarks)

    def to_inner_structure(self):
        return {
            "compliance_history_id": to_structure_SignedIntegerType_8(self.compliance_history_id),
            "documents": to_structure_OptionalType_VectorType_RecordType_core_FileList(self.documents),
            "completion_date": to_structure_CustomTextType_20(self.completion_date),
            "validity_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
            "next_due_date": to_structure_OptionalType_CustomTextType_20(self.next_due_date),
            "remarks": to_structure_OptionalType_CustomTextType_500(self.remarks),
        }

class GetOnOccurrenceCompliances(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetOnOccurrenceCompliances()

    def to_inner_structure(self):
        return {
        }

class StartOnOccurrenceCompliance(Request):
    def __init__(self, compliance_id, start_date):
        self.compliance_id = compliance_id
        self.start_date = start_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_id", "start_date"])
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        return StartOnOccurrenceCompliance(compliance_id, start_date)

    def to_inner_structure(self):
        return {
            "compliance_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "start_date": to_structure_CustomTextType_20(self.start_date),
        }


def _init_Request_class_map():
    classes = [GetComplianceDetail, CheckDiskSpace, UpdateComplianceDetail, GetOnOccurrenceCompliances, StartOnOccurrenceCompliance]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()

#
# Response
#

class Response(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
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

class GetComplianceDetailSuccess(Response):
    def __init__(self, compliance_detail):
        self.compliance_detail = compliance_detail

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_detail"])
        compliance_detail = data.get("compliance_detail")
        compliance_detail = parse_structure_RecordType_clientuser_ComplianceDetail(compliance_detail)
        return GetComplianceDetailSuccess(compliance_detail)

    def to_inner_structure(self):
        return {
            "compliance_detail": to_structure_RecordType_clientuser_ComplianceDetail(self.compliance_detail),
        }

class CheckDiskSpaceSuccess(Response):
    def __init__(self, total_disk_space, available_disk_space):
        self.total_disk_space = total_disk_space
        self.available_disk_space = available_disk_space

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total_disk_space", "available_disk_space"])
        total_disk_space = data.get("total_disk_space")
        total_disk_space = parse_structure_UnsignedIntegerType_32(total_disk_space)
        available_disk_space = data.get("available_disk_space")
        available_disk_space = parse_structure_UnsignedIntegerType_32(available_disk_space)
        return CheckDiskSpaceSuccess(total_disk_space, available_disk_space)

    def to_inner_structure(self):
        return {
            "total_disk_space": to_structure_SignedIntegerType_8(self.total_disk_space),
            "available_disk_space": to_structure_SignedIntegerType_8(self.available_disk_space),
        }

class UpdateComplianceDetailSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateComplianceDetailSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidUser(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUser()

    def to_inner_structure(self):
        return {
        }

class NotEnoughDiskSpaceAvailable(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return NotEnoughDiskSpaceAvailable()

    def to_inner_structure(self):
        return {
        }

class GetOnOccurrenceCompliancesSuccess(Response):
    def __init__(self, compliances):
        self.compliances = compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliances"])
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence(compliances)
        return GetOnOccurrenceCompliancesSuccess(compliances)

    def to_inner_structure(self):
        return {
            "compliances": to_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence(self.compliances),
        }

class StartOnOccurrenceComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return StartOnOccurrenceComplianceSuccess()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [GetComplianceDetailSuccess, CheckDiskSpaceSuccess, UpdateComplianceDetailSuccess, NotEnoughDiskSpaceAvailable, GetOnOccurrenceCompliancesSuccess, StartOnOccurrenceComplianceSuccess]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

#
# RequestFormat
#

class RequestFormat(object):
    def __init__(self, session_token, request):
        self.session_token = session_token
        self.request = request

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["session_token", "request"])
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        request = data.get("request")
        request = parse_structure_VariantType_clientuser_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_clientuser_Request(self.request),
        }

#
# ComplianceDetail
#

class ComplianceDetail(object):
    def __init__(self, current_compliances, upcoming_compliances):
        self.current_compliances = current_compliances
        self.upcoming_compliances = upcoming_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["current_compliances", "upcoming_compliances"])
        current_compliances = data.get("current_compliances")
        current_compliances = parse_structure_VectorType_RecordType_core_ActiveCompliance(current_compliances)
        upcoming_compliances = data.get("upcoming_compliances")
        upcoming_compliances = parse_structure_VectorType_RecordType_core_UpcomingCompliance(upcoming_compliances)
        return ComplianceDetail(current_compliances, upcoming_compliances)

    def to_structure(self):
        return {
            "current_compliances": to_structure_VectorType_RecordType_core_ActiveCompliance(self.current_compliances),
            "upcoming_compliances": to_structure_VectorType_RecordType_core_UpcomingCompliance(self.upcoming_compliances)
        }

#
# ComplianceOnOccurrence
#

class ComplianceOnOccurrence(object):
    def __init__(self, compliance_id, statutory_provision, compliance_name, description, complete_within_days):
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_name = compliance_name
        self.description = description
        self.complete_within_days = complete_within_days

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_id", "statutory_provision", "compliance_name", "description", "complete_within_days"])
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_CustomTextType_500(statutory_provision)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_100(compliance_name)
        description = data.get("description")
        description = parse_structure_CustomTextType_500(description)
        complete_within_days = data.get("complete_within_days")
        complete_within_days = parse_structure_UnsignedIntegerType_32(complete_within_days)
        return ComplianceOnOccurrence(compliance_id, statutory_provision, compliance_name, description, complete_within_days)

    def to_structure(self):
        return {
            "compliance_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "statutory_provision": to_structure_CustomTextType_500(self.statutory_provision),
            "compliance_name": to_structure_CustomTextType_100(self.compliance_name),
            "description": to_structure_CustomTextType_500(self.description),
            "complete_within_days": to_structure_SignedIntegerType_8(self.complete_within_days),
        }

