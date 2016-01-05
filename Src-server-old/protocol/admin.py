from basics.types import RecordType, VectorType, Field, VariantType, MapType
from core import Menu, UserGroup, Domain, Country, UserDetails,FORM_TYPE
from common import (Text50, FORM_ID,  COUNTRY_ID, DOMAIN_ID, USER_GROUP_ID, USER_GROUP_NAME,  
	IS_ACTIVE, USER_ID, EMAIL_ID, EMPLOYEE_NAME, EMPLOYEE_CODE, CONTACT_NUMBER, ADDRESS, DESIGNATION)

__all__=  [
	"Request", "Response"
]

FormIdList = VectorType(FORM_ID)
CountryIdList = VectorType(COUNTRY_ID)
DomainIdList = VectorType(DOMAIN_ID)
UserGroupList = VectorType(UserGroup)
DomainList = VectorType(Domain)
CountryList = VectorType(Country)
UserDetailsList = VectorType(UserDetails)

#	
#	Request
#

### User Groups

GetUserGroups = RecordType("GetUserGroups", [
])

SaveUserGroup = RecordType("SaveUserGroup", [
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_type", FORM_TYPE),
	Field("form_ids", FormIdList)
])

UpdateUserGroup = RecordType("UpdateUserGroup", [
	Field("user_group_id", USER_GROUP_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_type", FORM_TYPE),
	Field("form_ids", FormIdList)
])

ChangeUserGroupStatus = RecordType("ChangeUserGroupStatus", [
	Field("user_group_id", USER_GROUP_ID),
	Field("is_active", IS_ACTIVE)
])

### User

GetUsers = RecordType("GetUsers", [
])

SaveUser = RecordType("SaveUser", [
	Field("email_id", EMAIL_ID),
    Field("user_group_id", USER_GROUP_ID),
    Field("employee_name", EMPLOYEE_NAME),
    Field("employee_code", EMPLOYEE_CODE),
    Field("contact_no", CONTACT_NUMBER),
    Field("address", ADDRESS), 
    Field("designation", DESIGNATION),
    Field("country_ids", CountryIdList),
    Field("domain_ids", DomainIdList)

])

UpdateUser = RecordType("UpdateUser", [
	Field("user_id", USER_ID),
    Field("user_group_id", USER_GROUP_ID),
    Field("employee_name", EMPLOYEE_NAME),
    Field("employee_code", EMPLOYEE_CODE),
    Field("contact_no", CONTACT_NUMBER),
    Field("address", ADDRESS), 
    Field("designation", DESIGNATION),
    Field("country_ids", CountryIdList),
    Field("domain_ids", DomainIdList)

])

ChangeUserStatus = RecordType("ChangeUserStatus", [
	Field("user_id", USER_ID),
	Field("is_active", IS_ACTIVE)
])

Request = VariantType("Request", [
	GetUserGroups, SaveUserGroup, UpdateUserGroup,
	ChangeUserGroupStatus, GetUsers, SaveUser,UpdateUser,
	ChangeUserStatus
])

#	
#	Response
#

### User Group

GetUserGroupsSuccess = RecordType("GetUserGroupsSuccess", [
	Field("forms", MapType(Text50, Menu)),
	Field("user_groups", UserGroupList)
])

SaveUserGroupSuccess = RecordType("SaveUserGroupSuccess", [
])

GroupNameAlreadyExists = RecordType("GroupNameAlreadyExists", [
])

UpdateUserGroupSuccess = RecordType("UpdateUserGroupSuccess", [
])

InvalidUserGroupId = RecordType("InvalidUserGroupId", [
])

ChangeUserGroupStatusSuccess = RecordType("ChangeUserGroupStatusSuccess", [
])

### User

GetUsersSuccess = RecordType("GetUsersSuccess", [
	Field("user_groups", UserGroupList),
	Field("domains", DomainList),
	Field("users", UserDetailsList)
])

SaveUserSuccess = RecordType("SaveUserSuccess", [
])

EmailIDAlreadyExists = RecordType("EmailIDAlreadyExists", [
])

ContactNumberAlreadyExists = RecordType("ContactNumberAlreadyExists", [
])

EmployeeCodeAlreadyExists = RecordType("EmployeeCodeAlreadyExists", [
])

InvalidUserId = RecordType("InvalidUserId", [
])

UpdateUserSuccess = RecordType("UpdateUserSuccess", [
])

ChangeUserStatusSuccess = RecordType("ChangeUserStatusSuccess", [
])

Response = VariantType("Response", [
	GetUserGroupsSuccess, SaveUserGroupSuccess,
	GroupNameAlreadyExists, UpdateUserGroupSuccess,
	InvalidUserGroupId, ChangeUserGroupStatusSuccess,
	GetUsersSuccess, SaveUserSuccess, EmailIDAlreadyExists,
	ContactNumberAlreadyExists, EmployeeCodeAlreadyExists,
	InvalidUserId, UpdateUserSuccess, ChangeUserStatusSuccess
])