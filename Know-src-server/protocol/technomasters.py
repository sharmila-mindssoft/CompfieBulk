from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    to_structure_dictionary_values, parse_VariantType, to_VariantType
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


class GetClientGroups(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientGroups()

    def to_inner_structure(self):
        return {
        }


class GetClientGroupFormData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientGroupFormData()

    def to_inner_structure(self):
        return {
        }


class GetEditClientGroupFormData(Request):
    def __init__(self, group_id):
        self.group_id = group_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["group_id"])
        group_id = data.get("group_id")
        return GetEditClientGroupFormData(group_id)

    def to_inner_structure(self):
        return {
            "group_id": self.group_id
        }


class SaveClientGroup(Request):
    def __init__(
        self, group_name, email_id, short_name, no_of_view_licence,
        legal_entity_details, date_configurations
    ):
        self.group_name = group_name
        self.email_id = email_id
        self.short_name = short_name
        self.no_of_view_licence = no_of_view_licence
        self.legal_entity_details = legal_entity_details
        self.date_configurations = date_configurations

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "group_name", "email_id", "short_name", "no_of_view_licence",
            "legal_entity_details", "date_configurations"
        ])
        group_name = data.get("group_name")
        email_id = data.get("email_id")
        short_name = data.get("short_name")
        no_of_view_licence = data.get("no_of_view_licence")
        legal_entity_details = data.get("legal_entity_details")
        date_configurations = data.get("date_configurations")
        return SaveClientGroup(
            group_name, email_id, short_name, no_of_view_licence,
            legal_entity_details, date_configurations
        )

    def to_inner_structure(self):
        return {
            "group_name": self.group_name,
            "email_id": self.email_id,
            "short_name": self.short_name,
            "no_of_view_licence": self.no_of_view_licence,
            "legal_entity_details": self.legal_entities,
            "date_configurations": self.date_configurations
        }


class UpdateClientGroup(Request):
    def __init__(
        self, client_id, group_name, email_id, short_name, no_of_view_licence,
        legal_entities, date_configurations, remarks
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.email_id = email_id
        self.short_name = short_name
        self.no_of_view_licence = no_of_view_licence
        self.legal_entities = legal_entities
        self.date_configurations = date_configurations
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
               "client_id", "group_name", "email_id", "short_name",
               "no_of_view_licence", "legal_entities",
               "date_configurations", "remarks"
            ]
        )
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        email_id = data.get("email_id")
        short_name = data.get("short_name")
        no_of_view_licence = data.get("no_of_view_licence")
        legal_entities = data.get("legal_entities")
        date_configurations = data.get("date_configurations")
        remarks = data.get("remarks")
        return UpdateClientGroup(
            client_id, group_name, email_id, short_name, no_of_view_licence,
            legal_entities, date_configurations, remarks
        )

    def to_inner_structure(self):
        return {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "email_id": self.email_id,
            "short_name": self.short_name,
            "no_of_view_licence": self.no_of_view_licence,
            "legal_entities": self.legal_entities,
            "date_configurations": self.date_configurations,
            "remarks": self.remarks
        }


class GetClients(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClients()

    def to_inner_structure(self):
        return {
        }


class GetClientsEdit(Request):
    def __init__(self, client_id, business_group_id, legal_entity_id, country_id, from_count, page_count):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "bg_id", "le_id", "c_id", "from_count", "page_count"])
        client_id = data.get("client_id")
        business_group_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        country_id = data.get("c_id")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetClientsEdit(client_id, business_group_id, legal_entity_id, country_id, from_count, page_count)

    def to_inner_structure(self):
        data = {
            "client_id": self.client_id,
            "bg_id": self.business_group_id,
            "le_id": self.legal_entity_id,
            "c_id": self.country_id,
            "from_count": self.from_count,
            "page_count": self.page_count
        }
        return data


class LEGAL_ENTITY(Request):
    def __init__(self, legal_entity_id, legal_entity_name):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "le_name"])
        legal_entity_id = data.get("le_id")
        legal_entity_name = data.get("le_name")
        return LEGAL_ENTITY(legal_entity_id, legal_entity_name)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "le_name": self.legal_entity_name,
        }

