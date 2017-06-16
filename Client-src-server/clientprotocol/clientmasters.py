
from clientprotocol.jsonvalidators_client import (parse_dictionary, parse_static_list, to_structure_dictionary_values)

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
        return {}
#############################################################
# Save Service Provider Details
#############################################################
class SaveServiceProvider(Request):
    def __init__(
        self, service_provider_name, short_name, contract_from, contract_to, contact_person,
        contact_no, mobile_no, email_id, address
    ):
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
        ])
        return SaveServiceProvider(
            data.get("s_p_name"), data.get("s_p_short"), data.get("cont_from"),
            data.get("cont_to"), data.get("cont_person"), data.get("cont_no"),
            data.get("mob_no"), data.get("e_id"), data.get("address")
        )

#############################################################
# Update Service Provider Details
#############################################################
class UpdateServiceProvider(Request):
    def __init__(
        self, service_provider_id, service_provider_name, short_name, contract_from,
        contract_to, contact_person, contact_no, mobile_no, email_id, address
    ):
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
        ])

        return UpdateServiceProvider(
            data.get("s_p_id"), data.get("s_p_name"), data.get("s_p_short"),
            data.get("cont_from"), data.get("cont_to"), data.get("cont_person"),
            data.get("cont_no"), data.get("mob_no"), data.get("e_id"), data.get("address")
        )

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
        return ChangeServiceProviderStatus(
            data.get("sp_id"), data.get("active_status"), data.get("password")
        )


#################################################
# Block Service Provider Status
##################################################
class BlockServiceProvider(Request):
    def __init__(self, service_provider_id, is_blocked, remarks, password):
        self.service_provider_id = service_provider_id
        self.is_blocked = is_blocked
        self.password = password
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_id", "is_blocked", "remarks", "password"])
        service_provider_id = data.get("sp_id")
        is_blocked = data.get("is_blocked")
        remarks = data.get("remarks")
        password = data.get("password")
        return BlockServiceProvider(service_provider_id, is_blocked, remarks, password)

    def to_inner_structure(self):
        return {
            "sp_id": self.service_provider_id,
            "is_blocked": self.is_blocked,
            "remarks": self.remarks,
            "password": self.password,
        }

#################################################
# Disable User
##################################################
class BlockUser(Request):
    def __init__(self, user_id, is_blocked, remarks, password):
        self.user_id = user_id
        self.is_blocked = is_blocked
        self.password = password
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "is_blocked", "remarks", "password"])
        user_id = data.get("user_id")
        is_blocked = data.get("is_blocked")
        remarks = data.get("remarks")
        password = data.get("password")
        return BlockUser(user_id, is_blocked, remarks, password)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id, "is_blocked": self.is_blocked,
            "remarks": self.remarks, "password": self.password,
        }

#################################################
# Resend Registration Email for User
##################################################
class ResendRegistrationEmail(Request):
    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id"])
        user_id = data.get("user_id")
        return ResendRegistrationEmail(user_id)

    def to_inner_structure(self):
        return {"user_id": self.user_id}

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
        return {}
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
        return {}

########################################################
# User Management - Edit View
########################################################
class UserManagementEditView(Request):
    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id"])
        return UserManagementEditView(data.get("user_id"))

    def to_inner_structure(self):
        return {"user_id": self.user_id}

########################################################
# User Management - Employee Code Exits
########################################################
class EmployeeCodeExists(Request):
    def __init__(self, mode, user_id_optional, employee_code):
        self.mode = mode
        self.user_id_optional = user_id_optional
        self.employee_code = employee_code

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["mode", "user_id_optional", "employee_code"])
        return EmployeeCodeExists(data.get("mode"), data.get("user_id_optional"), data.get("employee_code"))

    def to_inner_structure(self):
        return {
            "mode": self.mode,
            "user_id_optional": self.user_id_optional,
            "employee_code": self.employee_code
            }


