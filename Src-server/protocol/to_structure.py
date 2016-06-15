from collections import OrderedDict
from protocol.jsonvalidators import (
    parse_bool,
    parse_number,
    parse_point_numbers,
    parse_string,
    parse_custom_string,
    parse_list,
    parse_dictionary
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

def to_structure_VectorType_RecordType_clientreport_Level1Statutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_Level1Statutory(item))
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

def to_structure_VariantType_knowledgemaster_Request(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.to_structure(data)

def to_structure_OptionalType_SignedIntegerType_8(data):
    if data is None: return data
    return to_structure_SignedIntegerType_8(data)

def to_structure_RecordType_clientreport_ReassignHistory(data):
    from protocol import clientreport
    return clientreport.ReassignHistory.to_structure(data)

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

def to_structure_MapType_UnsignedInteger_32_VectorType_RecordType_technomaster_UnitDetails(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_UnsignedIntegerType_32(key)
        value = to_structure_VectorType_RecordType_technomasters_UnitDetails(value)
        dict[key] = value
    return dict

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_core_Form(data):
    data = parse_dictionary(data)
    dict = OrderedDict()
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

def to_structure_VectorType_RecordType_clientreport_ReassignCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ReassignCompliance(item))
    return lst

def to_structure_VectorType_RecordType_core_Country(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Country(item))
    return lst

def to_structure_Bool(data):
    return parse_bool(data)

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
    # return parse_number(data, -128, 127)
    return parse_number(data, 0, 4294967295)

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

def to_structure_RecordType_dashboard_CompliedMap(data):
    from protocol import dashboard
    return dashboard.CompliedMap.to_structure(data)

def to_structure_Float(data):
    return parse_point_numbers(data)

def to_structure_VectorType_RecordType_core_Geography(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Geography(item))
    return lst

def to_structure_RecordType_clientreport_ComplianceList(data):
    from protocol import clientreport
    return clientreport.ComplianceList.to_structure(data)

def to_structure_VectorType_CustomTextType_20(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_CustomTextType_20(item))
    return lst

def to_structure_Text(data):
    return parse_string(data)

def to_structure_OptionalType_Text(data):
    if data is None: return None
    return to_structure_Text(data)

def to_structure_VectorType_CustomTextType_50(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_CustomTextType_50(item))
    return lst

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

def to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ApplicabilityCompliance(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_500(key)
        value = to_structure_VectorType_RecordType_clientreport_ApplicabilityCompliance(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(item))
    return lst

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

def to_structure_VectorType_RecordType_core_Domain(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Domain(item))
    return lst

def to_structure_CustomTextType_20(data):
    return parse_custom_string(data, 20)

def to_structure_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.REASSIGNED_COMPLIANCE.to_structure(data)

def to_structure_RecordType_technotransactions_ASSIGNED_STATUTORIES(data):
    from protocol import technotransactions
    return technotransactions.ASSIGNED_STATUTORIES.to_structure(data)

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

def to_structure_VectorType_Text(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_Text(item))
    return lst

def to_structure_CustomTextType_100(data):
    return parse_custom_string(data, 100)

def to_structure_CustomTextType_200(data):
    return parse_custom_string(data, 200)

def to_structure_CustomTextType_250(data):
    return parse_custom_string(data, 250)

def to_structure_OptionalType_Bool(data):
    if data is None: return data
    return to_structure_Bool(data)

def to_structure_RecordType_core_ServiceProvider(data):
    from protocol import core
    return core.ServiceProvider.to_structure(data)

def to_structure_RecordType_core_ServiceProviderDetails(data):
    from protocol import core
    return core.ServiceProviderDetails.to_structure(data)

def to_structure_RecordType_technomasters_LICENCE_HOLDER_DETAILS(data):
    from protocol import technomasters
    return technomasters.LICENCE_HOLDER_DETAILS.to_structure(data)

def to_structure_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.PAST_RECORD_COMPLIANCE.to_structure(data)

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

def to_structure_VariantType_clienttransactions_Request(data):
    from protocol import clienttransactions
    return clienttransactions.Request.to_structure(data)

def to_structure_CustomTextType_500(data):
    return parse_custom_string(data, 500)

def to_structure_RecordType_technomasters_PROFILE_DETAIL(data):
    from protocol import technomasters
    return technomasters.PROFILE_DETAIL.to_structure(data)

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

def to_structure_RecordType_technomasters_PROFILES(data):
    from protocol import technomasters
    return technomasters.PROFILES.to_structure(data)

def to_structure_EnumType_core_SESSION_TYPE(data):
    from protocol import core
    return core.SESSION_TYPE.to_structure(data)

def to_structure_EnumType_core_USER_TYPE(data):
    from protocol import core
    return core.USER_TYPE.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_APPROVAL_STATUS.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_ACTIVITY_STATUS.to_structure(data)

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

def to_structure_CustomIntegerType_1_12(data):
    return parse_number(data, 1, 12)

def to_structure_OptionalType_CustomIntegerType_1_12(data):
    if data is None: return None
    return to_structure_CustomIntegerType_1_12(data)

def to_structure_EnumType_core_COMPLIANCE_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_STATUS.to_structure(data)

def to_structure_EnumType_core_APPLICABILITY_STATUS(data):
    from protocol import core
    return core.APPLICABILITY_STATUS.to_structure(data)

def to_structure_EnumType_core_REPEATS_TYPE(data):
    from protocol import core
    return core.REPEATS_TYPE.to_structure(data)

def to_structure_EnumType_core_DURATION_TYPE(data):
    from protocol import core
    return core.DURATION_TYPE.to_structure(data)

def to_structure_RecordType_core_ActiveCompliance(data):
    from protocol import core
    return core.ActiveCompliance.to_structure(data)

def to_structure_RecordType_core_ClientUser(data):
    from protocol import core
    return core.ClientUser.to_structure(data)

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

def to_structure_RecordType_core_User(data):
    from protocol import core
    return core.User.to_structure(data)

def to_structure_VectorType_RecordType_core_ActiveCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ActiveCompliance(item))
    return lst

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

def to_structure_EnumType_core_APPROVAL_STATUS(data):
    from protocol import core
    return core.APPROVAL_STATUS.to_structure(data)

def to_structure_VectorType_RecordType_knowledgereport_GeographyMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_knowledgereport_GeographyMapping(item))
    return lst

