import os
import mimetypes
import tornado.web
from tornado.web import StaticFileHandler
import tornado.ioloop
import jinja2
from aparajitha.server.constants import ROOT_PATH, HTTP_PORT
from user_agents import parse
import json
from aparajitha.server import countries as countriesdb 
from collections import OrderedDict

from knowledge import handler as knowledge_handler
from client import handler as client_admin_handler
from admin import handler as admin_handler
from techno import handler as techno_handler

TEMPLATE_PATHS = [
    ("/", "files/desktop/Login/Login.html", "files/mobile/Login/Login.html", {}),
    ("/index", "files/desktop/Login/index.html", "files/mobile/index/index.html", {}),
    ("/login", "files/desktop/Login/Login.html",
        None, {}),
    ("/applicability/create", "files/desktop/Applicability_master/ApplicabilityMaster.html",
        None, {}),
    ("/test", "files/desktop/test.html",
        None, {}),
    ("/test1", "files/desktop/Home/test.html",
        None, {}),
    ("/applicability/list", "files/desktop/Applicability_master/ApplicabilityMasterList.html",
        None, {}),
    ("/district", "files/desktop/DistrictMaster/DistrictMaster.html",
        None, {}),
    ("/division/create", "files/desktop/DivisionMaster/DivisionMaster.html",
        None, {}),
    ("/division/list", "files/desktop/DivisionMaster/DivisionMasterList.html",
        None, {}),
    ("/domain/create", "files/desktop/DomainMaster/DomainMaster.html",
        None, {}),
    ("/domain/list", "files/desktop/DomainMaster/DomainMasterList.html",
        None, {}),
    ("/subdomain/create", "files/desktop/SubDomainMaster/SubDomainMaster.html",
        None, {}),
    ("/subdomain/list", "files/desktop/SubDomainMaster/SubDomainMasterList.html",
        None, {}),
    ("/group_company/create", "files/desktop/GroupCompanyMaster/GroupCompanyMaster.html",
        None, {}),
    ("/group_company/list", "files/desktop/GroupCompanyMaster/GroupCompanyMasterList.html",
        None, {}),
    ("/clientgroup/create", "files/desktop/ClientGroup/ClientGroup.html",
        None, {}),
    ("/clientgroup/list", "files/desktop/ClientGroup/ClientGroupList.html",
        None, {}),
    ("/industry_sector/create", "files/desktop/Industry_SectorMaster/Industry_SectorMaster.html",
        None, {}),
    ("/industry_sector/list", "files/desktop/Industry_SectorMaster/Industry_SectorMasterList.html",
        None, {}),
    ("/industry_sector/create", "files/desktop/Industry_SectorMaster/Industry_SectorMaster.html",
        None, {}),
    ("/industry_sector/list", "files/desktop/Industry_SectorMaster/Industry_SectorMasterList.html",
        None, {}),
    ("/industry/create", "files/desktop/Industry_Master/IndustryMaster.html",
        None, {}),
    ("/industry/list", "files/desktop/Industry_Master/IndustryMasterList.html",
        None, {}),
    ("/legal_entity/create", "files/desktop/LegalEntityMaster/LegalEntityMaster.html",
        None, {}),
    ("/legal_entity/list", "files/desktop/LegalEntityMaster/LegalEntityMasterList.html",
        None, {}),
    ("/province/create", "files/desktop/ProvinceMaster/ProvinceMaster.html",
        None, {}),
    ("/province/list", "files/desktop/ProvinceMaster/ProvinceMasterList.html",
        None, {}),
    ("/region/create", "files/desktop/RegionMaster/RegionMaster.html",
        None, {}),
    ("/region/list", "files/desktop/RegionMaster/RegionMasterList.html",
        None, {}),
    ("/state/create", "files/desktop/StateMaster/StateMaster.html",
        None, {}),
    ("/state/list", "files/desktop/StateMaster/StateMasterList.html",
        None, {}),
    ("/statutory/create", "files/desktop/StatutoryMaster/StatutoryMaster.html",
        None, {}),
    ("/statutory/list", "files/desktop/StatutoryMaster/StatutoryMasterList.html",
        None, {}),
    ("/unit_branch/create", "files/desktop/Unit_BranchMaster/Unit_BranchMaster.html",
        None, {}),
    ("/unit_branch/list", "files/desktop/Unit_BranchMaster/Unit_BranchMasterList.html",
        None, {}),
    ("/change_password", "files/desktop/ChangePassword/ChangePassword.html",
        None, {}),
    ("/home", "files/desktop/Home/ClientAdminHome/TaskStatusChart.html",
        None, {}),
    ("/home_escalations", "files/desktop/Home/ClientAdminHome/EscalationsChart.html",
        None, {}),
    ("/home_userwise", "files/desktop/Home/ClientAdminHome/UserwiseComplianceChart.html",
        None, {}),
    ("/home_ageingwise", "files/desktop/Home/ClientAdminHome/AgeingwiseCompliance.html",
        None, {}),
    ("/home_trend", "files/desktop/Home/ClientAdminHome/TrendChart.html",
        None, {}),
    ("/home_risk", "files/desktop/Home/ClientAdminHome/ComplianceRisk.html",
        None, {}),
    ("/service_provider", "files/desktop/Home/ServiceProviderHome.html",
        None, {}),
    ("/business_team", "files/desktop/Home/BusinessTeamHome.html",
        None, {}),
    ("/knowledge", "files/desktop/Home/KnowledgeHome.html",
        None, {}),
    ("/it", "files/desktop/Home/ITHome.html",
        None, {}),
    ("/techno", "files/desktop/Home/TechnoHome.html",
        None, {}),
    ("/profile", "files/desktop/Profile/Profile.html",
        None, {}),
    ("/profile_admin", "files/desktop/Profile/Profile_Admin.html",
        None, {}),
    ("/profile_knowledge_user", "files/desktop/Profile/Profile_Knowledge_User.html",
        None, {}),
    ("/profile_knowledge_manager", "files/desktop/Profile/Profile_Knowledge_Manager.html",
        None, {}),
    ("/profile_techno_manager", "files/desktop/Profile/Profile_Techno_Manager.html",
        None, {}),
    ("/profile_techno_user", "files/desktop/Profile/Profile_Techno_User.html",
        None, {}),
    ("/profile_client", "files/desktop/Profile/Profile_Client.html",
        None, {}),
    ("/profile_sp", "files/desktop/Profile/Profile_SP.html",
        None, {}),
    ("/user/create", "files/desktop/User/User.html",
        None, {}),
    ("/user/list", "files/desktop/User/UserList.html",
        None, {}),
    ("/userclient/create", "files/desktop/UserClient/UserClient.html",
        None, {}),
    ("/userclient/list", "files/desktop/UserClient/UserListClient.html",
        None, {}),
    ("/geography", "files/desktop/GeographyMaster/GeographyMaster.html",
        None, {}),
    ("/geography_singapore", "files/desktop/LocationMaster/GeographySingapore.html",
        None, {}),
    ("/geography_state", "files/desktop/LocationMaster/GeographyState.html",
        None, {}),
    ("/geography_municipal", "files/desktop/LocationMaster/GeographyMunicipal.html",
        None, {}),
    ("/geography_town", "files/desktop/LocationMaster/GeographyTown.html",
        None, {}),
    ("/geography_panchayat", "files/desktop/LocationMaster/GeographyPanchayat.html",
        None, {}),
    ("/manpower/create", "files/desktop/ManPower/ManPower.html",
        None, {}),
    ("/manpower/list", "files/desktop/ManPower/ManPowerList.html",
        None, {}),
    ("/prospective_client/create", "files/desktop/ProspectiveClientDetails/ProspectiveClientDetails.html",
        None, {}),
    ("/prospective_client/list", "files/desktop/ProspectiveClientDetails/ProspectiveClientDetailsList.html",
        None, {}),
	("/subtaskentry/create", "files/desktop/SubTaskEntry/SubTaskEntry.html",
        None, {}),
	("/subtaskentry/list", "files/desktop/SubTaskEntry/SubTaskEntryList.html",
        None, {}),
    ("/client_configuration/create", "files/desktop/ClientConfiguration/ClientConfiguration.html",
        None, {}),
    ("/client_configuration/list", "files/desktop/ClientConfiguration/ClientConfigurationList.html",
        None, {}),
    ("/configuration_approval", "files/desktop/ConfigurationApproval/ConfigurationApproval.html",
        None, {}),
    ("/requirement_approval", "files/desktop/RequirementApproval/RequirementApproval.html",
        None, {}),
    ("/prospectivemaster/list", "files/desktop/ProspectiveClientMaster/ProspectiveClientMaster.html",
        None, {}),
    ("/prospectivemaster/update", "files/desktop/ProspectiveClientMaster/ProspectiveClientMasterUpdate.html",
        None, {}),
	("/prospectivemaster/convert", "files/desktop/ProspectiveClientMaster/ProspectiveClientMasterConvert.html",
        None, {}),
    ("/define_req_conf/list", "files/desktop/DefineRequirement-Configuration/RequirementConfigurationList.html",
        None, {}),
    ("/define_req_conf/create", "files/desktop/DefineRequirement-Configuration/RequirementConfiguration.html",
        None, {}),
    ("/update_status", "files/desktop/UpdateStatus/UpdateStatusWithReason.html",
        None, {}),
    ("/assign_key_contact_client", "files/desktop/AssignKeyContact_Client/AssignKeyContact_Client.html",
        None, {}),
	("/assign_key_contact_bt", "files/desktop/AssignKeyContact_BT/AssignKeyContact.html",
        None, {}),
    ("/report/prospective_client_details", "files/desktop/ProspectiveClientDetailsReport/ProspectiveClientDetailsList.html",
        None, {}),
    ("/report/client_status_report", "files/desktop/ClientStatusReport/ClientStatusReport.html",
        None, {}),
    ("/report/client_requirement_report", "files/desktop/ClientRequirementReport/ClientRequirementReport.html",
        None, {}),
    ("/report/client", "files/desktop/ClientList/ClientList.html",
        None, {}),
    ("/client/list", "files/desktop/Client/ClientList.html",
        None, {}),
    ("/client/create", "files/desktop/Client/ClientMaster.html",
        None, {}),
    ("/report/service-provider", "files/desktop/ServiceProviderList/ServiceProviderList.html",
        None, {}),
    ("/service_provider/create", "files/desktop/ServiceProviderCreation/ServiceProviderCreation.html",
        None, {}),
    ("/service_provider/list", "files/desktop/ServiceProviderCreation/ServiceProviderList.html",
        None, {}),
    ("/approveservicemapping", "files/desktop/ApproveServiceMapping/ApproveServiceMapping.html",
        None, {}),
    ("/domainmapping", "files/desktop/DomainMapping/DomainMapping.html",
        None, {}),  
    ("/domainfinance", "files/desktop/DomainMapping/DomainMappingFinance.html",
        None, {}),
    ("/domainindustry", "files/desktop/DomainMapping/DomainMappingIndustrial.html",
        None, {}),
    ("/domainlabour", "files/desktop/DomainMapping/DomainMappingLabour.html",
        None, {}),
    ("/industrymapping", "files/desktop/IndustryMapping/IndustryMapping.html", 
        None, {}),
    ("/taskactivity/list", "files/desktop/Task-ActivityData/Task-ActivityDataList.html",
        None, {}),
    ("/taskactivity/create", "files/desktop/Task-ActivityData/Task-ActivityData.html",
        None, {}),
    ("/taskapproval", "files/desktop/TaskApproval/TaskApproval.html",
        None, {}),
    ("/audittrail", "files/desktop/AuditTrail/AuditTrail.html",
        None, {}),
    ("/audittrail_it", "files/desktop/AuditTrail/AuditTrailIT.html",
        None, {}),
    ("/audittrail_techno", "files/desktop/AuditTrail/AuditTrailTechno.html",
        None, {}),
    ("/audittrail_business", "files/desktop/AuditTrail/AuditTrailBusiness.html",
        None, {}),
    ("/audittrail_client", "files/desktop/AuditTrail/AuditTrailClient.html",
        None, {}),
    ("/audittrail_sp", "files/desktop/AuditTrail/AuditTrailsp.html",
        None, {}),
    ("/taskactivityreport", "files/desktop/Task-ActivityDataReport/Task-ActivityDataReport.html",
        None, {}),
    ("/viewservicemapping", "files/desktop/ViewServiceMapping/ViewServiceMapping.html",
        None, {}),
    ("/subtasklevel/list", "files/desktop/SubTaskLevelCreations/SubTaskLevelList.html",
        None, {}),
    ("/subtasklevel/create", "files/desktop/SubTaskLevelCreations/SubTaskLevel.html",
        None, {}),
    ("/assignservicemapping", "files/desktop/AssignServiceMapping/AssignServiceMapping.html",
        None, {}),
    ("/assignservicemapping_bajaj", "files/desktop/AssignServiceMapping/AssignServiceMappingBajaj.html",
        None, {}),
    ("/assignservicemapping_prg", "files/desktop/AssignServiceMapping/AssignServiceMappingPRG.html",
        None, {}),
    ("/assignservicemapping/list", "files/desktop/AssignServiceMapping/AssignServiceMappingList.html",
        None, {}),
     ("/assignservicemapping/editsubmit", "files/desktop/AssignServiceMapping/AssignServiceMappingSubmit.html",
        None, {}),
    ("/tasklist_techno", "files/desktop/TaskList_Technos/TaskList_Techno.html",
        None, {}),
    ("/servicemappinglist", "files/desktop/ServiceMappingList/ServiceMappingList.html",
        None, {}),
    ("/statutorymapping", "files/desktop/StatutoryMapping/StatutoryMapping.html",
        None, {}),
    ("/statutorymapping/list", "files/desktop/StatutoryMapping/StatutoryMappingList.html",
        None, {}),
	("/statutorymapping/approve", "files/desktop/ApproveStatutoryMapping/ApproveStatutoryMapping.html",
        None, {}),
	("/assignedstatutory/approve", "files/desktop/ApproveAssignedStatutory/ApproveAssignedStatutory.html",
        None, {}),
    ("/statutoryindustrial", "files/desktop/StatutoryMapping/StatutoryMappingIndustrial.html",
        None, {}),
    ("/statutoryfinance", "files/desktop/StatutoryMapping/StatutoryMappingFinance.html",
        None, {}),   
    ("/servicemapping/create", "files/desktop/ServiceMapping/ServiceMapping.html",
        None, {}),
    ("/servicemapping/create_insol", "files/desktop/ServiceMapping/ServiceMappingInsol.html",
        None, {}),
    ("/servicemapping/create_tax", "files/desktop/ServiceMapping/ServiceMappingTax.html",
        None, {}),
    ("/servicemapping/create_trust", "files/desktop/ServiceMapping/ServiceMappingTrust.html",
        None, {}),
    ("/servicemapping/create_admin", "files/desktop/ServiceMapping/ServiceMappingAdmin.html",
        None, {}),
    ("/servicemapping/create_wage", "files/desktop/ServiceMapping/ServiceMappingWage.html",
        None, {}),
    ("/servicemapping/list", "files/desktop/ServiceMapping/ServiceMappinglist.html",
        None, {}),
    ("/user_group_privileges/create", "files/desktop/UserGroupPrivileges/UserGroupPrivileges.html",
        None, {}),
    ("/user_group_privileges/list", "files/desktop/UserGroupPrivileges/UserGroupPrivilegesList.html",
        None, {}),
    ("/dataarchive", "files/desktop/DataArchive/DataArchive.html",
        None, {}),
    ("/task_subtask_request", "files/desktop/SubTaskRequest/SubTaskRequest.html",
        None, {}),
    ("/subtask_level_request", "files/desktop/SubTaskLevelRequest/SubTaskLevelRequest.html",
        None, {}),
    ("/assignsubtasklevel", "files/desktop/AssignSubTaskLevel/AssignSubTaskLevel.html",
        None, {}),
    ("/taskverification", "files/desktop/TaskVerification/TaskVerification.html",
        None, {}),
    ("/taskassignment", "files/desktop/TaskAssignment/TaskAssignment.html",
            None, {}),
    ("/taskassignment1", "files/desktop/TaskAssignment/TaskAssignmentUL2.html",
            None, {}),   
    ("/taskassignment2", "files/desktop/TaskAssignment/TaskAssignmentUL3.html",
            None, {}),
    ("/taskassignment3", "files/desktop/TaskAssignment/TaskAssignmentUL1.html",
            None, {}),          
    ("/reassigntask", "files/desktop/ReAssignTask/ReAssignTask.html",
            None, {}), 
    ("/reassigntask/edit", "files/desktop/ReAssignTask/ReAssignTaskForm.html",
            None, {}), 
    ("/assignduedate", "files/desktop/AssignDueDate/AssignDueDate.html",
            None, {}),
    ("/inhouseprivileges/create", "files/desktop/InhousePrivileges/InhousePrivileges.html",
            None, {}),         
    ("/inhouseprivileges/list", "files/desktop/InhousePrivileges/InhousePrivilegesList.html",
            None, {}),     
    ("/assignkeycontact", "files/desktop/AssignKeyContact/AssignKeyContact.html",
            None, {}),
    ("/assignkeycontact_clientsettings", "files/desktop/AssignKeyContact_Client/AssignKeyContact_Settings.html",
            None, {}),
    ("/settings", "files/desktop/Settings/Settings.html",
            None, {}),  
    ("/managetasks", "files/desktop/ManageTask/ManageTaskDetails.html",
            None, {}), 
    ("/dataarchive-sp", "files/desktop/DataArchive-sp/DataArchive-sp.html",
            None, {}), 
    ("/taskassignmentlist", "files/desktop/TaskAssignmentList/TaskAssignmentList.html",
            None, {}), 
    ("/userwisetaskreport", "files/desktop/UserwiseTaskDetailsList/UserwiseTaskDetailsList.html",
            None, {}),
    ("/userwisetaskreport/subtask", "files/desktop/UserwiseTaskDetailsList/UserwiseSubTaskDetailsList.html",
            None, {}),
	 ("/activityreport", "files/desktop/ActivityReport/ActivityReport.html",
            None, {}),
    ("/assignmanpower", "files/desktop/AssignManpower/AssignManpower.html",
            None, {}), 
    ("/reassignmanpower", "files/desktop/ReAssignManpower/ReAssignManpower.html",
            None, {}), 
    ("/taskstatusreport", "files/desktop/TaskStatusReport/TaskStatusReport.html",
            None, {}),
    ("/taskdetails/list", "files/desktop/TaskDetails/TaskDetailsList.html",
            None, {}),
    ("/taskdetails/subtask", "files/desktop/TaskDetails/SubTaskDetailsList.html",
            None, {}),
    ("/forgotpassword", "files/desktop/ForgotPassword/ForgotPassword.html",
            None, {}),
    ("/resetpassword", "files/desktop/ForgotPassword/resetpassword.html",
            None, {}),
    ("/subtasklist", "files/desktop/SubTaskList/SubTaskList.html",
            None, {}),
    ("/dataarchive-client", "files/desktop/DataArchive-Client/DataArchive-Client.html",
            None, {}),
    ("/subtaskrecommendation", "files/desktop/SubTaskRecommendation/SubTaskRecommendation.html",
            None, {}),
    ("/assignservicemappingrecommendation", "files/desktop/AssignServiceMappingRecommendation/AssignServiceMappingRecommendation.html",
            None, {}),
	("/index1", "files/desktop/UserCategory/UserCategoryList.html",
            None, {}),
	("/index1/create", "files/desktop/UserCategory/UserCategory.html",
            None, {}),
	("/user_category_approve/list", "files/desktop/UserCategory_Approve/UserCategoryList.html",
            None, {}),
	("/user_category_approve/update", "files/desktop/UserCategory_Approve/UserCategory_Approve.html",
            None, {}),
    ("/bmanager_home", "files/desktop/Home/BusinessTeamManagerHome.html",
            None, {}),
    ("/sales_home", "files/desktop/Home/SalesExecutiveHome.html",
            None, {}),
    ("/report/clients", "files/desktop/Client/ClientReport.html",
            None, {}),
    ("/approveassignedservicemapping", "files/desktop/ApproveAssignedServiceMapping/ApproveAssignedServiceMapping.html",
            None, {}),
    ("/knowledge/user/home", "files/desktop/Home/KnowledgeUserHome.html",
            None, {}),
    ("/techno/user/home", "files/desktop/Home/TechnoUserHome.html",
            None, {}),
    ("/it/user/home", "files/desktop/Home/ITUserHome.html",
            None, {}),
    ("/service_provider/user/home", "files/desktop/Home/ServiceProviderUserHome.html",
            None, {}),
    ("/inhouse/home", "files/desktop/Home/InhouseHome.html",
            None, {}),
    ("/taskmapping", "files/desktop/TaskMapping/TaskMapping.html",
            None, {}),
    ("/taskmappingreturns", "files/desktop/TaskMapping/TaskMappingReturns.html",
            None, {}),
    ("/approvetaskmapping", "files/desktop/ApproveTaskMapping/ApproveTaskMapping.html",
            None, {}),
    ("/home/in_progress", "files/desktop/Home/Group-Inprogress.html",
            None, {}),
    ("/home/completed", "files/desktop/Home/Group-Completed.html",
            None, {}),
    ("/home/delayed", "files/desktop/Home/Group-Delayed.html",
            None, {}),
    ("/home/unassigned", "files/desktop/Home/Group-Unassigned.html",
            None, {}),
    ("/home/pending", "files/desktop/Home/Group-Pending.html",
            None, {}),
    ("/home/company_inprogress", "files/desktop/Home/Company-Inprogress.html",
            None, {}),
    ("/home/company_pending", "files/desktop/Home/Company-Pending.html",
            None, {}),
    ("/home/company_completed", "files/desktop/Home/Company-Completed.html",
            None, {}),
	("/home/drill_group_completed", "files/desktop/Home/Drill-Group-Completed.html",
            None, {}),
	("/home/drill_entity_completed", "files/desktop/Home/Drill-Entity-Completed.html",
            None, {}),
	("/home/drill_division_completed", "files/desktop/Home/Drill-Division-Completed.html",
            None, {}),
	("/home/drill_unit_completed", "files/desktop/Home/Drill-Unit-Completed.html",
            None, {}),
    ("/home/unit_inprogress", "files/desktop/Home/Unit-Inprogress.html",
            None, {}),
    ("/home/unit_pending", "files/desktop/Home/Unit-Pending.html",
            None, {}),
    ("/home/unit_completed", "files/desktop/Home/Unit-Completed.html",
            None, {}),
	("/home/task_group_inprogress", "files/desktop/Home/Task-Group-Inprogress.html",
            None, {}),
	("/home/task_group_complied", "files/desktop/Home/Task-Group-Complied.html",
            None, {}),
	("/home/task_group_delayed", "files/desktop/Home/Task-Group-Delayed.html",
            None, {}),
	("/home/task_group_notcomplied", "files/desktop/Home/Task-Group-NotComplied.html",
            None, {}),
	("/home/task_entity_inprogress", "files/desktop/Home/Task-Entity-Inprogress.html",
            None, {}),
	("/home/task_entity_complied", "files/desktop/Home/Task-Entity-Complied.html",
            None, {}),
	("/home/task_division_inprogress", "files/desktop/Home/Task-Division-Inprogress.html",
            None, {}),
	("/home/task_division_complied", "files/desktop/Home/Task-Division-Complied.html",
            None, {}),
	("/home/task_unit_inprogress", "files/desktop/Home/Task-Unit-Inprogress.html",
            None, {}),
	("/home/task_unit_complied", "files/desktop/Home/Task-Unit-Complied.html",
            None, {}),
    ("/home/comp_risk", "files/desktop/Home/ComplianceRisk.html",
            None, {}),
	("/home/complienceopprtunity_group_not", "files/desktop/Home/ComplienceOpportunity-Group-Not.html",
            None, {}),
	("/home/complienceopprtunity_entity_not", "files/desktop/Home/ComplienceOpportunity-Entity-Not.html",
            None, {}),
	("/home/complienceopprtunity_division_not", "files/desktop/Home/ComplienceOpportunity-Division-Not.html",
            None, {}),
	("/home/complienceopprtunity_unit_not", "files/desktop/Home/ComplienceOpportunity-Unit-Not.html",
            None, {}),
	("/home/escalations_group_delayed", "files/desktop/Home/Escalations-Group-Delayed.html",
            None, {}),
	("/home/escalations_entity_delayed", "files/desktop/Home/Escalations-Entity-Delayed.html",
            None, {}),
	("/home/escalations_division_delayed", "files/desktop/Home/Escalations-Division-Delayed.html",
            None, {}),
	("/home/escalations_unit_delayed", "files/desktop/Home/Escalations-Unit-Delayed.html",
            None, {}),
    ("/home/co-assigned", "files/desktop/Home/CO-Assigned.html",
            None, {}),
    ("/home/co-unassigned", "files/desktop/Home/CO-Unassigned.html",
            None, {}),
    ("/country/list", "files/desktop/CountryMaster/CountryMasterList.html",
            None, {}),
    ("/country/create", "files/desktop/CountryMaster/CountryMaster.html",
            None, {}),
    ("/statutorylevel/list", "files/desktop/StatutoryLevelMaster/StatutoryLevelMasterList.html",
            None, {}),
    ("/statutorylevel/create", "files/desktop/StatutoryLevelMaster/StatutoryLevelMaster.html",
            None, {}),
    ("/geographylevel/create", "files/desktop/GeographyLevel/GeographyLevelMaster.html",
            None, {}),
    ("/geographylevel/list", "files/desktop/GeographyLevel/GeographyLevelList.html",
            None, {}),
    ("/geographymapping", "files/desktop/GeographyMaster/GeographyMapping.html", 
            None, {}),
    ("/geographymapping/list", "files/desktop/GeographyMaster/GeographyMappingList.html",
            None, {}),
    ("/assignuserlevel/list", "files/desktop/AssignUserLevel/AssignUserLevelList.html",
            None, {}),
	("/assignuserlevel/add", "files/desktop/AssignUserLevel/AssignUserLevel.html",
            None, {}),
    ("/notifications", "files/desktop/Home/Notifications.html",
            None, {}),
    ("/escalations", "files/desktop/Home/Escalations.html",
            None, {}),
    ("/reminders", "files/desktop/Home/Reminders.html",
            None, {}),
	("/report/statutory_master_report", "files/desktop/StatutoryMasterReport/StatutoryMasterReport.html",
        None, {}),
	("/report/statutory_mapping_report", "files/desktop/StatutoryMappingReport/StatutoryMappingReport.html",
        None, {}),
	("/report/client_detailed_report", "files/desktop/ClientDetailedReport/ClientDetailedReport.html",
        None, {}),
	("/report/assigned_statutory_report", "files/desktop/AssignedStatutoryReport/AssignedStatutoryReport.html",
        None, {}),
    ("/report/client_group_report", "files/desktop/ClientGroupReport/ClientGroupReport.html",
        None, {}),
    ("/statutory_settings", "files/desktop/StatutorySettings/StatutorySettings.html",
        None, {}),
    ("/statutorysettinglist", "files/desktop/StatutorySettings/StatutorySettingsList.html",
        None, {}),
    ("/home_userwise_2015", "files/desktop/Home/ClientAdminHome/UserwiseComplianceChart2015.html",
        None, {}),
    ("/report/domain", "files/desktop/KnowledgeMasterReport/domain.html",
        None, {}),
    ("/report/country", "files/desktop/KnowledgeMasterReport/country.html",
        None, {}),
    ("/report/applicability", "files/desktop/KnowledgeMasterReport/applicability.html",
        None, {}),
    ("/report/industry", "files/desktop/KnowledgeMasterReport/industry.html",
        None, {}),
    ("/report/geography", "files/desktop/KnowledgeMasterReport/geography.html",
        None, {}),
    ("/report/user-list", "files/desktop/UserList/UserList.html",
        None, {}),
     ("/report/assigned-compliances", "files/desktop/AssignedCompliances/AssignedCompliances.html",
        None, {}),
     ("/report/unitwise_compliance", "files/desktop/UnitwiseCompliances/UnitwiseCompliances.html",
        None, {}),
     ("/report/compliancerisk", "files/desktop/ComplianceRiskReport/ComplianceRiskReport.html",
        None, {}),
     ("/report/statutorynotification", "files/desktop/StatutoryNotificationsReport/StatutoryNotificationsReport.html",
        None, {}),
     ("/report/statutorynotificationtechno", "files/desktop/StatutoryNotificationsReportTechno/StatutoryNotificationsReport.html",
        None, {}),
    ("/report/riskreport", "files/desktop/RiskReport/RiskReport.html",
        None, {}),
    ("/closeunit", "files/desktop/CloseUnit/CloseUnit.html",
        None, {}),
    ("/client_user_list", "files/desktop/ClientUsersList/ClientUsersList.html",
        None, {}),
    ("/onoccurrence", "files/desktop/OnOccurrence/OnOccurrence.html",
        None, {}),
    ("/company_profile", "files/desktop/CompanyProfile/CompanyProfile.html",
        None, {}),
    ("/report/reassigntask", "files/desktop/ReassignTaskList/ReassignTaskList.html",
        None, {}),
    ("/previousentryform", "files/desktop/PreviousEntryForm/PreviousEntryForm.html",
        None, {}),
    ("/logintrace", "files/desktop/LoginTrace/LoginTrace.html",
        None, {}),

    ("/multi-check-box", "files/desktop/custom-controls/multi-check-box.html", None, {}),
]



