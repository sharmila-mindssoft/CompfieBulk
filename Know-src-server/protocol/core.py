from protocol.jsonvalidators import (
    parse_enum, parse_dictionary, to_structure_dictionary_values
)
#
# SESSION_TYPE
#
class SESSION_TYPE(object):
    # Web = "Web" # Android = "Android" # IOS = "IOS"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Web", "Android", "IOS", "BlackBerry"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, SESSION_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, SESSION_TYPE.values())

#
# APPROVAL_STATUS
#
class ASSIGN_STATUTORY_APPROVAL_STATUS(object):
    def __init__(self):
        self._value = {
            0 : "Is_new",
            1 : "Yet to submit",
            2 : "Pending",
            3 : "Approved",
            4 : "Rejected",
            5 : "Assigned"
        }

    @staticmethod
    def values():
        return ASSIGN_STATUTORY_APPROVAL_STATUS._value.values()

    def value(self, key):
        print key
        return self._value.get(key)

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, ASSIGN_STATUTORY_APPROVAL_STATUS.values())

    def to_structure(self):
        return self._value

class APPROVAL_STATUS(object):
    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Yet to submit", "Pending", "Approved", "Rejected", "Approved & Notified"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, APPROVAL_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, APPROVAL_STATUS.values())

#
# COMPLIANCE_FREQUENCY
#
class COMPLIANCE_FREQUENCY(object):
    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["One Time", "Periodical", "Review", "Flexi Review", "On Occurrence"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_FREQUENCY.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_FREQUENCY.values())
#
# REPEATS_TYPE
#
class REPEATS_TYPE(object):
    # Year = "Year(s)" # Month = "Month(s)" # Day = "Day(s)"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Year(s)", "Month(s)", "Day(s)"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, REPEATS_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, REPEATS_TYPE.values())

#
# DURATION_TYPE
#
class DURATION_TYPE(object):
    # Day = "Day(s)" # Hour = "Hour(s)"
    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Month(s)", "Day(s)", "Hour(s)"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, DURATION_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, DURATION_TYPE.values())
#
# UserGroup
#
class UserGroup(object):
    def __init__(
        self, user_group_id, user_category_id, user_group_name, is_active
    ):
        self.user_group_id = user_group_id
        self.user_category_id = user_category_id
        self.user_group_name = user_group_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_group_id", "user_category_id", "user_group_name", "is_active"
        ])
        return UserGroup(
            data.get("user_group_id"), data.get("user_category_id"),
            data.get("user_group_name"), data.get("is_active")
        )

    def to_structure(self):
        data = {
            "user_group_id": self.user_group_id,
            "user_category_id": self.user_category_id,
            "user_group_name": self.user_group_name,
            "is_active": self.is_active,
        }
        return data

class UserCategory(object):
    def __init__(self, user_category_id, user_category_name):
        self.user_category_id = user_category_id
        self.user_category_name = user_category_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_category_id", "user_category_name"])
        return UserCategory(
            data.get("user_category_id"), data.get("user_category_name")
        )

    def to_structure(self):
        return {
            "user_category_id": self.user_category_id,
            "user_category_name": self.user_category_name,
        }
#
# Country
#
class Country(object):
    def __init__(self, country_id, country_name, is_active):
        self.country_id = country_id
        self.country_name = country_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["country_id", "country_name", "is_active"])
        return Country(
            data.get("country_id"), data.get("country_name"), data.get("is_active")
        )

    def to_structure(self):
        data = {
            "country_id": self.country_id, "country_name": self.country_name, "is_active": self.is_active
        }
        return to_structure_dictionary_values(data)
#
# Domain
#
class Domain(object):
    def __init__(
        self, country_ids, country_names, domain_id, domain_name, is_active
    ):
        self.country_ids = country_ids
        self.country_names = country_names
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_ids", "c_names", "domain_id", "domain_name", "is_active"
        ])
        return Domain(
            data.get("country_ids"), data.get("c_names"), data.get("domain_id"),
            data.get("domain_name"), data.get("is_active")
        )

    def to_structure(self):
        data = {
            "country_ids": self.country_ids,
            "c_names": self.country_names,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "is_active": self.is_active,
        }
        return to_structure_dictionary_values(data)
#
# Level
#
class Level(object):
    def __init__(self, level_id, level_position, level_name):
        self.level_id = level_id
        self.level_position = level_position
        self.level_name = level_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["l_id", "l_position", "l_name"])
        return Level(
            data.get("l_id"), data.get("l_position"), data.get("l_name")
        )

    def to_structure(self):
        data = {
            "l_id": self.level_id,
            "l_position": self.level_position,
            "l_name": self.level_name,
        }
        return to_structure_dictionary_values(data)
#
# GeographyLevel
#
class GeographyLevel(object):
    def __init__(self, level_id, level_position, level_name):
        self.level_id = level_id
        self.level_position = level_position
        self.level_name = level_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "l_id", "l_position", "l_name"
        ])
        return GeographyLevel(
            data.get("l_id"), data.get("l_position"), data.get("l_name")
        )

    def to_structure(self):
        data = {
            "l_id": self.level_id,
            "l_position": self.level_position,
            "l_name": self.level_name,
        }
        return data
#
# Geography
#
class Geography(object):
    def __init__(
        self, geography_id, geography_name, level_id,
        parent_ids, parent_id, is_active
    ):
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.level_id = level_id
        self.parent_ids = parent_ids
        self.parent_id = parent_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "geography_id", "geography_name", "level_id",
            "parent_ids", "parent_id", "is_active"
        ])
        return Geography(
            data.get("geography_id"), data.get("geography_name"), data.get("level_id"),
            data.get("parent_ids"), data.get("parent_id"), data.get("is_active")
        )

    def to_structure(self):
        data = {
            "geography_id": self.geography_id,
            "geography_name": self.geography_name,
            "level_id": self.level_id,
            "parent_ids": self.parent_ids,
            "parent_id": self.parent_id,
            "is_active": self.is_active,
        }
        return data
