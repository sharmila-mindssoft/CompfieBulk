//country countryId legalEntity legalEntityId domain domainId
var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");
var filterCountryName = $(".filter-country-name");

var legalEntity = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");
var filterLegalEntityName = $(".filter-legal-entity-name");

var domain = $("#domain");
var domainId = $("#domain-id");
var acDomain = $("#ac-domain");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var taskDetails = $("#task-details");
var clientLogo = $("#client-logo");
var legalEntityName = $("#legal-entity-name");
var countryName = $("#country-name");
var domainName = $("#domain-name");

var reportTableTbody = $("#report-table-tbody");
var template = $("#template");
var reportTable = $("#report-table");
var REPORT = null;
var LOGO = null;

WorkFlowScoreCard = function() {
    this._entities = [];
    this._domains = [];
    this._report_data = [];
}

WorkFlowScoreCard.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

function PageControls() {

    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._entities;
        if (countryList.length == 0 && text_val != '')
            displayMessage(message.country_required);
        var condition_fields = [];
        var condition_values = [];
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            onCountryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntity.keyup(function(e) {
        var text_val = legalEntity.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.legalentity_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        if (domainList.length == 0 && text_val != '')
            displayMessage(message.domain_required);
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, legalEntityId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        var csv = false;
        processSubmit(csv);
    });

    exportButton.click(function() {
        var csv = true;
        processSubmit(csv);
    });
}

processSubmit = function(csv) {
    if (REPORT.validate()) {
        REPORT.fetchReportValues(csv);
    }
}

clearElement = function(arr) {
    if (arr.length > 0) {
        $.each(arr, function(i, element) {
            element.val('');
        });
    }
}

onCountryAutoCompleteSuccess = function(REPORT, val) {
    country.val(val[1]);
    countryId.val(val[0]);
    country.focus();
    clearElement([legalEntity, legalEntityId, domain, domainId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    legalEntity.val(val[1]);
    legalEntityId.val(val[0]);
    legalEntity.focus();
    clearElement([domain, domainId]);
    REPORT.fetchDomainList(val[0]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
}

WorkFlowScoreCard.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, legalEntity, legalEntityId, domain, domainId]);
    this.fetchSearchList();
};

WorkFlowScoreCard.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    /*if(le_id != "") {
        var jsondata = '{"domains":[{"d_id":1,"d_name":"Labour Law","le_id":1,"is_active":true},{"d_id":2,"d_name":"Finance Law","le_id":1,"is_active":true},{"d_id":3,"d_name":"Economic Law","le_id":1,"is_active":true}]}';
        var object = jQuery.parseJSON(jsondata);
        t_this._domains = object.domains;
    } else {
        displayMessage(message.legalentity_required);
    }*/
    displayLoader();
    client_mirror.getWorkFlowScoreCardFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};
//country legalEntity domain
WorkFlowScoreCard.prototype.validate = function() {
    if (country) {
        if (isNotEmpty(country, message.country_required) == false)
            return false;
        else if (isLengthMinMax(country, 1, 50, message.country_max) == false)
            return false;
        else if (isCommonName(country, message.country_str) == false)
            return false;
    }
    if (legalEntity) {
        if (isNotEmpty(legalEntity, message.legalentity_required) == false)
            return false;
        else if (isLengthMinMax(legalEntity, 1, 50, message.legalentity_max) == false)
            return false;
        else if (isCommonName(legalEntity, message.legalentity_str) == false)
            return false;
    }
    if (domain) {
        if (isNotEmpty(domain, message.domain_required) == false)
            return false;
        else if (isLengthMinMax(domain, 0, 50, message.domain_max) == false)
            return false;
        else if (isCommonName(domain, message.domain_str) == false)
            return false;
    }
    return true;
};

showAnimation = function(element) {
    element.removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
}

