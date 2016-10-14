from protocol.jsonvalidators import (
    parse_bool,
    parse_number,
    parse_point_numbers,
    parse_string,
    parse_custom_string,
    parse_list,
    parse_dictionary
)


def parse_structure_VectorType(data, fn):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(fn(item))
    return lst


def parse_structure_MapType(data, fn1, fn2):
    map = {}
    for key, value in data.items():
        key = fn1(key)
        value = fn2(value)
        map[key] = value
    return map


def parse_structure_VectorType_RecordType_clientreport_User(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_User(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_UnitName(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_UnitName(item))
    return lst

def parse_structure_VectorType_RecordType_general_Notification(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_general_Notification(item))
    return lst

def parse_structure_VectorType_RecordType_general_User(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_general_User(item))
    return lst

def parse_structure_VectorType_RecordType_general_AuditTrail(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_general_AuditTrail(item))
    return lst

def parse_structure_VectorType_RecordType_general_AuditTrailForm(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_general_AuditTrailForm(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_ComplianceName(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ComplianceName(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_Level1Statutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_Level1Statutory(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_UserName(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_UserName(item))
    return lst


def parse_structure_OptionalType_VectorType_SignedIntegerType_8(data):
    if data is None:
        return data
    return parse_structure_VectorType_SignedIntegerType_8(data)


def parse_structure_OptionalType_CustomTextType_50(data):
    if data is None:
        return data
    return parse_structure_CustomTextType_50(data)


def parse_structure_VariantType_knowledgemaster_Request(data):
    from protocol import knowledgemaster
    return knowledgemaster.Request.parse_structure(data)


def parse_structure_VariantType_clientcoordinationmaster_Request(data):
    from protocol import clientcoordinationmaster
    return clientcoordinationmaster.Request.parse_structure(data)


def parse_structure_OptionalType_SignedIntegerType_8(data):
    if data is None:
        return data
    return parse_structure_SignedIntegerType_8(data)


def parse_structure_OptionalType_UnsignedIntegerType_32(data):
    if data is None:
        return None
    return parse_structure_UnsignedIntegerType_32(data)


def parse_structure_RecordType_clientreport_ReassignHistory(data):
    from protocol import clientreport
    return clientreport.ReassignHistory.parse_structure(data)

def parse_structure_RecordType_general_Notification(data):
    from protocol import general
    return general.Notification.parse_structure(data)

def parse_structure_RecordType_general_User(data):
    from protocol import core
    return core.User.parse_structure(data)

def parse_structure_RecordType_general_AuditTrail(data):
    from protocol import general
    return general.AuditTrail.parse_structure(data)

def parse_structure_RecordType_general_AuditTrailForm(data):
    from protocol import general
    return general.AuditTrailForm.parse_structure(data)

def parse_structure_VectorType_SignedIntegerType_8(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_SignedIntegerType_8(item))
    return lst

def parse_structure_VectorType_UnsignedIntegerType_32(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_UnsignedIntegerType_32(item))
    return lst

def parse_structure_MapType_CustomTextType_50_VectorType_RecordType_core_Form(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_CustomTextType_50(key)
        value = parse_structure_VectorType_RecordType_core_Form(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_ReassignHistory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ReassignHistory(item))
    return lst

def parse_structure_RecordType_dashboard_TrendData(data):
    from protocol import dashboard
    return dashboard.TrendData.parse_structure(data)

def parse_structure_RecordType_clientreport_ReassignCompliance(data):
    from protocol import clientreport
    return clientreport.ReassignCompliance.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_ReassignCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ReassignCompliance(item))
    return lst

def parse_structure_VectorType_RecordType_core_Country(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Country(item))
    return lst

def parse_structure_Bool(data):
    return parse_bool(data)

def parse_structure_VectorType_RecordType_core_BusinessGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_BusinessGroup(item))
    return lst

def parse_structure_VectorType_RecordType_core_UserGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_UserGroup(item))
    return lst

def parse_structure_VectorType_RecordType_client_masters_ClientUserGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_client_masters_ClientUserGroup(item))
    return lst

def parse_structure_VectorType_RecordType_core_LegalEntity(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_LegalEntity(item))
    return lst

def parse_structure_VectorType_RecordType_core_ClientConfiguration(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ClientConfiguration(item))
    return lst

def parse_structure_SignedIntegerType_8(data):
    # return parse_number(data, -128, 127)
    return parse_number(data, 0, 52949672950)

def parse_structure_UnsignedIntegerType_32(data):
    return parse_number(data, 0, 52949672950)

def parse_structure_Smallvalue(data):
    return parse_number(data, 0, 999)

def parse_structure_OptionalType_Smallvalue(data):
    if data is None : return None
    return parse_structure_Smallvalue(data)

def parse_structure_VectorType_RecordType_core_Division(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Division(item))
    return lst

def parse_structure_VectorType_RecordType_techno_master_COUNTRYWISEUNITS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_techno_master_COUNTRYWISEUNITS(item))
    return lst

def parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_core_Industry(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Industry(item))
    return lst

def parse_structure_VariantType_technomasters_Request(data):
    from protocol import technomasters
    return technomasters.Request.parse_structure(data)

def parse_structure_MapType_UnsignedIntegerType_32_VectorType_RecordType_core_Geography(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_UnsignedIntegerType_32(key)
        value = parse_structure_VectorType_RecordType_core_Geography(value)
        d[key] = value
    return d

def parse_structure_RecordType_dashboard_CompliedMap(data):
    from protocol import dashboard
    return dashboard.CompliedMap.parse_structure(data)

def parse_structure_Float(data):
    return parse_point_numbers(data)

def parse_structure_VectorType_RecordType_core_Geography(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Geography(item))
    return lst

def parse_structure_RecordType_clientreport_ComplianceList(data):
    from protocol import clientreport
    return clientreport.ComplianceList.parse_structure(data)

def parse_structure_VectorType_CustomTextType_20(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_CustomTextType_20(item))
    return lst

def parse_structure_Text(data):
    return parse_string(data)

def parse_structure_OptionalType_Text(data):
    if data is None: return None
    return parse_structure_Text(data)

def parse_structure_VectorType_CustomTextType_50(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_CustomTextType_50(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_ComplianceList(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ComplianceList(item))
    return lst

def parse_structure_RecordType_clientreport_ApplicabilityCompliance(data):
    from protocol import clientreport
    return clientreport.ApplicabilityCompliance.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_ApplicabilityCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ApplicabilityCompliance(item))
    return lst

def parse_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ApplicabilityCompliance(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_CustomTextType_500(key)
        value = parse_structure_VectorType_RecordType_clientreport_ApplicabilityCompliance(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_core_ServiceProvider(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ServiceProvider(item))
    return lst

def parse_structure_VectorType_RecordType_core_ServiceProviderDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ServiceProviderDetails(item))
    return lst

def parse_structure_VectorType_RecordType_core_Domain(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Domain(item))
    return lst

def parse_structure_CustomTextType_20(data):
    return parse_custom_string(data, 20)

def parse_structure_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.REASSIGNED_COMPLIANCE.parse_structure(data)

def parse_structure_RecordType_technotransactions_ASSIGNED_STATUTORIES(data):
    from protocol import technotransactions
    return technotransactions.ASSIGNED_STATUTORIES.parse_structure(data)

def parse_structure_VectorType_RecordType_core_GroupCompany(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_GroupCompany(item))
    return lst

def parse_structure_VectorType_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(item))
    return lst

def parse_structure_VectorType_Text(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_Text(item))
    return lst

def parse_structure_CustomTextType_100(data):
    return parse_custom_string(data, 100)

def parse_structure_CustomTextType_200(data):
    return parse_custom_string(data, 200)

def parse_structure_CustomTextType_250(data):
    return parse_custom_string(data, 250)

def parse_structure_OptionalType_Bool(data):
    if data is None: return data
    return parse_structure_Bool(data)

def parse_structure_RecordType_core_ServiceProvider(data):
    from protocol import core
    return core.ServiceProvider.parse_structure(data)

def parse_structure_RecordType_core_ServiceProviderDetails(data):
    from protocol import core
    return core.ServiceProviderDetails.parse_structure(data)

def parse_structure_RecordType_technomasters_LICENCE_HOLDER_DETAILS(data):
    from protocol import technomasters
    return technomasters.LICENCE_HOLDER_DETAILS.parse_structure(data)

def parse_structure_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.PAST_RECORD_COMPLIANCE.parse_structure(data)

def parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(value)
        d[key] = value
    return d

def parse_structure_CustomTextType_50(data):
    return parse_custom_string(data, 50)

def parse_structure_VariantType_clienttransactions_Request(data):
    from protocol import clienttransactions
    return clienttransactions.Request.parse_structure(data)

def parse_structure_CustomTextType_500(data):
    return parse_custom_string(data, 500)

def parse_structure_RecordType_technomasters_PROFILE_DETAIL(data):
    from protocol import technomasters
    return technomasters.PROFILE_DETAIL.parse_structure(data)

def parse_structure_CustomIntegerType_1_10(data):
    return parse_number(data, 1, 10)

def parse_structure_CustomIntegerType_1_100(data):
    return parse_number(data, 1, 100)

def parse_structure_OptionalType_CustomIntegerType_1_100(data):
    if data is None : return None
    return parse_structure_CustomIntegerType_1_100(data)

def parse_structure_VectorType_RecordType_technotransactions_ASSIGNED_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technotransactions_ASSIGNED_STATUTORIES(item))
    return lst

def parse_structure_RecordType_core_UserDetails(data):
    from protocol import core
    return core.UserDetails.parse_structure(data)

def parse_structure_RecordType_technomasters_PROFILES(data):
    from protocol import technomasters
    return technomasters.PROFILES.parse_structure(data)

def parse_structure_EnumType_core_SESSION_TYPE(data):
    from protocol import core
    return core.SESSION_TYPE.parse_structure(data)

def parse_structure_EnumType_core_USER_TYPE(data):
    from protocol import core
    return core.USER_TYPE.parse_structure(data)

def parse_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_APPROVAL_STATUS.parse_structure(data)

def parse_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_ACTIVITY_STATUS.parse_structure(data)

def parse_structure_VectorType_RecordType_core_Unit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Unit(item))
    return lst

def parse_structure_CustomIntegerType_1_12(data):
    return parse_number(data, 1, 12)

def parse_structure_OptionalType_CustomIntegerType_1_12(data):
    if data is None: return None
    return parse_structure_CustomIntegerType_1_12(data)

def parse_structure_EnumType_core_COMPLIANCE_STATUS(data):
    from protocol import core
    return core.COMPLIANCE_STATUS.parse_structure(data)

def parse_structure_EnumType_core_APPLICABILITY_STATUS(data):
    from protocol import core
    return core.APPLICABILITY_STATUS.parse_structure(data)

def parse_structure_EnumType_core_REPEATS_TYPE(data):
    from protocol import core
    return core.REPEATS_TYPE.parse_structure(data)

def parse_structure_EnumType_core_DURATION_TYPE(data):
    from protocol import core
    return core.DURATION_TYPE.parse_structure(data)

def parse_structure_RecordType_core_ActiveCompliance(data):
    from protocol import core
    return core.ActiveCompliance.parse_structure(data)

def parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_VectorType_RecordType_core_Level(value)
        d[key] = value
    return d

def parse_structure_RecordType_core_User(data):
    from protocol import core
    return core.User.parse_structure(data)

def parse_structure_VectorType_RecordType_core_ActiveCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ActiveCompliance(item))
    return lst

def parse_structure_VectorType_RecordType_core_UpcomingCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_UpcomingCompliance(item))
    return lst

def parse_structure_VectorType_RecordType_dashboard_DomainWise(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_DomainWise(item))
    return lst

def parse_structure_EnumType_core_APPROVAL_STATUS(data):
    from protocol import core
    return core.APPROVAL_STATUS.parse_structure(data)

def parse_structure_VectorType_RecordType_knowledgereport_GeographyMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_knowledgereport_GeographyMapping(item))
    return lst

