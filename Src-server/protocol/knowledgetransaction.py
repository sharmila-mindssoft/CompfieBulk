from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    to_structure_dictionary_values
)
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

class GetStatutoryMappingsMaster(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryMappingsMaster()

    def to_inner_structure(self):
        return {}

class GetStatutoryMappings(Request):
    def __init__(self, approval_status_id, rcount):
        self.approval_status_id = approval_status_id
        self.rcount = rcount

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["approval_status_id", "rcount"])
        approval_status = data.get("approval_status_id")
        rcount = data.get("rcount")
        return GetStatutoryMappings(approval_status, rcount)

    def to_inner_structure(self):
        return {
            "approval_status": self.approval_status,
            "rcount": self.rcount
        }

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

class GetStatutoryMaster(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryMaster()

    def to_inner_structure(self):
        return {}


def _init_Request_class_map():
    classes = [
        GetStatutoryMappingsMaster, GetStatutoryMappings,
        SaveStatutoryMapping, UpdateStatutoryMapping,
        ChangeStatutoryMappingStatus, GetApproveStatutoryMappings,
        ApproveStatutoryMapping, CheckDuplicateStatutoryMapping,
        GetStatutoryMaster
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

class GetStatutoryMasterSuccess(Response):
    def __init__(self, statutories):
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutories_info"])
        statutories = data.get("statutory_info")
        return GetStatutoryMasterSuccess(statutories)

    def to_inner_structure(self):
        return {
            "statutory_info": self.statutories,
        }

class GetStatutoryMappingsMasterSuccess(Response):
    def __init__(
        self, countries, domains, industries,
        statutory_natures, statutory_levels,
        geography_levels, geographies,
        compliance_frequency, compliance_repeat_type,
        compliance_approval_status, compliance_duration_type
    ):
        self.countries = countries
        self.domains = domains
        self.industries = industries
        self.statutory_natures = statutory_natures
        self.statutory_levels = statutory_levels
        self.geography_levels = geography_levels
        self.geographies = geographies
        self.compliance_frequency = compliance_frequency
        self.compliance_repeat_type = compliance_repeat_type
        self.compliance_approval_status = compliance_approval_status
        self.compliance_duration_type = compliance_duration_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "domains", "industries", "statutory_natures",
            "statutory_levels", "geography_levels", "geographies",
            "compliance_frequency", "compliance_repeat_type",
            "compliance_approval_status", "compliance_duration_type"
        ])
        countries = data.get("country_info")
        domains = data.get("domain_info")
        industries = data.get("organisation_info")
        statutory_natures = data.get("nature_info")
        statutory_levels = data.get("statutory_levels")
        geography_levels = data.get("geography_level_info")
        geographies = data.get("geography_info")
        compliance_frequency = data.get("compliance_frequency")
        compliance_repeat_type = data.get("compliance_repeat_type")
        compliance_approval_status = data.get("compliance_approval_status")
        compliance_duration_type = data.get("compliance_duration_type")
        return GetStatutoryMappingsMasterSuccess(
            countries, domains, industries, statutory_natures,
            statutory_levels, geography_levels,
            geographies, compliance_frequency, compliance_repeat_type,
            compliance_approval_status, compliance_duration_type
        )

    def to_inner_structure(self):
        return {
            "country_info": self.countries,
            "domain_info": self.domains,
            "organisation_info": self.industries,
            "nature_info": self.statutory_natures,
            "statutory_levels": self.statutory_levels,
            "geography_level_info": self.geography_levels,
            "geography_info": self.geographies,
            "compliance_frequency": self.compliance_frequency,
            "compliance_repeat_type": self.compliance_repeat_type,
            "compliance_approval_status": self.compliance_approval_status,
            "compliance_duration_type": self.compliance_duration_type
        }

class GetStatutoryMappingsSuccess(Response):
    def __init__(self, statutory_mappings, total_records):
        self.statutory_mappings = statutory_mappings
        self.total_records = total_records

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statu_mappings"])
        statutory_mappings = data.get("statu_mappings")
        total_records = data.get("total_records")
        return GetStatutoryMappingsSuccess(statutory_mappings, total_records)

    def to_inner_structure(self):
        return {
            "statu_mappings": self.statutory_mappings,
            "total_records": self.total_records
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
    classes = [
        GetStatutoryMappingsMasterSuccess,
        GetStatutoryMappingsSuccess, SaveStatutoryMappingSuccess,
        CheckDuplicateStatutoryMappingResponse,
        CheckDuplicateStatutoryMappingSuccess,
        UpdateStatutoryMappingSuccess, InvalidStatutoryMappingId,
        ChangeStatutoryMappingStatusSuccess,
        ApproveStatutoryMappingSuccess,
        GetStatutoryMasterSuccess
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
        request = parse_structure_VariantType_knowledgetransaction_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_structure_VariantType_knowledgetransaction_Request(self.request),
        }

class DomainInfo(object):
    def __init__(self, domain_id, country_id, domain_name, is_active):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.country_id = country_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "d_id", "c_id", "d_name", "is_active"
        ])
        domain_id = data.get("d_id")
        domain_name = data.get("d_name")
        country_id = data.get("c_id")
        is_active = data.get("is_active")
        return DomainInfo(domain_id, country_id, domain_name, is_active)

    def to_structure(self):
        return {
            "d_id": self.domain_id,
            "c_id": self.country_id,
            "d_name": self.domain_name,
            "is_active": self.is_active
        }

