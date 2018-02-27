function initMethods() {
    return {
        getStatutoryMappingCsvList: getStatutoryMappingCsvList,
        uploadClientUnitsBulkCSV: uploadClientUnitsBulkCSV,
        uploadStatutoryMappingCSV: uploadStatutoryMappingCSV,
        uploadCSVFile: uploadCSVFile,
        getClientInfo: getClientInfo,
        uploadCSVFile: uploadCSVFile,
        getDownloadAssignStatutory: getDownloadAssignStatutory,
        getUploadAssignStatutoryCSV: getUploadAssignStatutoryCSV,
        getStatutoryMappingsBulkReportData:getStatutoryMappingsBulkReportData,
        getAssignedStatutoryBulkReportData:getAssignedStatutoryBulkReportData,
        getRejectedStatutoryMappingBulkUploadData:getRejectedStatutoryMappingBulkUploadData,
        deleteRejectedStatutoryMappingByCsvID:deleteRejectedStatutoryMappingByCsvID

    };
}

var bu = initMethods();