def parse_structure_RecordType_clientreport_UserWiseCompliance(data):
    from protocol import clientreport
    return clientreport.UserWiseCompliance.parse_structure(data)

def parse_structure_VariantType_clientadminsettings_Request(data):
    from protocol import clientadminsettings
    return clientadminsettings.Request.parse_structure(data)

def parse_structure_RecordType_clientuser_ComplianceOnOccurrence(data):
    from protocol import clientuser
    return clientuser.ComplianceOnOccurrence.parse_structure(data)

def parse_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientuser_ComplianceOnOccurrence(item))
    return lst

def parse_structure_VectorType_RecordType_core_Statutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Statutory(item))
    return lst

def parse_structure_OptionalType_RecordType_techno_master_BUSINESSGROUP(data):
    if data is None: return data
    return parse_structure_RecordType_techno_master_BUSINESSGROUP(data)

def parse_structure_OptionalType_RecordType_techno_master_LEGALENTITY(data):
    if data is None: return data
    return parse_structure_RecordType_techno_master_LEGALENTITY(data)

def parse_structure_OptionalType_RecordType_techno_master_DIVISION(data):
    if data is None: return data
    return parse_structure_RecordType_techno_master_DIVISION(data)

def parse_structure_OptionalType_CustomTextType_20(data):
    if data is None: return data
    return parse_structure_CustomTextType_20(data)

