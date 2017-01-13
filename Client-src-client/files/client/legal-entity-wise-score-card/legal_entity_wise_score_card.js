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
    var jsondata = '{"data_lists":[{"c_id":1,"le_id":1,"dom_id":1,"inprogress_count":25,"inprogress_unit_wise":[{"unit_name":"RG1001 - Corporate Office","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"unit_name":"RG1002 - Regional Office","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"unit_name":"RG1004 - Branch Office","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"inprogress_user_wise":[{"user_name":"Sathish","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"user_name":"Arun","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"user_name":"Mani","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"completed_count":10,"completed_unit_wise":[{"unit_name":"RG1001 - Corporate Office","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"unit_name":"RG1002 - Regional Office","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"unit_name":"RG1004 - Branch Office","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"completed_user_wise":[{"user_name":"Sathish","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"user_name":"Arun","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"user_name":"Mani","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"overdue_count":15,"overdue_unit_wise":[{"unit_name":"RG1001 - Corporate Office","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"unit_name":"RG1002 - Regional Office","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"unit_name":"RG1004 - Branch Office","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"overdue_user_wise":[{"user_name":"Sathish","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"user_name":"Arun","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"user_name":"Mani","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}]}]}';
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
    var total = 0;
    $.each(data, function(k, v) {
        $('.inprogress-count').text(v.inprogress_count);
        $('.completed-count').text(v.completed_count);
        $('.overdue-count').text(v.overdue_count);
        total = parseInt(v.inprogress_count) + parseInt(v.completed_count) + parseInt(v.over_due_count);

        $('.inprogress-unit-view').on('click', function() {
            t_this.inprogressUnitView(v.inprogress_unit_wise);
        });
        $('.inprogress-user-view').on('click', function() {
            t_this.inprogressUserView(v.inprogress_user_wise);
        });

        $('.completed-unit-view').on('click', function() {
            t_this.completedUnitView(v.completed_unit_wise);
        });
        $('.completed-user-view').on('click', function() {
            t_this.completedUserView(v.completed_user_wise);
        });

        $('.overdue-unit-view').on('click', function() {
            t_this.overdueUnitView(v.overdue_unit_wise);
        });
        $('.overdue-user-view').on('click', function() {
            t_this.overdueUserView(v.overdue_user_wise);
        });
    });
    $('.total-count').html(total);
};

LEWiseScoreCard.prototype.inprogressUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit wise Inprogress Task Count");
    $('.task-title').html("Unit");
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.inprogressUserView = function(data) {
    t_this = this;
    $('.task-name').html("User wise Inprogress Task Count");
    $('.task-title').html("Users");
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.completedUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit wise Completed Task Count");
    $('.task-title').html("Unit");
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.completedUserView = function(data) {
    t_this = this;
    $('.task-name').html("User wise Completed Task Count");
    $('.task-title').html("Users");
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.overdueUnitView = function(data) {
    t_this = this;
    $('.task-name').html("Unit wise Over due Task Count");
    $('.task-title').html("Unit");
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.overdueUserView = function(data) {
    t_this = this;
    $('.task-name').html("User wise Over due Task Count");
    $('.task-title').html("Users");
    t_this.renderReportDetails(data);
};

LEWiseScoreCard.prototype.renderReportDetails = function(data) {
    taskDetails.show();
    reportTableTbody.find('tr').remove();
    var to_complete_total = 0;
    var to_concur_total = 0;
    var to_approve_total = 0;
    var grand_total = 0;
    var j =0;
    $.each(data, function(k, v) {
        var cloneone = $('#template #report-table .report-row').clone();
        if(v.unit_name)
            $('.task-row-title', cloneone).text(v.unit_name);
        else
            $('.task-row-title', cloneone).text(v.user_name);
        $('.to-complete', cloneone).text(v.to_complete);
        $('.to-concur', cloneone).text(v.to_concur);
        $('.to-approve', cloneone).text(v.to_approve);
        $('.total-task', cloneone).text(v.total_task);
        reportTableTbody.append(cloneone);
        to_complete_total = to_complete_total + parseInt(v.to_complete);
        to_concur_total = to_concur_total + parseInt(v.to_concur);
        to_approve_total = to_approve_total + parseInt(v.to_approve);
        grand_total = grand_total + parseInt(v.total_task);
        j = j + 1;
    });
    if(j > 1) {
        var clonetwo = $('#template #report-table .report-total-row').clone();
        $('.to-complete-total', clonetwo).text(to_complete_total);
        $('.to-concur-total', clonetwo).text(to_concur_total);
        $('.to-approve-total', clonetwo).text(to_approve_total);
        $('.grand-total', clonetwo).text(grand_total);
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
