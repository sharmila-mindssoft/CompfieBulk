
from clientprotocol.jsonvalidators_client import (parse_dictionary, parse_static_list, to_structure_dictionary_values)
from clientprotocol.parse_structure import (
    parse_structure_VectorType_RecordType_core_UpcomingCompliance,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_RecordType_core_ActiveCompliance,
    parse_structure_CustomTextType_500,
    parse_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_CustomTextType_50,
    parse_structure_CustomTextType_20,
    parse_structure_VariantType_clientuser_Request,
    parse_structure_VectorType_CustomTextType_20,
    parse_structure_OptionalType_VectorType_RecordType_core_FileList,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_OptionalType_CustomTextType_500,
    parse_structure_OptionalType_VectorType_CustomTextType_500,
    parse_structure_MapType_CustomTextType_250_VectorType_RecordType_clientuser_ComplianceOnOccurrence,
    parse_structure_CustomTextType_250,
    parse_structure_Text
)
from clientprotocol.to_structure import (
    to_structure_VectorType_RecordType_core_UpcomingCompliance,
    to_structure_CustomTextType_100,
    to_structure_VectorType_RecordType_core_ActiveCompliance,
    to_structure_CustomTextType_500,
    to_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence,
    to_structure_SignedIntegerType_8, to_structure_CustomTextType_50,
    to_structure_CustomTextType_20,
    to_structure_VariantType_clientuser_Request,
    to_structure_VectorType_CustomTextType_20,
    to_structure_OptionalType_VectorType_RecordType_core_FileList,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_OptionalType_VectorType_CustomTextType_500,
    to_structure_MapType_CustomTextType_250_VectorType_RecordType_clientuser_ComplianceOnOccurrence,
    to_structure_UnsignedIntegerType_32,
    to_structure_CustomTextType_250,
    to_structure_Text
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
#######################################################
# Get Current Compliances
#######################################################
class GetCurrentComplianceDetail(Request):
    def __init__(
        self, legal_entity_id, unit_id, current_start_count
    ):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.current_start_count = current_start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["le_id", "unit_id", "current_start_count"]
        )
        current_start_count = data.get("current_start_count")
        legal_entity_id = data.get("le_id")
        unit_id = data.get("unit_id")
        return GetCurrentComplianceDetail(legal_entity_id, unit_id, current_start_count)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "current_start_count": self.current_start_count
        }
#############################################################
# Get Upcoming Compliances List
#############################################################
class GetUpcomingComplianceDetail(Request):
    def __init__(
        self, legal_entity_id, unit_id, upcoming_start_count
    ):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.upcoming_start_count = upcoming_start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "unit_id", "upcoming_start_count"])
        upcoming_start_count = data.get("upcoming_start_count")
        legal_entity_id = data.get("le_id")
        unit_id = data.get("unit_id")
        return GetUpcomingComplianceDetail(
            legal_entity_id, unit_id, upcoming_start_count
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "upcoming_start_count": self.upcoming_start_count,
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
#########################################################
# Save / Update Current Compliances
#########################################################
class UpdateComplianceDetail(Request):
    def __init__(
        self, legal_entity_id, compliance_history_id, documents, uploaded_documents,
        completion_date, validity_date, next_due_date, remarks
    ):
        self.legal_entity_id = legal_entity_id
        self.compliance_history_id = compliance_history_id
        self.documents = documents
        self.uploaded_documents = uploaded_documents
        self.completion_date = completion_date
        self.validity_date = validity_date
        self.next_due_date = next_due_date
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "le_id", "compliance_history_id", "documents", "uploaded_documents",
                "completion_date", "validity_date", "next_due_date", "remarks"
            ]
        )
        legal_entity_id = data.get("le_id")
        compliance_history_id = data.get("compliance_history_id")
        # compliance_history_id = parse_structure_UnsignedIntegerType_32(
        #     compliance_history_id)
        documents = data.get("documents")
        # documents = parse_structure_OptionalType_VectorType_RecordType_core_FileList(
        #     documents)
        uploaded_documents = data.get("uploaded_documents")
        # uploaded_documents = parse_structure_OptionalType_VectorType_CustomTextType_500(
        #     uploaded_documents)
        completion_date = data.get("completion_date")
        # completion_date = parse_structure_CustomTextType_20(completion_date)
        validity_date = data.get("validity_date")
        # validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        next_due_date = data.get("next_due_date")
        # next_due_date = parse_structure_OptionalType_CustomTextType_20(next_due_date)
        remarks = data.get("remarks")
        # remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        return UpdateComplianceDetail(
            legal_entity_id, compliance_history_id, documents, uploaded_documents,
            completion_date, validity_date, next_due_date, remarks
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "compliance_history_id": self.compliance_history_id,
            "documents": self.documents,
            "uploaded_documents": self.uploaded_documents,
            "completion_date": self.completion_date,
            "validity_date": self.validity_date,
            "next_due_date": self.next_due_date,
            "remarks": self.remarks,
        }