#
# Geography With Mapping & country for unit
#
class UnitGeographyMapping(object):
    def __init__(
        self, geography_id, geography_name, level_id, mapping,
        parent_ids, country_id, is_active
    ):
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.level_id = level_id
        self.mapping = mapping
        self.parent_ids = parent_ids
        self.country_id = country_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "geography_id", "geography_name", "level_id", "mapping",
            "parent_ids", "country_id", "is_active"
        ])
        return UnitGeographyMapping(
            data.get("geography_id"), data.get("geography_name"), data.get("level_id"),
            data.get("mapping"), data.get("parent_ids"), data.get("country_id"),
            data.get("is_active")
        )

    def to_structure(self):
        data = {
            "geography_id": self.geography_id, "geography_name": self.geography_name, "level_id": self.level_id,
            "mapping": self.mapping, "parent_ids": self.parent_ids, "country_id": self.country_id, "is_active": self.is_active,
        }
        return data

#
# Geography level & country for unit
#

class UnitGeographyLevel(object):
    def __init__(self, level_id, level_position, level_name, country_id):
        self.level_id = level_id
        self.level_position = level_position
        self.level_name = level_name
        self.country_id = country_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["l_id", "l_position", "l_name", "c_id"])
        return UnitGeographyLevel(
            data.get("l_id"), data.get("l_position"), data.get("l_name"), data.get("c_id")
        )

    def to_structure(self):
        data = {
            "l_id": self.level_id, "l_position": self.level_position, "l_name": self.level_name, "c_id": self.country_id,
        }
        return data
#
# Industry
#
class Industry(object):
    def __init__(
        self, country_id, country_name, domain_id, domain_name, industry_id,
        industry_name, is_active
    ):
        self.country_id = country_id
        self.country_name = country_name
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "country_name", "domain_id", "domain_name",
                "industry_id", "industry_name", "is_active"
            ]
        )
        return Industry(
            data.get("country_id"), data.get("country_name"), data.get("domain_id"),
            data.get("domain_name"), data.get("industry_id"), data.get("industry_name"),
            data.get("is_active")
        )

    def to_structure(self):
        data = {
            "country_id": self.country_id, "country_name": self.country_name,
            "domain_id": self.domain_id, "domain_name": self.domain_name, "industry_id": self.industry_id,
            "industry_name": self.industry_name, "is_active": self.is_active
        }
        return to_structure_dictionary_values(data)

class Industries(object):
    def __init__(self, industry_id, industry_name, is_active):
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["industry_id", "industry_name", "is_active"])

        return Industries(
            data.get("industry_id"), data.get("industry_name"),
            data.get("is_active")
        )

    def to_structure(self):
        data = {
            "industry_id": self.industry_id, "industry_name": self.industry_name, "is_active": self.is_active,
        }
        return data

class UnitIndustries(object):
    def __init__(
        self, industry_id, industry_name, country_id, domain_id,
        client_id, unit_count, legal_entity_id, is_active
    ):
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.country_id = country_id
        self.domain_id = domain_id
        self.client_id = client_id
        self.unit_count = unit_count
        self.legal_entity_id = legal_entity_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "industry_id", "industry_name", "country_id", "domain_id",
            "client_id", "unit_count", "legal_entity_id", "is_active"
        ])
        return UnitIndustries(
            data.get("industry_id"), data.get("industry_name"), data.get("country_id"),
            data.get("domain_id"), data.get("client_id"), data.get("unit_count"), data.get("legal_entity_id"),
            data.get("is_active")
        )

    def to_structure(self):
        data = {
            "industry_id": self.industry_id,
            "industry_name": self.industry_name,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "client_id": self.client_id,
            "unit_count": self.unit_count,
            "legal_entity_id": self.legal_entity_id,
            "is_active": self.is_active,
        }
        return data
#
# StatutoryNature
#
class StatutoryNature(object):
    def __init__(
        self, statutory_nature_id, statutory_nature_name, country_id,
        country_name, is_active
    ):
        self.statutory_nature_id = statutory_nature_id
        self.statutory_nature_name = statutory_nature_name
        self.country_id = country_id
        self.country_name = country_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["statutory_nature_id", "statutory_nature_name", "is_active"]
        )
        return StatutoryNature(
            data.get("statutory_nature_id"), data.get("statutory_nature_name"),
            data.get("country_id"), data.get("country_name"), data.get("is_active")
        )

    def to_structure(self):
        data = {
            "statutory_nature_id": self.statutory_nature_id,
            "statutory_nature_name": self.statutory_nature_name,
            "country_id": self.country_id,
            "country_name": self.country_name,
            "is_active": self.is_active,
        }
        return data
#
# Statutory
#

class Level1Statutory(object):
    def __init__(self, level_1_statutory_id, level_1_statutory_name):
        self.level_1_statutory_id = level_1_statutory_id
        self.level_1_statutory_name = level_1_statutory_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "level_1_statutory_id", "level_1_statutory_name"
        ])
        return Statutory(
            data.get("level_1_statutory_id"), data.get("level_1_statutory_name")
        )

    def to_structure(self):
        return {
            "level_1_statutory_id": self.level_1_statutory_id,
            "level_1_statutory_name": self.level_1_statutory_name
        }
#
# Statutory
#

class Statutory(object):
    def __init__(
        self, statutory_id, statutory_name, level_id, parent_ids,
        parent_id, parent_mappings
    ):
        self.statutory_id = statutory_id
        self.statutory_name = statutory_name
        self.level_id = level_id
        self.parent_ids = parent_ids
        self.parent_id = parent_id
        self.parent_mappings = parent_mappings

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "statutory_id", "statutory_name", "level_id", "parent_ids",
            "parent_id", "parent_mappings"
        ])
        return Statutory(
            data.get("statutory_id"), data.get("statutory_name"), data.get("level_id"),
            data.get("parent_ids"), data.get("parent_id"), data.get("parent_mappings")
        )

    def to_structure(self):
        return {
            "statutory_id": self.statutory_id,
            "statutory_name": self.statutory_name,
            "level_id": self.level_id,
            "parent_ids": self.parent_ids,
            "parent_id": self.parent_id,
            "parent_mappings": self.parent_mappings,
        }


