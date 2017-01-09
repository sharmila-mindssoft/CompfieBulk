//country countryId legalEntity legalEntityId domain domainId
var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");

var legalEntity = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");

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

LEWiseScoreCard = function() {
    this._countries = [];
    this._entities = [];
    this._domains = [];
    this._report_data = [];
}

LEWiseScoreCard.prototype.fetchSearchList = function() {
    t_this = this;
    var jsondata = '{"countries":[{"c_id":1,"c_name":"india","is_active":true},{"c_id":2,"c_name":"srilanka","is_active":true}],"entities":[{"le_id":1,"le_name":"RG Legal Entity","c_id":1,"is_active":true},{"le_id":2,"le_name":"ABC Legal Entity","c_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._countries = object.countries;
    t_this._entities = object.entities;
};

function PageControls() {

    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._countries;
        if (countryList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            onCountryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntity.keyup(function(e) {
        var text_val = legalEntity.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active", "c_id"];
        var condition_values = [true, countryId.val()];
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, 1];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            reportView.show();
            taskDetails.hide();
            showAnimation(reportView);
            REPORT.fetchReportValues();
            REPORT.showReportValues();
        }
    });

    exportButton.click(function() {
        if (REPORT.validate()) {
            REPORT.fetchReportValues();
            REPORT.exportReportValues();
        }
    });
}

clearElement = function(arr) {
    if(arr.length > 0) {
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

LEWiseScoreCard.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, legalEntity, legalEntityId, domain, domainId]);
    this.fetchSearchList();
};

LEWiseScoreCard.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    if(le_id != "") {
        var jsondata = '{"domains":[{"d_id":1,"d_name":"Labour Law","le_id":1,"is_active":true},{"d_id":2,"d_name":"Finance Law","le_id":1,"is_active":true},{"d_id":3,"d_name":"Economic Law","le_id":1,"is_active":true}]}';
        var object = jQuery.parseJSON(jsondata);
        t_this._domains = object.domains;
    } else {
        displayMessage(message.legalentity_required);
    }
};
//country legalEntity domain
LEWiseScoreCard.prototype.validate = function() {
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

LEWiseScoreCard.prototype.fetchReportValues = function() {
    t_this = this;
    var jsondata = '{"data_lists":[{"c_id":1,"le_id":1,"dom_id":1,"completed_assignee_count":25,"completed_concur_count":10,"completed_approver_count":15,"inprogress_assignee_count":25,"inprogress_concur_count":10,"inprogress_approver_count":15,"overdue_assignee_count":25,"overdue_concur_count":10,"overdue_approver_count":15,"completed_unit_wise":[{"unit_name":"RG1001 - Corporate Office","submit":1,"concur":2,"approve":4},{"unit_name":"RG1002 - Regional Office","submit":1,"concur":2,"approve":4},{"unit_name":"RG1004 - Branch Office","submit":1,"concur":2,"approve":4}],"inprogress_unit_wise":[{"unit_name":"RG1001 - Corporate Office","submit":1,"concur":2,"approve":4},{"unit_name":"RG1002 - Regional Office","submit":1,"concur":2,"approve":4},{"unit_name":"RG1004 - Branch Office","submit":1,"concur":2,"approve":4}],"overdue_unit_wise":[{"unit_name":"RG1001 - Corporate Office","submit":1,"concur":2,"approve":4},{"unit_name":"RG1002 - Regional Office","submit":1,"concur":2,"approve":4},{"unit_name":"RG1004 - Branch Office","submit":1,"concur":2,"approve":4}],"overdue_user_wise":[{"user_name":"Sathish","submit":1,"concur":2,"approve":4},{"user_name":"Arun","submit":1,"concur":2,"approve":4},{"user_name":"Mani","submit":1,"concur":2,"approve":4}]}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;
};

LEWiseScoreCard.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    clientLogo.attr("src", "/files/client/common/images/yourlogo.png");
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    domainName.html(domain.val());
    var completed_count = 0;
    var inprogress_count = 0;
    var over_due_count = 0;
    $.each(data, function(k, v) {
        $('.completed-assignee-count').text(v.completed_assignee_count);
        $('.completed-concur-count').text(v.completed_concur_count);
        $('.completed-approver-count').text(v.completed_approver_count);

        $('.inprogress-assignee-count').text(v.inprogress_assignee_count);
        $('.inprogress-concur-count').text(v.inprogress_concur_count);
        $('.inprogress-approver-count').text(v.inprogress_approver_count);

        $('.overdue-assignee-count').text(v.overdue_assignee_count);
        $('.overdue-concur-count').text(v.overdue_concur_count);
        $('.overdue-approver-count').text(v.overdue_approver_count);

        completed_count = completed_count + parseInt(v.completed_assignee_count) + parseInt(v.inprogress_assignee_count) + parseInt(v.overdue_assignee_count);
        inprogress_count = inprogress_count + parseInt(v.completed_concur_count) + parseInt(v.inprogress_concur_count) + parseInt(v.overdue_concur_count);
        over_due_count = over_due_count + parseInt(v.completed_approver_count) + parseInt(v.inprogress_approver_count) + parseInt(v.overdue_approver_count);

        $('.inprogress-unit-view').on('click', function() {
            t_this.inprogressUnitView(v.inprogress_unit_wise);
        });
        $('.completed-unit-view').on('click', function() {
            t_this.completedUnitView(v.completed_unit_wise);
        });
        $('.overdue-unit-view').on('click', function() {
            t_this.overdueUnitView(v.overdue_unit_wise);
        });
    });
    $('.total-assignee-count').html(completed_count);
    $('.total-concur-count').html(inprogress_count);
    $('.total-approver-count').html(over_due_count);
};