def parse_structure_OptionalType_VectorType_CustomTextType_20(data):
    if data is None: return data
    return parse_structure_VectorType_CustomTextType_20(data)

def parse_structure_VectorType_RecordType_dashboard_AssigneeWiseDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_AssigneeWiseDetails(item))
    return lst

def parse_structure_RecordType_clientadminsettings_LICENCE_HOLDER(data):
    from protocol import clientadminsettings
    return clientadminsettings.LICENCE_HOLDER.parse_structure(data)

def parse_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE(data):
    from protocol import core
    return core.ASSIGN_STATUTORY_SUBMISSION_TYPE.parse_structure(data)

def parse_structure_VariantType_technotransactions_Request(data):
    from protocol import technotransactions
    return technotransactions.Request.parse_structure(data)

def parse_structure_VectorType_RecordType_core_Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Compliance(item))
    return lst

def parse_structure_RecordType_dashboard_Compliance(data):
    from protocol import dashboard
    return dashboard.Compliance.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_Compliance(item))
    return lst

def parse_structure_MapType_CustomTextType_250_VectorType_RecordType_dashboard_Compliance(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = parse_structure_CustomTextType_250(key)
        value = parse_structure_VectorType_RecordType_dashboard_Compliance(value)
        dict[key] = value
    return dict


def parse_structure_VectorType_RecordType_clientadminsettings_LICENCE_HOLDER(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientadminsettings_LICENCE_HOLDER(item))
    return lst

def parse_structure_RecordType_clientadminsettings_PROFILE_DETAIL(data):
    from protocol import clientadminsettings
    return clientadminsettings.PROFILE_DETAIL.parse_structure(data)

def parse_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(data):
    if data is None: return data
    return parse_structure_EnumType_core_APPLICABILITY_STATUS(data)

def parse_structure_VectorType_RecordType_clientadminsettings_PROFILE_DETAIL(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientadminsettings_PROFILE_DETAIL(item))
    return lst

def parse_structure_EnumType_core_FILTER_TYPE(data):
    from protocol import core
    return core.FILTER_TYPE.parse_structure(data)

def parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_VectorType_RecordType_core_Statutory(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_core_Level(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Level(item))
    return lst

def parse_structure_VectorType_RecordType_knowledgemaster_Level(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_knowledgemaster_Level(item))
    return lst

def parse_structure_VariantType_knowledgetransaction_Request(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.Request.parse_structure(data)

def parse_structure_RecordType_core_StatutoryMapping(data):
    from protocol import core
    return core.StatutoryMapping.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_DrillDownData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_DrillDownData(item))
    return lst

def parse_structure_RecordType_core_LegalEntity(data):
    from protocol import core
    return core.LegalEntity.parse_structure(data)

def parse_structure_RecordType_core_GroupCompany(data):
    from protocol import core
    return core.GroupCompany.parse_structure(data)

def parse_structure_RecordType_dashboard_AssigneeChartData(data):
    from protocol import dashboard
    return dashboard.AssigneeChartData.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_AssigneeChartData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_AssigneeChartData(item))
    return lst

def parse_structure_RecordType_dashboard_Level1Compliance(data):
    from protocol import dashboard
    return dashboard.Level1Compliance.parse_structure(data)

def parse_structure_RecordType_core_GroupCompanyDetail(data):
    from protocol import core
    return core.GroupCompanyDetail.parse_structure(data)

def parse_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_Level1Compliance(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_Text(key)
        value = parse_structure_VectorType_RecordType_dashboard_Level1Compliance(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_clientreport_ComplianceUnit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ComplianceUnit(item))
    return lst

def parse_structure_VariantType_general_Request(data):
    from protocol import general
    return general.Request.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_UserWiseCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_UserWiseCompliance(item))
    return lst

def parse_structure_OptionalType_VectorType_RecordType_core_BusinessGroup(data):
    if data is None: return data
    return parse_structure_VectorType_RecordType_core_BusinessGroup(data)

def parse_structure_VectorType_RecordType_technomasters_LICENCE_HOLDER_DETAILS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technomasters_LICENCE_HOLDER_DETAILS(item))
    return lst

def parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_CustomTextType_50(key)
        value = parse_structure_VectorType_RecordType_clientreport_ActivityCompliance(value)
        d[key] = value
    return d

def parse_structure_VariantType_knowledgereport_Request(data):
    from protocol import knowledgereport
    return knowledgereport.Request.parse_structure(data)

def parse_structure_VectorType_RecordType_core_UnitDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_UnitDetails(item))
    return lst

def parse_structure_VectorType_RecordType_techno_report_UnitDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_techno_report_UnitDetails(item))
    return lst

def parse_structure_VectorType_RecordType_techno_master_UNIT(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_techno_master_UNIT(item))
    return lst

def parse_structure_VectorType_RecordType_technomasters_Unit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technomasters_Unit(item))
    return lst

def parse_structure_VectorType_RecordType_technomasters_CountryWiseUnits(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technomasters_CountryWiseUnits(item))
    return lst

def parse_structure_VectorType_RecordType_technotransactions_UNIT(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technotransactions_UNIT(item))
    return lst

def parse_structure_RecordType_clientreport_ServiceProviderCompliance(data):
    from protocol import clientreport
    return clientreport.ServiceProviderCompliance.parse_structure(data)

def parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_CustomTextType_50(key)
        value = parse_structure_VectorType_RecordType_clientreport_ComplianceUnit(value)
        d[key] = value
    return d

def parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_Level1Statutory(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_CustomTextType_50(key)
        value = parse_structure_VectorType_RecordType_clientreport_Level1Statutory(value)
        d[key] = value
    return d

def parse_structure_RecordType_dashboard_ApplicableDrillDown(data):
    from protocol import dashboard
    return dashboard.ApplicableDrillDown.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_ApplicableDrillDown(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_ApplicableDrillDown(item))
    return lst

def parse_structure_OptionalType_VectorType_RecordType_core_Division(data):
    if data is None: return data
    return parse_structure_VectorType_RecordType_core_Division(data)

def parse_structure_RecordType_core_UnitDetails(data):
    from protocol import core
    return core.UnitDetails.parse_structure(data)

def parse_structure_RecordType_techno_report_UnitDetails(data):
    from protocol import technoreports
    return technoreports.UnitDetails.parse_structure(data)

def parse_structure_VariantType_clientreport_Request(data):
    from protocol import clientreport
    return clientreport.Request.parse_structure(data)

def parse_structure_RecordType_clientreport_LoginTrace(data):
    from protocol import clientreport
    return clientreport.LoginTrace.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_LoginTrace(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_LoginTrace(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ServiceProviderCompliance(item))
    return lst

def parse_structure_RecordType_core_UserGroup(data):
    from protocol import core
    return core.UserGroup.parse_structure(data)

def parse_structure_RecordType_client_masters_ClientUserGroup(data):
    from protocol import clientmasters
    return clientmasters.ClientUserGroup.parse_structure(data)

def parse_structure_VectorType_RecordType_core_StatutoryNature(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_StatutoryNature(item))
    return lst

def parse_structure_RecordType_clientreport_FormName(data):
    from protocol import clientreport
    return clientreport.FormName.parse_structure(data)

def parse_structure_VectorType_RecordType_core_AssignedStatutory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_AssignedStatutory(item))
    return lst

def parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(item))
    return lst

