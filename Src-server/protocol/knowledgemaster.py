import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    parse_structure_VectorType_RecordType_core_Level,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_SignedIntegerType_8,
    parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_VectorType_RecordType_core_Industry,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    parse_structure_Bool,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    parse_structure_VectorType_RecordType_core_StatutoryNature,
    parse_structure_CustomTextType_50
)
from protocol.to_structure import (
to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    to_structure_VectorType_RecordType_core_Level,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_SignedIntegerType_8,
    to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    to_structure_VectorType_RecordType_core_Industry,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    to_structure_Bool,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    to_structure_VectorType_RecordType_core_StatutoryNature,
    to_structure_CustomTextType_50
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

class GetGeographyLevels(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetGeographyLevels()

    def to_inner_structure(self):
        return {
        }

class SaveGeographyLevel(Request):
    def __init__(self, country_id, levels):
        self.country_id = country_id
        self.levels = levels

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "levels"])
        country_id = data.get("country_id")
        country_id = parse_structure_SignedIntegerType_8(country_id)
        levels = data.get("levels")
        levels = parse_structure_VectorType_RecordType_core_Level(levels)
        return SaveGeographyLevel(country_id, levels)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "levels": to_structure_VectorType_RecordType_core_Level(self.levels),
        }

class GetGeographies(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetGeographies()

    def to_inner_structure(self):
        return {
        }

class SaveGeography(Request):
    def __init__(self, geography_level_id, geography_name, parent_ids):
        self.geography_level_id = geography_level_id
        self.geography_name = geography_name
        self.parent_ids = parent_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["geography_level_id", "geography_name", "parent_ids"])
        geography_level_id = data.get("geography_level_id")
        geography_level_id = parse_structure_SignedIntegerType_8(geography_level_id)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_50(geography_name)
        parent_ids = data.get("parent_ids")
        parent_ids = parse_structure_VectorType_SignedIntegerType_8(parent_ids)
        return SaveGeography(geography_level_id, geography_name, parent_ids)

    def to_inner_structure(self):
        return {
            "geography_level_id": to_structure_SignedIntegerType_8(self.geography_level_id),
            "geography_name": to_structure_CustomTextType_50(self.geography_name),
            "parent_ids": to_structure_VectorType_SignedIntegerType_8(self.parent_ids),
        }

class UpdateGeography(Request):
    def __init__(self, geography_id, geography_level_id, geography_name, parent_ids):
        self.geography_id = geography_id
        self.geography_level_id = geography_level_id
        self.geography_name = geography_name
        self.parent_ids = parent_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["geography_id", "geography_level_id", "geography_name", "parent_ids"])
        geography_id = data.get("geography_id")
        geography_id = parse_structure_SignedIntegerType_8(geography_id)
        geography_level_id = data.get("geography_level_id")
        geography_level_id = parse_structure_SignedIntegerType_8(geography_level_id)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_50(geography_name)
        parent_ids = data.get("parent_ids")
        parent_ids = parse_structure_VectorType_SignedIntegerType_8(parent_ids)
        return UpdateGeography(geography_id, geography_level_id, geography_name, parent_ids)

    def to_inner_structure(self):
        return {
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "geography_level_id": to_structure_SignedIntegerType_8(self.geography_level_id),
            "geography_name": to_structure_CustomTextType_50(self.geography_name),
            "parent_ids": to_structure_VectorType_SignedIntegerType_8(self.parent_ids),
        }

class ChangeGeographyStatus(Request):
    def __init__(self, geography_id, is_active):
        self.geography_id = geography_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["geography_id", "is_active"])
        geography_id = data.get("geography_id")
        geography_id = parse_structure_SignedIntegerType_8(geography_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeGeographyStatus(geography_id, is_active)

    def to_inner_structure(self):
        return {
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "is_active": to_structure_Bool(self.is_active),
        }

class GetIndustries(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetIndustries()

    def to_inner_structure(self):
        return {
        }

class SaveIndustry(Request):
    def __init__(self, industry_name):
        self.industry_name = industry_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["industry_name"])
        industry_name = data.get("industry_name")
        industry_name = parse_structure_CustomTextType_50(industry_name)
        return SaveIndustry(industry_name)

    def to_inner_structure(self):
        return {
            "industry_name": to_structure_CustomTextType_50(self.industry_name),
        }

class UpdateIndustry(Request):
    def __init__(self, industry_id, industry_name):
        self.industry_id = industry_id
        self.industry_name = industry_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["industry_id", "industry_name"])
        industry_id = data.get("industry_id")
        industry_id = parse_structure_SignedIntegerType_8(industry_id)
        industry_name = data.get("industry_name")
        industry_name = parse_structure_CustomTextType_50(industry_name)
        return UpdateIndustry(industry_id, industry_name)

    def to_inner_structure(self):
        return {
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "industry_name": to_structure_CustomTextType_50(self.industry_name),
        }