#
# Statutory
#

class Level1StatutoryList(object):
    def __init__(self, level_1_statutory_id, level_1_statutory_name, country_id, domain_id):
        self.level_1_statutory_id = level_1_statutory_id
        self.level_1_statutory_name = level_1_statutory_name
        self.country_id = country_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "level_1_statutory_id", "level_1_statutory_name", "country_id", "domain_id"
        ])
        return Level1StatutoryList(
            data.get("level_1_statutory_id"), data.get("level_1_statutory_name"), data.get("country_id"),
            data.get("domain_id")
        )

    def to_structure(self):
        data = {
            "level_1_statutory_id": self.level_1_statutory_id,
            "level_1_statutory_name": self.level_1_statutory_name,
            "country_id": self.country_id,
            "domain_id": self.domain_id
        }
        return to_structure_dictionary_values(data)

#
# FileList
#

class FileList(object):
    def __init__(self, file_size, file_name, file_content):
        self.file_size = file_size
        self.file_name = file_name
        self.file_content = file_content

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["file_size", "file_name", "file_content"])
        return FileList(
            data.get("file_size"), data.get("file_name"), data.get("file_content")
        )

    def to_structure(self):
        return {
            "file_size": self.file_size,
            "file_name": self.file_name,
            "file_content": self.file_content
        }
#
# Compliance
#

class Compliance_Download(object):
    def __init__(self, compliance_name, url):
        self.compliance_name = compliance_name
        self.url = url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", 'url'])
        return Compliance_Download(
            data.get("compliance_name"), data.get("url")
        )

    def to_structure(self):
        return {
            "compliance_name": self.compliance_name,
            "url": self.url
        }

class Compliance(object):
    def __init__(
        self, compliance_id, statutory_provision,
        compliance_task, description, document_name,
        format_file_list, penal_consequences,
        frequency_id, statutory_dates, repeats_type_id,
        repeats_every, duration_type_id,
        duration, is_active,
        frequency, summary, reference, is_file_removed
    ):
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_task = compliance_task
        self.description = description
        self.document_name = document_name
        self.format_file_list = format_file_list
        self.penal_consequences = penal_consequences
        self.frequency_id = frequency_id
        self.statutory_dates = statutory_dates
        self.repeats_type_id = repeats_type_id
        self.repeats_every = repeats_every
        self.duration_type_id = duration_type_id
        self.duration = duration
        self.is_active = is_active
        self.frequency = frequency
        self.summary = summary
        self.reference = reference
        self.is_file_removed = is_file_removed

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "s_provision", "comp_task", "description", "doc_name", "f_f_list",
            "p_consequences", "f_id", "statu_dates", "r_type_id", "r_every", "d_type_id",
            "duration", "is_active", "frequency", "summary", "reference", "is_file_removed"
        ])
        return Compliance(
            data.get("comp_id"), data.get("s_provision"), data.get("comp_task"),
            data.get("description"), data.get("doc_name"), data.get("f_f_list"),
            data.get("p_consequences"), data.get("f_id"), data.get("statu_dates"),
            data.get("r_type_id"), data.get("r_every"), data.get("d_type_id"),
            data.get("duration"), data.get("is_active"), data.get("frequency"),
            data.get("summary"), data.get("reference"), data.get("is_file_removed")
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id,
            "s_provision": self.statutory_provision,
            "comp_task": self.compliance_task,
            "description": self.description,
            "doc_name": self.document_name,
            "f_f_list": self.format_file_list,
            "p_consequences": self.penal_consequences,
            "f_id": self.frequency_id,
            "statu_dates": self.statutory_dates,
            "r_type_id": self.repeats_type_id,
            "r_every": self.repeats_every,
            "d_type_id": self.duration_type_id,
            "duration": self.duration,
            "is_active": self.is_active,
            "frequency": self.frequency,
            "summary": self.summary,
            "reference": self.reference,
            "is_file_removed": self.is_file_removed
        }

#
# StatutoryMapping
#
def getMappingApprovalStatus(status_id):
    dict = {
        0: "Yet to submit",
        1: "Pending",
        2: "Approved",
        3: "Approved & Notified",
        4: "Rejected",
    }

    return dict.get(status_id)

class MappedCompliance(object):
    def __init__(
        self, compliance_id, compliance_name, is_active, is_approved,
        approved_status, remarks
    ):
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.is_active = is_active
        self.is_approved = is_approved
        self.approve_status = approved_status
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id," "comp_name", "is_active",
            "is_approved", "approval_status_text",
            "remarks"
        ])
        return MappedCompliance(
            data.get("comp_id"), data.get("com_name"), data.get("is_active"),
            data.get("is_approved"), data.get("approval_status_text"), data.get("remarks")
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id, "comp_name": self.compliance_name,
            "is_active": self.is_active, "is_approved": self.is_approved,
            "approval_status_text": self.approve_status,
            "remarks": self.remarks
        }

class StatutoryMapping(object):
    def __init__(
        self, country_name,
        domain_name, industry_names,
        statutory_nature_name,
        statutory_mappings, mapped_compaliances,
        geography_mappings,
        approval_status, is_active, approval_status_text,
        mapping_id
    ):
        self.country_name = country_name
        self.domain_name = domain_name
        self.industry_names = industry_names
        self.statutory_nature_name = statutory_nature_name
        self.statutory_mappings = statutory_mappings
        self.mapped_compliances = mapped_compaliances
        self.geography_mappings = geography_mappings
        self.approval_status = approval_status
        self.is_active = is_active
        self.approval_status_text = approval_status_text
        self.mapping_id = mapping_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_name",
            "d_name", "i_names",
            "s_n_name",
            "s_maps",
            "mapped_comps",
            "geo_maps", "a_s_id", "is_active",
            "a_s_t", "m_id"
        ])
        return StatutoryMapping(
            data.get("c_name"), data.get("d_name"), data.get("i_names"), data.get("s_n_name"),
            data.get("s_maps"), data.get("mapped_comps"), data.get("geo_maps"),
            data.get("a_s_id"), data.get("is_active"), data.get("a_s_t"), data.get("m_id")
        )

    def to_structure(self):
        return {
            "c_name": self.country_name, "d_name": self.domain_name,
            "i_names": self.industry_names, "s_n_name": self.statutory_nature_name,
            "s_maps": self.statutory_mappings, "mapped_comps": self.mapped_compliances,
            "geo_maps": self.geography_mappings, "a_s_id": self.approval_status,
            "is_active": self.is_active, "a_s_t": self.approval_status_text,
            "m_id": self.mapping_id
        }

