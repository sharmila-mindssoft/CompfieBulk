from aparajitha.model.types import *
from aparajitha.model.common import *


__all__ = [
	"Request", "RequestFrame"
]


#
# define_request
#

_request_options = {}

def define_request(request, request_format, response_format, failures):
	if request in _request_options :
		print "%s already exists" % (request,)
		return None
	_request_options[request] = DictType(request_format)

	response_options = {}
	response_options[request + "Success"] = DictType(response_format)
	for failure in failures :
		response_options[failure] = DictType({})
	response_name = request + "Response"
	response_type = VariantType(response_name, DictType(response_options))
	g = globals()
	assert response_name not in g
	g[response_name] = response_type
	assert response_name not in __all__
	__all__.append(response_name)


#
# Login, Logout
#

Form = DictType({
	"form_id": Int,
	"form_name": Text50,
	"form_url": Text50,
	"form_type": Text20,
	"form_order": Int,
	"parent_menu": OptionalType(Text50)
})

Menu = DictType({
	"masters": ListType(Form),
	"transactions": ListType(Form),
	"reports": ListType(Form),
	"settings": ListType(Form),
})

Domain = DictType({
		"domain_id": Int,
		"domain_name": Text50,
		"is_active":Int
	})

Country = DictType({
		"country_id": Int,
		"country_name": Text50,
		"is_active":Int
	})

BusinessGroup = DictType({
		"business_group_id": Int,
		"business_group_name": Text50,
	})

LegalEntity = DictType({
		"legal_entity_id": Int,
		"legal_entity_name": Text50,
		"business_group_id": Int,
	})

Division = DictType({
		"division_id": Int,
		"division_name": Text50,
		"legal_entity_id": Int,
		"business_group_id": Int,
	})

Unit = DictType({
		"unit_id": Int,
		"unit_name": Text50,
		"division_id": Int,
		"legal_entity_id": Int,
		"business_group_id": Int,
	})

define_request(
	"Login", {
		"username": Text250,
		"password": Text50
	}, {
		"session_token": Text50,
		"user": DictType({
			"user_id": Int,
			"client_id": OptionalType(Int),
			"category": Text20,
			"email_id": Text100,
			"user_group_name": Text50,
			"employee_name": Text50,
			"employee_code": Text50,
			"contact_no": OptionalType(Text20),
			"address": OptionalType(Text250),
			"designation": OptionalType(Text50)
		}),
		"menu": Menu
	},
	["LoginFailed"]
)

define_request(
	"Logout",
	{},
	{},
	["InvalidSession"]
)

define_request(
	"Test",
	{},
	{},
	["InvalidSession"]
)

#
# Service Provider
#

define_request(
	"SaveServiceProvider",
	{
		"service_provider_name": Text50, 
        "address": Text500,
        "contract_from": Text20 ,
        "contract_to": Text20, 
        "contact_person": Text50,
        "contact_no": Text20
	},
	{},
	[
		"ServiceProviderNameAlreadyExists",
		"ContactNumberAlreadyExists"
	]
)

define_request(
	"UpdateServiceProvider",
	{
		"service_provider_id": Int,
		"service_provider_name": Text50, 
        "address": Text500,
        "contract_from": Text20 ,
        "contract_to": Text20, 
        "contact_person": Text50,
        "contact_no": Text20
	},
	{},
	[
		"InvalidServiceProviderId",
		"ServiceProviderNameAlreadyExists",
		"ContactNumberAlreadyExists"
	]
)

define_request(
	"ChangeServiceProviderStatus",
	{
		"service_provider_id" : Int,
        "is_active" : Int
	},
	{},
	[
		"InvalidServiceProviderId"
	]
)

define_request(
	"GetServiceProviders",
	{},
	{
		"service_providers": ListType(
			DictType({
				"service_provider_id": Int,
				"service_provider_name": Text50, 
		        "address": Text500,
		        "contract_from": Text20 ,
		        "contract_to": Text20, 
		        "contact_person": Text50,
		        "contact_no": Text20
			})
		)
	},
	[]
)

#
# Client User Group
#

define_request(
	"GetUserPrivileges",
	{},
	{
		"forms": Menu,
        "user_groups": ListType(
        		DictType(
        			{     
					    "user_group_id": Int,
					    "user_group_name": Text50,
					    "form_ids": ListType(Int),
					    "is_active": Int
					}
        		)
        	)
	},
	[]
)

