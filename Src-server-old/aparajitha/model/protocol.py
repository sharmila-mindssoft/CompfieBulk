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

Country = DictType({
	"country_id" : Int,
	"country_name": Text50,
	"is_active": Int
})

Domain = DictType({
	"domain_id": Int,
	"domain_name": Text50,
	"is_active": Int
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

Industry = DictType({
	"industry_id": Int,
	"industry_name": Text50,
	"is_active": Int
})

StatutoryNature = DictType({
	"statutory_nature_id": Int,
	"statutory_nature_name": Text50,
	"is_active": Int
})

Level = DictType({
	"level_id": OptionalType(Int),
	"level_position": Int,
	"level_name": Text50
})

Geography = DictType({
	"geography_id": Int,
    "geography_name": Text100,
    "level_id": Int,
    "parent_id": Int,
    "is_active": Int
})

Statutory = DictType({
	"statutory_id": Int, 
    "statutory_name": Text100,
    "level_id": Int,
    "parent_ids": ListType(Int),
    "parent_id": Int
})

Compliance = DictType({
	"compliance_id": OptionalType(Int),
    "statutory_provision" : Text100,
    "compliance_task": Text100,
    "description": Text500,
    "document_name": Text50,
    "format_file_name": ListType(Text50),
    "penal_description": Text100,
    "compliance_frequency": Text20,
    "statutory_dates": ListType(
    	DictType({
    		"statutory_date": Int,
            "statutory_month": Int,
            "trigger_before_days": Int
    	})
    ),
    "repeats_type": OptionalType(Text20),
    "repeats_every": OptionalType(Int),
    "duration_type": OptionalType(Text20),
    "duration": OptionalType(Int),
    "is_active": Int
})

StatutoryMapping = DictType({
	"country_id": Int,
    "country_name": Text50,
    "domain_id": Int,
    "domain_name": Text50,
    "industry_ids": ListType(Int),
    "industry_names": Text100,
    "statutory_nature_id": Int,
    "statutory_nature_name": Text50,
    "statutory_ids": ListType(Int),
    "statutory_mappings": ListType(Text500),
    "compliances": ListType(Compliance),
    "compliance_names": ListType(Text100),
    "geographies_ids": ListType(Int),
    "approval_status": Text50,
    "is_active": Int
})

DateConfiguration = DictType({
		"country_id": Int,
	    "domain_id": Int,
	    "period_from": Int,
	    "period_to": Int
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

# Domain
define_request("GetDomains", 
	{}, 
	{
		"domains": ListType(Domain)
	}, 
	[]
)

define_request ( "SaveDomain", 
	{
		"domain_name": Text50
	},
	{},
	["DomainNameAlreadyExists"]
)

define_request ( "UpdateDomain", 
	{
		"domain_id": Int,
		"domain_name": Text50
	},
	{},
	["DomainNameAlreadyExists", "InvalidDomainId"]
)

define_request ( "ChangeDomainStatus", 
	{
		"domain_id": Int,
		"is_active": Int
	},
	{},
	["InvalidDomainId"]
)

# Country
define_request( "GetCountries", 
	{}, 
	{
		"countries": ListType(Country)
	}, 
	[]
)

define_request ( "SaveCountry", 
	{
		"country_name": Text50
	},
	{},
	["CountryNameAlreadyExists"]
)

define_request ( "UpdateCountry", 
	{
		"country_id": Int,
		"country_name": Text50
	},
	{},
	["CountryNameAlreadyExists", "InvalidCountryId"]
)

define_request ( "ChangeCountryStatus", 
	{
		"country_id": Int,
		"is_active": Int
	},
	{},
	["InvalidCountryId"]
)

# Industry
define_request( "GetIndustries", 
	{}, 
	{
		"industries": ListType(Industry)
	}, 
	[]
)

define_request ( "SaveIndustry", 
	{
		"industry_name": Text50
	},
	{},
	["IndustryNameAlreadyExists"]
)

define_request ( "UpdateIndustry", 
	{
		"industry_id": Int,
		"industry_name": Text50
	},
	{},
	["IndustryNameAlreadyExists", "InvalidIndustryId"]
)

define_request ( "ChangeIndustryStatus", 
	{
		"industry_id": Int,
		"is_active": Int
	},
	{},
	["InvalidIndustryId"]
)

# Statutory Nature
define_request( "GetStatutoryNatures", 
	{}, 
	{
		"statutory_natures": ListType(StatutoryNature)
	}, 
	[]
)

define_request ( "SaveStatutoryNature", 
	{
		"statutory_nature_name": Text50
	},
	{},
	["StatutoryNatureNameAlreadyExists"]
)

define_request ( "UpdateStatutoryNature", 
	{
		"statutory_nature_id": Int,
		"statutory_nature_name": Text50
	},
	{},
	["StatutoryNatureNameAlreadyExists", "InvalidStatutoryNatureId"]
)

define_request ( "ChangeStatutoryNatureStatus", 
	{
		"statutory_nature_id": Int,
		"is_active": Int
	},
	{},
	["InvalidStatutoryNatureId"]
)

define_request ("GetStatutoryLevels", {},
	{
		"countries": ListType(Country),
		"domains": ListType(Domain),
		"statutory_levels": DictType({
			Int: DictType({
				Int: ListType(Level),
			})
		})
	},
	[]
)

define_request("SaveStatutoryLevels", 
	{
		"country_id": Int,
		"domain_id": Int,
		"levels": ListType(Level)
	},
	{},
	["DuplicateStatutoryLevelNamesExists", "DuplicateStatutoryLevelPositionsExists"]
)

define_request ("GetGeographyLevels", {},
	{
		"countries": ListType(Country),
		"geography_levels": DictType({
			"country_id": ListType(Level),
		})
	},
	[]
)

define_request("SaveGeographyLevels", 
	{
		"country_id": Int,
		"levels": ListType(Level)
	},
	{},
	["DuplicateGeographyLevelNamesExists", "DuplicateGeographyLevelPositionsExists"]
)

define_request("GetGeographies", 
	{}, 
	{
		"countries": ListType(Country),
		"geography_levels": DictType({
			"country_id": ListType(Level),
		}),
		"geographies": ListType(Geography)
	}, 
	[]
)

define_request ("SaveGeography", 
	{
		"geography_level_id": Int,
        "geography_name": Text50,
        "parent_ids": ListType(Int)
	},
	{},
	["GeographyNameAlreadyExists"]
)

define_request ("UpdateGeography", 
	{
		"geography_name": Text50,
		"parent_ids": ListType(Int)
	}, 
	{}, 
	["GeographyNameAlreadyExists", "InvalidGeographyId"]
)

define_request ("ChangeGeographyStatus", 
	{
		"geography_id": Int,
		"is_active": Int
	}, 
	{},
	["GeographyNameAlreadyExists", "InvalidGeographyId"]
)

define_request ("GeographyReport", 
	{}, 
	{
		"countries": ListType(Country),
		"geographies": DictType({
			"geography": Text250,
			"is_active": Int
		})
	},
	[]
)

define_request ("SaveStatutory", 
	{
		"statutory_level_id": Int,
        "statutory_name": Text250,
        "parent_ids": ListType(Int)
	},
	{},
	["StatutoryNameAlreadyExists"]
)

define_request ("UpdateStatutory", 
	{
		"statutory_id": Int,
		"statutory_name": Text250,
		"parent_ids": ListType(Int)
	},
	{},
	["StatutoryNameAlreadyExists", "InvalidStatutoryId"]
)

define_request ("GetStatutoryMappings", 
	{}, 
	{
		"countries": ListType(Country),
		"domains": ListType(Domain),
		"statutory_natures": ListType(StatutoryNature),
        "statutory_levels": DictType({
			"country_id": DictType({
				"domain_id": ListType(Level),
			})
		}),
        "statutories": ListType(Statutory),
        "geography_levels": DictType({
			"country_id": ListType(Level)
		}),
        "geographies": ListType(Geography),
        "statutory_mappings": DictType({
        	"statutory_mapping_id": StatutoryMapping
        })

	}, 
	[]
)

define_request( "SaveStatutoryMapping",
	{
		"country_id": Int,
        "domain_id": Int,
        "industry_ids": ListType(Int),
        "statutory_nature_id": Int,
        "statutory_ids": ListType(Int),
        "compliances":ListType(Compliance),
        "geography_ids": ListType(Int)
	},
	{},
	[]
)

define_request("UpdateStatutoryMapping", 
	{
		"statutory_mapping_id": Int,
		"country_id": Int,
        "domain_id": Int,
        "industry_ids": ListType(Int),
        "statutory_nature_id": Int,
        "statutory_ids": ListType(Int),
        "compliances":ListType(Compliance),
        "geography_ids": ListType(Int)
	}, 
	{}, 
	["InvalidStatutoryMappingId"]
)

define_request ("UpdateStatutoryMappingStatus", 
	{
		"statutory_mapping_id": Int,
		"is_active": Int
	}, 
	{}, 
	["InvalidStatutoryMappingId"]
)

define_request ("ApproveStatutoryMapping", 
	{
		"statutory_mapping_id": Int,
        "approval_status": Text20,
        "rejected_reason": OptionalType(Text500),
        "notification_text": OptionalType(Text500)
	}, 
	{}, 
	["InvalidStatutoryMappingId"]
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

#
#	Admin User Group
#
define_request(
	"GetUserGroups",
	{},
	{
		"forms": DictType(
			{
	            "knowledge": Menu,
	            "techno": Menu
	        }
	    ),
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
	"SaveUserGroup",
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
	"UpdateUserGroup",
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
	"ChangeUserGroupStatus",
	{
		"user_group_id" : Int,
        "is_active" : Int
	},
	{},
	[
		"InvalidUserGroupId"
	] 
)

#
#	Admin User
#
define_request(
	"GetUsers",
	{},
	{
		"user_groups": ListType(
			DictType(
				{
	                "user_group_id": Int,
	                "user_group_name": Text50,
	                "is_active":Int
            	}
			)
		),
        "domains": ListType(Domain),
        "users":ListType(
        	DictType(
	            {
	                "user_id": Int,
	                "email_id": Text50,
	                "user_group_id": OptionalType(Int),
	                "employee_name": Text50,
	                "employee_code": OptionalType(Text20),
	                "contact_no": OptionalType(Text20),
	                "address": OptionalType(Text250), 
	                "designation": OptionalType(Text50),
	                "country_ids": OptionalType(ListType(Int)),
	                "domain_ids": OptionalType(ListType(Int)),
	                "is_active": Int 
	            }
	        )
        )
	},
	[] 
)

define_request(
	"SaveUser",
	{
		"email_id": Text50,
		"user_group_id": Int,
		"employee_name": Text50,
		"employee_code": Text20,
		"contact_no": Text20,
		"address": Text250, 
		"designation": Text50,
		"country_ids": ListType(Int),
		"domain_ids": ListType(Int)
	},
	{},
	[
		"EmailIdAlreadyExists",
		"EmployeeNameAlreadyExists",
		"EmployeeCodeAlreadyExists",
		"ContactNumberAlreadyExists"
	] 
)

define_request(
	"UpdateUser",
	{
		"user_id": Int,
		"user_group_id": Int,
		"employee_name": Text50,
		"employee_code": Text20,
		"contact_no": Text20,
		"address": Text250, 
		"designation": Text50,
		"country_ids": ListType(Int),
		"domain_ids": ListType(Int)
	},
	{},
	[
		"InvalidUserId",
		"EmployeeNameAlreadyExists",
		"EmployeeCodeAlreadyExists",
		"ContactNumberAlreadyExists"
	] 
)

define_request(
	"ChangeUserStatus",
	{
		"user_id" : Int,
        "is_active" : Int
	},
	{},
	[
		"InvalidUserId"
	] 
)

#
#	Change Password
#

define_request(
	"ChangePassword",
	{
		"current_password" : Text50,
        "new_password" : Text50
	},
	{},
	[
		"InvalidCurrentPassword"
	] 
)

#
#	Forgot Password
#
define_request(
	"ForgotPassword",
	{
		"username" : Text50
	},
	{},
	[
		"InvalidUsername"
	] 
)

define_request(
	"ResetTokenValidation",
	{
		"reset_token" : Text100
	},
	{},
	[
		"InvalidResetToken"
	] 
)

define_request(
	"ResetPassword",
	{
		"reset_token" : Text100,
		"new_password" : Text50
	},
	{},
	[
		"InvalidResetToken"
	] 
)

#
#	Client Groups
#
define_request(
	"SaveClientGroup",
	{
		"group_name": Text50,
        "country_ids": ListType(Int),
		"domain_ids": ListType(Int),
		"logo" : Text250,
		"contract_from": Text20,
		"contract_to": Text20,
		"incharge_persons": ListType(Int),
		"no_of_user_licence": Int,
		"file_space": Text50,
		"is_sms_subscribed": Int,
		"email_id": Text50,
		"date_configurations":ListType(DateConfiguration)
	},
	{},
	[
		"GroupNameAlreadyExists",
		"UsernameAlreadyExists"
	] 
)

define_request(
	"UpdateClientGroup",
	{
		"client_id": Int,
		"group_name": Text50,
        "country_ids": ListType(Int),
		"domain_ids": ListType(Int),
		"logo" : Text250,
		"contract_from": Text20,
		"contract_to": Text20,
		"incharge_persons": ListType(Int),
		"no_of_user_licence": Int,
		"file_space": Text50,
		"is_sms_subscribed": Int,
		"email_id": Text50,
		"date_configurations":ListType(DateConfiguration)
	},
	{},
	[
		"GroupNameAlreadyExists"
	] 
)

define_request(
	"ChangeClientGroupStatus",
	{
		"client_id": Int,
        "is_active": Int
	},
	{},
	[
		"InvalidClientId"
	] 
)

define_request(
	"GetClientGroups",
	{},
	{
		"countries":ListType(Country),
        "domains":ListType(Domain),
        "users":ListType(
        	DictType(
        		{
	                "user_id": Int,
	                "employee_name": Text50,
            	}		
        	)
        ),
        "client_list":ListType(
        	DictType(
        		{
	                "client_id": Int,
	                "client_name": Text50,
	                "incharge_persons": ListType(Int),
	                "country_ids": ListType(Int),
	                "domain_ids":ListType(Int),
	                "logo" : Text250,
	                "contract_from": Text20,
	                "contract_to": Text20,
	                "no_of_user_licence": Int,
	                "file_space": Text20,
	                "is_sms_subscribed": Int,
	                "date_configurations":ListType(DateConfiguration),
	                "username": Text50,
	                "is_active": Int
	            }
        	)
        )
	},
	[] 
)


#
# Request, RequestFrame
#

Request = VariantType("Request", DictType(_request_options))
RequestFrame = DictType({
	"session_token": Text50,
	"request": Request
})
