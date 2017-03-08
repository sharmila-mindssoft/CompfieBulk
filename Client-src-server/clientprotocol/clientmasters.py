
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
#############################################################
# Save Service Provider Details
#############################################################
class SaveServiceProvider(Request):
    def __init__(self, service_provider_name, short_name, contract_from, contract_to, contact_person,
    contact_no, mobile_no, email_id, address):
        self.service_provider_name = service_provider_name
        self.short_name = short_name
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.contact_person = contact_person
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.email_id = email_id
        self.address = address

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "s_p_name", "s_p_short", "cont_from", "cont_to", "cont_person", "cont_no", "mob_no", "e_id", "address"
                ]
        )
        service_provider_name = data.get("s_p_name")
        short_name = data.get("s_p_short")
        contract_from = data.get("cont_from")
        contract_to = data.get("cont_to")
        contact_person = data.get("cont_person")
        contact_no = data.get("cont_no")
        mobile_no = data.get("mob_no")
        email_id = data.get("e_id")
        address = data.get("address")
        return SaveServiceProvider(
            service_provider_name, short_name, contract_from, contract_to, contact_person,
            contact_no, mobile_no, email_id, address
        )

    def to_inner_structure(self):
        return {
            "service_provider_name": self.service_provider_name,
            "short_name": self.short_name,
            "contact_person": self.contact_person,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "contact_no": self.contact_no,
            "mobile_no": self.mobile_no,
            "email_id": self.email_id,
            "address": self.address,
        }
#############################################################
# Update Service Provider Details
#############################################################
class UpdateServiceProvider(Request):
    def __init__(self, service_provider_id, service_provider_name, short_name, contract_from,
    contract_to, contact_person, contact_no, mobile_no, email_id, address):
        self.service_provider_id = service_provider_id
        self.service_provider_name = service_provider_name
        self.short_name = short_name
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.contact_person = contact_person
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.email_id = email_id
        self.address = address

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "s_p_id", "s_p_name", "s_p_short", "cont_from", "cont_to", "cont_person", "cont_no", "mob_no", "e_id", "address"
            ]
        )
        service_provider_id = data.get("s_p_id")
        service_provider_name = data.get("s_p_name")
        short_name = data.get("s_p_short")
        contract_from = data.get("cont_from")
        contract_to = data.get("cont_to")
        contact_person = data.get("cont_person")
        contact_no = data.get("cont_no")
        mobile_no = data.get("mob_no")
        email_id = data.get("e_id")
        address = data.get("address")

        return UpdateServiceProvider(
            service_provider_id, service_provider_name, short_name, contract_from, contract_to, contact_person,
            contact_no, mobile_no, email_id, address
        )

    def to_inner_structure(self):
        return {
            "service_provider_id": self.service_provider_id,
            "service_provider_name": self.service_provider_name,
            "short_name": self.short_name,
            "contact_person": self.contact_person,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "contact_no": self.contact_no,
            "mobile_no": self.mobile_no,
            "email_id": self.email_id,
            "address": self.address,
        }
##################################################
# Change Service Provider Status
##################################################
class ChangeServiceProviderStatus(Request):
    def __init__(self, service_provider_id, is_active, password):
        self.service_provider_id = service_provider_id
        self.is_active = is_active
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_id", "active_status", "password"])
        service_provider_id = data.get("sp_id")
        is_active = data.get("active_status")
        password = data.get("password")
        return ChangeServiceProviderStatus(service_provider_id, is_active, password)

    def to_inner_structure(self):
        return {
            "sp_id": self.service_provider_id,
            "active_status": self.is_active,
            "password": self.password,
        }
#################################################
# Block Service Provider Status
##################################################
class BlockServiceProvider(Request):
    def __init__(self, service_provider_id, is_blocked, password):
        self.service_provider_id = service_provider_id
        self.is_blocked = is_blocked
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_id", "is_blocked", "password"])
        service_provider_id = data.get("sp_id")
        is_blocked = data.get("is_blocked")
        password = data.get("password")
        return BlockServiceProvider(service_provider_id, is_blocked, password)

    def to_inner_structure(self):
        return {
            "sp_id": self.service_provider_id,
            "is_blocked": self.is_blocked,
            "password": self.password,
        }

