from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, to_structure_dictionary_values,
)
from protocol.parse_structure import (
    parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_VariantType_knowledgemaster_Request
)
from protocol.to_structure import (
    to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    to_structure_VariantType_knowledgemaster_Request
)


#
# Request
#
class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        if type(inner) is dict:
            to_structure_dictionary_values(inner)
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

class Level(object):
    def __init__(self, level_id, level_position, level_name, is_remove):
        self.level_id = level_id
        self.level_position = level_position
        self.level_name = level_name
        self.is_remove = is_remove

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["l_id", "l_position", "l_name", "is_remove"])
        level_id = data.get("l_id")
        level_position = data.get("l_position")
        level_name = data.get("l_name")
        is_remove = data.get("is_remove")
        return Level(level_id, level_position, level_name, is_remove)

    def to_structure(self):
        return {
            "l_id": self.level_id,
            "l_position": self.level_position,
            "l_name": self.level_name,
            "is_remove": self.is_remove
        }

class SaveGeographyLevel(Request):
    def __init__(self, country_id, levels):
        self.country_id = country_id
        self.levels = levels

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "levels"])
        country_id = data.get("c_id")
        levels = data.get("levels")
        return SaveGeographyLevel(country_id, levels)

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "levels": self.levels,
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
    def __init__(self, geography_level_id, geography_name, parent_ids, parent_names, country_id):
        self.geography_level_id = geography_level_id
        self.geography_name = geography_name
        self.parent_ids = parent_ids
        self.parent_names = parent_names
        self.country_id = country_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["g_l_id", "g_name", "p_ids", "p_names", "c_id"])
        geography_level_id = data.get("g_l_id")
        geography_name = data.get("g_name")
        parent_ids = data.get("p_ids")
        parent_names = data.get("p_names")
        country_id = data.get("c_id")
        return SaveGeography(geography_level_id, geography_name, parent_ids, parent_names, country_id)

    def to_inner_structure(self):
        return {
            "g_l_id": self.geography_level_id,
            "g_name": self.geography_name,
            "p_ids": self.parent_ids,
            "p_names": self.parent_names,
            "c_id": self.country_id
        }

class UpdateGeography(Request):
    def __init__(self, geography_id, geography_level_id, geography_name, parent_ids, parent_names, country_id):
        self.geography_id = geography_id
        self.geography_level_id = geography_level_id
        self.geography_name = geography_name
        self.parent_ids = parent_ids
        self.parent_names = parent_names
        self.country_id = country_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["g_id", "g_l_id", "g_name", "p_ids", "p_names", "c_id"])
        geography_id = data.get("g_id")
        geography_level_id = data.get("g_l_id")
        geography_name = data.get("g_name")
        parent_ids = data.get("p_ids")
        parent_names = data.get("p_names")
        country_id = data.get("c_id")
        return UpdateGeography(geography_id, geography_level_id, geography_name, parent_ids, parent_names, country_id)

    def to_inner_structure(self):
        return {
            "g_id": self.geography_id,
            "g_l_id": self.geography_level_id,
            "g_name": self.geography_name,
            "p_ids": self.parent_ids,
            "p_names": self.parent_names,
            "c_id": self.country_id
        }

class ChangeGeographyStatus(Request):
    def __init__(self, geography_id, is_active):
        self.geography_id = geography_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["g_id", "is_active"])
        geography_id = data.get("g_id")
        is_active = data.get("is_active")
        return ChangeGeographyStatus(geography_id, is_active)

    def to_inner_structure(self):
        return {
            "g_id": self.geography_id,
            "is_active": self.is_active,
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
    def __init__(self, country_id, domain_id, industry_name):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_name = industry_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "d_id", "i_name"])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_name = data.get("i_name")
        return SaveIndustry(country_id, domain_id, industry_name)

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "i_name": self.industry_name,
        }