#
# GroupCompanyForUnitCreation
#

class GroupCompanyForUnitCreation(object):
    def __init__(
        self, client_id, group_name, country_ids, domain_ids, next_unit_code
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.next_unit_code = next_unit_code

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "group_name",
            "country_ids", "domain_ids", "next_unit_code"
        ])
        return GroupCompanyForUnitCreation(
            data.get("client_id"), data.get("group_name"),
            data.get("country_ids"), data.get("domain_ids"), data.get("next_unit_code")
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id, "group_name": self.group_name,
            "country_ids": self.country_ids, "domain_ids": self.domain_ids,
            "next_unit_code": self.next_unit_code
        }
        return data

#
# GroupCompany
#

class GroupCompany(object):
    def __init__(
        self, client_id, group_name, is_active, country_ids, domain_ids
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.is_active = is_active
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "group_name", "is_active", "country_ids", "domain_ids"])

        return GroupCompany(
            data.get("client_id"), data.get("group_name"), data.get("is_active"),
            data.get("domain_ids"), data.get("country_ids")
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id, "group_name": self.group_name,
            "is_active": self.is_active, "country_ids": self.country_ids, "domain_ids": self.domain_ids,
        }
        return data


#
# ClientConfiguration
#

class ClientConfiguration(object):
    def __init__(self, country_id, domain_id, month_from, month_to):
        self.country_id = country_id
        self.domain_id = domain_id
        self.month_from = month_from
        self.month_to = month_to

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "month_from", "month_to"])
        return ClientConfiguration(
            data.get("country_id"), data.get("domain_id"), data.get("month_from"), data.get("month_to")
        )

    def to_structure(self):
        return {
            "country_id": self.country_id, "domain_id": self.domain_id, "month_from": self.month_from,
            "month_to": self.month_to,
        }

#
# BusinessGroup
#

class ClientBusinessGroupCountry(object):
    def __init__(self, business_group_id, business_group_name, client_id, country_id):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name
        self.client_id = client_id
        self.country_id = country_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "business_group_id", "business_group_name", "client_id", "country_id"
        ])
        return ClientBusinessGroupCountry(
            data.get("business_group_id"), data.get("business_group_name"), data.get("client_id"), data.get("country_id")
        )

    def to_structure(self):
        data = {
            "business_group_id": self.business_group_id, "business_group_name": self.business_group_name,
            "client_id": self.client_id, "country_id": self.country_id,
        }
        return data


class BusinessGroup(object):
    def __init__(self, business_group_id, business_group_name, client_id):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "business_group_id", "business_group_name", "client_id"
        ])
        return BusinessGroup(
            data.get("business_group_id"), data.get("business_group_name"), data.get("client_id")
        )

    def to_structure(self):
        data = {
            "business_group_id": self.business_group_id, "business_group_name": self.business_group_name,
            "client_id": self.client_id,
        }
        return data

class ClientBusinessGroup(object):
    def __init__(self, business_group_id, business_group_name):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_id", "business_group_name"])
        return ClientBusinessGroup(
            data.get("business_group_id"), data.get("business_group_name")
        )

    def to_structure(self):
        return {
            "business_group_id": self.business_group_id, "business_group_name": self.business_group_name,
        }


class ClientLegalEntity(object):
    def __init__(self, legal_entity_id, legal_entity_name, business_group_id):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id", "legal_entity_name", "business_group_id"])
        return ClientLegalEntity(
            data.get("legal_entity_id"), data.get("legal_entity_name"), data.get("business_group_id")
        )

    def to_structure(self):
        data = {
            "legal_entity_id": self.legal_entity_id, "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id,
        }
        return to_structure_dictionary_values(data)

#
# Division
#

class Division(object):
    def __init__(
        self, division_id, division_name, legal_entity_id,
        business_group_id, client_id
    ):
        self.division_id = division_id
        self.division_name = division_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["division_id", "division_name", "legal_entity_id", "business_group_id", "client_id"]
        )

        return Division(
            data.get("division_id"), data.get("division_name"), data.get("legal_entity_id"),
            data.get("business_group_id"), data.get("client_id")
        )

    def to_structure(self):
        data = {
            "division_id": self.division_id, "division_name": self.division_name,
            "legal_entity_id": self.legal_entity_id, "business_group_id": self.business_group_id,
            "client_id": self.client_id,
        }
        return data


#
# Category
#

class Category(object):
    def __init__(
        self, category_id, category_name, division_id, legal_entity_id,
        business_group_id, client_id
    ):
        self.category_id = category_id
        self.category_name = category_name
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "category_id", "category_name", "division_id",
                "legal_entity_id", "business_group_id",
                "client_id"
            ])
        return Category(
            data.get("category_id"), data.get("category_name"), data.get("division_id"),
            data.get("legal_entity_id"), data.get("business_group_id"), data.get("client_id")
        )

    def to_structure(self):
        return {
            "category_id": self.category_id, "category_name": self.category_name,
            "division_id": self.division_id, "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id, "client_id": self.client_id
        }

