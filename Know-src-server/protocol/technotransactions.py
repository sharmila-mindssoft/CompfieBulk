from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, parse_VariantType,
    to_VariantType, to_structure_dictionary_values
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


class ResendGroupAdminRegnMail(Request):
    def __init__(self, user_id, email_id, grp_mode):
        self.user_id = user_id
        self.email_id = email_id
        self.grp_mode = grp_mode

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "email_id", "grp_mode"])
        user_id = data.get("user_id")
        email_id = data.get("email_id")
        grp_mode = data.get("grp_mode")
        return ResendGroupAdminRegnMail(user_id, email_id, grp_mode)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "email_id": self.email_id,
            "grp_mode": self.grp_mode
        }

class SendGroupAdminRegnMail(Request):
    def __init__(
        self, grp_mode, username, email_id, client_id, group_name, legal_entity_id,
        legal_entity_name
    ):
        self.grp_mode = grp_mode
        self.username = username
        self.email_id = email_id
        self.client_id = client_id
        self.group_name = group_name
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "grp_mode", "username", "email_id",
                "client_id", "group_name", "legal_entity_id",
                "legal_entity_name"
            ]
        )
        return SendGroupAdminRegnMail(
            data.get("grp_mode"), data.get("username"),
            data.get("email_id"), data.get("client_id"), data.get("group_name"),
            data.get("legal_entity_id"), data.get("legal_entity_name")
        )

    def to_inner_structure(self):
        return {
            "grp_mode": self.grp_mode,
            "username": self.username,
            "email_id": self.email_id,
            "client_id": self.client_id,
            "group_name": self.group_name,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
        }

class GetCountriesForGroup(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetCountriesForGroup()

    def to_inner_structure(self):
        return {
        }

class GetGroupAdminGroupUnitList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetGroupAdminGroupUnitList()

    def to_inner_structure(self):
        return {
        }

class GetLegalEntityClosureReportData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetLegalEntityClosureReportData()

    def to_inner_structure(self):
        return {
        }

class SaveLegalEntityClosureData(Request):
    def __init__(
        self, password, closed_remarks, legal_entity_id, grp_mode
    ):
        self.password = password
        self.closed_remarks = closed_remarks
        self.legal_entity_id = legal_entity_id
        self.grp_mode = grp_mode

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "password", "closed_remarks", "legal_entity_id", "grp_mode"
        ])
        password = data.get("password")
        closed_remarks = data.get("closed_remarks")
        legal_entity_id = data.get("legal_entity_id")
        grp_mode = data.get("grp_mode")

        return SaveLegalEntityClosureData(
            password, closed_remarks, legal_entity_id, grp_mode
        )

    def to_inner_structure(self):
        data = {
            "password": self.password,
            "closed_remarks": self.closed_remarks,
            "legal_entity_id": self.legal_entity_id,
            "grp_mode": self.grp_mode,
        }
        return data

def _init_Request_class_map():
    classes = [
        GetCountriesForGroup,
        GetGroupAdminGroupUnitList,
        ResendGroupAdminRegnMail,
        SendGroupAdminRegnMail,
        GetLegalEntityClosureReportData,
        SaveLegalEntityClosureData
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
        print "inner: %s" % inner
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

class SaveGroupAdminRegnSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveGroupAdminRegnSuccess()

    def to_inner_structure(self):
        return {
        }

class ResendRegistraionSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ResendRegistraionSuccess()

    def to_inner_structure(self):
        return {
        }

class getGroupAdminGroupsUnitsSuccess(Response):
    def __init__(self, groupadmin_groupList, groupadmin_unitList):
        self.groupadmin_groupList = groupadmin_groupList
        self.groupadmin_unitList = groupadmin_unitList

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "groupadmin_groupList", "groupadmin_unitList"
        ])
        groupadmin_groupList = data.get("groupadmin_groupList")
        groupadmin_unitList = data.get("groupadmin_unitList")
        return getGroupAdminGroupsUnitsSuccess(
            groupadmin_groupList, groupadmin_unitList
        )

    def to_inner_structure(self):
        print "inside protocol"
        return {
            "groupadmin_groupList": self.groupadmin_groupList,
            "groupadmin_unitList": self.groupadmin_unitList,
        }

class LegalEntityClosureReportDataSuccess(Response):
    def __init__(self, legalentity_closure):
        self.legalentity_closure = legalentity_closure

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "legalentity_closure"
        ])
        legalentity_closure = data.get("legalentity_closure")
        return LegalEntityClosureReportDataSuccess(
            legalentity_closure
        )

    def to_inner_structure(self):
        return {
            "legalentity_closure": self.legalentity_closure,
        }

class SaveLegalEntityClosureSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveLegalEntityClosureSuccess()

    def to_inner_structure(self):
        return {
        }

