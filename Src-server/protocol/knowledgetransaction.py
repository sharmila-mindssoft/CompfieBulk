import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    parse_structure_VectorType_RecordType_core_Compliance,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    parse_structure_EnumType_core_APPROVAL_STATUS,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_SignedIntegerType_8,
    parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_VectorType_RecordType_core_Industry,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    parse_structure_Bool, parse_structure_Text,
    parse_structure_VectorType_RecordType_core_StatutoryNature,
    parse_structure_MapType_SignedIntegerType_8_RecordType_core_StatutoryMapping
)
from protocol.to_structure import (
to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    to_structure_VectorType_RecordType_core_Compliance,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    to_structure_EnumType_core_APPROVAL_STATUS,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_SignedIntegerType_8,
    to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    to_structure_VectorType_RecordType_core_Industry,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    to_structure_Bool, to_structure_Text,
    to_structure_VectorType_RecordType_core_StatutoryNature,
    to_structure_MapType_SignedIntegerType_8_RecordType_core_StatutoryMapping
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

class GetStatutoryMappings(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryMappings()

    def to_inner_structure(self):
        return {
        }

class SaveStatutoryMapping(Request):
    def __init__(self, country_id, domain_id, industry_ids, statutory_nature_id, statutory_ids, compliances, geography_ids):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_ids = industry_ids
        self.statutory_nature_id = statutory_nature_id
        self.statutory_ids = statutory_ids
        self.compliances = compliances
        self.geography_ids = geography_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "industry_ids", "statutory_nature_id", "statutory_ids", "compliances", "geography_ids"])
        country_id = data.get("country_id")
        country_id = parse_structure_SignedIntegerType_8(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_SignedIntegerType_8(domain_id)
        industry_ids = data.get("industry_ids")
        industry_ids = parse_structure_VectorType_SignedIntegerType_8(industry_ids)
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_id = parse_structure_SignedIntegerType_8(statutory_nature_id)
        statutory_ids = data.get("statutory_ids")
        statutory_ids = parse_structure_VectorType_SignedIntegerType_8(statutory_ids)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_core_Compliance(compliances)
        geography_ids = data.get("geography_ids")
        geography_ids = parse_structure_VectorType_SignedIntegerType_8(geography_ids)
        return SaveStatutoryMapping(country_id, domain_id, industry_ids, statutory_nature_id, statutory_ids, compliances, geography_ids)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "industry_ids": to_structure_VectorType_SignedIntegerType_8(self.industry_ids),
            "statutory_nature_id": to_structure_SignedIntegerType_8(self.statutory_nature_id),
            "statutory_ids": to_structure_VectorType_SignedIntegerType_8(self.statutory_ids),
            "compliances": to_structure_VectorType_RecordType_core_Compliance(self.compliances),
            "geography_ids": to_structure_VectorType_SignedIntegerType_8(self.geography_ids),
        }

class UpdateStatutoryMapping(Request):
    def __init__(self, statutory_mapping_id, industry_ids, statutory_nature_id, statutory_ids, compliances, geography_ids):
        self.statutory_mapping_id = statutory_mapping_id
        self.industry_ids = industry_ids
        self.statutory_nature_id = statutory_nature_id
        self.statutory_ids = statutory_ids
        self.compliances = compliances
        self.geography_ids = geography_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_mapping_id", "industry_ids", "statutory_nature_id", "statutory_ids", "compliances", "geography_ids"])
        statutory_mapping_id = data.get("statutory_mapping_id")
        statutory_mapping_id = parse_structure_SignedIntegerType_8(statutory_mapping_id)
        industry_ids = data.get("industry_ids")
        industry_ids = parse_structure_VectorType_SignedIntegerType_8(industry_ids)
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_id = parse_structure_SignedIntegerType_8(statutory_nature_id)
        statutory_ids = data.get("statutory_ids")
        statutory_ids = parse_structure_VectorType_SignedIntegerType_8(statutory_ids)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_core_Compliance(compliances)
        geography_ids = data.get("geography_ids")
        geography_ids = parse_structure_VectorType_SignedIntegerType_8(geography_ids)
        return UpdateStatutoryMapping(statutory_mapping_id, industry_ids, statutory_nature_id, statutory_ids, compliances, geography_ids)

    def to_inner_structure(self):
        return {
            "statutory_mapping_id": to_structure_SignedIntegerType_8(self.statutory_mapping_id),
            "industry_ids": to_structure_VectorType_SignedIntegerType_8(self.industry_ids),
            "statutory_nature_id": to_structure_SignedIntegerType_8(self.statutory_nature_id),
            "statutory_ids": to_structure_VectorType_SignedIntegerType_8(self.statutory_ids),
            "compliances": to_structure_VectorType_RecordType_core_Compliance(self.compliances),
            "geography_ids": to_structure_VectorType_SignedIntegerType_8(self.geography_ids),
        }