def to_structure_RecordType_clientreport_UserWiseCompliance(data):
    from protocol import clientreport
    return clientreport.UserWiseCompliance.to_structure(data)

def to_structure_VariantType_clientadminsettings_Request(data):
    from protocol import clientadminsettings
    return clientadminsettings.Request.to_structure(data)

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

def to_structure_OptionalType_CustomTextType_20(data):
    if data is None: return data
    return to_structure_CustomTextType_20(data)

def to_structure_OptionalType_VectorType_CustomTextType_20(data):
    if data is None: return data
    return to_structure_VectorType_CustomTextType_20(data)

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

def to_structure_OptionalType_RecordType_core_Division(data):
    if data is None: return data
    return to_structure_RecordType_core_Division(data)

def to_structure_VectorType_RecordType_core_Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Compliance(item))
    return lst


def to_structure_RecordType_dashboard_Compliance(data):
    from protocol import dashboard
    return dashboard.Compliance.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_Compliance(item))
    return lst

def to_structure_MapType_CustomTextType_250_VectorType_RecordType_dashboard_Compliance(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_250(key)
        value = to_structure_VectorType_RecordType_dashboard_Compliance(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_clientadminsettings_LICENCE_HOLDER(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientadminsettings_LICENCE_HOLDER(item))
    return lst

def to_structure_RecordType_clientadminsettings_PROFILE_DETAIL(data):
    from protocol import clientadminsettings
    return clientadminsettings.PROFILE_DETAIL.to_structure(data)

def to_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(data):
    if data is None: return data
    return to_structure_EnumType_core_APPLICABILITY_STATUS(data)

def to_structure_EnumType_core_FILTER_TYPE(data):
    from protocol import core
    return core.FILTER_TYPE.to_structure(data)

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_Statutory(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_core_Level(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_Level(item))
    return lst

def to_structure_VectorType_RecordType_knowledgemaster_Level(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_knowledgemaster_Level(item))
    return lst

def to_structure_VariantType_knowledgetransaction_Request(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Request.to_structure(data)

def to_structure_RecordType_core_StatutoryMapping(data):
    from protocol import core
    return core.StatutoryMapping.to_structure(data)

def to_structure_RecordType_knowledgereport_StatutoryMapping(data):
    from protocol import knowledgereport
    return knowledgereport.StatutoryMappingReport.to_structure(data)

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

def to_structure_RecordType_dashboard_AssigneeChartData(data):
    from protocol import dashboard
    return dashboard.AssigneeChartData.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_AssigneeChartData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_AssigneeChartData(item))
    return lst

def to_structure_RecordType_dashboard_Level1Compliance(data):
    from protocol import dashboard
    return dashboard.Level1Compliance.to_structure(data)

def to_structure_RecordType_core_GroupCompanyDetail(data):
    from protocol import core
    return core.GroupCompanyDetail.to_structure(data)

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_Level1Compliance(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_Text(key)
        value = to_structure_VectorType_RecordType_dashboard_Level1Compliance(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_clientreport_ComplianceUnit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ComplianceUnit(item))
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

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_clientreport_ActivityCompliance(value)
        dict[key] = value
    return dict

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


def to_structure_VectorType_RecordType_technomasters_UnitDetails(data):
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

def to_structure_VectorType_RecordType_technotransactions_UNIT(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technotransactions_UNIT(item))
    return lst

def to_structure_RecordType_clientreport_ServiceProviderCompliance(data):
    from protocol import clientreport
    return clientreport.ServiceProviderCompliance.to_structure(data)

def to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_RecordType_clientreport_ComplianceUnit(value)
        dict[key] = value
    return dict

def to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_Level1Statutory(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_500(key)
        value = to_structure_VectorType_RecordType_clientreport_Level1Statutory(value)
        dict[key] = value
    return dict

def to_structure_RecordType_dashboard_ApplicableDrillDown(data):
    from protocol import dashboard
    return dashboard.ApplicableDrillDown.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_ApplicableDrillDown(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_ApplicableDrillDown(item))
    return lst

def to_structure_OptionalType_VectorType_RecordType_core_Division(data):
    if data is None: return data
    return to_structure_VectorType_RecordType_core_Division(data)

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

def to_structure_VariantType_clientreport_Request(data):
    from protocol import clientreport
    return clientreport.Request.to_structure(data)


def to_structure_RecordType_clientreport_LoginTrace(data):
    from protocol import clientreport
    return clientreport.LoginTrace.to_structure(data)


def to_structure_VectorType_RecordType_clientreport_LoginTrace(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_LoginTrace(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ServiceProviderCompliance(item))
    return lst

def to_structure_RecordType_core_UserGroup(data):
    from protocol import core
    return core.UserGroup.to_structure(data)

def to_structure_RecordType_client_masters_ClientUserGroup(data):
    from protocol import clientmasters
    return clientmasters.ClientUserGroup.to_structure(data)

def to_structure_VectorType_RecordType_core_StatutoryNature(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_StatutoryNature(item))
    return lst

def to_structure_RecordType_clientreport_FormName(data):
    from protocol import clientreport
    return clientreport.FormName.to_structure(data)

def to_structure_VectorType_RecordType_core_AssignedStatutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_AssignedStatutory(item))
    return lst


def to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(item))
    return lst

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

def to_structure_RecordType_core_BusinessGroup(data):
    from protocol import core
    return core.BusinessGroup.to_structure(data)

def to_structure_RecordType_core_ClientBusinessGroup(data):
    from protocol import core
    return core.ClientBusinessGroup.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_FREQUENCY(data):
    from protocol import core
    return core.COMPLIANCE_FREQUENCY.to_structure(data)

def to_structure_RecordType_knowledgereport_GeographyMapping(data):
    from protocol import knowledgereport
    return knowledgereport.GeographyMapping.to_structure(data)

def to_structure_VariantType_clientmasters_Request(data):
    from protocol import clientmasters
    return clientmasters.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_ASSINGED_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.ASSINGED_COMPLIANCE.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_ASSINGED_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_ASSINGED_COMPLIANCE(item))
    return lst

def to_structure_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_USER_WISE_COMPLIANCE(item))
    return lst

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.iteritems() :
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_core_UserDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_UserDetails(item))
    return lst

def to_structure_RecordType_dashboard_ChartDataMap(data):
    from protocol import dashboard
    return dashboard.ChartDataMap.to_structure(data)

def to_structure_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(data):
    from protocol import technoreports
    return technoreports.COUNTRY_WISE_NOTIFICATIONS.to_structure(data)

def to_structure_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(data):
    from protocol import technoreports
    return technoreports.UNIT_WISE_ASSIGNED_STATUTORIES.to_structure(data)

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

def to_structure_RecordType_core_CountryWiseUnits(data):
    from protocol import core
    return core.CountryWiseUnits.to_structure(data)

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

def to_structure_RecordType_clientreport_AssigneeCompliance(data):
    from protocol import clientreport
    return clientreport.AssigneeCompliance.to_structure(data)

def to_structure_RecordType_core_Domain(data):
    from protocol import core
    return core.Domain.to_structure(data)

def to_structure_VectorType_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_AssigneeCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_AssigneeCompliance(item))
    return lst

