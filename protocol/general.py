from protocol.common import *

__all__ = [
	"Request", "Response"
]

NOTIFICATION_TEXT = Text500
EXTRA_DETAILS = Text500
DOMAIN_NAME = Text50
COUNTRY_NAME = Text50


#
# Request
#

UpdateUserProfile = RecordType("UpdateUserProfile", [
	Field("contact_no", CONTACT_NUMBER),
	Field("contact_no", ADDRESS)
])

GetDomains = RecordType("GetDomains", [
])

SaveDomain = RecordType("SaveDomain"),[
	Field("domain_name", DOMAIN_NAME)
])

UpdateDomain = RecordType("UpdateDomain"),[
	Field("domain_id", DOMAIN_ID),
	Field("domain_name", DOMAIN_NAME),

])

ChangeDomainStatus = RecordType("ChangeDomainStatus", [
	Field("domain_id", DOMAIN_ID),
	Field("is_active", IS_ACTIVE)
])

GetCountries = RecordType("GetCountries", [
])

SaveCountry = RecordType("SaveCountry"),[
	Field("country_name", COUNTRY_NAME)
])

UpdateCountry = RecordType("UpdateCountry"),[
	Field("country_id", COUNTRY_ID),
	Field("country_name", COUNTRY_NAME),

])

ChangeCountryStatus = RecordType("ChangeCountryStatus", [
	Field("country_id", COUNTRY_ID),
	Field("is_active", IS_ACTIVE)
])

GetNotifications = RecordType("GetNotifications", [
	Field("notification_type",  NOTIFICATION_TYPE)
])

UpdateNotificationStatus = RecordType("UpdateNotificationStatus", [
    
    Field("notification_id", NOTIFICATION_ID),
    Field("has_read", HAS_READ)
])

Request = VariantType("Request", [
	UpdateUserProfile, 
	GetDomains, SaveDomain, 
	UpdateDomain, ChangeDomainStatus, 
	GetCountries, SaveCountry, 
	UpdateCountry, ChangeCountryStatus, 
	GetNotifications, UpdateNotificationStatus
])

#
# Response
#

UpdateUserProfileSuccess = RecordType("UpdateUserProfileSuccess", [])

ContactNumberAlreadyExists = RecordType("ContactNumberAlreadyExists", [])

DomainList = VectorType(Domain)

GetDomainsSuccess = RecordType("GetDomainsSuccess", [
	Field("domains": DomainList)
])

SaveDomainSuccess = RecordType("SaveDomainSuccess", [])

DomainNameAlreadyExists = RecordType("DomainNameAlreadyExists", [])

UpdateDomainSuccess = RecordType("UpdateDomainSuccess", [])

InvalidDomainId = RecordType("InvalidDomainId", [])

ChangeDomainStatusSuccess = RecordType("ChangeDomainStatusSuccess", [])

CountryList = VectorType(Country)

GetCountriesSuccess = RecordType("GetCountriesSuccess", [
	Field("countries": CountryList)
])

SaveCountrySuccess = RecordType("SaveCountrySuccess", [])

CountryNameAlreadyExists = RecordType("CountryNameAlreadyExists", [])

UpdateCountrySuccess = RecordType("UpdateCountrySuccess", [])

InvalidCountryId = RecordType("InvalidCountryId", [])

ChangeCountryStatusSuccess = RecordType("ChangeCountryStatusSuccess", [])

Notification = RecordType("Notification", [
	Field("notification_id",  NOTIFICATION_ID),
	Field("notification_text", NOTIFICATION_TEXT),
	Field("extra_details": EXTRA_DETAILS),
	Field("has_read": HAS_READ),
	Field("date_and_time" : DATE_AND_TIME)
])

NotificationList = VectorType(Notification)

GetNotificationsSuccess = RecordType("GetNotificationsSuccess", [
	Field("notifications", NotificationList)
])

UpdateNotificationStatusSuccess = RecordType("UpdateNotificationStatusSuccess", [])

Response = VariantType("Response", [
	UpdateUserProfileSuccess, ContactNumberAlreadyExists,
	GetDomainsSuccess, 
	SaveDomainSuccess, DomainNameAlreadyExists,
	UpdateDomainSuccess, InvalidDomainId,
	ChangeDomainStatusSuccess,
	GetNotificationsSuccess,
	UpdateNotificationStatusSuccess
])
