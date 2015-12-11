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

GetUserGroups = Recordtype("GetUserGroups", [
])

SaveUserGroup = Recordtype("SaveUserGroup", [
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_type", FORM_TYPE),
	Field("form_ids", FormIdList)
])

UpdateUserGroup = Recordtype("UpdateUserGroup", [
	Field("user_group_id", USER_GROUP_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_type", FORM_TYPE),
	Field("form_ids", FormIdList)
])

ChangeUserGroupStatus = Recordtype("ChangeUserGroupStatus", [
	Field("user_group_id", USER_GROUP_ID),
	Field("is_active", IS_ACTIVE)
])

### User

GetUsers = Recordtype("GetUsers", [
])

SaveUser = Recordtype("SaveUser", [
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

UpdateUser = Recordtype("UpdateUser", [
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

ChangeUserStatus = Recordtype("ChangeUserStatus", [
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

GetUserGroupsSuccess = Recordtype("GetUserGroupsSuccess", [
	Field("forms", Maptype(Text50, Menu)),
	Field("user_groups", UserGroupList)
])

SaveUserGroupSuccess = Recordtype("SaveUserGroupSuccess", [
])

GroupNameAlreadyExists = Recordtype("GroupNameAlreadyExists", [
])

UpdateUserGroupSuccess = Recordtype("UpdateUserGroupSuccess", [
])

InvalidUserGroupId = Recordtype("InvalidUserGroupId", [
])

ChangeUserGroupStatusSuccess = Recordtype("ChangeUserGroupStatusSuccess", [
])

### User

GetUsersSuccess = Recordtype("GetUsersSuccess", [
	Field("user_groups", UserGroupList),
	Field("domains", DomainList),
	Field("users", UserDetailsList)
])

SaveUserSuccess = Recordtype("SaveUserSuccess", [
])

EmailIDAlreadyExists = Recordtype("EmailIDAlreadyExists", [
])

ContactNumberAlreadyExists = Recordtype("ContactNumberAlreadyExists", [
])

EmployeeCodeAlreadyExists = Recordtype("EmployeeCodeAlreadyExists", [
])

InvalidUserId = Recordtype("InvalidUserId", [
])

UpdateUserSuccess = Recordtype("UpdateUserSuccess", [
])

ChangeUserStatusSuccess = Recordtype("ChangeUserStatusSuccess", [
])

Response = VariantType("Response", [
	GetUserGroupsSuccess, SaveUserGroupSuccess,
	GroupNameAlreadyExists, UpdateUserGroupSuccess,
	InvalidUserGroupId, ChangeUserGroupStatusSuccess,
	GetUsersSuccess, SaveUserSuccess, EmailIDAlreadyExists,
	ContactNumberAlreadyExists, EmployeeCodeAlreadyExists,
	InvalidUserId, UpdateUserSuccess, ChangeUserStatusSuccess
])