WorkFlowScoreCard.prototype.fetchReportValues = function(csv) {
    t_this = this;

    var c_id = parseInt(countryId.val());
    var le_id = parseInt(legalEntityId.val());
    var d_id = parseInt(domainId.val());
    displayLoader();
    client_mirror.getWorkFlowScoreCard(c_id, le_id, d_id, csv, function(error, response) {
        if (error == null) {
            t_this._report_data = response.work_flow_score_card_list;
            LOGO = response.logo_url;
            if (csv == false) {
                reportView.show();
                showAnimation(reportView);
                REPORT.showReportValues();
            } else {
                REPORT.exportReportValues();
            }
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};

WorkFlowScoreCard.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    if(LOGO != null)
        clientLogo.attr("src", LOGO);
    else
        clientLogo.remove();
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    domainName.html(domain.val());
    var completed_count = 0;
    var inprogress_count = 0;
    var over_due_count = 0;
    taskDetails.hide();
    $.each(data, function(k, v) {
        $('.completed-assignee-count').text(v.c_assignee);
        $('.completed-concur-count').text(v.c_concur);
        $('.completed-approver-count').text(v.c_approver);

        $('.inprogress-assignee-count').text(v.inp_assignee);
        $('.inprogress-concur-count').text(v.inp_concur);
        $('.inprogress-approver-count').text(v.inp_approver);

        $('.overdue-assignee-count').text(v.ov_assignee);
        $('.overdue-concur-count').text(v.ov_concur);
        $('.overdue-approver-count').text(v.ov_approver);

        completed_count = completed_count + parseInt(v.c_assignee) + parseInt(v.inp_assignee) + parseInt(v.ov_assignee);
        inprogress_count = inprogress_count + parseInt(v.c_concur) + parseInt(v.inp_concur) + parseInt(v.ov_concur);
        over_due_count = over_due_count + parseInt(v.c_approver) + parseInt(v.inp_approver) + parseInt(v.ov_approver);

        $('.inprogress-unit-view').on('click', function() {
            t_this.inprogressUnitView(v.inprogress_within_duedate_task_count);
        });
        $('.completed-unit-view').on('click', function() {
            t_this.completedUnitView(v.completed_task_count);
        });
        $('.overdue-unit-view').on('click', function() {
            t_this.overdueUnitView(v.over_due_task_count);
        });
    });
    $('.total-assignee-count').html(completed_count);
    $('.total-concur-count').html(inprogress_count);
    $('.total-approver-count').html(over_due_count);
};

WorkFlowScoreCard.prototype.inprogressUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit Wise - In progress Within Due Date Task Count");
    $('.title-submit').html('Yet to Submit');
    $('.title-concur').html('Yet to Concurr');
    $('.title-approve').html('Yet to Approve');
    taskDetails.show();
    reportTableTbody.find('tr').remove();
    var submit_total = 0;
    var concur_total = 0;
    var approve_total = 0;
    var grand_total = 0;
    var j = 0;
    if(data.length > 0) {
        $.each(data, function(k, v) {
            var cloneone = $('#template #report-table .report-row').clone();
            $('.task-row-title', cloneone).text(v.unit);
            $('.submit', cloneone).text(v.inp_assignee);
            $('.concur', cloneone).text(v.inp_concur);
            $('.approve', cloneone).text(v.inp_approver);
            reportTableTbody.append(cloneone);
            submit_total = submit_total + parseInt(v.inp_assignee);
            concur_total = concur_total + parseInt(v.inp_concur);
            approve_total = approve_total + parseInt(v.inp_approver);
            j = j + 1;
        });
        if (j > 1) {
            var clonetwo = $('#template #report-table .report-total-row').clone();
            $('.submit-total', clonetwo).text(submit_total);
            $('.concur-total', clonetwo).text(concur_total);
            $('.approve-total', clonetwo).text(approve_total);
            reportTableTbody.append(clonetwo);
        }
    } else {
        reportTableTbody.html('<tr><td colspan="100%"><br><center>Record Not Found!</center><br></td></tr>');
    }
};

WorkFlowScoreCard.prototype.completedUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit Wise - Completed Task Count");
    $('.title-submit').html('You Submitted');
    $('.title-concur').html('You Concurred');
    $('.title-approve').html('You Approved');
    taskDetails.show();
    reportTableTbody.find('tr').remove();
    var submit_total = 0;
    var concur_total = 0;
    var approve_total = 0;
    var grand_total = 0;
    var j = 0;
    if(data.length > 0) {
        $.each(data, function(k, v) {
            var cloneone = $('#template #report-table .report-row').clone();
            $('.task-row-title', cloneone).text(v.unit);
            $('.submit', cloneone).text(v.c_assignee);
            $('.concur', cloneone).text(v.c_concur);
            $('.approve', cloneone).text(v.c_approver);
            reportTableTbody.append(cloneone);
            submit_total = submit_total + parseInt(v.c_assignee);
            concur_total = concur_total + parseInt(v.c_concur);
            approve_total = approve_total + parseInt(v.c_approver);
            j = j + 1;
        });
        if (j > 1) {
            var clonetwo = $('#template #report-table .report-total-row').clone();
            $('.submit-total', clonetwo).text(submit_total);
            $('.concur-total', clonetwo).text(concur_total);
            $('.approve-total', clonetwo).text(approve_total);
            reportTableTbody.append(clonetwo);
        }
    } else {
        reportTableTbody.html('<tr><td colspan="100%"><br><center>Record Not Found!</center><br></td></tr>');
    }
};