def parse_structure_VectorType_RecordType_core_StatutoryDate(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_StatutoryDate(item))
    return lst

def parse_structure_OptionalType_VectorType_RecordType_core_StatutoryDate(data):
    if data is None : return None
    return parse_structure_VectorType_RecordType_core_StatutoryDate(data)

def parse_structure_RecordType_core_FileList(data):
    from protocol import core
    return core.FileList.parse_structure(data)

def parse_structure_VectorType_RecordType_core_FileLst(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_core_FileList(item))
    return lst

def parse_structure_OptionalType_VectorType_RecordType_core_FileList(data):
    if data is None: return None
    return parse_structure_VectorType_RecordType_core_FileLst(data)

def parse_structure_VectorType_RecordType_core_User(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_User(item))
    return lst

def parse_structure_VectorType_RecordType_core_GroupCompanyDetail(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_GroupCompanyDetail(item))
    return lst

def parse_structure_RecordType_core_BusinessGroup(data):
    from protocol import core
    return core.BusinessGroup.parse_structure(data)

def parse_structure_RecordType_techno_master_BUSINESSGROUP(data):
    from protocol import technomasters
    return technomasters.BUSINESS_GROUP.parse_inner_structure(data)

def parse_structure_RecordType_techno_master_LEGALENTITY(data):
    from protocol import technomasters
    return technomasters.LEGAL_ENTITY.parse_inner_structure(data)

def parse_structure_RecordType_techno_master_DIVISION(data):
    from protocol import technomasters
    return technomasters.DIVISION.parse_inner_structure(data)

def parse_structure_RecordType_techno_master_UNIT(data):
    from protocol import technomasters
    return technomasters.UNIT.parse_structure(data)

def parse_structure_RecordType_technomasters_Unit(data):
    from protocol import technomasters
    return technomasters.Unit.parse_structure(data)

def parse_structure_RecordType_technomasters_CountryWiseUnits(data):
    from protocol import technomasters
    return technomasters.CountryWiseUnits.parse_structure(data)

def parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(data):
    from protocol import core
    return core.COMPLIANCE_FREQUENCY.parse_structure(data)

def parse_structure_RecordType_knowledgereport_GeographyMapping(data):
    from protocol import knowledgereport
    return knowledgereport.GeographyMapping.parse_structure(data)

def parse_structure_VariantType_clientmasters_Request(data):
    from protocol import clientmasters
    return clientmasters.Request.parse_structure(data)

def parse_structure_RecordType_clienttransactions_ASSINGED_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.ASSINGED_COMPLIANCE.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_ASSINGED_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_ASSINGED_COMPLIANCE(item))
    return lst

def parse_structure_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_USER_WISE_COMPLIANCE(item))
    return lst

def parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.iteritems() :
        key = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE(value)
        dict[key] = value
    return dict

def parse_structure_VectorType_RecordType_core_UserDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_UserDetails(item))
    return lst

def parse_structure_RecordType_dashboard_ChartDataMap(data):
    from protocol import dashboard
    return dashboard.ChartDataMap.parse_structure(data)

def parse_structure_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(data):
    from protocol import technoreports
    return technoreports.COUNTRY_WISE_NOTIFICATIONS.parse_structure(data)

def parse_structure_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(data):
    from protocol import technoreports
    return technoreports.UNIT_WISE_ASSIGNED_STATUTORIES.parse_structure(data)

def parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_knowledgereport_GeographyMapping(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_VectorType_RecordType_knowledgereport_GeographyMapping(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(item))
    return lst

def parse_structure_RecordType_dashboard_EscalationData(data):
    from protocol import dashboard
    return dashboard.EscalationData.parse_structure(data)

def parse_structure_RecordType_core_Menu(data):
    from protocol import core
    return core.Menu.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_EscalationData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_EscalationData(item))
    return lst

def parse_structure_RecordType_techno_master_COUNTRYWISEUNITS(data):
    from protocol import technomasters
    return technomasters.COUNTRYWISEUNITS.parse_structure(data)

def parse_structure_RecordType_clientreport_UnitName(data):
    from protocol import clientreport
    return clientreport.UnitName.parse_structure(data)

def parse_structure_VectorType_RecordType_core_Form(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Form(item))
    return lst

def parse_structure_VectorType_RecordType_dashboard_TrendData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_TrendData(item))
    return lst

def parse_structure_RecordType_core_ClientConfiguration(data):
    from protocol import core
    return core.ClientConfiguration.parse_structure(data)

def parse_structure_RecordType_clientreport_AssigneeCompliance(data):
    from protocol import clientreport
    return clientreport.AssigneeCompliance.parse_structure(data)

def parse_structure_RecordType_core_Domain(data):
    from protocol import core
    return core.Domain.parse_structure(data)

def parse_structure_VectorType_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_AssigneeCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_AssigneeCompliance(item))
    return lst

def parse_structure_VariantType_admin_Request(data):
    from protocol import admin
    return admin.Request.parse_structure(data)

def parse_structure_RecordType_clientreport_ComplianceForUnit(data):
    from protocol import clientreport
    return clientreport.ComplianceForUnit.parse_structure(data)

def parse_structure_VectorType_RecordType_core_FormCategory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_FormCategory(item))
    return lst

def parse_structure_RecordType_dashboard_DrillDownData(data):
    from protocol import dashboard
    return dashboard.DrillDownData.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_RessignedCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_RessignedCompliance(item))
    return lst

def parse_structure_RecordType_dashboard_DelayedCompliance(data):
    from protocol import dashboard
    return dashboard.DelayedCompliance.parse_structure(data)

def parse_structure_RecordType_core_Geography(data):
    from protocol import core
    return core.Geography.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_FormName(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_FormName(item))
    return lst

def parse_structure_RecordType_dashboard_DomainWise(data):
    from protocol import dashboard
    return dashboard.DomainWise.parse_structure(data)

def parse_structure_VariantType_clientuser_Request(data):
    from protocol import clientuser
    return clientuser.Request.parse_structure(data)

def parse_structure_RecordType_core_Industry(data):
    from protocol import core
    return core.Industry.parse_structure(data)

def parse_structure_RecordType_core_AssignedStatutory(data):
    from protocol import core
    return core.AssignedStatutory.parse_structure(data)

