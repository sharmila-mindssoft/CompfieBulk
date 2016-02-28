from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_core_GroupCompany,
    parse_structure_UnsignedIntegerType_32, parse_structure_Bool,
    parse_structure_OptionalType_VectorType_RecordType_core_Division,
    parse_structure_OptionalType_VectorType_RecordType_core_BusinessGroup,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_CustomTextType_50,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_User,
    parse_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_ClientConfiguration,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_RecordType_technomasters_PROFILE_DETAIL,
    parse_structure_VectorType_RecordType_technomasters_PROFILES,
    parse_structure_VariantType_technomasters_Request,
    parse_structure_CustomTextType_20,
    parse_structure_VectorType_RecordType_core_GroupCompanyDetail,
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
    parse_structure_CustomTextType_500
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
    to_structure_VectorType_RecordType_core_User,
    to_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_ClientConfiguration,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_RecordType_technomasters_PROFILE_DETAIL,
    to_structure_VectorType_RecordType_technomasters_PROFILES,
    to_structure_VariantType_technomasters_Request,
    to_structure_CustomTextType_20,
    to_structure_VectorType_RecordType_core_GroupCompanyDetail,
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
    to_structure_CustomTextType_500
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

class SaveClientGroup(Request):
    def __init__(self, group_name, country_ids, domain_ids, logo, contract_from, contract_to, incharge_persons, no_of_user_licence, file_space, is_sms_subscribed, email_id, date_configurations, short_name):
        self.group_name = group_name
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.logo = logo
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.incharge_persons = incharge_persons
        self.no_of_user_licence = no_of_user_licence
        self.file_space = file_space
        self.is_sms_subscribed = is_sms_subscribed
        self.email_id = email_id
        self.date_configurations = date_configurations
        self.short_name = short_name

    @staticmethod
    def parse_inner_structure(data):
        print "inside save client group  parse structure"
        data = parse_dictionary(data, ["group_name", "country_ids", "domain_ids", "logo", "contract_from", "contract_to", "incharge_persons", "no_of_user_licence", "file_space", "is_sms_subscribed", "email_id", "date_configurations", "short_name"])
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        logo = data.get("logo")
        logo = parse_structure_RecordType_core_FileList(logo)
        contract_from = data.get("contract_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("contract_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        incharge_persons = data.get("incharge_persons")
        incharge_persons = parse_structure_VectorType_UnsignedIntegerType_32(incharge_persons)
        no_of_user_licence = data.get("no_of_user_licence")
        no_of_user_licence = parse_structure_UnsignedIntegerType_32(no_of_user_licence)
        file_space = data.get("file_space")
        file_space = parse_structure_Float(file_space)
        is_sms_subscribed = data.get("is_sms_subscribed")
        is_sms_subscribed = parse_structure_Bool(is_sms_subscribed)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        date_configurations = data.get("date_configurations")
        date_configurations = parse_structure_VectorType_RecordType_core_ClientConfiguration(date_configurations)
        short_name = data.get("short_name")
        short_name = parse_structure_CustomTextType_20(short_name)
        return SaveClientGroup(group_name, country_ids, domain_ids, logo, contract_from, contract_to, incharge_persons, no_of_user_licence, file_space, is_sms_subscribed, email_id, date_configurations, short_name)

    def to_inner_structure(self):
        return {
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "logo": to_structure_RecordType_core_FileList(self.logo),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "incharge_persons": to_structure_VectorType_UnsignedIntegerType_32(self.incharge_persons),
            "no_of_user_licence": to_structure_UnsignedIntegerType_32(self.no_of_user_licence),
            "file_space": to_structure_Float(self.file_space),
            "is_sms_subscribed": to_structure_Bool(self.is_sms_subscribed),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "date_configurations": to_structure_VectorType_RecordType_core_ClientConfiguration(self.date_configurations),
            "short_name" : to_structure_CustomTextType_20(self.short_name)
        }

class UpdateClientGroup(Request):
    def __init__(self, client_id, group_name, country_ids, domain_ids, logo, contract_from, contract_to, incharge_persons, no_of_user_licence, file_space, is_sms_subscribed, date_configurations):
        self.client_id = client_id
        self.group_name = group_name
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.logo = logo
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.incharge_persons = incharge_persons
        self.no_of_user_licence = no_of_user_licence
        self.file_space = file_space
        self.is_sms_subscribed = is_sms_subscribed
        self.date_configurations = date_configurations

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "group_name", "country_ids", "domain_ids", "logo", "contract_from", "contract_to", "incharge_persons", "no_of_user_licence", "file_space", "is_sms_subscribed", "date_configurations"])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        logo = data.get("logo")
        logo = parse_structure_RecordType_core_FileList(logo)
        contract_from = data.get("contract_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("contract_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        incharge_persons = data.get("incharge_persons")
        incharge_persons = parse_structure_VectorType_UnsignedIntegerType_32(incharge_persons)
        no_of_user_licence = data.get("no_of_user_licence")
        no_of_user_licence = parse_structure_UnsignedIntegerType_32(no_of_user_licence)
        file_space = data.get("file_space")
        file_space = parse_structure_Float(file_space)
        is_sms_subscribed = data.get("is_sms_subscribed")
        is_sms_subscribed = parse_structure_Bool(is_sms_subscribed)
        date_configurations = data.get("date_configurations")
        date_configurations = parse_structure_VectorType_RecordType_core_ClientConfiguration(date_configurations)
        return UpdateClientGroup(client_id, group_name, country_ids, domain_ids, logo, contract_from, contract_to, incharge_persons, no_of_user_licence, file_space, is_sms_subscribed, date_configurations)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "logo": to_structure_RecordType_core_FileList(self.logo),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "incharge_persons": to_structure_VectorType_UnsignedIntegerType_32(self.incharge_persons),
            "no_of_user_licence": to_structure_UnsignedIntegerType_32(self.no_of_user_licence),
            "file_space": to_structure_Float(self.file_space),
            "is_sms_subscribed": to_structure_Bool(self.is_sms_subscribed),
            "date_configurations": to_structure_VectorType_RecordType_core_ClientConfiguration(self.date_configurations),
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

class BUSINESS_GROUP(Request):
    def __init__(self, business_group_id, business_group_name):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["business_group_id", "business_group_name"])
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_UnsignedIntegerType_32(business_group_id)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_CustomTextType_50(business_group_name)
        return BUSINESS_GROUP(business_group_id, business_group_name)

    def to_inner_structure(self):
        return {
            "business_group_id": to_structure_SignedIntegerType_8(self.business_group_id),
            "business_group_name": to_structure_CustomTextType_50(self.business_group_name),
        }