WorkFlowScoreCard.prototype.overdueUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit Wise - In progress Over Due Task Count");
    $('.title-submit').html('Yet to Submit');
    $('.title-concur').html('Yet to Concurr');
    $('.title-approve').html('Yet to Approve');
    taskDetails.show();
    reportTableTbody.find('tr').remove();
    var submit_total = 0;
    var concur_total = 0;
    var approve_total = 0;
    var grand_total = 0;
    var j = 0;
    if(data.length > 0) {
        $.each(data, function(k, v) {
            var cloneone = $('#template #report-table .report-row').clone();
            $('.task-row-title', cloneone).text(v.unit);
            $('.submit', cloneone).text(v.ov_assignee);
            $('.concur', cloneone).text(v.ov_concur);
            $('.approve', cloneone).text(v.ov_approver);
            reportTableTbody.append(cloneone);
            submit_total = submit_total + parseInt(v.ov_assignee);
            concur_total = concur_total + parseInt(v.ov_concur);
            approve_total = approve_total + parseInt(v.ov_approver);
            j = j + 1;
        });
        if (j > 1) {
            var clonetwo = $('#template #report-table .report-total-row').clone();
            $('.submit-total', clonetwo).text(submit_total);
            $('.concur-total', clonetwo).text(concur_total);
            $('.approve-total', clonetwo).text(approve_total);
            reportTableTbody.append(clonetwo);
        }
    } else {
        reportTableTbody.html('<tr><td colspan="100%"><br><center>Record Not Found!</center><br></td></tr>');
    }
};

WorkFlowScoreCard.prototype.exportReportValues = function() {
    alert('export');
};

WorkFlowScoreCard.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
    }
};

WorkFlowScoreCard.prototype.loadEntityDetails = function() {
    t_this = this;
    if (t_this._entities.length > 1) {
        country.parent().show();
        filterCountryName.hide();

        legalEntity.parent().show();
        filterLegalEntityName.hide();
    } else {
        filterCountryName.show();
        filterCountryName.html(t_this._entities[0]["c_name"]);
        countryId.val(t_this._entities[0]["c_id"]);
        country.parent().hide();
        country.val(t_this._entities[0]["c_name"]);

        filterLegalEntityName.show();
        filterLegalEntityName.html(t_this._entities[0]["le_name"]);
        legalEntityId.val(t_this._entities[0]["le_id"]);
        legalEntity.parent().hide();
        legalEntity.val(t_this._entities[0]["le_name"]);

        REPORT.fetchDomainList(t_this._entities[0]["le_id"]);
    }
    hideLoader();
};

REPORT = new WorkFlowScoreCard();

$(document).ready(function() {
    displayLoader();
    PageControls();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});
