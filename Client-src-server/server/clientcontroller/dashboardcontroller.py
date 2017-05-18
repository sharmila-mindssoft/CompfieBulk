from clientprotocol import (dashboard, clientreport)
from server.jsontocsvconverter import ConvertJsonToCSV
from server.constants import RECORD_DISPLAY_COUNT
from server.clientdatabase.dashboard import *

__all__ = [
    "process_client_dashboard_requests",
    "merge_compliance_status",
    "merge_escalation_status"
]

########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_dashboard_requests(request, db, session_user, session_category):

    request = request.request
    print " process_client_dashboard_requests -------------------------------------- "

    if type(request) is dashboard.GetComplianceStatusChart:

        result = process_compliance_status_chart(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.GetComplianceStatusDrillDownData:
        result = process_compliance_status_chart_drilldown(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.GetEscalationsChart:
        result = process_escalation_chart(db, request, session_user, session_category)

    elif type(request) is dashboard.GetEscalationsDrillDownData:
        result = process_escalation_chart_drilldown(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.GetNotCompliedChart:
        result = process_not_complied_chart(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.GetNotCompliedDrillDown:
        result = process_not_complied_drill_down(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.GetTrendChart:
        result = process_trend_chart(db, request, session_user, session_category)

    elif type(request) is dashboard.GetTrendChartDrillDownData:
        result = process_get_trend_chart_drilldown(
            db, request, session_user
        )

    elif type(request) is dashboard.GetComplianceApplicabilityStatusChart:
        result = process_compliance_applicability_chat(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.GetComplianceApplicabilityStatusDrillDown:

        result = process_compliance_applicability_drill_down(
            db, request, session_user
        )

    elif type(request) is dashboard.GetNotificationsCount:
        result = process_get_notifications_count(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.GetNotifications:
        result = process_get_notifications(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.UpdateNotificationStatus:
        result = process_update_notification_status(
            db, request, session_user
        )

    elif type(request) is dashboard.GetStatutoryNotifications:
        result = process_get_statutory_notifications(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.UpdateStatutoryNotificationsStatus:
        result = process_update_statutory_notification_status(
            db, request, session_user
        )

    elif type(request) is dashboard.GetAssigneeWiseCompliancesChart:
        result = process_assigneewise_compliances(
            db, request, session_user, session_category
        )
    elif type(request) is dashboard.GetAssigneewiseYearwiseCompliances:

        result = process_assigneewise_yearwise_compliances(
            db, request, session_user
        )

    elif type(request) is dashboard.GetAssigneewiseReassignedComplianes:

        result = process_get_assigneewise_reassigned_compliances(
            db, request, session_user
        )

    elif type(request) is dashboard.GetAssigneeWiseComplianceDrillDown:

        result = process_assigneewise_compliances_drilldown(
            db, request, session_user, session_category
        )

    elif type(request) is dashboard.CheckContractExpiration:
        result = check_contract_expiration(
            db, request, session_user
        )

    return result

def process_compliance_status_chart(db, request, session_user, session_category):

    return get_compliance_status_chart(db, request, session_user, session_category)


def process_trend_chart(db, request, session_user, session_category):
    years, data = get_trend_chart(db, request, session_user, session_category)
    return dashboard.GetTrendChartSuccess(
        years=years,
        data=data
    )


def process_get_trend_chart_drilldown(db, request, session_user):
    drill_down_info = None
    filter_ids = None if(
        request.filter_ids is None
    ) else ",".join(str(x) for x in request.filter_ids)
    drill_down_info = get_trend_chart_drill_down(
        db,
        request.country_ids,
        request.domain_ids, filter_ids,
        request.filter_type, request.year
    )
    print drill_down_info
    return dashboard.GetTrendChartDrillDownDataSuccess(
        drill_down_data=drill_down_info
    )


def process_compliance_status_chart_drilldown(
    db, request, session_user, session_category
):
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    unit_wise_data = get_compliances_details_for_status_chart(
        db,
        request, session_user, session_category,
        from_count, to_count
    )
    return dashboard.GetComplianceStatusDrillDownDataSuccess(
        unit_wise_data.values()
    )


def process_escalation_chart(db, request, session_user, session_category):
    return get_escalation_chart(db, request, session_user, session_category)


def process_escalation_chart_drilldown(db, request, session_user, session_category):
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    result_list = get_escalation_drill_down_data(
        db,
        request, session_user, session_category,
        from_count, to_count
    )
    return dashboard.GetEscalationsDrillDownDataSuccess(
        result_list[0],
        result_list[1]
    )


def process_not_complied_chart(db, request, session_user, session_category):
    return get_not_complied_count(db, request, session_user, session_category)


def process_not_complied_drill_down(db, request, session_user, session_category):
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    result_list = get_not_complied_drill_down(
        db,
        request, session_user, session_category,
        from_count, to_count
    )
    return dashboard.GetNotCompliedDrillDownSuccess(result_list.values())


def process_compliance_applicability_chat(
    db, request, session_user, session_category
):
    return get_risk_chart_count(
        db, request, session_user, session_category
    )


def process_compliance_applicability_drill_down(
    db, request, session_user
):
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    result_list = get_compliance_applicability_drill_down(
        db,
        request, session_user,
        from_count, to_count
    )
    return dashboard.GetComplianceApplicabilityStatusDrillDownSuccess(
        result_list
    )

def process_get_notifications_count(db, request, session_user, session_category):
    notification_count = get_notification_counts(db, session_user, session_category, request.legal_entity_ids)
    return dashboard.GetNotificationsCountSuccess(notification_count)

def process_get_notifications(db, request, session_user, session_category):
    notification_type = request.notification_type
    if request.notification_type == 2:  # Reminders
        reminders = get_reminders(db, request.notification_type, request.start_count, request.end_count, session_user, session_category)
        # reminder_count = get_reminders_count(db, request.notification_type, session_user, session_category)
        return dashboard.GetRemindersSuccess(reminders)
    elif request.notification_type == 3:  # Escalations
        escalations = get_escalations(db, request.notification_type, request.start_count, request.end_count, session_user, session_category)
        return dashboard.GetEscalationsSuccess(escalations)
    elif request.notification_type == 4:  # Messages
        messages = get_messages(db, request.notification_type, request.start_count, request.end_count, session_user, session_category)
        return dashboard.GetMessagesSuccess(messages)

def process_update_notification_status(db, request, session_user):
    if request.has_read is True:
        update_notification_status(db, request.notification_id, session_user)
    notification_details = notification_detail(db, request.notification_id, session_user)
    return dashboard.UpdateNotificationStatusSuccess(notification_details)


def process_get_statutory_notifications(db, request, session_user, session_category):
    statutory = get_statutory(db, request.start_count, request.end_count, session_user, session_category, request.legal_entity_ids)
    return dashboard.GetStatutorySuccess(statutory)

def process_update_statutory_notification_status(db, request, session_user):
    if request.has_read is True:
        update_statutory_notification_status(db, request.notification_id, session_user)
    statutory_notification_details = statutory_notification_detail(db, request.notification_id, session_user)
    return dashboard.StatutoryUpdateNotificationStatusSuccess(statutory_notification_details)


########################################################
# To retrieve data for assignee wise compliances chart
# based on the received filters
########################################################
def process_assigneewise_compliances(db, request, session_user, session_category):

    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "AssigneeWise", session_category
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        country_id = request.country_id
        business_group_id = request.business_group_id
        legal_entity_id = request.legal_entity_ids[0]
        division_id = request.division_id
        unit_id = request.unit_id
        user_id = request.user_id
        chart_data = get_assigneewise_compliances_list(
            db, country_id, business_group_id, legal_entity_id,
            division_id, unit_id, session_user, user_id, session_category
        )
        return dashboard.GetAssigneeWiseCompliancesChartSuccess(
            chart_data=chart_data
        )


def process_assigneewise_yearwise_compliances(
    db, request, session_user
):
    country_id = request.country_id
    unit_id = request.unit_id
    user_id = request.user_id
    domain_ids = request.domain_ids
    chart_data = get_assigneewise_yearwise_compliances(
        db, country_id, unit_id, user_id, domain_ids
    )
    return dashboard.GetAssigneewiseYearwiseCompliancesSuccess(
        chart_data=chart_data
    )


def process_get_assigneewise_reassigned_compliances(
    db, request, session_user
):
    country_id = request.country_id
    unit_id = request.unit_id
    user_id = request.user_id
    domain_id = request.domain_id
    chart_data = get_assigneewise_reassigned_compliances(
        db,
        country_id, unit_id, user_id, domain_id
    )
    return dashboard.GetAssigneewiseReassignedComplianesSuccess(
        chart_data=chart_data
    )


########################################################
# To get the detailed info of the selected domain in the
# assignee wise compliances chart
########################################################
def process_assigneewise_compliances_drilldown(
    db, request, session_user, session_category
):
    country_id = request.country_id
    assignee_id = request.assignee_id
    domain_ids = request.domain_ids
    year = request.year
    unit_id = request.unit_id
    start_count = request.start_count
    to_count = RECORD_DISPLAY_COUNT

    drill_down_data = {}
    (
        complied, delayed, inprogress, not_complied
    ) = get_assigneewise_compliances_drilldown_data(
            db, country_id, assignee_id, domain_ids,
            year, unit_id, start_count, to_count, session_user, session_category
    )
    total_count = get_assigneewise_compliances_drilldown_data_count(
        db, country_id, assignee_id, domain_ids,
        year, unit_id, session_user, session_category
    )

    drill_down_data = dashboard.AssigneeWiseCompliance(
        complied=complied,
        delayed=delayed,
        inprogress=inprogress,
        not_complied=not_complied
    )
    return dashboard.GetAssigneeWiseComplianceDrillDownSuccess(
        drill_down_data=drill_down_data,
        total_count=total_count
    )


########################################################
# To check whether the contract of the given client
# expired or not and to get the notification, reminder
# and escalation count
########################################################
def check_contract_expiration(
    db, request, session_user
):
    no_of_days_left = get_no_of_days_left_for_contract_expiration(
        db
    )
    if no_of_days_left < 0:
        no_of_days_left = 0
    (
        notification_count, reminder_count, escalation_count
    ) = get_dashboard_notification_counts(
        db,
        session_user
    )
    show_popup, notification_text = need_to_display_deletion_popup(db)
    return dashboard.CheckContractExpirationSuccesss(
        no_of_days_left=no_of_days_left,
        notification_count=notification_count,
        reminder_count=reminder_count,
        escalation_count=escalation_count,
        show_popup=show_popup,
        notification_text=notification_text
    )

########################################################
#To get the messages selected legal entity in menu
########################################################
def process_get_messages(
    db, request, session_user
):
    no_of_days_left = get_no_of_days_left_for_contract_expiration(
        db
    )
    if no_of_days_left < 0:
        no_of_days_left = 0
    (
        notification_count, reminder_count, escalation_count
    ) = get_dashboard_notification_counts(
        db,
        session_user
    )
    show_popup, notification_text = need_to_display_deletion_popup(db)
    return dashboard.CheckContractExpirationSuccesss(
        no_of_days_left=no_of_days_left,
        notification_count=notification_count,
        reminder_count=reminder_count,
        escalation_count=escalation_count,
        show_popup=show_popup,
        notification_text=notification_text
    )

def merge_compliance_status(chart_data) :
    final_data = {}
    for idx, c in enumerate(chart_data):
        if final_data.get(c.filter_type_id) is None :
            if len(c.data) == 1 :
                final_data[c.filter_type_id] = c
            else :
                for idx, count in enumerate(c.data):
                    if idx == 0 :
                        p_c = count
                    else :
                        p_c.complied_count += count.complied_count
                        p_c.delayed_compliance_count += count.delayed_compliance_count
                        p_c.inprogress_compliance_count += count.inprogress_compliance_count
                        p_c.not_complied_count += count.not_complied_count
                c.data = [p_c]
                final_data[c.filter_type_id] = c
        else :
            p_c = final_data[c.filter_type_id]
            if len(c.data) == 1 :
                p_c.data[0].complied_count += c.data[0].complied_count
                p_c.data[0].delayed_compliance_count += c.data[0].delayed_compliance_count
                p_c.data[0].inprogress_compliance_count += c.data[0].inprogress_compliance_count
                p_c.data[0].not_complied_count += c.data[0].not_complied_count
            else :
                for idx, count in enumerate(c.data):
                    p_c.data[0].complied_count += count.complied_count
                    p_c.data[0].delayed_compliance_count += count.delayed_compliance_count
                    p_c.data[0].inprogress_compliance_count += count.inprogress_compliance_count
                    p_c.data[0].not_complied_count += count.not_complied_count
            final_data[c.filter_type_id] = p_c
    return final_data.values()

def merge_escalation_status(chart_data):
    final_data = {}
    for d in chart_data :
        if final_data.get(d.year) is None :
            final_data[d.year] = d
        else :
            d1 = final_data.get(d.year)
            d1.delayed_compliance_count += d.delayed_compliance_count
            d1.not_complied_count += d.not_complied_count
            final_data[d.year] = d1

    return final_data.values()