class UnitDivision(object):
    def __init__(self, division_id, division_name, category_name, division_cnt, unit_cnt):
        self.division_id = division_id
        self.division_name = division_name
        self.category_name = category_name
        self.division_cnt = division_cnt
        self.unit_cnt = unit_cnt

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["dv_id", "dv_name", "cg", "div_cnt", "unit_cnt"])
        division_id = data.get("dv_id")
        division_name = data.get("dv_name")
        category_name = data.get("cg")
        division_cnt = data.get("div_cnt")
        unit_cnt = data.get("unit_cnt")

        return UnitDivision(division_id, division_name, category_name, division_cnt, unit_cnt)

    def to_structure(self):
        data = {
            "dv_id": self.division_id,
            "dv_name": self.division_name,
            "cg": self.category_name,
            "div_cnt": self.division_cnt,
            "unit_cnt": self.unit_cnt,
        }
        return data

class DivisionCategory(object):
    def __init__(self, client_id, business_group_id, legal_entity_id, division_id, division_name, cg):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.division_name = division_name
        self.cg = cg

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "cl_id", "bg_id", "le_id", "dv_id", "dv_name", "cg"
            ]
        )
        client_id = data.get("cl_id")
        business_group_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        division_id = data.get("dv_id")
        division_name = data.get("dv_name")
        cg = data.get("cg")
        return DivisionCategory(
            client_id, business_group_id, legal_entity_id, division_id, division_name, cg
        )

    def to_structure(self):
        data = {
            "cl_id": self.client_id,
            "bg_id": self.business_group_id,
            "le_id": self.legal_entity_id,
            "dv_id": self.division_id,
            "dv_name": self.division_name,
            "cg": self.cg,
        }
        return data


class UNIT(object):
    def __init__(
        self, unit_id, geography_id, unit_code, unit_name, unit_address,
        postal_code, domain_ids, industry_ids, is_approved
    ):
        self.unit_id = unit_id
        self.geography_id = geography_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.postal_code = postal_code
        self.domain_ids = domain_ids
        self.industry_ids = industry_ids
        self.is_approved = is_approved

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "unit_id", "geography_id", "unit_code", "unit_name",
                "address", "postal_code",  "d_ids",
                "i_ids_list", "is_approved"
            ]
        )
        unit_id = data.get("unit_id")
        geography_id = data.get("geography_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        unit_address = data.get("address")
        postal_code = data.get("postal_code")
        domain_ids = data.get("d_ids")
        industry_ids = data.get("i_ids_list")
        is_approved = data.get("is_approved")
        return UNIT(
            unit_id, geography_id, unit_code, unit_name, unit_address,
            postal_code, domain_ids, industry_ids, is_approved
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "geography_id": self.geography_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "address": self.unit_address,
            "postal_code": self.postal_code,
            "d_ids": self.domain_ids,
            "i_ids_list": self.industry_ids,
            "is_approved": self.is_approved
        }

class SaveClient(Request):
    def __init__(self, client_id, business_group_id, legal_entity_id, country_id, division_units, units, division_category):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.division_units = division_units
        self.units = units
        self.division_category = division_category

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "cl_id", "bg_id", "le_id", "c_id", "division_units", "units", "division_category"
            ]
        )
        client_id = data.get("cl_id")
        business_group_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        country_id = data.get("c_id")
        division_units = data.get("division_units")
        units = data.get("units")
        division_category = data.get("division_category")
        return SaveClient(
            client_id, business_group_id, legal_entity_id, country_id, division_units, units, division_category
        )

    def to_inner_structure(self):
        data = {
            "cl_id": self.client_id,
            "bg_id": self.business_group_id,
            "le_id": self.legal_entity_id,
            "c_id": self.country_id,
            "division_units": self.division_units,
            "units": self.units,
            "division_category": self.division_category
        }
        return data

class SaveDivisionCategory(Request):
    def __init__(self, division_category):
        self.division_category = division_category

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "division_category"
            ]
        )
        division_category = data.get("division_category")

        return SaveDivisionCategory(
            division_category
        )

    def to_inner_structure(self):
        data = {
            "division_category": self.division_category,
        }
        return data