######################################################################
# Get Onoccurrence Compliances
######################################################################
class GetOnOccurrenceCompliances(Request):
    def __init__(self, legal_entity_id, start_count):
        self.legal_entity_id = legal_entity_id
        self.start_count = start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "start_count"])
        legal_entity_id = data.get("le_id")
        start_count = data.get("start_count")
        # start_count = parse_structure_UnsignedIntegerType_32(start_count)
        return GetOnOccurrenceCompliances(legal_entity_id, start_count)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "start_count": self.start_count
        }

######################################################################
# Start Onoccurrence Compliances
######################################################################
class StartOnOccurrenceCompliance(Request):
    def __init__(self, legal_entity_id, compliance_id, start_date, unit_id, duration, remarks, password):
        self.legal_entity_id = legal_entity_id
        self.compliance_id = compliance_id
        self.start_date = start_date
        self.unit_id = unit_id
        self.duration = duration
        self.remarks = remarks
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "compliance_id", "start_date", "unit_id", "duration", "remarks", "password"])
        legal_entity_id = data.get("le_id")
        compliance_id = data.get("compliance_id")
        # compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        start_date = data.get("start_date")
        # start_date = parse_structure_CustomTextType_20(start_date)
        unit_id = data.get("unit_id")
        # unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        duration = data.get("duration")
        remarks = data.get("remarks")
        password = data.get("password")
        # duration = parse_structure_CustomTextType_20(duration)
        return StartOnOccurrenceCompliance(
            legal_entity_id, compliance_id, start_date, unit_id, duration, remarks, password
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "compliance_id": self.compliance_id,
            "start_date": self.start_date,
            "unit_id": self.unit_id,
            "duration": self.duration,
            "remarks": self.remarks,
            "password": self.password
        }
######################################################################
# Compliance Filters
######################################################################
class ComplianceFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")

        return ComplianceFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

######################################################################
# OnOccurrence Last Transactions
######################################################################
class OnOccurrenceLastTransaction(Request):
    def __init__(self, legal_entity_id, compliance_id, unit_id):
        self.legal_entity_id = legal_entity_id
        self.compliance_id = compliance_id
        self.unit_id = unit_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "compliance_id", "unit_id"])
        legal_entity_id = data.get("le_id")
        compliance_id = data.get("compliance_id")
        unit_id = data.get("unit_id")

        return OnOccurrenceLastTransaction(legal_entity_id, compliance_id, unit_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "compliance_id": self.compliance_id,
            "unit_id": self.unit_id
        }


def _init_Request_class_map():
    classes = [
        GetCurrentComplianceDetail, GetUpcomingComplianceDetail, CheckDiskSpace,
        UpdateComplianceDetail, GetOnOccurrenceCompliances,
        StartOnOccurrenceCompliance, ComplianceFilters, OnOccurrenceLastTransaction
    ]
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

####################################################################
# Get Compliance Task Details
####################################################################
class GetCurrentComplianceDetailSuccess(Response):
    def __init__(self, current_compliances, current_date, overdue_count, inprogress_count):
        self.current_compliances = current_compliances
        self.current_date = current_date
        self.overdue_count = overdue_count
        self.inprogress_count = inprogress_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["current_compliances", "current_date",
                                       "overdue_count", "inprogress_count"])
        current_compliances = data.get("current_compliances")
        current_date = data.get("current_date")
        overdue_count = data.get("overdue_count")
        inprogress_count = data.get("inprogress_count")
        return GetCurrentComplianceDetailSuccess(
            current_compliances, current_date, overdue_count, inprogress_count
        )

    def to_inner_structure(self):
        return {
            "current_compliances": self.current_compliances,
            "current_date" : self.current_date,
            "overdue_count" : self.overdue_count,
            "inprogress_count": self.inprogress_count
        }