def to_structure_VariantType_admin_Request(data):
    from protocol import admin
    return admin.Request.to_structure(data)

def to_structure_RecordType_clientreport_ComplianceForUnit(data):
    from protocol import clientreport
    return clientreport.ComplianceForUnit.to_structure(data)

def to_structure_VectorType_RecordType_core_FormCategory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_FormCategory(item))
    return lst

def to_structure_RecordType_dashboard_DrillDownData(data):
    from protocol import dashboard
    return dashboard.DrillDownData.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_RessignedCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_RessignedCompliance(item))
    return lst

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

def to_structure_VariantType_clientuser_Request(data):
    from protocol import clientuser
    return clientuser.Request.to_structure(data)

def to_structure_RecordType_core_Industry(data):
    from protocol import core
    return core.Industry.to_structure(data)

def to_structure_RecordType_core_AssignedStatutory(data):
    from protocol import core
    return core.AssignedStatutory.to_structure(data)

def to_structure_RecordType_core_StatutoryNature(data):
    from protocol import core
    return core.StatutoryNature.to_structure(data)

def to_structure_VariantType_technoreports_Request(data):
    from protocol import technoreports
    return technoreports.Request.to_structure(data)

def to_structure_RecordType_core_Division(data):
    from protocol import core
    return core.Division.to_structure(data)

