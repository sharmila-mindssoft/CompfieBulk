from server.jsontocsvconverter import ConvertJsonToCSV
from clientprotocol import (clientreport, clientreportnew)

from server.clientdatabase.clientreport import *

from server.clientdatabase.clientreportnew import *

from server.clientdatabase.general import (
    get_domains_for_user,
    get_units_for_user, get_acts_for_user,
    get_client_users,
    get_client_compliances,
    get_compliance_frequency, get_divisions,
    get_categories, legal_entity_logo_url
)

from server.clientdatabase.clientmaster import (
    get_service_providers_list
)

__all__ = [
    "process_client_report_requests"
]

def process_client_report_requests(request, db, session_user, session_category):
    request = request.request

    if type(request) is clientreport.GetReassignedHistoryReportFilters:
        result = get_reassignedhistory_report_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetReassignedHistoryReport:
        result = get_reassignedhistory_report(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetStatusReportConsolidatedFilters:

        result = get_status_report_consolidated_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetStatusReportConsolidated:
        result = get_status_report_consolidated(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetStatutorySettingsUnitWiseFilters:

        result = get_statutory_settings_unit_Wise_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetStatutorySettingsUnitWise:
        result = get_statutory_settings_unit_Wise(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetDomainScoreCardFilters:

        result = get_domain_score_card_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetDomainScoreCard:
        result = get_domain_score_card(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetLEWiseScoreCardFilters:

        result = get_le_wise_score_card_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetLEWiseScoreCard:
        result = get_le_wise_score_card(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetWorkFlowScoreCardFilters:
        result = get_work_flow_score_card_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreportnew.GetWorkFlowScoreCard:
        result = get_work_flow_score_card(
            db, request, session_user, session_category
        )

    # elif type(request) is clientreport.GetClientDetailsReportData:
    #     result = get_client_details_report_data(
    #         db, request, session_user, session_category
    #     )

    elif type(request) is clientreport.GetLegalEntityWiseReportFilters:
        result = get_legal_entity_wise_report_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetLegalEntityWiseReport:
        result = get_legal_entity_wise_report(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetDomainWiseReportFilters:
        result = get_domain_wise_report_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetDomainWiseReport:
        result = get_domain_wise_report(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetUnitWiseReportFilters:
        result = get_unit_wise_report_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetUnitWiseReport:
        result = get_unit_wise_report(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetServiceProviderWiseReportFilters:
        result = get_service_provider_wise_report_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetServiceProviderWiseReport:
        result = get_service_provider_wise_report(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetUserWiseReportFilters:
        result = get_user_wise_report_filters(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetUserWiseReport:
        result = get_user_wise_report(
            db, request, session_user, session_category
        )

    elif type(request) is clientreport.GetUnitListReportFilters:
        result = get_unit_list_report_filters(
            db, request, session_user
        )

    elif type(request) is clientreport.GetUnitListReport:
        result = get_unit_list_report(
            db, request, session_user
        )

    elif type(request) is clientreport.GetStatutoryNotificationsListReportFilters:
        result = get_statutory_notifications_list_report_filters(
            db, request, session_user
        )

    elif type(request) is clientreport.GetStatutoryNotificationsListReportData:
        result = get_statutory_notification_list_report(
            db, request, session_user
        )

    elif type(request) is clientreport.GetAuditTrailReportData:
        result = get_audit_trail_report_data(
            db, request, session_user
        )

    elif type(request) is clientreport.GetRiskReportFilters:
        result = get_risk_report_filters(
            db, request, session_user
        )

    elif type(request) is clientreport.GetRiskReportData:
        result = get_risk_report_data(
            db, request, session_user
        )

    return result


# Reassigned History Report Start


def get_reassignedhistory_report_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    unit_list = get_units_for_user(db, session_user)
    acts_list = get_acts_for_user(db, session_user)
    compliances_list = get_client_compliances(db, session_user)
    users_list = get_client_users(db)

    return clientreportnew.GetReassignedHistoryReportFiltersSuccess(
        domains=domain_list,
        units=unit_list,
        acts=acts_list,
        compliances=compliances_list,
        legal_entity_users=users_list
    )


def get_reassignedhistory_report(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        unit_id = request.unit_id
        act = request.act
        compliance_id = request.compliance_id
        usr_id = request.usr_id
        from_date = request.from_date
        to_date = request.to_date
        csv = request.csv
        f_count = request.f_count
        t_count = request.t_count

        reassigned_history_list = report_reassigned_history(
            db, country_id, legal_entity_id, domain_id, unit_id,
            act, compliance_id, usr_id, from_date, to_date, session_user, f_count, t_count
        )
        total_count = 0
        if request.count_qry:
            total_count = report_reassigned_history_total(
                db, country_id, legal_entity_id, domain_id, unit_id,
                act, compliance_id, usr_id, from_date, to_date, session_user
            )
        logo_url = legal_entity_logo_url(
            db, legal_entity_id
        )
        return clientreportnew.GetReassignedHistoryReportSuccess(
            reassigned_history_list, total_count, logo_url
        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreportnew.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Reassigned History Report End

# Status Report Consolidated Report Start

def get_status_report_consolidated_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    unit_list = get_units_for_user(db, session_user)
    acts_list = get_acts_for_user(db, session_user)
    compliances_list = get_client_compliances(db, session_user)
    compliance_frequency_list = get_compliance_frequency(db)
    users_list = get_client_users(db)
    return clientreportnew.GetStatusReportConsolidatedFiltersSuccess(
        domains=domain_list,
        units=unit_list,
        acts=acts_list,
        compliances=compliances_list,
        compliance_frequency=compliance_frequency_list,
        legal_entity_users=users_list
    )


def get_status_report_consolidated(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        unit_id = request.unit_id
        act = request.act
        compliance_id = request.compliance_id
        frequency_id = request.frequency_id
        user_type_id = request.user_type_id
        status_name = request.status_name
        usr_id = request.usr_id
        from_date = request.from_date
        to_date = request.to_date
        csv = request.csv
        f_count = request.f_count
        t_count = request.t_count

        status_report_consolidated_list = report_status_report_consolidated(
            db, country_id, legal_entity_id, domain_id, unit_id, act, compliance_id, frequency_id,
            user_type_id, status_name, usr_id, from_date, to_date, session_user, f_count, t_count
        )
        total_count = 0
        if request.count_qry:
            total_count = report_status_report_consolidated_total(
                db, country_id, legal_entity_id, domain_id, unit_id,act, compliance_id,
                frequency_id, user_type_id, status_name, usr_id, from_date, to_date, session_user
            )

        logo_url = legal_entity_logo_url(
            db, legal_entity_id
        )
        return clientreportnew.GetStatusReportConsolidatedSuccess(
            status_report_consolidated_list, total_count, logo_url
        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "StatusReportConsolidated"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Status Report Consolidated Report End

# Statutory Settings Unit Wise Start


def get_statutory_settings_unit_Wise_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    unit_list = get_units_for_user(db, session_user)
    acts_list = get_acts_for_user(db, session_user)
    compliances_list = get_client_compliances(db, session_user)
    compliance_frequency_list = get_compliance_frequency(db)
    divisions_list = get_divisions(db)
    categories_list = get_categories(db)

    return clientreportnew.GetStatutorySettingsUnitWiseFiltersSuccess(
        domains=domain_list,
        units=unit_list,
        acts=acts_list,
        compliances=compliances_list,
        compliance_frequency=compliance_frequency_list,
        divisions=divisions_list,
        categories=categories_list
    )


def get_statutory_settings_unit_Wise(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        bg_id = request.bg_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        unit_id = request.unit_id
        div_id = request.div_id
        cat_id = request.cat_id
        act = request.act
        compliance_id = request.compliance_id
        frequency_id = request.frequency_id
        status_name = request.status_name
        csv = request.csv
        f_count = request.f_count
        t_count = request.t_count

        statutory_settings_unit_Wise_list = report_statutory_settings_unit_Wise(
            db, country_id, bg_id, legal_entity_id, domain_id, unit_id,
            div_id, cat_id, act, compliance_id, frequency_id, status_name, session_user, f_count, t_count
        )
        total_count = 0
        if request.count_qry:
            total_count = report_statutory_settings_unit_Wise_total(
                db, country_id, bg_id, legal_entity_id, domain_id, unit_id, div_id, cat_id,
                act, compliance_id, frequency_id, status_name, session_user
            )

        logo_url = legal_entity_logo_url(
            db, legal_entity_id
        )
        return clientreportnew.GetStatutorySettingsUnitWiseSuccess(
            statutory_settings_unit_Wise_list, total_count, logo_url
        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "StatutorySettingsUnitWise"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Statutory Settings Unit Wise End

# Domain Score Card Start


def get_domain_score_card_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    divisions_list = get_divisions(db)
    categories_list = get_categories(db)

    return clientreportnew.GetDomainScoreCardFiltersSuccess(
        domains=domain_list,
        divisions=divisions_list,
        categories=categories_list
    )


def get_domain_score_card(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        bg_id = request.bg_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        div_id = request.div_id
        cat_id = request.cat_id

        domain_score_card_list = report_domain_score_card(
            db, country_id, bg_id, legal_entity_id, domain_id, div_id, cat_id, session_user
        )
        logo_url = legal_entity_logo_url(
            db, legal_entity_id
        )
        return clientreportnew.GetDomainScoreCardSuccess(domain_score_card_list, logo_url)
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreportnew.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Domain Score Card End


# Legal Entity Wise Score Card Start
def get_le_wise_score_card_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)

    return clientreportnew.GetLEWiseScoreCardFiltersSuccess(
        domains=domain_list
    )


def get_le_wise_score_card(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id

        le_wise_score_card_list = report_le_wise_score_card(
            db, country_id, legal_entity_id, domain_id, session_user, session_category
        )
        logo_url = legal_entity_logo_url(
            db, legal_entity_id
        )
        return clientreportnew.GetLEWiseScoreCardSuccess(le_wise_score_card_list, logo_url)
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreportnew.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Legal Entity Wise Score Card End


# Work Flow Score Card Start
def get_work_flow_score_card_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    return clientreportnew.GetWorkFlowScoreCardFiltersSuccess(
        domains=domain_list
    )


def get_work_flow_score_card(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id

        work_flow_score_card_list = report_work_flow_score_card(
            db, country_id, legal_entity_id, domain_id, session_user, session_category
        )
        logo_url = legal_entity_logo_url(
            db, legal_entity_id
        )
        return clientreportnew.GetWorkFlowScoreCardSuccess(work_flow_score_card_list, logo_url)
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreportnew.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Work Flow Score Card End


def get_client_details_report_data(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ClientDetails"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        units = get_client_details_report(
            db, request.country_id, request.business_group_id,
            request.legal_entity_id, request.division_id, request.unit_id,
            request.domain_ids, session_user, request.from_count, request.page_count
        )
        total_count = get_client_details_count(
            db, request.country_id, request.business_group_id,
            request.legal_entity_id, request.division_id, request.unit_id,
            request.domain_ids, session_user
        )
        return clientreport.GetClientDetailsReportDataSuccess(
            units=units, total_count=total_count
        )


def export_to_csv(db, request, session_user, session_category):
    converter = ConvertJsonToCSV(db, request, session_user)
    return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)


##########################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains domain list, compliances, units
##########################################################################

def get_legal_entity_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domains_list = get_domains_for_le(db, legal_entity_id)
    unit_list = get_units_for_le_domain(db, country_id, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    # task_list = get_task_for_le_domain(db, legal_entity_id)
    frequency_list = get_frequency_list(db)
    compliance_user_type = get_compliance_user_type(db)
    compliance_status = get_compiance_status(db)
    compliance_user_list = get_compliance_user_list(
        db, country_id, legal_entity_id)
    return clientreport.GetLegalEntityWiseReportFiltersSuccess(
        domains=domains_list, unit_legal_entity=unit_list, act_legal_entity=act_list,
        # compliance_task_list=task_list,
        compliance_frequency_list=frequency_list,
        compliance_user_type=compliance_user_type, compliance_task_status=compliance_status,
        compliance_users=compliance_user_list
    )

##########################################################################
# Objective: To get legal entity wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
##########################################################################


def get_legal_entity_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "LegalEntityWiseReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_legal_entity_wise_report(db, request)
        return clientreport.GetLegalEntityWiseReportSuccess(legal_entities_compliances=result, total_count=total_record)

##########################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains domain list, compliances, units
##########################################################################


def get_domain_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domains_list = get_domains_for_le(db, legal_entity_id)
    unit_list = get_units_for_le_domain(db, country_id, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    #task_list = get_task_for_le_domain(db, legal_entity_id)
    frequency_list = get_frequency_list(db)
    compliance_user_type = get_compliance_user_type(db)
    compliance_status = get_compiance_status(db)
    compliance_user_list = get_compliance_user_list(
        db, country_id, legal_entity_id)
    return clientreport.GetDomainWiseReportFiltersSuccess(
        domains=domains_list, unit_legal_entity=unit_list, act_legal_entity=act_list,
        compliance_frequency_list=frequency_list,
        compliance_user_type=compliance_user_type, compliance_task_status=compliance_status,
        compliance_users=compliance_user_list
    )

##########################################################################
# Objective: To get legal entity wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
##########################################################################


def get_domain_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "DomainWiseReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_domain_wise_report(db, request)
        return clientreport.GetDomainWiseReportSuccess(legal_entities_compliances=result, total_count=total_record)


##########################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains domain list, compliances, units
##########################################################################

def get_unit_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domains_list = get_domains_for_le(db, legal_entity_id)
    unit_list = get_units_for_le_domain(db, country_id, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    # task_list = get_task_for_le_domain(db, legal_entity_id)
    frequency_list = get_frequency_list(db)
    compliance_user_type = get_compliance_user_type(db)
    compliance_status = get_compiance_status(db)
    compliance_user_list = get_compliance_user_list(
        db, country_id, legal_entity_id)
    return clientreport.GetUnitWiseReportFiltersSuccess(
        domains=domains_list, unit_legal_entity=unit_list, act_legal_entity=act_list,
        compliance_frequency_list=frequency_list,
        compliance_user_type=compliance_user_type, compliance_task_status=compliance_status,
        compliance_users=compliance_user_list
    )

##########################################################################
# Objective: To get unit wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
##########################################################################


def get_unit_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "UnitWiseReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_unit_wise_report(db, request)
        return clientreport.GetUnitWiseReportSuccess(unit_compliances=result, total_count=total_record)


##########################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains service provider list, domain list, compliances.
##########################################################################
def get_service_provider_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    sp_list = get_service_providers_list(db)
    sp_domains_list = get_domains_for_sp_users(db, legal_entity_id)
    sp_unit_list = get_units_for_sp_users(db, country_id, legal_entity_id)
    sp_act_task_list = get_acts_for_sp_users(db, legal_entity_id, country_id)
    compliance_status = get_compiance_status(db)
    sp_user_list = get_service_provider_user_list(
        db, country_id, legal_entity_id)
    return clientreport.GetServiceProviderWiseReportFiltersSuccess(
        sp_domains_list=sp_domains_list, sp_unit_list=sp_unit_list,
        sp_act_task_list=sp_act_task_list, sp_list=sp_list,
        compliance_task_status=compliance_status, sp_users_list=sp_user_list
    )

##########################################################################
# Objective: To get unit wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
##########################################################################


def get_service_provider_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ServiceProviderWiseReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_service_provider_wise_report(db, request)
        return clientreport.GetServiceProviderWiseReportSuccess(sp_compliances=result, total_count=total_record)


##########################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains users lits, domain list, compliances, units
##########################################################################

def get_user_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    le_users_list = get_le_users_list(db)
    user_domains_list = get_domains_for_le_users(db, legal_entity_id)
    users_units_list = get_units_for_le_users(db, country_id, legal_entity_id)
    user_act_task_list = get_acts_for_le_users(db, legal_entity_id, country_id)
    frequency_list = get_frequency_list(db)
    compliance_user_type = get_compliance_user_type(db)
    compliance_status = get_compiance_status(db)
    return clientreport.GetUserWiseReportFiltersSuccess(
        le_users_list=le_users_list, user_domains_list=user_domains_list,
        users_units_list=users_units_list,
        user_act_task_list=user_act_task_list,
        compliance_frequency_list=frequency_list,
        compliance_user_type=compliance_user_type, compliance_task_status=compliance_status
    )

##########################################################################
# Objective: To get unit wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
##########################################################################


def get_user_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "UserWiseReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_user_wise_report(db, request)
        return clientreport.GetUserWiseReportSuccess(user_compliances=result, total_count=total_record)


##########################################################################
# Objective: To get the filters data under selected legal entity, country and business group
# Parameter: request object and the client id
# Result: list of record sets which contains division, category, unit, domain and organization
##########################################################################
def get_unit_list_report_filters(db, request, session_user):
    country_id = request.country_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    divsions_list = get_divisions_for_unit_list(
        db, business_group_id, legal_entity_id)
    categories_list = get_categories_for_unit_list(
        db, business_group_id, legal_entity_id)
    units_list = get_units_list(
        db, country_id, business_group_id, legal_entity_id)
    domains_organisation_list = get_domains_organization_for_le(
        db, legal_entity_id)
    unit_status_list = get_units_status(db)
    return clientreport.GetUnitListReportFiltersSuccess(
        divisions=divsions_list, categories=categories_list, units_list=units_list,
        domains_organisations_list=domains_organisation_list, unit_status_list=unit_status_list
    )

##########################################################################
# Objective: To get unit details under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains units and its status
##########################################################################


def get_unit_list_report(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "UnitListReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_unit_list_report(db, request)
        return clientreport.GetunitListReportSuccess(unit_list_report=result, total_count=total_record)

##########################################################################
# Objective: To get domains and acts under legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains domains and acts
##########################################################################


def get_statutory_notifications_list_report_filters(db, request, session_user):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_list = get_domains_for_le(db, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    return clientreport.GetStatutoryNotificationsListReportFilterSuccess(
        domains=domain_list, act_legal_entity=act_list
    )


##########################################################################
# Objective: To get statutory notification list under domain and legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains act and compliance tasks
##########################################################################
def get_statutory_notification_list_report(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "StatutoryNotificationListReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_statutory_notification_list_report(db, request)
        return clientreport.GetStatutoryNotificationReportDataSuccess(stat_notf_list_report=result, total_count=total_record)

##########################################################################
# Objective: To get activity log under user and form
# Parameter: request object and the client id
# Result: list of record sets which contains activity log of forms
##########################################################################


def get_audit_trail_report_data(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "AuditTrailReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_audit_trail_report(db, request)
        return clientreport.GetAuditTrailReportDataSuccess(audit_activities=result, total_count=total_record)

##########################################################################
# Objective: To get risk report filters
# Parameter: request object and the client id
# Result: list of record sets which contains domains, division, categories, and units
##########################################################################


def get_risk_report_filters(db, request, session_user):
    country_id = request.country_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    domain_list = get_domains_for_le(db, legal_entity_id)
    divsions_list = get_divisions_for_unit_list(
        db, business_group_id, legal_entity_id)
    categories_list = get_categories_for_unit_list(
        db, business_group_id, legal_entity_id)
    units_list = get_units_list(
        db, country_id, business_group_id, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    task_list = get_task_for_le_domain(db, legal_entity_id)
    compliance_status = get_risk_compiance_status(db)
    return clientreport.GetRiskReportFiltersSuccess(
        domains=domain_list, divisions=divsions_list, categories=categories_list,
        units_list=units_list, act_legal_entity=act_list, compliance_task_list=task_list,
        compliance_task_status=compliance_status)

##########################################################################
# Objective: To get legal entity wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains risk compliance list with the status
##########################################################################


def get_risk_report_data(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "RiskReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_risk_report(db, request)
        return clientreport.GetRiskReportSuccess(risk_report=result, total_count=total_record)