def parse_structure_RecordType_core_StatutoryNature(data):
    from protocol import core
    return core.StatutoryNature.parse_structure(data)

def parse_structure_VariantType_technoreports_Request(data):
    from protocol import technoreports
    return technoreports.Request.parse_structure(data)

def parse_structure_RecordType_core_Division(data):
    from protocol import core
    return core.Division.parse_structure(data)

def parse_structure_RecordType_core_Country(data):
    from protocol import core
    return core.Country.parse_structure(data)

def parse_structure_MapType_SignedIntegerType_8_RecordType_core_Menu(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_RecordType_core_Menu(value)
        d[key] = value
    return d

def parse_structure_RecordType_core_Statutory(data):
    from protocol import core
    return core.Statutory.parse_structure(data)

def parse_structure_RecordType_core_Unit(data):
    from protocol import core
    return core.Unit.parse_structure(data)

def parse_structure_RecordType_core_UpcomingCompliance(data):
    from protocol import core
    return core.UpcomingCompliance.parse_structure(data)

def parse_structure_VectorType_RecordType_core_ComplianceFrequency(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ComplianceFrequency(item))
    return lst

def parse_structure_VectorType_RecordType_core_ComplianceRepeatType(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ComplianceRepeatType(item))
    return lst

def parse_structure_RecordType_core_NumberOfCompliances(data):
    from protocol import core
    return core.NumberOfCompliances.parse_structure(data)

def parse_structure_VectorType_RecordType_core_NumberOfCompliances(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_core_NumberOfCompliances(item))
    return lst

def parse_structure_VectorType_RecordType_dashboard_ChartDataMap(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_ChartDataMap(item))
    return lst

def parse_structure_VectorType_RecordType_core_ComplianceDurationType(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ComplianceDurationType(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_ComplianceForUnit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ComplianceForUnit(item))
    return lst

def parse_structure_RecordType_clientreport_UnitCompliance(data):
    from protocol import clientreport
    return clientreport.UnitCompliance.parse_structure(data)

def parse_structure_RecordType_core_ComplianceShortDescription(data):
    from protocol import core
    return core.ComplianceShortDescription.parse_structure(data)

def parse_structure_RecordType_core_ComplianceApplicability(data):
    from protocol import core
    return core.ComplianceApplicability.parse_structure(data)

def parse_structure_VectorType_RecordType_core_ComplianceApplicability(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ComplianceApplicability(item))
    return lst

def parse_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability(data):
    if data is None: return None
    return parse_structure_VectorType_RecordType_core_ComplianceApplicability(data)

def parse_structure_maptype_signedIntegerType_8_VectorType_RecordType_core_ComplianceApplicability(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items() :
        key  = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_VectorType_RecordType_core_ComplianceApplicability(value)
        dict[key] = value
    return dict

def parse_structure_VectorType_RecordType_core_ComplianceShortDescription(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ComplianceShortDescription(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_UnitCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_UnitCompliance(item))
    return lst

def parse_structure_RecordType_core_ComplianceRepeatType(data):
    from protocol import core
    return core.ComplianceRepeatType.parse_structure(data)

def parse_structure_RecordType_core_ComplianceFrequency(data):
    from protocol import core
    return core.ComplianceFrequency.parse_structure(data)

def parse_structure_VectorType_RecordType_technomasters_PROFILES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technomasters_PROFILES(item))
    return lst

def parse_structure_RecordType_dashboard_AssigneeWiseDetails(data):
    from protocol import dashboard
    return dashboard.AssigneeWiseDetails.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_APPROVALCOMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_APPROVALCOMPLIANCE(item))
    return lst

def parse_structure_RecordType_core_ComplianceDurationType(data):
    from protocol import core
    return core.ComplianceDurationType.parse_structure(data)

def parse_structure_RecordType_clientreport_UserName(data):
    from protocol import clientreport
    return clientreport.UserName.parse_structure(data)

def parse_structure_RecordType_clienttransactions_APPROVALCOMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.APPROVALCOMPLIANCE.parse_structure(data)

def parse_structure_RecordType_core_Compliance(data):
    from protocol import core
    return core.Compliance.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(item))
    return lst

def parse_structure_RecordType_core_StatutoryDate(data):
    from protocol import core
    return core.StatutoryDate.parse_structure(data)

def parse_structure_RecordType_clientreport_Activities(data):
    from protocol import clientreport
    return clientreport.Activities.parse_structure(data)

def parse_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(data):
    from protocol import clienttransactions
    return clienttransactions.ASSIGN_COMPLIANCE_USER.parse_structure(data)

def parse_structure_CustomIntegerType_1_31(data):
    return parse_number(data, 1, 31)

def parse_structure_OptionalType_CustomIntegerType_1_31(data):
    if data is None: return None
    return parse_structure_CustomIntegerType_1_31(data)

def parse_structure_RecordType_clientreport_ActivityCompliance(data):
    from protocol import clientreport
    return clientreport.ActivityCompliance.parse_structure(data)

def parse_structure_RecordType_core_Form(data):
    from protocol import core
    return core.Form.parse_structure(data)

def parse_structure_RecordType_core_Level(data):
    from protocol import core
    return core.Level.parse_structure(data)

def parse_structure_RecordType_knowledgemaster_Level(data):
    from protocol import knowledgemaster
    return knowledgemaster.Level.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_ActivityCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ActivityCompliance(item))
    return lst

def parse_structure_OptionalType_CustomTextType_100(data):
    if data is None: return data
    return parse_structure_CustomTextType_100(data)

def parse_structure_OptionalType_CustomTextType_500(data):
    if data is None: return data
    return parse_structure_CustomTextType_500(data)

def parse_structure_VectorType_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(item))
    return lst