class UpdateIndustry(Request):
    def __init__(self, country_id, domain_id, industry_id, industry_name):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_id = industry_id
        self.industry_name = industry_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "d_id", "i_id", "i_name"])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_id = data.get("i_id")
        industry_name = data.get("i_name")
        return UpdateIndustry(country_id, domain_id, industry_id, industry_name)

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "i_id": self.industry_id,
            "i_name": self.industry_name,
        }


class ChangeIndustryStatus(Request):
    def __init__(self, industry_id, is_active):
        self.industry_id = industry_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["i_id", "is_active"])
        industry_id = data.get("i_id")
        is_active = data.get("is_active")
        return ChangeIndustryStatus(industry_id, is_active)

    def to_inner_structure(self):
        return {
            "i_id": self.industry_id,
            "is_active": self.is_active,
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
    def __init__(self, statutory_nature_name, country_id):
        self.statutory_nature_name = statutory_nature_name
        self.country_id = country_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["s_n_name", "c_id"])
        statutory_nature_name = data.get("s_n_name")
        country_id = data.get("c_id")
        return SaveStatutoryNature(statutory_nature_name, country_id)

    def to_inner_structure(self):
        return {
            "s_n_name": self.statutory_nature_name,
            "c_id": self.country_id,
        }

class UpdateStatutoryNature(Request):
    def __init__(self, statutory_nature_id, statutory_nature_name, country_id):
        self.statutory_nature_id = statutory_nature_id
        self.statutory_nature_name = statutory_nature_name
        self.country_id = country_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["s_n_id", "s_n_name", "c_ids"])
        statutory_nature_id = data.get("s_n_id")
        statutory_nature_name = data.get("s_n_name")
        country_id = data.get("c_id")
        return UpdateStatutoryNature(statutory_nature_id, statutory_nature_name, country_id)

    def to_inner_structure(self):
        return {
            "s_n_id": self.statutory_nature_id,
            "s_n_name": self.statutory_nature_name,
            "c_id": self.country_id,
        }

class ChangeStatutoryNatureStatus(Request):
    def __init__(self, statutory_nature_id, is_active):
        self.statutory_nature_id = statutory_nature_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["s_n_id", "is_active"])
        statutory_nature_id = data.get("s_n_id")
        is_active = data.get("is_active")
        return ChangeStatutoryNatureStatus(statutory_nature_id, is_active)

    def to_inner_structure(self):
        return {
            "s_n_id": self.statutory_nature_id,
            "is_active": self.is_active,
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
        data = parse_dictionary(data, ["c_id", "d_id", "levels"])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        levels = data.get("levels")
        return SaveStatutoryLevel(country_id, domain_id, levels)

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "levels": self.levels,
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
    def __init__(self, domain_id, statutory_level_id, statutory_name, parent_ids, parent_names):
        self.domain_id = domain_id
        self.statutory_level_id = statutory_level_id
        self.statutory_name = statutory_name
        self.parent_ids = parent_ids
        self.parent_names = parent_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["d_id", "s_l_id", "s_name", "p_ids", "p_names"])
        domain_id = data.get("d_id")
        statutory_level_id = data.get("s_l_id")
        statutory_name = data.get("s_name")
        parent_ids = data.get("p_ids")
        parent_names = data.get("p_names")
        return SaveStatutory(domain_id, statutory_level_id, statutory_name, parent_ids, parent_names)

    def to_inner_structure(self):
        return {
            "d_id": self.domain_id,
            "s_l_id": self.statutory_level_id,
            "s_name": self.statutory_name,
            "p_ids": self.parent_ids,
            "p_names": self.parent_names
        }

