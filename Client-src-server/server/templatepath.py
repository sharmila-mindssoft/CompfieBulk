CLIENT_TEMPLATE_PATHS = [
    (
        r"/login/([a-zA-Z-0-9]+)",
        "files/desktop/login/login.html",
        None, {}
    ),
    (
        "/profile",
        "files/desktop/client/profile.html",
        None, {}
    ),
    (
        r"/forgot_password/([a-zA-Z-0-9]+)",
        "files/desktop/client/forgotpassword.html",
        None, {}
    ),
    (
        r"/reset_password/([a-zA-Z-0-9]+)/([a-zA-Z-0-9]+)",
        "files/desktop/client/resetpassword.html",
        None, {}
    ),
    (
        "/change-password",
        "files/desktop/client/changepassword.html",
        None, {}
    ),
    (
        r"/test/([a-zA-Z-0-9]+)", "test_apis.html", None, {}
    ),
    # (
    #     "/home", "files/desktop/home/home.html",
    #     None, {}
    # ),
    (
        "/home",
        "files/desktop/client/home/home.html",
        None, {}
    ),
    (
        "/dashboard",
        "files/desktop/client/client-home/client-home.html",
        None, {}
    ),
    # client admin
    (
        "/service-provider",
        "files/desktop/client/service-provider/serviceprovider.html",
        None, {}
    ),
    (
        "/client-user-privilege",
        "files/desktop/client/client-user-privilege/clientuserprivilege.html",
        None, {}
    ),
    (
        "/client-user-master",
        "files/desktop/client/client-user-master/clientusermaster.html",
        None, {}
    ),
    (
        "/settings",
        "files/desktop/client/settings/settings.html",
        None, {}
    ),
    (
        "/unit-closure",
        "files/desktop/client/unit-closure/unitclosure.html",
        None, {}
    ),
    (
        "/reminders",
        "files/desktop/client/reminders/reminders.html",
        None, {}
    ),
    (
        "/escalations",
        "files/desktop/client/escalations/escalations.html",
        None, {}
    ),
    # reports
    (
        "/compliance",
        "files/desktop/client/audit-trail/audittrail.html",
        None, {}
    ),
    (
        "/audit-trail",
        "files/desktop/client/audit-trail/audittrail.html",
        None, {}
    ),
    (
        "/unit-wise-compliance",
        "files/desktop/client/unit-wise-compliance/unitwisecompliance.html",
        None, {}
    ),
    (
        "/assignee-wise-compliance",
        "files/desktop/client/assignee-wise-compliance/assigneewisecompliance.html",
        None, {}
    ),
    (
        "/service-provider-wise-compliance",
        "files/desktop/client/service-provider-wise-compliance/serviceproviderwisecompliance.html",
        None, {}
    ),
    (
        "/compliance-details",
        "files/desktop/client/compliance-details/compliancedetails.html",
        None, {}
    ),
    (
        "/risk-report",
        "files/desktop/client/risk-report/riskreport.html",
        None, {}
    ),
    (
        "/statutory-notifications-list",
        "files/desktop/client/statutory-notifications-list-report/statutorynotificationslistreport.html",
        None, {}
    ),
    (
        "/reassigned-history",
        "files/desktop/client/reassigned-history-report/reassignedhistoryreport.html",
        None, {}
    ),
    (
        "/compliance-task-applicability-status",
        "files/desktop/client/compliance-task-applicability-report/compliancetaskapplicabilityreport.html",
        None, {}
    ),
    (
        "/login-trace",
        "files/desktop/client/login-trace/logintrace.html",
        None, {}
    ),
    (
        "/statutory-settings",
        "files/desktop/client/statutory-settings/statutorysettings.html",
        None, {}
    ),
    (
        "/assign-compliance",
        "files/desktop/client/assign-compliance/assigncompliance.html",
        None, {}
    ),
    (
        "/notifications",
        "files/desktop/client/notifications/notifications.html",
        None, {}
    ),
    (
        "/compliance-activity-report",
        "files/desktop/client/compliance-activity-report/complianceactivityreport.html",
        None, {}
    ),
    (
        "/unit-details",
        "files/desktop/client/unit-details-report/unitdetailsreport.html",
        None, {}
    ),
    (
        "/compliance-task-details",
        "files/desktop/client/compliance-task-details/compliancetaskdetails.html",
        None, {}
    ),
    (
        "/compliance-approval",
        "files/desktop/client/compliance-approval/complianceapproval.html",
        None, {}
    ),
    (
        "/completed-tasks-current-year",
        "files/desktop/client/completed-tasks-current-year/completedtaskscurrentyear.html",
        None, {}
    ),
    (
        "/on-occurrence-compliances",
        "files/desktop/client/on-occurrence-compliances/onoccurrencecompliances.html",
        None, {}
    ),
    (
        "/reassign-compliance",
        "files/desktop/client/reassign-compliance/reassigncompliance.html",
        None, {}
    ),
]

