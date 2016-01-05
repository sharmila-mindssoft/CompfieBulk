from basics.types import RecordType, VariantType, EnumType, CustomTextType, VectorType
from common import *
__all__ = [
	"SESSION_TYPE",
	"USER_TYPE", "APPROVAL_STATUS", "COMPLIANCE_APPROVAL_STATUS",
	"ASSIGN_STATUTORY_SUBMISSION_STATUS", 
	"ASSIGN_STATUTORY_SUBMISSION_TYPE", "NOTIFICATION_TYPE",
	"FILTER_TYPE", "COMPLIANCE_FREQUENCY", "COMPLIANCE_STATUS",
	"APPLICABILITY_STATUS", "FORM_TYPE", "REPEATS_TYPE",
	"DURATION_TYPE", "COMPLIANCE_ACTIVITY_STATUS",
	"KnowledgeForm", "Menu", "UserGroup", "Country", "Domain", "Level",
	"GeographyLevel", "Geography", "Industry", "StatutoryNature",
	"StatutoryLevel", "Statutory", "Compliance", "StatutoryMapping",
	"GroupCompany", "GroupCompanyDetail", "ClientConfiguration", 
	"BusinessGroup", "LegalEntity", "Division", "Unit", "UnitDetails", 
	"ServiceProvider", "ClientUser", "AssignedStatutory", 
	"ActiveCompliance", "UpcomingCompliance", "NumberOfCompliances", 
	"ChartFilters", "ComplianceStatusDrillDown","EscalationsDrillDown", 
	"UserGroupDetails", "User", "UserDetails", "CountryWiseUnits", 
	"ComplianceApplicability", "ComplianceShortDescription","StatutoryDate",
	"FormCategory", "FormType", "ComplianceFrequency", "ComplianceRepeatType",
	"ComplianceDurationType", "ComplianceApprovalStatus"
]

# frm = EnumType("FORM_TYPE", [
# 	"IT", 
# 	"Knowledge",
# 	"Blah"
# ])

# Form = RecordType("Form", [
# 	Field("form_id", FORM_ID),
# 	Field("form_name", Text)
# ])

# Geography = RecordType("Geography",[fields...])

# FormList = StaticArrayType(Form, 100)
# FormListvector = VectorType(Form)


# Menu = RecordType("Menu", [
# 	Field("masters", FormList),
# 	Field("masters2", FormListvector),
# 	Field("masters3", Maptype(Text50, Form)),
# 	Field("geographies", Maptype(COUNTry_ID, VectorType(Geography)))
# ])

SESSION_TYPE = EnumType ("SESSION_TYPE", [
	"Web",
	"Android",
	"IOS",
	"BlackBerry"
])

USER_TYPE = EnumType("USER_TYPE", [
	"Inhouse", 
	"ServiceProvider"
])

APPROVAL_STATUS = EnumType("APPROVAL_STATUS", [
	"Approve", 
	"Reject",
	"ApproveAndNotify"
])

COMPLIANCE_APPROVAL_STATUS = EnumType("COMPLIANCE_APPROVAL_STATUS", [
	"Concur", 
	"RejectConcurrence",
	"Approve",
	"RejectApproval"
])

COMPLIANCE_ACTIVITY_STATUS = EnumType("COMPLIANCE_ACTIVITY_STATUS", [
	"Submited",
	"Approved",
	"Rejected"
])

ASSIGN_STATUTORY_SUBMISSION_STATUS = EnumType("ASSIGN_STATUTORY_SUBMISSION_STATUS", [
	"Submited", 
	"Pending"
])

ASSIGN_STATUTORY_SUBMISSION_TYPE = EnumType("ASSIGN_STATUTORY_SUBMISSION_TYPE", [
	"Submit", 
	"Save"
])

NOTIFICATION_TYPE = EnumType("NOTIFICATION_TYPE", [
	"Notification", 
	"Reminder",
	"Escalation"
])

FILTER_TYPE = EnumType("FILTER_TYPE", [
	"Group", 
	"BusinessGroup",
	"LegalEntity",
	"Division",
	"Unit"
])