########################################################
# Get User Management List - Create users
########################################################
class UserManagementPrerequisite(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UserManagementPrerequisite()

    def to_inner_structure(self):
        return {
        }
########################################################
# Get User Management List - Get users list
########################################################
class UserManagementList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UserManagementList()

    def to_inner_structure(self):
        return {
        }

########################################################
# User Management - Edit View
########################################################
class UserManagementEditView(Request):
    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id"])
        user_id = data.get("user_id")
        return UserManagementEditView(user_id)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
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
    def __init__(self, user_group_id, is_active, password):
        self.user_group_id = user_group_id
        self.is_active = is_active
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_g_id", "is_active", "password"])
        user_group_id = data.get("u_g_id")
        is_active = data.get("is_active")
        password = data.get("password")
        return ChangeUserPrivilegeStatus(user_group_id, is_active, password)

    def to_inner_structure(self):
        return {
            "u_g_id": self.user_group_id,
            "is_active": self.is_active,
            "password": self.password,
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
###########################################################################
# User Management - Get User Details
###########################################################################
class get_user_management_details(Request):
    def __init__(
        self, c_id, legal_entity_id, d_id, csv
    ):
        self.c_id = c_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "le_id", "d_id", "csv"]
        )
        c_id = data.get("c_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        csv = data.get("csv")
        return GetWorkFlowScoreCard(
            c_id, legal_entity_id, d_id, csv)

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "csv": self.csv
        }
# -----------------------------------------------------------------------------------------------------------------
# Save Client Users
class SaveClientUser(Request):
    def __init__(self, user_category, user_group_id, email_id, employee_name,
        employee_code, contact_no, mobile_no, user_level, seating_unit_id,
        is_service_provider, service_provider_id, user_domain_ids, user_unit_ids,
        user_entity_ids):
        self.user_category = user_category
        self.user_group_id = user_group_id
        self.email_id = email_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.user_level = user_level
        self.seating_unit_id = seating_unit_id
        self.is_service_provider = is_service_provider
        self.service_provider_id = service_provider_id
        self.user_domain_ids = user_domain_ids
        self.user_unit_ids =user_unit_ids
        self.user_entity_ids =user_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_cat_id", "u_g_id", "email_id", "emp_name", "emp_code",
        "cont_no", "mob_no", "u_level", "s_unit", "is_sp", "sp_id", "user_domain_ids", "user_unit_ids", "user_entity_ids"])
        user_category = data.get("u_cat_id")
        user_group_id = data.get("u_g_id")
        email_id = data.get("email_id")
        employee_name = data.get("emp_name")
        employee_code = data.get("emp_code")
        contact_no = data.get("cont_no")
        mobile_no = data.get("mob_no")
        user_level = data.get("u_level")
        seating_unit_id = data.get("s_unit")
        is_service_provider = data.get("is_sp")
        service_provider_id = data.get("sp_id")
        user_domain_ids = data.get("user_domain_ids")
        user_unit_ids = data.get("user_unit_ids")
        user_entity_ids = data.get("user_entity_ids")

        return SaveClientUser(user_category, user_group_id, email_id, employee_name, employee_code, contact_no, mobile_no, user_level,
                              seating_unit_id, is_service_provider, service_provider_id, user_domain_ids, user_unit_ids, user_entity_ids)

    def to_inner_structure(self):
        return {
            "user_category" : self.user_category,
            "user_group_id" : self.user_group_id,
            "email_id" : self.email_id,
            "employee_name" : self.employee_name,
            "employee_code" : self.employee_code,
            "contact_no" : self.contact_no,
            "mobile_no" : self.mobile_no,
            "user_level" : self.user_level,
            "seating_unit_id" : self.seating_unit_id,
            "is_service_provider" : self.is_service_provider,
            "service_provider_id" : self.service_provider_id,
            "user_domain_ids" : self.user_domain_ids,
            "user_unit_ids" : self.user_unit_ids,
            "user_entity_ids" : self.user_entity_ids,
        }