LEWiseScoreCard.prototype.inprogressUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit Wise - In progress Within Due Date Task Count");
    $('.title-submit').html('Yet to Submit');
    $('.title-concur').html('Yet to Concurr');
    $('.title-approve').html('Yet to Approve');
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.completedUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit Wise - Completed Task Count");
    $('.title-submit').html('You Submitted');
    $('.title-concur').html('You Concurred');
    $('.title-approve').html('You Approved');
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.overdueUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit Wise - In progress Over Due Task Count");
    $('.title-submit').html('Yet to Submit');
    $('.title-concur').html('Yet to Concurr');
    $('.title-approve').html('Yet to Approve');
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.renderReportDetails = function(data) {
    taskDetails.show();
    reportTableTbody.find('tr').remove();
    var submit_total = 0;
    var concur_total = 0;
    var approve_total = 0;
    var grand_total = 0;
    var j =0;
    $.each(data, function(k, v) {
        var cloneone = $('#template #report-table .report-row').clone();
        $('.submit', cloneone).text(v.submit);
        $('.concur', cloneone).text(v.concur);
        $('.approve', cloneone).text(v.approve);
        reportTableTbody.append(cloneone);
        submit_total = submit_total + parseInt(v.submit);
        concur_total = concur_total + parseInt(v.concur);
        approve_total = approve_total + parseInt(v.approve);
        j = j + 1;
    });
    if(j > 1) {
        var clonetwo = $('#template #report-table .report-total-row').clone();
        $('.submit-total', clonetwo).text(submit_total);
        $('.concur-total', clonetwo).text(concur_total);
        $('.approve-total', clonetwo).text(approve_total);
        reportTableTbody.append(clonetwo);
    }
};

LEWiseScoreCard.prototype.exportReportValues = function() {
    alert('export');
};

LEWiseScoreCard.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        this.displayMessage("Domain name exists");
    } else {
        this.displayMessage(error);
    }
};

REPORT = new LEWiseScoreCard();

$(document).ready(function() {
    PageControls();
    REPORT.loadSearch();
});