define_request(
	"SaveUserPrivilege",
	{
		"user_group_name": Text50,
        "form_type": Text20,
        "form_ids": ListType(Int)
	},
	{},
	[
		"GroupNameAlreadyExists"
	]
)

define_request(
	"UpdateUserPrivilege",
	{
		"user_group_id": Int,
		"user_group_name": Text50,
        "form_type": Text20,
        "form_ids": ListType(Int)
	},
	{},
	[
		"InvalidUserGroupId",
		"GroupNameAlreadyExists"
	]
)

define_request(
	"ChangeUserPrivilegeStatus",
	{
		"user_group_id": Int,
		"is_active": Int
	},
	{},
	[
		"InvalidUserGroupId",
	]
)

#
# Client Users
#
define_request(
	"GetClientUsers",
	{},
	{
		"domains":ListType(Domain),
		"countries":ListType(Country),
		"business_groups":ListType(BusinessGroup),
		"legal_entities":ListType(LegalEntity),
		"divisions": ListType(Division),
		"units": ListType(Unit),
		"user_groups":ListType(
			DictType(
				{
					"user_group_id": Int,
					"user_group_name": Text50,
					"is_active": Int
				}
			)
		),
		"users": ListType(
			DictType(
				{
				    "user_id": Int,
				    "email_id": Text100,
				    "user_group_id": OptionalType(Int), 
				    "employee_name": Text50,
				    "contact_no": OptionalType(Text20),
				    "seating_unit_id": OptionalType(Int),
				    "user_level": OptionalType(Int),
				    "country_ids":ListType(Int),
				    "domain_ids": ListType(Int),
				    "unit_ids": OptionalType(ListType(Int)),
				    "is_admin": Int,
				    "is_service_provider": Int,
				    "service_provider_id": OptionalType(Int),
				    "is_active": Int
				}
			)
		)
	},
	[]
)

define_request(
	"SaveClientUser",
	{
        "email_id": Text100,
        "user_group_id": Int, 
        "employee_name": Text50,
        "employee_code": Text50,
        "contact_no": Text20,
        "seating_unit_id": Int,
        "seating_unit_name": Text50,
        "user_level": Int,
        "country_ids": ListType(Int),
        "domain_ids": ListType(Int),
        "unit_ids": ListType(Int),
        "is_service_provider": Int,
        "service_provider_id": OptionalType(Int)
    },
	{},
	[
		"EmailIdAlreadyExists",
		"EmployeeCodeAlreadyExists",
		"ContactNumberAlreadyExists"
	]
)

define_request(
	"UpdateClientUser",
	{
		"user_id": Int,
        "user_group_id": Int, 
        "employee_name": Text50,
        "employee_code": Text50,
        "contact_no": Text20,
        "seating_unit_id": Int,
        "seating_unit_name": Text50,
        "user_level": Int,
        "country_ids": ListType(Int),
        "domain_ids": ListType(Int),
        "unit_ids": ListType(Int),
        "is_service_provider": Int,
        "service_provider_id": OptionalType(Int)
    },
	{},
	[
		"InvalidUserId",
		"EmployeeCodeAlreadyExists",
		"ContactNumberAlreadyExists"
	]
)

define_request(
	"ChangeClientUserStatus",
	{
		"user_id": Int,
		"is_active": Int
	},
	{},
	[
		"InvalidUserId",
	]
)

define_request(
	"ChangeAdminStatus",
	{
		"user_id": Int,
		"is_admin": Int
	},
	{},
	[
		"InvalidUserId",
	] 
)

#
# 	Unit Closure
#
define_request(
	"GetUnitClosureList",
	{},
	{
		"units": ListType(
			DictType(
				{
					"business_group_name":Text50,
					"legal_entity_name": Text50,
					"division_name": Text50,
					"unit_id": Int,
					"unit_name": Text100,
					"address": Text250,
					"is_active": Int,
				}
			)
		)
	},
	[] 
)

define_request(
	"CloseUnit",
	{
		"unit_id":Int,
		"password": Text50
	},
	{},
	[
		"InvalidPassword"
	] 
)

define_request

#
# Request, RequestFrame
#

Request = VariantType("Request", DictType(_request_options))
RequestFrame = DictType({
	"session_token": Text50,
	"request": Request
})
