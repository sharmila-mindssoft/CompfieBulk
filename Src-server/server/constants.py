CLIENT_TEMPLATE_PATHS = [
    (
        r"/login/([a-zA-Z-0-9]+)",
        "files/desktop/login/login.html",
        "files/mobile/login/login.html", {}
    ),
    (
        r"/forgot_password/([a-zA-Z-0-9]+)",
        "files/desktop/ForgotPassword/ForgotPassword.html",
        "", {}
    ),
    (
        r"/reset_password/([a-zA-Z-0-9]+)",
        "files/desktop/ForgotPassword/resetpassword.html",
        "", {}
    ),
    (
        "/change-password",
        "files/desktop/change-password/changepassword.html",
        None, {}
    ),
    (
        "/test", "test_apis.html", "", {}
    ),
    (
        "/home", "files/desktop/home/home.html",
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
]

TEMPLATE_PATHS = [
    (
        "/login", "files/desktop/login/login.html",
        "files/mobile/login/login.html", {}
    ),
    (
        "/login",
        "files/desktop/login/login.html",
        "files/mobile/login/login.html", {}
    ),
    ("/test", "test_apis.html", "", {}),
    ("/home", "files/desktop/home/home.html", None, {}),
    (
        "/custom-controls",
        "files/desktop/custom-controls/custom-controls.html",
        None, {}
    ),
    # common
    (
        "/profile",
        "files/desktop/profile/profile.html",
        None, {}
    ),
    (
        "/change-password",
        "files/desktop/change-password/changepassword.html",
        None, {}
    ),
    # IT Admin Master
    (
        "/domain-master",
        "files/desktop/domain-master/domainmaster.html",
        None, {}
    ),
    (
        "/country-master",
        "files/desktop/country-master/countrymaster.html",
        None, {}
    ),
    (
        "/user-group-master",
        "files/desktop/user-group-master/usergroupmaster.html",
        None, {}
    ),
    (
        "/user-master",
        "files/desktop/user-master/usermaster.html",
        None, {}
    ),
    # knowledge manager transaction
    (
        "/approve-statutory-mapping",
        "files/desktop/approve-statutory-mapping/approvestatutorymapping.html",
        None, {}
    ),
    # knowledge user master
    (
        "/geography-master",
        "files/desktop/geography-master/geographymaster.html",
        None, {}
    ),
    (
        "/geography-level-master",
        "files/desktop/geography-level-master/geographylevelmaster.html",
        None, {}
    ),
    (
        "/industry-master",
        "files/desktop/industry-master/industrymaster.html",
        None, {}
    ),
    (
        "/statutory-nature-master",
        "files/desktop/statutory-nature-master/statutorynaturemaster.html",
        None, {}
    ),
    (
        "/statutory-level-master",
        "files/desktop/statutory-level-master/statutorylevelmaster.html",
        None, {}
    ),
    # knowledge user Transaction
    (
        "/statutory-mapping",
        "files/desktop/statutory-mapping/statutorymapping.html",
        None, {}
    ),
    # knowledge Reports
    (
        "/statutory-mapping-report",
        "files/desktop/statutory-mapping-report/statutorymappingreport.html",
        None, {}
    ),
    (
        "/country-report",
        "files/desktop/knowledge-master-report/country-master-report/countrymasterreport.html",
        None, {}
    ),
    (
        "/domain-report",
        "files/desktop/knowledge-master-report/domain-master-report/domainmasterreport.html",
        None, {}
    ),
    (
        "/geography-report",
        "files/desktop/knowledge-master-report/geography-master-report/geographymasterreport.html",
        None, {}
    ),
    (
        "/industry-report",
        "files/desktop/knowledge-master-report/industry-master-report/industrymasterreport.html",
        None, {}
    ),
    (
        "/statutory-nature-report",
        "files/desktop/knowledge-master-report/statutory-nature-master-report/statutorynaturemasterreport.html",
        None, {}
    ),
    # Techno Manager master
    (
        "/client-master", "files/desktop/client-master/clientmaster.html",
        None, {}
    ),
    # Techno user master
    (
        "/client-unit", "files/desktop/client-unit/clientunit.html",
        None, {}
    ),
    (
        "/unit-closure",
        "files/desktop/unit-closure/unitclosure.html",
        None, {}
    ),
    (
        "/client-profile", "files/desktop/client-profile/clientprofile.html",
        None, {}
    ),
    # Techno User Transaction
    (
        "/assign-statutory",
        "files/desktop/assign-statutory/assignstatutory.html",
        None, {}
    ),
    # Techno reports
    (
        "/client-details-report",
        "files/desktop/client-details-report/clientdetailsreport.html",
        None, {}
    ),
    (
        "/statutory-notifications-list",
        "files/desktop/statutory-notifications-list-report/statutorynotificationslistreport.html",
        None, {}
    ),
    (
        "/assigned-statutory-report",
        "files/desktop/assigned-statutory-report/assignedstatutoryreport.html",
        None, {}
    ),
    (
        "/compliance-task-list",
        "files/desktop/compliance-task-list/compliancetasklist.html",
        None, {}
    ),
    # audit trial
    (
        "/audit-trail", "files/desktop/audit-trail/audittrail.html",
        None, {}
    ),

]