def to_structure_RecordType_core_ClientDivision(data):
    from protocol import core
    return core.ClientDivision.to_structure(data)

def to_structure_RecordType_core_Country(data):
    from protocol import core
    return core.Country.to_structure(data)

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

def to_structure_VectorType_RecordType_core_ComplianceRepeatType(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceRepeatType(item))
    return lst

# Core Number of compliances

def to_structure_RecordType_core_NumberOfCompliances(data):
    from protocol import core
    return core.NumberOfCompliances.to_structure(data)

def to_structure_VectorType_RecordType_core_NumberOfCompliances(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_NumberOfCompliances(item))
    return lst


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

def to_structure_VectorType_RecordType_clientreport_ComplianceForUnit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ComplianceForUnit(item))
    return lst

def to_structure_RecordType_clientreport_UnitCompliance(data):
    from protocol import clientreport
    return clientreport.UnitCompliance.to_structure(data)

def to_structure_RecordType_core_ComplianceShortDescription(data):
    from protocol import core
    return core.ComplianceShortDescription.to_structure(data)


def to_structure_VectorType_RecordType_core_COMPLIANCE_APPROVAL_STATUS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(item))
    return lst

def to_structure_RecordType_core_ComplianceApplicability(data):
    from protocol import core
    return core.ComplianceApplicability.to_structure(data)

def to_structure_VectorType_RecordType_core_ComplianceApplicability(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceApplicability(item))
    return lst

def to_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability(data):
    if data is None: return None
    return to_structure_VectorType_RecordType_core_ComplianceApplicability(data)