def parse_structure_VectorType_RecordType_dashboard_CompliedMap(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_CompliedMap(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_Activities(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_Activities(item))
    return lst

def parse_structure_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(data):
    from protocol import clienttransactions
    return clienttransactions.UNIT_WISE_COMPLIANCE.parse_structure(data)

def parse_structure_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(data):
    from protocol import clienttransactions
    return clienttransactions.APPORVALCOMPLIANCELIST.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(item))
    return lst

def parse_structure_RecordType_clientreport_User(data):
    from protocol import clientreport
    return clientreport.User.parse_structure(data)

def parse_structure_RecordType_technotransactions_UNIT(data):
    from protocol import technotransactions
    return technotransactions.UNIT.parse_structure(data)

def parse_structure_RecordType_clientreport_ComplianceName(data):
    from protocol import clientreport
    return clientreport.ComplianceName.parse_structure(data)

def parse_structure_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.STATUTORYWISECOMPLIANCE.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        d = parse_structure_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(item)
        lst.append(d)
    return lst

def parse_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.iteritems() :
        key = parse_structure_CustomTextType_100(key)
        value = parse_structure_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(value)
        dict[key] = value
    return dict

def parse_structure_MapType_SignedIntegerType_8_RecordType_core_StatutoryMapping(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_UnsignedIntegerType_32(key)
        value = parse_structure_RecordType_core_StatutoryMapping(value)
        d[key] = value
    return d

def parse_structure_RecordType_clientreport_ComplianceUnit(data):
    from protocol import clientreport
    return clientreport.ComplianceUnit.parse_structure(data)

def parse_structure_RecordType_core_FormCategory(data):
    from protocol import core
    return core.FormCategory.parse_structure(data)

def parse_structure_RecordType_clienttransactions_USER_WISE_UNITS(data):
    from protocol import clienttransactions
    return clienttransactions.USER_WISE_UNITS.parse_structure(data)

def parse_structure_RecordType_clientreport_StatutoryReassignCompliance(data):
    from protocol import clientreport
    return clientreport.StatutoryReassignCompliance.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_StatutoryReassignCompliance(item))
    return lst

def parse_structure_VectorType_RecordType_clienttransactions_USER_WISE_UNITS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_USER_WISE_UNITS(item))
    return lst

def parse_structure_VariantType_dashboard_Request(data):
    from protocol import dashboard
    return dashboard.Request.parse_structure(data)

def parse_structure_RecordType_clienttransactions_USER_WISE_COMPLIANCE(data):
    from protocol import clienttransactions
    return clienttransactions.USER_WISE_COMPLIANCE.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_Level1Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_Level1Compliance(item))
    return lst

def parse_structure_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(data):
    from protocol import clienttransactions
    return clienttransactions.STATUTORY_WISE_COMPLIANCES.parse_structure(data)

def parse_structure_RecordType_dashboard_RessignedCompliance(data):
    from protocol import dashboard
    return dashboard.RessignedCompliance.parse_structure(data)

def parse_structure_RecordType_clientreport_ComplianceDetails(data):
    from protocol import clientreport
    return clientreport.ComplianceDetails.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_ComplianceDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ComplianceDetails(item))
    return lst

def parse_structure_RecordType_clientreport_ActivityLog(data):
    from protocol import clientreport
    return clientreport.ActivityLog.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_ActivityLog(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ActivityLog(item))
    return lst

def parse_structure_RecordType_clientreport_Level1Statutory(data):
    from protocol import clientreport
    return clientreport.Level1Statutory.parse_structure(data)

def parse_structure_RecordType_admin_UserGroup(data):
    from protocol import admin
    return admin.UserGroup.parse_structure(data)

def parse_structure_VectorType_RecordType_admin_UserGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_admin_UserGroup(item))
    return lst

def parse_structure_RecordType_knowledgetransaction_ApproveMapping(data):
    from protocol import knowledgetransaction
    return knowledgetransaction.ApproveMapping.parse_structure(data)

def parse_structure_VectorType_RecordType_knowledgetransaction_ApproveMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_knowledgetransaction_ApproveMapping(item))
    return lst

def parse_structure_MapType_UnsignedIntegerType_32_Bool(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items():
        key = parse_structure_UnsignedIntegerType_32(int(key))
        value = parse_structure_Bool(value)
        d[key] = value
    return d

def parse_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items():
        key = parse_structure_UnsignedIntegerType_32(int(key))
        value = parse_structure_UnsignedIntegerType_32(value)
        d[key] = value
    return d

def parse_structure_RecordType_technotransactions_AssignedStatutoryCompliance(data):
    from protocol import technotransactions
    return technotransactions.AssignedStatutoryCompliance.parse_structure(data)

def parse_structure_VectorType_RecordType_technotransactions_AssignedStatutoryCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technotransactions_AssignedStatutoryCompliance(item))
    return lst

# clienttransactions ComplianceApplicability
def parse_structure_RecordType_clienttransactions_ComplianceApplicability(data):
    from protocol import clienttransactions
    return clienttransactions.ComplianceApplicability.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_ComplianceApplicability(item))
    return lst

# UnitStatutoryCompliances
def parse_structure_RecordType_clienttransactions_UnitStatutoryCompliances(data):
    from protocol import clienttransactions
    return clienttransactions.UnitStatutoryCompliances.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_UnitStatutoryCompliances(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_clienttransactions_UnitStatutoryCompliances(item))
    return lst

# clienttransaction UpdateStatutoryCompliance
def parse_structure_RecordType_clienttransactions_UpdateStatutoryCompliance(data):
    from protocol import clienttransactions
    return clienttransactions.UpdateStatutoryCompliance.parse_structure(data)


def parse_structure_VectorType_RecordType_clienttransactions_UpdateStatutoryCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_clienttransactions_UpdateStatutoryCompliance(item))
    return lst

#clienttransaction getcompliancforunit
def parse_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    from protocol import clienttransactions
    return clienttransactions.UNIT_WISE_STATUTORIES.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(item))
    return lst

def parse_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.iteritems():
        key = parse_structure_CustomTextType_100(key)
        value = parse_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(value)
        d[key] = value
    return d

#
#   Get Clients
#

def parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_GeographyWithMapping(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_SignedIntegerType_8(key)
        value = parse_structure_VectorType_RecordType_core_GeographyWithMapping(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_core_GeographyWithMapping(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_GeographyWithMapping(item))
    return lst

def parse_structure_RecordType_core_GeographyWithMapping(data):
    from protocol import core
    return core.GeographyWithMapping.parse_structure(data)

# Client Business Group

def parse_structure_RecordType_core_ClientBusinessGroup(data):
    from protocol import core
    return core.ClientBusinessGroup.parse_structure(data)

def parse_structure_VectorType_RecordType_core_ClientBusinessGroup(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ClientBusinessGroup(item))
    return lst

# client Legal Entity
def parse_structure_RecordType_core_ClientLegalEntity(data):
    from protocol import core
    return core.ClientLegalEntity.parse_structure(data)

def parse_structure_VectorType_RecordType_core_ClientLegalEntity(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ClientLegalEntity(item))
    return lst

#client Division
def parse_structure_RecordType_core_ClientDivision(data):
    from protocol import core
    return core.ClientDivision.parse_structure(data)

def parse_structure_VectorType_RecordType_core_ClientDivision(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ClientDivision(item))
    return lst

# Client Report Filter
def parse_structure_VectorType_RecordType_core_ClientUnit(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_Unit(item))
    return lst

# Statutory Notifications (Techno)

def parse_structure_VectorType_RecordType_technoreports_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technoreports_NOTIFICATIONS(item))
    return lst

# Trend Chart
def parse_structure_OptionalType_VectorType_UnsignedIntegerType_32(data):
    if data is None: return data
    return parse_structure_VectorType_UnsignedIntegerType_32(data)

def parse_structure_VectorType_RecordType_dashboard_TrendCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_TrendCompliance(item))
    return lst

