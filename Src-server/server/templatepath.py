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
        r"/knowledge/reset-password/([a-zA-Z-0-9]+)",
        "files/knowledge/resetpassword.html",
        None, {}
    ),

    ("/knowledge/test", "test_apis.html", None, {}),
    ("/knowledge/home", "files/knowledge/home/home.html", None, {}),
    (
        "/knowledge/profile",
        "files/knowledge/profile.html",
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
        "files/knowledge/approve-statutory-mapping/approvestatutorymapping.html",
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
        "files/knowledge/statutory-mapping/statutorymapping.html",
        None, {}
    ),
    # knowledge Reports
    (
        "/knowledge/statutory-mapping-report",
        "files/knowledge/statutory-mapping-report/statutorymappingreport.html",
        None, {}
    ),
    (
        "/knowledge/country-report",
        "files/knowledge/knowledge-master-report/country-master-report/countrymasterreport.html",
        None, {}
    ),
    (
        "/knowledge/domain-report",
        "files/knowledge/knowledge-master-report/domain-master-report/domainmasterreport.html",
        None, {}
    ),
    (
        "/knowledge/geography-report",
        "files/knowledge/knowledge-master-report/geography-master-report/geographymasterreport.html",
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
        "files/knowledge/client-master/clientmaster-new.html",
        None, {}
    ),
    (
        "/knowledge/client-master-approval",
        "files/knowledge/client-master-approval/clientmasterapproval.html",
        None, {}
    ),
    (
        "/knowledge/assign-legal-entity",
        "files/knowledge/assign-legal-entity/assignlegalentity.html",
        None, {}
    ),
    # Techno user master
    (
        "/knowledge/client-unit",
        "files/knowledge/client-unit/clientunit.html",
        None, {}
    ),
    (
        "/knowledge/client-unit-approval",
        "files/knowledge/client-unit-approval/clientunitapproval.html",
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
        "files/knowledge/assign-statutory/assignstatutory.html",
        None, {}
    ),
    # Techno reports
    (
        "/knowledge/client-details-report",
        "files/knowledge/client-details-report/clientdetailsreport.html",
        None, {}
    ),
    (
        "/knowledge/statutory-notifications-list",
        "files/knowledge/statutory-notifications-list-report/statutorynotificationslistreport.html",
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
        "files/knowledge/user-mapping-report/usermappingreport.html",
        None, {}
    ),
    # audit trial
    (
        "/knowledge/audit-trail",
        "files/knowledge/audit-trail/audittrail.html",
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
        r"/knowledge/userregistration/([a-zA-Z-0-9]+)",
        "files/common/html/CreateLoginDetails.html",
        None, {}
    )
]
