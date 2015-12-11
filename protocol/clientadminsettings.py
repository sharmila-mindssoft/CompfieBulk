from protocol.common import *
# from protocol.core import (
# 	ActiveCompliance,
# 	UpcomingCompliance
# )

__all__ = [
	"Request", "Response"
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

#
# Response
#

LicenceHolder = RecordType("LicenceHolder", [
	Field("user_id", USER_ID),
	Field("user_name", Text100),
	Field("email_id", EMAIL_ID),
	Field("contact_no", CONTACT_NUMBER),
	Field("seating_unit_name", Text100),
	Field("address", ADDRESS),
	Field("total_disk_space", Int8),
	Field("used_disk_space", Int8),
])

ProfileDetails = RecordType("ProfileDetails", [
	Field("contract_from", Text20),
	Field("contract_to", Text20),
	Field("no_of_user_licence", Int8),
	Field("remaining_licence", Int8),
	Field("licence_holders", VectorType(LicenceHolder))
])

GetSettingsSuccess = RecordType("GetSettingsSuccess", [
	Field("is_two_levels_of_approval", Bool),
	Field("assignee_reminder_days", Int8),
	Field("escalation_reminder_In_advance_days", Int8),
	Field("escalation_reminder_days", Int8),
	Field("profile_detail", VectorType(ProfileDetails))
])

UpdateSettingsSuccess = RecordType("UpdateSettingsSuccess", [])

Response = VariantType("Response", [
	GetSettingsSuccess,
	UpdateSettingsSuccess
])