COMPLIANCE_FREQUENCY = EnumType("COMPLIANCE_FREQUENCY", [
	"OneTime", 
	"Periodical",
	"Review",
	"OnOccurrence"
])

COMPLIANCE_STATUS = EnumType("COMPLIANCE_STATUS", [
	"Complied", 
	"DelayedCompliance",
	"Inprogress",
	"NotComplied"
])

APPLICABILITY_STATUS = EnumType("APPLICABILITY_STATUS", [
	"Applicable", 
	"NotApplicable",
	"NotOpted"
])

FORM_TYPE = EnumType("FORM_TYPE", [
	"IT", 
	"Knowledge",
	"Techno",
	"Client",
	"ServiceProvider"
])

REPEATS_TYPE = EnumType("REPEATS_TYPE", [
	"Year", 
	"Month",
	"Day"
])

DURATION_TYPE = EnumType("DURATION_TYPE", [
	"Day", 
	"Hour"
])

FormIdList = VectorType(FORM_ID)
CountryIdList = VectorType(COUNTRY_ID)
DomainIdList = VectorType(DOMAIN_ID)
IndustryIdList = VectorType(INDUSTRY_ID)
GeographyIdList = VectorType(GEOGRAPHY_ID)
StatutoryIdList = VectorType(STATUTORY_ID)
FormatFilesList = VectorType(FORMAT_FILE_NAME)
UserIdList = VectorType(USER_ID)
UnitIdList = VectorType(UNIT_ID)

FormCategory = RecordType("FormCategory", [
	Field("form_category_id", FORM_CATEGORY_ID),
	Field("form_category", FORM_CATEGORY_NAME)
])

FormType = RecordType("FormType", [
	Field("form_type_id", FORM_TYPE_ID),
	Field("form_type", FORM_TYPE_NAME)
])

KnowledgeForm = RecordType("Form", [
	Field("form_id", FORM_ID),
	Field("form_name", FORM_NAME),
	Field("form_category_id", FORM_CATEGORY_ID),
	Field("form_type_id", FORM_TYPE_ID),
	Field("form_url", URL),
	Field("parent_menu", OptionalType(Text50)),
	Field("form_type", FORM_TYPE_NAME)
])

FormList = VectorType(KnowledgeForm)

Menu = RecordType("Menu", [
	Field("menus", MapType(FORM_TYPE_NAME, FormList)),
])

StatutoryDate = RecordType("StatutoryDate", [
	Field("statutory_date", STATUTORY_DATE),
	Field("statutory_month", STATUTORY_MONTH),
	Field("trigger_before_days", Int8)
])

StatutoryDates = VectorType(StatutoryDate)



