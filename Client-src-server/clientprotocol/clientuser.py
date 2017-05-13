
from clientprotocol.jsonvalidators_client import (parse_dictionary, parse_static_list, to_structure_dictionary_values)


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
        self, legal_entity_id, unit_id, current_start_count, cal_view, cal_date
    ):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.current_start_count = current_start_count
        self.cal_view = cal_view
        self.cal_date = cal_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["le_id", "unit_id", "current_start_count", "cal_view", "cal_date"]
        )
        current_start_count = data.get("current_start_count")
        legal_entity_id = data.get("le_id")
        unit_id = data.get("unit_id")
        cal_view = data.get("cal_view")
        cal_date = data.get("cal_date")

        return GetCurrentComplianceDetail(legal_entity_id, unit_id, current_start_count, cal_view, cal_date)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "current_start_count": self.current_start_count,
            "cal_view": self.cal_view,
            "cal_date": self.cal_date
        }
#############################################################
# Get Upcoming Compliances List
#############################################################
class GetUpcomingComplianceDetail(Request):
    def __init__(
        self, legal_entity_id, unit_id, upcoming_start_count, cal_view, cal_date
    ):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.upcoming_start_count = upcoming_start_count
        self.cal_view = cal_view
        self.cal_date = cal_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "unit_id", "upcoming_start_count", "cal_view", "cal_date"])
        upcoming_start_count = data.get("upcoming_start_count")
        legal_entity_id = data.get("le_id")
        unit_id = data.get("unit_id")
        cal_view = data.get("cal_view")
        cal_date = data.get("cal_date")
        return GetUpcomingComplianceDetail(
            legal_entity_id, unit_id, upcoming_start_count, cal_view, cal_date
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "upcoming_start_count": self.upcoming_start_count,
            "cal_view": self.cal_view,
            "cal_date": self.cal_date
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
    def __init__(self, legal_entity_id, unit_id, start_count):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.start_count = start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "unit_id", "start_count"])
        legal_entity_id = data.get("le_id")
        unit_id = data.get("unit_id")
        start_count = data.get("start_count")
        return GetOnOccurrenceCompliances(legal_entity_id, unit_id, start_count)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "unit_id": self.unit_id,
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
######################################################################
# Calendar View
######################################################################
class GetCalendarView(Request):
    def __init__(self, legal_entity_id, unit_id, cal_date):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.cal_date = cal_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "unit_id", "cal_date"])
        legal_entity_id = data.get("le_id")
        unit_id = data.get("unit_id")
        cal_date = data.get("cal_date")

        return GetCalendarView(legal_entity_id, unit_id, cal_date)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "cal_date": self.cal_date
        }


class GetSettingsFormDetails(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entity_id"])
        return GetSettingsFormDetails(data.get("legal_entity_id"))

    def to_inner_structure(self):
        return {"legal_entity_id": self.legal_entity_id}

class SaveSettingsFormDetails(Request):
    def __init__(
        self, legal_entity_id, legal_entity_name, two_level_approve, assignee_reminder, advance_escalation_reminder,
        escalation_reminder, reassign_sp
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.two_level_approve = two_level_approve
        self.assignee_reminder = assignee_reminder
        self.advance_escalation_reminder = advance_escalation_reminder
        self.escalation_reminder = escalation_reminder
        self.reassign_sp = reassign_sp

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "legal_entity_name", "two_level_approve", "assignee_reminder", "advance_escalation_reminder",
            "escalation_reminder", "reassign_sp"
        ])
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        two_level_approve = data.get("two_level_approve")
        assignee_reminder = data.get("assignee_reminder")
        advance_escalation_reminder = data.get("advance_escalation_reminder")
        escalation_reminder = data.get("escalation_reminder")
        reassign_sp = data.get("reassign_sp")
        return SaveSettingsFormDetails(
            legal_entity_id, legal_entity_name, two_level_approve, assignee_reminder, advance_escalation_reminder,
            escalation_reminder, reassign_sp
        )

    def to_inner_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "two_level_approve": self.two_level_approve,
            "assignee_reminder": self.assignee_reminder,
            "advance_escalation_reminder": self.advance_escalation_reminder,
            "escalation_reminder": self.escalation_reminder,
            "reassign_sp": self.reassign_sp
        }

