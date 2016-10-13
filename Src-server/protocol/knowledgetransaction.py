from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VariantType_knowledgetransaction_Request,
)
from protocol.to_structure import (
    to_structure_VariantType_knowledgetransaction_Request,
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

class GetStatutoryMappingsMaster(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryMappingsMaster()

    def to_inner_structure(self):
        return{}

class GetStatutoryMappings(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryMappings()

    def to_inner_structure(self):
        return {}

class CheckDuplicateStatutoryMapping(Request):
    def __init__(
        self, country_id, domain_id, industry_ids,
        statutory_nature_id, statutory_ids
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_ids = industry_ids
        self.statutory_nature_id = statutory_nature_id
        self.statutory_ids = statutory_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "d_id", "i_ids",
            "s_n_id", "s_ids",
        ])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_ids = data.get("i_ids")
        statutory_nature_id = data.get("s_n_id")
        statutory_ids = data.get("s_ids")
        return CheckDuplicateStatutoryMapping(
            country_id, domain_id, industry_ids, statutory_nature_id, statutory_ids
        )

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "i_ids": self.industry_ids,
            "s_n_id": self.statutory_nature_id,
            "s_ids": self.statutory_ids,
        }

class SaveStatutoryMapping(Request):
    def __init__(
        self, country_id, domain_id, industry_ids,
        statutory_nature_id, statutory_ids,
        compliances, geography_ids, mappings
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_ids = industry_ids
        self.statutory_nature_id = statutory_nature_id
        self.statutory_ids = statutory_ids
        self.compliances = compliances
        self.geography_ids = geography_ids
        self.mappings = mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "d_id", "i_ids",
            "s_n_id", "s_ids",
            "compliances", "g_ids", "mappings"
        ])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_ids = data.get("i_ids")
        statutory_nature_id = data.get("s_n_id")
        statutory_ids = data.get("s_ids")
        compliances = data.get("compliances")
        geography_ids = data.get("g_ids")
        mappings = data.get("mappings")
        return SaveStatutoryMapping(
            country_id, domain_id, industry_ids,
            statutory_nature_id, statutory_ids,
            compliances, geography_ids, mappings
        )

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "i_ids": self.industry_ids,
            "s_n_id": self.statutory_nature_id,
            "s_ids": self.statutory_ids,
            "compliances": self.compliances,
            "g_ids": self.geography_ids,
            "mappings": self.mappings
        }

class UpdateStatutoryMapping(Request):
    def __init__(
        self, statutory_mapping_id, country_id, domain_id,
        industry_ids, statutory_nature_id, statutory_ids,
        compliances, geography_ids, mappings
    ):
        self.statutory_mapping_id = statutory_mapping_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_ids = industry_ids
        self.statutory_nature_id = statutory_nature_id
        self.statutory_ids = statutory_ids
        self.compliances = compliances
        self.geography_ids = geography_ids
        self.mappings = mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "s_m_id", "c_id", "d_id", "i_ids",
            "s_n_id", "s_ids", "compliances",
            "g_ids", "mappings"
        ])
        statutory_mapping_id = data.get("s_m_id")
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_ids = data.get("i_ids")
        statutory_nature_id = data.get("s_n_id")
        statutory_ids = data.get("s_ids")
        compliances = data.get("compliances")
        geography_ids = data.get("g_ids")
        mappings = data.get("mappings")
        return UpdateStatutoryMapping(
            statutory_mapping_id, country_id, domain_id, industry_ids,
            statutory_nature_id, statutory_ids, compliances,
            geography_ids, mappings
        )

    def to_inner_structure(self):
        return {
            "s_m_id": self.statutory_mapping_id,
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "i_ids": self.industry_ids,
            "s_n_id": self.statutory_nature_id,
            "s_ids": self.statutory_ids,
            "compliances": self.compliances,
            "g_ids": self.geography_ids,
            "mappings": self.mappings
        }

class ChangeStatutoryMappingStatus(Request):
    def __init__(self, statutory_mapping_id, is_active):
        self.statutory_mapping_id = statutory_mapping_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["s_m_id", "is_active"])
        statutory_mapping_id = data.get("s_m_id")
        is_active = data.get("is_active")
        return ChangeStatutoryMappingStatus(statutory_mapping_id, is_active)

    def to_inner_structure(self):
        return {
            "s_m_id": self.statutory_mapping_id,
            "is_active": self.is_active
        }

class GetApproveStatutoryMappings(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetApproveStatutoryMappings()

    def to_inner_structure(self):
        return {}


class ApproveMapping(object):
    def __init__(self, statutory_mapping_id, approval_status, rejected_reason, statutory_provision, notification_text):
        self.statutory_mapping_id = statutory_mapping_id
        self.approval_status = approval_status
        self.rejected_reason = rejected_reason
        self.statutory_provision = statutory_provision
        self.notification_text = notification_text

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["s_m_id", "a_status", "r_reason", "s_provision", "n_text"])
        statutory_mapping_id = data.get("s_m_id")
        approval_status = data.get("a_status")
        rejected_reason = data.get("r_reason")
        statutory_provision = data.get("s_provision")
        notification_text = data.get("n_text")
        return ApproveMapping(statutory_mapping_id, approval_status, rejected_reason, statutory_provision, notification_text)

    def to_structure(self):
        return {
            "s_m_id": self.statutory_mapping_id,
            "a_status": self.approval_status,
            "r_reason": self.rejected_reason,
            "s_provision": self.statutory_provision,
            "n_text": self.notification_text,
        }