def parse_structure_RecordType_dashboard_TrendCompliance(data):
    from protocol import dashboard
    return dashboard.TrendCompliance.parse_structure(data)

def parse_structure_MapType_CustomTextType_100_VectorType_RecordType_dashboard_TrendCompliance(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_CustomTextType_100(key)
        value = parse_structure_VectorType_RecordType_dashboard_TrendCompliance(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_dashboard_TrendDrillDownData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_TrendDrillDownData(item))
    return lst

def parse_structure_RecordType_dashboard_TrendDrillDownData(data):
    from protocol import dashboard
    return dashboard.TrendDrillDownData.parse_structure(data)

def parse_structure_RecordType_technoreports_NOTIFICATIONS(data):
    from protocol import technoreports
    return technoreports.NOTIFICATIONS.parse_structure(data)

# Complaince details report
def parse_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ComplianceDetailsUnitWise(item))
    return lst

def parse_structure_RecordType_clientreport_ComplianceDetailsUnitWise(data):
    from protocol import clientreport
    return clientreport.ComplianceDetailsUnitWise.parse_structure(data)



# Client Compliance Filter
def parse_structure_VectorType_RecordType_core_ComplianceFilter(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_core_ComplianceFilter(item))
    return lst

# not complied enum type

def parse_structure_EnumType_core_NOT_COMPLIED_TYPE(data):
    from protocol import core
    return core.NOT_COMPLIED_TYPE.parse_structure(data)

def parse_structure_OptionalType_CustomTextType_250(data):
    if data is None: return data
    return parse_custom_string(data, 250)

def parse_structure_VectorType_CustomTextType_100(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_CustomTextType_100(item))
    return lst

# Risk Report

def parse_structure_VectorType_RecordType_clientreport_RiskData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_RiskData(item))
    return lst

def parse_structure_RecordType_clientreport_RiskData(data):
    from protocol import clientreport
    return clientreport.RiskData.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_Level1Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_Level1Compliance(item))
    return lst

def parse_structure_RecordType_clientreport_Level1Compliance(data):
    from protocol import clientreport
    return clientreport.Level1Compliance.parse_structure(data)

# Client Notifications

def parse_structure_VectorType_RecordType_dashboard_Notification(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_Notification(item))
    return lst

def parse_structure_RecordType_dashboard_Notification(data):
    from protocol import dashboard
    return dashboard.Notification.parse_structure(data)


def parse_structure_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(data):
    from protocol import clientreport
    return clientreport.STATUTORY_WISE_NOTIFICATIONS.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(item))
    return lst

# ReassignUnitCompliance

def parse_structure_RecordType_clientreport_ReassignUnitCompliance(data):
    from protocol import clientreport
    return clientreport.ReassignUnitCompliance.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreport_ReassignUnitCompliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ReassignUnitCompliance(item))
    return lst

def parse_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(item))
    return lst

def parse_structure_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(data):
    from protocol import clienttransactions
    return clienttransactions.UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS.parse_structure(data)

def parse_structure_OptionalType_EnumType_core_COMPLIANCE_FREQUENCY(data):
    if data is None: return None
    return parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(data)

# Compliance Activity Report

def parse_structure_VectorType_RecordType_clientreport_ActivityData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_ActivityData(item))
    return lst

def parse_structure_RecordType_clientreport_ActivityData(data):
    from protocol import clientreport
    return clientreport.ActivityData.parse_structure(data)

def parse_structure_OptionalType_VectorType_RecordType_dashboard_RessignedCompliance(data):
    if data is None: return None
    return parse_structure_VectorType_RecordType_dashboard_RessignedCompliance(data)

def parse_structure_VectorType_RecordType_client_report_UnitDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_client_report_UnitDetails(item))
    return lst

def parse_structure_RecordType_client_report_UnitDetails(data):
    from protocol import clientreport
    return clientreport.UnitDetails.parse_structure(data)

def parse_structure_RecordType_core_Compliance_Download(data):
    from protocol import core
    return core.Compliance_Download.parse_structure(data)

def parse_structure_VectorType_RecordType_core_Compliance_Download(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_core_Compliance_Download(item))
    return lst

def parse_structure_VectorType_RecordType_core_COMPLIANCE_APPROVAL_STATUS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_COMPLIANCE_APPROVAL_STATUS(item))
    return lst

def parse_structure_VectorType_CustomTextType_500(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_CustomTextType_500(item))
    return lst

def parse_structure_OptionalType_VectorType_CustomTextType_500(data):
    if data is None: return data
    return parse_structure_VectorType_CustomTextType_500(data)

def parse_structure_RecordType_core_StatutoryApprovalStatus(data):
    from protocol import core
    return core.StatutoryApprovalStatus.parse_structure(data)

def parse_structure_VectorType_RecordType_core_StatutoryApprovalStatus(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_StatutoryApprovalStatus(item))
    return lst

def parse_structure_VectorType_RecordType_clienttransactions_PastRecordUnits(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_PastRecordUnits(item))
    return lst

def parse_structure_RecordType_clienttransactions_PastRecordUnits(data):
    from protocol import clienttransactions
    return clienttransactions.PastRecordUnits.parse_structure(data)