# --------------------------------------------------------------------------------------------------
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

class GetServiceProviderDetailsReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetServiceProviderDetailsReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetServiceProviderDetailsReport(Request):
    def __init__(self, sp_id, user_id, s_p_status, from_count, page_count):
        self.sp_id = sp_id
        self.user_id = user_id
        self.s_p_status = s_p_status
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_id", "user_id", "s_p_status", "from_count", "page_count"])
        sp_id = data.get("sp_id")
        user_id = data.get("user_id")
        s_p_status = data.get("s_p_status")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetServiceProviderDetailsReport(sp_id, user_id, s_p_status, from_count, page_count)

    def to_inner_structure(self):
        return {
            "sp_id": self.sp_id,
            "user_id": self.user_id,
            "s_p_status": self.s_p_status,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetAuditTrailReportFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entity_id"])
        legal_entity_id = data.get("legal_entity_id")
        return GetAuditTrailReportFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id
        }

class GetLogintraceReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetLogintraceReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetLoginTraceReportData(Request):
    def __init__(
        self, user_id, due_from_date, due_to_date, csv, from_count, page_count
    ):
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_id", "due_from_date", "due_to_date", "csv", "from_count", "page_count"
        ])
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetLoginTraceReportData(
            user_id, due_from_date, due_to_date, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetUserProfile(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserProfile()

    def to_inner_structure(self):
        return {
        }

class UpdateUserProfile(Request):
    def __init__(self, user_id, email_id, con_no, mob_no, address, emp_code, emp_name):
        self.user_id = user_id
        self.email_id = email_id
        self.con_no = con_no
        self.mob_no = mob_no
        self.address = address
        self.emp_code = emp_code
        self.emp_name = emp_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_id", "email_id", "con_no", "mob_no", "address", "emp_code", "emp_name"
        ])
        user_id = data.get("user_id")
        email_id = data.get("email_id")
        con_no = data.get("con_no")
        mob_no = data.get("mob_no")
        address = data.get("address")
        emp_code = data.get("emp_code")
        emp_name = data.get("emp_name")
        return UpdateUserProfile(user_id, email_id, con_no, mob_no, address, emp_code, emp_name)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "email_id": self.email_id,
            "con_no": self.con_no,
            "mob_no": self.mob_no,
            "address": self.address,
            "emp_code": self.emp_code,
            "emp_name": self.emp_name
        }

class GetSettingsFormDetails(Request):
    def __init__(self, le_id):
        self.le_id = le_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        le_id = data.get("le_id")

        return GetSettingsFormDetails(le_id)

    def to_inner_structure(self):
        return {
            "le_id": self.le_id
        }

class SaveSettingsFormDetails(Request):
    def __init__(
        self, le_id, legal_entity_name, two_level_approve, assignee_reminder, advance_escalation_reminder,
        escalation_reminder, reassign_sp
    ):
        self.le_id = le_id
        self.legal_entity_name = legal_entity_name
        self.two_level_approve = two_level_approve
        self.assignee_reminder = assignee_reminder
        self.advance_escalation_reminder = advance_escalation_reminder
        self.escalation_reminder = escalation_reminder
        self.reassign_sp = reassign_sp

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_id", "legal_entity_name", "two_level_approve", "assignee_reminder", "advance_escalation_reminder",
            "escalation_reminder", "reassign_sp"
        ])
        le_id = data.get("le_id")
        legal_entity_name = data.get("legal_entity_name")
        two_level_approve = data.get("two_level_approve")
        assignee_reminder = data.get("assignee_reminder")
        advance_escalation_reminder = data.get("advance_escalation_reminder")
        escalation_reminder = data.get("escalation_reminder")
        reassign_sp = data.get("reassign_sp")
        return SaveSettingsFormDetails(
            le_id, legal_entity_name, two_level_approve, assignee_reminder, advance_escalation_reminder,
            escalation_reminder, reassign_sp
        )

    def to_inner_structure(self):
        return {
            "le_id": self.le_id,
            "legal_entity_name": self.legal_entity_name,
            "two_level_approve": self.two_level_approve,
            "assignee_reminder": self.assignee_reminder,
            "advance_escalation_reminder": self.advance_escalation_reminder,
            "escalation_reminder": self.escalation_reminder,
            "reassign_sp": self.reassign_sp
        }

