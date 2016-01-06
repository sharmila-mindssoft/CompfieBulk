from basics.types import RecordType, VectorType, Field, VariantType, MapType
from core import Menu, UserGroup, Domain, Country, UserDetails,FORM_TYPE, FormCategory
from common import (Text50, FORM_ID, FORM_CATEGORY_ID, COUNTRY_ID, DOMAIN_ID, USER_GROUP_ID, USER_GROUP_NAME,  
	IS_ACTIVE, USER_ID, EMAIL_ID, EMPLOYEE_NAME, EMPLOYEE_CODE, CONTACT_NUMBER, ADDRESS, DESIGNATION, SESSION_TOKEN)

__all__=  [
	"Request", "Response", "RequestFormat", "UserGroupDetail"
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
	Field("form_category_id", FORM_CATEGORY_ID),
	Field("form_ids", FormIdList)
])

UpdateUserGroup = RecordType("UpdateUserGroup", [
	Field("user_group_id", USER_GROUP_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_category_id", FORM_CATEGORY_ID),
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

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])

#	
#	Response
#

### User Group

UserGroupDetail = RecordType("UserGroupDetail", [
	Field("user_group_id", USER_GROUP_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_category_id", FORM_CATEGORY_ID),
	Field("form_ids", VectorType(FORM_ID)),
	Field("is_active", IS_ACTIVE)
])

GetUserGroupsSuccess = RecordType("GetUserGroupsSuccess", [
	Field("form_categories", VectorType(FormCategory) ),
	Field("forms", MapType(FORM_CATEGORY_ID, Menu)),
	Field("user_groups", VectorType(UserGroupDetail))
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
	Field("countries", CountryList),
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