def parse_structure_MapType_CustomTextType_50_VectorType_CustomTextType_500(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_CustomTextType_50(key)
        value = parse_structure_VectorType_CustomTextType_500(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_technomasters_UnitDetails(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_technomasters_UnitDetails(item))
    return lst

def parse_structure_RecordType_technomasters_UnitDetails(data):
    from protocol import technomasters
    return technomasters.UnitDetails.parse_structure(data)

def parse_structure_MapType_CustomTextType_500_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_CustomTextType_500(key)
        value = parse_structure_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(value)
        d[key] = value
    return d

def parse_structure_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_AssigneeWiseLevel1Compliance(item))
    return lst

def parse_structure_RecordType_dashboard_AssigneeWiseLevel1Compliance(data):
    from protocol import dashboard
    return dashboard.AssigneeWiseLevel1Compliance.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_YearWise(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_YearWise(item))
    return lst

def parse_structure_RecordType_dashboard_YearWise(data):
    from protocol import dashboard
    return dashboard.YearWise.parse_structure(data)

def parse_structure_RecordType_dashboard_AssigneeWiseCompliance(data):
    from protocol import dashboard
    return dashboard.AssigneeWiseCompliance.parse_inner_structure(data)

def parse_structure_VectorType_RecordType_core_ClientInchargePersons(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ClientInchargePersons(item))
    return lst

def parse_structure_RecordType_core_ClientInchargePersons(data):
    from protocol import core
    return core.ClientInchargePersons.parse_structure(data)

def parse_structure_RecordType_dashboard_DomainWiseYearConfiguration(data):
    from protocol import dashboard
    return dashboard.DomainWiseYearConfiguration.parse_structure(data)

def parse_structure_VectorType_RecordType_dashboard_DomainWiseYearConfiguration(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_dashboard_DomainWiseYearConfiguration(item))
    return lst

def parse_structure_MapType_CustomTextType_100_VectorType_RecordType_dashboard_DomainWiseYearConfiguration(data):
    data = parse_dictionary(data)
    d = {}
    for key, value in data.items():
        key = parse_structure_CustomTextType_100(key)
        value = parse_structure_VectorType_RecordType_dashboard_DomainWiseYearConfiguration(value)
        d[key] = value
    return d

def parse_structure_MapType_CustomTextType_250_VectorType_RecordType_clientuser_ComplianceOnOccurrence(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_MapType_CustomTextType_250(key)
        value = parse_structure_VectorType_RecordType_clientuser_ComplianceOnOccurrence(value)
        d[key] = value
    return d

def parse_structure_OptionalType_RecordType_core_FileList(data):
    if data is None: return data
    return parse_structure_RecordType_core_FileList(data)

def parse_structure_OptionalType_RecordType_core_ClientBusinessGroup(data):
    if data is None: return data
    return parse_structure_RecordType_core_ClientBusinessGroup(data)

def parse_structure_VectorType_CustomTextType_250(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_Text(item))
    return lst

def parse_structure_OptionalType_VectorType_CustomTextType_250(data):
    if data is None: return data
    return parse_structure_VectorType_CustomTextType_250(data)

def parse_structure_RecordType_clienttransactions_NewUnitSettings(data):
    from protocol import clienttransactions
    return clienttransactions.NewUnitSettings.parse_structure(data)

def parse_structure_VectorType_RecordType_clienttransactions_NewUnitSettings(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clienttransactions_NewUnitSettings(item))
    return lst

def parse_structure_OptionalType_VectorType_RecordType_clienttransactions_NewUnitSettings(data):
    if data is None: return data
    return parse_structure_VectorType_RecordType_clienttransactions_NewUnitSettings(data)

def parse_structure_RecordType_mobile_GetUSersList(data):
    from protocol import mobile
    return mobile.GetUsersList.parse_structure(data)

def parse_structure_VectorType_RecordType_mobile_GetUsersList(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_mobile_GetUSersList(item))
    return lst

def parse_structure_RecordType_mobile_ComplianceApplicability(data):
    from protocol import mobile
    return mobile.ComplianceApplicability.parse_structure(data)

def parse_structure_VectorType_RecordType_mobile_ComplianceApplicability(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_mobile_ComplianceApplicability(item))
    return lst

def parse_structure_RecordType_mobile_DomainWiseCount(data):
    from protocol import mobile
    return mobile.DomainWiseCount.parse_structure(data)

def parse_structure_VectorType_RecordType_mobile_DomainWiseCount(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_mobile_DomainWiseCount(item))
    return lst

def parse_structure_RecordType_mobile_UnitWiseCount(data):
    from protocol import mobile
    return mobile.UnitWiseCount.parse_structure(data)

def parse_structure_VectorType_RecordType_mobile_UnitWiseCount(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_mobile_UnitWiseCount(item))
    return lst

def parse_structure_VariantType_mobile_Request(data):
    from protocol import mobile
    return mobile.Request.parse_structure(data)

def parse_structure_RecordType_mobile_ComplianceHistory(data):
    from protocol import mobile
    return mobile.ComplianceHistory.parse_structure(data)

def parse_structure_VectorType_RecordType_mobile_ComplianceHistory(data):
    data = parse_list(data, 0)
    lst = []
    for item in data :
        lst.append(parse_structure_RecordType_mobile_ComplianceHistory(item))
    return lst

def parse_structure_VectorType_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(item))
    return lst

def parse_structure_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(data):
    from protocol import clientreport
    return clientreport.GetComplianceTaskApplicabilityStatusReportData.parse_structure(data)

def parse_structure_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS(data):
    from protocol import clientreport
    return clientreport.LEVEL_1_STATUTORY_NOTIFICATIONS.parse_structure(data)

def parse_structure_VectorType_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS(item))
    return lst

def parse_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS(data):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = parse_structure_CustomTextType_500(key)
        value = parse_structure_VectorType_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS(value)
        dict[key] = value
    return dict


def parse_structure_VectorType_RecordType_core_ValidityDates(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_core_ValidityDates(item))
    return lst


def parse_structure_RecordType_core_ValidityDates(data):
    from protocol import core
    return core.ValidityDates.parse_structure(data)


def parse_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_UnsignedIntegerType_32(key)
        value = parse_structure_VectorType_UnsignedIntegerType_32(value)
        d[key] = value
    return d


def return_import(module, class_name):
    mod = __import__('protocol.'+module, fromlist=[class_name])
    klass = getattr(mod, class_name)
    return klass


def parse_structure_RecordType(module, class_name, data):
    klass = return_import(module, class_name)
    return klass.parse_structure(data)


def parse_structure_VectorType_RecordType_core_ClientGroup(data):
    return parse_structure_VectorType(
        data, parse_structure_RecordType_core_ClientGroup)


def parse_structure_RecordType_core_ClientGroup(data):
    return parse_structure_RecordType(
        "core", "ClientGroup", data
    )


def parse_structure_VectorType_RecordType_core_LegalEntityDetails(data):
    return parse_structure_VectorType(
        data, parse_structure_RecordType_core_LegalEntityDetails)


def parse_structure_RecordType_core_LegalEntityDetails(data):
    return parse_structure_RecordType(
        "core", "LegalEntityDetails", data
    )


def parse_structure_VectorType_RecordType_core_EntityDomainDetails(data):
    return parse_structure_VectorType(
        data, parse_structure_RecordType_core_EntityDomainDetails)


def parse_structure_RecordType_core_EntityDomainDetails(data):
    return parse_structure_RecordType(
        "core", "EntityDomainDetails", data
    )


def parse_structure_VectorType_RecordType_core_Industries(data):
    return parse_structure_VectorType(
        data, parse_structure_RecordType_core_Industries)


def parse_structure_RecordType_core_Industries(data):
    return parse_structure_RecordType(
        "core", "Industries", data
    )


def parse_structure_MapType_CustomTextType_50_VectorType_UnsignedIntegerType_32(data):
    return parse_structure_MapType(
        data, parse_structure_CustomTextType_50,
        parse_structure_UnsignedIntegerType_32
    )

def parse_structure_VectorType_RecordType_core_AssignLegalEntity(data):
    return parse_structure_VectorType(
        data, parse_structure_RecordType_core_AssignLegalEntity)


def parse_structure_RecordType_core_AssignLegalEntity(data):
    return parse_structure_RecordType(
        "core", "AssignLegalEntity", data
    )