#
# Unit
#
class UnitDetails(object):
    def __init__(
        self, unit_id, client_id, business_group_id, legal_entity_id, country_id,
        division_id, category_name, geography_id, unit_code, unit_name, address,
        postal_code, domain_ids, i_ids, assign_count, is_active, is_approved,
        category_id, remarks
    ):
        self.unit_id = unit_id
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.division_id = division_id
        self.category_name = category_name
        self.geography_id = geography_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.domain_ids = domain_ids
        self.i_ids = i_ids
        self.assign_count = assign_count
        self.is_active = is_active
        self.is_approved = is_approved
        self.category_id = category_id
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "unit_id", "client_id", "business_group_id", "legal_entity_id", "country_id", "division_id", "category_name",
                "geography_id", "unit_code", "unit_name", "address", "postal_code", "domain_ids", "i_ids",
                "assign_count", "is_active", "is_approved", "category_id", "remarks"
        ])
        return UnitDetails(
            data.get("unit_id"), data.get("client_id"), data.get("business_group_id"),
            data.get("legal_entity_id"), data.get("country_id"), data.get("division_id"),
            data.get("category_name"), data.get("geography_id"), data.get("unit_code"),
            data.get("unit_name"), data.get("address"), data.get("postal_code"),
            data.get("domain_ids"), data.get("i_ids"), data.get("assign_count"),
            data.get("is_active"), data.get("is_approved"),
            data.get("category_id"), data.get("remarks")
        )

    def to_structure(self):
        data = {
            "unit_id": self.unit_id, "client_id": self.client_id,
            "business_group_id": self.business_group_id, "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id, "division_id": self.division_id,
            "category_name": self.category_name, "geography_id": self.geography_id,
            "unit_code": self.unit_code, "unit_name": self.unit_name,
            "address": self.address, "postal_code": self.postal_code,
            "domain_ids": self.domain_ids, "i_ids": self.i_ids, "assign_count": self.assign_count,
            "is_active": self.is_active, "is_approved": self.is_approved,
            "category_id": self.category_id, "remarks": self.remarks,
        }
        return to_structure_dictionary_values(data)

class UnitList(object):
    def __init__(
        self, client_id, business_group_id, legal_entity_id, country_id,
        country_name, client_name, business_group_name, legal_entity_name,
        is_approved
    ):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.country_name = country_name
        self.client_name = client_name
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.is_approved = is_approved

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "client_id", "business_group_id", "legal_entity_id", "country_id",
                "country_name", "client_name", "business_group_name", "legal_entity_name",
                "is_approved"
        ])

        return UnitList(
            data.get("client_id"), data.get("business_group_id"), data.get("legal_entity_id"),
            data.get("country_id"), data.get("country_name"), data.get("client_name"),
            data.get("business_group_name"), data.get("legal_entity_name"),
            data.get("is_approved")
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id, "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id, "country_id": self.country_id,
            "country_name": self.country_name, "client_name": self.client_name,
            "business_group_name": self.business_group_name, "legal_entity_name": self.legal_entity_name,
            "is_approved": self.is_approved
        }
        return to_structure_dictionary_values(data)

#
# UnitDetails
#

class Unit(object):
    def __init__(
        self, unit_id, division_id, legal_entity_id, business_group_id, client_id,
        unit_code, unit_name, address, is_active, domain_ids
    ):
        self.unit_id = unit_id
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.client_id = client_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.is_active = is_active
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "unit_id", "division_id", "legal_entity_id", "business_group_id",
                "client_id", "unit_code", "unit_name", "address", "is_active", "domain_ids"
            ])
        return Unit(
            data.get("unit_id"), data.get("division_id"), data.get("legal_entity_id"),
            data.get("business_group_id"), data.get("client_id"), data.get("unit_code"),
            data.get("unit_name"), data.get("address"), data.get("is_active"), data.get("domain_ids")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "division_id": self.division_id,
            "legal_entity_id": self.legal_entity_id, "business_group_id": self.business_group_id,
            "client_id": self.client_id, "unit_code": self.unit_code,
            "unit_name": self.unit_name, "address": self.address,
            "is_active": self.is_active, "domain_ids": self.domain_ids
        }

#
#   Units - Countries
#

class UnitCountries(object):
    def __init__(
        self, client_id, business_group_id, country_id, country_name
    ):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.country_id = country_id
        self.country_name = country_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["client_id", "business_group_id", "country_id", "country_name"]
        )
        return UnitCountries(
            data.get("client_id"), data.get("business_group_id"), data.get("country_id"), data.get("country_name")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id, "business_group_id": self.business_group_id,
            "country_id": self.country_id, "country_name": self.country_name
        }

#
# Audit UnitDetails
#

class AuditUnits(object):
    def __init__(
        self, client_id, business_group_id, legal_entity_id, division_id,
        category_id, unit_id, unit_name
    ):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.category_id = category_id
        self.unit_id = unit_id
        self.unit_name = unit_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_id", "business_group_id", "legal_entity_id", "division_id",
                "category_id", "unit_id", "unit_name"
            ])
        return AuditUnits(
            data.get("client_id"), data.get("business_group_id"), data.get("legal_entity_id"),
            data.get("division_id"), data.get("category_id"), data.get("unit_id"), data.get("unit_name")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id, "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id, "division_id": self.division_id,
            "category_id": self.category_id, "unit_id": self.unit_id, "unit_name": self.unit_name
        }

#
#   Units - legal Entity details
#

class UnitLegalEntity(object):
    def __init__(
        self, legal_entity_id, legal_entity_name, business_group_id, client_id, country_id,
        le_expiry_days, is_approved
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.client_id = client_id
        self.country_id = country_id
        self.le_expiry_days = le_expiry_days
        self.is_approved = is_approved

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id", "legal_entity_name", "business_group_id", "client_id", "country_id",
                "le_expiry_days", "is_approved"
            ]
        )
        return UnitLegalEntity(
            data.get("legal_entity_id"), data.get("legal_entity_name"), data.get("business_group_id"),
            data.get("client_id"), data.get("country_id"), data.get("le_expiry_days"), data.get("is_approved")
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id, "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id, "client_id": self.client_id,
            "country_id": self.country_id, "le_expiry_days": self.le_expiry_days,
            "is_approved": self.is_approved
        }

class AssignUnitLegalEntity(object):
    def __init__(
        self, legal_entity_id, legal_entity_name, business_group_id, client_id
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["legal_entity_id", "legal_entity_name", "business_group_id", "client_id"]
        )
        return AssignUnitLegalEntity(
            data.get("legal_entity_id"), data.get("legal_entity_name"),
            data.get("business_group_id"), data.get("client_id")
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id, "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id, "client_id": self.client_id,
        }
