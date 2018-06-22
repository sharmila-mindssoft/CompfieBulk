function initMethods() {
    return {
        // getStatutoryMappingCsvList: getStatutoryMappingCsvList
        // getCompletedTaskCurrentYearCsvList: getCompletedTaskCurrentYearCsvList,
        // getDomains: getDomains,
        UploadCompletedTaskCurrentYearCSV: UploadCompletedTaskCurrentYearCSV,
        uploadCSVFile: uploadCSVFile,
        getDownloadData: getDownloadData,
        saveBulkRecords: saveBulkRecords,
        GetCompletedTaskCsvUploadedList: GetCompletedTaskCsvUploadedList,
        uploadFile : uploadFile,
        getUnits : getUnits,
        downloadUploadedData: downloadUploadedData,
        updateDocumentCount: updateDocumentCount,
        GetStatus: GetStatus,
        processQueuedTasksRequest: processQueuedTasksRequest
    };
}

var buClient = initMethods();