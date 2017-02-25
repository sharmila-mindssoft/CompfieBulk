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

var statusDetails = $("#status-details");
var template = $("#template");
var reportTable = $("#report-table");
var REPORT = null;

LEWiseScoreCard = function() {
    this._entities = [];
    this._domains = [];
    this._report_data = [];
}

LEWiseScoreCard.prototype.fetchSearchList = function() {
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
        var condition_values = [true, 1];
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
    /*if(le_id != "") {
        var jsondata = '{"domains":[{"d_id":1,"d_name":"Labour Law","le_id":1,"is_active":true},{"d_id":2,"d_name":"Finance Law","le_id":1,"is_active":true},{"d_id":3,"d_name":"Economic Law","le_id":1,"is_active":true}]}';
        var object = jQuery.parseJSON(jsondata);
        t_this._domains = object.domains;
    } else {
        displayMessage(message.legalentity_required);
    }*/
    client_mirror.getLEWiseScoreCardFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
        } else {
            t_this.possibleFailures(error);
        }
    });
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

LEWiseScoreCard.prototype.fetchReportValues = function(csv) {
    t_this = this;
    /*var jsondata = '{"data_lists":[{"c_id":1,"le_id":1,"dom_id":1,"inprogress_count":25,"inprogress_unit_wise":[{"unit_name":"RG1001 - Corporate Office","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"unit_name":"RG1002 - Regional Office","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"unit_name":"RG1004 - Branch Office","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"inprogress_user_wise":[{"user_name":"Sathish","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"user_name":"Arun","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"user_name":"Mani","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"completed_count":10,"completed_unit_wise":[{"unit_name":"RG1001 - Corporate Office","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"unit_name":"RG1002 - Regional Office","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"unit_name":"RG1004 - Branch Office","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"completed_user_wise":[{"user_name":"Sathish","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"user_name":"Arun","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"user_name":"Mani","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"overdue_count":15,"overdue_unit_wise":[{"unit_name":"RG1001 - Corporate Office","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"unit_name":"RG1002 - Regional Office","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"unit_name":"RG1004 - Branch Office","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}],"overdue_user_wise":[{"user_name":"Sathish","to_complete":1,"to_concur":2,"to_approve":4,"total_task":7},{"user_name":"Arun","to_complete":2,"to_concur":5,"to_approve":2,"total_task":9},{"user_name":"Mani","to_complete":5,"to_concur":3,"to_approve":1,"total_task":9}]}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;*/

    var c_id = parseInt(countryId.val());
    var le_id = parseInt(legalEntityId.val());
    var d_id = parseInt(domainId.val());

    client_mirror.getLEWiseScoreCard(c_id, le_id, d_id, csv, function(error, response) {
        if (error == null) {
            t_this._report_data = response.le_wise_score_card_list;
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
    });
};

LEWiseScoreCard.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    clientLogo.attr("src", "/files/client/common/images/yourlogo.png");
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    domainName.html(domain.val());
    $.each(data, function(k, v) {
        $('.inprogress-count').text(v.inprogress_count);
        $('.completed-count').text(v.completed_count);
        $('.overdue-count').text(v.overdue_count);
        var total = parseInt(v.inprogress_count) + parseInt(v.completed_count) + parseInt(v.overdue_count);
        $('.total-count').html(total);
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
};

LEWiseScoreCard.prototype.inprogressUnitView = function(data) {
    t_this = this;
    statusDetails.empty();
    taskDetails.show();
    $('.task-name').html("Unit wise Inprogress Task Count");
    var to_complete_total = 0;
    var to_concur_total = 0;
    var to_approve_total = 0;
    var grand_total = 0;
    var j =0;
    var clone = $('#template #inprogress-unit-table').clone();
    var name = "";
    $.each(data, function(k, v) {
        var total_task = parseInt(v.to_complete) + parseInt(v.to_approve) + parseInt(v.to_concur)
        if(name != "") {
            var cloneone = $('.report-row', clone).last().clone();
            $('.task-row-title', cloneone).text(v.unit);
            $('.to-complete', cloneone).text(v.to_complete);
            $('.to-concur', cloneone).text(v.to_concur);
            $('.to-approve', cloneone).text(v.to_approve);
            $('.total-task', cloneone).text(total_task);
            $('.table-body', clone).append(cloneone);
            name = name + v.unit;
        } else {
            $('.task-row-title', clone).text(v.unit);
            $('.to-complete', clone).text(v.to_complete);
            $('.to-concur', clone).text(v.to_concur);
            $('.to-approve', clone).text(v.to_approve);
            $('.total-task', clone).text(total_task);
            name = name + v.unit;
        }
        to_complete_total = to_complete_total + parseInt(v.to_complete);
        to_concur_total = to_concur_total + parseInt(v.to_concur);
        to_approve_total = to_approve_total + parseInt(v.to_approve);
        grand_total = grand_total + total_task;
        j = j + 1;
    });
    if(j > 1) {
        $('.to-complete-total', clone).text(to_complete_total);
        $('.to-concur-total', clone).text(to_concur_total);
        $('.to-approve-total', clone).text(to_approve_total);
        $('.grand-total', clone).text(grand_total);
        $('.report-total-row', clone).attr("style", "");
    }
    statusDetails.append(clone);
};

LEWiseScoreCard.prototype.inprogressUserView = function(data) {
    t_this = this;
    statusDetails.empty();
    taskDetails.show();
    $('.task-name').html("User wise Inprogress Task Count");
    var to_complete_total = 0;
    var to_concur_total = 0;
    var to_approve_total = 0;
    var grand_total = 0;
    var j =0;
    var clone = $('#template #inprogress-user-table').clone();
    var name = "";
    $.each(data, function(k, v) {
        var total_task = parseInt(v.to_complete) + parseInt(v.to_approve) + parseInt(v.to_concur)
        if(name != "") {
            var cloneone = $('.report-row', clone).last().clone();
            $('.task-row-title', cloneone).text(v.user_name);
            $('.to-complete', cloneone).text(v.to_complete);
            $('.to-concur', cloneone).text(v.to_concur);
            $('.to-approve', cloneone).text(v.to_approve);
            $('.total-task', cloneone).text(total_task);
            $('.table-body', clone).append(cloneone);
            name = name + v.user_name;
        } else {
            $('.task-row-title', clone).text(v.user_name);
            $('.to-complete', clone).text(v.to_complete);
            $('.to-concur', clone).text(v.to_concur);
            $('.to-approve', clone).text(v.to_approve);
            $('.total-task', clone).text(total_task);
            name = name + v.user_name;
        }
        to_complete_total = to_complete_total + parseInt(v.to_complete);
        to_concur_total = to_concur_total + parseInt(v.to_concur);
        to_approve_total = to_approve_total + parseInt(v.to_approve);
        grand_total = grand_total + total_task;
        j = j + 1;
    });
    if(j > 1) {
        $('.to-complete-total', clone).text(to_complete_total);
        $('.to-concur-total', clone).text(to_concur_total);
        $('.to-approve-total', clone).text(to_approve_total);
        $('.grand-total', clone).text(grand_total);
        $('.report-total-row', clone).attr("style", "");
    }
    statusDetails.append(clone);
};

LEWiseScoreCard.prototype.completedUnitView = function(data) {
    t_this = this;
    statusDetails.empty();
    taskDetails.show();
    $('.task-name').html("Unit wise Completed Task Count");
    var delayed_count_total = 0;
    var complied_count_total = 0;
    var grand_total = 0;
    var j =0;
    var clone = $('#template #completed-unit-table').clone();
    var name = "";
    $.each(data, function(k, v) {
        var total_task = parseInt(v.delayed_count) + parseInt(v.complied_count)
        if(name != "") {
            var cloneone = $('.report-row', clone).last().clone();
            $('.task-row-title', cloneone).text(v.unit);
            $('.delayed-count', cloneone).text(v.delayed_count);
            $('.complied-count', cloneone).text(v.complied_count);
            $('.total-task', cloneone).text(total_task);
            $('.table-body', clone).append(cloneone);
            name = name + v.unit;
        } else {
            $('.task-row-title', clone).text(v.unit);
            $('.delayed-count', clone).text(v.delayed_count);
            $('.complied-count', clone).text(v.complied_count);
            $('.total-task', clone).text(total_task);
            name = name + v.unit;
        }
        delayed_count_total = delayed_count_total + parseInt(v.delayed_count);
        complied_count_total = complied_count_total + parseInt(v.complied_count);
        grand_total = grand_total + total_task;
        j = j + 1;
    });
    if(j > 1) {
        $('.delayed-count-total', clone).text(delayed_count_total);
        $('.complied-count-total', clone).text(complied_count_total);
        $('.grand-total', clone).text(grand_total);
        $('.report-total-row', clone).attr("style", "");
    }
    statusDetails.append(clone);
};

LEWiseScoreCard.prototype.completedUserView = function(data) {
    t_this = this;
    statusDetails.empty();
    taskDetails.show();
    $('.task-name').html("User wise Completed Task Count");
    var delayed_count_total = 0;
    var complied_count_total = 0;
    var grand_total = 0;
    var j =0;
    var clone = $('#template #completed-user-table').clone();
    var name = "";
    $.each(data, function(k, v) {
        var total_task = parseInt(v.delayed_count) + parseInt(v.complied_count)
        if(name != "") {
            var cloneone = $('.report-row', clone).last().clone();
            $('.task-row-title', cloneone).text(v.user_name);
            $('.delayed-count', cloneone).text(v.delayed_count);
            $('.complied-count', cloneone).text(v.complied_count);
            $('.total-task', cloneone).text(total_task);
            $('.table-body', clone).append(cloneone);
            name = name + v.user_name;
        } else {
            $('.task-row-title', clone).text(v.user_name);
            $('.delayed-count', clone).text(v.delayed_count);
            $('.complied-count', clone).text(v.complied_count);
            $('.total-task', clone).text(total_task);
            name = name + v.user_name;
        }
        delayed_count_total = delayed_count_total + parseInt(v.delayed_count);
        complied_count_total = complied_count_total + parseInt(v.complied_count);
        grand_total = grand_total + total_task;
        j = j + 1;
    });
    if(j > 1) {
        $('.delayed-count-total', clone).text(delayed_count_total);
        $('.complied-count-total', clone).text(complied_count_total);
        $('.grand-total', clone).text(grand_total);
        $('.report-total-row', clone).attr("style", "");
    }
    statusDetails.append(clone);
};

LEWiseScoreCard.prototype.overdueUnitView = function(data) {
    t_this = this;
    statusDetails.empty();
    taskDetails.show();
    $('.task-name').html("Unit wise Overdue Task Count");
    var overdue_total = 0;
    var j =0;
    var clone = $('#template #overdue-unit-table').clone();
    var name = "";
    $.each(data, function(k, v) {
        if(name != "") {
            var cloneone = $('.report-row', clone).last().clone();
            $('.task-row-title', cloneone).text(v.unit);
            $('.overdue-count', cloneone).text(v.overdue_count);
            $('.table-body', clone).append(cloneone);
            name = name + v.unit;
        } else {
            $('.task-row-title', clone).text(v.unit);
            $('.overdue-count', clone).text(v.overdue_count);
            name = name + v.unit;
        }
        overdue_total = overdue_total + parseInt(v.overdue_count);
        j = j + 1;
    });
    if(j > 1) {
        $('.overdue-count-total', clone).text(overdue_total);
        $('.report-total-row', clone).attr("style", "");
    }
    statusDetails.append(clone);
};

LEWiseScoreCard.prototype.overdueUserView = function(data) {
    t_this = this;
    statusDetails.empty();
    taskDetails.show();
    $('.task-name').html("Completed wise Completed Task Count");
    var overdue_total = 0;
    var j =0;
    var clone = $('#template #overdue-user-table').clone();
    var name = "";
    $.each(data, function(k, v) {
        if(name != "") {
            var cloneone = $('.report-row', clone).last().clone();
            $('.task-row-title', cloneone).text(v.user_name);
            $('.overdue-count', cloneone).text(v.overdue_count);
            $('.table-body', clone).append(cloneone);
            name = name + v.user_name;
        } else {
            $('.task-row-title', clone).text(v.user_name);
            $('.overdue-count', clone).text(v.overdue_count);
            name = name + v.user_name;
        }
        overdue_total = overdue_total + parseInt(v.overdue_count);
        j = j + 1;
    });
    if(j > 1) {
        $('.overdue-count-total', clone).text(overdue_total);
        $('.report-total-row', clone).attr("style", "");
    }
    statusDetails.append(clone);
};

LEWiseScoreCard.prototype.exportReportValues = function() {
    alert('export');
};

LEWiseScoreCard.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
    }
};

LEWiseScoreCard.prototype.loadEntityDetails = function(){
    t_this = this;
    if(t_this._entities.length > 1) {
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
};

REPORT = new LEWiseScoreCard();

$(document).ready(function() {
    PageControls();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});