def _init_Request_class_map():
    classes = [
        GetServiceProviders, ChangeClientUserStatus, ChangeAdminStatus,
        SaveServiceProvider, UpdateServiceProvider, ChangeServiceProviderStatus,
        GetUserPrivileges, SaveUserPrivileges, UpdateUserPrivileges,
        ChangeUserPrivilegeStatus, GetClientUsers, SaveClientUser, UpdateClientUser,
        UpdateClientUserStatus, GetUnits, CloseUnit, GetAuditTrails,
        GetUnitClosureData, SaveUnitClosureData, GetUnitClosureUnitData,
        UserManagementPrerequisite,
        GetServiceProviderDetailsReportFilters, GetServiceProviderDetailsReport,
        GetAuditTrailReportFilters, GetLogintraceReportFilters, GetLoginTraceReportData,
        GetUserProfile, UpdateUserProfile, UserManagementList, GetSettingsFormDetails,
        SaveSettingsFormDetails, BlockServiceProvider, UserManagementEditView
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

        return GetServiceProvidersSuccess(service_providers)

    def to_inner_structure(self):
        return {
            "service_providers": self.service_providers,
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
#################################################################
# Service Provider Short Name + Service Provider Name Exists
#################################################################
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
##############################################################################
# User Management Add - Prerequisite
##############################################################################
class BlockServiceProviderSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return BlockServiceProviderSuccess()

    def to_inner_structure(self):
        return {
        }
##############################################################################
# User Management Add - Prerequisite
##############################################################################
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
##############################################################################
# User Management Add - Prerequisite
##############################################################################
class GetUserManagementPrerequisiteSuccess(Response):
    def __init__(self, user_category, user_group, business_group,
                 legal_entity, group_division, group_category,
                 legal_Domains, legal_units, service_providers):
        self.user_category = user_category
        self.user_group = user_group
        self.business_group = business_group
        self.legal_entity = legal_entity
        self.group_division = group_division
        self.group_category = group_category
        self.legal_Domains = legal_Domains
        self.legal_units = legal_units
        self.service_providers = service_providers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["um_user_category", "um_user_group",
                                       "um_business_group", "um_legal_entity",
                                       "um_group_division", "um_group_category",
                                       "um_legal_domain", "um_legal_units",
                                       "um_service_providers"])
        user_category = data.get("um_user_category")
        user_group = data.get("um_user_group")
        business_group = data.get("um_business_group")
        legal_entity = data.get("um_legal_entity")
        group_division = data.get("um_group_division")
        group_category = data.get("um_group_category")
        legal_Domains = data.get("um_legal_domain")
        legal_units = data.get("um_legal_units")
        service_providers = data.get("um_service_providers")

        user_category = user_category
        user_group = user_group
        business_group = business_group
        legal_entity = legal_entity
        group_division = group_division
        group_category = group_category
        legal_Domains = legal_Domains
        legal_units = legal_units
        service_providers = service_providers
        return GetUserManagementPrerequisiteSuccess(user_category, user_group,
                                                    business_group, legal_entity,
                                                    group_division, group_category,
                                                    legal_Domains, legal_units, service_providers)

    def to_inner_structure(self):
        return {
            "um_user_category": self.user_category,
            "um_user_group": self.user_group,
            "um_business_group": self.business_group,
            "um_legal_entity": self.legal_entity,
            "um_group_division": self.group_division,
            "um_group_category": self.group_category,
            "um_legal_domain": self.legal_Domains,
            "um_legal_units": self.legal_units,
            "um_service_providers": self.service_providers
        }

##############################################################################
# User Management Add - List Users
##############################################################################
class UserManagementListSuccess(Response):
    def __init__(self, legal_entities, users):
        self.legal_entities = legal_entities
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ul_legal_entity", "ul_users"])
        legal_entities = data.get("ul_legal_entity")
        users = data.get("ul_users")

        legal_entities = legal_entities
        users = users
        return UserManagementListSuccess(legal_entities, users)

    def to_inner_structure(self):
        return {
            "ul_legal_entity": self.legal_entities,
            "ul_users": self.users
        }

##############################################################################
# User Management Add - List Users
##############################################################################
class UserManagementEditViewSuccess(Response):
    def __init__(self, users, legal_entities, domains, units):
        self.users = users
        self.legal_entities = legal_entities
        self.domains = domains
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ul_userDetails","ul_legal_entities", "ul_user_domains", "ul_user_units"])
        users = data.get("ul_userDetails")
        legal_entities = data.get("ul_legal_entities")
        domains = data.get("ul_user_domains")
        units = data.get("ul_user_units")

        users = users
        legal_entities = legal_entities
        return UserManagementEditViewSuccess(users, legal_entities, domains, units)

    def to_inner_structure(self):
        return {
            "ul_userDetails": self.users,
            "ul_legal_entities": self.legal_entities,
            "ul_user_domains": self.domains,
            "ul_user_units": self.units
        }
##############################################################################
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

class GetServiceProviderDetailsFilterSuccess(Response):
    def __init__(self, sp_list, sp_user_list, sp_status_list):
        self.sp_list = sp_list
        self.sp_user_list = sp_user_list
        self.sp_status_list = sp_status_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_list", "sp_user_list", "sp_status_list"])
        sp_list = data.get("sp_list")
        sp_user_list = data.get("sp_user_list")
        sp_status_list = data.get("sp_status_list")
        return GetServiceProviderDetailsFilterSuccess(sp_list, sp_user_list, sp_status_list)

    def to_inner_structure(self):
        return {
            "sp_list": self.sp_list,
            "sp_user_list": self.sp_user_list,
            "sp_status_list": self.sp_status_list
        }

class GetServiceProviderDetailsReportSuccess(Response):
    def __init__(self, sp_details_list):
        self.sp_details_list = sp_details_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_details_list"])
        sp_details_list = data.get("sp_details_list")
        return GetServiceProviderDetailsReportSuccess(sp_details_list)

    def to_inner_structure(self):
        return {
            "sp_details_list" : self.sp_details_list
        }

class GetAuditTrailFilterSuccess(Response):
    def __init__(self, audit_users_list, audit_forms_list):
        self.audit_users_list = audit_users_list
        self.audit_forms_list = audit_forms_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["audit_users_list", "audit_forms_list"])
        audit_users_list = data.get("audit_users_list")
        audit_forms_list = data.get("audit_forms_list")
        return GetAuditTrailFilterSuccess(
            audit_users_list, audit_forms_list
        )

    def to_inner_structure(self):
        return {
            "audit_users_list": self.audit_users_list,
            "audit_forms_list": self.audit_forms_list
        }

