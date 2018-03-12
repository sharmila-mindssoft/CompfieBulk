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
        getApproveMappingViewFilter: getApproveMappingViewFilter,

        getAssignedStatutoryBulkReportData:getAssignedStatutoryBulkReportData,
        getRejectedStatutoryMappingBulkUploadData:getRejectedStatutoryMappingBulkUploadData,
        deleteRejectedStatutoryMappingByCsvID:deleteRejectedStatutoryMappingByCsvID,
        setDownloadClickCount:setDownloadClickCount,
        getClientUnitBulkReportData:getClientUnitBulkReportData,
        getClientUnitRejectedData:getClientUnitRejectedData,
        updateDownloadClickCount:updateDownloadClickCount,
        deleteRejectedUnitByCsvID:deleteRejectedUnitByCsvID,

        performClientUnitApproveReject: performClientUnitApproveReject,
        getRejectedAssignSMData:getRejectedAssignSMData,
        updateASMDownloadClickCount:updateASMDownloadClickCount,
        deleteRejectedASMByCsvID:deleteRejectedASMByCsvID,
        exportCUBulkReportData:exportCUBulkReportData,
        exportASBulkReportData:exportASBulkReportData,
        downloadRejectedSMReportData:downloadRejectedSMReportData,
        downloadRejectedClientUnitReport:downloadRejectedClientUnitReport,
        downloadRejectedASMReportData:downloadRejectedASMReportData,
        getAssignStatutoryFilters: getAssignStatutoryFilters,
        getViewAssignStatutoryData: getViewAssignStatutoryData,
        getViewAssignStatutoryDataFromFilter: getViewAssignStatutoryDataFromFilter,
        assignStatutoryActionInList: assignStatutoryActionInList,
        getBulkClientUnitApproveRejectList: getBulkClientUnitApproveRejectList,
        updateAssignStatutoryActionFromView: updateAssignStatutoryActionFromView,
        confirmAssignStatutoryUpdateAction: confirmAssignStatutoryUpdateAction,
        confirmClientUnitDeclination: confirmClientUnitDeclination,
        getClientUnitViewFilter: getClientUnitViewFilter,
        updateClientUnitActionFromView: updateClientUnitActionFromView

    };
}

var bu = initMethods();
