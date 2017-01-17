from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    to_structure_dictionary_values, parse_VariantType, to_VariantType
)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_core_GroupCompany,
    parse_structure_UnsignedIntegerType_32, parse_structure_Bool,
    parse_structure_OptionalType_VectorType_RecordType_core_Division,
    parse_structure_OptionalType_VectorType_RecordType_core_BusinessGroup,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_CustomTextType_50,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_ClientConfiguration,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_RecordType_technomasters_PROFILE_DETAIL,
    parse_structure_VectorType_RecordType_technomasters_PROFILES,
    parse_structure_VariantType_technomasters_Request,
    parse_structure_CustomTextType_20,
    parse_structure_OptionalType_RecordType_techno_master_BUSINESSGROUP,
    parse_structure_OptionalType_RecordType_techno_master_LEGALENTITY,
    parse_structure_OptionalType_RecordType_techno_master_DIVISION,
    parse_structure_VectorType_RecordType_techno_master_UNIT,
    parse_structure_VectorType_RecordType_techno_master_COUNTRYWISEUNITS,
    parse_structure_Float,
    parse_structure_VectorType_RecordType_core_Industry,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    parse_structure_VectorType_RecordType_technomasters_Unit,
    parse_structure_VectorType_RecordType_technomasters_CountryWiseUnits,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_GeographyWithMapping,
    parse_structure_RecordType_core_FileList,
    parse_structure_VectorType_UnsignedIntegerType_32,
    parse_structure_CustomTextType_500,
    parse_structure_VectorType_RecordType_core_ClientInchargePersons,
    parse_structure_OptionalType_RecordType_core_FileList,
    parse_structure_OptionalType_CustomTextType_250,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_OptionalType_CustomTextType_50,
    parse_structure_VectorType_RecordType_core_ClientGroup,
    parse_structure_VectorType_RecordType_core_LegalEntityDetails,
    parse_structure_VectorType_RecordType_core_Industries,
    parse_structure_VectorType_RecordType_core_AssignLegalEntity
)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_core_GroupCompany,
    to_structure_SignedIntegerType_8, to_structure_Bool,
    to_structure_OptionalType_VectorType_RecordType_core_Division,
    to_structure_RecordType_core_CountryWiseUnits,
    to_structure_OptionalType_VectorType_RecordType_core_BusinessGroup,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_OptionalType_RecordType_core_Division,
    to_structure_VectorType_RecordType_core_UnitDetails,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_CustomTextType_50,
    to_structure_RecordType_core_LegalEntity,
    to_structure_CustomTextType_100,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_OptionalType_RecordType_core_BusinessGroup,
    to_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_ClientConfiguration,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_RecordType_technomasters_PROFILE_DETAIL,
    to_structure_VectorType_RecordType_technomasters_PROFILES,
    to_structure_VariantType_technomasters_Request,
    to_structure_CustomTextType_20,
    to_structure_Float,
    to_structure_VectorType_RecordType_core_Industry,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    to_structure_VectorType_RecordType_technomasters_Unit,
    to_structure_VectorType_RecordType_technomasters_UnitDetails,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_UnsignedIntegerType_32,
    to_structure_MapType_UnsignedInteger_32_VectorType_RecordType_technomaster_UnitDetails,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_GeographyWithMapping,
    to_structure_RecordType_core_FileList,
    to_structure_VectorType_UnsignedIntegerType_32,
    to_structure_CustomTextType_500,
    to_structure_VectorType_RecordType_core_ClientInchargePersons,
    to_structure_OptionalType_RecordType_core_FileList,
    to_structure_OptionalType_CustomTextType_250,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_OptionalType_CustomTextType_50,
    to_structure_VectorType_RecordType_core_GroupCompanyForUnitCreation,
    to_structure_VectorType_RecordType_core_ClientGroup,
    to_structure_VectorType_RecordType_core_LegalEntityDetails,
    to_structure_VectorType_RecordType_core_Industries,
    to_structure_VectorType_RecordType_core_AssignLegalEntity
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