class GetLoginTraceFilterSuccess(Response):
    def __init__(self, audit_users_list):
        self.audit_users_list = audit_users_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["audit_users_list"])
        audit_users_list = data.get("audit_users_list")
        return GetLoginTraceFilterSuccess(
            audit_users_list
        )

    def to_inner_structure(self):
        return {
            "audit_users_list": self.audit_users_list
        }

class GetLoginTraceReportDataSuccess(Response):
    def __init__(self, log_trace_activities):
        self.log_trace_activities = log_trace_activities

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["log_trace_activities"])
        log_trace_activities = data.get("log_trace_activities")
        return GetLoginTraceReportDataSuccess(log_trace_activities)

    def to_inner_structure(self):
        return {
            "log_trace_activities" : self.log_trace_activities
        }

class GetUserProfileSuccess(Response):
    def __init__(self, user_profile):
        self.user_profile = user_profile

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_profile"])
        user_profile = data.get("user_profile")
        return GetUserProfileSuccess(user_profile)

    def to_inner_structure(self):
        return {
            "user_profile" : self.user_profile
        }

class UpdateUserProfileSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserProfileSuccess()

    def to_inner_structure(self):
        return {
        }

class GetSettingsFormDetailsSuccess(Response):
    def __init__(self, settings_details, settings_domains, settings_users):
        self.settings_details = settings_details
        self.settings_domains = settings_domains
        self.settings_users = settings_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["settings_details", "settings_domains", "settings_users"])
        settings_details = data.get("settings_details")
        settings_domains = data.get("settings_domains")
        settings_users = data.get("settings_users")
        return GetSettingsFormDetailsSuccess(settings_details, settings_domains, settings_users)

    def to_inner_structure(self):
        return {
            "settings_details": self.settings_details,
            "settings_domains": self.settings_domains,
            "settings_users": self.settings_users
        }

class SaveSettingsFormDetailsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveSettingsFormDetailsSuccess()

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
        GetUnitClosureDataSuccess, SaveUnitClosureSuccess, InvalidUnitId,
        GetUserManagementPrerequisiteSuccess,
        GetServiceProviderDetailsFilterSuccess,
        GetServiceProviderDetailsReportSuccess, GetAuditTrailFilterSuccess,
        GetLoginTraceFilterSuccess, GetLoginTraceReportDataSuccess,
        GetUserProfileSuccess, UpdateUserProfileSuccess, UserManagementListSuccess,
        GetSettingsFormDetailsSuccess, SaveSettingsFormDetailsSuccess,
        BlockServiceProviderSuccess, UserManagementEditViewSuccess
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
# Service Provider List
#
class ServiceProviders(object):
    def __init__(self, sp_id, sp_name):
        self.sp_id = sp_id
        self.sp_name = sp_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["sp_id", "sp_name"])
        sp_id = data.get("sp_id")
        sp_name = data.get("sp_name")
        return ServiceProviders(sp_id, sp_name)

    def to_structure(self):
        return {
            "sp_id": self.sp_id,
            "sp_name": self.sp_name,
        }

#
# Service Provider - Users List
#
class ServiceProviderUsers(object):
    def __init__(self, sp_id_optional, user_id, user_name):
        self.sp_id_optional = sp_id_optional
        self.user_id = user_id
        self.user_name = user_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["sp_id_optional", "user_id", "user_name"])
        sp_id_optional = data.get("sp_id_optional")
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        return ServiceProviderUsers(sp_id_optional, user_id, user_name)

    def to_structure(self):
        data = {
            "sp_id_optional": self.sp_id_optional,
            "user_id": self.user_id,
            "user_name": self.user_name
        }
        return to_structure_dictionary_values(data)

#
# Service Provider - status List
#
class ServiceProvidersStatus(object):
    def __init__(self, s_p_status_id, s_p_status):
        self.s_p_status_id = s_p_status_id
        self.s_p_status = s_p_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["s_p_status_id", "s_p_status"])
        s_p_status_id = data.get("s_p_status_id")
        s_p_status = data.get("s_p_status")
        return ServiceProvidersStatus(s_p_status_id, s_p_status)

    def to_structure(self):
        return {
            "s_p_status_id": self.s_p_status_id,
            "s_p_status": self.s_p_status,
        }


#
# Service Provider - Details
#
class ServiceProvidersDetailsList(object):
    def __init__(
        self, sp_id, sp_name, con_no, email_id, address, contract_period,
        s_p_status, sp_status_date, unit_count
    ):
        self.sp_id = sp_id
        self.sp_name = sp_name
        self.con_no = con_no
        self.email_id = email_id
        self.address = address
        self.contract_period = contract_period
        self.s_p_status = s_p_status
        self.sp_status_date = sp_status_date
        self.unit_count = unit_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "sp_id", "sp_name", "con_no", "email_id", "address", "contract_period",
            "s_p_status", "sp_status_date", "unit_count"
        ])
        sp_id = data.get("sp_id")
        sp_name = data.get("sp_name")
        con_no = data.get("con_no")
        email_id = data.get("email_id")
        address = data.get("address")
        contract_period = data.get("contract_period")
        s_p_status = data.get("s_p_status")
        sp_status_date = data.get("sp_status_date")
        unit_count = data.get("unit_count")
        return ServiceProvidersDetailsList(
            sp_id, sp_name, con_no, email_id, address, contract_period, s_p_status,
            sp_status_date, unit_count
        )

    def to_structure(self):
        return {
            "sp_id": self.sp_id,
            "sp_name": self.sp_name,
            "con_no": self.con_no,
            "email_id": self.email_id,
            "address": self.address,
            "contract_period": self.contract_period,
            "s_p_status": self.s_p_status,
            "sp_status_date": self.sp_status_date,
            "unit_count": self.unit_count
        }