UserGroupDetails = RecordType("UserGroupDetails", [
	Field("user_group_id", USER_GROUP_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_category_id", FORM_CATEGORY_ID),
	Field("form_ids", FormIdList),
	Field("is_active", IS_ACTIVE)
])

UserGroup = RecordType("UserGroup", [
	Field("user_group_id", USER_GROUP_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("is_active", IS_ACTIVE)
])

Country = RecordType("Country", [
	Field("country_id", COUNTRY_ID),
	Field("country_name", COUNTRY_NAME),
	Field("is_active", IS_ACTIVE)
])

CountryList = VectorType(Country)

Domain = RecordType("Domain", [
	Field("domain_id", DOMAIN_ID),
	Field("domain_name", DOMAIN_NAME),
	Field("is_active", IS_ACTIVE)
])

DomainList = VectorType(Domain)

Level = RecordType("Level", [
	Field("level_id", OptionalType(LEVEL_ID)),
	Field("level_position", LEVEL_POSITION),
	Field("level_name", LEVEL_NAME)
])


GeographyLevel = RecordType("GeographyLevel", [
	Field("level_id", GEOGRAPHY_LEVEL_ID),
	Field("level_position", LEVEL_POSITION),
	Field("level_name", LEVEL_NAME)
])

Geography = RecordType("Geography", [
	Field("geography_id", GEOGRAPHY_ID),
	Field("geography_name", GEOGRAPHY_NAME),
	Field("level_id", GEOGRAPHY_LEVEL_ID),
	Field("parent_ids", GeographyIdList),
	Field("parent_id", Int8),
	Field("is_active", IS_ACTIVE),
])

GeographyList = VectorType(Geography)

Industry = RecordType("Industry", [
	Field("industry_id", INDUSTRY_ID),
	Field("industry_name", INDUSTRY_NAME),
	Field("is_active", IS_ACTIVE),
])

StatutoryNature = RecordType("StatutoryNature", [
	Field("statutory_nature_id", STATUTORY_NATURE_ID),
	Field("statutory_nature_name", STATUTORY_NATURE_NAME),
	Field("is_active", IS_ACTIVE),
])

StatutoryLevel = RecordType("StatutoryLevel", [
	Field("level_id", STATUTORY_LEVEL_ID),
	Field("level_position", LEVEL_POSITION),
	Field("level_name", LEVEL_NAME)
])

Statutory = RecordType("Statutory", [
	Field("statutory_id", STATUTORY_ID),
	Field("statutory_name", STATUTORY_NAME),
	Field("level_id", STATUTORY_LEVEL_ID),
	Field("parent_ids", StatutoryIdList),
	Field("parent_id", Int8),
	Field("parent_mappings", Text),
])

StatutoryList = VectorType(Statutory)

Compliance = RecordType("Compliance", [
	Field("compliance_id",  OptionalType(COMPLIANCE_ID)),
    Field("statutory_provision", STATUTORY_PROVISION),
    Field("compliance_task", COMPLIANCE_NAME), 
    Field("description", DESCRIPTION), 
    Field("document_name", DOCUMENT_NAME), 
    Field("format_file_name", FormatFilesList), 
    Field("penal_description", DESCRIPTION), 
    Field("frequency_id", COMPLIANCE_FREQUENCY), 
    Field("statutory_dates", StatutoryDates),
    Field("repeats_type_id", REPEATS_TYPE_ID), 
    Field("repeats_every", Int8), 
    Field("duration_type_id", DURATION_TYPE_ID),
    Field("duration", Int8),
    Field("is_active", IS_ACTIVE)
])

ComplianceList = VectorType(Compliance)

ComplianceApplicability = RecordType("ComplianceApplicability", [
	Field("compliance_id", COMPLIANCE_ID),
	Field("compliance_name", COMPLIANCE_NAME),
	Field("description", DESCRIPTION), 
    Field("statutory_provision", STATUTORY_PROVISION),
    Field("statutory_nature", STATUTORY_NATURE_NAME), 
    Field("compliance_applicable_status", STATUS), 
    Field("compliance_opted_status", STATUS), 
    Field("compliance_remarks", DESCRIPTION)
])

ComplianceApplicabilityList = VectorType(ComplianceApplicability)

StatutoryMapping = RecordType("StatutoryMapping", [
	Field("country_id", COUNTRY_ID),
	Field("country_name", COUNTRY_NAME),
	Field("domain_id", DOMAIN_ID),
	Field("domain_name", DOMAIN_NAME),
	Field("industry_ids", VectorType(INDUSTRY_ID)),
	Field("industry_names", Text),
	Field("statutory_nature_id", STATUTORY_NATURE_ID),
	Field("statutory_nature_name", STATUTORY_NATURE_NAME),
	Field("statutory_ids", VectorType(STATUTORY_ID)),
	Field("statutory_mappings", VectorType(Text)),
	Field("compliances", VectorType(Compliance)),
	Field("compliance_names", VectorType(Text)),
	Field("geography_ids", VectorType(GEOGRAPHY_ID)),
	Field("geography_mappings", VectorType(Text)),
	Field("approval_status", APPROVAL_STATUS),
	Field("is_active", IS_ACTIVE)
])


GroupCompany = RecordType("GroupCompany", [
	Field("client_id", GROUP_ID),
    Field("group_name", CLIENT_NAME),
    Field("is_active", IS_ACTIVE),
    Field("country_ids", VectorType(COUNTRY_ID)),
    Field("domain_ids", VectorType(DOMAIN_ID)),
])

GroupCompanyDetail = RecordType("GroupCompanyDetail", [
	Field("client_id", GROUP_ID),
    Field("client_name", CLIENT_NAME),
    Field("domain_ids", DomainIdList),
    Field("country_ids", CountryIdList),
    Field("incharge_persons", UserIdList),
    Field("logo", URL),
    Field("contract_from", DATE),
    Field("contract_to", DATE),
    Field("no_of_user_licence", NO_OF_USER_LICENCE),
    Field("total_disk_space", TOTAL_DISK_SPACE),
    Field("is_sms_subscribed", Bool),
    Field("username", USERNAME),
    Field("is_active", IS_ACTIVE)
])

ClientConfiguration = RecordType("ClientConfiguration", [
	Field("country_id", COUNTRY_ID),
    Field("domain_id", DOMAIN_ID),
    Field("period_from", Int8),
    Field("period_to", Int8)
])

BusinessGroup = RecordType("BusinessGroup", [
	Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
    Field("business_group_name", BUSINESS_GROUP_NAME),
    Field("client_id", GROUP_ID)
])

LegalEntity = RecordType("LegalEntity", [
	Field("legal_entity_id", OptionalType(LEGAL_ENTITY_ID)),
    Field("legal_entity_name", LEGAL_ENTITY_NAME),
    Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
    Field("client_id", GROUP_ID)
])

Division = RecordType("Division", [
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("division_name", DIVISION_NAME),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
    Field("business_group_id", BUSINESS_GROUP_ID),
    Field("client_id", GROUP_ID)
])

UnitDetails = RecordType("UnitDetails", [
	Field("unit_id", OptionalType(UNIT_ID)),
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
    Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
    Field("client_id", GROUP_ID),
    Field("country_id", COUNTRY_ID),
    Field("geography_id", GEOGRAPHY_ID),
    Field("unit_code", UNIT_CODE),
    Field("unit_name", UNIT_NAME),
    Field("industry_id", INDUSTRY_ID),
    Field("unit_address", ADDRESS),
    Field("postal_code", Int8),
    Field("domain_ids", DomainIdList),
    Field("is_active", IS_ACTIVE)
])

UnitDetailsList = VectorType(UnitDetails)

Unit = RecordType("Unit", [
	Field("unit_id", OptionalType(UNIT_ID)),
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
    Field("business_group_id",OptionalType(BUSINESS_GROUP_ID)),
    Field("client_id", GROUP_ID),
    Field("unit_code", UNIT_CODE),
    Field("unit_name", UNIT_NAME),
    Field("unit_address", ADDRESS),
    Field("is_active", IS_ACTIVE),
])

CountryWiseUnits = RecordType("CountryWiseUnits", [
	Field("country_id", COUNTRY_ID),
	Field("units", UnitDetailsList),
])

ServiceProvider = RecordType("ServiceProvider", [
	 Field("service_provider_id", OptionalType(SERVICE_PROVIDER_ID)),
     Field("service_provider_name", SERVICE_PROVIDER_NAME), 
     Field("address", ADDRESS),
     Field("contract_from", DATE),
     Field("contract_to", DATE), 
     Field("contact_person", Text50),
     Field("contact_no", CONTACT_NUMBER),
     Field("is_active", OptionalType(IS_ACTIVE))
])


UserDetails = RecordType("UserDetails", [
	Field("user_id", USER_ID),
    Field("email_id", EMAIL_ID),
    Field("user_group_id", USER_GROUP_ID), 
    Field("employee_name", EMPLOYEE_NAME),
    Field("employee_code", EMPLOYEE_CODE),
    Field("contact_no", CONTACT_NUMBER),
    Field("address", ADDRESS),
    Field("designation", DESIGNATION),
    Field("country_ids",CountryIdList),
    Field("domain_ids", DomainIdList),
    Field("is_active", IS_ACTIVE)
])

User = RecordType("User", [
	Field("user_id", USER_ID),
    Field("employee_name", EMPLOYEE_NAME),
    Field("is_active", IS_ACTIVE)
])

ClientUser = RecordType("ClientUser", [
	Field("user_id", USER_ID),
    Field("email_id", EMAIL_ID),
    Field("user_group_id", USER_GROUP_ID), 
    Field("employee_name", EMPLOYEE_NAME),
    Field("employee_code", EMPLOYEE_CODE),
    Field("contact_no", CONTACT_NUMBER),
    Field("seating_unit_id", UNIT_ID),
    Field("seating_unit_name", UNIT_NAME),
    Field("user_level", USER_LEVEL),
    Field("country_ids",CountryIdList),
    Field("domain_ids", DomainIdList),
    Field("unit_ids", UnitIdList),
    Field("is_admin", STATUS),
    Field("is_service_provider", STATUS),
    Field("service_provider_id", SERVICE_PROVIDER_ID),
    Field("is_active", IS_ACTIVE)
])

AssignedStatutory = RecordType("AssignedStatutory", [
	Field("level_1_statutory_id", USER_ID),
    Field("level_1_statutory_name", LEVEL_1_STATUTORY_NAME),
    Field("compliances", ComplianceApplicabilityList), 
    Field("applicable_status", STATUS),
    Field("not_applicable_remarks", DESCRIPTION)
])

ActiveCompliance = RecordType("ActiveCompliance", [
	Field("compliance_history_id", COMPLIANCE_HISTORY_ID),
    Field("compliance_name", COMPLIANCE_NAME),
    Field("compliance_frequency", COMPLIANCE_FREQUENCY), 
    Field("domain_name", DOMAIN_NAME),
    Field("start_date", DATE),
    Field("due_date", DATE),
    Field("compliance_status", STATUS),
    Field("validity_date", DATE),
    Field("next_due_date", DATE),
    Field("ageing", Int8),
    Field("format_file_name", FormatFilesList)
])

UpcomingCompliance = RecordType("UpcomingCompliance", [
	Field("compliance_history_id", COMPLIANCE_HISTORY_ID),
    Field("compliance_name", COMPLIANCE_NAME),
    Field("compliance_frequency", COMPLIANCE_FREQUENCY), 
    Field("domain_name", DOMAIN_NAME),
    Field("start_date", DATE),
    Field("due_date", DATE),
    Field("format_file_name", FormatFilesList)
])

NumberOfCompliances = RecordType("NumberOfCompliances", [
	Field("complied_count", Int8),
    Field("delayed_compliance_count", Int8),
    Field("inprogress_compliance_count", Int8), 
    Field("not_complied_count", Int8)
])

ChartFilters = RecordType("ChartFilters", [
	Field("country_id", COUNTRY_ID),
    Field("domain_id", DOMAIN_ID),
    Field("from_date", DATE), 
    Field("to_date", DATE),
    Field("filter_type", FILTER_TYPE),
    Field("filter_id", Int8)
])

ComplianceShortDescription = RecordType("ComplianceShortDescription", [
	Field("compliance_name", COMPLIANCE_NAME),
	Field("description", DESCRIPTION), 
    Field("assignee_name", EMPLOYEE_NAME),
    Field("compliance_status", COMPLIANCE_STATUS),
    Field("ageing", Int8)
])

ComplianceStatusDrillDown = RecordType("ComplianceStatusDrillDown", [
	Field("unit_name", COUNTRY_ID),
    Field("address", DOMAIN_ID),
    Field("compliances", VectorType(ComplianceShortDescription))
])

EscalationsDrillDown = RecordType("EscalationsDrillDown", [
	Field("unit_name", COUNTRY_ID),
    Field("address", DOMAIN_ID),
    Field("compliances", VectorType(ComplianceShortDescription))
])

ComplianceFrequency = RecordType("ComplianceFrequency", [
	Field("frequency_id", FREQUENCY_ID),
	Field("frequency", COMPLIANCE_FREQUENCY)
])

ComplianceRepeatType = RecordType("ComplianceRepeatType", [
	Field("repeat_type_id", REPEATS_TYPE_ID),
	Field("repeat_type", REPEATS_TYPE)
])

ComplianceDurationType = RecordType("ComplianceDurationType", [
	Field("duration_type_id", DURATION_TYPE_ID),
	Field("duration_type", DURATION_TYPE)
])

ComplianceApprovalStatus = RecordType("ComplianceApprovalStatus", [
	Field("approval_status_id", APPROVAL_STATUS_ID),
	Field("approval_status", APPROVAL_STATUS)
])