def to_structure_maptype_signedIntegerType_8_VectorType_RecordType_core_ComplianceApplicability(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items() :
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_ComplianceApplicability(value)
        dict[key] = value
    return dict


def to_structure_VectorType_RecordType_core_ComplianceShortDescription(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceShortDescription(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_UnitCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_UnitCompliance(item))
    return lst


def to_structure_VectorType_RecordType_core_ClientUser(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ClientUser(item))
    return lst

def to_structure_RecordType_core_ComplianceRepeatType(data):
    from protocol import core
    return core.ComplianceRepeatType.to_structure(data)

def to_structure_RecordType_core_ComplianceFrequency(data):
    from protocol import core
    return core.ComplianceFrequency.to_structure(data)

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

def to_structure_RecordType_core_ComplianceDurationType(data):
    from protocol import core
    return core.ComplianceDurationType.to_structure(data)

def to_structure_RecordType_clientreport_UserName(data):
    from protocol import clientreport
    return clientreport.UserName.to_structure(data)

def to_structure_RecordType_clienttransactions_APPROVALCOMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.APPROVALCOMPLIANCE.to_structure(data)

def to_structure_RecordType_core_Compliance(data):
    from protocol import core
    return core.Compliance.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(item))
    return lst

def to_structure_RecordType_core_StatutoryDate(data):
    from protocol import core
    return core.StatutoryDate.to_structure(data)

def to_structure_RecordType_clientreport_Activities(data):
    from protocol import clientreport
    return clientreport.Activities.to_structure(data)

def to_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(data):
    from protocol import clienttransactions
    return clienttransactions.ASSIGN_COMPLIANCE_USER.to_structure(data)


def to_structure_CustomIntegerType_1_31(data):
    return parse_number(data, 1, 31)

def to_structure_OptionalType_CustomIntegerType_1_31(data):
    if data is None : return None
    return to_structure_CustomIntegerType_1_31(data)

def to_structure_RecordType_clientreport_ActivityCompliance(data):
    from protocol import clientreport
    return clientreport.ActivityCompliance.to_structure(data)

def to_structure_RecordType_core_Form(data):
    from protocol import core
    return core.Form.to_structure(data)

def to_structure_RecordType_core_Level(data):
    from protocol import core
    return core.Level.to_structure(data)

def to_structure_RecordType_knowledgemaster_Level(data):
    from protocol import knowledgemaster
    return knowledgemaster.Level.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ActivityCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ActivityCompliance(item))
    return lst

def to_structure_OptionalType_CustomTextType_100(data):
    if data is None: return data
    return to_structure_CustomTextType_100(data)

def to_structure_VectorType_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(item))
    return lst

def to_structure_VectorType_RecordType_dashboard_CompliedMap(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_CompliedMap(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_Activities(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_Activities(item))
    return lst

def to_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(data):
    from protocol import clienttransactions
    return clienttransactions.ASSIGN_COMPLIANCE_UNITS.to_structure(data)


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

def to_structure_RecordType_technotransactions_UNIT(data):
    from protocol import technotransactions
    return technotransactions.UNIT.to_structure(data)

def to_structure_RecordType_clientreport_ComplianceName(data):
    from protocol import clientreport
    return clientreport.ComplianceName.to_structure(data)

def to_structure_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.STATUTORYWISECOMPLIANCE.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        d = to_structure_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(item)
        lst.append(d)
    return lst

def to_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.iteritems() :
        key = to_structure_CustomTextType_100(key)
        value = to_structure_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(value)
        dict[key] = value
    return dict

def to_structure_MapType_SignedIntegerType_8_RecordType_core_StatutoryMapping(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_UnsignedIntegerType_32(key)
        value = to_structure_RecordType_core_StatutoryMapping(value)
        dict[key] = value
    return dict

def to_structure_RecordType_clientreport_ComplianceUnit(data):
    from protocol import clientreport
    return clientreport.ComplianceUnit.to_structure(data)

def to_structure_RecordType_core_FormCategory(data):
    from protocol import core
    return core.FormCategory.to_structure(data)

def to_structure_RecordType_clienttransactions_USER_WISE_UNITS(data):
    from protocol import clienttransactions
    return clienttransactions.USER_WISE_UNITS.to_structure(data)

def to_structure_RecordType_clientreport_StatutoryReassignCompliance(data):
    from protocol import clientreport
    return clientreport.StatutoryReassignCompliance.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_StatutoryReassignCompliance(item))
    return lst

def to_structure_VectorType_RecordType_clienttransactions_USER_WISE_UNITS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_USER_WISE_UNITS(item))
    return lst

def to_structure_VariantType_dashboard_Request(data):
    from protocol import dashboard
    return dashboard.Request.to_structure(data)

def to_structure_RecordType_clienttransactions_USER_WISE_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.USER_WISE_COMPLIANCE.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_Level1Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_Level1Compliance(item))
    return lst

def to_structure_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(data):
    from protocol import clienttransactions
    return clienttransactions.STATUTORY_WISE_COMPLIANCES.to_structure(data)

def to_structure_RecordType_dashboard_RessignedCompliance(data):
    from protocol import dashboard
    return dashboard.RessignedCompliance.to_structure(data)

def to_structure_RecordType_clientreport_ComplianceDetails(data):
    from protocol import clientreport
    return clientreport.ComplianceDetails.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ComplianceDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ComplianceDetails(item))
    return lst

