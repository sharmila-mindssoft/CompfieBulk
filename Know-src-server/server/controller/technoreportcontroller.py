from server.jsontocsvconverter import ConvertJsonToCSV
from protocol import technoreports, knowledgereport, core
from server.constants import RECORD_DISPLAY_COUNT
from server.database.admin import (
    get_countries_for_user, get_domains_for_user,
    get_countries_for_user_filter, get_level_1_statutories
)
from server.database.general import (
    get_compliance_frequency
)
from server.database.technomaster import (
    get_business_groups_for_user,
    get_legal_entities_for_user,
    get_active_industries,
    get_client_groups_for_user
)
from server.database.knowledgemaster import (
    get_country_wise_level_1_statutoy,
    get_industries, get_statutory_nature,
    get_geographies,
)

from server.database.technoreport import (
    get_statutory_notifications_report_data,
    get_statutory_notifications_report_count,
    get_client_details_report,
    get_compliance_list_report_techno,
    get_client_agreement_report,
    get_client_agreement_report_count,
    get_domainwise_agreement_report,
    get_domainwise_agreement_report_count,
    get_organizationwise_unit_count,
    get_user_category_details,
    get_countries_for_usermapping_report_filter,
    get_group_details_for_usermapping_report_filter,
    get_business_groups_for_usermapping_report,
    get_legal_entities_for_usermapping_report,
    get_unit_details_for_usermapping_report,
    get_usermapping_report_dataset,
    get_group_companies_for_statutorysetting_report,
    get_business_groups_for_statutorysetting_report,
    get_units_for_statutorysetting_report,
    get_compliance_statutoy_for_statutorysetting_report,
    get_assigned_statutories_report_data,
    get_units_for_clientdetails_report,
    get_GroupAdminReportData,
    get_AssignedUserClientGroupsDetails,
    get_ReassignUserReportData,
    get_ReassignUserDomainReportData,
    get_assigned_statutories_list,
    get_ComplianceStatutoriesList,
    get_domains_for_unit
)

__all__ = [
    "process_techno_report_request"
]


