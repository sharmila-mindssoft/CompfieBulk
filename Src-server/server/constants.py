import os
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
        "files/desktop/knowledge/login.html",
        None, {}
    ),
    (
        "/knowledge/forgot-password",
        "files/desktop/knowledge/forgotpassword.html",
        None, {}
    ),
    (
        r"/knowledge/reset-password/([a-zA-Z-0-9]+)",
        "files/desktop/knowledge/resetpassword.html",
        None, {}
    ),
    # (
    #     "/knowledge/login",
    #     "files/desktop/login/login.html",
    #     "files/mobile/login/login.html", {}
    # ),
    ("/knowledge/test", "test_apis.html", None, {}),
    ("/knowledge/home", "files/desktop/knowledge/home/home.html", None, {}),
    # (
    #     "/knowledge/custom-controls",
    #     "files/desktop/custom-controls/custom-controls.html",
    #     None, {}
    # ),
    # common
    (
        "/knowledge/profile",
        "files/desktop/knowledge/profile.html",
        None, {}
    ),
    (
        "/knowledge/change-password",
        "files/desktop/knowledge/changepassword.html",
        None, {}
    ),
    # IT Admin Master
    (
        "/knowledge/domain-master",
        "files/desktop/knowledge/domain-master/domainmaster.html",
        None, {}
    ),
    (
        "/knowledge/country-master",
        "files/desktop/knowledge/country-master/countrymaster.html",
        None, {}
    ),
    (
        "/knowledge/user-group-master",
        "files/desktop/knowledge/user-group-master/usergroupmaster.html",
        None, {}
    ),
    (
        "/knowledge/user-master",
        "files/desktop/knowledge/user-master/usermaster.html",
        None, {}
    ),
    # knowledge manager transaction
    (
        "/knowledge/approve-statutory-mapping",
        "files/desktop/knowledge/approve-statutory-mapping/approvestatutorymapping.html",
        None, {}
    ),
    # knowledge user master
    (
        "/knowledge/geography-master",
        "files/desktop/knowledge/geography-master/geographymaster.html",
        None, {}
    ),
    (
        "/knowledge/geography-level-master",
        "files/desktop/knowledge/geography-level-master/geographylevelmaster.html",
        None, {}
    ),
    (
        "/knowledge/industry-master",
        "files/desktop/knowledge/industry-master/industrymaster.html",
        None, {}
    ),
    (
        "/knowledge/statutory-nature-master",
        "files/desktop/knowledge/statutory-nature-master/statutorynaturemaster.html",
        None, {}
    ),
    (
        "/knowledge/statutory-level-master",
        "files/desktop/knowledge/statutory-level-master/statutorylevelmaster.html",
        None, {}
    ),
    # knowledge user Transaction
    (
        "/knowledge/statutory-mapping",
        "files/desktop/knowledge/statutory-mapping/statutorymapping.html",
        None, {}
    ),
    # knowledge Reports
    (
        "/knowledge/statutory-mapping-report",
        "files/desktop/knowledge/statutory-mapping-report/statutorymappingreport.html",
        None, {}
    ),
    (
        "/knowledge/country-report",
        "files/desktop/knowledge/knowledge-master-report/country-master-report/countrymasterreport.html",
        None, {}
    ),
    (
        "/knowledge/domain-report",
        "files/desktop/knowledge/knowledge-master-report/domain-master-report/domainmasterreport.html",
        None, {}
    ),
    (
        "/knowledge/geography-report",
        "files/desktop/knowledge/knowledge-master-report/geography-master-report/geographymasterreport.html",
        None, {}
    ),
    (
        "/knowledge/industry-report",
        "files/desktop/knowledge/knowledge-master-report/industry-master-report/industrymasterreport.html",
        None, {}
    ),
    (
        "/knowledge/statutory-nature-report",
        "files/desktop/knowledge/knowledge-master-report/statutory-nature-master-report/statutorynaturemasterreport.html",
        None, {}
    ),
    # Techno Manager master
    (
        "/knowledge/client-master",
        "files/desktop/knowledge/client-master/clientmaster.html",
        None, {}
    ),
    # Techno user master
    (
        "/knowledge/client-unit",
        "files/desktop/knowledge/client-unit/clientunit.html",
        None, {}
    ),
    (
        "/knowledge/unit-closure",
        "files/desktop/knowledge/unit-closure/unitclosure.html",
        None, {}
    ),
    (
        "/knowledge/client-profile",
        "files/desktop/knowledge/client-profile/clientprofile.html",
        None, {}
    ),
    # Techno User Transaction
    (
        "/knowledge/assign-statutory",
        "files/desktop/knowledge/assign-statutory/assignstatutory.html",
        None, {}
    ),
    # Techno reports
    (
        "/knowledge/client-details-report",
        "files/desktop/knowledge/client-details-report/clientdetailsreport.html",
        None, {}
    ),
    (
        "/knowledge/statutory-notifications-list",
        "files/desktop/knowledge/statutory-notifications-list-report/statutorynotificationslistreport.html",
        None, {}
    ),
    (
        "/knowledge/assigned-statutory-report",
        "files/desktop/knowledge/assigned-statutory-report/assignedstatutoryreport.html",
        None, {}
    ),
    (
        "/knowledge/compliance-task-list",
        "files/desktop/knowledge/compliance-task-list/compliancetasklist.html",
        None, {}
    ),
    # audit trial
    (
        "/knowledge/audit-trail",
        "files/desktop/knowledge/audit-trail/audittrail.html",
        None, {}
    ),

]
ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
IS_DEVELOPMENT = True
VERSION = 1

KNOWLEDGE_DB_HOST = "localhost"
KNOWLEDGE_DB_PORT = 3306
KNOWLEDGE_DB_USERNAME = "root"
KNOWLEDGE_DB_PASSWORD = "123456"
KNOWLEDGE_DATABASE_NAME = "compfie_knowledge"

CLIENT_URL = "http://localhost:8082/"
KNOWLEDGE_URL = "http://localhost:8080/knowledge"
