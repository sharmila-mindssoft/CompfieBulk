
function initMirror() {
    return {
        log: log,
        toJSON: toJSON,
        parseJSON: parseJSON,
        getBaseUrl: getBaseUrl,
        initSession: initSession,
        clearSession: clearSession,
        verifyLoggedIn: verifyLoggedIn,
        logout: logout,
        getEmployeeName: getEmployeeName,
        getUserId: getUserId,
        getUserInfo: getUserInfo,
        updateUserInfo: updateUserInfo,
        getUserProfile: getUserProfile,
        getSessionToken: getSessionToken,
        getUserMenu: getUserMenu,
        getPageUrl: getPageUrl,
        apiRequest: apiRequest,
        LoginApiRequest: LoginApiRequest,
        saveDomain: saveDomain,
        updateDomain: updateDomain,
        changeDomainStatus: changeDomainStatus,
        getDomainList: getDomainList,
        getDomainReport: getDomainReport,
        saveCountry: saveCountry,
        updateCountry: updateCountry,
        changeCountryStatus: changeCountryStatus,
        getCountryList: getCountryList,
        getCountryListForUser: getCountryListForUser,
        getCountryReport: getCountryReport,
        getSaveIndustryDict: getSaveIndustryDict,
        saveIndustry: saveIndustry,
        getUpdateIndustryDict: getUpdateIndustryDict,
        updateIndustry: updateIndustry,
        changeIndustryStatus: changeIndustryStatus,
        getIndustryList: getIndustryList,
        getSaveStatutoryNatureDict: getSaveStatutoryNatureDict,
        saveStatutoryNature: saveStatutoryNature,
        getUpdateStatutoryNatureDict: getUpdateStatutoryNatureDict,
        updateStatutoryNature: updateStatutoryNature,
        changeStatutoryNatureStatus: changeStatutoryNatureStatus,
        getStatutoryNatureList: getStatutoryNatureList,
        levelDetails: levelDetails,
        getGeographyLevels: getGeographyLevels,
        saveAndUpdateGeographyLevels: saveAndUpdateGeographyLevels,
        getStatutoryLevels: getStatutoryLevels,
        saveAndUpdateStatutoryLevels: saveAndUpdateStatutoryLevels,
        getGeographies: getGeographies,
        saveGeography: saveGeography,
        updateGeography: updateGeography,
        changeGeographyStatus: changeGeographyStatus,
        getGeographyReport: getGeographyReport,
        saveStatutory: saveStatutory,
        updateStatutory: updateStatutory,
        statutoryDates: statutoryDates,
        uploadFile: uploadFile,
        uploadFileFormat: uploadFileFormat,
        complianceDetails: complianceDetails,
        statutoryMapping: statutoryMapping,
        checkDuplicateStatutoryMapping: checkDuplicateStatutoryMapping,
        saveStatutoryMapping: saveStatutoryMapping,
        updateStatutoryMapping: updateStatutoryMapping,
        updateComplianceOnly: updateComplianceOnly,
        getStatutoryMaster: getStatutoryMaster,
        getStatutoryMappingsMaster: getStatutoryMappingsMaster,
        getStatutoryMappings: getStatutoryMappings,
        changeStatutoryMappingStatus: changeStatutoryMappingStatus,
        getApproveStatutoryMapingsFilters: getApproveStatutoryMapingsFilters,
        approveStatutoryList: approveStatutoryList,
        approveStatutoryMapping: approveStatutoryMapping,
        getStatutoryMappingsReportFilter: getStatutoryMappingsReportFilter,
        filterData: filterData,
        getStatutoryMappingsReportData: getStatutoryMappingsReportData,
        getApproveStatutoryMapings: getApproveStatutoryMapings,
        getComplianceInfo: getComplianceInfo,
        getSaveAdminUserGroupDict: getSaveAdminUserGroupDict,
        saveAdminUserGroup: saveAdminUserGroup,
        getUpdateAdminUserGroupDict: getUpdateAdminUserGroupDict,
        updateAdminUserGroup: updateAdminUserGroup,
        changeAdminUserGroupStatus: changeAdminUserGroupStatus,
        getAdminUserGroupList: getAdminUserGroupList,
        getSaveAdminUserDict: getSaveAdminUserDict,
        saveAdminUser: saveAdminUser,
        sendRegistration: sendRegistration,
        getUpdateAdminUserDict: getUpdateAdminUserDict,
        updateAdminUser: updateAdminUser,
        changeAdminUserStatus: changeAdminUserStatus,
        getAdminUserList: getAdminUserList,
        getDateConfigurations: getDateConfigurations,
        saveClientGroup: saveClientGroup,
        updateClientGroup: updateClientGroup,
        getClientGroups: getClientGroups,
        changeClientGroupStatus: changeClientGroupStatus,
        getAssignLegalEntityList: getAssignLegalEntityList,
        getEditAssignLegalEntity: getEditAssignLegalEntity,
        saveAssignLegalEntity: saveAssignLegalEntity,
        viewAssignLegalEntity: viewAssignLegalEntity,
        changePassword: changePassword,
        forgotPassword: forgotPassword,
        validateResetToken: validateResetToken,
        resetPassword: resetPassword,
        getClients: getClients,
        getClientsEdit: getClientsEdit,
        getBusinessGroupDict: getBusinessGroupDict,
        getLegalEntityDict: getLegalEntityDict,
        getDivisionDict: getDivisionDict,
        getUnitDict: getUnitDict,
        mapUnitsToCountry: mapUnitsToCountry,
        saveClient: saveClient,
        updateClient: updateClient,
        changeClientStatus: changeClientStatus,
        reactivateUnit: reactivateUnit,
        getClientProfile: getClientProfile,
        getClientDetailsReportFilters: getClientDetailsReportFilters,
        getClientDetailsReport: getClientDetailsReport,
        getAssignedStatutoryReportFilters: getAssignedStatutoryReportFilters,
        getAssignedStatutoryReport: getAssignedStatutoryReport,
        getStatutoryNotificationsFilters: getStatutoryNotificationsFilters,
        getStatutoryNotificationsReportData: getStatutoryNotificationsReportData,
        getComplianceTaskFilter: getComplianceTaskFilter,
        get_ip: get_ip,
        getAuditTrail: getAuditTrail,
        getAuditTrailFilter: getAuditTrailFilter,
        updateUserProfile: updateUserProfile,
        getNotifications: getNotifications,
        updateNotificationStatus: updateNotificationStatus,
        createNewAdmin: createNewAdmin,
        getNextUnitCode: getNextUnitCode,
        uploadFormatFile: uploadFormatFile,
        getValidityDateList: getValidityDateList,
        get_validity_day_setting: get_validity_day_setting,
        saveValidityDateSettings: saveValidityDateSettings,
        getClientGroupFormData: getClientGroupFormData,
        getLegalEntityRow: getLegalEntityRow,
        getDomainRow: getDomainRow,
        getEditClientGroupFormData: getEditClientGroupFormData,
        getLegalEntityUpdateRow: getLegalEntityUpdateRow,
        getClientUnitApprovalList: getClientUnitApprovalList,
        getEntityApprovalList: getEntityApprovalList,
        approveUnit: approveUnit,
        getClientGroupApprovalList: getClientGroupApprovalList,
        getLegalEntity: getLegalEntity,
        approveClientGroupList: approveClientGroupList,
        approveClientGroup: approveClientGroup,
        getDatabaseServerList: getDatabaseServerList,
        saveDBServer: saveDBServer,
        getClientServerList: getClientServerList,
        saveClientServer: saveClientServer,
        getAllocatedDBEnv: getAllocatedDBEnv,
        saveDBEnv: saveDBEnv,
        getFileStorage: getFileStorage,
        saveFileStorage: saveFileStorage,
        getAutoDeletionList: getAutoDeletionList,
        getDeletionDetails: getDeletionDetails,
        saveAutoDeletion: saveAutoDeletion,
        getUserMappings: getUserMappings,
        saveUserMappings: saveUserMappings,
        checkUserMappings: checkUserMappings,
        getUnassignedUnitsList: getUnassignedUnitsList,
        getAssignedUnitsList: getAssignedUnitsList,
        getAssignedUnitDetails: getAssignedUnitDetails,
        getAssignUnitFormData: getAssignUnitFormData,
        saveAssignedUnits: saveAssignedUnits,
        getReassignUserAccountFormdata: getReassignUserAccountFormdata,
        getTechnoUSerInfo: getTechnoUSerInfo,
        getDomainUserInfo: getDomainUserInfo,
        ReassignTechnoManager: ReassignTechnoManager,
        ReassignTechnoExecutive: ReassignTechnoExecutive,
        ReassignDomainManager: ReassignDomainManager,
        ReassignDomainExecutive: ReassignDomainExecutive,
        SaveUserReplacement: SaveUserReplacement,
        getAssignStatutoryWizardOneData: getAssignStatutoryWizardOneData,
        getAssignStatutoryWizardOneDataUnits: getAssignStatutoryWizardOneDataUnits,
        getAssignStatutoryWizardTwoData: getAssignStatutoryWizardTwoData,
        getAssignStatutoryWizardTwoCount: getAssignStatutoryWizardTwoCount,
        saveAssignedStatutory: saveAssignedStatutory,
        //submitAssignedStatutory: submitAssignedStatutory,
        getAssignedStatutories: getAssignedStatutories,
        getAssignedStatutoriesById: getAssignedStatutoriesById,
        changeAdminDisaleStatus: changeAdminDisaleStatus,
        getUserMappingReportFilters: getUserMappingReportFilters,
        getUsermappingDetailsReport: getUsermappingDetailsReport,
        getGroupAdminGroupList: getGroupAdminGroupList,
        sendGroupAdminRegnmail: sendGroupAdminRegnmail,
        resendGroupAdminRegnmail: resendGroupAdminRegnmail,
        getGroupAdminReportData: getGroupAdminReportData,
        getAssignedUserClientGroups: getAssignedUserClientGroups,
        getReassignUserReportData: getReassignUserReportData,
        getLegalEntityClosureData: getLegalEntityClosureData,
        saveLegalEntityClosureData: saveLegalEntityClosureData,
        verifyPassword: verifyPassword,
        getClientAgreementReportFilters: getClientAgreementReportFilters,
        getClientAgreementReport: getClientAgreementReport,
        getDomainwiseAgreementReport: getDomainwiseAgreementReport,
        getOrganizationWiseUnitCount: getOrganizationWiseUnitCount,
        getMessages: getMessages,
        getStatutoryNotifications: getStatutoryNotifications,
        updateStatutoryNotificationStatus: updateStatutoryNotificationStatus,
        updateMessageStatus: updateMessageStatus,
        getReassignUserDomainReportData: getReassignUserDomainReportData,
        getStatutoryMappingsEdit: getStatutoryMappingsEdit,
        saveComplianceStatus: saveComplianceStatus,
        getAssignedStatutoriesList: getAssignedStatutoriesList,
        getComplianceStatutoriesList: getComplianceStatutoriesList,
        getAssignedStatutoriesForApprove: getAssignedStatutoriesForApprove,
        getAssignedStatutoriesComplianceToApprove: getAssignedStatutoriesComplianceToApprove,
        approveAssignedStatutory: approveAssignedStatutory,
        technoManagerInfo: technoManagerInfo,
        technoExecutiveInfo: technoExecutiveInfo,
        getFileServerList: getFileServerList,
        fileServerEntry: fileServerEntry,
        domainManagerInfo: domainManagerInfo,
        getIPSettingsList: getIPSettingsList,
        getGroupIPDetails: getGroupIPDetails,
        getIPSettingsDetails: getIPSettingsDetails,
        saveIPSettings: saveIPSettings,
        deleteIPSettings: deleteIPSettings,
        getIPSettingsReportFilter: getIPSettingsReportFilter,
        getIPSettingsReport: getIPSettingsReport,
        getAllocateServerReportData: getAllocateServerReportData,
        exportClientDetailsReportData: exportClientDetailsReportData,
        exportAuditTrail: exportAuditTrail,
        exportReassignUserReportData: exportReassignUserReportData,
        exportAllocateServerReportData: exportAllocateServerReportData,
        exportGroupAdminReportData: exportGroupAdminReportData,
        getClientDetailsReportData: getClientDetailsReportData,
        saveDivisionCategory: saveDivisionCategory,
        getDiviCatgDict: getDiviCatgDict,
        checkAssignedDomainUnits: checkAssignedDomainUnits,
        checkUserReplacement: checkUserReplacement,
        getClientAuditTrailFilter: getClientAuditTrailFilter,
        getClientAuditTrail: getClientAuditTrail,
        getExportClientAuditTrail: getExportClientAuditTrail,
        getClientLoginTraceFilter: getClientLoginTraceFilter,
        getClientLoginTrace: getClientLoginTrace,
        getExportClientLoginTrace: getExportClientLoginTrace,
        /* client bulk upload - api function starts */
        getClientGroupsList: getClientGroupsList,
        uploadCSVFile: uploadCSVFile,
        /* client bulk upload - api function ends */
        getKnowledgeUserInfo: getKnowledgeUserInfo
    };
}

var mirror = initMirror();