#
# Audit Trail Users
#

class AuditTrailUsers(object):
    def __init__(self, user_id, user_name, user_category_id, u_g_id):
        self.user_id = user_id
        self.user_name = user_name
        self.user_category_id = user_category_id
        self.u_g_id = u_g_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_name", "user_category_id", "u_g_id"
        ])
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        user_category_id = data.get("user_category_id")
        u_g_id = data.get("u_g_id")
        return AuditTrailUsers(user_id, user_name, user_category_id, u_g_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_category_id": self.user_category_id,
            "u_g_id": self.u_g_id
        }

#
# Audit Trail Forms
#

class AuditTrailForms(object):
    def __init__(self, u_g_id, form_id, form_name):
        self.u_g_id = u_g_id
        self.form_id = form_id
        self.form_name = form_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_g_id", "form_id", "form_name"
        ])
        u_g_id = data.get("u_g_id")
        form_id = data.get("form_id")
        form_name = data.get("form_name")
        return AuditTrailForms(u_g_id, form_id, form_name)

    def to_structure(self):
        return {
            "u_g_id": self.u_g_id,
            "form_id": self.form_id,
            "form_name": self.form_name,
        }

#
# Login Trace Forms
#

class LoginTraceActivities(object):
    def __init__(self, form_id, form_name, action, created_on):
        self.form_id = form_id
        self.form_name = form_name
        self.action = action
        self.created_on = created_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "form_id", "form_name", "action," "created_on"
        ])
        form_id = data.get("form_id")
        form_name = data.get("form_name")
        action = data.get("action")
        created_on = data.get("created_on")
        return LoginTraceActivities(form_id, form_name, action, created_on)

    def to_structure(self):
        return {
            "form_id": self.form_id,
            "form_name": self.form_name,
            "action": self.action,
            "created_on": self.created_on
        }

#
# View Profile
#

class UserProfile(object):
    def __init__(
        self, user_id, user_name, emp_code, emp_name, short_name, email_id,
        con_no, mob_no, u_g_name, address
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.emp_code = emp_code
        self.emp_name = emp_name
        self.short_name = short_name
        self.email_id = email_id
        self.con_no = con_no
        self.mob_no = mob_no
        self.u_g_name = u_g_name
        self.address = address

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_name", "emp_code," "emp_name", "short_name",
            "email_id", "con_no", "mob_no", "u_g_name", "address"
        ])
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        emp_code = data.get("emp_code")
        emp_name = data.get("emp_name")
        short_name = data.get("short_name")
        email_id = data.get("email_id")
        con_no = data.get("con_no")
        mob_no = data.get("mob_no")
        u_g_name = data.get("u_g_name")
        address = data.get("address")
        return UserProfile(
            user_id, user_name, emp_code, emp_name, short_name, email_id, con_no,
            mob_no, u_g_name, address
        )

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "emp_code": self.emp_code,
            "emp_name": self.emp_name,
            "short_name": self.short_name,
            "email_id": self.email_id,
            "con_no": self.con_no,
            "mob_no": self.mob_no,
            "u_g_name": self.u_g_name,
            "address": self.address
        }

#
# Settings Details
#