class GetUserPrivileges(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserPrivileges()

    def to_inner_structure(self):
        return {}

class SaveUserPrivileges(Request):
    def __init__(self, user_group_name, user_category_id, form_ids):
        self.user_group_name = user_group_name
        self.user_category_id = user_category_id
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_g_name", "u_c_id", "f_ids"])
        return SaveUserPrivileges(
            data.get("u_g_name"), data.get("u_c_id"), data.get("f_ids")
        )

    def to_inner_structure(self):
        return {
            "u_g_name": self.user_group_name, "u_c_id": self.form_category_id,
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
        return UpdateUserPrivileges(
            data.get("u_g_id"), data.get("u_c_id"),
            data.get("u_g_name"), data.get("f_ids")
        )

    def to_inner_structure(self):
        return {
            "u_g_id": self.user_group_id, "u_c_id": self.form_category_id,
            "u_g_name": self.user_group_name, "f_ids": self.form_ids,
        }

class ChangeUserPrivilegeStatus(Request):
    def __init__(self, user_group_id, is_active, password):
        self.user_group_id = user_group_id
        self.is_active = is_active
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_g_id", "is_active", "password"])
        return ChangeUserPrivilegeStatus(
            data.get("u_g_id"), data.get("is_active"), data.get("password")
        )

    def to_inner_structure(self):
        return {
            "u_g_id": self.user_group_id, "is_active": self.is_active, "password": self.password,
        }

class GetClientUsers(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientUsers()

    def to_inner_structure(self):
        return {}

# -----------------------------------------------------------------------------------------------------------------
# Save Client Users
class SaveClientUser(Request):
    def __init__(
        self, user_category, user_group_id, email_id, employee_name,
        employee_code, contact_no, mobile_no, user_level, seating_unit_id,
        is_service_provider, service_provider_id, user_domain_ids, user_unit_ids,
        user_entity_ids
    ):
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
        self.user_unit_ids = user_unit_ids
        self.user_entity_ids = user_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "u_cat_id", "u_g_id", "email_id", "emp_name", "emp_code",
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
    def __init__(self, user_id, user_group_id,
        email_id, employee_name, employee_code, contact_no, mobile_no, user_level, seating_unit_id,is_service_provider, service_provider_id, user_domain_ids, user_unit_ids , user_entity_ids
        ):
        self.user_id = user_id
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
        data = parse_dictionary(data, ["u_id", "u_g_id", "email_id", "emp_name", "emp_code",
        "cont_no", "mob_no", "u_level", "s_unit", "is_sp", "sp_id", "user_domain_ids", "user_unit_ids", "user_entity_ids"])

        user_id = data.get("u_id")
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

        # return UpdateClientUser(user_id, user_group_id, employee_name, employee_code, contact_no, seating_unit_id, user_level, country_ids, domain_ids, unit_ids, is_service_provider, service_provider_id)

        return UpdateClientUser(user_id, user_group_id, email_id, employee_name, employee_code, contact_no, mobile_no, user_level,
                              seating_unit_id, is_service_provider, service_provider_id, user_domain_ids, user_unit_ids, user_entity_ids)

    def to_inner_structure(self):
        return {
            "u_id": self.user_id,
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

class ChangeClientUserStatus(Request):
    def __init__(self, user_id, active_status, employee_name, password):
        self.user_id = user_id
        self.active_status = active_status
        self.employee_name = employee_name
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_id", "active_status", "emp_name", "password"])
        user_id = data.get("u_id")
        active_status = data.get("active_status")
        employee_name = data.get("emp_name")
        password = data.get("password")
        return ChangeClientUserStatus(user_id, active_status, employee_name, password)

    def to_inner_structure(self):
        return {
            "u_id": self.user_id,
            "active_status": self.active_status,
            "emp_name": self.employee_name,
            "password": self.password
        }

class GetUnitClosureData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUnitClosureData()

    def to_inner_structure(self):
        return {}

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
        self, password, closed_remarks, unit_id, grp_mode,
        legal_entity_id
    ):
        self.legal_entity_id = legal_entity_id
        self.password = password
        self.closed_remarks = closed_remarks
        self.unit_id = unit_id
        self.grp_mode = grp_mode

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "password", "closed_remarks", "unit_id", "grp_mode",
            "legal_entity_id"
        ])
        password = data.get("password")
        closed_remarks = data.get("closed_remarks")
        unit_id = data.get("unit_id")
        grp_mode = data.get("grp_mode")
        legal_entity_id = data.get("legal_entity_id")
        return SaveUnitClosureData(
            password, closed_remarks, unit_id, grp_mode,
            legal_entity_id
        )

    def to_inner_structure(self):
        data = {
            "password": self.password,
            "closed_remarks": self.closed_remarks,
            "unit_id": self.unit_id,
            "grp_mode": self.grp_mode,
            "legal_entity_id": self.legal_entity_id
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
        return {}

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
        return {}

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
        return {}

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
        return UpdateUserProfile(
            data.get("user_id"), data.get("email_id"), data.get("con_no"),
            data.get("mob_no"), data.get("address"), data.get("emp_code"),
            data.get("emp_name")
        )

    def to_inner_structure(self):
        return {
            "user_id": self.user_id, "email_id": self.email_id, "con_no": self.con_no,
            "mob_no": self.mob_no, "address": self.address, "emp_code": self.emp_code,
            "emp_name": self.emp_name
        }

class GetLegalEntityDomains(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entity_id"])
        return GetLegalEntityDomains(data.get("legal_entity_id"))

    def to_inner_structure(self):
        return {"legal_entity_id": self.legal_entity_id}

def _init_Request_class_map():
    classes = [
        GetServiceProviders, ChangeClientUserStatus,
        SaveServiceProvider, UpdateServiceProvider, ChangeServiceProviderStatus,
        GetUserPrivileges, SaveUserPrivileges, UpdateUserPrivileges,
        ChangeUserPrivilegeStatus, GetClientUsers, SaveClientUser, UpdateClientUser,
        GetUnitClosureData, SaveUnitClosureData, GetUnitClosureUnitData,
        UserManagementPrerequisite,
        GetServiceProviderDetailsReportFilters, GetServiceProviderDetailsReport,
        GetAuditTrailReportFilters, GetLogintraceReportFilters, GetLoginTraceReportData,
        GetUserProfile, UpdateUserProfile, UserManagementList, BlockServiceProvider,
        UserManagementEditView, BlockUser, ResendRegistrationEmail, EmployeeCodeExists,
        GetLegalEntityDomains
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

        return GetServiceProvidersSuccess(data.get("service_providers"))

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
        return {}
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
        return {}

class UpdateServiceProviderSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateServiceProviderSuccess()

    def to_inner_structure(self):
        return {}

class CannotChangeStatusOfContractExpiredSP(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotChangeStatusOfContractExpiredSP()

    def to_inner_structure(self):
        return {}
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
        return {}
##############################################################################
# Disable User - Success
##############################################################################
class BlockUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return BlockUserSuccess()

    def to_inner_structure(self):
        return {}

##############################################################################
# Employee Code Not Available
##############################################################################
class EmployeeCodeSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmployeeCodeSuccess()

    def to_inner_structure(self):
        return {}

##############################################################################
# Disable User - Success
##############################################################################
class ResendRegistrationEmailSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ResendRegistrationEmailSuccess()

    def to_inner_structure(self):
        return {}

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
        return {}
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
        data = parse_dictionary(data, [
            "um_user_category", "um_user_group", "um_business_group", "um_legal_entity",
            "um_group_division", "um_group_category", "um_legal_domain", "um_legal_units",
            "um_service_providers"
        ])
        user_category = data.get("um_user_category")
        user_group = data.get("um_user_group")
        business_group = data.get("um_business_group")
        legal_entity = data.get("um_legal_entity")
        group_division = data.get("um_group_division")
        group_category = data.get("um_group_category")
        legal_Domains = data.get("um_legal_domain")
        legal_units = data.get("um_legal_units")
        service_providers = data.get("um_service_providers")
        return GetUserManagementPrerequisiteSuccess(
            user_category, user_group, business_group, legal_entity, group_division,
            group_category, legal_Domains, legal_units, service_providers
        )

    def to_inner_structure(self):
        return {
            "um_user_category": self.user_category, "um_user_group": self.user_group,
            "um_business_group": self.business_group, "um_legal_entity": self.legal_entity,
            "um_group_division": self.group_division, "um_group_category": self.group_category,
            "um_legal_domain": self.legal_Domains, "um_legal_units": self.legal_units,
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
            "ul_legal_entity": self.legal_entities, "ul_users": self.users
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
        data = parse_dictionary(data, ["ul_userDetails", "ul_legal_entities", "ul_user_domains", "ul_user_units"])
        users = data.get("ul_userDetails")
        legal_entities = data.get("ul_legal_entities")
        domains = data.get("ul_user_domains")
        units = data.get("ul_user_units")

        users = users
        legal_entities = legal_entities
        return UserManagementEditViewSuccess(users, legal_entities, domains, units)

    def to_inner_structure(self):
        return {
            "ul_userDetails": self.users, "ul_legal_entities": self.legal_entities,
            "ul_user_domains": self.domains, "ul_user_units": self.units
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
            "forms": self.forms, "user_groups": self.user_groups, "user_category": self.user_category,
        }

class UserGroupNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UserGroupNameAlreadyExists()

    def to_inner_structure(self):
        return {}

class InvalidUserGroupId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserGroupId()

    def to_inner_structure(self):
        return {}

class SaveUserPrivilegesSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserPrivilegesSuccess()

    def to_inner_structure(self):
        return {}

class UpdateUserPrivilegesSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserPrivilegesSuccess()

    def to_inner_structure(self):
        return {}

class ChangeUserPrivilegeStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeUserPrivilegeStatusSuccess()

    def to_inner_structure(self):
        return {}

class SaveClientUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveClientUserSuccess()

    def to_inner_structure(self):
        return {}


class EmailIdAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmailIdAlreadyExists()

    def to_inner_structure(self):
        return {}


class EmployeeCodeAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmployeeCodeAlreadyExists()

    def to_inner_structure(self):
        return {}

class EmployeeNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmployeeNameAlreadyExists()

    def to_inner_structure(self):
        return {}

class UnitsAlreadyAssigned(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UnitsAlreadyAssigned()

    def to_inner_structure(self):
        return {}

class UpdateClientUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateClientUserSuccess()

    def to_inner_structure(self):
        return {}

class InvalidUserId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserId()

    def to_inner_structure(self):
        return {}

class ChangeClientUserStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeClientUserStatusSuccess()

    def to_inner_structure(self):
        return {}

class InvalidPassword(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidPassword()

    def to_inner_structure(self):
        return {}

class InvalidServiceProviderId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidServiceProviderId()

    def to_inner_structure(self):
        return {}

class ReassignCompliancesBeforeDeactivate(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ReassignCompliancesBeforeDeactivate()

    def to_inner_structure(self):
        return {}


class CannotChangeOldPrimaryAdminStatus(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotChangeOldPrimaryAdminStatus()

    def to_inner_structure(self):
        return {}


class CannotChangePrimaryAdminStatus(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotChangePrimaryAdminStatus()

    def to_inner_structure(self):
        return {}


class CannotPromoteServiceProvider(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotChangePrimaryAdminStatus()

    def to_inner_structure(self):
        return {}

class ContactNumberAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ContactNumberAlreadyExists()

    def to_inner_structure(self):
        return {}

class CannotDeactivateUserExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotDeactivateUserExists()

    def to_inner_structure(self):
        return {}

class UserLimitExceeds(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UserLimitExceeds()

    def to_inner_structure(self):
        return {}

class CannotCloseUnit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotCloseUnit()

    def to_inner_structure(self):
        return {}

class GetUnitClosureDataSuccess(Response):
    def __init__(self, unit_closure_legal_entities):
        self.unit_closure_legal_entities = unit_closure_legal_entities

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_closure_legal_entities"])
        return GetUnitClosureDataSuccess(data.get("unit_closure_legal_entities"))

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
        return GetUnitClosureUnitDataSuccess(data.get("unit_closure_units"))

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
        return {}

class InvalidUnitId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUnitId()

    def to_inner_structure(self):
        return {}

class GetServiceProviderDetailsFilterSuccess(Response):
    def __init__(self, sp_list, sp_user_list, sp_status_list):
        self.sp_list = sp_list
        self.sp_user_list = sp_user_list
        self.sp_status_list = sp_status_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_list", "sp_user_list", "sp_status_list"])
        return GetServiceProviderDetailsFilterSuccess(
            data.get("sp_list"), data.get("sp_user_list"), data.get("sp_status_list")
        )

    def to_inner_structure(self):
        return {
            "sp_list": self.sp_list, "sp_user_list": self.sp_user_list, "sp_status_list": self.sp_status_list
        }

class GetServiceProviderDetailsReportSuccess(Response):
    def __init__(self, sp_details_list, total_count):
        self.sp_details_list = sp_details_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_details_list", "total_count"])
        return GetServiceProviderDetailsReportSuccess(data.get("sp_details_list"), data.get("total_count"))

    def to_inner_structure(self):
        return {
            "sp_details_list" : self.sp_details_list, "total_count": self.total_count
        }

class GetAuditTrailFilterSuccess(Response):
    def __init__(self, audit_users_list, audit_forms_list):
        self.audit_users_list = audit_users_list
        self.audit_forms_list = audit_forms_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["audit_users_list", "audit_forms_list"])
        return GetAuditTrailFilterSuccess(
            data.get("audit_users_list"), data.get("audit_forms_list")
        )

    def to_inner_structure(self):
        return {
            "audit_users_list": self.audit_users_list, "audit_forms_list": self.audit_forms_list
        }

class GetLoginTraceFilterSuccess(Response):
    def __init__(self, audit_users_list):
        self.audit_users_list = audit_users_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["audit_users_list"])
        return GetLoginTraceFilterSuccess(data.get("audit_users_list"))

    def to_inner_structure(self):
        return {"audit_users_list": self.audit_users_list}

class GetLoginTraceReportDataSuccess(Response):
    def __init__(self, log_trace_activities, total_count):
        self.log_trace_activities = log_trace_activities
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["log_trace_activities", "total_count"])
        return GetLoginTraceReportDataSuccess(data.get("log_trace_activities"), data.get("total_count"))

    def to_inner_structure(self):
        return {
            "log_trace_activities" : self.log_trace_activities, "total_count": self.total_count
        }

class GetUserProfileSuccess(Response):
    def __init__(self, user_profile):
        self.user_profile = user_profile

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_profile"])
        return GetUserProfileSuccess(data.get("user_profile"))

    def to_inner_structure(self):
        return {"user_profile" : self.user_profile}

class UpdateUserProfileSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserProfileSuccess()

    def to_inner_structure(self):
        return {}

class GetLegalEntityDomainsDetailsSuccess(Response):
    def __init__(self, settings_domains):
        self.settings_domains = settings_domains

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["settings_domains"])
        return GetLegalEntityDomainsDetailsSuccess(
            data.get("settings_domains")
        )

    def to_inner_structure(self):
        return {
            "settings_domains": self.settings_domains,
        }


def _init_Response_class_map():
    classes = [
        GetServiceProvidersSuccess, SaveServiceProviderSuccess,
        ServiceProviderNameAlreadyExists, UpdateServiceProviderSuccess,
        ChangeServiceProviderStatusSuccess, GetUserPrivilegesSuccess,
        UserGroupNameAlreadyExists, InvalidUserGroupId, SaveUserPrivilegesSuccess,
        UpdateUserPrivilegesSuccess, ChangeUserPrivilegeStatusSuccess,
        SaveClientUserSuccess, EmployeeCodeAlreadyExists,
        EmployeeNameAlreadyExists, CannotChangeOldPrimaryAdminStatus,
        UpdateClientUserSuccess, InvalidUserId, ChangeClientUserStatusSuccess,
        CannotDeactivateUserExists,
        InvalidPassword, ContactNumberAlreadyExists,
        InvalidServiceProviderId, EmailIdAlreadyExists, CannotChangePrimaryAdminStatus ,
        CannotPromoteServiceProvider, ReassignCompliancesBeforeDeactivate,
        CannotChangeStatusOfContractExpiredSP, CannotCloseUnit, GetUnitClosureUnitDataSuccess,
        GetUnitClosureDataSuccess, SaveUnitClosureSuccess, InvalidUnitId,
        GetUserManagementPrerequisiteSuccess,
        GetServiceProviderDetailsFilterSuccess,
        GetServiceProviderDetailsReportSuccess, GetAuditTrailFilterSuccess,
        GetLoginTraceFilterSuccess, GetLoginTraceReportDataSuccess,
        GetUserProfileSuccess, UpdateUserProfileSuccess, UserManagementListSuccess,
        BlockServiceProviderSuccess, UserManagementEditViewSuccess,
        UnitsAlreadyAssigned, BlockUserSuccess, EmployeeCodeSuccess,
        GetLegalEntityDomainsDetailsSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


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
        return ServiceProviders(data.get("sp_id"), data.get("sp_name"))

    def to_structure(self):
        return {
            "sp_id": self.sp_id, "sp_name": self.sp_name,
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
        return ServiceProviderUsers(data.get("sp_id_optional"), data.get("user_id"), data.get("user_name"))

    def to_structure(self):
        data = {
            "sp_id_optional": self.sp_id_optional, "user_id": self.user_id, "user_name": self.user_name
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
        return ServiceProvidersStatus(data.get("s_p_status_id"), data.get("s_p_status"))

    def to_structure(self):
        return {
            "s_p_status_id": self.s_p_status_id, "s_p_status": self.s_p_status,
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
        return ServiceProvidersDetailsList(
            data.get("sp_id"), data.get("sp_name"), data.get("con_no"), data.get("email_id"),
            data.get("address"), data.get("contract_period"), data.get("s_p_status"),
            data.get("sp_status_date"), data.get("unit_count"),
        )

    def to_structure(self):
        return {
            "sp_id": self.sp_id, "sp_name": self.sp_name, "con_no": self.con_no,
            "email_id": self.email_id, "address": self.address,
            "contract_period": self.contract_period, "s_p_status": self.s_p_status,
            "sp_status_date": self.sp_status_date, "unit_count": self.unit_count
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
        return AuditTrailUsers(
            data.get("user_id"), data.get("user_name"), data.get("user_category_id"),
            data.get("u_g_id"),
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "user_name": self.user_name,
            "user_category_id": self.user_category_id, "u_g_id": self.u_g_id
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
        data = parse_dictionary(data, ["u_g_id", "form_id", "form_name"])
        return AuditTrailForms(
            data.get("u_g_id"), data.get("form_id"), data.get("form_name")
        )

    def to_structure(self):
        return {
            "u_g_id": self.u_g_id, "form_id": self.form_id, "form_name": self.form_name,
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
        return LoginTraceActivities(
            data.get("form_id"), data.get("form_name"), data.get("action"), data.get("created_on"),
        )

    def to_structure(self):
        return {
            "form_id": self.form_id, "form_name": self.form_name, "action": self.action, "created_on": self.created_on
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
        return UserProfile(
            data.get("user_id"), data.get("user_name"), data.get("emp_code"),
            data.get("emp_name"), data.get("short_name"), data.get("email_id"),
            data.get("con_no"), data.get("mob_no"), data.get("u_g_name"), data.get("address")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "user_name": self.user_name, "emp_code": self.emp_code,
            "emp_name": self.emp_name, "short_name": self.short_name, "email_id": self.email_id,
            "con_no": self.con_no, "mob_no": self.mob_no, "u_g_name": self.u_g_name, "address": self.address
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
        return LegalEntityDomains(
            data.get("domain_name"), data.get("organisation_name"),
            data.get("org_count"), data.get("activity_date")
        )

    def to_structure(self):
        return {
            "domain_name": self.domain_name, "organisation_name": self.organisation_name,
            "org_count": self.org_count, "activity_date": self.activity_date
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
        return LegalEntityUsers(
            data.get("employee_name"), data.get("user_name"), data.get("user_level_name"),
            data.get("category_name"), data.get("unit_code_name"), data.get("address")
        )

    def to_structure(self):
        return {
            "employee_name": self.employee_name, "user_name": self.user_name,
            "user_level_name": self.user_level_name, "category_name": self.category_name,
            "unit_code_name": self.unit_code_name, "address": self.address
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
        request = data.get("request")
        request = Request.parse_structure(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": Request.to_structure(self.request)
        }
