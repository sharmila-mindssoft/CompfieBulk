
from clientprotocol.jsonvalidators_client import (parse_dictionary, parse_static_list, to_structure_dictionary_values)
from clientprotocol.parse_structure import (
    parse_structure_CustomTextType_100,
    parse_structure_RecordType_core_Menu,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_UserGroup,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_VectorType_RecordType_core_Unit,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_VectorType_RecordType_core_ServiceProvider,
    parse_structure_Bool, parse_structure_CustomIntegerType_1_10,
    parse_structure_CustomTextType_20,
    parse_structure_VectorType_RecordType_core_BusinessGroup,
    parse_structure_VariantType_clientmasters_Request,
    parse_structure_VectorType_RecordType_core_Division,
    parse_structure_CustomTextType_50,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_OptionalType_CustomTextType_250,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_OptionalType_CustomTextType_50
)
from clientprotocol.to_structure import (
    to_structure_CustomTextType_100,
    to_structure_RecordType_core_Menu, to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_ClientUser,
    to_structure_VectorType_RecordType_core_UserGroup,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_VectorType_RecordType_core_Unit,
    to_structure_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_ServiceProvider,
    to_structure_Bool, to_structure_CustomIntegerType_1_10,
    to_structure_CustomTextType_20,
    to_structure_VectorType_RecordType_core_BusinessGroup,
    to_structure_VariantType_clientmasters_Request,
    to_structure_VectorType_RecordType_core_Division,
    to_structure_CustomTextType_50,
    to_structure_VectorType_RecordType_client_masters_ClientUserGroup,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_VectorType_RecordType_core_ServiceProviderDetails,
    to_structure_VectorType_RecordType_core_ClientBusinessGroup,
    to_structure_VectorType_RecordType_core_ClientLegalEntity,
    to_structure_VectorType_RecordType_core_ClientDivision,
    to_structure_VectorType_RecordType_core_ClientUnit,
    to_structure_OptionalType_CustomTextType_250,
    to_structure_UnsignedIntegerType_32,
    to_structure_OptionalType_CustomTextType_50
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

class GetServiceProviders(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetServiceProviders()

    def to_inner_structure(self):
        return {
        }

class SaveServiceProvider(Request):
    def __init__(self, service_provider_name, address, contract_from, contract_to, contact_person, contact_no):
        self.service_provider_name = service_provider_name
        self.address = address
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.contact_person = contact_person
        self.contact_no = contact_no

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "s_name", "add", "c_from", "c_to",
                "c_person", "c_no"
            ]
        )
        service_provider_name = data.get("s_name")
        service_provider_name = parse_structure_CustomTextType_50(service_provider_name)
        address = data.get("add")
        address = parse_structure_OptionalType_CustomTextType_250(address)
        contract_from = data.get("c_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("c_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        contact_person = data.get("c_person")
        contact_person = parse_structure_CustomTextType_50(contact_person)
        contact_no = data.get("c_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        return SaveServiceProvider(
            service_provider_name, address, contract_from, contract_to, contact_person,
            contact_no
        )

    def to_inner_structure(self):
        return {
            "service_provider_name": to_structure_CustomTextType_50(self.service_provider_name),
            "address": to_structure_OptionalType_CustomTextType_250(self.address),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "contact_person": to_structure_CustomTextType_50(self.contact_person),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
        }

class UpdateServiceProvider(Request):
    def __init__(self, service_provider_id, service_provider_name, address, contract_from, contract_to, contact_person, contact_no):
        self.service_provider_id = service_provider_id
        self.service_provider_name = service_provider_name
        self.address = address
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.contact_person = contact_person
        self.contact_no = contact_no

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "s_id", "s_name", "add", "c_from", "c_to", "c_person", "c_no"
            ]
        )
        service_provider_id = data.get("s_id")
        service_provider_id = parse_structure_UnsignedIntegerType_32(service_provider_id)
        service_provider_name = data.get("s_name")
        service_provider_name = parse_structure_CustomTextType_50(service_provider_name)
        address = data.get("add")
        address = parse_structure_OptionalType_CustomTextType_250(address)
        contract_from = data.get("c_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("c_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        contact_person = data.get("c_person")
        contact_person = parse_structure_CustomTextType_50(contact_person)
        contact_no = data.get("c_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        return UpdateServiceProvider(service_provider_id, service_provider_name, address, contract_from, contract_to, contact_person, contact_no)

    def to_inner_structure(self):
        return {
            "service_provider_id": to_structure_SignedIntegerType_8(self.service_provider_id),
            "service_provider_name": to_structure_CustomTextType_50(self.service_provider_name),
            "address": to_structure_CustomTextType_250(self.address),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "contact_person": to_structure_CustomTextType_50(self.contact_person),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
        }

class ChangeServiceProviderStatus(Request):
    def __init__(self, service_provider_id, is_active):
        self.service_provider_id = service_provider_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["s_id", "active"])
        service_provider_id = data.get("s_id")
        service_provider_id = parse_structure_UnsignedIntegerType_32(service_provider_id)
        is_active = data.get("active")
        is_active = parse_structure_Bool(is_active)
        return ChangeServiceProviderStatus(service_provider_id, is_active)

    def to_inner_structure(self):
        return {
            "s_id": to_structure_SignedIntegerType_8(self.service_provider_id),
            "active": to_structure_Bool(self.is_active),
        }

class GetUserPrivileges(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserPrivileges()

    def to_inner_structure(self):
        return {
        }

class SaveUserPrivileges(Request):
    def __init__(self, user_group_name, user_category_id, form_ids):
        self.user_group_name = user_group_name
        self.user_category_id = user_category_id
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_g_name", "u_c_id", "f_ids"])
        user_group_name = data.get("u_g_name")
        form_category_id = data.get("u_c_id")
        form_ids = data.get("f_ids")
        return SaveUserPrivileges(user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "u_g_name": self.user_group_name,
            "u_c_id": self.form_category_id,
            "f_ids": self.form_ids,
        }

class UpdateUserPrivileges(Request):
    def __init__(self, user_group_id, user_category_id, user_group_name, form_ids):
        self.user_group_id = user_group_id
        self.user_category_id = user_category_id
        self.user_group_name = user_group_name
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_g_id", "u_c_id", "u_g_name", "f_ids"])
        user_group_id = data.get("u_g_id")
        form_category_id = data.get("u_c_id")
        user_group_name = data.get("u_g_name")
        form_ids = data.get("f_ids")
        form_ids = form_ids
        return UpdateUserPrivileges(user_group_id, form_category_id, user_group_name, form_ids)

    def to_inner_structure(self):
        return {
            "u_g_id": self.user_group_id,
            "u_c_id": self.form_category_id,
            "u_g_name": self.user_group_name,
            "f_ids": self.form_ids,
        }

class ChangeUserPrivilegeStatus(Request):
    def __init__(self, user_group_id, is_active):
        self.user_group_id = user_group_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_id", "active"])
        user_group_id = data.get("ug_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        is_active = data.get("active")
        is_active = parse_structure_Bool(is_active)
        return ChangeUserPrivilegeStatus(user_group_id, is_active)

    def to_inner_structure(self):
        return {
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "is_active": to_structure_Bool(self.is_active),
        }

class GetClientUsers(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientUsers()

    def to_inner_structure(self):
        return {
        }

class SaveClientUser(Request):
    def __init__(self, email_id, user_group_id, employee_name,
        employee_code, contact_no, seating_unit_id, user_level,
        country_ids, domain_ids, unit_ids, is_service_provider,
        service_provider_id):
        self.email_id = email_id
        self.user_group_id = user_group_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.seating_unit_id = seating_unit_id
        self.user_level = user_level
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.unit_ids = unit_ids
        self.is_service_provider = is_service_provider
        self.service_provider_id = service_provider_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["email", "ug_id", "emp_n", "emp_c", "cn",
            "s_u_id", "ul", "c_ids", "d_ids", "u_ids", "sp", "sp_id"])
        email_id = data.get("email")
        email_id = parse_structure_CustomTextType_100(email_id)
        user_group_id = data.get("ug_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        employee_name = data.get("emp_n")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("emp_c")
        employee_code = parse_structure_OptionalType_CustomTextType_50(employee_code)
        contact_no = data.get("cn")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        seating_unit_id = data.get("s_u_id")
        seating_unit_id = parse_structure_OptionalType_UnsignedIntegerType_32(seating_unit_id)
        user_level = data.get("ul")
        user_level = parse_structure_CustomIntegerType_1_10(user_level)
        country_ids = data.get("c_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("d_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        unit_ids = data.get("u_ids")
        unit_ids = parse_structure_VectorType_SignedIntegerType_8(unit_ids)
        is_service_provider = data.get("sp")
        is_service_provider = parse_structure_Bool(is_service_provider)
        service_provider_id = data.get("sp_id")
        service_provider_id = parse_structure_OptionalType_UnsignedIntegerType_32(service_provider_id)
        return SaveClientUser(email_id, user_group_id, employee_name, employee_code, contact_no, seating_unit_id, user_level, country_ids, domain_ids, unit_ids, is_service_provider, service_provider_id)

    def to_inner_structure(self):
        return {
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_OptionalType_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "seating_unit_id": to_structure_OptionalType_UnsignedIntegerType_32(self.seating_unit_id),
            "user_level": to_structure_CustomIntegerType_1_10(self.user_level),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "unit_ids": to_structure_VectorType_SignedIntegerType_8(self.unit_ids),
            "is_service_provider": to_structure_Bool(self.is_service_provider),
            "service_provider_id": to_structure_OptionalType_UnsignedIntegerType_32(self.service_provider_id),
        }

class UpdateClientUser(Request):
    def __init__(self, user_id, user_group_id, employee_name,
        employee_code, contact_no, seating_unit_id,
        user_level, country_ids, domain_ids, unit_ids, is_service_provider,
        service_provider_id):
        self.user_id = user_id
        self.user_group_id = user_group_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.seating_unit_id = seating_unit_id
        self.user_level = user_level
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.unit_ids = unit_ids
        self.is_service_provider = is_service_provider
        self.service_provider_id = service_provider_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_id", "ug_id",
            "emp_n", "emp_c", "cn", "s_u_id", "ul", "c_ids", "d_ids", "u_ids",
            "sp", "sp_id"])
        user_id = data.get("u_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        user_group_id = data.get("ug_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        employee_name = data.get("emp_n")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("emp_c")
        employee_code = parse_structure_OptionalType_CustomTextType_50(employee_code)
        contact_no = data.get("cn")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        seating_unit_id = data.get("s_u_id")
        seating_unit_id = parse_structure_OptionalType_UnsignedIntegerType_32(seating_unit_id)
        user_level = data.get("ul")
        user_level = parse_structure_CustomIntegerType_1_10(user_level)
        country_ids = data.get("c_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("d_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        unit_ids = data.get("u_ids")
        unit_ids = parse_structure_VectorType_SignedIntegerType_8(unit_ids)
        is_service_provider = data.get("sp")
        is_service_provider = parse_structure_Bool(is_service_provider)
        service_provider_id = data.get("sp_id")
        service_provider_id = parse_structure_OptionalType_UnsignedIntegerType_32(service_provider_id)
        return UpdateClientUser(user_id, user_group_id, employee_name, employee_code, contact_no, seating_unit_id, user_level, country_ids, domain_ids, unit_ids, is_service_provider, service_provider_id)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_OptionalType_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "seating_unit_id": to_structure_OptionalType_UnsignedIntegerType_32(self.seating_unit_id),
            "user_level": to_structure_CustomIntegerType_1_10(self.user_level),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "unit_ids": to_structure_VectorType_SignedIntegerType_8(self.unit_ids),
            "is_service_provider": to_structure_Bool(self.is_service_provider),
            "service_provider_id": to_structure_OptionalType_UnsignedIntegerType_32(self.service_provider_id),
        }

class UpdateClientUserStatus(Request):
    def __init__(self, user_id, is_active):
        self.user_id = user_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_id", "active"])
        user_id = data.get("u_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        is_active = data.get("active")
        is_active = parse_structure_Bool(is_active)
        return UpdateClientUserStatus(user_id, is_active)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "is_active": to_structure_Bool(self.is_active),
        }

class ChangeClientUserStatus(Request):
    def __init__(self, user_id, is_active, employee_name):
        self.user_id = user_id
        self.is_active = is_active
        self.employee_name = employee_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_id", "active", "emp_name"])
        user_id = data.get("u_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        is_active = data.get("active")
        is_active = parse_structure_Bool(is_active)
        employee_name = data.get("emp_name")
        employee_name = parse_structure_CustomTextType_100(employee_name)
        return ChangeClientUserStatus(user_id, is_active, employee_name)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "is_active": to_structure_Bool(self.is_active),
            "employee_name": to_structure_CustomTextType_100(self.employee_name)
        }

class ChangeAdminStatus(Request):
    def __init__(self, user_id, is_admin, employee_name):
        self.user_id = user_id
        self.is_admin = is_admin
        self.employee_name = employee_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_id", "admin", "emp_name"])
        user_id = data.get("u_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        is_admin = data.get("admin")
        is_admin = parse_structure_Bool(is_admin)
        employee_name = data.get("emp_name")
        employee_name = parse_structure_CustomTextType_100(employee_name)
        return ChangeAdminStatus(user_id, is_admin, employee_name)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "is_admin": to_structure_Bool(self.is_admin),
            "employee_name": to_structure_CustomTextType_100(self.employee_name)
        }


class GetUnits(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUnits()

    def to_inner_structure(self):
        return {
        }

class CloseUnit(Request):
    def __init__(self, unit_id, unit_name, password):
        self.unit_id = unit_id
        self.password = password
        self.unit_name = unit_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_id", "pwd", "u_name"])
        unit_id = data.get("u_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        password = data.get("pwd")
        password = parse_structure_CustomTextType_100(password)
        unit_name = data.get("u_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        return CloseUnit(unit_id, unit_name, password)

    def to_inner_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "password": to_structure_CustomTextType_100(self.password),
            "unit_name": to_structure_CustomTextType_100(self.unit_name)
        }

class GetAuditTrails(Request):
    def __init__(self, from_date, to_date, user_id, form_id, record_count, page_count):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id = user_id
        self.form_id = form_id
        self.record_count = record_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["from_date", "to_date", "user_id", "form_id", "record_count"])
        from_date = data.get("from_date")
        from_date = parse_structure_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_CustomTextType_20(to_date)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_UnsignedIntegerType_32(user_id)
        form_id = data.get("form_id")
        form_id = parse_structure_OptionalType_UnsignedIntegerType_32(form_id)
        record_count = data.get("record_count")
        record_count = parse_structure_UnsignedIntegerType_32(record_count)
        page_count = data.get("page_count")
        page_count = parse_structure_UnsignedIntegerType_32(page_count)
        return GetAuditTrails(
            from_date, to_date,
            user_id, form_id,
            record_count, page_count
        )

    def to_inner_structure(self):
        return {
            "from_date": to_structure_CustomTextType_20(self.from_date),
            "to_date": to_structure_CustomTextType_20(self.to_date),
            "user_id": to_structure_OptionalType_UnsignedIntegerType_32(self.user_id),
            "form_id": to_structure_OptionalType_UnsignedIntegerType_32(self.form_id),
            "record_count": to_structure_UnsignedIntegerType_32(self.record_count),
            "page_count": to_structure_UnsignedIntegerType_32(self.page_count)
        }

class GetUnitClosureData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUnitClosureData()

    def to_inner_structure(self):
        return {
        }

class GetUnitClosureUnitData(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entity_id"])
        legal_entity_id = data.get("legal_entity_id")
        return GetUnitClosureUnitData(legal_entity_id)

    def to_inner_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id
        }

class SaveUnitClosureData(Request):
    def __init__(
        self, password, closed_remarks, unit_id, grp_mode
    ):
        self.password = password
        self.closed_remarks = closed_remarks
        self.unit_id = unit_id
        self.grp_mode = grp_mode

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "password", "closed_remarks", "unit_id", "grp_mode"
        ])
        password = data.get("password")
        closed_remarks = data.get("closed_remarks")
        unit_id = data.get("unit_id")
        grp_mode = data.get("grp_mode")

        return SaveUnitClosureData(
            password, closed_remarks, unit_id, grp_mode
        )

    def to_inner_structure(self):
        data = {
            "password": self.password,
            "closed_remarks": self.closed_remarks,
            "unit_id": self.unit_id,
            "grp_mode": self.grp_mode,
        }
        return data

def _init_Request_class_map():
    classes = [
        GetServiceProviders, ChangeClientUserStatus, ChangeAdminStatus,
        SaveServiceProvider, UpdateServiceProvider, ChangeServiceProviderStatus,
        GetUserPrivileges, SaveUserPrivileges, UpdateUserPrivileges,
        ChangeUserPrivilegeStatus, GetClientUsers, SaveClientUser, UpdateClientUser,
        UpdateClientUserStatus, GetUnits, CloseUnit, GetAuditTrails,
        GetUnitClosureData, SaveUnitClosureData, GetUnitClosureUnitData
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

class GetServiceProvidersSuccess(Response):
    def __init__(self, service_providers):
        self.service_providers = service_providers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["service_providers"])
        service_providers = data.get("service_providers")
        service_providers = parse_structure_VectorType_RecordType_core_ServiceProviderDetails(service_providers)
        return GetServiceProvidersSuccess(service_providers)

    def to_inner_structure(self):
        return {
            "service_providers": to_structure_VectorType_RecordType_core_ServiceProviderDetails(self.service_providers),
        }

class SaveServiceProviderSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveServiceProviderSuccess()

    def to_inner_structure(self):
        return {
        }

class ServiceProviderNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ServiceProviderNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class UpdateServiceProviderSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateServiceProviderSuccess()

    def to_inner_structure(self):
        return {
        }

class CannotChangeStatusOfContractExpiredSP(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotChangeStatusOfContractExpiredSP()

    def to_inner_structure(self):
        return {
        }

class ChangeServiceProviderStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeServiceProviderStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class GetUserPrivilegesSuccess(Response):
    def __init__(self, forms, user_groups, user_category):
        self.forms = forms
        self.user_groups = user_groups
        self.user_category = user_category

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["forms", "user_groups", "user_category"])
        forms = data.get("forms")
        forms = forms
        user_groups = data.get("user_groups")
        user_groups = user_groups
        user_category = data.get("user_category")
        user_category = user_category
        return GetUserPrivilegesSuccess(forms, user_groups, user_category)

    def to_inner_structure(self):
        return {
            "forms": self.forms,
            "user_groups": self.user_groups,
            "user_category": self.user_category,
        }

class UserGroupNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UserGroupNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class InvalidUserGroupId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserGroupId()

    def to_inner_structure(self):
        return {
        }

class SaveUserPrivilegesSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserPrivilegesSuccess()

    def to_inner_structure(self):
        return {
        }

class UpdateUserPrivilegesSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserPrivilegesSuccess()

    def to_inner_structure(self):
        return {
        }

class ChangeUserPrivilegeStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeUserPrivilegeStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class ChangeAdminStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeAdminStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class GetClientUsersSuccess(Response):
    def __init__(
        self, user_countries, user_domains, countries, domains, business_groups,
        legal_entities, divisions, units, session_user_units, user_groups, users,
        service_providers, remaining_licence, is_primary_admin
    ):
        self.user_countries = user_countries
        self.user_domains = user_domains
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.session_user_units = session_user_units
        self.user_groups = user_groups
        self.users = users
        self.service_providers = service_providers
        self.remaining_licence = remaining_licence
        self.is_primary_admin = is_primary_admin

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "user_countries", "user_domains", "countries","domains", "business_groups",
	        	"legal_entities", "divisions", "units", "session_user_units"
                "user_groups", "users", "service_providers",
                "remaining_licence", "is_primary_admin"
        	]
       	)
        user_countries = data.get("user_countries")
        user_countries = parse_structure_VectorType_RecordType_core_Country(user_countries)
        user_domains = data.get("user_domains")
        user_domains = parse_structure_VectorType_RecordType_core_Domain(user_domains)
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_VectorType_RecordType_core_BusinessGroup(business_groups)
        legal_entities= data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_LegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_VectorType_RecordType_core_Division(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_Unit(units)
        session_user_units = data.get("session_user_units")
        session_user_units = parse_structure_VectorType_RecordType_core_Unit(session_user_units)
        user_groups = data.get("user_groups")
        user_groups = parse_structure_VectorType_RecordType_core_UserGroup(user_groups)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_core_User(users)
        service_providers = data.get("service_providers")
        service_providers = parse_structure_VectorType_RecordType_core_ServiceProvider(service_providers)
        remaining_licence = data.get("remaining_licence")
        remaining_licence = parse_structure_UnsignedIntegerType_32(remaining_licence)
        is_primary_admin = data.get("is_primary_admin")
        is_primary_admin = parse_structure_Bool(is_primary_admin)
        return GetClientUsersSuccess(
        	user_countries, user_domains, countries,domains, business_groups,
            legal_entities, divisions, units, session_user_units, user_groups,
            users, service_providers, remaining_licence, is_primary_admin
        )

    def to_inner_structure(self):
        return {
            "user_countries" : to_structure_VectorType_RecordType_core_Country(self.user_countries),
            "user_domains" : to_structure_VectorType_RecordType_core_Domain(self.user_domains),
            "countries" : to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains" : to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities" : to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions" : to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units" : to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "session_user_units" : to_structure_VectorType_RecordType_core_ClientUnit(self.session_user_units),
            "user_groups" : to_structure_VectorType_RecordType_core_UserGroup(self.user_groups),
            "users" : to_structure_VectorType_RecordType_core_ClientUser(self.users),
            "service_providers" : to_structure_VectorType_RecordType_core_ServiceProvider(self.service_providers),
            "remaining_licence" : to_structure_UnsignedIntegerType_32(self.remaining_licence),
            "is_primary_admin" : to_structure_Bool(self.is_primary_admin)
        }

class SaveClientUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveClientUserSuccess()

    def to_inner_structure(self):
        return {
        }


class EmailIdAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmailIdAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class EmployeeCodeAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmployeeCodeAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class EmployeeNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmployeeNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class UpdateClientUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateClientUserSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidUserId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserId()

    def to_inner_structure(self):
        return {
        }

class ChangeClientUserStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeClientUserStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class GetUnitsSuccess(Response):
    def __init__(self, business_groups, legal_entities, divisions, units):
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["business_groups", "legal_entities", "divisions", "units"])
        business_groups = data.get("business_groups")
        business_groups = parse_structure_VectorType_RecordType_core_ClientBusinessGroup(business_groups)
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_ClientLegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_VectorType_RecordType_core_ClientDivision(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        return GetUnitsSuccess(business_groups, legal_entities, divisions, units)

    def to_inner_structure(self):
        return {
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
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

class InvalidServiceProviderId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidServiceProviderId()

    def to_inner_structure(self):
        return {
        }

class ReassignCompliancesBeforeDeactivate(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ReassignCompliancesBeforeDeactivate()

    def to_inner_structure(self):
        return {
        }


class CannotChangeOldPrimaryAdminStatus(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotChangeOldPrimaryAdminStatus()

    def to_inner_structure(self):
        return {
        }


class CannotChangePrimaryAdminStatus(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotChangePrimaryAdminStatus()

    def to_inner_structure(self):
        return {
        }


class CannotPromoteServiceProvider(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotChangePrimaryAdminStatus()

    def to_inner_structure(self):
        return {
        }


class CloseUnitSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CloseUnitSuccess()

    def to_inner_structure(self):
        return {
        }


class ContactNumberAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ContactNumberAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class CannotDeactivateUserExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotDeactivateUserExists()

    def to_inner_structure(self):
        return {
        }

class GetAuditTrailSuccess(Response):
    def __init__(self, audit_trails):
        self.audit_trails = audit_trails

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["audit_trails"])
        audit_trails = data.get("audit_trails")
        audit_trails = parse_structure_VectorType_RecordType_general_AuditTrail(audit_trails)
        return GetAuditTrailSuccess(audit_trails)

    def to_inner_structure(self):
        return {
            "audit_trail_details": to_structure_VectorType_RecordType_general_AuditTrail(self.audit_trails),
        }

class UserLimitExceeds(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UserLimitExceeds()

    def to_inner_structure(self):
        return {
        }

class CannotCloseUnit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotCloseUnit()

    def to_inner_structure(self):
        return {
        }

class GetUnitClosureDataSuccess(Response):
    def __init__(self, unit_closure_legal_entities):
        self.unit_closure_legal_entities = unit_closure_legal_entities

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_closure_legal_entities"])
        unit_closure_legal_entities = data.get("unit_closure_legal_entities")
        return GetUnitClosureDataSuccess(unit_closure_legal_entities)

    def to_inner_structure(self):
        return {
            "unit_closure_legal_entities": self.unit_closure_legal_entities,
        }

class GetUnitClosureUnitDataSuccess(Response):
    def __init__(self, unit_closure_units):
        self.unit_closure_units = unit_closure_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_closure_units"])
        unit_closure_units = data.get("unit_closure_units")
        return GetUnitClosureUnitDataSuccess(unit_closure_units)

    def to_inner_structure(self):
        return {
            "unit_closure_units": self.unit_closure_units,
        }

class SaveUnitClosureSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUnitClosureSuccess()

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

def _init_Response_class_map():
    classes = [
        GetServiceProvidersSuccess, SaveServiceProviderSuccess,
        ServiceProviderNameAlreadyExists, UpdateServiceProviderSuccess,
        ChangeServiceProviderStatusSuccess, GetUserPrivilegesSuccess,
        UserGroupNameAlreadyExists, InvalidUserGroupId, SaveUserPrivilegesSuccess,
        UpdateUserPrivilegesSuccess, ChangeUserPrivilegeStatusSuccess,
        GetClientUsersSuccess, SaveClientUserSuccess, EmployeeCodeAlreadyExists,
        EmployeeNameAlreadyExists, CannotChangeOldPrimaryAdminStatus,
        UpdateClientUserSuccess, InvalidUserId, ChangeClientUserStatusSuccess,
        ChangeAdminStatusSuccess, GetAuditTrailSuccess, CannotDeactivateUserExists,
        GetUnitsSuccess, InvalidPassword, CloseUnitSuccess, ContactNumberAlreadyExists,
        InvalidServiceProviderId, EmailIdAlreadyExists, CannotChangePrimaryAdminStatus ,
        CannotPromoteServiceProvider, ReassignCompliancesBeforeDeactivate,
        CannotChangeStatusOfContractExpiredSP, CannotCloseUnit, GetUnitClosureUnitDataSuccess,
        GetUnitClosureDataSuccess, SaveUnitClosureSuccess, InvalidUnitId
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

#
# Audit Trail
#
class AuditTrail(object):
    def __init__(self, user_id, form_id, action, date):
        self.user_id = user_id
        self.form_id = form_id
        self.action = action
        self.date = date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "form_id", "action", "date"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        form_id = data.get("form_id")
        form_id = parse_structure_UnsignedIntegerType_32(form_id)
        action = data.get("action")
        action = parse_structure_CustomTextType_500(action)
        date = data.get("date")
        date = parse_structure_CustomTextType_20(date)
        return AuditTrail(user_id, form_id, action, date)

    def to_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "form_id": to_structure_UnsignedIntegerType_32(self.form_id),
            "action": to_structure_CustomTextType_500(self.action),
            "date": to_structure_CustomTextType_20(self.date)
        }



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
        request = parse_structure_VariantType_clientmasters_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_clientmasters_Request(self.request),
        }