class CountryInfo(object):
    def __init__(self, country_id, country_name, is_active):
        self.country_id = country_id
        self.country_name = country_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_id", "c_name", "is_active"
        ])
        country_id = data.get("c_id")
        country_name = data.get("c_name")
        is_active = data.get("is_active")
        return CountryInfo(country_id, country_name, is_active)

    def to_structure(self):
        return {
            "c_id": self.country_id,
            "c_name": self.country_name,
            "is_active": self.is_active
        }

class OrganisationInfo(object):
    def __init__(
        self, organisation_id, country_id, domain_id,
        organisation_name, is_active
    ):
        self.organisation_id = organisation_id
        self.organisation_name = organisation_name
        self.country_id = country_id
        self.domain_id = domain_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "org_id", "org_name", "c_id", "d_id", "is_active"
        ])
        organisation_id = data.get("org_id")
        organisation_name = data.get("org_name")
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        is_active = data.get("is_active")
        return OrganisationInfo(
            organisation_id, country_id,
            domain_id, organisation_name, is_active
        )

    def to_structure(self):
        return {
            "org_id": self.organisation_id,
            "org_name": self.organisation_name,
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "is_active": self.is_active
        }

class StatutoryNatureInfo(object):
    def __init__(self, nature_id, nature_name, country_id, is_active):
        self.nature_id = nature_id
        self.nature_name = nature_name
        self.country_id = country_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data[
            "s_n_id", "s_n_name", "c_id", "is_active"
        ])
        nature_id = data.get("s_n_id")
        nature_name = data.get("s_n_name")
        country_id = data.et("c_id")
        is_active = data.get("is_active")
        return StatutoryNatureInfo(
            nature_id, nature_name, country_id, is_active
        )

    def to_structure(self):
        return {
            "s_n_id": self.nature_id,
            "s_n_name": self.nature_name,
            "c_id": self.country_id,
            "is_active": self.is_active
        }

class StatutoryInfo(object):
    def __init__(
        self, statutory_id, statutory_name, level_id, parent_ids,
        parent_id, parent_mappings, country_id, domain_id,
        level_position
    ):
        self.statutory_id = statutory_id
        self.statutory_name = statutory_name
        self.level_id = level_id
        self.parent_ids = parent_ids
        self.parent_id = parent_id
        self.parent_mappings = parent_mappings
        self.country_id = country_id
        self.domain_id = domain_id
        self.level_position = level_position

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "s_id", "s_name", "l_id", "p_ids",
            "p_id", "p_maps", "c_id", "d_id",
            "l_position"
        ])
        statutory_id = data.get("s_id")
        statutory_name = data.get("s_name")
        level_id = data.get("l_id")
        parent_ids = data.get("p_ids")
        parent_id = data.get("p_id")
        parent_mappings = data.get("p_maps")
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        level_position = data.get("l_position")
        return StatutoryInfo(
            statutory_id, statutory_name, level_id, parent_ids,
            parent_id, parent_mappings,
            country_id, domain_id,
            level_position
        )

    def to_structure(self):
        return {
            "s_id": self.statutory_id,
            "s_name": self.statutory_name,
            "l_id": self.level_id,
            "p_ids": self.parent_ids,
            "p_id": self.parent_id,
            "p_maps": self.parent_mappings,
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "l_position": self.level_position
        }

class GeographyInfo(object):
    def __init__(
        self, geography_id, geography_name, level_id,
        parent_ids, parent_id, parent_names, is_active, country_id,
        level_position
    ):
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.level_id = level_id
        self.parent_ids = parent_ids
        self.parent_id = parent_id
        self.parent_names = parent_names
        self.is_active = is_active
        self.country_id = country_id
        self.level_position = level_position

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "g_id", "g_name", "l_id", "p_ids",
            "p_id", "p_maps", "is_active", "c_id",
            "l_position"
        ])
        geography_id = data.get("g_id")
        geography_name = data.get("g_name")
        level_id = data.get("l_id")
        parent_ids = data.get("p_ids")
        parent_id = data.get("p_id")
        parent_mappings = data.get("p_maps")
        is_active = data.get("is_active")
        country_id = data.get("c_id")
        level_position = data.get('l_position')
        return GeographyInfo(
            geography_id, geography_name, level_id, parent_ids, parent_id,
            parent_mappings, is_active, country_id,
            level_position
        )

    def to_structure(self):
        data = {
            "g_id": self.geography_id,
            "g_name": self.geography_name,
            "l_id": self.level_id,
            "p_ids": self.parent_ids,
            "p_id": self.parent_id,
            "p_maps": self.parent_names,
            "is_active": self.is_active,
            "c_id": self.country_id,
            "l_position": self.level_position
        }
        return data