class ChangeIndustryStatus(Request):
    def __init__(self, industry_id, is_active):
        self.industry_id = industry_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["industry_id", "is_active"])
        industry_id = data.get("industry_id")
        industry_id = parse_structure_SignedIntegerType_8(industry_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeIndustryStatus(industry_id, is_active)

    def to_inner_structure(self):
        return {
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "is_active": to_structure_Bool(self.is_active),
        }

class GetStatutoryNatures(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryNatures()

    def to_inner_structure(self):
        return {
        }

class SaveStatutoryNature(Request):
    def __init__(self, statutory_nature_name):
        self.statutory_nature_name = statutory_nature_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_nature_name"])
        statutory_nature_name = data.get("statutory_nature_name")
        statutory_nature_name = parse_structure_CustomTextType_50(statutory_nature_name)
        return SaveStatutoryNature(statutory_nature_name)

    def to_inner_structure(self):
        return {
            "statutory_nature_name": to_structure_CustomTextType_50(self.statutory_nature_name),
        }

class UpdateStatutoryNature(Request):
    def __init__(self, statutory_nature_id, statutory_nature_name):
        self.statutory_nature_id = statutory_nature_id
        self.statutory_nature_name = statutory_nature_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_nature_id", "statutory_nature_name"])
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_id = parse_structure_SignedIntegerType_8(statutory_nature_id)
        statutory_nature_name = data.get("statutory_nature_name")
        statutory_nature_name = parse_structure_CustomTextType_50(statutory_nature_name)
        return UpdateStatutoryNature(statutory_nature_id, statutory_nature_name)

    def to_inner_structure(self):
        return {
            "statutory_nature_id": to_structure_SignedIntegerType_8(self.statutory_nature_id),
            "statutory_nature_name": to_structure_CustomTextType_50(self.statutory_nature_name),
        }

class ChangeStatutoryNatureStatus(Request):
    def __init__(self, statutory_nature_id, is_active):
        self.statutory_nature_id = statutory_nature_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_nature_id", "is_active"])
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_id = parse_structure_SignedIntegerType_8(statutory_nature_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeStatutoryNatureStatus(statutory_nature_id, is_active)

    def to_inner_structure(self):
        return {
            "statutory_nature_id": to_structure_SignedIntegerType_8(self.statutory_nature_id),
            "is_active": to_structure_Bool(self.is_active),
        }

class GetStatutoryLevels(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryLevels()

    def to_inner_structure(self):
        return {
        }

class SaveStatutoryLevel(Request):
    def __init__(self, country_id, domain_id, levels):
        self.country_id = country_id
        self.domain_id = domain_id
        self.levels = levels

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "levels"])
        country_id = data.get("country_id")
        country_id = parse_structure_SignedIntegerType_8(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_SignedIntegerType_8(domain_id)
        levels = data.get("levels")
        levels = parse_structure_VectorType_RecordType_core_Level(levels)
        return SaveStatutoryLevel(country_id, domain_id, levels)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "levels": to_structure_VectorType_RecordType_core_Level(self.levels),
        }

class GetStatutories(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutories()

    def to_inner_structure(self):
        return {
        }

class SaveStatutory(Request):
    def __init__(self, statutory_level_id, statutory_name, parent_ids):
        self.statutory_level_id = statutory_level_id
        self.statutory_name = statutory_name
        self.parent_ids = parent_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_level_id", "statutory_name", "parent_ids"])
        statutory_level_id = data.get("statutory_level_id")
        statutory_level_id = parse_structure_SignedIntegerType_8(statutory_level_id)
        statutory_name = data.get("statutory_name")
        statutory_name = parse_structure_CustomTextType_50(statutory_name)
        parent_ids = data.get("parent_ids")
        parent_ids = parse_structure_VectorType_SignedIntegerType_8(parent_ids)
        return SaveStatutory(statutory_level_id, statutory_name, parent_ids)

    def to_inner_structure(self):
        return {
            "statutory_level_id": to_structure_SignedIntegerType_8(self.statutory_level_id),
            "statutory_name": to_structure_CustomTextType_50(self.statutory_name),
            "parent_ids": to_structure_VectorType_SignedIntegerType_8(self.parent_ids),
        }

class UpdateStatutory(Request):
    def __init__(self, statutory_id, statutory_level_id, statutory_name, parent_ids):
        self.statutory_id = statutory_id
        self.statutory_level_id = statutory_level_id
        self.statutory_name = statutory_name
        self.parent_ids = parent_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_id", "statutory_level_id", "statutory_name", "parent_ids"])
        statutory_id = data.get("statutory_id")
        statutory_id = parse_structure_SignedIntegerType_8(statutory_id)
        statutory_level_id = data.get("statutory_level_id")
        statutory_level_id = parse_structure_SignedIntegerType_8(statutory_level_id)
        statutory_name = data.get("statutory_name")
        statutory_name = parse_structure_CustomTextType_50(statutory_name)
        parent_ids = data.get("parent_ids")
        parent_ids = parse_structure_VectorType_SignedIntegerType_8(parent_ids)
        return UpdateStatutory(statutory_id, statutory_level_id, statutory_name, parent_ids)

    def to_inner_structure(self):
        return {
            "statutory_id": to_structure_SignedIntegerType_8(self.statutory_id),
            "statutory_level_id": to_structure_SignedIntegerType_8(self.statutory_level_id),
            "statutory_name": to_structure_CustomTextType_50(self.statutory_name),
            "parent_ids": to_structure_VectorType_SignedIntegerType_8(self.parent_ids),
        }


def _init_Request_class_map():
    classes = [GetGeographyLevels, SaveGeographyLevel, GetGeographies, SaveGeography, UpdateGeography, ChangeGeographyStatus, GetIndustries, SaveIndustry, UpdateIndustry, ChangeIndustryStatus, GetStatutoryNatures, SaveStatutoryNature, UpdateStatutoryNature, ChangeStatutoryNatureStatus, GetStatutoryLevels, SaveStatutoryLevel, GetStatutories, SaveStatutory, UpdateStatutory]
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

class GetGeographyLevelsSuccess(Response):
    def __init__(self, countries, geography_levels):
        self.countries = countries
        self.geography_levels = geography_levels

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "geography_levels"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        geography_levels = data.get("geography_levels")
        geography_levels = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(geography_levels)
        return GetGeographyLevelsSuccess(countries, geography_levels)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "geography_levels": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(self.geography_levels),
        }

class SaveGeographyLevelSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveGeographyLevelSuccess()

    def to_inner_structure(self):
        return {
        }

class DuplicateGeographyLevelsExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return DuplicateGeographyLevelsExists()

    def to_inner_structure(self):
        return {
        }

class UpdateGeographyLevelSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateGeographyLevelSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidGeographyLevelId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidGeographyLevelId()

    def to_inner_structure(self):
        return {
        }

class GetGeographiesSuccess(Response):
    def __init__(self, countries, geography_levels, geographies):
        self.countries = countries
        self.geography_levels = geography_levels
        self.geographies = geographies

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "geography_levels", "geographies"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        geography_levels = data.get("geography_levels")
        geography_levels = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(geography_levels)
        geographies = data.get("geographies")
        geographies = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(geographies)
        return GetGeographiesSuccess(countries, geography_levels, geographies)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "geography_levels": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(self.geography_levels),
            "geographies": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(self.geographies),
        }

class SaveGeographySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveGeographySuccess()

    def to_inner_structure(self):
        return {
        }

class GeographyNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GeographyNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class InvalidGeographyId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidGeographyId()

    def to_inner_structure(self):
        return {
        }

class ChangeGeographyStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeGeographyStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class GetIndustriesSuccess(Response):
    def __init__(self, industries):
        self.industries = industries

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["industries"])
        industries = data.get("industries")
        industries = parse_structure_VectorType_RecordType_core_Industry(industries)
        return GetIndustriesSuccess(industries)

    def to_inner_structure(self):
        return {
            "industries": to_structure_VectorType_RecordType_core_Industry(self.industries),
        }

class SaveIndustrySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveIndustrySuccess()

    def to_inner_structure(self):
        return {
        }

class IndustryNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return IndustryNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class UpdateIndustrySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateIndustrySuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidIndustryId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidIndustryId()

    def to_inner_structure(self):
        return {
        }

class ChangeIndustryStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeIndustryStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class GetStatutoryNaturesSuccess(Response):
    def __init__(self, statutory_natures):
        self.statutory_natures = statutory_natures

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_natures"])
        statutory_natures = data.get("statutory_natures")
        statutory_natures = parse_structure_VectorType_RecordType_core_StatutoryNature(statutory_natures)
        return GetStatutoryNaturesSuccess(statutory_natures)

    def to_inner_structure(self):
        return {
            "statutory_natures": to_structure_VectorType_RecordType_core_StatutoryNature(self.statutory_natures),
        }

class SaveStatutoryNatureSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveStatutoryNatureSuccess()

    def to_inner_structure(self):
        return {
        }

class StatutoryNatureNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return StatutoryNatureNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class UpdateStatutoryNatureSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateStatutoryNatureSuccess()

    def to_inner_structure(self):
        return {
        }

class ChangeStatutoryNatureStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeStatutoryNatureStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidStatutoryNatureId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidStatutoryNatureId()

    def to_inner_structure(self):
        return {
        }

