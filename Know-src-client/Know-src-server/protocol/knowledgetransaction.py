from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    to_structure_dictionary_values,
    parse_VariantType,
    to_VariantType
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
    def __init__(self, approval_status_id, active_status_id, rcount, page_limit):
        self.approval_status_id = approval_status_id
        self.rcount = rcount
        self.page_limit = page_limit
        self.active_status_id = active_status_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["approval_status_id", "active_status_id", "rcount", "page_limit"])
        approval_status = data.get("approval_status_id")
        active_status_id = data.get("active_status_id")
        rcount = data.get("rcount")
        page_limit = data.get("page_limit")
        return GetStatutoryMappings(approval_status, active_status_id, rcount, page_limit)

    def to_inner_structure(self):
        return {
            "approval_status": self.approval_status,
            "rcount": self.rcount,
            "page_limit": self.page_limit,
            "active_status_id": self.active_status_id
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
        compliances, geography_ids, mappings,
        tr_type
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_ids = industry_ids
        self.statutory_nature_id = statutory_nature_id
        self.statutory_ids = statutory_ids
        self.compliances = compliances
        self.geography_ids = geography_ids
        self.mappings = mappings
        self.tr_type = tr_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "d_id", "i_ids",
            "s_n_id", "s_ids",
            "compliances", "g_ids", "mappings", "tr_type"
        ])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_ids = data.get("i_ids")
        statutory_nature_id = data.get("s_n_id")
        statutory_ids = data.get("s_ids")
        compliances = data.get("compliances")
        geography_ids = data.get("g_ids")
        mappings = data.get("mappings")
        tr_type = data.get("tr_type")
        return SaveStatutoryMapping(
            country_id, domain_id, industry_ids,
            statutory_nature_id, statutory_ids,
            compliances, geography_ids, mappings, tr_type
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
            "mappings": self.mappings,
            "tr_type": self.tr_type
        }

class UpdateStatutoryMapping(Request):
    def __init__(
        self, mapping_id, country_id, domain_id, industry_ids,
        statutory_nature_id, statutory_ids,
        compliances, geography_ids, mappings,
        tr_type
    ):
        self.mapping_id = mapping_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_ids = industry_ids
        self.statutory_nature_id = statutory_nature_id
        self.statutory_ids = statutory_ids
        self.compliances = compliances
        self.geography_ids = geography_ids
        self.mappings = mappings
        self.tr_type = tr_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "m_id", "c_id", "d_id", "i_ids",
            "s_n_id", "s_ids",
            "compliances", "g_ids", "mappings", "tr_type"
        ])
        mapping_id = data.get("m_id")
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_ids = data.get("i_ids")
        statutory_nature_id = data.get("s_n_id")
        statutory_ids = data.get("s_ids")
        compliances = data.get("compliances")
        geography_ids = data.get("g_ids")
        mappings = data.get("mappings")
        tr_type = data.get("tr_type")
        return UpdateStatutoryMapping(
            mapping_id, country_id, domain_id, industry_ids,
            statutory_nature_id, statutory_ids,
            compliances, geography_ids, mappings, tr_type
        )

    def to_inner_structure(self):
        return {
            "m_id": self.mapping_id,
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "i_ids": self.industry_ids,
            "s_n_id": self.statutory_nature_id,
            "s_ids": self.statutory_ids,
            "compliances": self.compliances,
            "g_ids": self.geography_ids,
            "mappings": self.mappings,
            "tr_type": self.tr_type
        }