class ChangeStatutoryMappingStatus(Request):
    def __init__(self, statutory_mapping_id, is_active):
        self.statutory_mapping_id = statutory_mapping_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_mapping_id", "is_active"])
        statutory_mapping_id = data.get("statutory_mapping_id")
        statutory_mapping_id = parse_structure_SignedIntegerType_8(statutory_mapping_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeStatutoryMappingStatus(statutory_mapping_id, is_active)

    def to_inner_structure(self):
        return {
            "statutory_mapping_id": to_structure_SignedIntegerType_8(self.statutory_mapping_id),
            "is_active": to_structure_Bool(self.is_active),
        }

class ApproveStatutoryMapping(Request):
    def __init__(self, statutory_mapping_id, approval_status, rejected_reason, notification_text):
        self.statutory_mapping_id = statutory_mapping_id
        self.approval_status = approval_status
        self.rejected_reason = rejected_reason
        self.notification_text = notification_text

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_mapping_id", "approval_status", "rejected_reason", "notification_text"])
        statutory_mapping_id = data.get("statutory_mapping_id")
        statutory_mapping_id = parse_structure_SignedIntegerType_8(statutory_mapping_id)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_EnumType_core_APPROVAL_STATUS(approval_status)
        rejected_reason = data.get("rejected_reason")
        rejected_reason = parse_structure_Text(rejected_reason)
        notification_text = data.get("notification_text")
        notification_text = parse_structure_Text(notification_text)
        return ApproveStatutoryMapping(statutory_mapping_id, approval_status, rejected_reason, notification_text)

    def to_inner_structure(self):
        return {
            "statutory_mapping_id": to_structure_SignedIntegerType_8(self.statutory_mapping_id),
            "approval_status": to_structure_EnumType_core_APPROVAL_STATUS(self.approval_status),
            "rejected_reason": to_structure_Text(self.rejected_reason),
            "notification_text": to_structure_Text(self.notification_text),
        }


def _init_Request_class_map():
    classes = [GetStatutoryMappings, SaveStatutoryMapping, UpdateStatutoryMapping, ChangeStatutoryMappingStatus, ApproveStatutoryMapping]
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

class GetStatutoryMappingsSuccess(Response):
    def __init__(self, countries, domains, industries, statutory_natures, statutory_levels, statutories, geography_levels, geographies, statutory_mappings):
        self.countries = countries
        self.domains = domains
        self.industries = industries
        self.statutory_natures = statutory_natures
        self.statutory_levels = statutory_levels
        self.statutories = statutories
        self.geography_levels = geography_levels
        self.geographies = geographies
        self.statutory_mappings = statutory_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "industries", "statutory_natures", "statutory_levels", "statutories", "geography_levels", "geographies", "statutory_mappings"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        industries = data.get("industries")
        industries = parse_structure_VectorType_RecordType_core_Industry(industries)
        statutory_natures = data.get("statutory_natures")
        statutory_natures = parse_structure_VectorType_RecordType_core_StatutoryNature(statutory_natures)
        statutory_levels = data.get("statutory_levels")
        statutory_levels = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(statutory_levels)
        statutories = data.get("statutories")
        statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(statutories)
        geography_levels = data.get("geography_levels")
        geography_levels = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(geography_levels)
        geographies = data.get("geographies")
        geographies = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(geographies)
        statutory_mappings = data.get("statutory_mappings")
        statutory_mappings = parse_structure_MapType_SignedIntegerType_8_RecordType_core_StatutoryMapping(statutory_mappings)
        return GetStatutoryMappingsSuccess(countries, domains, industries, statutory_natures, statutory_levels, statutories, geography_levels, geographies, statutory_mappings)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "industries": to_structure_VectorType_RecordType_core_Industry(self.industries),
            "statutory_natures": to_structure_VectorType_RecordType_core_StatutoryNature(self.statutory_natures),
            "statutory_levels": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(self.statutory_levels),
            "statutories": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(self.statutories),
            "geography_levels": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(self.geography_levels),
            "geographies": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(self.geographies),
            "statutory_mappings": to_structure_MapType_SignedIntegerType_8_RecordType_core_StatutoryMapping(self.statutory_mappings),
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
    classes = [GetStatutoryMappingsSuccess, SaveStatutoryMappingSuccess, UpdateStatutoryMappingSuccess, InvalidStatutoryMappingId, ChangeStatutoryMappingStatusSuccess, ApproveStatutoryMappingSuccess]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

