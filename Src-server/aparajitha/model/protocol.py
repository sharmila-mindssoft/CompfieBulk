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

# Service Provider

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
		"UserGroupNameAlreadyExists"
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
		"UserGroupNameAlreadyExists"
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
# Request, RequestFrame
#

Request = VariantType("Request", DictType(_request_options))
RequestFrame = DictType({
	"session_token": Text50,
	"request": Request
})
