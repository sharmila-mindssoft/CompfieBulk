from basics.types import RecordType, Field, Bool, VariantType, VectorType
from common import (Int8, Text20, Text100, REMINDER_DAYS, USER_ID, EMAIL_ID,
		CONTACT_NUMBER, ADDRESS, SESSION_TOKEN)

__all__ = [
	"Request", "Response", "RequestFormat", "PROFILE_DETAIL", "LICENCE_HOLDER"
]

#
# Request
#

GetSettings = RecordType("GetSettings", [])

UpdateSettings = RecordType("UpdateSettings", [
	Field("is_two_levels_of_approval", Bool),
	Field("assignee_reminder_days", REMINDER_DAYS),
	Field("escalation_reminder_In_advance_days", REMINDER_DAYS),
	Field("escalation_reminder_days", REMINDER_DAYS)
])

Request = VariantType("Request", [
	GetSettings,
	UpdateSettings
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])


#
# Response
#

LICENCE_HOLDER = RecordType("LICENCE_HOLDER", [
	Field("user_id", USER_ID),
	Field("user_name", Text100),
	Field("email_id", EMAIL_ID),
	Field("contact_no", CONTACT_NUMBER),
	Field("seating_unit_name", Text100),
	Field("address", ADDRESS),
	Field("total_disk_space", Int8),
	Field("used_disk_space", Int8),
])

PROFILE_DETAIL = RecordType("PROFILE_DETAIL", [
	Field("contract_from", Text20),
	Field("contract_to", Text20),
	Field("no_of_user_licence", Int8),
	Field("remaining_licence", Int8),
	Field("licence_holders", VectorType(LICENCE_HOLDER))
])

GetSettingsSuccess = RecordType("GetSettingsSuccess", [
	Field("is_two_levels_of_approval", Bool),
	Field("assignee_reminder_days", Int8),
	Field("escalation_reminder_In_advance_days", Int8),
	Field("escalation_reminder_days", Int8),
	Field("profile_detail", VectorType(PROFILE_DETAIL))
])

UpdateSettingsSuccess = RecordType("UpdateSettingsSuccess", [])

Response = VariantType("Response", [
	GetSettingsSuccess,
	UpdateSettingsSuccess
])