class CreateNewAdmin(Request):
    def __init__(self, new_admin_id, client_id, old_admin_id, username):
        self.new_admin_id = new_admin_id
        self.client_id = client_id
        self.old_admin_id = old_admin_id
        self.username = username

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["new_admin_id", "client_id", "old_admin_id", "username"])
        new_admin_id = data.get("new_admin_id")
        new_admin_id = parse_structure_UnsignedIntegerType_32(new_admin_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        old_admin_id = data.get("old_admin_id")
        old_admin_id = parse_structure_UnsignedIntegerType_32(old_admin_id)
        username = data.get("username")
        username = parse_structure_CustomTextType_100(username)
        return CreateNewAdmin(
            new_admin_id, client_id, old_admin_id, username
        )

    def to_inner_structure(self):
        return {
            "new_admin_id": to_structure_UnsignedIntegerType_32(
                self.new_admin_id),
            "client_id": to_structure_UnsignedIntegerType_32(self.client_id),
            "old_admin_id": to_structure_UnsignedIntegerType_32(
                self.old_admin_id),
            "username": to_structure_CustomTextType_100(self.username)
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


class ChangeClientGroupStatus(Request):
    def __init__(self, client_id, is_active):
        self.client_id = client_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "is_active"])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeClientGroupStatus(client_id, is_active)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "is_active": to_structure_Bool(self.is_active),
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
    def __init__(self, client_id, business_group_id, legal_entity_id, country_id):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "bg_id", "le_id", "c_id"])
        client_id = data.get("client_id")
        business_group_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        country_id = data.get("c_id")
        return GetClientsEdit(client_id, business_group_id, legal_entity_id, country_id)

    def to_inner_structure(self):
        data = {
            "client_id": self.client_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id
        }
        return data


class BUSINESS_GROUP(Request):
    def __init__(self, business_group_id, business_group_name):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "bg_id", "bg_name"
            ]
        )
        business_group_id = data.get("bg_id")
        business_group_name = data.get("bg_name")
        return BUSINESS_GROUP(business_group_id, business_group_name)

    def to_inner_structure(self):
        data = {
            "business_group_id": self.business_group_id,
            "business_group_name": self.business_group_name,
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
        legal_entity_id = parse_structure_OptionalType_UnsignedIntegerType_32(legal_entity_id)
        legal_entity_name = data.get("le_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        return LEGAL_ENTITY(legal_entity_id, legal_entity_name)

    def to_inner_structure(self):
        return {
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
        }

class DIVISION(Request):
    def __init__(self, division_id, division_name):
        self.division_id = division_id
        self.division_name = division_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["d_id", "d_name"])
        division_id = data.get("d_id")
        division_id = parse_structure_OptionalType_UnsignedIntegerType_32(division_id)
        division_name = data.get("d_name")
        division_name = parse_structure_CustomTextType_50(division_name)
        return DIVISION(division_id, division_name)

    def to_inner_structure(self):
        return {
            "division_id": to_structure_SignedIntegerType_8(self.division_id),
            "division_name": to_structure_CustomTextType_50(self.division_name),
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
            "division_id": self.division_id,
            "division_name": self.division_name,
            "category_name": self.category_name,
            "division_cnt": self.division_cnt,
            "unit_cnt": self.unit_cnt,
        }
        return data


class UNIT(object):
    def __init__(
        self, unit_id, geography_id, unit_code, unit_name, unit_address,
        postal_code, domain_ids, industry_ids
    ):
        self.unit_id = unit_id
        self.geography_id = geography_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.postal_code = postal_code
        self.domain_ids = domain_ids
        self.industry_ids = industry_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "unit_id", "geography_id", "unit_code", "unit_name",
                "address", "postal_code",  "d_ids",
                "i_ids_list"
            ]
        )
        print "inside class uint after append"
        unit_id = data.get("unit_id")
        geography_id = data.get("geography_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        unit_address = data.get("address")
        postal_code = data.get("postal_code")
        domain_ids = data.get("d_ids")
        industry_ids = data.get("i_ids_list")
        return UNIT(
            unit_id, geography_id, unit_code, unit_name, unit_address,
            postal_code, domain_ids, industry_ids
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "geography_id": self.geography_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "unit_address": self.unit_address,
            "postal_code": self.postal_code,
            "domain_ids": self.domain_ids,
            "industry_ids": self.industry_ids
        }

class COUNTRYWISEUNITS(object):
    def __init__(self, country_id, units):
        self.country_id = country_id
        self.units = units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["c_id", "units"])
        country_id = data.get("c_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_techno_master_UNIT(units)
        return COUNTRYWISEUNITS(country_id, units)

    def to_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "units": to_structure_VectorType_RecordType_core_UnitDetails(self.units),
        }