class UpdateClient(Request):
    def __init__(self, client_id, business_group, legal_entity_id, division, country_wise_units):
        self.client_id = client_id
        self.business_group = business_group
        self.legal_entity_id = legal_entity_id
        self.division = division
        self.country_wise_units = country_wise_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "c_id", "bg", "le", "d", "cw_units"
            ]
        )
        client_id = data.get("c_id")
        business_group = data.get("bg")
        legal_entity = data.get("le")
        division = data.get("d")
        country_wise_units = data.get("cw_units")
        return UpdateClient(client_id, business_group, legal_entity, division, country_wise_units)

    def to_inner_structure(self):
        return {
            "client_id": self.client_id,
            "business_group": self.business_group,
            "legal_entity": self.legal_entity,
            "division": self.division,
            "country_wise_units": self.country_wise_units
        }


class GetClientProfile(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientProfile()

    def to_inner_structure(self):
        return {
        }

class GetNextUnitCode(Request):
    def __init__(self, client_id):
        self.client_id = client_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id"])
        client_id = data["client_id"]
        return GetNextUnitCode(client_id)

    def to_inner_structure(self):
        return {
            "client_id" : self.client_id
        }


class GetAssignLegalEntityList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssignLegalEntityList()

    def to_inner_structure(self):
        return {
        }


class GetUnassignedUnits(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUnassignedUnits()

    def to_inner_structure(self):
        return {
        }


class GetAssignedUnits(Request):
    def __init__(self, client_id, domain_id, legal_entity_id):
        self.client_id = client_id
        self.domain_id = domain_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "domain_id", "legal_entity_id"])
        client_id = data.get("client_id")
        domain_id = data.get("domain_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetAssignedUnits(client_id, domain_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "client_id": self.client_id,
            "domain_id": self.domain_id,
            "legal_entity_id": self.legal_entity_id
        }


class GetAssignedUnitDetails(Request):
    def __init__(self, legal_entity_id, user_id, client_id, domain_id):
        self.legal_entity_id = legal_entity_id
        self.user_id = user_id
        self.client_id = client_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entity_id", "user_id", "client_id", "domain_id"])
        legal_entity_id = data.get("legal_entity_id")
        user_id = data.get("user_id")
        client_id = data.get("client_id")
        domain_id = data.get("domain_id")
        return GetAssignedUnitDetails(legal_entity_id, user_id, client_id, domain_id)

    def to_inner_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "user_id": self.user_id,
            "client_id": self.client_id,
            "domain_id": self.domain_id
        }


class GetAssignUnitFormData(Request):
    def __init__(self, client_id, domain_id, legal_entity_id):
        self.client_id = client_id
        self.domain_id = domain_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "domain_id", "legal_entity_id"])
        client_id = data.get("client_id")
        domain_id = data.get("domain_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetAssignUnitFormData(client_id, domain_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "client_id": self.client_id,
            "domain_id": self.domain_id,
            "legal_entity_id": self.legal_entity_id
        }


class GetEditAssignLegalEntity(Request):
    def __init__(self, group_id):
        self.group_id = group_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["group_id"])
        group_id = data.get("group_id")
        return GetEditAssignLegalEntity(group_id)

    def to_inner_structure(self):
        return {
            "group_id": self.group_id
        }

class SaveAssignLegalEntity(Request):
    def __init__(
        self, client_id, legal_entity_ids, user_ids
    ):
        self.client_id = client_id
        self.legal_entity_ids = legal_entity_ids
        self.user_ids = user_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "client_id", "legal_entity_ids", "user_ids"
        ])
        client_id = data.get("client_id")
        legal_entity_ids = data.get("legal_entity_ids")
        user_ids = data.get("user_ids")
        return SaveAssignLegalEntity(
            client_id, legal_entity_ids, user_ids
        )

    def to_inner_structure(self):
        return {
            "client_id": self.client_id,
            "legal_entity_ids": self.legal_entity_ids,
            "user_ids": self.user_ids
        }


class ActiveUnit(object):
    def __init__(self, unit_id, domain_name, legal_entity_id):
        self.unit_id = unit_id
        self.domain_name = domain_name
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["unit_id", "domain_name", "legal_entity_id"])
        unit_id = data.get("unit_id")
        domain_name = data.get("domain_name")
        legal_entity_id = data.get("legal_entity_id")
        return ActiveUnit(unit_id, domain_name, legal_entity_id)

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "domain_name": self.domain_name,
            "legal_entity_id": self.legal_entity_id
        }