class LEGAL_ENTITY(Request):
    def __init__(self, legal_entity_id, legal_entity_name):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entity_id", "legal_entity_name"])
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_UnsignedIntegerType_32(legal_entity_id)
        legal_entity_name = data.get("legal_entity_name")
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
        data = parse_dictionary(data, ["division_id", "division_name"])
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_UnsignedIntegerType_32(division_id)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_50(division_name)
        return DIVISION(division_id, division_name)

    def to_inner_structure(self):
        return {
            "division_id": to_structure_SignedIntegerType_8(self.division_id),
            "division_name": to_structure_CustomTextType_50(self.division_name),
        }


class UNIT(object):
    country_id = None

    def __init__(
        self, unit_id, geography_id, unit_code, unit_name, industry_id,
        industry_name, unit_address, unit_location, postal_code, domain_ids
    ):
        self.unit_id = unit_id
        self.geography_id = geography_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.unit_address = unit_address
        self.unit_location = unit_location
        self.postal_code = postal_code
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "geography_id", "unit_code", "unit_name", "industry_id", "industry_name", "unit_address", "unit_location", "postal_code", "domain_ids"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_UnsignedIntegerType_32(unit_id)
        geography_id = data.get("geography_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        unit_code = data.get("unit_code")
        unit_code = parse_structure_CustomTextType_20(unit_code)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        industry_id = data.get("industry_id")
        industry_id = parse_structure_UnsignedIntegerType_32(industry_id)
        industry_name = data.get("industry_name")
        industry_name = parse_structure_CustomTextType_50(industry_name)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_250(unit_address)
        unit_location = data.get("unit_location")
        unit_location = parse_structure_CustomTextType_250(unit_location)
        postal_code = data.get("postal_code")
        postal_code = parse_structure_UnsignedIntegerType_32(postal_code)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        return UNIT(
            unit_id, geography_id, unit_code, unit_name, industry_id,
            industry_name, unit_address, unit_location, postal_code, domain_ids
        )

    def to_structure(self):
        return {
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "industry_name": to_structure_CustomTextType_50(self.industry_name),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "unit_location": to_structure_CustomTextType_250(self.unit_location),
            "postal_code": to_structure_SignedIntegerType_8(self.postal_code),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
        }

class COUNTRYWISEUNITS(object):
    def __init__(self, country_id, units):
        self.country_id = country_id
        self.units = units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "units"])
        country_id = data.get("country_id")
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
    def __init__(self, client_id, business_group, legal_entity, division, country_wise_units):
        self.client_id = client_id
        self.business_group = business_group
        self.legal_entity = legal_entity
        self.division = division
        self.country_wise_units = country_wise_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "business_group", "legal_entity", "division", "country_wise_units"])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        business_group = data.get("business_group")
        business_group = parse_structure_OptionalType_RecordType_techno_master_BUSINESSGROUP(business_group)
        legal_entity = data.get("legal_entity")
        legal_entity = parse_structure_OptionalType_RecordType_techno_master_LEGALENTITY(legal_entity)
        division = data.get("division")
        division = parse_structure_OptionalType_RecordType_techno_master_DIVISION(division)
        country_wise_units = data.get("country_wise_units")
        country_wise_units = parse_structure_VectorType_RecordType_techno_master_COUNTRYWISEUNITS(country_wise_units)
        return SaveClient(client_id, business_group, legal_entity, division, country_wise_units)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "business_group": to_structure_OptionalType_RecordType_core_BusinessGroup(self.business_group),
            "legal_entity": to_structure_RecordType_core_LegalEntity(self.legal_entity),
            "division": to_structure_OptionalType_RecordType_core_Division(self.division),
            "country_wise_units": to_structure_RecordType_core_CountryWiseUnits(self.country_wise_units),
        }