#############################################################
# Get Upcoming Compliances List - Success
#############################################################
class GetUpcomingComplianceDetailSuccess(Response):
    def __init__(self, upcoming_compliances, total_count):
        self.upcoming_compliances = upcoming_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["upcoming_compliances", "total_count"])
        upcoming_compliances = data.get("upcoming_compliances")
        # upcoming_compliances = parse_structure_VectorType_RecordType_core_UpcomingCompliance(upcoming_compliances)
        total_count = data.get("total_count")
        # total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetUpcomingComplianceDetailSuccess(upcoming_compliances, total_count)

    def to_inner_structure(self):
        return {
            "upcoming_compliances": self.upcoming_compliances,
            "total_count":  self.total_count
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

class NextDueDateMustBeWithIn90DaysBeforeValidityDate(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return NextDueDateMustBeWithIn90DaysBeforeValidityDate()

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


class UnSupportedFile(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UnSupportedFile()

    def to_inner_structure(self):
        return {
        }


class FileSizeExceedsLimit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return FileSizeExceedsLimit()

    def to_inner_structure(self):
        return {
        }

class InvalidPassword(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidPassword()

    def to_inner_structure(self):
        return {
        }

class GetOnOccurrenceCompliancesSuccess(Response):
    def __init__(self, compliances, total_count):
        self.compliances = compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["onoccur_compliances", "total_count"])
        compliances = data.get("onoccur_compliances")
        # compliances = parse_structure_MapType_CustomTextType_250_VectorType_RecordType_clientuser_ComplianceOnOccurrence(compliances) #parse_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence(compliances)
        total_count = data.get("total_count")
        # total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetOnOccurrenceCompliancesSuccess(compliances, total_count)

    def to_inner_structure(self):
        return {
            "onoccur_compliances": self.compliances,
            "total_count": self.total_count
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

class ComplianceFiltersSuccess(Response):
    def __init__(self, user_units):
        self.user_units = user_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_units"])
        user_units = data.get("user_units")
        return ComplianceFiltersSuccess(user_units)

    def to_inner_structure(self):
        return {
            "user_units": self.user_units
        }

class OnOccurrenceLastTransactionSuccess(Response):
    def __init__(self, onoccurrence_transactions):
        self.onoccurrence_transactions = onoccurrence_transactions

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["onoccurrence_transactions"])
        onoccurrence_transactions = data.get("onoccurrence_transactions")

        return OnOccurrenceLastTransactionSuccess(onoccurrence_transactions)

    def to_inner_structure(self):
        return {
            "onoccurrence_transactions": self.onoccurrence_transactions
        }

def _init_Response_class_map():
    classes = [
        GetCurrentComplianceDetailSuccess, GetUpcomingComplianceDetailSuccess,
        CheckDiskSpaceSuccess, UpdateComplianceDetailSuccess,
        NotEnoughDiskSpaceAvailable, GetOnOccurrenceCompliancesSuccess,
        StartOnOccurrenceComplianceSuccess, UnSupportedFile,
        NextDueDateMustBeWithIn90DaysBeforeValidityDate, FileSizeExceedsLimit,
        ComplianceFiltersSuccess, OnOccurrenceLastTransactionSuccess, InvalidPassword
    ]
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
    def __init__(self, current_compliances, upcoming_compliances, current_date):
        self.current_compliances = current_compliances
        self.upcoming_compliances = upcoming_compliances
        self.current_date = current_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["current_compliances", "upcoming_compliances", "current_date"])
        current_compliances = data.get("current_compliances")
        current_compliances = parse_structure_VectorType_RecordType_core_ActiveCompliance(current_compliances)
        upcoming_compliances = data.get("upcoming_compliances")
        upcoming_compliances = parse_structure_VectorType_RecordType_core_UpcomingCompliance(upcoming_compliances)
        current_date = data.get("current_date")
        current_date = parse_structure_CustomTextType_20(current_date)
        return ComplianceDetail(current_compliances, upcoming_compliances, current_date)

    def to_structure(self):
        return {
            "current_compliances": to_structure_VectorType_RecordType_core_ActiveCompliance(self.current_compliances),
            "upcoming_compliances": to_structure_VectorType_RecordType_core_UpcomingCompliance(self.upcoming_compliances),
            "current_date" : to_structure_CustomTextType_20(self.current_date)
        }

#
# ComplianceOnOccurrence
#

class ComplianceOnOccurrence(object):
    def __init__(
        self, compliance_id, statutory_provision, compliance_name,
        description, complete_within_days, unit_id
    ):
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_name = compliance_name
        self.description = description
        self.complete_within_days = complete_within_days
        self.unit_id = unit_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_id", "statutory_provision", "compliance_name",
                "description", "complete_within_days", "unit_id"
            ]
        )
        compliance_id = data.get("compliance_id")
        # compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        statutory_provision = data.get("statutory_provision")
        # statutory_provision = parse_structure_Text(statutory_provision)
        compliance_name = data.get("compliance_name")
        # compliance_name = parse_structure_CustomTextType_250(compliance_name)
        description = data.get("description")
        # description = parse_structure_Text(description)
        complete_within_days = data.get("complete_within_days")
        # complete_within_days = parse_structure_CustomTextType_50(complete_within_days)
        unit_id = data.get("unit_id")
        # unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        return ComplianceOnOccurrence(
            compliance_id, statutory_provision, compliance_name, description,
            complete_within_days, unit_id
        )

    def to_structure(self):
        return {
            "compliance_id": self.compliance_id,
            "statutory_provision": self.statutory_provision,
            "compliance_name": self.compliance_name,
            "description": self.description,
            "complete_within_days": self.complete_within_days,
            "unit_id": self.unit_id,
        }