class UpdateCompliance(Request):
    def __init__(
        self, mapping_id, country_id, domain_id, industry_ids,
        statutory_nature_id, statutory_ids,
        compliances, geography_ids, mappings,
        tr_type
    ):
        self.mapping_id = mapping_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_ids = industry_ids
        self.statutory_nature_id = statutory_nature_id
        self.statutory_ids = statutory_ids
        self.compliances = compliances
        self.geography_ids = geography_ids
        self.mappings = mappings
        self.tr_type = tr_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "m_id", "c_id", "d_id", "i_ids",
            "s_n_id", "s_ids",
            "compliances", "g_ids", "mappings", "tr_type"
        ])
        mapping_id = data.get("m_id")
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_ids = data.get("i_ids")
        statutory_nature_id = data.get("s_n_id")
        statutory_ids = data.get("s_ids")
        compliances = data.get("compliances")
        geography_ids = data.get("g_ids")
        mappings = data.get("mappings")
        tr_type = data.get("tr_type")
        return UpdateCompliance(
            mapping_id, country_id, domain_id, industry_ids,
            statutory_nature_id, statutory_ids,
            compliances, geography_ids, mappings, tr_type
        )

    def to_inner_structure(self):
        return {
            "m_id": self.mapping_id,
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "i_ids": self.industry_ids,
            "s_n_id": self.statutory_nature_id,
            "s_ids": self.statutory_ids,
            "compliances": self.compliances,
            "g_ids": self.geography_ids,
            "mappings": self.mappings,
            "tr_type": self.tr_type
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

class GetApproveStatutoryMappingsFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetApproveStatutoryMappingsFilters()

    def to_inner_structure(self):
        return {}


class GetApproveStatutoryMappings(Request):
    def __init__(self, i_id, s_n_id, c_id, d_id, u_id, r_count):
        self.industry_id = i_id
        self.nature_id = s_n_id
        self.country_id = c_id
        self.domain_id = d_id
        self.user_id = u_id
        self.r_count = r_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["a_i_id", "a_s_n_id", "a_c_id", "a_d_id", "a_u_id", "r_count"])
        industry_id = data.get("a_i_id")
        nature_id = data.get("a_s_n_id")
        country_id = data.get("a_c_id")
        domain_id = data.get("a_d_id")
        user_id = data.get("a_u_id")
        r_count = data.get("r_count")
        return GetApproveStatutoryMappings(industry_id, nature_id, country_id, domain_id, user_id, r_count)

    def to_inner_structure(self):
        return {
            "a_i_id": self.industry_id,
            "a_s_n_id": self.nature_id,
            "a_c_id": self.country_id,
            "a_d_id": self.domain_id,
            "a_u_id": self.user_id,
            "r_count": self.r_count
        }


class GetComplianceInfo(Request):
    def __init__(self, compliance_id):
        self.compliance_id = compliance_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["comp_id"])
        comp_id = data.get("comp_id")
        return GetComplianceInfo(comp_id)

    def to_inner_structure(self):
        return {
            "comp_id": self.compliance_id
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

class GetComplianceEdit(Request):
    def __init__(self, compliance_id, mapping_id):
        self.compliance_id = compliance_id
        self.mapping_id = mapping_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["comp_id", "m_id"])
        comp_id = data.get("comp_id")
        mapping_id = data.get("m_id")
        return GetComplianceEdit(comp_id, mapping_id)

    def to_inner_structure(self):
        return {
            "comp_id": self.compliance_id,
            "m_id": self.mapping_id
        }


def _init_Request_class_map():
    classes = [
        GetStatutoryMappingsMaster, GetStatutoryMappings,
        SaveStatutoryMapping, UpdateStatutoryMapping,
        ChangeStatutoryMappingStatus, GetApproveStatutoryMappings,
        ApproveStatutoryMapping, CheckDuplicateStatutoryMapping,
        GetStatutoryMaster, GetApproveStatutoryMappingsFilters,
        GetComplianceEdit, GetComplianceInfo, UpdateCompliance
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

class UpdateComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateComplianceSuccess()

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

class GetApproveStatutoryMappingFilterSuccess(Response):
    def __init__(self, countries, domains, statutory_natures, industries, knowledgeusers):
        self.countries = countries
        self.domains = domains
        self.statutory_natures = statutory_natures
        self.industries = industries
        self.knowledgeusers = knowledgeusers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "domains", "statutory_natures", "industries",
            "knowledgeusers"
        ])
        countries = data.get("countries")
        domains = data.get("domains")
        statutory_natures = data.get("statutory_natures")
        industries = data.get("industries")
        knowledgeusers = data.get("knowledgeusers")
        return GetApproveStatutoryMappingFilterSuccess(
            countries, domains, statutory_natures, industries,
            knowledgeusers
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "statutory_natures": self.statutory_natures,
            "industries": self.industries,
            "knowledgeusers": self.knowledgeusers
        }


class GetApproveStatutoryMappingSuccess(Response):
    def __init__(self, approve_mappings, total_count):
        self.approve_mappings = approve_mappings
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["approv_mappings", "total_count"])
        approve_mappings = data.get("approv_mappings")
        total_count = data.get("total_count")
        return GetApproveStatutoryMappingSuccess(approve_mappings, total_count)

    def to_inner_structure(self):
        return {
            "approv_mappings": self.approve_mappings,
            "total_count": self.total_count
        }