def to_structure_VectorType_RecordType_knowledgereport_StatutoryMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_knowledgereport_StatutoryMapping(item))
    return lst

def to_structure_RecordType_clientreport_ActivityLog(data):
    from protocol import clientreport
    return clientreport.ActivityLog.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ActivityLog(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ActivityLog(item))
    return lst

def to_structure_RecordType_clientreport_Level1Statutory(data):
    from protocol import clientreport
    return clientreport.Level1Statutory.to_structure(data)

def to_structure_RecordType_client_transactions_IndustryWiseUnits(data):
    from protocol import clienttransactions
    return clienttransactions.IndustryWiseUnits.to_structure(data)

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
        lst.append(to_structure_RecordType_knowledgetransaction_ApproveMapping(item))
    return lst

def to_structure_MapType_UnsignedIntegerType_32_Bool(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items():
        key = to_structure_UnsignedIntegerType_32(key)
        value = to_structure_Bool(value)
        d[key] = value
    return d

def to_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items():
        key = to_structure_UnsignedIntegerType_32(int(key))
        value = to_structure_UnsignedIntegerType_32(value)
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

def to_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.iteritems():
        key = to_structure_CustomTextType_100(key)
        value = to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(value)
        d[key] = value
    return d

#
#   Get Clients
#

def to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_GeographyWithMapping(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_SignedIntegerType_8(key)
        value = to_structure_VectorType_RecordType_core_GeographyWithMapping(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_core_GeographyWithMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_GeographyWithMapping(item))
    return lst

def to_structure_RecordType_core_GeographyWithMapping(data):
    from protocol import core
    return core.GeographyWithMapping.to_structure(data)

#
# Trend Chart
#
def to_structure_OptionalType_VectorType_UnsignedIntegerType_32(data):
    if data is None: return data
    return to_structure_VectorType_UnsignedIntegerType_32(data)

def to_structure_VectorType_RecordType_dashboard_TrendCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_TrendCompliance(item))
    return lst

def to_structure_RecordType_dashboard_TrendCompliance(data):
    from protocol import dashboard
    return dashboard.TrendCompliance.to_structure(data)

def to_structure_MapType_CustomTextType_100_VectorType_RecordType_dashboard_TrendCompliance(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_100(key)
        value = to_structure_VectorType_RecordType_dashboard_TrendCompliance(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_dashboard_TrendDrillDownData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_TrendDrillDownData(item))
    return lst

def to_structure_RecordType_dashboard_TrendDrillDownData(data):
    from protocol import dashboard
    return dashboard.TrendDrillDownData.to_structure(data)

# Statutory Notifications (Techno)

def to_structure_VectorType_RecordType_technoreports_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_technoreports_NOTIFICATIONS(item))
    return lst

def to_structure_RecordType_technoreports_NOTIFICATIONS(data):
    from protocol import technoreports
    return technoreports.NOTIFICATIONS.to_structure(data)

# Complaince details report
def to_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        item1 = to_structure_RecordType_clientreport_ComplianceDetailsUnitWise(item)
        lst.append(item1)
    return lst

def to_structure_RecordType_clientreport_ComplianceDetailsUnitWise(data):
    from protocol import clientreport
    return clientreport.ComplianceDetailsUnitWise.to_structure(data)

# Client Compliance Filter
def to_structure_VectorType_RecordType_core_ComplianceFilter(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceFilter(item))
    return lst

def to_structure_RecordType_core_ComplianceFilter(data):
    from protocol import core
    return core.ComplianceFilter.to_structure(data)

# not complied enum type

def to_structure_EnumType_core_NOT_COMPLIED_TYPE(data):
    from protocol import core
    return core.NOT_COMPLIED_TYPE.to_structure(data)

def to_structure_OptionalType_CustomTextType_250(data):
    if data is None: return data
    return parse_custom_string(data, 250)

def to_structure_VectorType_CustomTextType_100(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_CustomTextType_100(item))
    return lst

# Risk Report

def to_structure_VectorType_RecordType_clientreport_RiskData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_RiskData(item))
    return lst

def to_structure_RecordType_clientreport_RiskData(data):
    from protocol import clientreport
    return clientreport.RiskData.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_Level1Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_Level1Compliance(item))
    return lst

def to_structure_RecordType_clientreport_Level1Compliance(data):
    from protocol import clientreport
    return clientreport.Level1Compliance.to_structure(data)

# Client Notification

def to_structure_VectorType_RecordType_dashboard_Notification(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_Notification(item))
    return lst

