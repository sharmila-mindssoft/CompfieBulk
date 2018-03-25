CLIENT_TEMPLATE_PATHS = [
    # (
    #     r"/",
    #     "files/client/login/login.html",
    #     None, {}
    # ),
    (
        r"/login",
        "files/client/login/login.html",
        None, {}
    ),
    # (
    #     r"/forgot_password/([a-zA-Z-0-9]+)",
    #     "files/client/forgotpassword.html",
    #     None, {}
    # ),
    (
        "/forgot-password",
        "files/client/forgot-password/forgot-password.html",
        None, {}
    ),
    (
        r"/reset_password/([a-zA-Z-0-9]+)/([a-zA-Z-0-9]+)",
        "files/client/reset-password/resetpassword.html",
        None, {}
    ),
    (
        r"/test/([a-zA-Z-0-9]+)", "test_apis.html", None, {}
    ),
    # Widgets ---------------------------------------------------------------------
    (
        r"/home",
        "files/client/widgets/widgets.html",
        None, {}
    ),
    # Welcome ---------------------------------------------------------------------
    (
        r"/welcome",
        "files/client/home/welcome.html",
        None, {}
    ),
    # Dashboard ---------------------------------------------------------------------
    (
        r"/dashboard",
        "files/client/dashboard/dashboard.html",
        None, {}
    ),
    # Master ---------------------------------------------------------------------
    (
        r"/service-provider",
        "files/client/service-provider/service_provider.html",
        None, {}
    ),
    (
        "/client-user-privilege",
        "files/client/user-privileges/user_privileges.html",
        None, {}
    ),
    (
        "/client-user-management",
        "files/client/client-user-management/client_user_management.html",
        None, {}
    ),
    (
        "/unit-closure",
        "files/client/unit-closure/unit_closure.html",
        None, {}
    ),
    (
        r"/userregistration/([a-zA-Z-0-9]+)/([a-zA-Z-0-9]+)",
        "files/client/login/user-create-login-details.html",
        None, {}
    ),
    # transactions ---------------------------------------------------------------------
    (
        r"/statutory-settings/([a-zA-Z-0-9=]+)",
        "files/client/statutory-settings/statutory_settings.html",
        None, {}
    ),
    (
        r"/review-settings/([a-zA-Z-0-9=]+)",
        "files/client/review-settings/review-settings.html",
        None, {}
    ),
    (
        r"/assign-compliance/([a-zA-Z-0-9=]+)",
        "files/client/assign-compliance/assign-compliance.html",
        None, {}
    ),
    (
        r"/reassign-compliance/([a-zA-Z-0-9=]+)",
        "files/client/reassign-compliance/reassign-compliance.html",
        None, {}
    ),
    (
        r"/compliance-approval/([a-zA-Z-0-9=]+)",
        "files/client/compliance-approval/compliance-approval.html",
        None, {}
    ),
    (
        r"/completed-tasks-current-year/([a-zA-Z-0-9=]+)",
        "files/client/completed-task-current-year/completed-task-current-year.html",
        None, {}
    ),
    (
        r"/on-occurrence-compliances/([a-zA-Z-0-9=]+)",
        "files/client/on-occurrence-compliances/on_occurrence_compliances.html",
        None, {}
    ),
    (
        r"/compliance-task-details/([a-zA-Z-0-9=]+)",
        "files/client/compliance-task-details/compliance_task_details.html",
        None, {}
    ),
    (
        r"/completed-tasks-current-year-bu/([a-zA-Z-0-9=]+)",
        "files/client/bulkupload/completed_task_current_year/Completed-task-current-year-BulkUpload_List.html",
        None, {}
    ),
    # reports ---------------------------------------------------------------------
    (
        "/legal-entity-wise-report",
        "files/client/legal-entity-wise-report/legal_entity_wise_report.html",
        None, {}
    ),
    (
        "/domain-wise-report",
        "files/client/domain-wise-report/domain_wise_report.html",
        None, {}
    ),
    (
        "/unit-wise-compliance",
        "files/client/unit-wise-report/unit_wise_report.html",
        None, {}
    ),
    (
        "/service-provider-wise-compliance",
        "files/client/service-provider-wise-report/service_provider_wise_report.html",
        None, {}
    ),
    (
        "/user-wise-compliance",
        "files/client/user-wise-report/user_wise_report.html",
        None, {}
    ),
    (
        "/status-report-consolidated",
        "files/client/status-report-consolidated/status_report_consolidated.html",
        None, {}
    ),
    (
        "/domain-score-card",
        "files/client/domain-score-card/domain_score_card.html",
        None, {}
    ),
    (
        "/legal-entity-wise-score-card",
        "files/client/legal-entity-wise-score-card/legal_entity_wise_score_card.html",
        None, {}
    ),
    (
        "/work-flow-score-card",
        "files/client/work-flow-score-card/work_flow_score_card.html",
        None, {}
    ),
    (
        "/statutory-settings-unit-wise-report",
        "files/client/statutory-settings-unit-wise/statutory_settings_unit_wise.html",
        None, {}
    ),
    (
        "/reassigned-history-report",
        "files/client/reassigned-history/reassign_history.html",
        None, {}
    ),
    (
        "/risk-report",
        "files/client/risk-report/risk_report.html",
        None, {}
    ),
    (
        "/unit-list",
        "files/client/unit-list/unit_list.html",
        None, {}
    ),
    (
        "/statutory-notification-list",
        "files/client/statutory-notifications-list/statutory-notifications-list.html",
        None, {}
    ),
    (
        "/service-provider-details",
        "files/client/service-provider-details/service_provider_details.html",
        None, {}
    ),
    (
        "/audit-trail",
        "files/client/audit-trail-client/audit_trail_client.html",
        None, {}
    ),
    (
        "/login-trace",
        "files/client/login-trace/login_trace.html",
        None, {}
    ),
    # My Accounts ---------------------------------------------------------------------
    (
        "/view-profile",
        "files/client/profile/profile.html",
        None, {}
    ),
    (
        "/change-password",
        "files/client/change-password/change-password.html",
        None, {}
    ),
    (
        "/settings",
        "files/client/settings/client-settings.html",
        None, {}
    ),
    (
        "/themes",
        "files/client/settings/themes.html",
        None, {}
    ),
    # Notification ---------------------------------------------------------------------
    (
        "/notifications",
        "files/client/statutory-notification/statutory_notification.html",
        None, {}
    ),
    # Reminders ---------------------------------------------------------------------
    (
        "/reminders",
        "files/client/reminders/reminders.html",
        None, {}
    ),
    # Escalations ---------------------------------------------------------------------
    (
        "/escalations",
        "files/client/escalations/escalations.html",
        None, {}
    ),
    # Message ---------------------------------------------------------------------
    (
        "/message",
        "files/client/messages/messages.html",
        None, {}
    )
]