class UpdateClient(Request):
    def __init__(self, client_id, business_group, legal_entity, division, country_wise_units):
        self.client_id = client_id
        self.business_group = business_group
        self.legal_entity = legal_entity
        self.division = division
        self.country_wise_units = country_wise_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "business_group", "legal_entity", "division", "country_wise_units"])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        business_group = data.get("business_group")
        business_group = parse_structure_OptionalType_RecordType_techno_master_BUSINESSGROUP(business_group)
        legal_entity = data.get("legal_entity")
        legal_entity = parse_structure_OptionalType_RecordType_techno_master_LEGALENTITY(legal_entity)
        division = data.get("division")
        division = parse_structure_OptionalType_RecordType_techno_master_DIVISION(division)
        country_wise_units = data.get("country_wise_units")
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


def _init_Request_class_map():
    classes = [GetClientGroups, SaveClientGroup, UpdateClientGroup, ChangeClientGroupStatus, GetClients, SaveClient, UpdateClient, ChangeClientStatus, ReactivateUnit, GetClientProfile]
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

class GetClientGroupsSuccess(Response):
    def __init__(self, countries, domains, users, client_list):
        self.countries = countries
        self.domains = domains
        self.users = users
        self.client_list = client_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "users", "client_list"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_core_User(users)
        client_list = data.get("client_list")
        client_list = parse_structure_VectorType_RecordType_core_GroupCompanyDetail(client_list)
        return GetClientGroupsSuccess(countries, domains, users, client_list)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "users": to_structure_VectorType_RecordType_core_User(self.users),
            "client_list": to_structure_VectorType_RecordType_core_GroupCompanyDetail(self.client_list),
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