class SaveLegalEntityClosureFailure(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveLegalEntityClosureFailure()

    def to_inner_structure(self):
        return {
        }



def _init_Response_class_map():
    classes = [
        SaveGroupAdminRegnSuccess,
        ResendRegistraionSuccess,
        LegalEntityClosureReportDataSuccess,
        SaveLegalEntityClosureSuccess,
        SaveLegalEntityClosureFailure,
        getGroupAdminGroupsUnitsSuccess
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
            request, "technotransactions", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "technotransactions", "Response"
            ),
        }

#
# ASSIGNED_STATUTORIES
#

class GroupAdmin_GroupList(object):
    def __init__(
        self, client_id, group_name, no_of_legal_entities, c_names, ug_name, email_id,
        user_id_search, emp_code_name, registration_email_date, resend_email_date
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.no_of_legal_entities = no_of_legal_entities
        self.c_names = c_names
        self.ug_name = ug_name
        self.email_id = email_id
        self.user_id_search = user_id_search
        self.emp_code_name = emp_code_name
        self.registration_email_date = registration_email_date
        self.resend_email_date = resend_email_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "group_name", "no_of_legal_entities", "c_names",
            "ug_name", "email_id", "user_id_search", "emp_code_name",
            "registration_email_date", "resend_email_date"
        ])
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        no_of_legal_entities = data.get("no_of_legal_entities")
        c_names = data.get("c_names")
        ug_name = data.get("ug_name")
        email_id = data.get("email_id")
        user_id_search = data.get("user_id_search")
        emp_code_name = data.get("emp_code_name")
        registration_email_date = data.get("registration_email_date")
        resend_email_date = data.get("resend_email_date")
        return GroupAdmin_GroupList(
            client_id, group_name, no_of_legal_entities, c_names, ug_name, email_id,
            user_id_search, emp_code_name, registration_email_date, resend_email_date
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "no_of_legal_entities": self.no_of_legal_entities,
            "c_names": self.c_names,
            "ug_name": self.ug_name,
            "email_id": self.email_id,
            "user_id_search": self.user_id_search,
            "emp_code_name": self.emp_code_name,
            "registration_email_date": self.registration_email_date,
            "resend_email_date": self.resend_email_date
        }

class GroupAdmin_UnitList(object):
    def __init__(
        self, client_id, legal_entity_id, legal_entity_name, country_name, unit_count,
        unit_creation_informed, statutory_assigned_informed, email_id, user_id_search, emp_code_name,
        statutory_count
    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.country_name = country_name
        self.unit_count = unit_count
        self.unit_creation_informed = unit_creation_informed
        self.statutory_assigned_informed = statutory_assigned_informed
        self.email_id = email_id
        self.user_id_search = user_id_search
        self.emp_code_name = emp_code_name
        self.statutory_count = statutory_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "legal_entity_id", "legal_entity_name", "country_name",
            "unit_count", "unit_creation_informed", "statutory_assigned_informed", "email_id",
            "user_id_search", "emp_code_name", "statutory_count"
        ])
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        country_name = data.get("country_name")
        unit_count = data.get("unit_count")
        unit_creation_informed = data.get("unit_creation_informed")
        statutory_assigned_informed = data.get("statutory_assigned_informed")
        email_id = data.get("email_id")
        user_id_search = data.get("user_id_search")
        emp_code_name = data.get("emp_code_name")
        statutory_count = data.get("statutory_count")
        return GroupAdmin_UnitList(
            client_id, legal_entity_id, legal_entity_name, country_name, unit_count,
            unit_creation_informed, statutory_assigned_informed, email_id, user_id_search,
            emp_code_name, statutory_count
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "country_name": self.country_name,
            "unit_count": self.unit_count,
            "unit_creation_informed": self.unit_creation_informed,
            "statutory_assigned_informed": self.statutory_assigned_informed,
            "email_id": self.email_id,
            "user_id_search": self.user_id_search,
            "emp_code_name": self.emp_code_name,
            "statutory_count": self.statutory_count,
        }

class LegalEntityClosure(object):
    def __init__(
        self, client_id, group_name, legal_entity_id, legal_entity_name, business_group_name,
        country_name, is_active, closed_on, validity_days
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.country_name = country_name
        self.is_active = is_active
        self.closed_on = closed_on
        self.validity_days = validity_days

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "group_name", "legal_entity_id", "legal_entity_name", "business_group_name",
            "country_name", "is_active", "closed_on", "validity_days"
        ])
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        business_group_name = data.get("business_group_name")
        country_name = data.get("country_name")
        is_active = data.get("is_active")
        closed_on = data.get("closed_on")
        validity_days = data.get("validity_days")
        return LegalEntityClosure(
            client_id, group_name, legal_entity_id, legal_entity_name, business_group_name,
            country_name, is_active, closed_on, validity_days
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "business_group_name": self.business_group_name,
            "country_name": self.country_name,
            "is_active": self.is_active,
            "closed_on": self.closed_on,
            "validity_days": self.validity_days,
        }
        return data