def process_techno_report_request(request, db, user_id):

    request_frame = request.request

    if type(request_frame) is technoreports.GetAssignedStatutoryReportFilters:
        result = process_get_assigned_statutory_report_filters(db, user_id)

    elif type(request_frame) is technoreports.GetAssignedStatutoryReport:
        result = process_get_assigned_statutory_report_data(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.GetClientDetailsReportFilters:
        result = process_get_client_details_report_filters(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.GetClientDetailsReportData:
        result = process_get_client_details_report_data(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.ExportClientDetailsReportData:
        result = process_export_client_details_report_data(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.GetStatutoryNotificationsFilters:
        result = process_get_statutory_notifications_filters(
            db, request_frame, user_id
        )

    elif (
        type(
            request_frame
        ) is technoreports.GetStatutoryNotificationsReportData
    ):
        result = process_get_statutory_notifications_report_data(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.GetComplianceTaskFilter:
        result = process_get_compliance_task_filter(db, request_frame, user_id)

    # elif type(request_frame) is technoreports.GetComplianceTaskReport:
    #     result = process_get_compliance_task_report(db, request_frame, user_id)

    elif type(request_frame) is technoreports.GetUserMappingReportFilters:
        result = process_get_user_mapping_reports_filter(db, request_frame, user_id)

    elif type(request_frame) is technoreports.GetUserMappingDetailsReportData:
        result = process_get_user_mapping_details_reports_data(db, request_frame, user_id)

    elif type(request_frame) is technoreports.GetClientAgreementReportFilters:
        result = process_get_client_agreement_report_filters(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.GetClientAgreementReportData:
        result = process_get_client_agreement_report_data(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.GetDomainwiseAgreementReportData:
        result = process_get_domainwise_agreement_report_data(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.GetOrganizationWiseUnitCount:
        result = process_get_organizationwise_unit_count(
            db, request_frame, user_id
        )

    elif type(request_frame) is technoreports.GetGroupAdminReportData:
        result = process_get_GroupAdminReportData(db, user_id)

    elif type(request_frame) is technoreports.ExportGroupAdminReportData:
        result = process_export_GroupAdminReportData(db, request_frame, user_id)

    elif type(request_frame) is technoreports.GetAssignedUserClientGroups:
        result = process_get_AssignedUserClientGroups(db, user_id)

    elif type(request_frame) is technoreports.GetReassignUserReportData:
        result = process_get_ReassignUserReportData(db, request_frame, user_id)

    elif type(request_frame) is technoreports.ExportReassignUserReportData:
        result = process_export_ReassignUserReportData(db, request_frame, user_id)

    elif type(request_frame) is technoreports.GetReassignUserDomainReportData:
        result = process_get_ReassignUserDomainReportData(db, request_frame, user_id)

    elif type(request_frame) is technoreports.GetAssignedStatutoriesList:
        result = process_get_AssignedStatutoriesList(db, request_frame, user_id)

    elif type(request_frame) is technoreports.GetComplianceStatutoriesList:
        result = process_get_ComplianceStatutoriesList(db, request_frame, user_id)

    return result

######################################################################################
# To process statutory setting report filter data for assigned statutories
# Parameter(s) : Object of the database, user id
# Return Type : Return lists of data
######################################################################################
def process_get_assigned_statutory_report_filters(db, user_id):
    countries = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    group_companies = get_group_companies_for_statutorysetting_report(db, user_id)
    business_groups = get_business_groups_for_statutorysetting_report(db, user_id)
    unit_list = get_units_for_statutorysetting_report(db, user_id)
    compliance_statutories = get_compliance_statutoy_for_statutorysetting_report(db, user_id)
    return technoreports.GetAssignedStatutoryReportFiltersSuccess(
        countries, domains, group_companies,
        business_groups, unit_list, compliance_statutories
    )

######################################################################################
# To get the assigned statutory report data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of assigned statutories
######################################################################################
def process_get_assigned_statutory_report_data(db, request_frame, user_id):
    if request_frame.csv:
        converter = ConvertJsonToCSV(
            db, request_frame, user_id, "StatutorySettingsReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return technoreports.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result = get_assigned_statutories_report_data(db, request_frame, user_id)
        unit_groups = result[0]
        act_groups = result[1]
        compliance_statutories_list = result[2]
        return technoreports.GetAssignedStatutoryReportSuccess(unit_groups, act_groups, compliance_statutories_list, total_count=result[3])

######################################################################################
# To get the statutory notifications list filters data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of countries, domains and statutories
######################################################################################
def process_get_statutory_notifications_filters(db, request_frame, user_id):
    countries = get_countries_for_user_filter(db, user_id)
    domains = get_domains_for_user(db, user_id)
    level_one_statutories = get_level_1_statutories(db)

    return technoreports.GetStatutoryNotificationsFiltersSuccess(
        countries=countries,
        domains=domains,
        level_one_statutories=level_one_statutories
    )
######################################################################################
# To get the statutory notofication list report data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of statutory notofications
######################################################################################
def process_get_statutory_notifications_report_data(db, request, user_id):
    result = get_statutory_notifications_report_data(db, request)
    total_count = get_statutory_notifications_report_count(
            db, request
        )
    return technoreports.GetStatutoryNotificationsReportDataSuccess(
        statutory_notifictions_list=result, total_count=total_count
    )
##################################################################################################################
# To get the client details report filters data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of countries, domains,client groups, units, business groups,industries
##################################################################################################################
def process_get_client_details_report_filters(db, request_frame, session_user):
    countries = get_countries_for_user(db, session_user)
    domains_organization_list = get_domains_for_unit(db, session_user)
    group_companies = get_group_companies_for_statutorysetting_report(db, session_user)
    business_groups = get_business_groups_for_statutorysetting_report(db, session_user)
    units_report = get_units_for_clientdetails_report(db, session_user)
    industries = get_active_industries(db)
    return technoreports.GetClientDetailsReportFiltersSuccess(
        countries=countries,
        domains_organization_list=domains_organization_list,
        statutory_groups=group_companies,
        statutory_business_groups=business_groups,
        units_report=units_report,
        industry_name_id=industries
    )

##################################################################################################################
# To get the client details report data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of units matched under the parameters
##################################################################################################################
def process_get_client_details_report_data(db, request, session_user):
    units_list = get_client_details_report(
        db, request, session_user
    )

    return technoreports.GetClientDetailsReportDataSuccess(
        units_list=units_list
    )

##################################################################################################################
# To get the client details report data and export to file
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of units matched under the parameters
##################################################################################################################
def process_export_client_details_report_data(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ClientUnitDetailsReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return technoreports.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )

def process_get_compliance_task_filter(db, request, session_user):
    countries = get_countries_for_user(db, session_user)
    domains = get_domains_for_user(db, session_user)
    industries = get_industries(db)
    statutory_nature = get_statutory_nature(db)
    geographies = get_geographies(db)
    level_1_statutories = get_country_wise_level_1_statutoy(db)
    compliance_frequency = get_compliance_frequency(db)
    return knowledgereport.GetStatutoryMappingReportFiltersSuccess(
        countries, domains, industries, statutory_nature,
        geographies, level_1_statutories, compliance_frequency
    )


def process_get_compliance_task_report(db, request_frame, user_id):
    country_id = request_frame.country_id
    domain_id = request_frame.domain_id
    industry_id = request_frame.industry_id
    nature_id = request_frame.statutory_nature_id
    geography_id = request_frame.geography_id
    level_1_id = request_frame.level_1_statutory_id
    frequency_id = request_frame.frequency_id
    from_count = request_frame.record_count
    to_count = RECORD_DISPLAY_COUNT
    report_data, total_count = get_compliance_list_report_techno(
        db, country_id, domain_id, industry_id,
        nature_id, geography_id, level_1_id, frequency_id, user_id,
        from_count, to_count
    )

    return knowledgereport.GetStatutoryMappingReportDataSuccess(
        country_id, domain_id, report_data, total_count
    )
##################################################################################################################
# To get the client agreement report filters data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of countries, domains,client groups, business groups,units legal entities
##################################################################################################################
def process_get_client_agreement_report_filters(db, request_frame, session_user):
    countries = get_countries_for_user_filter(db, session_user)
    domains = get_domains_for_user(db, session_user)
    groups = get_client_groups_for_user(db, session_user)
    business_groups = get_business_groups_for_user(db, session_user)
    unit_legal_entity = get_legal_entities_for_user(db, session_user)

    return technoreports.GetClientAgreementReportFiltersSuccess(
        countries=countries,
        domains=domains,
        groups=groups,
        business_groups=business_groups,
        unit_legal_entity=unit_legal_entity
    )
##################################################################################################################
# To get the client agreement report filters data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of client agreement report data
##################################################################################################################
def process_get_client_agreement_report_data(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ClientAgreementReport"
        )
        return technoreports.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        client_agreement_list = get_client_agreement_report(
            db, request.country_id, request.client_id, request.business_group_id, request.legal_entity_id,
            request.domain_id, request.contract_from, request.contract_to,
            request.from_count, request.page_count, session_user
        )
        total_count = get_client_agreement_report_count(
            db, request.country_id, request.client_id, request.business_group_id, request.legal_entity_id,
            request.domain_id, request.contract_from, request.contract_to, session_user
        )
        return technoreports.GetClientAgreementReportDataSuccess(
            client_agreement_list=client_agreement_list, total_count=total_count
        )

##################################################################################################################
# To get the domain wise agreement report filters data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of domain wise agreement report data
##################################################################################################################
def process_get_domainwise_agreement_report_data(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "DomainwiseAgreementReport"
        )
        return technoreports.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        client_agreement_list = get_domainwise_agreement_report(
            db, request.country_id, request.client_id, request.business_group_id, request.legal_entity_id,
            request.domain_id, request.contract_from, request.contract_to,
            request.from_count, request.page_count, session_user
        )
        total_count = get_domainwise_agreement_report_count(
            db, request.country_id, request.client_id, request.business_group_id, request.legal_entity_id,
            request.domain_id, request.contract_from, request.contract_to, session_user
        )
        return technoreports.GetDomainwiseAgreementReportDataSuccess(
            domainwise_agreement_list=client_agreement_list, total_count=total_count
        )

##################################################################################################################
# To get the organization units count under the legal entity id
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of units count
##################################################################################################################
def process_get_organizationwise_unit_count(db, request, session_user):
    unit_count_list = get_organizationwise_unit_count(
        db, request.legal_entity_id, request.domain_id
    )

    return technoreports.GetOrganizationWiseUnitCountSuccess(
        organizationwise_unit_count_list=unit_count_list
    )
##################################################################################################################
# To get the user mapping report filter data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of countries,client groups,business groups,legal entities and units list
##################################################################################################################
def process_get_user_mapping_reports_filter(db, request_frame, session_user):
    user_category_details = get_user_category_details(db, session_user)
    for row in user_category_details:
        countries = get_countries_for_usermapping_report_filter(db, int(row["user_category_id"]), int(session_user))
        usermapping_groupdetails = get_group_details_for_usermapping_report_filter(db, int(row["user_category_id"]), int(session_user))
        usermapping_business_groups = get_business_groups_for_usermapping_report(db)
        usermapping_legal_entities = get_legal_entities_for_usermapping_report(db)
        usermapping_unit = get_unit_details_for_usermapping_report(db, int(row["user_category_id"]), int(session_user))
        return technoreports.GetUserMappingReportFiltersSuccess(
            countries=countries,
            usermapping_groupdetails=usermapping_groupdetails,
            usermapping_business_groups=usermapping_business_groups,
            usermapping_legal_entities=usermapping_legal_entities,
            usermapping_unit=usermapping_unit
        )
##################################################################################################################
# To get the user mapping reports data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of mapped user list
##################################################################################################################
def process_get_user_mapping_details_reports_data(db, request_frame, session_user):
    if request_frame.csv:
        converter = ConvertJsonToCSV(
            db, request_frame, session_user, "UserMappingReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return technoreports.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        country_id = request_frame.country_id
        client_id = request_frame.client_id
        legal_entity_id = request_frame.legal_entity_id
        user_mapping_none_values = request_frame.u_m_none
        from_count = request_frame.from_count
        page_count = request_frame.page_count
        bgrp_id = division_id = catagory_id = unit_id = 0
        if user_mapping_none_values.find(",") > 0:
            bgrp_id = user_mapping_none_values.split(",")[0]
            division_id = user_mapping_none_values.split(",")[1]
            catagory_id = user_mapping_none_values.split(",")[2]
            unit_id = user_mapping_none_values.split(",")[3]
        usermapping_report_dataset = []
        usermapping_report_dataset = get_usermapping_report_dataset(
            db, int(session_user), client_id, legal_entity_id,
            country_id, int(bgrp_id), int(division_id), int(catagory_id),
            int(unit_id), from_count, page_count
        )

        techno_details = []
        unit_domains = []
        domains = []
        if(len(usermapping_report_dataset) > 0):

            for techno in usermapping_report_dataset[0]:

                techno_details.append(core.UserMappingReportTechno(
                    techno["unit_id"], techno["techno_manager"], techno["techno_user"],
                    unit_code_with_name=techno["unit_name"]
                ))

            for assign_domain in usermapping_report_dataset[1]:
                unit_domains.append(core.UserMappingReportDomain(
                    assign_domain["unit_id"], assign_domain["employee_name"], assign_domain["user_category_name"], assign_domain["domain_id"]
                ))
            for domain in usermapping_report_dataset[2]:
                domains.append(technoreports.UserMappingDomain(
                    domain["domain_id"], domain["domain_name"], bool(domain["is_active"])
                ))
            '''if(len(usermapping_report_dataset[0]) > 0):
                techno_details = usermapping_report_dataset[0]
            else:
                techno_details = None,

            if(len(usermapping_report_dataset[1]) > 0):
                unit_domains = usermapping_report_dataset[1]
            else:
                unit_domains = None,

            if(len(usermapping_report_dataset[2]) > 0):
                domains = usermapping_report_dataset[2]
            else:
                domains = None'''

            return technoreports.GetUserMappingReportDataSuccess(
                techno_details=techno_details,
                unit_domains=unit_domains,
                usermapping_domain=domains
            )

def process_export_user_mapping_details_reports_data(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "UserMappingReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return technoreports.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
##################################################################################################################
# To get the group admin registration email report data
# Parameter(s) : Object of the database, user id
# Return Type : Return list of group admin registered list
##################################################################################################################
def process_get_GroupAdminReportData(db, user_id):
    result = get_GroupAdminReportData(db, user_id)
    groupList = []
    countriesList = []
    group_admin_data = []
    print result[1]
    for groups in result[1]:
        groupList.append(technoreports.GroupAdminClientGroup(
                groups.get("client_id"), groups.get("group_name"), bool(groups.get("is_active"))
            ))

    for countries in result[2]:
        countriesList.append(technoreports.GroupAdminCountry(
                countries.get("client_id"), countries.get("country_id"), countries.get("country_name"),
                bool(countries.get("is_active"))
            ))

    for groupadmin in result[3]:
        group_admin_data.append(technoreports.GroupAdminClientGroupData(
                groupadmin.get("client_id"), groupadmin.get("legal_entity_id"),
                groupadmin.get("legal_entity_name"), groupadmin.get("unit_count"),
                groupadmin.get("country_id"), groupadmin.get("country_name"),
                groupadmin.get("unit_email_date"), groupadmin.get("statutory_email_date"),
                groupadmin.get("registration_email_date"), groupadmin.get("resend_email_date")
            ))
    return technoreports.GetGroupAdminReportDataSuccess(
        groupadmin_clients=groupList,
        group_admin_countries=countriesList,
        group_admin_list=group_admin_data
    )
##################################################################################################################
# To get the assigned client groups filter data and user categories
# Parameter(s) : Object of the database, user id
# Return Type : Return list of user details, client groups, legal entities, domains
##################################################################################################################
def process_get_AssignedUserClientGroups(db, user_id):
    result = get_AssignedUserClientGroupsDetails(db, user_id)
    user_category = []
    user_clients = []
    client_list = []
    domain_user_list = []
    for category in result[0]:
        user_category.append(core.UserCategory(
            int(category.get("user_category_id")), category.get("user_category_name")
        ))

    for cl_user in result[1]:
        user_id = int(cl_user[0])
        user_catg_id = int(cl_user[1])
        emp_code_name = cl_user[2]
        client_ids = cl_user[3]
        user_clients.append(technoreports.ReassignUserClients(
            user_id, user_catg_id, emp_code_name, client_ids
        ))

    for cl_list in result[2]:
        client_list.append(core.Client(
            int(cl_list.get("client_id")), cl_list.get("short_name"), bool(cl_list.get("is_active"))
        ))

    for d_list in result[3]:
        domain_user_list.append(technoreports.ReassignUserDomainList(
            int(d_list.get("user_id")), int(d_list.get("client_id")),
            d_list.get("legal_entity_id"), d_list.get("legal_entity_name"), d_list.get("business_group_id"),
            d_list.get("business_group_name"), int(d_list.get("domain_id")), d_list.get("domain_name")
        ))

    return technoreports.GetAssignedUserClientGroupsSuccess(
        user_categories=user_category,
        reassign_user_clients=user_clients,
        clients=client_list,
        reassign_domains=domain_user_list
    )
##################################################################################################################
# To get the Reassigned user report data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of reassigned user data under the parameters
##################################################################################################################
def process_get_ReassignUserReportData(db, request_frame, user_id):
    user_category_id = request_frame.user_category_id
    user_id = request_frame.user_id
    group_id = request_frame.group_id_none

    result = get_ReassignUserReportData(db, user_category_id, user_id, group_id)
    return technoreports.ReassignUserReportDataSuccess(result)

##################################################################################################################
# To get the Reassigned user report data and export to file
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of reassigned user data under the parameters
##################################################################################################################
def process_export_ReassignUserReportData(db, request, user_id):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, user_id, "ReassignUserReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return technoreports.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )

##################################################################################################################
# To get the Reassigned domain user report data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return list of reassigned domain user data under the parameters
##################################################################################################################
def process_get_ReassignUserDomainReportData(db, request_frame, user_id):
    result = get_ReassignUserDomainReportData(db, request_frame)
    return technoreports.ReassignUserDomainReportDataSuccess(result)

def process_get_AssignedStatutoriesList(db, request_frame, user_id):
    result = get_assigned_statutories_list(db, user_id)
    return technoreports.ApproveAssignedStatutoriesListSuccess(result)

def process_get_ComplianceStatutoriesList(db, request_frame, user_id):
    unit_id = request_frame.unit_id
    domain_id = request_frame.domain_id
    result = get_ComplianceStatutoriesList(db, unit_id, domain_id, user_id)


##################################################################################################################
# To export the group admin registration email report data
# Parameter(s) : Object of the database, user id
# Return Type : export list of group admin registered list
##################################################################################################################
def process_export_GroupAdminReportData(db, request, user_id):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, user_id, "GroupAdminRegistrationEMail"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return technoreports.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
