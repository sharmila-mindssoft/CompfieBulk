__all__=  [
	"Request", "Response"
]

#	
#	Request
#

### User Groups

GetUserGroups = Recordtype("GetUserGroups", [
])

SaveUserGroup = Recordtype("SaveUserGroup", [
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_type", FORM_TYPE),
	Field("form_ids", VectorType(FORM_ID))
])

UpdateUserGroup = Recordtype("UpdateUserGroup", [
	Field("user_group_id", USER_GROUP_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_type", FORM_TYPE),
	Field("form_ids", VectorType(FORM_ID))
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
    Field("country_ids", VectorType(COUNTRY_ID)),
    Field("domain_ids", VectorType(DOMAIN_ID))

])

UpdateUser = Recordtype("UpdateUser", [
	Field("user_id", USER_ID),
    Field("user_group_id", USER_GROUP_ID),
    Field("employee_name", EMPLOYEE_NAME),
    Field("employee_code", EMPLOYEE_CODE),
    Field("contact_no", CONTACT_NUMBER),
    Field("address", ADDRESS), 
    Field("designation", DESIGNATION),
    Field("country_ids", VectorType(COUNTRY_ID)),
    Field("domain_ids", VectorType(DOMAIN_ID))

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
	Field("user_groups", VectorType(UserGroup))
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
	Field("user_groups", VectorType(UserGroup)),
	Field("domains", VectorType(Domain)),
	Field("users", VectorType(User))
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