def to_structure_RecordType_dashboard_Notification(data):
    from protocol import dashboard
    return dashboard.Notification.to_structure(data)

def to_structure_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(data):
    from protocol import clientreport
    return clientreport.STATUTORY_WISE_NOTIFICATIONS.to_structure(data)

def to_structure_VectorType_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS(item))
    return lst

def to_structure_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS(data):
    from protocol import clientreport
    return clientreport.LEVEL_1_STATUTORY_NOTIFICATIONS.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(item))
    return lst

def to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_500(key)
        value = to_structure_VectorType_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS(value)
        dict[key] = value
    return dict
# ReassignUnitCompliance

def to_structure_RecordType_clientreport_ReassignUnitCompliance(data):
    from protocol import clientreport
    return clientreport.ReassignUnitCompliance.to_structure(data)

def to_structure_VectorType_RecordType_clientreport_ReassignUnitCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ReassignUnitCompliance(item))
    return lst

def to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(item))
    return lst

def to_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(data):
    from protocol import clienttransactions
    return clienttransactions.UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS.to_structure(data)

def to_structure_OptionalType_EnumType_core_COMPLIANCE_FREQUENCY(data):
    if data is None: return data
    return to_structure_EnumType_core_COMPLIANCE_FREQUENCY(data)

# Compliance Activity Report

def to_structure_VectorType_RecordType_clientreport_ActivityData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_ActivityData(item))
    return lst

def to_structure_RecordType_clientreport_ActivityData(data):
    from protocol import clientreport
    return clientreport.ActivityData.to_structure(data)

