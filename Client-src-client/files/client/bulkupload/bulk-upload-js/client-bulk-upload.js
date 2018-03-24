function getCompletedTaskCurrentYearCsvList(callback) {
    var request = [
        'GetStatutoryMappingCsvUploadedList',
        {}
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}

function getDomains(le_id, callback) {
    var request = [
        'GetCompletedTask_Domains', {
            'le_id': le_id
        }
    ];
    clientApiRequest('bu/completed_task', request, callback);
}
function getDownloadData(legalEntityId, domainId, unitId, complianceFrequency, startCount, 
                         LegalEntityName, domainName, unitName, unitCode,
                         callback) {
    var request = [
        'GetDownloadData', {
            'le_id': legalEntityId,
            'unit_id': unitId,
            'domain_id': domainId,
            'compliance_task_frequency': complianceFrequency,
            'start_count': startCount,
            "le_name": LegalEntityName,
            "d_name": domainName,
            "u_name": unitName,
            "u_code": unitCode
        }
    ];
    clientApiRequest('client_transaction', request, callback);
}