class SaveClient(Request):
    def __init__(self, client_id, business_group_id, legal_entity_id, country_id, division_units, units):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.division_units = division_units
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "cl_id", "bg_id", "le_id", "c_id", "division_units", "units"
            ]
        )
        client_id = data.get("cl_id")
        business_group_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        country_id = data.get("c_id")
        division_units = data.get("division_units")
        units = data.get("units")
        return SaveClient(
            client_id, business_group_id, legal_entity_id, country_id, division_units, units
        )

    def to_inner_structure(self):
        data = {
            "client_id": self.client_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "division_units": self.division_units,
            "units": self.units,
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
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        business_group = data.get("bg")
        business_group = parse_structure_OptionalType_RecordType_techno_master_BUSINESSGROUP(business_group)
        legal_entity = data.get("le")
        legal_entity = parse_structure_OptionalType_RecordType_techno_master_LEGALENTITY(legal_entity)
        division = data.get("d")
        division = parse_structure_OptionalType_RecordType_techno_master_DIVISION(division)
        country_wise_units = data.get("cw_units")
        country_wise_units = parse_structure_VectorType_RecordType_techno_master_COUNTRYWISEUNITS(country_wise_units)
        return UpdateClient(client_id, business_group, legal_entity, division, country_wise_units)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "business_group": to_structure_OptionalType_RecordType_core_BusinessGroup(self.business_group),
            "legal_entity": to_structure_RecordType_core_LegalEntity(self.legal_entity),
            "division": to_structure_OptionalType_RecordType_core_Division(self.division),
            "country_wise_units": to_structure_RecordType_core_CountryWiseUnits(self.country_wise_units),
        }

class ChangeClientStatus(Request):
    def __init__(self, client_id, legal_entity_id, division_id, is_active):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "legal_entity_id", "division_id", "is_active"])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_UnsignedIntegerType_32(division_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeClientStatus(client_id, legal_entity_id, division_id, is_active)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "is_active": to_structure_Bool(self.is_active),
        }