class GetComplianceInfoSuccess(Response):
    def __init__(
        self, compliance_id, statutory_provision,
        compliance_task, description,
        penal_consequences, is_active,
        frequency, summary, reference, locations, url
    ):
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_task = compliance_task
        self.description = description
        self.penal_consequences = penal_consequences
        self.is_active = is_active
        self.frequency = frequency
        self.summary = summary
        self.reference = reference
        self.locations = locations
        self.url = url

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "s_pro",
            "c_task", "descrip",
            "p_cons", "is_active",
            "freq", "summary",
            "refer", "locat", "url"
        ])
        compliance_id = data.get("comp_id")
        statutory_provision = data.get("s_pro")
        compliance_task = data.get("c_task")
        description = data.get("descrip")
        penal_consequences = data.get("p_cons")
        is_active = data.get("is_active")
        frequency = data.get("freq")
        summary = data.get("summary")
        reference = data.get("refer")
        locations = data.get("locat")
        url = data.get("url")

        return GetComplianceInfoSuccess(
            compliance_id, statutory_provision,
            compliance_task, description,
            penal_consequences,
            is_active,
            frequency, summary, reference, locations, url
        )

    def to_inner_structure(self):
        return {
            "comp_id": self.compliance_id,
            "s_pro": self.statutory_provision,
            "c_task": self.compliance_task,
            "descrip": self.description,
            "p_cons": self.penal_consequences,
            "is_active": self.is_active,
            "freq": self.frequency,
            "summary": self.summary,
            "refer": self.reference,
            "locat": self.locations,
            "url": self.url
        }

class GetComplianceEditSuccess(Response):
    def __init__(
        self, mapping_id, country_id, domain_id, nature_id, org_list,
        statu_list, compliance_list, geo_list, allow_domain_edit
    ):
        self.mapping_id = mapping_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.nature_id = nature_id
        self.org_list = org_list
        self.statu_list = statu_list
        self.compliance_list = compliance_list
        self.geo_list = geo_list
        self.allow_domain_edit = allow_domain_edit

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "m_id", "c_id", "d_id", "s_n_id", "i_ids",
            "s_ids", "comp_list", "g_ids", "allow_domain_edit"
        ])
        mapping_id = data.get("m_id")
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        nature_id = data.get("s_n_id")
        org_list = data.get("i_ids")
        statu_list = data.get("s_ids")
        comp_list = data.get("comp_list")
        geo_list = data.get("g_ids")
        allow_domain_edit = data.get("allow_domain_edit")
        return GetComplianceEditSuccess(
            mapping_id, country_id, domain_id, nature_id, org_list,
            statu_list, comp_list, geo_list, allow_domain_edit
        )

    def to_inner_structure(self):
        return {
            "m_id": self.mapping_id,
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "s_n_id": self.nature_id,
            "i_ids": self.org_list,
            "s_ids": self.statu_list,
            "comp_list": self.compliance_list,
            "g_ids": self.geo_list,
            "allow_domain_edit": self.allow_domain_edit
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
        GetStatutoryMasterSuccess,
        GetApproveStatutoryMappingSuccess,
        GetComplianceInfoSuccess,
        GetApproveStatutoryMappingFilterSuccess,
        GetComplianceEditSuccess, UpdateComplianceSuccess
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
        request = parse_VariantType(
            request, "knowledgetransaction", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "knowledgetransaction", "Response"
            )
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

class MappingApproveInfo(object):
    def __init__(
        self, mapping_id, compliance_id, country_id, domain_id,
        compliance_task, is_active, created_by, created_on, updated_by,
        updated_on, nature_name, organisations, mapping_text
    ):
        self.mapping_id = mapping_id
        self.compliance_id = compliance_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.compliance_task = compliance_task
        self.is_active = is_active
        self.created_by = created_by
        self.created_on = created_on
        self.updated_by = updated_by
        self.updated_on = updated_on
        self.nature_name = nature_name
        self.organisations = organisations
        self.mapping_text = mapping_text

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "m_id", "comp_id", "c_id", "d_id", "c_task", "is_active",
            "c_by", "c_on", "u_by", "u_on", "s_n_name", "org_names",
            "map_text"
        ])
        mapping_id = data.get("m_id")
        compliance_id = data.get("comp_id")
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        compliance_task = data.get("c_task")
        is_active = data.get("is_active")
        created_by = data.get("c_by")
        created_on = data.get("c_on")
        updated_by = data.get("u_by")
        updated_on = data.get("u_on")
        nature_name = data.get("s_n_name")
        organisations = data.get("org_namees")
        mapping_text = data.get("map_text")
        return MappingApproveInfo(
            mapping_id, compliance_id, country_id, domain_id, compliance_task,
            is_active, created_by, created_on, updated_by, updated_on,
            nature_name, organisations, mapping_text
        )

    def to_structure(self):
        return {
            "m_id": self.mapping_id,
            "comp_id": self.compliance_id,
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "c_task": self.compliance_task,
            "is_active": self.is_active,
            "c_by": self.created_by,
            "c_on": self.created_on,
            "u_by": self.updated_by,
            "u_on": self.updated_on,
            "s_n_name": self.nature_name,
            "org_names": self.organisations,
            "map_text": self.mapping_text
        }