class Unit(object):
    def __init__(self, business_group_id, legal_entity_id, division_id, client_id, units, is_active):
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
    def __init__(self, unit_id, geography_id, unit_code, unit_name, industry_id, unit_address, postal_code, domain_ids, is_active):
        self.unit_id = unit_id
        self.geography_id = geography_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.industry_id = industry_id
        self.unit_address = unit_address
        self.postal_code = postal_code
        self.domain_ids = domain_ids
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "geography_id", "unit_code", "unit_name", "industry_id", "unit_address", "postal_code", "domain_ids", "is_active"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_UnsignedIntegerType_32(unit_id)
        geography_id = data.get("geography_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        unit_code = data.get("unit_code")
        unit_code = parse_structure_CustomTextType_20(unit_code)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        industry_id = data.get("industry_id")
        industry_id = parse_structure_UnsignedIntegerType_32(industry_id)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_250(unit_address)
        postal_code = data.get("postal_code")
        postal_code = parse_structure_UnsignedIntegerType_32(postal_code)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return UnitDetails(unit_id, geography_id, unit_code, unit_name, industry_id, unit_address, postal_code, domain_ids, is_active)

    def to_structure(self):
        return {
            "unit_id": to_structure_OptionalType_UnsignedIntegerType_32(self.unit_id),
            "geography_id": to_structure_UnsignedIntegerType_32(self.geography_id),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "postal_code": to_structure_UnsignedIntegerType_32(self.postal_code),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "is_active": to_structure_Bool(self.is_active),
        }





class GetClientsSuccess(Response):
    def __init__(self, countries, domains, group_companies, business_groups, legal_entities, divisions, units, geography_levels, geographies, industries):
        self.countries = countries
        self.domains = domains
        self.group_companies = group_companies
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.geography_levels = geography_levels
        self.geographies = geographies
        self.industries = industries

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "group_companies", "business_groups", "legal_entities", "divisions", "units", "geography_levels", "geographies", "industries"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        group_companies = data.get("group_companies")
        group_companies = parse_structure_VectorType_RecordType_core_GroupCompany(group_companies)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_OptionalType_VectorType_RecordType_core_BusinessGroup(business_groups)
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_LegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_OptionalType_VectorType_RecordType_core_Division(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_technomasters_Unit(units)
        geography_levels = data.get("geography_levels")
        geography_levels = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(geography_levels)
        geographies = data.get("geographies")
        geographies = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_GeographyWithMapping(geographies)
        industries = data.get("industries")
        industries = parse_structure_VectorType_RecordType_core_Industry(industries)
        return GetClientsSuccess(countries, domains, group_companies, business_groups, legal_entities, divisions, units, geography_levels, geographies, industries)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "group_companies": to_structure_VectorType_RecordType_core_GroupCompany(self.group_companies),
            "business_groups": to_structure_OptionalType_VectorType_RecordType_core_BusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_LegalEntity(self.legal_entities),
            "divisions": to_structure_OptionalType_VectorType_RecordType_core_Division(self.divisions),
            "units": to_structure_VectorType_RecordType_technomasters_Unit(self.units),
            "industries": to_structure_VectorType_RecordType_core_Industry(self.industries),
            "geography_levels": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(self.geography_levels),
            "geographies": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_GeographyWithMapping(self.geographies)
        }

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
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UnitCodeAlreadyExists()

    def to_inner_structure(self):
        return {
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
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ReactivateUnitSuccess()

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


def _init_Response_class_map():
    classes = [GetClientGroupsSuccess, SaveClientGroupSuccess, GroupNameAlreadyExists,
    UpdateClientGroupSuccess, ChangeClientGroupStatusSuccess, InvalidClientId,
    GetClientsSuccess, SaveClientSuccess, BusinessGroupNameAlreadyExists,
    LegalEntityNameAlreadyExists, DivisionNameAlreadyExists, UnitNameAlreadyExists,
    UnitCodeAlreadyExists, LogoSizeLimitExceeds, UpdateClientSuccess,
    ChangeClientStatusSuccess, ReactivateUnitSuccess, GetClientProfileSuccess,
    InvalidBusinessGroupId, InvalidLegalEntityId, InvalidDivisionId, 
    InvalidUnitId, UserIsNotResponsibleForAnyClient, ClientCreationFailed]
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
        session_token = parse_structure_CustomTextType_50(session_token)
        request = data.get("request")
        request = parse_structure_VariantType_technomasters_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_technomasters_Request(self.request),
        }

#
# LICENCE_HOLDER_DETAILS
#

class LICENCE_HOLDER_DETAILS(object):
    def __init__(self, user_id, user_name, email_id, contact_no, seating_unit_name, address, total_disk_space, used_disk_space):
        self.user_id = user_id
        self.user_name = user_name
        self.email_id = email_id
        self.contact_no = contact_no
        self.seating_unit_name = seating_unit_name
        self.address = address
        self.total_disk_space = total_disk_space
        self.used_disk_space = used_disk_space

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_name", "email_id", "contact_no", "seating_unit_name", "address", "total_disk_space", "used_disk_space"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        user_name = data.get("user_name")
        user_name = parse_structure_CustomTextType_50(user_name)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        seating_unit_name = data.get("seating_unit_name")
        seating_unit_name = parse_structure_CustomTextType_50(seating_unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        total_disk_space = data.get("total_disk_space")
        total_disk_space = parse_structure_Float(total_disk_space)
        used_disk_space = data.get("used_disk_space")
        used_disk_space = parse_structure_Float(used_disk_space)
        return LICENCE_HOLDER_DETAILS(user_id, user_name, email_id, contact_no, seating_unit_name, address, total_disk_space, used_disk_space)

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "user_name": to_structure_CustomTextType_50(self.user_name),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "seating_unit_name": to_structure_CustomTextType_50(self.seating_unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "total_disk_space": to_structure_Float(self.total_disk_space),
            "used_disk_space": to_structure_Float(self.used_disk_space),
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
            "no_of_user_licence": to_structure_SignedIntegerType_8(self.no_of_user_licence),
            "remaining_licence": to_structure_SignedIntegerType_8(self.remaining_licence),
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