class ReactivateUnit(Request):
    def __init__(self, client_id, unit_id, password):
        self.unit_id = unit_id
        self.password = password
        self.client_id = client_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_id", "password"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        password = data.get("password")
        password = parse_structure_CustomTextType_20(password)
        return ReactivateUnit(client_id, unit_id, password)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "password": to_structure_CustomTextType_20(self.password),
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
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        return GetNextUnitCode(client_id)

    def to_inner_structure(self):
        return {
            "client_id" : to_structure_UnsignedIntegerType_32(self.client_id)
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


def _init_Request_class_map():
    classes = [
        GetClientGroups, SaveClientGroup, UpdateClientGroup,
        ChangeClientGroupStatus, GetClients, GetClientsEdit, SaveClient, UpdateClient,
        ChangeClientStatus, ReactivateUnit, GetClientProfile, CreateNewAdmin,
        GetNextUnitCode, GetClientGroupFormData, GetEditClientGroupFormData,
        GetAssignLegalEntityList, GetUnassignedUnits, GetAssignedUnits,
        GetAssignedUnitDetails, GetAssignUnitFormData, SaveAsssignedUnits,
        GetEditAssignLegalEntity, SaveAssignLegalEntity, ViewAssignLegalEntity
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
            "unassign_legal_entities", "techno_users"
        ])

        unassign_legal_entities = data.get("unnssign_legal_entities")
        techno_users = data.get("techno_users")

        return GetEditAssignLegalEntitySuccess(
            unassign_legal_entities, techno_users
        )

    def to_inner_structure(self):

        return {
            "unassign_legal_entities": self.unassign_legal_entities,
            "techno_users": self.techno_users
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

class Unit(object):
    def __init__(
        self, business_group_id, legal_entity_id, division_id,
        client_id, units, is_active
    ):
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.client_id = client_id
        self.units = units
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_id", "legal_entity_id", "division_id", "client_id", "units", "is_active"])
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_UnsignedIntegerType_32(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_UnsignedIntegerType_32(division_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_technomasters_CountryWiseUnits(units)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Unit(business_group_id, legal_entity_id, division_id, client_id, units, is_active)

    def to_structure(self):
        return {
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "units" : to_structure_MapType_UnsignedInteger_32_VectorType_RecordType_technomaster_UnitDetails(self.units),
            "is_active": to_structure_Bool(self.is_active)
        }

#
# CountryWiseUnits
#

class CountryWiseUnits(object):
    def __init__(self, country_id, units):
        self.country_id = country_id
        self.units = units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "units"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_technomasters_UnitDetails(units)
        return CountryWiseUnits(country_id, units)

    def to_structure(self):
        return {
            to_structure_SignedIntegerType_8(self.country_id) : to_structure_VectorType_RecordType_technomasters_UnitDetails(self.units),
        }


class UnitDetails(object):
    def __init__(
        self, unit_id, client_id, business_group_id,
        legal_entity_id, country_id, division_id, category_name,
        geography_id, unit_code, unit_name, unit_address,
        postal_code, domain_ids, i_ids, is_active, approve_status
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
        self.unit_address = unit_address
        self.postal_code = postal_code
        self.domain_ids = domain_ids
        self.i_ids = i_ids
        self.is_active = is_active
        self.approve_status = approve_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "unit_id", "client_id", "business_group_id", "legal_entity_id", "country_id", "division_id", "category_name",
                "geography_id", "unit_code", "unit_name", "unit_address",
                "postal_code", "domain_id", "industry_id", "is_active", "approve_status"])
        unit_id = data.get("unit_id")
        client_id = data.get("client_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        country_id = data.get("country_id")
        division_id = data.get("division_id")
        category_name = data.get("category_name")
        geography_id = data.get("geography_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        unit_address = data.get("unit_address")
        postal_code = data.get("postal_code")
        domain_ids = data.get("domain_id")
        i_ids = data.get("industry_id")
        is_active = data.get("is_active")
        approve_status = data.get("approve_status")
        return UnitDetails(
            unit_id, client_id, business_group_id, legal_entity_id, country_id, division_id, category_name,
            geography_id, unit_code, unit_name, unit_address, postal_code,
            domain_ids, i_ids, is_active, approve_status
        )

    def to_structure(self):
        data = {
            "unit_id": self.unit_id,
            "client_id": self.client_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "division_id": self.division_id,
            "category_name": self.category_name,
            "geography_id": self.geography_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "unit_address": self.unit_address,
            "postal_code": self.postal_code,
            "domain_ids": self.domain_ids,
            "i_ids": self.i_ids,
            "is_active": self.is_active,
            "approve_status": self.approve_status,
        }
        return data


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
        self, countries,  business_groups, domains, industries,
        group_name, email_id, short_name, no_of_licence,
        legal_entities, date_configurations
    ):
        self.countries = countries
        self.business_groups = business_groups
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
            "countries", "business_groups", "domains", "industries",
            "client_details", "group_name", "email_id", "legal_entities_list",
            "date_configurations", "short_name", "no_of_licence"
        ])
        countries = data.get("countries")
        business_groups = data.get("business_groups")
        domains = data.get("domains")
        industries = data.get("industries")
        group_name = data.get("group_name")
        short_name = data.get("short_name")
        email_id = data.get("email_id")
        legal_entities = data.get("legal_entities_list")
        date_configurations = data.get("date_configurations")
        no_of_licence = data.get("no_of_licence")
        return GetEditClientGroupFormDataSuccess(
            countries,  business_groups, domains, industries,
            group_name, email_id, short_name, no_of_licence,
            legal_entities, date_configurations
        )

    def to_inner_structure(self):
        #print "self.business_groups: %s" % self.business_groups
        return {
            "countries": self.countries,
            "business_groups": self.business_groups,
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
        self, unit_list, group_company_list, business_group_list, countries_units, unit_legal_entity,
        domains_organization_list, divisions, unit_geography_level_list, unit_geographies_list
    ):
        self.unit_list = unit_list
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
            "unit_list", "group_company_list", "business_group_list", "countries_units", "unit_legal_entity",
            "domains_organization_list", "divisions", "unit_geography_level_list", "unit_geographies_list"
        ])
        unit_list = data.get("unit_list")
        group_company_list = data.get("group_company_list")
        business_group_list = data.get("business_group_list")
        countries_units = data.get("countries_units")
        unit_legal_entity = data.get("unit_legal_entity")
        domains_organization_list = data.get("domains_organization_list")
        divisions = data.get("divisions")
        unit_geography_level_list = data.get("unit_geography_level_list")
        unit_geographies_list = data.get("unit_geographies_list")

        return GetClientsSuccess(
            unit_list, group_company_list, business_group_list, countries_units, unit_legal_entity,
            domains_organization_list, divisions, unit_geography_level_list, unit_geographies_list
        )

    def to_inner_structure(self):
        data = {
            "unit_list": self.unit_list,
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
        next_unit_code = parse_structure_UnsignedIntegerType_32(next_unit_code)
        return GetNextUnitCodeSuccess(next_unit_code)

    def to_inner_structure(self):
        return {
            "next_unit_code": to_structure_UnsignedIntegerType_32(self.next_unit_code)
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
        error = parse_structure_CustomTextType_500(error)
        return ClientCreationFailed(error)

    def to_inner_structure(self):
        return {
            "error": to_structure_CustomTextType_500(self.error)
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

class ReactivateUnitSuccess(Response):
    def __init__(self, unit_code, unit_name):
        self.unit_code = unit_code
        self.unit_name = unit_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_code"])
        unit_code = data.get("unit_code")
        unit_code = parse_structure_CustomTextType_50(unit_code)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        return ReactivateUnitSuccess(
            unit_code=unit_code, unit_name=unit_name
        )

    def to_inner_structure(self):
        return {
            "unit_code": to_structure_CustomTextType_50(self.unit_code),
            "unit_name": to_structure_CustomTextType_50(self.unit_name)
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

class ReassignFirst(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ReassignFirst()

    def to_inner_structure(self):
        return {
        }

class GetClientProfileSuccess(Response):
    def __init__(self, group_companies, profiles):
        self.group_companies = group_companies
        self.profiles = profiles

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["group_companies", "profiles"])
        group_companies = data.get("group_companies")
        group_companies = parse_structure_VectorType_RecordType_core_GroupCompany(group_companies)
        profiles = data.get("profiles")
        profiles = parse_structure_VectorType_RecordType_technomasters_PROFILES(profiles)
        return GetClientProfileSuccess(group_companies, profiles)

    def to_inner_structure(self):
        return {
            "group_companies": to_structure_VectorType_RecordType_core_GroupCompany(self.group_companies),
            "profiles": to_structure_VectorType_RecordType_technomasters_PROFILES(self.profiles),
        }

class InvalidNoOfLicence(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidNoOfLicence()

    def to_inner_structure(self):
        return {
        }


class InvalidFileSpace(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidFileSpace()

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
        user_category_id = data.get("user_category_id");
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


def _init_Response_class_map():
    classes = [
        GetClientGroupsSuccess, SaveClientGroupSuccess, GroupNameAlreadyExists,
        UpdateClientGroupSuccess, ChangeClientGroupStatusSuccess,
        InvalidClientId, GetClientsSuccess, GetClientsEditSuccess, SaveClientSuccess,
        BusinessGroupNameAlreadyExists, LegalEntityNameAlreadyExists,
        DivisionNameAlreadyExists, UnitNameAlreadyExists,
        UnitCodeAlreadyExists, LogoSizeLimitExceeds, UpdateClientSuccess,
        ChangeClientStatusSuccess, ReactivateUnitSuccess,
        GetClientProfileSuccess, InvalidBusinessGroupId,
        InvalidLegalEntityId, InvalidDivisionId,
        InvalidDivisionName, InvalidCategoryName,
        InvalidUnitId, UserIsNotResponsibleForAnyClient, ClientCreationFailed,
        CannotDeactivateCountry, CannotDeactivateDomain, CreateNewAdminSuccess,
        ClientDatabaseNotExists, CannotDeactivateClient, ReassignFirst,
        InvalidNoOfLicence, InvalidFileSpace, ServerIsFull, NotAnImageFile,
        GetNextUnitCodeSuccess, GetClientGroupFormDataSuccess,
        GetAssignLegalEntityListSuccess, GetUnassignedUnitsSuccess,
        GetAssignUnitFormDataSuccess, SaveAsssignedUnitsSuccess,
        GetEditAssignLegalEntitySuccess, SaveAssignLegalEntitySuccess,
        ViewAssignLegalEntitySuccess
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
            "session_token": to_structure_CustomTextType_50(
                self.session_token),
            "request": to_VariantType(
                self.request, "technomasters", "Response"
            )
        }

#
# LICENCE_HOLDER_DETAILS
#

class LICENCE_HOLDER_DETAILS(object):
    def __init__(
        self, user_id, user_name, email_id, contact_no,
        seating_unit_name, address, total_disk_space, used_disk_space,
        is_active, is_admin, is_service_provider
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.email_id = email_id
        self.contact_no = contact_no
        self.seating_unit_name = seating_unit_name
        self.address = address
        self.total_disk_space = total_disk_space
        self.used_disk_space = used_disk_space
        self.is_active = is_active
        self.is_admin = is_admin
        self.is_service_provider = is_service_provider

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "user_id", "user_name", "email_id", "contact_no",
                "seating_unit_name", "address", "total_disk_space",
                "used_disk_space", "is_active", "is_admin", "is_service_provider"
            ]
        )
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        user_name = data.get("user_name")
        user_name = parse_structure_CustomTextType_50(user_name)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_OptionalType_CustomTextType_20(contact_no)
        seating_unit_name = data.get("seating_unit_name")
        seating_unit_name = parse_structure_OptionalType_CustomTextType_50(seating_unit_name)
        address = data.get("address")
        address = parse_structure_OptionalType_CustomTextType_250(address)
        total_disk_space = data.get("total_disk_space")
        total_disk_space = parse_structure_Float(total_disk_space)
        used_disk_space = data.get("used_disk_space")
        used_disk_space = parse_structure_Float(used_disk_space)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        is_admin = data.get("is_admin")
        is_admin = parse_structure_Bool(is_admin)
        is_service_provider = data.get("is_service_provider")
        is_service_provider = parse_structure_Bool(is_service_provider)
        return LICENCE_HOLDER_DETAILS(
            user_id, user_name, email_id, contact_no, seating_unit_name,
            address, total_disk_space, used_disk_space, is_active, is_admin,
            is_service_provider
        )

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "user_name": to_structure_CustomTextType_50(self.user_name),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "contact_no": to_structure_OptionalType_CustomTextType_20(self.contact_no),
            "seating_unit_name": to_structure_OptionalType_CustomTextType_50(self.seating_unit_name),
            "address": to_structure_OptionalType_CustomTextType_250(self.address),
            "total_disk_space": to_structure_Float(self.total_disk_space),
            "used_disk_space": to_structure_Float(self.used_disk_space),
            "is_active": to_structure_Bool(self.is_active),
            "is_admin": to_structure_Bool(self.is_admin),
            "is_service_provider": to_structure_Bool(self.is_service_provider)
        }

#
# PROFILE_DETAIL
#

class PROFILE_DETAIL(object):
    def __init__(self, contract_from, contract_to, no_of_user_licence, remaining_licence, total_disk_space, used_disk_space, licence_holders):
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.no_of_user_licence = no_of_user_licence
        self.remaining_licence = remaining_licence
        self.total_disk_space = total_disk_space
        self.used_disk_space = used_disk_space
        self.licence_holders = licence_holders

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["contract_from", "contract_to", "no_of_user_licence", "remaining_licence", "total_disk_space", "used_disk_space", "licence_holders"])
        contract_from = data.get("contract_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("contract_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        no_of_user_licence = data.get("no_of_user_licence")
        no_of_user_licence = parse_structure_UnsignedIntegerType_32(no_of_user_licence)
        remaining_licence = data.get("remaining_licence")
        remaining_licence = parse_structure_UnsignedIntegerType_32(remaining_licence)
        total_disk_space = data.get("total_disk_space")
        total_disk_space = parse_structure_Float(total_disk_space)
        used_disk_space = data.get("used_disk_space")
        used_disk_space = parse_structure_Float(used_disk_space)
        licence_holders = data.get("licence_holders")
        licence_holders = parse_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS(licence_holders)
        return PROFILE_DETAIL(contract_from, contract_to, no_of_user_licence, remaining_licence, total_disk_space, used_disk_space, licence_holders)

    def to_structure(self):
        return {
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "no_of_user_licence": to_structure_UnsignedIntegerType_32(self.no_of_user_licence),
            "remaining_licence": to_structure_UnsignedIntegerType_32(self.remaining_licence),
            "total_disk_space": to_structure_Float(self.total_disk_space),
            "used_disk_space": to_structure_Float(self.used_disk_space),
            "licence_holders": to_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS(self.licence_holders),
        }

#
# PROFILES
#

class PROFILES(object):
    def __init__(self, client_id, profile_detail):
        self.client_id = client_id
        self.profile_detail = profile_detail

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "profile_detail"])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        profile_detail = data.get("profile_detail")
        profile_detail = parse_structure_RecordType_technomasters_PROFILE_DETAIL(profile_detail)
        return PROFILES(client_id, profile_detail)

    def to_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "profile_detail": to_structure_RecordType_technomasters_PROFILE_DETAIL(self.profile_detail),
        }
