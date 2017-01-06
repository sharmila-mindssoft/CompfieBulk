CLIENT_TEMPLATE_PATHS = [
    (
        "/login",
        "files/client/login/login.html",
        None, {}
    ),
    (
        r"/forgot_password/([a-zA-Z-0-9]+)",
        "files/client/forgotpassword.html",
        None, {}
    ),
    (
        r"/reset_password/([a-zA-Z-0-9]+)/([a-zA-Z-0-9]+)",
        "files/client/resetpassword.html",
        None, {}
    ),
    (
        r"/test/([a-zA-Z-0-9]+)", "test_apis.html", None, {}
    ),
    # Widgets ---------------------------------------------------------------------
    (
        "/home",
        "files/client/home/home.html",
        None, {}
    ),
    # Dashboard ---------------------------------------------------------------------
    (
        "/dashboard",
        "files/client/client-home/client-home.html",
        None, {}
    ),
    # Master ---------------------------------------------------------------------
    (
        "/service-provider",
        "files/client/service-provider/service_provider_list.html",
        None, {}
    ),
    (
        "/client-user-privilege",
        "files/client/user-privileges/user_privileges.html",
        None, {}
    ),
    (
        "/client-user-management",
        "files/client/client-user-management/client-user-management.html",
        None, {}
    ),
    (
        "/unit-closure",
        "files/client/unit-closure/unitclosure.html",
        None, {}
    ),
    # transactions ---------------------------------------------------------------------
    (
        "/statutory-settings",
        "files/client/statutory-settings/statutorysettings.html",
        None, {}
    ),
    (
        "/review-settings",
        "files/client/review-settings/review-settings.html",
        None, {}
    ),
    (
        "/assign-compliance",
        "files/client/assign-compliance/assigncompliance.html",
        None, {}
    ),
    (
        "/reassign-compliance",
        "files/client/reassign-compliance/reassigncompliance.html",
        None, {}
    ),
    (
        "/compliance-approval",
        "files/client/compliance-approval/complianceapproval.html",
        None, {}
    ),
    (
        "/completed-tasks-current-year",
        "files/client/completed-tasks-current-year/completed-task-current-year.html",
        None, {}
    ),
    (
        "/on-occurrence-compliances",
        "files/client/on-occurrence-compliances/onoccurrencecompliances.html",
        None, {}
    ),
    (
        "/compliance-details",
        "files/client/compliance-details/compliancedetails.html",
        None, {}
    ),
    # reports ---------------------------------------------------------------------
    (
        "/legal-entity-wise-report",
        "files/client/legal-entity-wise-report/legal-entity-wise-report.html",
        None, {}
    ),
    (
        "/domain-wise-report",
         "files/client/domain-wise-report/domain-wise-report.html",
        None, {}
    ),
    (
        "/unit-wise-compliance",
        "files/client/unit-wise-compliance/unitwisecompliance.html",
        None, {}
    ),
    (
        "/service-provider-wise-compliance",
        "files/client/service-provider-wise-compliance/serviceproviderwisecompliance.html",
        None, {}
    ),
    (
        "/user-wise-compliance",
        "files/client/user-wise-compliance/user-wise-compliance.html",
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
        "files/client/legal-entity-wise-score-card/legal-entity-wise-score-card.html",
        None, {}
    ),
    (
        "/work-flow-score-card",
        "files/client/work-flow-score-card/work-flow-score-card.html",
        None, {}
    ),
    (
        "/statutory-settings-unit-wise-report",
        "files/client/statutory-settings-unit-wise-report/statutory-settings-unit-wise-report.html",
        None, {}
    ),
    (
        "/reassigned-history-report",
        "files/client/reassigned-history-report/reassigned-history-report.html",
        None, {}
    ),
    (
        "/risk-report",
        "files/client/risk-report/risk-report.html",
        None, {}
    ),
    (
        "/unit-list",
        "files/client/unit-list/risk-report.html",
        None, {}
    ),
    (
        "/statutory-notification-list",
        "files/client/statutory-notification-list/statutory-notification-list.html",
        None, {}
    ),
    (
        "/service-provider-details",
        "files/client/service-provider-details/service-provider-details.html",
        None, {}
    ),
    (
        "/audit-trail",
        "files/client/audit-trail/audit-trail.html",
        None, {}
    ),
    (
        "/login-trace",
        "files/client/login-trace/login-trace.html",
        None, {}
    ),
    # My Accounts ---------------------------------------------------------------------
    (
        "/view-profile",
        "files/client/view-profile/view-profile.html",
        None, {}
    ),
    (
        "/client-view-profile",
        "files/client/client-view-profile/client-view-profile.html",
        None, {}
    ),
    (
        "/change-password",
        "files/client/change-password/change-password.html",
        None, {}
    ),
    (
        "/client-settings",
        "files/client/client-settings/client-settings.html",
        None, {}
    ),
    (
        "/themes",
        "files/client/themes/themes.html",
        None, {}
    ),
    # Notification ---------------------------------------------------------------------
    (
        "/notifications",
        "files/client/notifications/notifications.html",
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
        "files/client/message/message.html",
        None, {}
    )
]