class GetStatutoryLevelsSuccess(Response):
    def __init__(self, countries, domains, statutory_levels):
        self.countries = countries
        self.domains = domains
        self.statutory_levels = statutory_levels

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "statutory_levels"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        statutory_levels = data.get("statutory_levels")
        statutory_levels = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(statutory_levels)
        return GetStatutoryLevelsSuccess(countries, domains, statutory_levels)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "statutory_levels": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(self.statutory_levels),
        }

class SaveStatutoryLevelSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveStatutoryLevelSuccess()

    def to_inner_structure(self):
        return {
        }

class DuplicateStatutoryLevelsExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return DuplicateStatutoryLevelsExists()

    def to_inner_structure(self):
        return {
        }

class GetStatutoriesSuccess(Response):
    def __init__(self, countries, domains, statutory_levels, statutories):
        self.countries = countries
        self.domains = domains
        self.statutory_levels = statutory_levels
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "statutory_levels", "statutories"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        statutory_levels = data.get("statutory_levels")
        statutory_levels = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(statutory_levels)
        statutories = data.get("statutories")
        statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(statutories)
        return GetStatutoriesSuccess(countries, domains, statutory_levels, statutories)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "statutory_levels": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(self.statutory_levels),
            "statutories": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(self.statutories),
        }

class SaveStatutorySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveStatutorySuccess()

    def to_inner_structure(self):
        return {
        }

class StatutoryNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return StatutoryNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class InvalidStatutoryId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidStatutoryId()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [GetGeographyLevelsSuccess, SaveGeographyLevelSuccess, DuplicateGeographyLevelsExists, UpdateGeographyLevelSuccess, InvalidGeographyLevelId, GetGeographiesSuccess, SaveGeographySuccess, GeographyNameAlreadyExists, InvalidGeographyId, ChangeGeographyStatusSuccess, GetIndustriesSuccess, SaveIndustrySuccess, IndustryNameAlreadyExists, UpdateIndustrySuccess, InvalidIndustryId, ChangeIndustryStatusSuccess, GetStatutoryNaturesSuccess, SaveStatutoryNatureSuccess, StatutoryNatureNameAlreadyExists, UpdateStatutoryNatureSuccess, ChangeStatutoryNatureStatusSuccess, InvalidStatutoryNatureId, GetStatutoryLevelsSuccess, SaveStatutoryLevelSuccess, DuplicateStatutoryLevelsExists, GetStatutoriesSuccess, SaveStatutorySuccess, StatutoryNameAlreadyExists, InvalidStatutoryId]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