class SaveAsssignedUnits(Request):
    def __init__(self, client_id, user_id, active_units):
        self.client_id = client_id
        self.user_id = user_id
        self.active_units = active_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "user_id", "active_units"])
        client_id = data.get("client_id")
        user_id = data.get("user_id")
        active_units = data.get("active_units")
        return SaveAsssignedUnits(client_id, user_id, active_units)

    def to_inner_structure(self):
        return {
            "client_id": self.client_id,
            "user_id": self.user_id,
            "active_units": self.active_units
        }


class ViewAssignLegalEntity(Request):
    def __init__(self, client_id):
        self.client_id = client_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id"])
        client_id = data.get("client_id")
        return ViewAssignLegalEntity(client_id)

    def to_inner_structure(self):
        return {
            "client_id": self.client_id
        }

class CheckAssignedDomainUnits(Request):
    def __init__(self, unit_id, d_id):
        self.unit_id = unit_id
        self.d_id = d_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_id", "d_id"])
        unit_id = data.get("unit_id")
        d_id = data.get("d_id")
        return CheckAssignedDomainUnits(unit_id, d_id)

    def to_inner_structure(self):
        return {
            "unit_id": self.unit_id,
            "d_id": self.d_id
        }


def _init_Request_class_map():
    classes = [
        GetClientGroups, SaveClientGroup, UpdateClientGroup,
        GetClients, GetClientsEdit, SaveClient, UpdateClient,
        GetClientProfile,
        GetNextUnitCode, GetClientGroupFormData, GetEditClientGroupFormData,
        GetAssignLegalEntityList, GetUnassignedUnits, GetAssignedUnits,
        GetAssignedUnitDetails, GetAssignUnitFormData, SaveAsssignedUnits,
        GetEditAssignLegalEntity, SaveAssignLegalEntity, ViewAssignLegalEntity,
        SaveDivisionCategory, CheckAssignedDomainUnits
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


class GetClientGroupsSuccess(Response):
    def __init__(self, groups):
        self.groups = groups

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["groups"])
        groups = data.get("groups")
        return GetClientGroupsSuccess(groups)

    def to_inner_structure(self):
        return {
            "groups": self.groups
        }


class SaveClientGroupSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveClientGroupSuccess()

    def to_inner_structure(self):
        return {
        }


class GroupNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GroupNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class GroupShortNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GroupShortNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class UpdateClientGroupSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateClientGroupSuccess()

    def to_inner_structure(self):
        return {
        }


class ChangeClientGroupStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeClientGroupStatusSuccess()

    def to_inner_structure(self):
        return {
        }


class InvalidClientId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidClientId()

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


class InvalidBusinessGroupId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidBusinessGroupId()

    def to_inner_structure(self):
        return {
        }


class InvalidLegalEntityId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidLegalEntityId()

    def to_inner_structure(self):
        return {
        }


class InvalidDivisionId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidDivisionId()

    def to_inner_structure(self):
        return {
        }

class InvalidDivisionName(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidDivisionName()

    def to_inner_structure(self):
        return {
        }

class InvalidCategoryName(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidCategoryName()

    def to_inner_structure(self):
        return {
        }

class InvalidUnitId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUnitId()

    def to_inner_structure(self):
        return {
        }

class GetAssignLegalEntityListSuccess(Response):
    def __init__(self, assign_le_list):
        self.assign_le_list = assign_le_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assign_le_list"])
        assign_le_list = data.get("assign_le_list")
        return GetAssignLegalEntityListSuccess(assign_le_list)

    def to_inner_structure(self):
        return {
            "assign_le_list": self.assign_le_list
        }

class GetEditAssignLegalEntitySuccess(Response):
    def __init__(
        self,
        unassign_legal_entities,
        techno_users
    ):

        self.unassign_legal_entities = unassign_legal_entities
        self.techno_users = techno_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "unassign_legal_entities", "mapped_techno_users"
        ])

        unassign_legal_entities = data.get("unnssign_legal_entities")
        techno_users = data.get("mapped_techno_users")

        return GetEditAssignLegalEntitySuccess(
            unassign_legal_entities, techno_users
        )

    def to_inner_structure(self):

        return {
            "unassign_legal_entities": self.unassign_legal_entities,
            "mapped_techno_users": self.techno_users
        }

class SaveAssignLegalEntitySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveAssignLegalEntitySuccess()

    def to_inner_structure(self):
        return {
        }

class ViewAssignLegalEntitySuccess(Response):
    def __init__(
        self,
        assigned_legal_entities
    ):

        self.assigned_legal_entities = assigned_legal_entities

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "view_assigned_legal_entities"
        ])

        assigned_legal_entities = data.get("view_assigned_legal_entities")

        return ViewAssignLegalEntitySuccess(
            assigned_legal_entities
        )

    def to_inner_structure(self):

        return {
            "view_assigned_legal_entities": self.assigned_legal_entities
        }

class GetClientGroupFormDataSuccess(Response):
    def __init__(
        self, countries, domains, industries
    ):
        self.countries = countries
        self.domains = domains
        self.industries = industries

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "domains", "industries"
        ])
        countries = data.get("countries")
        domains = data.get("domains")
        industries = data.get("industries")
        return GetClientGroupFormDataSuccess(
            countries, domains, industries
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "industries": self.industries
        }


class GetEditClientGroupFormDataSuccess(Response):
    def __init__(
        self, countries,  business_groups_country, domains, industries,
        group_name, email_id, short_name, no_of_licence,
        legal_entities, date_configurations
    ):
        self.countries = countries
        self.business_groups_country = business_groups_country
        self.domains = domains
        self.industries = industries
        self.group_name = group_name
        self.email_id = email_id
        self.short_name = short_name
        self.no_of_licence = no_of_licence
        self.legal_entities = legal_entities
        self.date_configurations = date_configurations

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "business_groups_country", "domains", "industries",
            "client_details", "group_name", "email_id", "legal_entities_list",
            "date_configurations", "short_name", "no_of_licence"
        ])
        countries = data.get("countries")
        business_groups_country = data.get("business_groups_country")
        domains = data.get("domains")
        industries = data.get("industries")
        group_name = data.get("group_name")
        short_name = data.get("short_name")
        email_id = data.get("email_id")
        legal_entities = data.get("legal_entities_list")
        date_configurations = data.get("date_configurations")
        no_of_licence = data.get("no_of_licence")
        return GetEditClientGroupFormDataSuccess(
            countries,  business_groups_country, domains, industries,
            group_name, email_id, short_name, no_of_licence,
            legal_entities, date_configurations
        )

    def to_inner_structure(self):
        # print "self.business_groups_country: %s" % self.business_groups_country
        return {
            "countries": self.countries,
            "business_groups_country": self.business_groups_country,
            "domains": self.domains,
            "industries": self.industries,
            "group_name": self.group_name,
            "short_name": self.short_name,
            "email_id": self.email_id,
            "no_of_licence": self.no_of_licence,
            "legal_entities_list": self.legal_entities,
            "date_configurations": self.date_configurations
        }


class GetClientsSuccess(Response):
    def __init__(
        self, client_unit_list, group_company_list, business_group_list, countries_units, unit_legal_entity,
        domains_organization_list, divisions, unit_geography_level_list, unit_geographies_list
    ):
        self.client_unit_list = client_unit_list
        self.group_company_list = group_company_list
        self.business_group_list = business_group_list
        self.countries_units = countries_units
        self.unit_legal_entity = unit_legal_entity
        self.domains_organization_list = domains_organization_list
        self.divisions = divisions
        self.unit_geography_level_list = unit_geography_level_list
        self.unit_geographies_list = unit_geographies_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "client_unit_list", "group_company_list", "business_group_list", "countries_units", "unit_legal_entity",
            "domains_organization_list", "divisions", "unit_geography_level_list", "unit_geographies_list"
        ])
        client_unit_list = data.get("client_unit_list")
        group_company_list = data.get("group_company_list")
        business_group_list = data.get("business_group_list")
        countries_units = data.get("countries_units")
        unit_legal_entity = data.get("unit_legal_entity")
        domains_organization_list = data.get("domains_organization_list")
        divisions = data.get("divisions")
        unit_geography_level_list = data.get("unit_geography_level_list")
        unit_geographies_list = data.get("unit_geographies_list")

        return GetClientsSuccess(
            client_unit_list, group_company_list, business_group_list, countries_units, unit_legal_entity,
            domains_organization_list, divisions, unit_geography_level_list, unit_geographies_list
        )

    def to_inner_structure(self):
        data = {
            "client_unit_list": self.client_unit_list,
            "group_company_list": self.group_company_list,
            "business_group_list": self.business_group_list,
            "countries_units": self.countries_units,
            "unit_legal_entity": self.unit_legal_entity,
            "domains_organization_list": self.domains_organization_list,
            "divisions": self.divisions,
            "unit_geography_level_list": self.unit_geography_level_list,
            "unit_geographies_list": self.unit_geographies_list,
        }
        return data