def _init_Request_class_map():
    classes = [
        GetCurrentComplianceDetail, GetUpcomingComplianceDetail, CheckDiskSpace,
        UpdateComplianceDetail, GetOnOccurrenceCompliances,
        StartOnOccurrenceCompliance, ComplianceFilters, OnOccurrenceLastTransaction, GetCalendarView,
        GetSettingsFormDetails, SaveSettingsFormDetails
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
        total_count = data.get("total_count")
        return GetUpcomingComplianceDetailSuccess(upcoming_compliances, total_count)

    def to_inner_structure(self):
        return {
            "upcoming_compliances": self.upcoming_compliances,
            "total_count":  self.total_count
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

class ChartSuccess(Response):
    def __init__(self, chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chart_data):
        self.chart_title = chart_title
        self.xaxis_name = xaxis_name
        self.xaxis = xaxis
        self.yaxis_name = yaxis_name
        self.yaxis = yaxis
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "chart_title", "xaxis_name", "xaxis", "yaxis_name", "yaxis",
            "widget_data"
        ])
        return ChartSuccess(
            data.get("chart_title"), data.get("xaxis_name"),
            data.get("xaxis"), data.get("yaxis_name"), data.get("yaxis"),
            data.get("widget_data")
        )

    def to_inner_structure(self):
        return {
            "chart_title": self.chart_title,
            "xaxis_name": self.xaxis_name,
            "xaxis": self.xaxis,
            "yaxis_name": self.yaxis_name,
            "yaxis": self.yaxis,
            "widget_data": self.chart_data
        }

class GetSettingsFormDetailsSuccess(Response):
    def __init__(self, settings_details, settings_domains, settings_users):
        self.settings_details = settings_details
        self.settings_domains = settings_domains
        self.settings_users = settings_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["settings_details", "settings_domains", "settings_users"])
        return GetSettingsFormDetailsSuccess(
            data.get("settings_details"), data.get("settings_domains"), data.get("settings_users")
        )

    def to_inner_structure(self):
        return {
            "settings_details": self.settings_details, "settings_domains": self.settings_domains,
            "settings_users": self.settings_users
        }

class SaveSettingsFormDetailsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveSettingsFormDetailsSuccess()

    def to_inner_structure(self):
        return {}

def _init_Response_class_map():
    classes = [
        GetCurrentComplianceDetailSuccess, GetUpcomingComplianceDetailSuccess,
        UpdateComplianceDetailSuccess,
        NotEnoughDiskSpaceAvailable, GetOnOccurrenceCompliancesSuccess,
        StartOnOccurrenceComplianceSuccess, UnSupportedFile,
        NextDueDateMustBeWithIn90DaysBeforeValidityDate, FileSizeExceedsLimit,
        ComplianceFiltersSuccess, OnOccurrenceLastTransactionSuccess, InvalidPassword, ChartSuccess,
        GetSettingsFormDetailsSuccess, SaveSettingsFormDetailsSuccess,
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
        request = data.get("request")
        request = Request.parse_structure(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": Request.to_structure(self.request),
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

#
# Settings Details
#

class SettingsInfo(object):
    def __init__(
        self, legal_entity_name, business_group_name, country_name, contract_from, contract_to,
        two_level_approve, assignee_reminder, advance_escalation_reminder, escalation_reminder,
        reassign_sp, file_space_limit, used_file_space, total_licence, used_licence
    ):
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.country_name = country_name
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.two_level_approve = two_level_approve
        self.assignee_reminder = assignee_reminder
        self.advance_escalation_reminder = advance_escalation_reminder
        self.escalation_reminder = escalation_reminder
        self.reassign_sp = reassign_sp
        self.file_space_limit = file_space_limit
        self.used_file_space = used_file_space
        self.total_licence = total_licence
        self.used_licence = used_licence

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_name", "business_group_name", "country_name", "contract_from", "contract_to",
            "two_level_approve", "assignee_reminder", "advance_escalation_reminder", "escalation_reminder",
            "reassign_sp", "file_space_limit", "used_file_space", "total_licence", "used_licence"
        ])

        return SettingsInfo(
            data.get("legal_entity_name"), data.get("business_group_name"),
            data.get("country_name"), data.get("contract_from"), data.get("contract_to"),
            data.get("two_level_approve"), data.get("assignee_reminder"), data.get("advance_escalation_reminder"),
            data.get("escalation_reminder"), data.get("reassign_sp"), data.get("file_space_limit"),
            data.get("used_file_space"), data.get("total_licence"), data.get("used_licence")
        )

    def to_structure(self):
        return {
            "legal_entity_name": self.legal_entity_name, "business_group_name": self.business_group_name,
            "country_name": self.country_name, "contract_from": self.contract_from,
            "contract_to": self.contract_to, "two_level_approve": self.two_level_approve,
            "assignee_reminder": self.assignee_reminder, "advance_escalation_reminder": self.advance_escalation_reminder,
            "escalation_reminder": self.escalation_reminder, "reassign_sp": self.reassign_sp,
            "file_space_limit": self.file_space_limit, "used_file_space": self.used_file_space,
            "total_licence": self.total_licence, "used_licence": self.used_licence
        }