#
#   Units - Domain & organisation
#
class UnitDomainOrganisation(object):
    def __init__(
        self, legal_entity_id, domain_id, domain_name, industry_id, industry_name, unit_count
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.unit_count = unit_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id", "domain_id", "domain_name", "industry_id", "industry_name", "unit_count"
            ]
        )
        return UnitDomainOrganisation(
            data.get("legal_entity_id"), data.get("domain_id"), data.get("domain_name"),
            data.get("industry_id"), data.get("industry_name"), data.get("unit_count")
        )

    def to_structure(self):
        data = {
            "legal_entity_id": self.legal_entity_id, "domain_id": self.domain_id,
            "domain_name": self.domain_name, "industry_id": self.industry_id,
            "industry_name": self.industry_name, "unit_count": self.unit_count
        }
        return data
#
# User
#
class User(object):
    def __init__(self, user_id, user_category_id, employee_name, is_active):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.employee_name = employee_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_category_id", "employee_name", "is_active"])
        return User(
            data.get("user_id"), data.get("user_category_id"), data.get("employee_name"),
            data.get("is_active")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "user_category_id": self.user_category_id,
            "employee_name": self.employee_name, "is_active": self.is_active
        }

#
# Audit Trail Client User
#

class AuditTrailClientUser(object):
    def __init__(self, user_id, user_category_id, client_id, user_category_name, employee_name, is_active):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.client_id = client_id
        self.user_category_name = user_category_name
        self.employee_name = employee_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_category_id", "client_id", "user_category_name", "employee_name", "is_active"
        ])
        return AuditTrailClientUser(
            data.get("user_id"), data.get("user_category_id"), data.get("client_id"),
            data.get("user_category_name"), data.get("employee_name"), data.get("is_active")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "user_category_id": self.user_category_id, "client_id": self.client_id,
            "user_category_name": self.user_category_name, "employee_name": self.employee_name,
            "is_active": self.is_active
        }


class DomainUser(object):
    def __init__(self, user_id, legal_entity_id):
        self.user_id = user_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "legal_entity_id"])
        return DomainUser(
            data.get("user_id"), data.get("legal_entity_id")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "legal_entity_id": self.legal_entity_id,
        }

#
# UserDetails
#

class UserDetails(object):
    def __init__(
        self, user_id, user_category_id, user_category_name, employee_name,
        employee_code,  email_id, user_group_id,
        contact_no, mobile_no, address, designation, country_ids,
        domain_ids, is_active, is_disable, username,
        allow_enable, days_left, d_reason
    ):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.user_category_name = user_category_name
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.email_id = email_id
        self.user_group_id = user_group_id
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.address = address
        self.designation = designation
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.is_active = is_active
        self.is_disable = is_disable
        self.username = username
        self.allow_enable = allow_enable
        self.days_left = days_left
        self.d_reason = d_reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_category_id", "user_category_name", "employee_name", "employee_code",
            "email_id", "user_group_id", "contact_no", "mobile_no", "address", "designation",
            "country_ids", "country_wise_domain", "is_active", "is_disable", "username_id",
            "allow_enable", "days_left", "d_reason"
        ])
        return UserDetails(
            data.get("user_id"), data.get("user_category-id"), data.get("user_category_name"),
            data.get("employee_name"), data.get("employee_code"), data.get("email_id"),
            data.get("user_group_id"), data.get("contact_no"), data.get("mobile_no"),
            data.get("address"), data.get("designation"), data.get("country_ids"),
            data.get("country_wise_domain"), data.get("is_active"), data.get("is_disable"),
            data.get("username_id"), data.get("allow_enable"), data.get("days_left"), data.get("d_reason")
        )

    def to_structure(self):
        return {
            "user_id" : self.user_id, "user_category_id": self.user_category_id, "user_category_name": self.user_category_name,
            "employee_name": self.employee_name, "employee_code": self.employee_code, "email_id": self.email_id,
            "user_group_id": self.user_group_id, "contact_no": self.contact_no, "mobile_no": self.mobile_no,
            "address": self.address, "designation": self.designation, "country_ids": self.country_ids,
            "country_wise_domain": self.domain_ids, "is_active": self.is_active, "is_disable": self.is_disable,
            "username_id": self.username, "allow_enable": self.allow_enable, "days_left": self.days_left,
            "d_reason": self.d_reason
        }
#
# StatutoryDate
#

class StatutoryDate(object):
    def __init__(self, statutory_date, statutory_month, trigger_before_days, repeat_by):
        self.statutory_date = statutory_date
        self.statutory_month = statutory_month
        self.trigger_before_days = trigger_before_days
        self.repeat_by = repeat_by

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_date", "statutory_month", "trigger_before_days", "repeat_by"])
        return StatutoryDate(
            data.get("statutory_date"), data.get("statutory_month"), data.get("trigger_before_days"),
            data.get("repeat_by")
        )

    def to_structure(self):
        return {
            "statutory_date": self.statutory_date, "statutory_month": self.statutory_month,
            "trigger_before_days": self.trigger_before_days, "repeat_by": self.repeat_by
        }
#
# Validity Dates
#
class ValidityDates(object):
    def __init__(self, validity_days_id, country_id, domain_id, validity_days):
        self.validity_days_id = validity_days_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.validity_days = validity_days

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "validity_days_id", "country_id", "domain_id", "validity_days"
            ]
        )
        return ValidityDates(
            data.get("validity_days_id"), data.get("country_id"), data.get("domain_id"),
            data.get("validity_days")
        )

    def to_structure(self):
        return {
            "validity_days_id": self.validity_days_id, "country_id": self.country_id,
            "domain_id": self.domain_id, "validity_days": self.validity_days
        }