TEMPLATE_PATHS = [
    (
        "/knowledge/login",
        "files/knowledge/login/login.html",
        None, {}
    ),
    (
        "/knowledge/forgot-password",
        "files/knowledge/forgot-password/forgot-password.html",
        None, {}
    ),
    (
        "/knowledge/reset-password/<code>",
        "files/knowledge/resetpassword.html",
        None, {}
    ),

    ("/knowledge/test", "test_apis.html", None, {}),
    ("/knowledge/home", "files/knowledge/home/home.html", None, {}),
    (
        "/knowledge/profile",
        "files/knowledge/profile/profile.html",
        None, {}
    ),
    (
        "/knowledge/change-password",
        "files/knowledge/change-password/change-password.html",
        None, {}
    ),
    # IT Admin Master
    (
        "/knowledge/domain-master",
        "files/knowledge/domain-master/domain-master.html",
        None, {}
    ),
    (
        "/knowledge/country-master",
        "files/knowledge/country-master/country-master.html",
        None, {}
    ),
    (
        "/knowledge/user-privileges",
        "files/knowledge/user-privileges/user-privileges.html",
        None, {}
    ),
    (
        "/knowledge/user-management",
        "files/knowledge/user-management/user-management.html",
        None, {}
    ),
    (
        "/knowledge/validity-date-settings",
        "files/knowledge/validity-date-settings/settings.html",
        None, {}
    ),
    # knowledge manager transaction
    (
        "/knowledge/approve-statutory-mapping",
        "files/knowledge/approve-statutory-mapping/approve-statutory-mapping.html",
        None, {}
    ),
    # knowledge user master
    (
        "/knowledge/geography-master",
        "files/knowledge/geography-master/geography-master.html",
        None, {}
    ),
    (
        "/knowledge/geography-level-master",
        "files/knowledge/geography-level-master/geography-level-master.html",
        None, {}
    ),
    (
        "/knowledge/organization",
        "files/knowledge/organization/organization-master.html",
        None, {}
    ),
    (
        "/knowledge/statutory-nature",
        "files/knowledge/statutory-nature/statutory-nature.html",
        None, {}
    ),
    (
        "/knowledge/statutory-level-master",
        "files/knowledge/statutory-level-master/statutory-level-master.html",
        None, {}
    ),
    # knowledge user Transaction
    (
        "/knowledge/statutory-mapping",
        "files/knowledge/statutory-mapping/statutory-mapping-list.html",
        None, {}
    ),
    (
        "/knowledge/approve-assigned-statutory",
        "files/knowledge/approve-assigned-statutory/approve_assigned_statutory.html",
        None, {}
    ),
    # knowledge Reports
    (
        "/knowledge/statutory-mapping-report",
        "files/knowledge/statutory-mapping-report/statutory-mapping-report.html",
        None, {}
    ),
    (
        "/knowledge/client-agreement-master-report",
        "files/knowledge/client-agreement-master-report/client-agreement-master-report.html",
        None, {}
    ),
    (
        "/knowledge/country-report",
        "files/knowledge/country-report/country-report.html",
        None, {}
    ),
    (
        "/knowledge/domain-report",
        "files/knowledge/domain-report/domain-report.html",
        None, {}
    ),
    (
        "/knowledge/geography-report",
        "files/knowledge/geography-report/geography-report.html",
        None, {}
    ),
    (
        "/knowledge/organization-report",
        "files/knowledge/organization-report/organization-report.html",
        None, {}
    ),
    (
        "/knowledge/statutory-nature-report",
        "files/knowledge/statutory-nature-report/statutory-nature-report.html",
        None, {}
    ),
    # Techno Manager master
    (
        "/knowledge/client-master",
        "files/knowledge/client-master/client-master.html",
        None, {}
    ),
    (
        "/knowledge/client-master-approval",
        "files/knowledge/approve-client-group/approve-client-group.html",
        None, {}
    ),
    (
        "/knowledge/assign-legal-entity",
        "files/knowledge/assign-legal-entity/assign-legal-entity.html",
        None, {}
    ),
    (
        "/knowledge/legal-entity-closure",
        "files/knowledge/legal-entity-closure/legal-entity-closure.html",
        None, {}
    ),
    # Techno user master
    (
        "/knowledge/client-unit",
        "files/knowledge/client-unit/client_unit.html",
        None, {}
    ),
    (
        "/knowledge/client-unit-approval",
        "files/knowledge/client-unit-approval/client-unit-approval.html",
        None, {}
    ),
    (
        "/knowledge/unit-closure",
        "files/knowledge/unit-closure/unitclosure.html",
        None, {}
    ),
    (
        "/knowledge/client-profile",
        "files/knowledge/client-profile/clientprofile.html",
        None, {}
    ),
    # Techno User Transaction
    (
        "/knowledge/assign-statutory",
        "files/knowledge/assign-statutory/assign-statutory.html",
        None, {}
    ),
    # Techno reports
    (
        "/knowledge/client-unit-details",
        "files/knowledge/client-unit-details/client-unit-details.html",
        None, {}
    ),
    (
        "/knowledge/domain-agreement-master-report",
        "files/knowledge/domain-agreement-master-report/domain-agreement-master-report.html",
        None, {}
    ),
    (
        "/knowledge/statutory-notifications-list",
        "files/knowledge/statutory-notifications-list/statutory-notifications-list.html",
        None, {}
    ),
    (
        "/knowledge/assigned-statutory-report",
        "files/knowledge/assigned-statutory-report/assignedstatutoryreport.html",
        None, {}
    ),
    (
        "/knowledge/compliance-task-list",
        "files/knowledge/compliance-task-list/compliancetasklist.html",
        None, {}
    ),
    (
        "/knowledge/user-mapping-report",
        "files/knowledge/user-mapping-report/user-mapping-report.html",
        None, {}
    ),
    (
        "/knowledge/statutory-setting-report",
        "files/knowledge/statutory-setting-report/statutory-setting-report.html",
        None, {}
    ),
    (
        "/knowledge/group-admin-registration-email-report",
        "files/knowledge/group-admin-registration-email-report/group-admin-registration-email-report.html",
        None, {}
    ),
    (
        "/knowledge/reassign-user-report",
        "files/knowledge/reassign-user-report/reassign-user-report.html",
        None, {}
    ),
    # audit trial
    (
        "/knowledge/audit-trail-login-trace",
        "files/knowledge/audit-trail-login-trace/audit-trail-login-trace.html",
        None, {}
    ),
    # Console Admin
    (
        "/knowledge/configure-db-server",
        "files/knowledge/configure-db-server/configure-db-server.html",
        None, {}
    ),
    (
        "/knowledge/configure-client-server",
        "files/knowledge/configure-client-server/configure-client-server.html",
        None, {}
    ),
    (
        "/knowledge/allocate-db-env",
        "files/knowledge/allocate-db-env/allocate-db-env.html",
        None, {}
    ),
    (
        "/knowledge/auto-deletion",
        "files/knowledge/auto-deletion/auto-deletion.html",
        None, {}
    ),
    (
        "/knowledge/configure-file-storage",
        "files/knowledge/configure-file-storage/configure-file-storage.html",
        None, {}
    ),
    (
        "/knowledge/user-mapping",
        "files/knowledge/user-mapping/user-mapping.html",
        None, {}
    ),
    (
        "/knowledge/assign-client-unit",
        "files/knowledge/assign-client-unit/assign-client-unit.html",
        None, {}
    ),
    (
        "/knowledge/reassign-user-account",
        "files/knowledge/reassign-user-account/reassign-user-account.html",
        None, {}
    ),
    (
        "/knowledge/userregistration/<code>",
        "files/knowledge/login/create-login-details.html",
        None, {}
    ),
    (
        "/knowledge/group-admin-registration-email",
        "files/knowledge/group-admin-registration-email/group-admin-registration-email.html",
        None, {}
    ),
    (
        "/knowledge/messages",
        "files/knowledge/messages/messages.html",
        None, {}
    ),
    (
        "/knowledge/statutory-notifications",
        "files/knowledge/statutorynotifications/statutorynotifications.html",
        None, {}
    )
]