#
# TemplateHandler
#

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Src-client")
)
template_env = jinja2.Environment(loader=template_loader)

class TemplateHandler(tornado.web.RequestHandler) :
    def initialize(self, path_desktop, path_mobile, parameters) :
        parameters = {"user":self.get_cookie("user"), "data":OrderedDict(sorted(countriesdb.countries.items(), key=lambda t: t[1])),}
        self.__path_desktop = path_desktop
        self.__path_mobile = path_mobile
        self.__parameters = parameters

    def get(self) :
        path = self.__path_desktop
        if self.__path_mobile is not None :
            user_agent = parse(self.request.headers["User-Agent"])
            if user_agent.is_mobile :
                path = self.__path_mobile
        mime_type, encoding = mimetypes.guess_type(path)
        self.set_header("Content-Type", mime_type)
        template = template_env.get_template(path)
        output = template.render(**self.__parameters)
        self.write(output)

class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    def get(self,username):
        username = self.get_argument("username")
        password = self.get_argument("password")
        parameters = {"username":username, "password":password}
        template = template_env.get_template("files/desktop/Login/Login.html")
        output = template.render(parameters)
        self.write(output)
 
    def post(self):
        json_data = json.loads(self.request.body)
        data = json_data["data"]
        username = data["username"]
        password = data["password"]
        js = ""
        if(username == "serviceproviderManager@domain.com" and password == '0123456789'):
            js = '../service_provider'
        elif(username == "serviceproviderUser@domain.com" and password == '0123456789'):
            js = '../service_provider'
        elif(username == "business@domain.com" and password == '0123456789'):
            js = '../business_team'
        elif(username == "itManager@domain.com" and password == '0123456789'):
            js = '../it'
        elif(username == "itUser@domain.com" and password == '0123456789'):
            js = '../it/user/home'
        elif(username == "knowledgeManager@domain.com" and password == '0123456789'):
            js = '../knowledge'
        elif(username == "knowledgeUser@domain.com" and password == '0123456789'):
            js = '../knowledge/user/home'
        elif(username == "technoManager@domain.com" and password == '0123456789'):
            js = '../techno'
        elif(username == "technoUser@domain.com" and password == '0123456789'):
            js = '../techno/user/home'
        elif(username == "bmanager@domain.com" and password == '0123456789'):
            js = '../bmanager_home'
        elif(username == "sales@domain.com" and password == '0123456789'):
            js = '../sales_home'
        elif(username == "client@domain.com" and password == '0123456789'):
            js = '../inhouse/home'
        elif(username == "clientadmin@domain.com" and password == '0123456789'):
            js = '../home'
        else:
            js = '../index'
        self.set_cookie("user", username)
        self.set_header('Content-Type', 'application/json')
        json_ = tornado.escape.json_encode(js)
        self.write(json_)