class UpdateStatutory(Request):
    def __init__(self, statutory_id, statutory_level_id, statutory_name, parent_ids, parent_names):
        self.statutory_id = statutory_id
        self.statutory_level_id = statutory_level_id
        self.statutory_name = statutory_name
        self.parent_ids = parent_ids
        self.parent_names = parent_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["s_id", "s_l_id", "s_name", "p_ids", "p_names"])
        statutory_id = data.get("s_id")
        statutory_level_id = data.get("s_l_id")
        statutory_name = data.get("s_name")
        parent_ids = data.get("p_ids")
        parent_names = data.get("p_names")
        return UpdateStatutory(statutory_id, statutory_level_id, statutory_name, parent_ids, parent_names)

    def to_inner_structure(self):
        return {
            "s_id": self.statutory_id,
            "s_l_id": self.statutory_level_id,
            "s_name": self.statutory_name,
            "p_ids": self.parent_ids,
            "p_names": self.parent_names
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
        if type(inner) is dict:
            to_structure_dictionary_values(inner)
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
        geography_levels = data.get("geography_levels")
        return GetGeographyLevelsSuccess(countries, geography_levels)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "geography_levels": self.geography_levels,
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

class LevelShouldNotbeEmpty(Response):
    def __init__(self, level):
        self.level = level

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["level"])
        level = data.get("level")
        return LevelShouldNotbeEmpty(level)

    def to_inner_structure(self):
        return {
            "level": self.level
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
        geography_levels = data.get("geography_levels")
        geographies = data.get("geographies")
        return GetGeographiesSuccess(countries, geography_levels, geographies)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "geography_levels": self.geography_levels,
            "geographies": self.geographies,
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

class UpdateGeographySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateGeographySuccess()

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
    def __init__(self, industries, countries, domains):
        self.industries = industries
        self.countries = countries
        self.domains = domains

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["industries", "countries", "domains"])
        industries = data.get("industries")
        countries = data.get("countries")
        domains = data.get("domains")
        return GetIndustriesSuccess(industries, countries, domains)

    def to_inner_structure(self):
        return {
            "industries": self.industries,
            "countries": self.countries,
            "domains": self.domains
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
    def __init__(self, statutory_natures, countries):
        self.statutory_natures = statutory_natures
        self.countries = countries

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_natures", "countries"])
        statutory_natures = data.get("statutory_natures")
        countries = data.get("countries")
        return GetStatutoryNaturesSuccess(statutory_natures, countries)

    def to_inner_structure(self):
        return {
            "statutory_natures": self.statutory_natures,
            "countries": self.countries,
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
        domains = data.get("domains")
        statutory_levels = data.get("statutory_levels")
        return GetStatutoryLevelsSuccess(countries, domains, statutory_levels)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "statutory_levels": self.statutory_levels,
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

class LevelIdCannotBeNull(Response):
    def __init__(self, level_name):
        self.level_name = level_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["level_name"])
        level_name = data.get("level_name")
        return LevelIdCannotBeNull(level_name)

    def to_inner_structure(self):
        return {
            "level_name": self.level_name
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
        domains = data.get("domains")
        statutory_levels = data.get("statutory_levels")
        statutories = data.get("statutories")
        statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(statutories)
        return GetStatutoriesSuccess(countries, domains, statutory_levels, statutories)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "statutory_levels": self.statutory_levels,
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
    classes = [GetGeographyLevelsSuccess, SaveGeographyLevelSuccess, DuplicateGeographyLevelsExists, LevelShouldNotbeEmpty, UpdateGeographyLevelSuccess, InvalidGeographyLevelId, GetGeographiesSuccess, SaveGeographySuccess, GeographyNameAlreadyExists, InvalidGeographyId, ChangeGeographyStatusSuccess, GetIndustriesSuccess, SaveIndustrySuccess, IndustryNameAlreadyExists, UpdateIndustrySuccess, InvalidIndustryId, ChangeIndustryStatusSuccess, GetStatutoryNaturesSuccess, SaveStatutoryNatureSuccess, StatutoryNatureNameAlreadyExists, UpdateStatutoryNatureSuccess, ChangeStatutoryNatureStatusSuccess, InvalidStatutoryNatureId, GetStatutoryLevelsSuccess, SaveStatutoryLevelSuccess, DuplicateStatutoryLevelsExists, GetStatutoriesSuccess, SaveStatutorySuccess, StatutoryNameAlreadyExists, InvalidStatutoryId]
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
        request = parse_structure_VariantType_knowledgemaster_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_structure_VariantType_knowledgemaster_Request(self.request),
        }
