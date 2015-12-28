import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_RecordType_core_Division,
    parse_structure_VectorType_RecordType_core_GroupCompany,
    parse_structure_SignedIntegerType_8, parse_structure_Bool,
    parse_structure_VectorType_RecordType_core_BusinessGroup,
    parse_structure_RecordType_core_CountryWiseUnits,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_RecordType_core_BusinessGroup,
    parse_structure_VectorType_RecordType_core_UnitDetails,
    parse_structure_VectorType_RecordType_technomasters_PROFILES,
    parse_structure_RecordType_core_LegalEntity,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_User,
    parse_structure_VectorType_RecordType_core_Division,
    parse_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_ClientConfiguration,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_RecordType_technomasters_PROFILE_DETAIL,
    parse_structure_CustomTextType_50,
    parse_structure_VariantType_technomasters_Request,
    parse_structure_CustomTextType_20,
    parse_structure_VectorType_RecordType_core_GroupCompanyDetail
)
from protocol.to_structure import (
    to_structure_RecordType_core_Division,
    to_structure_VectorType_RecordType_core_GroupCompany,
    to_structure_SignedIntegerType_8, to_structure_Bool,
    to_structure_VectorType_RecordType_core_BusinessGroup,
    to_structure_RecordType_core_CountryWiseUnits,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_RecordType_core_BusinessGroup,
    to_structure_VectorType_RecordType_core_UnitDetails,
    to_structure_VectorType_RecordType_technomasters_PROFILES,
    to_structure_RecordType_core_LegalEntity,
    to_structure_CustomTextType_100,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_User,
    to_structure_VectorType_RecordType_core_Division,
    to_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_ClientConfiguration,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_RecordType_technomasters_PROFILE_DETAIL,
    to_structure_CustomTextType_50,
    to_structure_VariantType_technomasters_Request,
    to_structure_CustomTextType_20,
    to_structure_VectorType_RecordType_core_GroupCompanyDetail
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
    def __init__(self, group_name, country_ids, domain_ids, logo, contract_from, contract_to, incharge_persons, no_of_user_licence, file_space, is_sms_subscribed, email_id, DATE_configurations):
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
        self.DATE_configurations = DATE_configurations

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["group_name", "country_ids", "domain_ids", "logo", "contract_from", "contract_to", "incharge_persons", "no_of_user_licence", "file_space", "is_sms_subscribed", "email_id", "DATE_configurations"])
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_RecordType_core_Country(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_RecordType_core_Domain(domain_ids)
        logo = data.get("logo")
        logo = parse_structure_CustomTextType_250(logo)
        contract_from = data.get("contract_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("contract_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        incharge_persons = data.get("incharge_persons")
        incharge_persons = parse_structure_VectorType_SignedIntegerType_8(incharge_persons)
        no_of_user_licence = data.get("no_of_user_licence")
        no_of_user_licence = parse_structure_SignedIntegerType_8(no_of_user_licence)
        file_space = data.get("file_space")
        file_space = parse_structure_SignedIntegerType_8(file_space)
        is_sms_subscribed = data.get("is_sms_subscribed")
        is_sms_subscribed = parse_structure_Bool(is_sms_subscribed)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        DATE_configurations = data.get("DATE_configurations")
        DATE_configurations = parse_structure_VectorType_RecordType_core_ClientConfiguration(DATE_configurations)
        return SaveClientGroup(group_name, country_ids, domain_ids, logo, contract_from, contract_to, incharge_persons, no_of_user_licence, file_space, is_sms_subscribed, email_id, DATE_configurations)

    def to_inner_structure(self):
        return {
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "country_ids": to_structure_VectorType_RecordType_core_Country(self.country_ids),
            "domain_ids": to_structure_VectorType_RecordType_core_Domain(self.domain_ids),
            "logo": to_structure_CustomTextType_250(self.logo),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "incharge_persons": to_structure_VectorType_SignedIntegerType_8(self.incharge_persons),
            "no_of_user_licence": to_structure_SignedIntegerType_8(self.no_of_user_licence),
            "file_space": to_structure_SignedIntegerType_8(self.file_space),
            "is_sms_subscribed": to_structure_Bool(self.is_sms_subscribed),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "DATE_configurations": to_structure_VectorType_RecordType_core_ClientConfiguration(self.DATE_configurations),
        }

class UpdateClientGroup(Request):
    def __init__(self, client_id, group_name, country_ids, domain_ids, logo, contract_from, contract_to, incharge_persons, no_of_user_licence, file_space, is_sms_subscribed, email_id, DATE_configurations):
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
        self.email_id = email_id
        self.DATE_configurations = DATE_configurations

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "group_name", "country_ids", "domain_ids", "logo", "contract_from", "contract_to", "incharge_persons", "no_of_user_licence", "file_space", "is_sms_subscribed", "email_id", "DATE_configurations"])
        client_id = data.get("client_id")
        client_id = parse_structure_SignedIntegerType_8(client_id)
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_RecordType_core_Country(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_RecordType_core_Domain(domain_ids)
        logo = data.get("logo")
        logo = parse_structure_CustomTextType_250(logo)
        contract_from = data.get("contract_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("contract_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        incharge_persons = data.get("incharge_persons")
        incharge_persons = parse_structure_VectorType_SignedIntegerType_8(incharge_persons)
        no_of_user_licence = data.get("no_of_user_licence")
        no_of_user_licence = parse_structure_SignedIntegerType_8(no_of_user_licence)
        file_space = data.get("file_space")
        file_space = parse_structure_SignedIntegerType_8(file_space)
        is_sms_subscribed = data.get("is_sms_subscribed")
        is_sms_subscribed = parse_structure_Bool(is_sms_subscribed)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        DATE_configurations = data.get("DATE_configurations")
        DATE_configurations = parse_structure_VectorType_RecordType_core_ClientConfiguration(DATE_configurations)
        return UpdateClientGroup(client_id, group_name, country_ids, domain_ids, logo, contract_from, contract_to, incharge_persons, no_of_user_licence, file_space, is_sms_subscribed, email_id, DATE_configurations)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "country_ids": to_structure_VectorType_RecordType_core_Country(self.country_ids),
            "domain_ids": to_structure_VectorType_RecordType_core_Domain(self.domain_ids),
            "logo": to_structure_CustomTextType_250(self.logo),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "incharge_persons": to_structure_VectorType_SignedIntegerType_8(self.incharge_persons),
            "no_of_user_licence": to_structure_SignedIntegerType_8(self.no_of_user_licence),
            "file_space": to_structure_SignedIntegerType_8(self.file_space),
            "is_sms_subscribed": to_structure_Bool(self.is_sms_subscribed),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "DATE_configurations": to_structure_VectorType_RecordType_core_ClientConfiguration(self.DATE_configurations),
        }

class ChangeClientGroupStatus(Request):
    def __init__(self, client_id, is_active):
        self.client_id = client_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "is_active"])
        client_id = data.get("client_id")
        client_id = parse_structure_SignedIntegerType_8(client_id)
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
        client_id = parse_structure_SignedIntegerType_8(client_id)
        business_group = data.get("business_group")
        business_group = parse_structure_RecordType_core_BusinessGroup(business_group)
        legal_entity = data.get("legal_entity")
        legal_entity = parse_structure_RecordType_core_LegalEntity(legal_entity)
        division = data.get("division")
        division = parse_structure_RecordType_core_Division(division)
        country_wise_units = data.get("country_wise_units")
        country_wise_units = parse_structure_RecordType_core_CountryWiseUnits(country_wise_units)
        return SaveClient(client_id, business_group, legal_entity, division, country_wise_units)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "business_group": to_structure_RecordType_core_BusinessGroup(self.business_group),
            "legal_entity": to_structure_RecordType_core_LegalEntity(self.legal_entity),
            "division": to_structure_RecordType_core_Division(self.division),
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
        client_id = parse_structure_SignedIntegerType_8(client_id)
        business_group = data.get("business_group")
        business_group = parse_structure_RecordType_core_BusinessGroup(business_group)
        legal_entity = data.get("legal_entity")
        legal_entity = parse_structure_RecordType_core_LegalEntity(legal_entity)
        division = data.get("division")
        division = parse_structure_RecordType_core_Division(division)
        country_wise_units = data.get("country_wise_units")
        country_wise_units = parse_structure_RecordType_core_CountryWiseUnits(country_wise_units)
        return UpdateClient(client_id, business_group, legal_entity, division, country_wise_units)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "business_group": to_structure_RecordType_core_BusinessGroup(self.business_group),
            "legal_entity": to_structure_RecordType_core_LegalEntity(self.legal_entity),
            "division": to_structure_RecordType_core_Division(self.division),
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
        client_id = parse_structure_SignedIntegerType_8(client_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_SignedIntegerType_8(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_SignedIntegerType_8(division_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeClientStatus(client_id, legal_entity_id, division_id, is_active)

    def to_inner_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_SignedIntegerType_8(self.division_id),
            "is_active": to_structure_Bool(self.is_active),
        }

class ReactivateUnit(Request):
    def __init__(self, unit_id, passsword):
        self.unit_id = unit_id
        self.passsword = passsword

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_id", "passsword"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_SignedIntegerType_8(unit_id)
        passsword = data.get("passsword")
        passsword = parse_structure_CustomTextType_20(passsword)
        return ReactivateUnit(unit_id, passsword)

    def to_inner_structure(self):
        return {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "passsword": to_structure_CustomTextType_20(self.passsword),
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

class GetClientsSuccess(Response):
    def __init__(self, countries, domains, group_companies, business_groups, legal_entities, divisions, units):
        self.countries = countries
        self.domains = domains
        self.group_companies = group_companies
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "group_companies", "business_groups", "legal_entities", "divisions", "units"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        group_companies = data.get("group_companies")
        group_companies = parse_structure_VectorType_RecordType_core_GroupCompany(group_companies)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_VectorType_RecordType_core_BusinessGroup(business_groups)
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_LegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_VectorType_RecordType_core_Division(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_UnitDetails(units)
        return GetClientsSuccess(countries, domains, group_companies, business_groups, legal_entities, divisions, units)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "group_companies": to_structure_VectorType_RecordType_core_GroupCompany(self.group_companies),
            "business_groups": to_structure_VectorType_RecordType_core_BusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_LegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_Division(self.divisions),
            "units": to_structure_VectorType_RecordType_core_UnitDetails(self.units),
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
    classes = [GetClientGroupsSuccess, SaveClientGroupSuccess, GroupNameAlreadyExists, UpdateClientGroupSuccess, ChangeClientGroupStatusSuccess, InvalidClientId, GetClientsSuccess, SaveClientSuccess, BusinessGroupNameAlreadyExists, LegalEntityNameAlreadyExists, DivisionNameAlreadyExists, UnitNameAlreadyExists, UnitCodeAlreadyExists, LogoSizeLimitExceeds, UpdateClientSuccess, ChangeClientStatusSuccess, ReactivateUnitSuccess, GetClientProfileSuccess]
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
        user_id = parse_structure_SignedIntegerType_8(user_id)
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
        total_disk_space = parse_structure_SignedIntegerType_8(total_disk_space)
        used_disk_space = data.get("used_disk_space")
        used_disk_space = parse_structure_SignedIntegerType_8(used_disk_space)
        return LICENCE_HOLDER_DETAILS(user_id, user_name, email_id, contact_no, seating_unit_name, address, total_disk_space, used_disk_space)

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "user_name": to_structure_CustomTextType_50(self.user_name),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "seating_unit_name": to_structure_CustomTextType_50(self.seating_unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "total_disk_space": to_structure_SignedIntegerType_8(self.total_disk_space),
            "used_disk_space": to_structure_SignedIntegerType_8(self.used_disk_space),
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
        no_of_user_licence = parse_structure_SignedIntegerType_8(no_of_user_licence)
        remaining_licence = data.get("remaining_licence")
        remaining_licence = parse_structure_SignedIntegerType_8(remaining_licence)
        total_disk_space = data.get("total_disk_space")
        total_disk_space = parse_structure_SignedIntegerType_8(total_disk_space)
        used_disk_space = data.get("used_disk_space")
        used_disk_space = parse_structure_SignedIntegerType_8(used_disk_space)
        licence_holders = data.get("licence_holders")
        licence_holders = parse_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS(licence_holders)
        return PROFILE_DETAIL(contract_from, contract_to, no_of_user_licence, remaining_licence, total_disk_space, used_disk_space, licence_holders)

    def to_structure(self):
        return {
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "no_of_user_licence": to_structure_SignedIntegerType_8(self.no_of_user_licence),
            "remaining_licence": to_structure_SignedIntegerType_8(self.remaining_licence),
            "total_disk_space": to_structure_SignedIntegerType_8(self.total_disk_space),
            "used_disk_space": to_structure_SignedIntegerType_8(self.used_disk_space),
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
        client_id = parse_structure_SignedIntegerType_8(client_id)
        profile_detail = data.get("profile_detail")
        profile_detail = parse_structure_RecordType_technomasters_PROFILE_DETAIL(profile_detail)
        return PROFILES(client_id, profile_detail)

    def to_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "profile_detail": to_structure_RecordType_technomasters_PROFILE_DETAIL(self.profile_detail),
        }

