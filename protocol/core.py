from protocol.common import FORM_ID
__all__ = [
	"USER_TYPE", "APPROVAL_STATUS", "COMPLIANCE_APPROVAL_STATUS",
	"ASSIGN_STATUTORY_SUBMISSION_STATUS", 
	"ASSIGN_STATUTORY_SUBMISSION_TYPE", "NOTIFICATION_TYPE",
	"FILTER_TYPE", "COMPLIANCE_FREQUENCY", "COMPLIANCE_STATUS",
	"APPLICABILITY_STATUS", "FORM_TYPE", "REPEATS_TYPE",
	"DURATION_TYPE","Form", "Menu", "UserGroup", "Country", "Domain",
	"GeographyLevel", "Geography", "Industry", "StatutoryNature",
	"StatutoryLevel", "Statutory", "Compliance", "StatutoryMapping",
	"GroupCompany", "GroupCompanyDetail", "ClientConfiguration", 
	"BusinessGroup", "LegalEntity", "Division", "Unit", "ServiceProvider",
	"ClientUser", "AssignedStatutory", "ActiveCompliance", "UpcomingCompliance",
	"NumberOfCompliances", "ChartFilters", "ComplianceStatusDrillDown",
	"EscalationsDrillDown", "UserGroupDetails", "User"
]

# frm = EnumType("FORM_TYPE", [
# 	"IT", 
# 	"Knowledge",
# 	"Blah"
# ])

# Form = RecordType("Form", [
# 	Filed("form_id", FORM_ID),
# 	Filed("form_name", Text)
# ])

# Geography = RecordType("Geography",[fields...])

# FormList = StaticArrayType(Form, 100)
# FormListvector = VectorType(Form)


# Menu = RecordType("Menu", [
# 	Field("masters", FormList),
# 	Field("masters2", FormListvector),
# 	Field("masters3", Maptype(Text50, Form)),
# 	Filed("geographies", Maptype(COUNTry_ID, VectorType(Geography)))
# ])

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

ASSIGN_STATUTORY_SUBMISSION_STATUS = EnumType("ASSIGN_STATUTORY_SUBMISSION_STATUS", [
	"Submited", 
	"Pending"
])