#
# Client Group Master
#
class ClientGroupMaster(object):
    def __init__(
        self, country_ids, group_id, group_name, is_active, is_approved
    ):
        self.country_ids = country_ids
        self.group_id = group_id
        self.group_name = group_name
        self.is_active = is_active
        self.is_approved = is_approved

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "country_ids", "group_id", "group_name", "is_active", "is_approved", "remarks"
            ]
        )
        return ClientGroupMaster(
            data.get("country_ids"), data.get("group_id"), data.get("group_name"),
            data.get("is_active"), data.get("is_approved")
        )

    def to_structure(self):
        return {
            "country_ids": self.country_ids, "group_id": self.group_id,
            "group_name": self.group_name, "is_active": self.is_active, "is_approved": self.is_approved,
        }
#
# Client Group Master
#
class ClientGroup(object):
    def __init__(
        self, group_id, group_name, country_name,
        legal_entity_name, is_closed_cg, is_approved, reason
    ):
        self.group_id = group_id
        self.group_name = group_name
        self.country_name = country_name
        self.legal_entity_name = legal_entity_name
        self.is_closed_cg = is_closed_cg
        self.is_approved = is_approved
        self.reason = reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "group_id", "group_name", "country_name",
                "legal_entity_name", "is_closed_cg", "is_approved",
                "reason"
            ]
        )
        return ClientGroup(
            data.get("group_id"), data.get("group_name"), data.get("country_name"),
            data.get("legal_entity_name"), data.get("is_closed_cg"), data.get("is_approved"), data.get("reason")
        )

    def to_structure(self):
        return {
            "group_id": self.group_id, "group_name": self.group_name,
            "country_name": self.country_name, "legal_entity_name": self.legal_entity_name,
            "is_closed_cg": self.is_closed_cg, "is_approved": self.is_approved, "remarks": self.reason
        }

class ReassignClientGroup(object):
    def __init__(
        self, group_id, group_name,
    ):
        self.group_id = group_id
        self.group_name = group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["group_id", "group_name"])
        return ReassignClientGroup(
            data.get("group_id"), data.get("group_name")
        )

    def to_structure(self):
        return {
            "group_id": self.group_id, "group_name": self.group_name,
        }

class LegalEntity(object):
    def __init__(
        self, country_id, business_group, legal_entity_id,
        legal_entity_name, old_logo, new_logo,
        no_of_licence, file_space, contract_from,
        contract_to, domain_details
    ):
        self.country_id = country_id
        self.business_group = business_group
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.old_logo = old_logo
        self.new_logo = new_logo
        self.no_of_licence = no_of_licence
        self.file_space = file_space
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.domain_details = domain_details

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "business_group", "legal_entity_id",
                "legal_entity_name", "old_logo", "new_logo", "no_of_licence",
                "file_space", "contract_from", "contract_to", "domain_details"
            ]
        )
        return LegalEntity(
            data.get("country_id"), data.get("business_group"), data.get("legal_entity_id"),
            data.get("legal_entity_name"), data.get("old_logo"), data.get("new_logo"),
            data.get("no_of_licence"), data.get("file_space"), data.get("contract_from"),
            data.get("contract_to"), data.get("domain_details")
        )

    def to_structure(self):
        return {
            "country_id": self.country_id, "business_group": self.business_group, "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name, "old_logo": self.old_logo, "new_logo": self.new_logo,
            "no_of_licence": self.no_of_licence, "file_space": self.file_space, "contract_from": self.contract_from,
            "contract_to": self.contract_to, "domain_details": self.domain_details
        }

class LegalEntityList(object):
    def __init__(
        self, country_id, business_group, legal_entity_id,
        legal_entity_name, old_logo, new_logo,
        no_of_licence, file_space, contract_from,
        contract_to, domain_details, is_closed, is_approved
    ):
        self.country_id = country_id
        self.business_group = business_group
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.old_logo = old_logo
        self.new_logo = new_logo
        self.no_of_licence = no_of_licence
        self.file_space = file_space
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.domain_details = domain_details
        self.is_closed = is_closed
        self.is_approved = is_approved

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "business_group", "legal_entity_id",
                "legal_entity_name", "old_logo", "new_logo", "no_of_licence",
                "file_space", "contract_from", "contract_to", "domain_details",
                "is_closed", "is_approved"
            ]
        )
        return LegalEntity(
            data.get("country_id"), data.get("business_group"), data.get("legal_entity_id"),
            data.get("legal_entity_name"), data.get("old_logo"), data.get("new_logo"),
            data.get("no_of_licence"), data.get("file_space"), data.get("contract_from"),
            data.get("contract_to"), data.get("domain_details"), data.get("is_closed"),
            data.get("is_approved")
        )

    def to_structure(self):
        return {
            "country_id": self.country_id, "business_group": self.business_group,
            "legal_entity_id": self.legal_entity_id, "legal_entity_name": self.legal_entity_name,
            "old_logo": self.old_logo, "new_logo": self.new_logo,
            "no_of_licence": self.no_of_licence, "file_space": self.file_space,
            "contract_from": self.contract_from, "contract_to": self.contract_to,
            "domain_details": self.domain_details, "is_closed": self.is_closed,
            "is_approved": self.is_approved
        }