class GetClientsEditSuccess(Response):
    def __init__(self, unit_list):
        self.unit_list = unit_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_list"])
        unit_list = data.get("unit_list")
        return GetClientsEditSuccess(
            unit_list
        )

    def to_inner_structure(self):
        data = {
            "unit_list": self.unit_list
        }
        return data


class SaveClientSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveClientSuccess()

    def to_inner_structure(self):
        return {
        }

class SaveDivisionCategorySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveDivisionCategorySuccess()

    def to_inner_structure(self):
        return {
        }

class EmailIDAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmailIDAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class CannotDeactivateDomain(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotDeactivateDomain()

    def to_inner_structure(self):
        return {
        }


class CannotDeactivateCountry(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotDeactivateCountry()

    def to_inner_structure(self):
        return {
        }


class ShortNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ShortNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class NotAnImageFile(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return NotAnImageFile()

    def to_inner_structure(self):
        return {
        }


class ServerIsFull(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ServerIsFull()

    def to_inner_structure(self):
        return {
        }


class BusinessGroupNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return BusinessGroupNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class LegalEntityNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return LegalEntityNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class DivisionNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return DivisionNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class CategoryNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CategoryNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class UnitNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UnitNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class UnitCodeAlreadyExists(Response):
    def __init__(self, next_unit_code):
        self.next_unit_code = next_unit_code

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["next_unit_code"])
        next_unit_code = data.get("next_unit_code")
        return UnitCodeAlreadyExists(next_unit_code)

    def to_inner_structure(self):
        return {
            "next_unit_code": self.next_unit_code
        }

class GetNextUnitCodeSuccess(Response):
    def __init__(self, next_unit_code):
        self.next_unit_code = next_unit_code

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["next_unit_code"])
        next_unit_code = data.get("next_unit_code")
        return GetNextUnitCodeSuccess(next_unit_code)

    def to_inner_structure(self):
        return {
            "next_unit_code": self.next_unit_code
        }

class LogoSizeLimitExceeds(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return LogoSizeLimitExceeds()

    def to_inner_structure(self):
        return {
        }

class UpdateClientSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateClientSuccess()

    def to_inner_structure(self):
        return {
        }

class ClientCreationFailed(Response):
    def __init__(self, error):
        self.error = error

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["error"])
        error = data.get("error")
        return ClientCreationFailed(error)

    def to_inner_structure(self):
        return {
            "error": self.error
        }

class CreateNewAdminSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CreateNewAdminSuccess()

    def to_inner_structure(self):
        return {
        }

class ClientDatabaseNotExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ClientDatabaseNotExists()

    def to_inner_structure(self):
        return {
        }

class ChangeClientStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeClientStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class UserIsNotResponsibleForAnyClient(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UserIsNotResponsibleForAnyClient()

    def to_inner_structure(self):
        return {
        }

class CannotDeactivateClient(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotDeactivateClient()

    def to_inner_structure(self):
        return {
        }


class UnassignedUnit(object):
    def __init__(
        self, domain_name, domain_id, group_name, legal_entity_name,
        business_group_name, client_id, unassigned_units, legal_entity_id
    ):
        self.domain_name = domain_name
        self.domain_id = domain_id
        self.group_name = group_name
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.client_id = client_id
        self.unassigned_units = unassigned_units
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "domain_name", "domain_id", "group_name", "legal_entity_name",
                "business_group_name", "client_id", "unassigned_units", "legal_entity_id"
            ]
        )
        domain_name = data.get("domain_name")
        domain_id = data.get("domain_id")
        group_name = data.get("group_name")
        legal_entity_name = data.get("legal_entity_name")
        business_group_name = data.get("business_group_name")
        client_id = data.get("client_id")
        unassigned_units = data.get("unassigned_units")
        legal_entity_id = data.get("legal_entity_id")
        return UnassignedUnit(
            domain_name, domain_id, group_name, legal_entity_name,
            business_group_name, client_id, unassigned_units, legal_entity_id
        )

    def to_structure(self):
        return {
            "domain_name": self.domain_name,
            "domain_id": self.domain_id,
            "group_name": self.group_name,
            "legal_entity_name": self.legal_entity_name,
            "business_group_name": self.business_group_name,
            "client_id": self.client_id,
            "unassigned_units": self.unassigned_units,
            "legal_entity_id": self.legal_entity_id
        }


class AssignedUnit(object):
    def __init__(
        self, user_id, employee_name, business_group_name,
        legal_entity_id, legal_entity_name, unit_count, user_category_id, client_id, domain_id
    ):
        self.user_id = user_id
        self.employee_name = employee_name
        self.business_group_name = business_group_name
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.unit_count = unit_count
        self.user_category_id = user_category_id
        self.client_id = client_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "employee_name", "business_group_name",
                "legal_entity_id", "legal_entity_name", "unit_count",
                "user_category_id", "client_id", "domain_id"
            ]
        )
        user_id = data.get("user_id")
        employee_name = data.get("employee_name")
        business_group_name = data.get("business_group_name")
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        unit_count = data.get("unit_count")
        user_category_id = data.get("user_category_id")
        client_id = data.get("client_id")
        domain_id = data.get("domain_id")
        return AssignedUnit(
            user_id, employee_name, business_group_name,
            legal_entity_id, legal_entity_name, unit_count,
            user_category_id, client_id, domain_id
        )

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "employee_name": self.employee_name,
            "business_group_name": self.business_group_name,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "unit_count": self.unit_count,
            "user_category_id": self.user_category_id,
            "client_id": self.client_id,
            "domain_id": self.domain_id
        }