def to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ActivityData(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_500(key)
        value = to_structure_VectorType_RecordType_clientreport_ActivityData(value)
        dict[key] = value
    return dict

def to_structure_MapType_CustomTextType_500_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ActivityData(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_500(key)
        value = to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ActivityData(value)
        dict[key] = value
    return dict

def to_structure_OptionalType_VectorType_RecordType_dashboard_RessignedCompliance(data):
    if data is None: return data
    return to_structure_VectorType_RecordType_dashboard_RessignedCompliance(data)

def to_structure_VectorType_RecordType_client_report_GroupedUnits(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_client_report_GroupedUnits(item))
    return lst

def to_structure_RecordType_client_report_GroupedUnits(data):
    from protocol import clientreport
    return clientreport.GroupedUnits.to_structure(data)

def to_structure_VectorType_RecordType_client_report_UnitDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_client_report_UnitDetails(item))
    return lst

def to_structure_RecordType_client_report_UnitDetails(data):
    from protocol import clientreport
    return clientreport.UnitDetails.to_structure(data)

def to_structure_RecordType_core_Compliance_Download(data):
    from protocol import core
    return core.Compliance_Download.to_structure(data)

def to_structure_VectorType_RecordType_core_Compliance_Download(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_core_Compliance_Download(item))
    return lst

def to_structure_VectorType_CustomTextType_500(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_CustomTextType_500(item))
    return lst

def to_structure_OptionalType_VectorType_CustomTextType_500(data):
    if data is None: return data
    return to_structure_VectorType_CustomTextType_500(data)

def to_structure_RecordType_core_StatutoryApprovalStatus(data):
    from protocol import core
    return core.StatutoryApprovalStatus.to_structure(data)

def to_structure_VectorType_RecordType_core_StatutoryApprovalStatus(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_StatutoryApprovalStatus(item))
    return lst

def to_structure_VectorType_RecordType_clienttransactions_PastRecordUnits(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clienttransactions_PastRecordUnits(item))
    return lst

def to_structure_RecordType_clienttransactions_PastRecordUnits(data):
    from protocol import clienttransactions
    return clienttransactions.PastRecordUnits.to_structure(data)

def to_structure_MapType_CustomTextType_50_VectorType_CustomTextType_500(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_50(key)
        value = to_structure_VectorType_CustomTextType_500(value)
        dict[key] = value
    return dict

def to_structure_MapType_CustomTextType_500_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_500(key)
        value = to_structure_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(value)
        dict[key] = value
    return dict

def to_structure_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_AssigneeWiseLevel1Compliance(item))
    return lst

def to_structure_RecordType_dashboard_AssigneeWiseLevel1Compliance(data):
    from protocol import dashboard
    return dashboard.AssigneeWiseLevel1Compliance.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_YearWise(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_YearWise(item))
    return lst

def to_structure_RecordType_dashboard_YearWise(data):
    from protocol import dashboard
    return dashboard.YearWise.to_structure(data)

def to_structure_RecordType_dashboard_AssigneeWiseCompliance(data):
    from protocol import dashboard
    return dashboard.AssigneeWiseCompliance.to_inner_structure(data)

def to_structure_VectorType_RecordType_core_ClientInchargePersons(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ClientInchargePersons(item))
    return lst

def to_structure_RecordType_core_ClientInchargePersons(data):
    from protocol import core
    return core.ClientInchargePersons.to_structure(data)

def to_structure_RecordType_dashboard_DomainWiseYearConfiguration(data):
    from protocol import dashboard
    return dashboard.DomainWiseYearConfiguration.to_structure(data)

def to_structure_VectorType_RecordType_dashboard_DomainWiseYearConfiguration(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_dashboard_DomainWiseYearConfiguration(item))
    return lst

def to_structure_MapType_CustomTextType_100_VectorType_RecordType_dashboard_DomainWiseYearConfiguration(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_100(key)
        value = to_structure_VectorType_RecordType_dashboard_DomainWiseYearConfiguration(value)
        d[key] = value
    return d

def to_structure_MapType_CustomTextType_250_VectorType_RecordType_clientuser_ComplianceOnOccurrence(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_CustomTextType_250(key)
        value = to_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence(value)
        dict[key] = value
    return dict

def to_structure_OptionalType_RecordType_core_FileList(data):
    if data is None: return data
    return to_structure_RecordType_core_FileList(data)

def to_structure_VectorType_CustomTextType_250(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_Text(item))
    return lst

def to_structure_OptionalType_VectorType_CustomTextType_250(data):
    if data is None: return data
    return to_structure_VectorType_CustomTextType_250(data)

def to_structure_VectorType_RecordType_core_GroupCompanyForUnitCreation(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_GroupCompanyForUnitCreation(item))
    return lst

def to_structure_RecordType_core_GroupCompanyForUnitCreation(data):
    from protocol import core
    return core.GroupCompanyForUnitCreation.to_structure(data)

def to_structure_RecordType_clienttransactions_NewUnitSettings(data):
    from protocol import clienttransactions
    return clienttransactions.NewUnitSettings.to_structure(data)

def to_structure_VectorType_RecordType_clienttransactions_NewUnitSettings(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_clienttransactions_NewUnitSettings(item))
    return lst

def to_structure_OptionalType_VectorType_RecordType_clienttransactions_NewUnitSettings(data):
    if data is None: return data
    return to_structure_VectorType_RecordType_clienttransactions_NewUnitSettings(data)

def to_structure_RecordType_mobile_GetUSersList(data):
    from protocol import mobile
    return mobile.GetUsersList.to_structure(data)

def to_structure_VectorType_RecordType_mobile_GetUsersList(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_mobile_GetUSersList(item))
    return lst

def to_structure_RecordType_mobile_ComplianceApplicability(data):
    from protocol import mobile
    return mobile.ComplianceApplicability.to_structure(data)

def to_structure_VectorType_RecordType_mobile_ComplianceApplicability(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_mobile_ComplianceApplicability(item))
    return lst

def to_structure_VectorType_RecordType_mobile_UnitWiseCount(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_mobile_UnitWiseCount(item))
    return lst

def to_structure_RecordType_mobile_UnitWiseCount(data):
    from protocol import mobile
    return mobile.UnitWiseCount.to_structure(data)


def to_structure_VectorType_RecordType_mobile_DomainWiseCount(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_mobile_DomainWiseCount(item))
    return lst

def to_structure_RecordType_mobile_DomainWiseCount(data):
    from protocol import mobile
    return mobile.DomainWiseCount.to_structure(data)

def to_structure_VariantType_mobile_Request(data):
    from protocol import mobile
    return mobile.Request.to_structure(data)

def to_structure_RecordType_mobile_ComplianceHistory(data):
    from protocol import mobile
    return mobile.ComplianceHistory.to_structure(data)

def to_structure_VectorType_RecordType_mobile_ComplianceHistory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(to_structure_RecordType_mobile_ComplianceHistory(item))
    return lst

def to_structure_VectorType_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(item))
    return lst

def to_structure_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(data):
    from protocol import clientreport
    return clientreport.GetComplianceTaskApplicabilityStatusReportData.to_structure(data)