class ApproveStatutoryMapping(Request):
    def __init__(self, statutory_mappings):
        self.statutory_mappings = statutory_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["s_mappings"])
        statutory_mappings = data.get("s_mappings")
        return ApproveStatutoryMapping(statutory_mappings)

    def to_inner_structure(self):
        return {
            "s_mappings": self.statutory_mappings,
        }


def _init_Request_class_map():
    classes = [GetStatutoryMappingsMaster, GetStatutoryMappings, SaveStatutoryMapping, UpdateStatutoryMapping, ChangeStatutoryMappingStatus, GetApproveStatutoryMappings, ApproveStatutoryMapping, CheckDuplicateStatutoryMapping]
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

class GetStatutoryMappingsMasterSuccess(Response):
    def __init__(
        self, countries, domains, industries,
        statutory_natures, statutory_levels, statutories,
        geography_levels, geographies,
        compliance_frequency, compliance_repeat_type,
        compliance_approval_status, compliance_duration_type
    ):
        self.countries = countries
        self.domains = domains
        self.industries = industries
        self.statutory_natures = statutory_natures
        self.statutory_levels = statutory_levels
        self.statutories = statutories
        self.geography_levels = geography_levels
        self.geographies = geographies
        self.compliance_frequency = compliance_frequency
        self.compliance_repeat_type = compliance_repeat_type
        self.compliance_approval_status = compliance_approval_status
        self.compliance_duration_type = compliance_duration_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "industries", "statutory_natures", "statutory_levels", "statutories", "geography_levels", "geographies", "compliance_frequency", "compliance_repeat_type", "compliance_approval_status", "compliance_duration_type"])
        countries = data.get("countries")
        domains = data.get("domains")
        industries = data.get("industries")
        statutory_natures = data.get("statutory_natures")
        statutory_levels = data.get("statutory_levels")
        statutories = data.get("statutories")
        geography_levels = data.get("geography_levels")
        geographies = data.get("geographies")
        compliance_frequency = data.get("compliance_frequency")
        compliance_repeat_type = data.get("compliance_repeat_type")
        compliance_approval_status = data.get("compliance_approval_status")
        compliance_duration_type = data.get("compliance_duration_type")
        return GetStatutoryMappingsMasterSuccess(
            countries, domains, industries, statutory_natures,
            statutory_levels, statutories, geography_levels,
            geographies, compliance_frequency, compliance_repeat_type,
            compliance_approval_status, compliance_duration_type
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "industries": self.industries,
            "statutory_natures": self.statutory_natures,
            "statutory_levels": self.statutory_levels,
            "statutories": self.statutories,
            "geography_levels": self.geography_levels,
            "geographies": self.geographies,
            "compliance_frequency": self.compliance_frequency,
            "compliance_repeat_type": self.compliance_repeat_type,
            "compliance_approval_status": self.compliance_approval_status,
            "compliance_duration_type": self.compliance_duration_type
        }

class GetStatutoryMappingsSuccess(Response):
    def __init__(self, statutory_mappings):
        self.statutory_mappings = statutory_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statu_mappings"])
        statutory_mappings = data.get("statu_mappings")
        return GetStatutoryMappingsSuccess(statutory_mappings)

    def to_inner_structure(self):
        return {
            "statu_mappings": self.statutory_mappings
        }

class SaveStatutoryMappingSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveStatutoryMappingSuccess()

    def to_inner_structure(self):
        return {
        }

class StatutoryMappingAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return StatutoryMappingAlreadyExists()

    def to_inner_structure(self):
        return {}

class ComplianceNameAlreadyExists(Response):
    def __init__(self, compliance_name):
        self.compliance_name = compliance_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_name"])
        compliance_name = data.get("compliance_name")
        return ComplianceNameAlreadyExists(compliance_name)

    def to_inner_structure(self):
        return {
            "compliance_name": self.compliance_name
        }

class CheckDuplicateStatutoryMappingResponse(Response):
    def __init__(self, is_exists):
        self.is_exists = is_exists

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["is_exists"])
        is_exists = data.get("is_exists")
        return CheckDuplicateStatutoryMappingResponse(is_exists)

    def to_inner_structure(self):
        return {
            "is_exists": self.is_exists
        }


class CheckDuplicateStatutoryMappingSuccess(Response):
    def __init__(self, is_exists):
        self.is_exists = is_exists

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["is_exists"])
        is_exists = data.get("is_exists")
        return CheckDuplicateStatutoryMappingSuccess(is_exists)

    def to_inner_structure(self):
        return {
            "is_exists": self.is_exist
        }


class UpdateStatutoryMappingSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateStatutoryMappingSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidStatutoryMappingId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidStatutoryMappingId()

    def to_inner_structure(self):
        return {
        }

class TransactionFailed(Response):
    def __init__(self, message, extra_details):
        self.message = message
        self.extra_details = extra_details

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["message", "extra_details"])
        message = data.get("message")
        extra_details = data.get("extra_details")
        return TransactionFailed(message, extra_details)

    def to_inner_structure(self):
        return {
            "message": self.message,
            "extra_details": self.extra_details
        }

class ChangeStatutoryMappingStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeStatutoryMappingStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class ApproveStatutoryMappingSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ApproveStatutoryMappingSuccess()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [GetStatutoryMappingsMasterSuccess, GetStatutoryMappingsSuccess, SaveStatutoryMappingSuccess, CheckDuplicateStatutoryMappingResponse, CheckDuplicateStatutoryMappingSuccess, UpdateStatutoryMappingSuccess, InvalidStatutoryMappingId, ChangeStatutoryMappingStatusSuccess, ApproveStatutoryMappingSuccess]
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
        request = parse_structure_VariantType_knowledgetransaction_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_structure_VariantType_knowledgetransaction_Request(self.request),
        }