class AssignedUnitDetails(object):
    def __init__(
        self, unit_id, legal_entity_name, division_name, category_name,
        unit_code, unit_name, address, domain_names, org_names_list,
        geography_name
    ):
        self.unit_id = unit_id
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.category_name = category_name
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.domain_names = domain_names
        self.org_names_list = org_names_list
        self.geography_name = geography_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "unit_id", "legal_entity_name", "division_name",
                "category_name", "unit_code", "unit_name",
                "address", "domain_names",
                "org_names_list", "geography_name"
            ]
        )
        unit_id = data.get("unit_id")
        legal_entity_name = data.get("legal_entity_name")
        division_name = data.get("division_name")
        category_name = data.get("category_name")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        address = data.get("address")
        domain_names = data.get("domain_names")
        org_names_list = data.get("org_names_list")
        geography_name = data.get("geography_name")
        return AssignedUnitDetails(
            unit_id, legal_entity_name, division_name, category_name,
            unit_code, unit_name, address, domain_names,
            org_names_list, geography_name
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "legal_entity_name": self.legal_entity_name,
            "division_name": self.division_name,
            "category_name": self.category_name,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "address": self.address,
            "domain_names": self.domain_names,
            "org_names_list": self.org_names_list,
            "geography_name": self.geography_name
        }


class GetUnassignedUnitsSuccess(Response):
    def __init__(self, unassigned_units_list, user_category_id):
        self.unassigned_units_list = unassigned_units_list
        self.user_category_id = user_category_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unassigned_units_list"])
        unassigned_units_list = data.get("unassigned_units_list")
        user_category_id = data.get("user_category_id")
        return GetUnassignedUnitsSuccess(unassigned_units_list, user_category_id)

    def to_inner_structure(self):
        return {
            "unassigned_units_list": self.unassigned_units_list,
            "user_category_id": self.user_category_id
        }