class ApproveMapping(object):
    def __init__(
        self, country_name, domain_name, nature_name,
        mapping_text, compliance_task, approval_status_id,
        remarks, mapping_id, compliance_id, is_common, updated_by

    ):
        self.country_name = country_name
        self.domain_name = domain_name
        self.nature_name = nature_name
        self.mapping_text = mapping_text
        self.compliance_task = compliance_task
        self.approval_status_id = approval_status_id
        self.remarks = remarks
        self.mapping_id = mapping_id
        self.compliance_id = compliance_id
        self.is_common = is_common
        self.updated_by = updated_by

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_name", "d_name", "s_n_name", "map_text",
            "c_task", "a_s_id", "remarks", "m_id",
            "comp_id", "is_common", "u_by"
        ])
        c_name = data.get("c_name")
        d_name = data.get("d_name")
        s_n_name = data.get("s_n_name")
        map_text = data.get("map_text")
        c_task = data.get("c_task")
        a_s_id = data.get("a_s_id")
        remarks = data.get("remarks")
        m_id = data.get("m_id")
        comp_id = data.get("comp_id")
        is_common = data.get("is_common")
        updated_by = data.get("u_by")
        return ApproveMapping(
            c_name, d_name, s_n_name, map_text, c_task, a_s_id,
            remarks, m_id, comp_id, is_common, updated_by
        )

    def to_structure(self):
        return {
            "c_name": self.country_name,
            "d_name": self.domain_name,
            "s_n_name": self.nature_name,
            "map_text": self.mapping_text,
            "c_task": self.compliance_task,
            "a_s_id": self.approval_status_id,
            "remarks": self.remarks,
            "m_id": self.mapping_id,
            "comp_id": self.compliance_id,
            "is_common": self.is_common,
            "u_by": self.updated_by
        }

class ComplianceList(object):
    def __init__(
        self, compliance_id, statutory_provision,
        compliance_task, document_name, description,
        penal_consequences, is_active,
        frequency_id, statutory_dates, repeats_type_id,
        repeats_every, duration_type_id, duration,
        format_file, file_list,
        summary, reference, frequency, is_file_removed
    ):
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_task = compliance_task
        self.document_name = document_name
        self.description = description
        self.penal_consequences = penal_consequences
        self.is_active = is_active
        self.frequency_id = frequency_id
        self.statutory_dates = statutory_dates
        self.repeats_type_id = repeats_type_id
        self.repeats_every = repeats_every
        self.duration_type_id = duration_type_id
        self.duration = duration
        self.format_file = format_file
        self.file_list = file_list
        self.summary = summary
        self.reference = reference
        self.frequency = frequency
        self.is_file_removed = is_file_removed

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "s_provision",
            "comp_task", "doc_name", "description",
            "p_consequences", "is_active",
            "f_id", "statu_dates", "r_type_id", "r_every",
            "d_type_id", "duration", "file_name",
            "summary", "reference", "f_f_list", "frequency", "is_file_removed",
        ])
        compliance_id = data.get("comp_id")
        statutory_provision = data.get("s_provision")
        compliance_task = data.get("comp_task")
        document_name = data.get("doc_name")
        description = data.get("description")
        penal_consequences = data.get("p_consequences")
        is_active = data.get("is_active")
        frequency = data.get("f_id")
        statu_dates = data.get("statu_dates")
        repeats_type_id = data.get("r_type_id")
        repeats_every = data.get("r_every")
        duration_type_id = data.get("d_type_id")
        duration = data.get("duration")
        file_name = data.get("file_name")
        summary = data.get("summary")
        reference = data.get("reference")
        file_list = data.get("f_f_list")
        frequency = data.get("frequency")
        is_file_removed = data.get("is_file_removed")

        return GetComplianceInfoSuccess(
            compliance_id, statutory_provision,
            compliance_task, document_name, description,
            penal_consequences, is_active,
            frequency, statu_dates, repeats_type_id,
            repeats_every, duration_type_id, duration,
            file_name, file_list,
            summary, reference, frequency, is_file_removed,
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id,
            "s_provision": self.statutory_provision,
            "comp_task": self.compliance_task,
            "doc_name": self.document_name,
            "description": self.description,
            "p_consequences": self.penal_consequences,
            "is_active": self.is_active,
            "f_id": self.frequency_id,
            "statu_dates": self.statutory_dates,
            "r_type_id": self.repeats_type_id,
            "r_every": self.repeats_every,
            "d_type_id": self.duration_type_id,
            "duration": self.duration,
            "file_name": self.format_file,
            "summary": self.summary,
            "reference": self.reference,
            "f_f_list": self.file_list,
            "frequency": self.frequency,
            "is_file_removed": self.is_file_removed
        }