class APIHandler(tornado.web.RequestHandler):
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    def get(self) :
        countries = {"IND": "India", "SGP": "Singapore", "MYS": "Malaysia", "USA": "United States", "CAN": "Canada"}
        template = template_env.get_template("files/desktop/Test/test.html")
        output = template.render()
        self.write(output)


#
# run_server
#

REQUEST_PATHS = [
    ("/post/login", LoginHandler),
    ("/login/(.*)", LoginHandler),
    ("/test2", APIHandler),
] 
 
def run_server() :
    application_urls = []
    for url, path_desktop, path_mobile, parameters in TEMPLATE_PATHS :
        args = {
            "path_desktop": path_desktop,
            "path_mobile": path_mobile,
            "parameters": parameters
        }
        entry = (url, TemplateHandler, args)
        application_urls.append(entry)

    for url, handler in REQUEST_PATHS :
        args = {
            "url": url,
            "handler": handler
        }
        entry = (url, handler, args)
        application_urls.append(entry)

    for url, handler in client_admin_handler.initializeClientAdminHandler() :
        args = {
            "url": url,
            "handler": handler
        }
        entry = (url, handler, args)
        application_urls.append(entry)

    for url, handler in admin_handler.initializeAdminHandler() :
        args = {
            "url": url,
            "handler": handler
        }
        entry = (url, handler, args)
        application_urls.append(entry)

    for url, handler in techno_handler.initializeTechnoHandler() :
        args = {
            "url": url,
            "handler": handler
        }
        entry = (url, handler, args)
        application_urls.append(entry)

    for url, handler in knowledge_handler.initializeKnowledgeHandler() :
        args = {
            "url": url,
            "handler": handler
        }
        entry = (url, handler, args)
        application_urls.append(entry)

    static_path = os.path.join(ROOT_PATH, "Src-client")
    files_path = os.path.join(static_path, "files")
    desktop_path = os.path.join(files_path, "desktop")
    common_path = os.path.join(desktop_path, "common")
    images_path = os.path.join(common_path, "images")
    css_path = os.path.join(common_path, "css")
    js_path = os.path.join(common_path, "js")

    lower_level_handlers = [
        (r"/images/(.*)", tornado.web.StaticFileHandler, dict(path=images_path)),
		(r"/css/(.*)", tornado.web.StaticFileHandler, dict(path=css_path)),
        (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path=js_path)),
        (r"/(.*)", tornado.web.StaticFileHandler, dict(path=static_path)),
    ]
    application_urls.extend(lower_level_handlers)
    
    print "Listening on port %s" % (HTTP_PORT,)
    application = tornado.web.Application(
        application_urls,
        gzip=True
    )
    application.listen(HTTP_PORT)
    try :
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt :
        print ""
        print "Ctrl-C received. Exiting."