class GetAssignedUnitsSuccess(Response):
    def __init__(self, assigned_units_list):
        self.assigned_units_list = assigned_units_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assigned_units_list"])
        assigned_units_list = data.get("assigned_units_list")
        return GetAssignedUnitsSuccess(assigned_units_list)

    def to_inner_structure(self):
        return {
            "assigned_units_list": self.assigned_units_list
        }


class GetAssignedUnitDetailsSuccess(Response):
    def __init__(self, assigned_unit_details_list):
        self.assigned_unit_details_list = assigned_unit_details_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assigned_unit_details_list"])
        assigned_unit_details_list = data.get("assigned_unit_details_list")
        return GetAssignedUnitDetailsSuccess(assigned_unit_details_list)

    def to_inner_structure(self):
        return {
            "assigned_unit_details_list": self.assigned_unit_details_list
        }


class GetAssignUnitFormDataSuccess(Response):
    def __init__(
        self, business_groups, unit_legal_entity, assigned_unit_details_list,
        domain_manager_users, mapped_domain_users
    ):
        self.business_groups = business_groups
        self.unit_legal_entity = unit_legal_entity
        self.assigned_unit_details_list = assigned_unit_details_list
        self.domain_manager_users = domain_manager_users
        self.mapped_domain_users = mapped_domain_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "business_groups", "unit_legal_entity",
                "assigned_unit_details_list",
                "domain_manager_users", "mapped_domain_users"
            ])
        business_groups = data.get("business_groups")
        unit_legal_entity = data.get("unit_legal_entity")
        assigned_unit_details_list = data.get("assigned_unit_details_list")
        domain_manager_users = data.get("domain_manager_users")
        mapped_domain_users = data.get("mapped_domain_users")
        return GetAssignUnitFormDataSuccess(
            business_groups, unit_legal_entity, assigned_unit_details_list,
            domain_manager_users, mapped_domain_users
        )

    def to_inner_structure(self):
        return {
            "business_groups": self.business_groups,
            "unit_legal_entity": self.unit_legal_entity,
            "assigned_unit_details_list": self.assigned_unit_details_list,
            "domain_manager_users": self.domain_manager_users,
            "mapped_domain_users": self.mapped_domain_users,
        }


class SaveAsssignedUnitsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveAsssignedUnitsSuccess()

    def to_inner_structure(self):
        return {
        }

class UnassignedUnitSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UnassignedUnitSuccess()

    def to_inner_structure(self):
        return {
        }

def _init_Response_class_map():
    classes = [
        GetClientGroupsSuccess, SaveClientGroupSuccess, GroupNameAlreadyExists,
        UpdateClientGroupSuccess, ChangeClientGroupStatusSuccess,
        InvalidClientId, GetClientsSuccess, GetClientsEditSuccess, SaveClientSuccess,
        BusinessGroupNameAlreadyExists, LegalEntityNameAlreadyExists,
        DivisionNameAlreadyExists, UnitNameAlreadyExists, CategoryNameAlreadyExists,
        UnitCodeAlreadyExists, LogoSizeLimitExceeds, UpdateClientSuccess,
        ChangeClientStatusSuccess,
        InvalidBusinessGroupId,
        InvalidLegalEntityId, InvalidDivisionId,
        InvalidDivisionName, InvalidCategoryName,
        InvalidUnitId, UserIsNotResponsibleForAnyClient, ClientCreationFailed,
        CannotDeactivateCountry, CannotDeactivateDomain, CreateNewAdminSuccess,
        ClientDatabaseNotExists, CannotDeactivateClient,
        ServerIsFull, NotAnImageFile,
        GetNextUnitCodeSuccess, GetClientGroupFormDataSuccess,
        GetAssignLegalEntityListSuccess, GetUnassignedUnitsSuccess,
        GetAssignUnitFormDataSuccess, SaveAsssignedUnitsSuccess,
        GetEditAssignLegalEntitySuccess, SaveAssignLegalEntitySuccess,
        ViewAssignLegalEntitySuccess, SaveDivisionCategorySuccess,
        UnassignedUnitSuccess
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
            request, "technomasters", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "technomasters", "Response"
            )
        }
