
var clientGroupName = $("#client-group");
var clientGroupId = $("#client-group-id");
var acClientGroup = $("#ac-client-group");

var legalEntityName = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function PageControls() {

    clientGroupName.keyup(function(e) {
        var text_val = clientGroupName.val().trim();
        var clientGroupList = REPORT._entities;
        if (clientGroupList.length == 0 && text_val != '')
            displayMessage(message.group_required);
        var condition_fields = [];
        var condition_values = [];
        commonAutoComplete(e, acClientGroup, clientGroupId, text_val, clientGroupList, "c_name", "c_id", function(val) {
            onClientGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntityName.keyup(function(e) {
        var text_val = legalEntityName.val().trim();
        var legalEntityList = REPORT._entities;
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            csv = false;
            on_current_page = 1;
            this._sno = 0;
            this._total_record = 0;
            reportView.show();
            showAnimation(reportView);
            REPORT.fetchReportValues();
        }
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        on_current_page = 1;
        this._sno = 0;
        createPageView(t_this._total_record);
        csv = false;
        REPORT.fetchReportValues();
    });

}

clearElement = function(arr) {
    if(arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

onClientGroupAutoCompleteSuccess = function(REPORT, val) {
    clientGroupName.val(val[1]);
    clientGroupId.val(val[0]);
    clientGroupName.focus();
    clearElement([legalEntityName, legalEntityId]);
    REPORT.fetchLegalEntityList(val[0]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    legalEntityName.val(val[1]);
    legalEntityId.val(val[0]);
    legalEntityName.focus();
    // REPORT.fetchDomainList(val[0]);
}

UserWiseReport = function() {
    this._client_group = [];
    this._entities = [];
    /*this._domains = [];
    this._units = [];
    this._acts = [];
    this._frequencies = [];
    this._user_type = [];
    this._users = [];
    this._compliance_task_status = [];
    this._service_providers = [];
    this._report_data = [];
    on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
    this._UserCompliances = [];*/
}

UserWiseReport.prototype.loadSearch = function() {
    reportView.hide();
    country.val('');
    countryId.val('');
    legalEntityName.val('');
    legalEntityId.val('');
    /*domain.val('');
    domainId.val('');
    unit.val('');
    unitId.val('');
    act.val('');
    actId.val('');
    complianceTask.val('');
    users.val('');
    userId.val('');
    fromDate.val('');
    toDate.val('');
    this.fetchSearchList();*/
};

StatusReportConsolidated.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._entities = client_mirror.getSelectedLegalEntity();
    t_this._userType = UserTypes; // common-functions.js
    t_this._complianceTaskStatus = TaskStatuses; // common-functions.js
    t_this.renderUserTypeList(t_this._userType);
    t_this.renderComplianceTaskStatusList(t_this._complianceTaskStatus);
};

StatusReportConsolidated.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getStatusReportConsolidatedFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
            t_this._units = response.units;
            t_this._acts = response.acts;
            // t_this._compliance_task = response.compliances;
            t_this._users = response.legal_entity_users;
            t_this._frequencies = response.compliance_frequency;
            t_this.renderComplianceFrequencyList(t_this._frequencies);

        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};

REPORT = new UserWiseReport();

$(document).ready(function() {
    // displayLoader();
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});