class SettingsInfo(object):
    def __init__(
        self, legal_entity_name, business_group_name, country_name, contract_from, contract_to,
        two_level_approve, assignee_reminder, advance_escalation_reminder, escalation_reminder,
        reassign_sp, file_space_limit, used_file_space, total_licence, used_licence
    ):
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.country_name = country_name
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.two_level_approve = two_level_approve
        self.assignee_reminder = assignee_reminder
        self.advance_escalation_reminder = advance_escalation_reminder
        self.escalation_reminder = escalation_reminder
        self.reassign_sp = reassign_sp
        self.file_space_limit = file_space_limit
        self.used_file_space = used_file_space
        self.total_licence = total_licence
        self.used_licence = used_licence

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_name", "business_group_name", "country_name", "contract_from", "contract_to",
            "two_level_approve", "assignee_reminder", "advance_escalation_reminder", "escalation_reminder",
            "reassign_sp", "file_space_limit", "used_file_space", "total_licence", "used_licence"
        ])
        legal_entity_name = data.get("legal_entity_name")
        business_group_name = data.get("business_group_name")
        country_name = data.get("country_name")
        contract_from = data.get("contract_from")
        contract_to = data.get("contract_to")
        two_level_approve = data.get("two_level_approve")
        assignee_reminder = data.get("assignee_reminder")
        advance_escalation_reminder = data.get("advance_escalation_reminder")
        escalation_reminder = data.get("escalation_reminder")
        reassign_sp = data.get("reassign_sp")
        file_space_limit = data.get("file_space_limit")
        used_file_space = data.get("used_file_space")
        total_licence = data.get("total_licence")
        used_licence = data.get("used_licence")

        return SettingsInfo(
            legal_entity_name, business_group_name, country_name, contract_from, contract_to, two_level_approve,
            assignee_reminder, advance_escalation_reminder, escalation_reminder, reassign_sp, file_space_limit,
            used_file_space, total_licence, used_licence
        )

    def to_structure(self):
        return {
            "legal_entity_name": self.legal_entity_name,
            "business_group_name": self.business_group_name,
            "country_name": self.country_name,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "two_level_approve": self.two_level_approve,
            "assignee_reminder": self.assignee_reminder,
            "advance_escalation_reminder": self.advance_escalation_reminder,
            "escalation_reminder": self.escalation_reminder,
            "reassign_sp": self.reassign_sp,
            "file_space_limit": self.file_space_limit,
            "used_file_space": self.used_file_space,
            "total_licence": self.total_licence,
            "used_licence": self.used_licence
        }

#
# legal entity domains
#

class LegalEntityDomains(object):
    def __init__(self, domain_name, organisation_name, org_count, activity_date):
        self.domain_name = domain_name
        self.organisation_name = organisation_name
        self.org_count = org_count
        self.activity_date = activity_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "domain_name", "organisation_name", "org_count", "activity_date"
        ])
        domain_name = data.get("domain_name")
        organisation_name = data.get("organisation_name")
        org_count = data.get("org_count")
        activity_date = data.get("activity_date")
        return LegalEntityDomains(domain_name, organisation_name, org_count, activity_date)

    def to_structure(self):
        return {
            "domain_name": self.domain_name,
            "organisation_name": self.organisation_name,
            "org_count": self.org_count,
            "activity_date": self.activity_date
        }

#
# legal entity users
#

class LegalEntityUsers(object):
    def __init__(self, employee_name, user_name, user_level_name, category_name, unit_code_name, address):
        self.employee_name = employee_name
        self.user_name = user_name
        self.user_level_name = user_level_name
        self.category_name = category_name
        self.unit_code_name = unit_code_name
        self.address = address

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "employee_name", "user_name", "user_level_name", "category_name", "unit_code_name", "address"
        ])
        employee_name = data.get("employee_name")
        user_name = data.get("user_name")
        user_level_name = data.get("user_level_name")
        category_name = data.get("category_name")
        unit_code_name = data.get("unit_code_name")
        address = data.get("address")
        return LegalEntityUsers(employee_name, user_name, user_level_name, category_name, unit_code_name, address)

    def to_structure(self):
        return {
            "employee_name": self.employee_name,
            "user_name": self.user_name,
            "user_level_name": self.user_level_name,
            "category_name": self.category_name,
            "unit_code_name": self.unit_code_name,
            "address": self.address
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
