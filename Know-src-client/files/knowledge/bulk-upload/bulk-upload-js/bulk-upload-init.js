function initMethods() {
    return {
        getStatutoryMappingCsvList: getStatutoryMappingCsvList,
        uploadClientUnitsBulkCSV: uploadClientUnitsBulkCSV,
        uploadStatutoryMappingCSV: uploadStatutoryMappingCSV,
        uploadCSVFile: uploadCSVFile,
        getClientGroupsClientUnitFilesList: getClientGroupsClientUnitFilesList,
        getClientInfo: getClientInfo,
        uploadCSVFile: uploadCSVFile,
        getDownloadAssignStatutory: getDownloadAssignStatutory,
        getUploadAssignStatutoryCSV: getUploadAssignStatutoryCSV,
        getAssignStatutoryForApprove: getAssignStatutoryForApprove,
        uploadCSVFile: uploadCSVFile,
        getStatutoryMappingsBulkReportData:getStatutoryMappingsBulkReportData,

        updateActionFromList: updateActionFromList,
        confirmUpdateAction: confirmUpdateAction,
        getApproveMappingView: getApproveMappingView,
        getApproveMappingCSVList: getApproveMappingCSVList,
        updateActionFromView: updateActionFromView,

        getAssignedStatutoryBulkReportData:getAssignedStatutoryBulkReportData,
        getRejectedStatutoryMappingBulkUploadData:getRejectedStatutoryMappingBulkUploadData,
        deleteRejectedStatutoryMappingByCsvID:deleteRejectedStatutoryMappingByCsvID,
        setDownloadClickCount:setDownloadClickCount,
        getClientUnitBulkReportData:getClientUnitBulkReportData,
        getClientUnitRejectedData:getClientUnitRejectedData,
        updateDownloadClickCount:updateDownloadClickCount,
        deleteRejectedUnitByCsvID:deleteRejectedUnitByCsvID,
        performClientUnitApproveReject: performClientUnitApproveReject

    };
}

var bu = initMethods();
