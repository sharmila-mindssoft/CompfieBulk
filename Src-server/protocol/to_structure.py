from sets import Set
from protocol.jsonvalidators import (
    parse_bool,
    parse_number,
    parse_point_numbers,
    parse_string,
    parse_custom_string,
    parse_bytes,
    parse_list,
    parse_dictionary,
    parse_enum,
    parse_date
)

def to_structure_VectorType_RecordType_clientreport_User(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_User(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_UnitName(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_UnitName(item))
    return lst

def to_structure_RecordType_knowledgemaster_Request_GetStatutoryNatures(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_VectorType_RecordType_general_Notification(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_general_Notification(item))
    return lst

def to_structure_VectorType_RecordType_general_User(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_general_User(item))
    return lst

def to_structure_VectorType_RecordType_general_AuditTrail(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_general_AuditTrail(item))
    return lst

def to_structure_VectorType_RecordType_general_AuditTrailForm(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_general_AuditTrailForm(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_ComplianceName(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ComplianceName(item))
    return lst

def to_structure_RecordType_general_Response_GetNotificationsSuccess(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_Level1Statutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_Level1Statutory(item))
    return lst

def to_structure_VectorType_RecordType_core_Level1Statutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Level1Statutory(item))
    return lst

def to_structure_VectorType_RecordType_client_transactions_IndustryWiseUnits(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_client_transactions_IndustryWiseUnits(item))
    return lst


def to_structure_VectorType_RecordType_clientreport_UserName(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_UserName(item))
    return lst

def to_structure_VariantType_general_Response(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetReassignComplianceTaskReportFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_technomasters_Request_ChangeClientStatus(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_OptionalType_VectorType_SignedIntegerType_8(data):
    if data is None: return data
    return to_structure_VectorType_SignedIntegerType_8(data)

def to_structure_VectorType_UnsignedIntegerType_32(data):
    return to_structure_VectorType_UnignedIntegerType_32(data)

def to_structure_OptionalType_CustomTextType_50(data):
    if data is None: return data
    return to_structure_CustomTextType_50(data)

def to_structure_OptionalType_CustomTextType_500(data):
    if data is None: return data
    return to_structure_CustomTextType_500(data)


def to_structure_RecordType_technotransactions_Response_GetAssignedStatutoriesByIdSuccess(data):
    from protocol import technotransactions
    return technotransactions.Response.to_structure(data)

def to_structure_VariantType_knowledgemaster_Request(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_technoreports_Request_GetClientDetailsReportData(data):
    from protocol import technoreports
    return technoreports.Request.to_structure(data)

def to_structure_OptionalType_SignedIntegerType_8(data):
    if data is None: return data
    return to_structure_SignedIntegerType_8(data)

def to_structure_RecordType_clientreport_ReassignHistory(data):
    from protocol import clientreport
    return clientreport.ReassignHistory.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_UpdateStatutory(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_general_Notification(data):
    from protocol import general
    return general.Notification.to_structure(data)

def to_structure_RecordType_general_User(data):
    from protocol import core
    return core.User.to_structure(data)

def to_structure_RecordType_general_AuditTrail(data):
    from protocol import general
    return general.AuditTrail.to_structure(data)

def to_structure_RecordType_general_AuditTrailForm(data):
    from protocol import general
    return general.AuditTrailForm.to_structure(data)

def to_structure_RecordType_technoreports_Request_GetAssignedStatutoryReportFilters(data):
    from protocol import technoreports
    return technoreports.Request.to_structure(data)

def to_structure_RecordType_general_Request_UpdateUserProfile(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_VectorType_SignedIntegerType_8(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_SignedIntegerType_8(item))
    return lst

def to_structure_VectorType_UnignedIntegerType_32(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_UnsignedIntegerType_32(item))
    return lst

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_core_Unit(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_core_Unit(value)
        dict.append([key, value])
    return dict

def to_structure_MapType_UnsignedInteger_32_VectorType_RecordType_technomaster_UnitDetails(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_UnsignedIntegerType_32(key)
        value = to_structure_VectorType_RecordType_techno_master_UnitDetails(value)
        dict[key] = value
    return dict

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_core_Form(data):
    data = parse_dictionary(data)
    dict = {}
    # for key, value in data.items():
    #     key = to_structure_CustomTextType_50(key)
    #     value = to_structure_VectorType_RecordType_core_Form(value)
    #     dict.append([key, value])
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_core_Form(value)
        dict[key] = value        
    return dict

def to_structure_VectorType_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_ReassignHistory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ReassignHistory(item))
    return lst

def to_structure_RecordType_dashboard_TrendData(data):
    from protocol import dashboard
    return dashboard.TrendData.to_structure(data)

def to_structure_RecordType_clientreport_ReassignCompliance(data):
    from protocol import clientreport
    return clientreport.ReassignCompliance.to_structure(data)

def to_structure_RecordType_technotransactions_Response_GetAssignedStatutoryWizardOneDataSuccess(data):
    from protocol import technotransactions
    return technotransactions.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ReassignCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ReassignCompliance(item))
    return lst

def to_structure_RecordType_clientadminsettings_Response_GetSettingsSuccess(data):
    from protocol import clientadminsettings
    return clientadminsettings.Response.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetReassignComplianceTaskDetailsSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_dashboard_Response_GetNotCompliedChartSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_Country(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Country(item))
    return lst

def to_structure_Bool(data):
    return parse_bool(data)

def to_structure_RecordType_dashboard_Request_GetChartFilters(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_VectorType_RecordType_core_BusinessGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_BusinessGroup(item))
    return lst

def to_structure_VectorType_RecordType_core_ClientBusinessGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ClientBusinessGroup(item))
    return lst

def to_structure_VectorType_RecordType_core_UserGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_UserGroup(item))
    return lst

def to_structure_VectorType_RecordType_client_masters_ClientUserGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_client_masters_ClientUserGroup(item))
    return lst    

def to_structure_VectorType_RecordType_core_LegalEntity(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_LegalEntity(item))
    return lst

def to_structure_VectorType_RecordType_core_ClientLegalEntity(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ClientLegalEntity(item))
    return lst

def to_structure_VectorType_RecordType_core_ClientConfiguration(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ClientConfiguration(item))
    return lst

def to_structure_SignedIntegerType_8(data):
    return parse_number(data, -128, 127)

def to_structure_UnsignedIntegerType_32(data):
    return parse_number(data, 0, 4294967295)

def to_structure_OptionalType_UnsignedIntegerType_32(data):
    if data is None : return data
    return to_structure_UnsignedIntegerType_32(data)

def to_structure_VectorType_RecordType_core_Division(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Division(item))
    return lst

def to_structure_VectorType_RecordType_core_ClientDivision(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ClientDivision(item))
    return lst

def to_structure_RecordType_knowledgemaster_Response_InvalidGeographyId(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_SaveGeographyLevel(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_VectorType_RecordType_core_GeographyLevel(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_GeographyLevel(item))
    return lst

def to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_core_Industry(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Industry(item))
    return lst

def to_structure_RecordType_clientreport_Response_GetTaskApplicabilityStatusFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_VariantType_technomasters_Request(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_Geography(value)
        dict[key] = value
    return dict

def to_structure_RecordType_knowledgemaster_Request_SaveGeography(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_dashboard_CompliedMap(data):
    from protocol import dashboard
    return dashboard.CompliedMap.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_USERWISESTATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_USERWISESTATUTORIES(item))
    return lst

def to_structure_Float(data):
    return parse_point_numbers(data)

def to_structure_VariantType_admin_Response(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_Geography(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Geography(item))
    return lst

def to_structure_RecordType_technoreports_Response_GetClientDetailsReportFiltersSuccess(data):
    from protocol import technoreports
    return technoreports.Response.to_structure(data)

def to_structure_RecordType_clientreport_ComplianceList(data):
    from protocol import clientreport
    return clientreport.ComplianceList.to_structure(data)

def to_structure_RecordType_technoreports_Response_GetClientDetailsReportDataSuccess(data):
    from protocol import technoreports
    return technoreports.Response.to_structure(data)

def to_structure_VectorType_CustomTextType_20(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_CustomTextType_20(item))
    return lst

def to_structure_Text(data):
    return parse_string(data)

def to_structure_VectorType_CustomTextType_50(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_CustomTextType_50(item))
    return lst

def to_structure_OptionalType_VectorType_CustomTextType_50(data):
    if data is None: return data
    return to_structure_VectorType_CustomTextType_50(data)


def to_structure_VectorType_RecordType_clientreport_ComplianceList(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ComplianceList(item))
    return lst

def to_structure_RecordType_clientreport_ApplicabilityCompliance(data):
    from protocol import clientreport
    return clientreport.ApplicabilityCompliance.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ApplicabilityCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ApplicabilityCompliance(item))
    return lst

def to_structure_RecordType_core_EscalationsDrillDown(data):
    from protocol import core
    return core.EscalationsDrillDown.to_structure(data)

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_clientreport_ApplicabilityCompliance(value)
        dict.append([key, value])
    return dict

def to_structure_RecordType_knowledgemaster_Request_SaveIndustry(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(item))
    return lst

def to_structure_RecordType_knowledgemaster_Request_UpdateIndustry(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_technomasters_RequestFormat(data):
    from protocol import technomasters
    return technomasters.RequestFormat.to_structure(data)

def to_structure_VectorType_RecordType_core_ServiceProvider(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ServiceProvider(item))
    return lst

def to_structure_VectorType_RecordType_core_ServiceProviderDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ServiceProviderDetails(item))
    return lst

def to_structure_MapType_SignedIntegerType_8_RecordType_core_Statutory(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_RecordType_core_Statutory(value)
        dict.append([key, value])
    return dict

def to_structure_RecordType_knowledgemaster_Request_ChangeIndustryStatus(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Response_SaveUserPrivilegesSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetComplianceTaskApplicabilityStatusReportSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_SaveStatutoryNature(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_VectorType_RecordType_core_Domain(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Domain(item))
    return lst

def to_structure_RecordType_clienttransactions_Request_SaveAssignedCompliance(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_CustomTextType_20(data):
    return parse_custom_string(data, 20)

def to_structure_RecordType_clienttransactions_Request_GetUserwiseCompliances(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_RecordType_admin_Response_UpdateUserGroupSuccess(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.REASSIGNED_COMPLIANCE.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Request_ChangeStatutoryMappingStatus(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_DuplicateGeographyLevelsExists(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_technotransactions_ASSIGNED_STATUTORIES(data):
    from protocol import technotransactions
    return technotransactions.ASSIGNED_STATUTORIES.to_structure(data)

def to_structure_RecordType_technomasters_Response_GetClientsSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_GroupCompany(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_GroupCompany(item))
    return lst

def to_structure_VectorType_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(item))
    return lst

def to_structure_RecordType_technomasters_Response_BusinessGroupNameAlreadyExists(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_VectorType_Text(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_Text(item))
    return lst

def to_structure_RecordType_technomasters_Response_LegalEntityNameAlreadyExists(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_technomasters_Response_DivisionNameAlreadyExists(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_CustomTextType_100(data):
    return parse_custom_string(data, 100)

def to_structure_RecordType_clienttransactions_Response_GetStatutoriesByUnitSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_technomasters_Response_UnitNameAlreadyExists(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_general_Request_GetDomains(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_technoreports_Request_GetStatutoryNotifications(data):
    from protocol import technoreports
    return technoreports.Request.to_structure(data)

def to_structure_RecordType_technomasters_Response_LogoSizeLimitExceeds(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Request_ApproveCompliance(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_Request_GetPastRecordsFormData(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_CustomTextType_250(data):
    return parse_custom_string(data, 250)

def to_structure_RecordType_general_Request_UpdateDomain(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_general_Request_ChangeDomainStatus(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_dashboard_Request_GetComplianceStatusChart(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_Request_GetStatutoriesByUnit(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_OptionalType_Bool(data):
    if data is None: return data
    return to_structure_Bool(data)

def to_structure_RecordType_clienttransactions_Response_SavePastRecordsSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_general_Request_SaveCountry(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_core_ServiceProvider(data):
    from protocol import core
    return core.ServiceProvider.to_structure(data)

def to_structure_RecordType_core_ServiceProviderDetails(data):
    from protocol import core
    return core.ServiceProviderDetails.to_structure(data)

def to_structure_RecordType_technomasters_LICENCE_HOLDER_DETAILS(data):
    from protocol import technomasters
    return technomasters.LICENCE_HOLDER_DETAILS.to_structure(data)

def to_structure_RecordType_general_Request_UpdateCountry(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_technomasters_Response_SaveClientGroupSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.PAST_RECORD_COMPLIANCE.to_structure(data)

def to_structure_VariantType_clienttransactions_Response(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_general_Request_ChangeCountryStatus(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_admin_Response_InvalidUserGroupId(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(value)
        dict[key] = value
    return dict

def to_structure_CustomTextType_50(data):
    return parse_custom_string(data, 50)

def to_structure_RecordType_clienttransactions_Request_SavePastRecords(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_VariantType_clienttransactions_Request(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_SaveStatutory(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_CustomTextType_500(data):
    return parse_custom_string(data, 500)

def to_structure_RecordType_technomasters_PROFILE_DETAIL(data):
    from protocol import technomasters
    return technomasters.PROFILE_DETAIL.to_structure(data)

def to_structure_RecordType_clienttransactions_RequestFormat(data):
    from protocol import clienttransactions
    return clienttransactions.RequestFormat.to_structure(data)

def to_structure_CustomIntegerType_1_10(data):
    return parse_number(data, 1, 10)

def to_structure_CustomIntegerType_1_100(data):
    return parse_number(data, 1, 100)

def to_structure_OptionalType_CustomIntegerType_1_100(data):
    if data is None: return None
    return to_structure_CustomIntegerType_1_100(data)

def to_structure_VectorType_RecordType_technotransactions_ASSIGNED_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technotransactions_ASSIGNED_STATUTORIES(item))
    return lst

def to_structure_RecordType_core_UserDetails(data):
    from protocol import core
    return core.UserDetails.to_structure(data)

def to_structure_RecordType_general_Request_GetNotifications(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_technomasters_PROFILES(data):
    from protocol import technomasters
    return technomasters.PROFILES.to_structure(data)

def to_structure_CustomIntegerType_1_7(data):
    return parse_number(data, 1, 7)

def to_structure_RecordType_knowledgetransaction_Request_ApproveStatutoryMapping(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Request.to_structure(data)

def to_structure_EnumType_core_SESSION_TYPE(data):
    from protocol import core
    return core.SESSION_TYPE.to_structure(data)

def to_structure_EnumType_core_USER_TYPE(data):
    from protocol import core
    return core.USER_TYPE.to_structure(data)

def to_structure_RecordType_clientmasters_Response_EmployeeCodeAlreadyExists(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_technomasters_Response_GetClientProfileSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_APPROVAL_STATUS.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_ACTIVITY_STATUS.to_structure(data)

def to_structure_RecordType_technomasters_Response_SaveClientSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_general_Response_SaveDomainSuccess(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_RecordType_technomasters_Response_ChangeClientGroupStatusSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_general_Response_DomainNameAlreadyExists(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_Unit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Unit(item))
    return lst

def to_structure_VectorType_RecordType_core_ClientUnit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ClientUnit(item))
    return lst

def to_structure_VectorType_RecordType_core_Form(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Form(item))
    return lst


def to_structure_RecordType_general_Response_UpdateDomainSuccess(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_CustomIntegerType_1_12(data):
    return parse_number(data, 1, 12)

def to_structure_OptionalType_CustomIntegerType_1_12(data):
    if data is None: return None
    return to_structure_CustomIntegerType_1_12(data)

def to_structure_RecordType_general_Response_InvalidDomainId(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_InvalidPassword(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_STATUS.to_structure(data)

def to_structure_EnumType_core_APPLICABILITY_STATUS(data):
    from protocol import core
    return core.APPLICABILITY_STATUS.to_structure(data)

def to_structure_RecordType_technomasters_Response_InvalidClientId(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_EnumType_core_FORM_TYPE(data):
    from protocol import core
    return core.FORM_TYPE.to_structure(data)

def to_structure_EnumType_core_REPEATS_TYPE(data):
    from protocol import core
    return core.REPEATS_TYPE.to_structure(data)

def to_structure_RecordType_technotransactions_Response_GetStatutoryWizardTwoDataSuccess(data):
    from protocol import technotransactions
    return technotransactions.Response.to_structure(data)

def to_structure_RecordType_general_RequestFormat(data):
    from protocol import general
    return general.RequestFormat.to_structure(data)

def to_structure_EnumType_core_DURATION_TYPE(data):
    from protocol import core
    return core.DURATION_TYPE.to_structure(data)

def to_structure_RecordType_core_ActiveCompliance(data):
    from protocol import core
    return core.ActiveCompliance.to_structure(data)

def to_structure_RecordType_admin_Request_UpdateUser(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_RecordType_core_ClientUser(data):
    from protocol import core
    return core.ClientUser.to_structure(data)

def to_structure_RecordType_general_Response_UpdateUserProfileSuccess(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_RecordType_technoreports_Request_GetClientDetailsReportFilters(data):
    from protocol import technoreports
    return technoreports.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_SaveIndustrySuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(data):
    data = parse_dictionary(data)
    dict = {}
    # for key, value in data.items():
    #     key = to_structure_SignedIntegerType_8(key)
    #     value = to_structure_VectorType_RecordType_core_Level(value)
    #     dict.append([key, value])
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_Level(value)
        dict[key] = value
    return dict

def to_structure_RecordType_admin_Response_GetUsersSuccess(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_admin_Response_SaveUserSuccess(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_knowledgereport_MappingReport(data):
    from protocol import knowledgereport
    return knowledgereport.MappingReport.to_structure(data)

def to_structure_RecordType_core_User(data):
    from protocol import core
    return core.User.to_structure(data)

def to_structure_VectorType_RecordType_core_ActiveCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ActiveCompliance(item))
    return lst

def to_structure_RecordType_technotransactions_Request_SaveAssignedStatutory(data):
    from protocol import technotransactions
    return technotransactions.Request.to_structure(data)

def to_structure_VectorType_RecordType_core_UpcomingCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_UpcomingCompliance(item))
    return lst

def to_structure_VectorType_RecordType_dashboard_DomainWise(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_DomainWise(item))
    return lst

def to_structure_RecordType_dashboard_Request_GetNotCompliedChart(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_admin_Response_ChangeUserStatusSuccess(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_EnumType_core_APPROVAL_STATUS(data):
    from protocol import core
    return core.APPROVAL_STATUS.to_structure(data)

def to_structure_RecordType_clientuser_Response_GetComplianceDetailSuccess(data):
    from protocol import clientuser
    return clientuser.Response.to_structure(data)

def to_structure_VectorType_RecordType_knowledgereport_GeographyMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_knowledgereport_GeographyMapping(item))
    return lst

def to_structure_RecordType_clienttransactions_Request_UpdateStatutorySettings(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetUnitwisecomplianceReport(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetReassignComplianceTaskReportFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_knowledgereport_Response_GetGeographyReportSuccess(data):
    from protocol import knowledgereport
    return knowledgereport.Response.to_structure(data)

def to_structure_VariantType_technomasters_Response(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_UserGroupNameAlreadyExists(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_clientuser_Response_NotEnoughDiskSpaceAvailable(data):
    from protocol import clientuser
    return clientuser.Response.to_structure(data)

def to_structure_RecordType_clientreport_UserWiseCompliance(data):
    from protocol import clientreport
    return clientreport.UserWiseCompliance.to_structure(data)

def to_structure_RecordType_technomasters_Request_UpdateClientGroup(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_VariantType_clientadminsettings_Request(data):
    from protocol import clientadminsettings
    return clientadminsettings.Request.to_structure(data)

def to_structure_RecordType_admin_Response_ContactNumberAlreadyExists(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_general_Response_GetDomainsSuccess(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_RecordType_clientuser_ComplianceOnOccurrence(data):
    from protocol import clientuser
    return clientuser.ComplianceOnOccurrence.to_structure(data)

def to_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientuser_ComplianceOnOccurrence(item))
    return lst

def to_structure_VectorType_RecordType_core_Statutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Statutory(item))
    return lst

def to_structure_OptionalType_RecordType_core_BusinessGroup(data):
    if data is None: return data
    return to_structure_RecordType_core_BusinessGroup(data)

def to_structure_OptionalType_RecordType_core_ClientBusinessGroup(data):
    if data is None: return data
    return to_structure_RecordType_core_ClientBusinessGroup(data)

def to_structure_RecordType_clientuser_Response_GetOnOccurrenceCompliancesSuccess(data):
    from protocol import clientuser
    return clientuser.Response.to_structure(data)

def to_structure_RecordType_clientuser_Response_StartOnOccurrenceComplianceSuccess(data):
    from protocol import clientuser
    return clientuser.Response.to_structure(data)

def to_structure_OptionalType_CustomTextType_20(data):
    if data is None: return data
    return to_structure_CustomTextType_20(data)

def to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_STATUS(data):
    from protocol import core
    return core.ASSIGN_STATUTORY_SUBMISSION_STATUS.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Request_GetStatutoryMappings(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Request.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetClientReportFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetReassignComplianceTaskDetails(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_InvalidGeographyLevelId(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetTaskApplicabilityStatusFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_AssigneeWiseDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_AssigneeWiseDetails(item))
    return lst

def to_structure_RecordType_clientadminsettings_LICENCE_HOLDER(data):
    from protocol import clientadminsettings
    return clientadminsettings.LICENCE_HOLDER.to_structure(data)

def to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE(data):
    from protocol import core
    return core.ASSIGN_STATUTORY_SUBMISSION_TYPE.to_structure(data)

def to_structure_VariantType_technotransactions_Request(data):
    from protocol import technotransactions
    return technotransactions.Request.to_structure(data)

def to_structure_RecordType_technotransactions_Response_GetAssignedStatutoriesListSuccess(data):
    from protocol import technotransactions
    return technotransactions.Response.to_structure(data)

def to_structure_OptionalType_RecordType_core_Division(data):
    if data is None: return data
    return to_structure_RecordType_core_Division(data)

def to_structure_OptionalType_RecordType_core_ClientDivision(data):
    if data is None: return data
    return to_structure_RecordType_core_ClientDivision(data)

def to_structure_VectorType_RecordType_core_Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Compliance(item))
    return lst

def to_structure_VectorType_RecordType_clientadminsettings_LICENCE_HOLDER(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientadminsettings_LICENCE_HOLDER(item))
    return lst

def to_structure_RecordType_clientmasters_Request_SaveServiceProvider(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_clientadminsettings_PROFILE_DETAIL(data):
    from protocol import clientadminsettings
    return clientadminsettings.PROFILE_DETAIL.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_GetStatutorySettingsSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Request_SaveStatutoryMapping(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Request_UpdateServiceProvider(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_dashboard_Response_GetTrendChartSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Request_GetServiceProviders(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(data):
    if data is None: return data
    return to_structure_EnumType_core_APPLICABILITY_STATUS(data)

def to_structure_RecordType_dashboard_Response_GetEscalationsChartSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientadminsettings_PROFILE_DETAIL(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientadminsettings_PROFILE_DETAIL(item))
    return lst

def to_structure_RecordType_clientreport_Request_GetComplianceTaskApplicabilityStatusReport(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_EnumType_core_FILTER_TYPE(data):
    from protocol import core
    return core.FILTER_TYPE.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetComplianceActivityReportFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientadminsettings_Response_UpdateSettingsSuccess(data):
    from protocol import clientadminsettings
    return clientadminsettings.Response.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_GeographyLevel(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_GeographyLevel(value)
        dict.append([key, value])
    return dict

def to_structure_VariantType_clientadminsettings_Response(data):
    from protocol import clientadminsettings
    return clientadminsettings.Response.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Request_UpdateStatutoryMapping(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Request.to_structure(data)

def to_structure_RecordType_general_Response_ChangeDomainStatusSuccess(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Request_CloseUnit(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_technoreports_Request_GetAssignedStatutoryReport(data):
    from protocol import technoreports
    return technoreports.Request.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_Statutory(value)
        dict[key] = value
    return dict

def to_structure_RecordType_technomasters_Response_GetClientGroupsSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_UpdateIndustrySuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_technomasters_Response_GroupNameAlreadyExists(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_Level(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Level(item))
    return lst

def to_structure_VariantType_knowledgetransaction_Request(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_SaveStatutoryLevelSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetComplianceActivityReport(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetReassignedHistoryReportFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_GetGeographyLevels(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_general_Request_UpdateNotificationStatus(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_dashboard_Response_GetTrendChartDrillDownDataSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_core_StatutoryMapping(data):
    from protocol import core
    return core.StatutoryMapping.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_DrillDownData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_DrillDownData(item))
    return lst

def to_structure_RecordType_core_LegalEntity(data):
    from protocol import core
    return core.LegalEntity.to_structure(data)

def to_structure_RecordType_core_ClientLegalEntity(data):
    from protocol import core
    return core.ClientLegalEntity.to_structure(data)

def to_structure_RecordType_core_GroupCompany(data):
    from protocol import core
    return core.GroupCompany.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetReassignedHistoryReportSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_dashboard_AssigneeChartData(data):
    from protocol import dashboard
    return dashboard.AssigneeChartData.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_AssigneeChartData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_AssigneeChartData(item))
    return lst

def to_structure_RecordType_knowledgemaster_Response_GetStatutoryLevelsSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_technomasters_Response_UpdateClientSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_dashboard_Response_GetAssigneeWiseCompliancesChartSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientuser_ComplianceDetail(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientuser_ComplianceDetail(item))
    return lst

def to_structure_RecordType_technoreports_RequestFormat(data):
    from protocol import technoreports
    return technoreports.RequestFormat.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetClientReportFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_technomasters_Request_GetClients(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_RecordType_dashboard_Level1Compliance(data):
    from protocol import dashboard
    return dashboard.Level1Compliance.to_structure(data)

def to_structure_RecordType_core_GroupCompanyDetail(data):
    from protocol import core
    return core.GroupCompanyDetail.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_GetStatutoriesSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_Level1Compliance(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_dashboard_Level1Compliance(value)
        dict.append([key, value])
    return dict

def to_structure_RecordType_knowledgemaster_Response_StatutoryNameAlreadyExists(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_InvalidIndustryId(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_DuplicateStatutoryLevelsExists(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_GetGeographies(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_UnitCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_UnitCompliance(item))
    return lst

def to_structure_RecordType_dashboard_Request_GetTrendChart(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_knowledgereport_Request_GetStatutoryMappingReportFilters(data):
    from protocol import knowledgereport
    return knowledgereport.Request.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ComplianceUnit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ComplianceUnit(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_UnitWiseCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_UnitWiseCompliance(item))
    return lst

def to_structure_VariantType_general_Request(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_UserWiseCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_UserWiseCompliance(item))
    return lst

def to_structure_OptionalType_VectorType_RecordType_core_BusinessGroup(data):
    if data is None: return data
    return to_structure_VectorType_RecordType_core_BusinessGroup(data)

def to_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technomasters_LICENCE_HOLDER_DETAILS(item))
    return lst

def to_structure_RecordType_knowledgereport_Request_GetStatutoryMappingReportData(data):
    from protocol import knowledgereport
    return knowledgereport.Request.to_structure(data)

def to_structure_RecordType_technomasters_Response_ChangeClientStatusSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_clientreport_ActivityCompliance(value)
        dict.append([key, value])
    return dict

def to_structure_RecordType_knowledgereport_Request_GetGeographyReport(data):
    from protocol import knowledgereport
    return knowledgereport.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    from protocol import clienttransactions
    return clienttransactions.UNIT_WISE_STATUTORIES.to_structure(data)

def to_structure_VariantType_knowledgereport_Request(data):
    from protocol import knowledgereport
    return knowledgereport.Request.to_structure(data)

def to_structure_VectorType_RecordType_core_UnitDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_UnitDetails(item))
    return lst

def to_structure_VectorType_RecordType_techno_report_UnitDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_techno_report_UnitDetails(item))
    return lst

def to_structure_VectorType_RecordType_techno_report_GroupedUnits(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_techno_report_GroupedUnits(item))
    return lst

def to_structure_VectorType_RecordType_techno_master_UnitDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_techno_master_UnitDetails(item))
    return lst

def to_structure_VectorType_RecordType_technomasters_Unit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technomasters_Unit(item))
    return lst

def to_structure_VectorType_RecordType_technomasters_CountryWiseUnits(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technomasters_CountryWiseUnits(item))
    return lst

def to_structure_VectorType_RecordType_technotransactions_UNIT(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technotransactions_UNIT(item))
    return lst

def to_structure_RecordType_dashboard_Response_GetComplianceStatusDrillDownDataSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_knowledgereport_RequestFormat(data):
    from protocol import knowledgereport
    return knowledgereport.RequestFormat.to_structure(data)

def to_structure_RecordType_clientreport_ServiceProviderCompliance(data):
    from protocol import clientreport
    return clientreport.ServiceProviderCompliance.to_structure(data)

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_clientreport_ComplianceUnit(value)
        dict.append([key, value])
    return dict

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_Level1Statutory(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_clientreport_Level1Statutory(value)
        dict.append([key, value])
    return dict

def to_structure_RecordType_dashboard_Response_GetEscalationsDrillDownDataSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetServiceProviderWiseCompliance(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetComplianceDetailsReportFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_clientreport_DomainWiseCompliance(data):
    from protocol import clientreport
    return clientreport.DomainWiseCompliance.to_structure(data)

def to_structure_RecordType_dashboard_ApplicableDrillDown(data):
    from protocol import dashboard
    return dashboard.ApplicableDrillDown.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_ApplicableDrillDown(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_ApplicableDrillDown(item))
    return lst

def to_structure_RecordType_clientreport_Request_GetComplianceDetailsReport(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_OptionalType_VectorType_RecordType_core_Division(data):
    if data is None: return data
    return to_structure_VectorType_RecordType_core_Division(data)

def to_structure_RecordType_dashboard_Response_GetComplianceApplicabilityStatusDrillDownSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_EnumType_core_NOTIFICATION_TYPE(data):
    from protocol import core
    return core.NOTIFICATION_TYPE.to_structure(data)

def to_structure_RecordType_technotransactions_Request_GetAssignedStatutoriesList(data):
    from protocol import technotransactions
    return technotransactions.Request.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetServiceProviderWiseComplianceSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_dashboard_Response_GetNotCompliedDrillDownSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_technotransactions_RequestFormat(data):
    from protocol import technotransactions
    return technotransactions.RequestFormat.to_structure(data)

def to_structure_RecordType_clientmasters_Request_UpdateClientUserStatus(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_core_UnitDetails(data):
    from protocol import core
    return core.UnitDetails.to_structure(data)

def to_structure_RecordType_techno_report_UnitDetails(data):
    from protocol import technoreports
    return technoreports.UnitDetails.to_structure(data)

def to_structure_RecordType_techno_report_GroupedUnits(data):
    from protocol import technoreports
    return technoreports.GroupedUnits.to_structure(data)

def to_structure_RecordType_techno_master_UnitDetails(data):
    from protocol import technomasters
    return technomasters.UnitDetails.to_structure(data)

def to_structure_RecordType_technomasters_Unit(data):
    from protocol import technomasters
    return technomasters.Unit.to_structure(data)

def to_structure_RecordType_technomasters_CountryWiseUnits(data):
    from protocol import technomasters
    return technomasters.CountryWiseUnits.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_SaveGeographySuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetAssigneewisecomplianceReport(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_VariantType_clientreport_Request(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientuser_Request_GetOnOccurrenceCompliances(data):
    from protocol import clientuser
    return clientuser.Request.to_structure(data)

def to_structure_RecordType_login_Request_Logout(data):
    from protocol import login
    return login.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_SaveAssignedComplianceSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetActivityLogReportSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_VectorType_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(item))
    return lst

def to_structure_RecordType_clientreport_LoginTrace(data):
    from protocol import clientreport
    return clientreport.LoginTrace.to_structure(data)

def to_structure_RecordType_technomasters_Response_ReactivateUnitSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_dashboard_Request_GetTrendChartDrillDownData(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_StatutoryMapping(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_StatutoryMapping(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_clientreport_LoginTrace(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_LoginTrace(item))
    return lst

def to_structure_RecordType_clientreport_Response_GetLoginTraceSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ServiceProviderCompliance(item))
    return lst

def to_structure_VariantType_clientreport_Response(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_SaveStatutorySuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_InvalidStatutoryId(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_login_Response_UserLoginSuccess(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_clientuser_RequestFormat(data):
    from protocol import clientuser
    return clientuser.RequestFormat.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetActivityLogReport(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientreport_RequestFormat(data):
    from protocol import clientreport
    return clientreport.RequestFormat.to_structure(data)

def to_structure_RecordType_login_Response_AdminLoginSuccess(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_admin_Response_EmailIDAlreadyExists(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_core_UserGroup(data):
    from protocol import core
    return core.UserGroup.to_structure(data)

def to_structure_RecordType_client_masters_ClientUserGroup(data):
    from protocol import clientmasters
    return clientmasters.ClientUserGroup.to_structure(data)

def to_structure_RecordType_login_Response_InvalidCredentials(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_StatutoryNature(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_StatutoryNature(item))
    return lst

def to_structure_RecordType_login_Response_ForgotPasswordSuccess(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_login_Response_InvalidUserName(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_core_GeographyLevel(data):
    from protocol import core
    return core.GeographyLevel.to_structure(data)

def to_structure_RecordType_login_Response_ResetSessionTokenValidationSuccess(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_dashboard_UnitCompliance(data):
    from protocol import dashboard
    return dashboard.UnitCompliance.to_structure(data)

def to_structure_RecordType_login_Response_InvalidResetToken(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_ChangeStatutoryNatureStatus(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_login_Response_ResetPasswordSuccess(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_VectorType_RecordType_knowledgereport_MappingReport(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_knowledgereport_MappingReport(item))
    return lst

def to_structure_RecordType_login_Response_ChangePasswordSuccess(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_login_Response_InvalidCurrentPassword(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_UpdateGeography(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_login_Response_LogoutSuccess(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_InvalidUserId(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_login_Response_InvalidSessionToken(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetRiskReportFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_VariantType_login_Response(data):
    from protocol import login
    return login.Response.to_structure(data)

def to_structure_RecordType_technomasters_Request_SaveClientGroup(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_RecordType_clientreport_FormName(data):
    from protocol import clientreport
    return clientreport.FormName.to_structure(data)

def to_structure_RecordType_admin_Request_GetUserGroups(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(value)
        dict.append([key, value])
    return dict

def to_structure_RecordType_dashboard_Response_GetComplianceApplicabilityStatusChartSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_AssignedStatutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_AssignedStatutory(item))
    return lst

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_AssignedStatutory(data):
    data = parse_dictionary(data)    
    d = {}
    for key, value in data:
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_AssignedStatutory(value)
        d[key] = value
    return d


def to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(item))
    return lst

def to_structure_RecordType_knowledgereport_Response_GetStatutoryMappingReportDataSuccess(data):
    from protocol import knowledgereport
    return knowledgereport.Response.to_structure(data)

def to_structure_RecordType_dashboard_Request_GetAssigneeWiseComplianceDrillDown(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_VectorType_RecordType_core_StatutoryDate(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_StatutoryDate(item))
    return lst

def to_structure_OptionalType_VectorType_RecordType_core_StatutoryDate(data):
    if data is None : return None
    return to_structure_VectorType_RecordType_core_StatutoryDate(data)

def to_structure_RecordType_core_FileList(data):
    from protocol import core
    return core.FileList.to_structure(data)

def to_structure_VectorType_RecordType_core_FileLst(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_core_FileList(item))
    return lst        

def to_structure_OptionalType_VectorType_RecordType_core_FileList(data):
    if data is None : return None
    return to_structure_VectorType_RecordType_core_FileLst(data)


def to_structure_RecordType_clientmasters_Request_ChangeServiceProviderStatus(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_admin_Response_UpdateUserSuccess(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_ChangeGeographyStatus(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_Request_GetStatutorySettings(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_VectorType_RecordType_core_User(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_User(item))
    return lst

def to_structure_VectorType_RecordType_core_GroupCompanyDetail(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_GroupCompanyDetail(item))
    return lst

def to_structure_RecordType_clientuser_ComplianceDetail(data):
    from protocol import clientuser
    return clientuser.ComplianceDetail.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_GetIndustries(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_core_BusinessGroup(data):
    from protocol import core
    return core.BusinessGroup.to_structure(data)

def to_structure_RecordType_core_ClientBusinessGroup(data):
    from protocol import core
    return core.ClientBusinessGroup.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_FREQUENCY(data):
    from protocol import core
    return core.COMPLIANCE_FREQUENCY.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_GetStatutoryLevels(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_technomasters_Request_GetClientGroups(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_RecordType_knowledgereport_GeographyMapping(data):
    from protocol import knowledgereport
    return knowledgereport.GeographyMapping.to_structure(data)

def to_structure_VariantType_clientmasters_Request(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_Request_GetAssignCompliancesFormData(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_ASSINGED_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.ASSINGED_COMPLIANCE.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_ASSINGED_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_ASSINGED_COMPLIANCE(item))
    return lst

def to_structure_VectorType_RecordType_clienttransactions_USERWISECOMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_USERWISECOMPLIANCE(item))
    return lst

def to_structure_RecordType_knowledgemaster_Request_UpdateStatutoryNature(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_RecordType_dashboard_DataMap(data):
    from protocol import dashboard
    return dashboard.DataMap.to_structure(data)

def to_structure_RecordType_technomasters_Response_UpdateClientGroupSuccess(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_UserDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_UserDetails(item))
    return lst

def to_structure_VectorType_VectorType_RecordType_core_StatutoryDate(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_VectorType_RecordType_core_StatutoryDate(item))
    return lst

def to_structure_RecordType_technoreports_Response_GetAssignedStatutoryReportFiltersSuccess(data):
    from protocol import technoreports
    return technoreports.Response.to_structure(data)

def to_structure_RecordType_dashboard_ChartDataMap(data):
    from protocol import dashboard
    return dashboard.ChartDataMap.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetAssigneewisecomplianceReportSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(data):
    from protocol import technoreports
    return technoreports.COUNTRY_WISE_NOTIFICATIONS.to_structure(data)

def to_structure_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(data):
    from protocol import technoreports
    return technoreports.UNIT_WISE_ASSIGNED_STATUTORIES.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetRiskReportFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_dashboard_Response_GetAssigneeWiseComplianceDrillDownSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_technoreports_Response_GetAssignedStatutoryReportSuccess(data):
    from protocol import technoreports
    return technoreports.Response.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_knowledgereport_GeographyMapping(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_knowledgereport_GeographyMapping(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(item))
    return lst

def to_structure_RecordType_knowledgemaster_Response_GetStatutoryNaturesSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_dashboard_EscalationData(data):
    from protocol import dashboard
    return dashboard.EscalationData.to_structure(data)

def to_structure_RecordType_core_Menu(data):
    from protocol import core
    return core.Menu.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_EscalationData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_EscalationData(item))
    return lst

def to_structure_RecordType_dashboard_Request_GetComplianceStatusDrillDownData(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Response_SaveServiceProviderSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_CloseUnitSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_GetGeographyLevelsSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_admin_Request_GetUsers(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_RecordType_clientadminsettings_Request_GetSettings(data):
    from protocol import clientadminsettings
    return clientadminsettings.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Response_UpdateServiceProviderSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_technotransactions_Request_GetAssignedStatutoriesById(data):
    from protocol import technotransactions
    return technotransactions.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Response_ChangeServiceProviderStatusSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_RequestFormat(data):
    from protocol import knowledgemaster
    return knowledgemaster.RequestFormat.to_structure(data)

def to_structure_RecordType_core_CountryWiseUnits(data):
    from protocol import core
    return core.CountryWiseUnits.to_structure(data)

def to_structure_RecordType_clientuser_Response_UpdateComplianceDetailSuccess(data):
    from protocol import clientuser
    return clientuser.Response.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetRiskReportSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_technomasters_Response_UnitCodeAlreadyExists(data):
    from protocol import technomasters
    return technomasters.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_InvalidUserGroupId(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_admin_Request_SaveUser(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_SaveGeographyLevelSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_VariantType_knowledgereport_Response(data):
    from protocol import knowledgereport
    return knowledgereport.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_UpdateGeographyLevelSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientreport_UnitName(data):
    from protocol import clientreport
    return clientreport.UnitName.to_structure(data)

def to_structure_VectorType_RecordType_core_Form(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Form(item))
    return lst

def to_structure_VectorType_RecordType_dashboard_TrendData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_TrendData(item))
    return lst

def to_structure_RecordType_core_ClientConfiguration(data):
    from protocol import core
    return core.ClientConfiguration.to_structure(data)

def to_structure_RecordType_dashboard_Request_GetAssigneeWiseCompliancesChart(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Response_SaveClientUserSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_clientreport_AssigneeCompliance(data):
    from protocol import clientreport
    return clientreport.AssigneeCompliance.to_structure(data)

def to_structure_RecordType_clientmasters_Response_ContactNumberAlreadyExistss(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetServiceProviderReportFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_UpdateClientUserSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_ChangeIndustryStatusSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_core_Domain(data):
    from protocol import core
    return core.Domain.to_structure(data)

def to_structure_VectorType_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(item))
    return lst

def to_structure_RecordType_knowledgemaster_Response_GetGeographiesSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_AssigneeCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_AssigneeCompliance(item))
    return lst

def to_structure_RecordType_admin_Request_ChangeUserStatus(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_VariantType_login_Request(data):
    from protocol import login
    return login.Request.to_structure(data)

def to_structure_VariantType_admin_Request(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_RecordType_clientreport_ComplianceForUnit(data):
    from protocol import clientreport
    return clientreport.ComplianceForUnit.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_SaveStatutoryNatureSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_GetUnitsSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_admin_RequestFormat(data):
    from protocol import admin
    return admin.RequestFormat.to_structure(data)

def to_structure_VectorType_RecordType_core_FormCategory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_FormCategory(item))
    return lst

def to_structure_RecordType_dashboard_DrillDownData(data):
    from protocol import dashboard
    return dashboard.DrillDownData.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_GetIndustriesSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_InvalidPassword(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_RessignedCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_RessignedCompliance(item))
    return lst

def to_structure_RecordType_clientadminsettings_Request_UpdateSettings(data):
    from protocol import clientadminsettings
    return clientadminsettings.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Response_UpdateUserPrivilegesSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_IndustryNameAlreadyExists(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_dashboard_DelayedCompliance(data):
    from protocol import dashboard
    return dashboard.DelayedCompliance.to_structure(data)

def to_structure_RecordType_technoreports_Response_GetStatutoryNotificationsSuccess(data):
    from protocol import technoreports
    return technoreports.Response.to_structure(data)

def to_structure_RecordType_technotransactions_Request_GetAssignedStatutoryWizardOneData(data):
    from protocol import technotransactions
    return technotransactions.Request.to_structure(data)

def to_structure_RecordType_admin_Response_GetUserGroupsSuccess(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_admin_Response_SaveUserGroupSuccess(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_admin_Response_GroupNameAlreadyExists(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_clientuser_Request_UpdateComplianceDetail(data):
    from protocol import clientuser
    return clientuser.Request.to_structure(data)

def to_structure_RecordType_core_Geography(data):
    from protocol import core
    return core.Geography.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_FormName(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_FormName(item))
    return lst

def to_structure_RecordType_dashboard_DomainWise(data):
    from protocol import dashboard
    return dashboard.DomainWise.to_structure(data)

def to_structure_RecordType_admin_Response_ChangeUserGroupStatusSuccess(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_GetPastRecordsFormDataSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_clientuser_Response_CheckDiskSpaceSuccess(data):
    from protocol import clientuser
    return clientuser.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_StatutoryNatureNameAlreadyExists(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientuser_Request_StartOnOccurrenceCompliance(data):
    from protocol import clientuser
    return clientuser.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_USERWISESTATUTORIES(data):
    from protocol import clienttransactions
    return clienttransactions.USERWISESTATUTORIES.to_structure(data)

def to_structure_VariantType_clientuser_Request(data):
    from protocol import clientuser
    return clientuser.Request.to_structure(data)

def to_structure_RecordType_dashboard_RequestFormat(data):
    from protocol import dashboard
    return dashboard.RequestFormat.to_structure(data)

def to_structure_RecordType_core_Industry(data):
    from protocol import core
    return core.Industry.to_structure(data)

def to_structure_RecordType_technomasters_Request_ChangeClientGroupStatus(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_RecordType_technotransactions_Request_GetStatutoryWizardTwoData(data):
    from protocol import technotransactions
    return technotransactions.Request.to_structure(data)

def to_structure_RecordType_knowledgetransaction_RequestFormat(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.RequestFormat.to_structure(data)

def to_structure_RecordType_core_AssignedStatutory(data):
    from protocol import core
    return core.AssignedStatutory.to_structure(data)

def to_structure_RecordType_dashboard_Request_GetComplianceApplicabilityStatusDrillDown(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_core_StatutoryNature(data):
    from protocol import core
    return core.StatutoryNature.to_structure(data)

def to_structure_VariantType_technoreports_Request(data):
    from protocol import technoreports
    return technoreports.Request.to_structure(data)

def to_structure_VariantType_dashboard_Response(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_core_StatutoryLevel(data):
    from protocol import core
    return core.StatutoryLevel.to_structure(data)

def to_structure_RecordType_core_Division(data):
    from protocol import core
    return core.Division.to_structure(data)

def to_structure_RecordType_core_ClientDivision(data):
    from protocol import core
    return core.ClientDivision.to_structure(data)

def to_structure_RecordType_core_Country(data):
    from protocol import core
    return core.Country.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetServiceProviderReportFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_RecordType_core_Menu(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_RecordType_core_Menu(value)
        dict[key] = value
    return dict

def to_structure_RecordType_core_Statutory(data):
    from protocol import core
    return core.Statutory.to_structure(data)

def to_structure_VariantType_clientmasters_Response(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_admin_Request_UpdateUserGroup(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Response_ChangeUserPrivilegeStatusSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_clientmasters_RequestFormat(data):
    from protocol import clientmasters
    return clientmasters.RequestFormat.to_structure(data)

def to_structure_RecordType_dashboard_Response_GetChartFiltersSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_core_Unit(data):
    from protocol import core
    return core.Unit.to_structure(data)

def to_structure_RecordType_core_ClientUnit(data):
    from protocol import core
    return core.ClientUnit.to_structure(data)

def to_structure_RecordType_core_UpcomingCompliance(data):
    from protocol import core
    return core.UpcomingCompliance.to_structure(data)

def to_structure_VectorType_RecordType_core_ComplianceFrequency(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceFrequency(item))
    return lst

def to_structure_RecordType_core_UserGroupDetails(data):
    from protocol import core
    return core.UserGroupDetails.to_structure(data)

def to_structure_VectorType_RecordType_core_ComplianceRepeatType(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceRepeatType(item))
    return lst

def to_structure_RecordType_core_NumberOfCompliances(data):
    from protocol import core
    return core.NumberOfCompliances.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_ChartDataMap(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_ChartDataMap(item))
    return lst

def to_structure_VectorType_RecordType_core_ComplianceDurationType(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceDurationType(item))
    return lst

def to_structure_RecordType_clientmasters_Request_UpdateClientUser(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_Request_ReassignCompliance(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_VariantType_technotransactions_Response(data):
    from protocol import technotransactions
    return technotransactions.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_GetUserPrivilegesSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Response_GetStatutoryMappingsSuccess(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ComplianceForUnit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ComplianceForUnit(item))
    return lst

def to_structure_VariantType_knowledgemaster_Response(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Response_SaveStatutoryMappingSuccess(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Response.to_structure(data)

def to_structure_VariantType_clientuser_Response(data):
    from protocol import clientuser
    return clientuser.Response.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Response_UpdateStatutoryMappingSuccess(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Response.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Response_InvalidStatutoryMappingId(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Response.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Response_ChangeStatutoryMappingStatusSuccess(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Response.to_structure(data)

def to_structure_RecordType_knowledgetransaction_Response_ApproveStatutoryMappingSuccess(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Response.to_structure(data)

def to_structure_RecordType_clientreport_UnitCompliance(data):
    from protocol import clientreport
    return clientreport.UnitCompliance.to_structure(data)

def to_structure_VariantType_knowledgetransaction_Response(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Response.to_structure(data)

def to_structure_RecordType_core_ComplianceShortDescription(data):
    from protocol import core
    return core.ComplianceShortDescription.to_structure(data)

def to_structure_VectorType_RecordType_core_ComplianceApprovalStatus(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceApprovalStatus(item))
    return lst

def to_structure_RecordType_core_ComplianceApplicability(data):
    from protocol import core
    return core.ComplianceApplicability.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_UpdateStatutoryNatureSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_VectorType_RecordType_core_ComplianceApplicability(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceApplicability(item))
    return lst

def to_structure_VectorType_RecordType_core_ComplianceShortDescription(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceShortDescription(item))
    return lst

def to_structure_RecordType_general_Response_UpdateNotificationStatusSuccess(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_UnitCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_UnitCompliance(item))
    return lst

def to_structure_RecordType_core_ComplianceStatusDrillDown(data):
    from protocol import core
    return core.ComplianceStatusDrillDown.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_SaveStatutoryLevel(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_VectorType_RecordType_core_ClientUser(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ClientUser(item))
    return lst

def to_structure_VectorType_RecordType_dashboard_DataMap(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_DataMap(item))
    return lst

def to_structure_RecordType_clientmasters_Response_ChangeClientUserStatusSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_admin_Response_EmployeeCodeAlreadyExists(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_RecordType_login_Request_Login(data):
    from protocol import login
    return login.Request.to_structure(data)

def to_structure_RecordType_core_ComplianceRepeatType(data):
    from protocol import core
    return core.ComplianceRepeatType.to_structure(data)

def to_structure_RecordType_login_Request_ForgotPassword(data):
    from protocol import login
    return login.Request.to_structure(data)

def to_structure_RecordType_technomasters_Request_SaveClient(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_RecordType_core_ComplianceFrequency(data):
    from protocol import core
    return core.ComplianceFrequency.to_structure(data)

def to_structure_RecordType_login_Request_ResetTokenValidation(data):
    from protocol import login
    return login.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Request_GetUnits(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_VectorType_RecordType_technomasters_PROFILES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technomasters_PROFILES(item))
    return lst

def to_structure_RecordType_dashboard_AssigneeWiseDetails(data):
    from protocol import dashboard
    return dashboard.AssigneeWiseDetails.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_APPROVALCOMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_APPROVALCOMPLIANCE(item))
    return lst

def to_structure_RecordType_clientreport_Response_GetUnitwisecomplianceReportSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_login_Request_ResetPassword(data):
    from protocol import login
    return login.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_AssigneeNotBelongToUnit(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_core_ComplianceDurationType(data):
    from protocol import core
    return core.ComplianceDurationType.to_structure(data)

def to_structure_RecordType_clientreport_UserName(data):
    from protocol import clientreport
    return clientreport.UserName.to_structure(data)

def to_structure_RecordType_clienttransactions_APPROVALCOMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.APPROVALCOMPLIANCE.to_structure(data)

def to_structure_RecordType_login_Request_ChangePassword(data):
    from protocol import login
    return login.Request.to_structure(data)

def to_structure_RecordType_core_ComplianceApprovalStatus(data):
    from protocol import core
    return core.ComplianceApprovalStatus.to_structure(data)

def to_structure_RecordType_technomasters_Request_ReactivateUnit(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_RecordType_dashboard_Request_GetEscalationsChart(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_core_Compliance(data):
    from protocol import core
    return core.Compliance.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetRiskReport(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Request_GetStatutories(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(value)
        dict.append([key, value])
    return dict

def to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(item))
    return lst

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items() :
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(value)
        d[key] = value
    return d

def to_structure_RecordType_clientreport_Response_GetComplianceActivityReportFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_InvalidStatutoryNatureId(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_ChangeGeographyStatusSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_core_StatutoryDate(data):
    from protocol import core
    return core.StatutoryDate.to_structure(data)

def to_structure_RecordType_admin_Request_SaveUserGroup(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_GeographyNameAlreadyExists(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientreport_Activities(data):
    from protocol import clientreport
    return clientreport.Activities.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetReassignedHistoryReport(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(data):
    from protocol import clienttransactions
    return clienttransactions.ASSIGN_COMPLIANCE_USER.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetComplianceDetailsReportFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_CustomIntegerType_1_31(data):
    return parse_number(data, 1, 31)

def to_structure_OptionalType_CustomIntegerType_1_31(data):
    if data is None : return None
    return to_structure_CustomIntegerType_1_31(data)

def to_structure_RecordType_clientreport_ActivityCompliance(data):
    from protocol import clientreport
    return clientreport.ActivityCompliance.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetActivityLogFilters(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientadminsettings_RequestFormat(data):
    from protocol import clientadminsettings
    return clientadminsettings.RequestFormat.to_structure(data)

def to_structure_RecordType_core_Form(data):
    from protocol import core
    return core.Form.to_structure(data)

def to_structure_RecordType_core_Level(data):
    from protocol import core
    return core.Level.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ActivityCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ActivityCompliance(item))
    return lst

def to_structure_RecordType_admin_Response_InvalidUserId(data):
    from protocol import admin
    return admin.Response.to_structure(data)

def to_structure_OptionalType_CustomTextType_100(data):
    if data is None: return data
    return to_structure_CustomTextType_100(data)

def to_structure_VectorType_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(item))
    return lst

def to_structure_RecordType_core_ChartFilters(data):
    from protocol import core
    return core.ChartFilters.to_structure(data)

def to_structure_RecordType_clientreport_Request_GetLoginTrace(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)

def to_structure_RecordType_clientuser_Request_GetComplianceDetail(data):
    from protocol import clientuser
    return clientuser.Request.to_structure(data)

def to_structure_RecordType_dashboard_Response_GetComplianceStatusChartSuccess(data):
    from protocol import dashboard
    return dashboard.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_GetAssignCompliancesFormDataSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Request_GetComplianceApprovalList(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_DomainWiseCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_DomainWiseCompliance(item))
    return lst

def to_structure_RecordType_technotransactions_Response_SaveAssignedStatutorySuccess(data):
    from protocol import technotransactions
    return technotransactions.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_ReassignComplianceSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_ConcurrenceNotBelongToUnit(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_CompliedMap(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_CompliedMap(item))
    return lst

def to_structure_RecordType_clienttransactions_Response_ApprovalPersonNotBelongToUnit(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_Activities(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_Activities(item))
    return lst

def to_structure_RecordType_dashboard_Request_GetEscalationsDrillDownData(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(data):
    from protocol import clienttransactions
    return clienttransactions.ASSIGN_COMPLIANCE_UNITS.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetComplianceActivityReportSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_dashboard_Request_GetComplianceApplicabilityStatusChart(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(data):
    from protocol import clienttransactions
    return clienttransactions.APPORVALCOMPLIANCELIST.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(item))
    return lst

def to_structure_RecordType_clientreport_User(data):
    from protocol import clientreport
    return clientreport.User.to_structure(data)

def to_structure_RecordType_clientmasters_Request_GetUserPrivileges(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_technotransactions_UNIT(data):
    from protocol import technotransactions
    return technotransactions.UNIT.to_structure(data)

def to_structure_RecordType_clientreport_UnitWiseCompliance(data):
    from protocol import clientreport
    return clientreport.UnitWiseCompliance.to_structure(data)

def to_structure_RecordType_core_FormType(data):
    from protocol import core
    return core.FormType.to_structure(data)

def to_structure_RecordType_clientreport_ComplianceName(data):
    from protocol import clientreport
    return clientreport.ComplianceName.to_structure(data)

def to_structure_RecordType_clientmasters_Request_SaveUserPrivileges(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.STATUTORYWISECOMPLIANCE.to_structure(data)

def to_structure_VariantType_technoreports_Response(data):
    from protocol import technoreports
    return technoreports.Response.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(item))
    return lst

def to_structure_RecordType_clientmasters_Request_UpdateUserPrivileges(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_technomasters_Request_UpdateClient(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_RecordType_core_StatutoryMapping(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_RecordType_core_StatutoryMapping(value)
        dict[key] = value
    return dict

def to_structure_RecordType_general_Response_ContactNumberAlreadyExists(data):
    from protocol import general
    return general.Response.to_structure(data)

def to_structure_RecordType_knowledgemaster_Response_ChangeStatutoryNatureStatusSuccess(data):
    from protocol import knowledgemaster
    return knowledgemaster.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Request_ChangeUserPrivilegeStatus(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_general_Request_SaveDomain(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_RecordType_clientreport_ComplianceUnit(data):
    from protocol import clientreport
    return clientreport.ComplianceUnit.to_structure(data)

def to_structure_RecordType_clientmasters_Request_GetClientUsers(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_core_FormCategory(data):
    from protocol import core
    return core.FormCategory.to_structure(data)

def to_structure_RecordType_clientreport_Response_GetReassignedHistoryReportFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_knowledgereport_Response_GetStatutoryMappingReportFiltersSuccess(data):
    from protocol import knowledgereport
    return knowledgereport.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_USERWISEUNITS(data):
    from protocol import clienttransactions
    return clienttransactions.USERWISEUNITS.to_structure(data)

def to_structure_RecordType_admin_Request_ChangeUserGroupStatus(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Response_GetClientUsersSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_clientmasters_Response_GetServiceProvidersSuccess(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_GetComplianceApprovalListSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_clientreport_StatutoryReassignCompliance(data):
    from protocol import clientreport
    return clientreport.StatutoryReassignCompliance.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_StatutoryReassignCompliance(item))
    return lst

def to_structure_RecordType_technomasters_Request_GetClientProfile(data):
    from protocol import technomasters
    return technomasters.Request.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_USERWISEUNITS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_USERWISEUNITS(item))
    return lst

def to_structure_VariantType_dashboard_Request(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_clientuser_Request_CheckDiskSpace(data):
    from protocol import clientuser
    return clientuser.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_USERWISECOMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.USERWISECOMPLIANCE.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_Level1Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_Level1Compliance(item))
    return lst

def to_structure_RecordType_clienttransactions_Response_ApproveComplianceSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(data):
    from protocol import clienttransactions
    return clienttransactions.STATUTORY_WISE_COMPLIANCES.to_structure(data)

def to_structure_RecordType_dashboard_RessignedCompliance(data):
    from protocol import dashboard
    return dashboard.RessignedCompliance.to_structure(data)

def to_structure_RecordType_dashboard_Request_GetNotCompliedDrillDown(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_clientmasters_Request_SaveClientUser(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_clientreport_ComplianceDetails(data):
    from protocol import clientreport
    return clientreport.ComplianceDetails.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_GetUserwiseCompliancesSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_RecordType_clienttransactions_Response_UpdateStatutorySettingsSuccess(data):
    from protocol import clienttransactions
    return clienttransactions.Response.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Form(data):
    data = parse_dictionary(data)
    dict = []
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_Form(value)
        dict.append([key, value])
    return dict

def to_structure_RecordType_clientreport_Response_GetActivityLogFiltersSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ComplianceDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ComplianceDetails(item))
    return lst

def to_structure_VectorType_RecordType_core_StatutoryMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_StatutoryMapping(item))
    return lst

def to_structure_RecordType_clientreport_Response_GetComplianceDetailsReportSuccess(data):
    from protocol import clientreport
    return clientreport.Response.to_structure(data)

def to_structure_RecordType_clientreport_ActivityLog(data):
    from protocol import clientreport
    return clientreport.ActivityLog.to_structure(data)

def to_structure_RecordType_general_Request_GetCountries(data):
    from protocol import general
    return general.Request.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ActivityLog(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ActivityLog(item))
    return lst

def to_structure_RecordType_clientreport_Level1Statutory(data):
    from protocol import clientreport
    return clientreport.Level1Statutory.to_structure(data)

def to_structure_RecordType_core_Level1Statutory(data):
    from protocol import core
    return core.Level1Statutory.to_structure(data)

def to_structure_RecordType_client_transactions_IndustryWiseUnits(data):
    from protocol import clienttransactions
    return clienttransactions.IndustryWiseUnits.to_structure(data)

def to_structure_RecordType_clientmasters_Response_ServiceProviderNameAlreadyExists(data):
    from protocol import clientmasters
    return clientmasters.Response.to_structure(data)

def to_structure_RecordType_admin_UserGroup(data):
    from protocol import admin
    return admin.UserGroup.to_structure(data)

def to_structure_VectorType_RecordType_admin_UserGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_admin_UserGroup(item))
    return lst

def to_structure_RecordType_knowledgetransaction_ApproveMapping(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.ApproveMapping.parse_structure(data)

def to_structure_VectorType_RecordType_knowledgetransaction_ApproveMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_knowledgetransaction_ApproveMapping(item))
    return lst

def to_structure_MapType_UnsignedIntegerType_32_Bool(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items():
        key = to_structure_UnsignedIntegerType_32(key)
        value = to_structure_Bool(value)
        d[key] = value
    return d

def to_structure_RecordType_technotransactions_AssignedStatutoryCompliance(data):
    from protocol import technotransactions
    return technotransactions.AssignedStatutoryCompliance.to_structure(data)

def to_structure_VectorType_RecordType_technotransactions_AssignedStatutoryCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technotransactions_AssignedStatutoryCompliance(item))
    return lst


# clienttransactions ComplianceApplicability
def to_structure_RecordType_clienttransactions_ComplianceApplicability(data):
    from protocol import clienttransactions
    return clienttransactions.ComplianceApplicability.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_ComplianceApplicability(item))
    return lst

# clienttransactions AssignedStatutory
def to_structure_RecordType_clienttransactions_AssignedStatutory(data):
    from protocol import clienttransactions
    return clienttransactions.AssignedStatutory.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_AssignedStatutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_AssignedStatutory(item))
    return lst

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_AssignedStatutory(data):
    data = parse_dictionary(data)    
    d = {}
    print data
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_clienttransactions_AssignedStatutory(value)
        d[key] = value
    return d

# UnitStatutoryCompliances
def to_structure_RecordType_clienttransactions_UnitStatutoryCompliances(data):
    from protocol import clienttransactions
    return clienttransactions.UnitStatutoryCompliances.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_UnitStatutoryCompliances(data):
    data = parse_list(data, 0)    
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_clienttransactions_UnitStatutoryCompliances(item))
    return lst


# Clienttransaction ApplicableCompliance
def to_structure_RecordType_clienttransactions_ApplicableCompliance(data):
    from protocol import clienttransactions
    return clienttransactions.ApplicableCompliance.to_structure(data)


def to_structure_VectorType_RecordType_clienttransactions_ApplicableCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_clienttransactions_ApplicableCompliance(item))
    return lst

# clienttransaction UpdateStatutoryCompliance
def to_structure_RecordType_clienttransactions_UpdateStatutoryCompliance(data):
    from protocol import clienttransactions
    return clienttransactions.UpdateStatutoryCompliance.to_structure(data)


def to_structure_VectorType_RecordType_clienttransactions_UpdateStatutoryCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_clienttransactions_UpdateStatutoryCompliance(item))
    return lst

#clienttransaction getcompliancforunit
def to_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    from protocol import clienttransactions
    return clienttransactions.UNIT_WISE_STATUTORIES.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(item))
    return lst

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(value)
        d[key] = value
    return d