class Client(object):
    def __init__(
        self, client_id, group_name, is_active
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        d = parse_dictionary(
            data, ["client_id", "group_name", "is_active"]
        )
        return Client(
            d.get("client_id"), d.get("group_name"), d.get("is_active")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "is_active": self.is_active
        }

class UserMappingGroupDetails(object):
    def __init__(
        self, client_id, client_name, legal_entity_id, country_id, business_group_id
    ):
        self.client_id = client_id
        self.client_name = client_name
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        d = parse_dictionary(
            data, [
                "client_id", "client_name", "legal_entity_id", "country_id"
                "business_group_id"
            ]
        )
        return UserMappingGroupDetails(
            d.get("client_id"), d.get("client_name"), d.get("legal_entity_id"),
            d.get("country_id"), d.get("business_group_id")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "client_name": self.client_name,
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "business_group_id": self.business_group_id
        }

class UserMappingUnitDetails(object):
    def __init__(
        self, unit_id, unit_code_name, client_id, business_group_id, legal_entity_id, country_id,
        division_id, division_name, category_id, category_name
    ):
        self.unit_id = unit_id
        self.unit_code_name = unit_code_name
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.division_id = division_id
        self.division_name = division_name
        self.category_id = category_id
        self.category_name = category_name

    @staticmethod
    def parse_structure(data):
        d = parse_dictionary(
            data, [
                "unit_id", "unit_code_name", "client_id", "business_group_id", "legal_entity_id", "country_id",
                "division_id", "division_name", "category_id", "category_name"
            ]
        )
        return UserMappingUnitDetails(
            d.get("unit_id"), d.get("unit_code_name"), d.get("client_id"),
            d.get("business_group_id"), d.get("legal_entity_id"), d.get("country_id"),
            d.get("division_id"), d.get("division_name"), d.get("category_id"), d.get("category_name")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit_code_name": self.unit_code_name, "client_id": self.client_id,
            "business_group_id": self.business_group_id, "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id, "division_id": self.division_id,
            "division_name": self.division_name, "category_id": self.category_id, "category_name": self.category_name
        }

class UserMappingReportTechno(object):
    def __init__(
        self, unit_id, techno_manager, techno_user, unit_code_with_name
    ):
        self.unit_id = unit_id
        self.techno_manager = techno_manager
        self.techno_user = techno_user
        self.unit_code_with_name = unit_code_with_name

    @staticmethod
    def parse_structure(data):
        d = parse_dictionary(
            data, ["unit_id", "techno_manager", "techno_user", "unit_code_with_name"]
        )
        return UserMappingReportTechno(
            d.get("unit_id"), d.get("techno_manager"), d.get("techno_user"),
            d.get("unit_code_with_name")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "techno_manager": self.techno_manager,
            "techno_user": self.techno_user, "unit_code_with_name": self.unit_code_with_name
        }

class UserMappingReportDomain(object):
    def __init__(
        self, unit_id, employee_name, user_category_name, domain_id
    ):
        self.unit_id = unit_id
        self.employee_name = employee_name
        self.user_category_name = user_category_name
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        d = parse_dictionary(
            data, ["unit_id", "employee_name", "user_category_name", "domain_id"]
        )
        return UserMappingReportTechno(
            d.get("unit_id"), d.get("employee_name"), d.get("user_category_name"), d.get("domain_id")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "employee_name": self.employee_name,
            "user_category_name": self.user_category_name, "domain_id": self.domain_id
        }

class ChildUsers(object):
    def __init__(self, user_id, employee_name):
        self.user_id = user_id
        self.employee_name = employee_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "employee_name"])
        return ChildUsers(data.get("user_id"), data.get("employee_name"))

    def to_structure(self):
        return {
            "user_id": self.user_id, "employee_name": self.employee_name,
        }


class DomainIndustryList(object):
    def __init__(self, domain_id, industry_id):
        self.domain_id = domain_id
        self.industry_id = industry_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["domain_id", "industry_id"])
        return DomainIndustryList(data.get("domain_id"), data.get("industry_id"))

    def to_structure(self):
        return {
            "domain_id": self.domain_id, "industry_id": self.industry_id,
        }
#
# Unit closure - Legal Entity
#
class UnitClosure_LegalEntity(object):
    def __init__(self, legal_entity_id, legal_entity_name):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["legal_entity_id", "legal_entity_name"])
        return UnitClosure_LegalEntity(data.get("legal_entity_id"), data.get("legal_entity_name"))

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id, "legal_entity_name": self.legal_entity_name,
        }

#
# Unit Closure - Units List
#
class UnitClosure_Units(object):
    def __init__(
        self, unit_id, unit_code, unit_name, address, postal_code,
        legal_entity_id, legal_entity_name, business_group_name, division_name,
        category_name, is_active, closed_on, validity_days
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.division_name = division_name
        self.category_name = category_name
        self.is_active = is_active
        self.closed_on = closed_on
        self.validity_days = validity_days

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "address", "postal_code",
            "legal_entity_id", "legal_entity_name", "business_group_name",
            "division_name", "category_name", "is_active", "closed_on",
            "validity_days"
            ])
        return UnitClosure_Units(
            data.get("unit_id"), data.get("unit_code"), data.get("unit_name"),
            data.get("address"), data.get("postal_code"), data.get("legal_entity_id"),
            data.get("legal_entity_name"), data.get("business_group_name"),
            data.get("division_name"), data.get("category_name"), data.get("is_active"),
            data.get("closed_on"), data.get("validity_days")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit_code": self.unit_code, "unit_name": self.unit_name,
            "address": self.address, "postal_code": self.postal_code, "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name, "business_group_name": self.business_group_name,
            "division_name": self.division_name, "category_name": self.category_name, "is_active": self.is_active,
            "closed_on": self.closed_on, "validity_days": self.validity_days,
        }
#
# Legal Entity Details
#
class LegalEntityDetails(object):
    def __init__(
        self, country_id, business_group, legal_entity_name,
        logo, no_of_licence, file_space, contract_from,
        contract_to, domain_details
    ):
        self.country_id = country_id
        self.business_group = business_group
        self.legal_entity_name = legal_entity_name
        self.logo = logo
        self.no_of_licence = no_of_licence
        self.file_space = file_space
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.domain_details = domain_details

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "business_group", "legal_entity_name", "logo",
                "no_of_licence", "file_space", "contract_from",
                "contract_to", "domain_details"
            ]
        )
        return LegalEntityDetails(
            data.get("country_id"), data.get("business_group"), data.get("legal_entity_name"),
            data.get("logo"), data.get("no_of_licence"), data.get("file_space"),
            data.get("contract_from"), data.get("contract_to"), data.get("domain_details")
        )

    def to_structure(self):
        return {
            "country_id": self.country_id, "business_group": self.business_group, "legal_entity_name": self.legal_entity_name,
            "logo": self.logo, "no_of_licence": self.no_of_licence, "file_space": self.file_space,
            "contract_from": self.contract_from, "contract_to": self.contract_to, "domain_details": self.domain_details
        }