ASSIGN_STATUTORY_SUBMISSION_TYPE = EnumType("ASSIGN_STATUTORY_SUBMISSION_TYPE", [
	"Submit", 
	"Save"
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

FormIdsList = VectorType(FORM_ID)
CountryIdsList = VectorType(COUNTRY_ID)
DomainIdsList = VectorType(DOMAIN_ID)
IndustryIdsList = VectorType(INDUSTRY_ID)
GeographyIdsList = VectorType(GEOGRAPHY_ID)
StatutoryIdsList = VectorType(STATUTORY_ID)
FormatFilesList = VectorType(FORMAT_FILE_NAME)

Form = RecordType("Form", [
	Filed("form_id", FORM_ID),
	Filed("form_name", FORM_NAME),
	Filed("form_url", URL),
	Filed("form_type", FORM_TYPE)
])

FormList = VectorType(Form)

StatutoryDate = RecordType("Form", [
	Filed("statutory_date", STATUTORY_DATE),
	Filed("statutory_month", STATUTORY_MONTH),
	Filed("trigger_before_days", Int8)
])

StatutoryDates = VectorType(StatutoryDate)

Menu = RecordType("Menu", [
	Filed("masters", FormList),
	Filed("transactions", FormList),
	Filed("reports", FormList),
	Filed("settings", FormList)
])

UserGroupDetails = RecordType("UserGroupDetails", [
	Filed("user_group_id", USER_GROUP_ID),
	Filed("user_group_name", USER_GROUP_NAME),
	Filed("form_ids", FormIdsList),
	Filed("is_active", IS_ACTIVE)
])

UserGroup = RecordType("UserGroup", [
	Filed("user_group_id", USER_GROUP_ID),
	Filed("user_group_name", USER_GROUP_NAME),
	Filed("is_active", IS_ACTIVE)
])

Country = RecordType("Country", [
	Filed("country_id", COUNTRY_ID),
	Filed("country_name", COUNTRY_NAME),
	Filed("is_active", IS_ACTIVE)
])

Domain = RecordType("Domain", [
	Filed("domain_id", DOMAIN_ID),
	Filed("domain_name", DOMAIN_NAME),
	Filed("is_active", IS_ACTIVE)
])

DomainList = VectorType(Domain)

GeographyLevel = RecordType("GeographyLevel", [
	Filed("level_id", GEOGRAPHY_LEVEL_ID),
	Filed("level_position", LEVEL_POSITION),
	Filed("level_name", LEVEL_NAME)
])

Geography = RecordType("Geography", [
	Filed("geography_id", GEOGRAPHY_ID),
	Filed("geography_name", GEOGRAPHY_NAME),
	Filed("level_id", GEOGRAPHY_LEVEL_ID),
	Filed("parent_ids", GeographyIdsList),
	Filed("is_active", IS_ACTIVE),
])

GeographyList = VectorType(Geography)

Industry = RecordType("Industry", [
	Filed("industry_id", INDUSTRY_ID),
	Filed("industry_name", INDUSTRY_NAME),
	Filed("is_active", IS_ACTIVE),
])

StatutoryNature = RecordType("StatutoryNature", [
	Filed("statutory_nature_id", STATUTORY_NATURE_ID),
	Filed("statutory_nature_name", STATUTORY_NATURE_NAME),
	Filed("is_active", IS_ACTIVE),
])

StatutoryLevel = RecordType("StatutoryLevel", [
	Filed("level_id", STATUTORY_LEVEL_ID),
	Filed("level_position", LEVEL_POSITION),
	Filed("level_name", LEVEL_NAME)
])

Statutory = RecordType("Statutory", [
	Filed("statutory_id", STATUTORY_ID),
	Filed("statutory_name", STATUTORY_NAME),
	Filed("level_id", STATUTORY_LEVEL_ID),
	Filed("parent_ids", StatutoryIdsList),
	Filed("is_active", IS_ACTIVE),
])

StatutoryList = VectorType(Statutory)

Compliance = RecordType("Compliance", [
	Filed("compliance_id", COMPLIANCE_ID),
    Filed("statutory_provision", STATUTORY_PROVISION),
    Filed("compliance_task", COMPLIANCE_NAME), 
    Filed("description", DESCRIPTION), 
    Filed("document_name", DOCUMENT_NAME), 
    Filed("format_file_name", FormatFilesList), 
    Filed("penal_description", DESCRIPTION), 
    Filed("compliance_frequency", COMPLIANCE_FREQUENCY), 
    Filed("statutory_dates", StatutoryDates),
    Filed("repeats_type", REPEATS_TYPE), 
    Filed("repeats_every", Int8), 
    Filed("duration_type", DURATION_TYPE),
    Filed("duration", Int8),
    Filed("is_active", IS_ACTIVE)
])

ComplianceList = VectorType(Compliance)

ComplianceApplicability = RecordType("ComplianceApplicability", [
	Filed("compliance_id", COMPLIANCE_ID),
	Filed("compliance_name", COMPLIANCE_NAME),
	Filed("description", DESCRIPTION), 
    Filed("statutory_provision" STATUTORY_PROVISION),
    Filed("statutory_nature", STATUTORY_NATURE_NAME), 
    Filed("compliance_applicable_status", STATUS), 
    Filed("compliance_opted_status", STATUS), 
    Filed("compliance_remarks", DESCRIPTION)
])

ComplianceApplicabilityList = VectorType(ComplianceApplicability)

StatutoryMapping = RecordType("StatutoryMapping", [
	Filed("statutory_mapping_id", STATUTORY_MAPPING_ID),
    Filed("country_id", COUNTRY_ID),
    Filed("domain_id", DOMAIN_ID), 
    Filed("industry_ids", IndustryIdsList), 
    Filed("statutory_nature_id", STATUTORY_NATURE_ID), 
    Filed("statutories", StatutoryList), 
    Filed("compliances", ComplianceList), 
    Filed("geographies", COMPLIANCE_FREQUENCY), 
    Filed("approval_status", StatutoryDates)
])

GroupCompany = RecordType("GroupCompany", [
	Filed("client_id", GROUP_ID),
    Filed("group_name", CLIENT_NAME),
])

GroupCompanyDetail = RecordType("GroupCompanyDetail", [
	Filed("client_id", GROUP_ID),
    Filed("group_name", CLIENT_NAME),
    Filed("domains", DomainList),
    Filed("logo", URL),
    Filed("contract_from", DATE),
    Filed("contract_to", DATE),
    Filed("no_of_user_licence", NO_OF_USER_LICENCE),
    Filed("total_disk_space", TOTAL_DISK_SPACE),
    Filed("is_sms_subscribed", Bool),
    Filed("username", USERNAME)
])

ClientConfiguration = RecordType("ClientConfiguration", [
	Filed("country_id", COUNTRY_ID),
    Filed("domain_id", DOMAIN_ID),
    Filed("period_from", Int8),
    Filed("period_to", Int8)
])

BusinessGroup = RecordType("BusinessGroup", [
	Filed("business_group_id", BUSINESS_GROUP_ID),
    Filed("business_group_name", BUSINESS_GROUP_NAME),
    Filed("client_id", GROUP_ID)
])

LegalEntity = RecordType("LegalEntity", [
	Filed("legal_entity_id", LEGAL_ENTITY_ID),
    Filed("legal_entity_name", BUSINESS_GROUP_NAME),
    Filed("business_group_id", BUSINESS_GROUP_ID),
    Filed("client_id", GROUP_ID)
])

Division = RecordType("Division", [
	Filed("division_id", DIVISION_ID),
	Filed("division_name", DIVISION_NAME),
	Filed("legal_entity_id", LEGAL_ENTITY_ID),
    Filed("business_group_id", BUSINESS_GROUP_ID),
    Filed("client_id", GROUP_ID)
])

Unit = RecordType("Unit", [
	Filed("unit_id", UNIT_ID),
	Filed("division_id", DIVISION_ID),
	Filed("legal_entity_id", LEGAL_ENTITY_ID),
    Filed("business_group_id", BUSINESS_GROUP_ID),
    Filed("client_id", GROUP_ID),
    Filed("country_id", COUNTRY_ID),
    Filed("geography_id", GEOGRAPHY_ID),
    Filed("unit_code", UNIT_CODE),
    Filed("unit_name", UNIT_NAME),
    Filed("industry_id", INDUSTRY_ID),
    Filed("unit_address", ADDRESS),
    Filed("postal_code", Int8),
    Filed("domain_ids", DomainIdsList),
    Filed("is_active", IS_ACTIVE),
])

ServiceProvider = RecordType("ServiceProvider", [
	 Filed("service_provider_id", SERVICE_PROVIDER_ID),
     Filed("service_provider_name", SERVICE_PROVIDER_NAME), 
     Filed("address", ADDRESS),
     Filed("contract_from", DATE),
     Filed("contract_to", DATE), 
     Filed("contact_person", Text50),
     Filed("contact_no", CONTACT_NUMBER),
     Filed("is_active", IS_ACTIVE)
])


User = RecordType("User", [
	Filed("user_id", USER_ID),
    Filed("email_id", EMAIL_ID),
    Filed("user_group_id", USER_GROUP_ID), 
    Filed("employee_name", EMPLOYEE_NAME),
    Filed("employee_code", EMPLOYEE_CODE),
    Filed("contact_no", CONTACT_NUMBER),
    Filed("address", ADDRESS),
    Filed("designation", DESIGNATION),
    Filed("country_ids",CountryIdsList),
    Filed("domain_ids", DomainIdsList),
    Filed("is_active", IS_ACTIVE)
])

ClientUser = RecordType("ClientUser", [
	Filed("user_id", USER_ID),
    Filed("email_id", EMAIL_ID),
    Filed("user_group_id", USER_GROUP_ID), 
    Filed("employee_name", EMPLOYEE_NAME),
    Filed("employee_code", EMPLOYEE_CODE),
    Filed("contact_no", CONTACT_NUMBER),
    Filed("seating_unit_id", UNIT_ID),
    Filed("seating_unit_name", UNIT_NAME),
    Filed("user_level", USER_LEVEL),
    Filed("country_ids",CountryIdsList),
    Filed("domain_ids", DomainIdsList),
    Filed("unit_ids", UnitIds),
    Filed("is_admin", STATUS),
    Filed("is_service_provider", STATUS),
    Filed("service_provider_id", SERVICE_PROVIDER_ID),
    Filed("is_active", IS_ACTIVE)
])

AssignedStatutory = RecordType("AssignedStatutory", [
	Filed("level_1_statutory_id", USER_ID),
    Filed("level_1_statutory_name", EMAIL_ID),
    Filed("compliances", ComplianceApplicabilityList), 
    Filed("applicable_status", STATUS),
    Filed("not_applicable_remarks", DESCRIPTION)
])

ActiveCompliance = RecordType("ActiveCompliance", [
	Filed("compliance_history_id", COMPLIANCE_HISTORY_ID),
    Filed("compliance_name", COMPLIANCE_NAME),
    Filed("compliance_frequency", COMPLIANCE_FREQUENCY), 
    Filed("domain_name", DOMAIN_NAME),
    Filed("start_date", DATE),
    Filed("due_date", DATE),
    Filed("compliance_status", STATUS),
    Filed("validity_date", DATE),
    Filed("next_due_date", DATE),
    Filed("ageing", Int8),
    Filed("format_file_name", FormatFilesList)
])

UpcomingCompliance = RecordType("UpcomingCompliance", [
	Filed("compliance_history_id", COMPLIANCE_HISTORY_ID),
    Filed("compliance_name", COMPLIANCE_NAME),
    Filed("compliance_frequency", COMPLIANCE_FREQUENCY), 
    Filed("domain_name", DOMAIN_NAME),
    Filed("start_date", DATE),
    Filed("due_date", DATE),
    Filed("format_file_name", FormatFilesList)
])

NumberOfCompliances = RecordType("NumberOfCompliances", [
	Filed("complied_count", Int8),
    Filed("delayed_compliance_count", Int8),
    Filed("inprogress_compliance_count", Int8), 
    Filed("not_complied_count", Int8)
])

ChartFilters = RecordType("ChartFilters", [
	Filed("country_id", COUNTRY_ID),
    Filed("domain_id", DOMAIN_ID),
    Filed("from_date", DATE), 
    Filed("to_date", DATE),
    Filed("filter_type", FILTER_TYPE),
    Filed("filter_id", Int8)
])

ComplianceShortDescription = RecordType("ComplianceShortDescription", [
	Filed("compliance_name", COMPLIANCE_NAME),
	Filed("description", DESCRIPTION), 
    Filed("assignee_name", EMPLOYEE_NAME),
    Filed("compliance_status", COMPLIANCE_STATUS),
    Filed("ageing", Int8)
])

ComplianceStatusDrillDown = RecordType("ComplianceStatusDrillDown", [
	Filed("unit_name", COUNTRY_ID),
    Filed("address", DOMAIN_ID),
    Filed("compliances", VectorType(ComplianceShortDescription))
])

EscalationsDrillDown = RecordType("EscalationsDrillDown", [
	Filed("unit_name", COUNTRY_ID),
    Filed("address", DOMAIN_ID),
    Filed("compliances", VectorType(ComplianceShortDescription))
])