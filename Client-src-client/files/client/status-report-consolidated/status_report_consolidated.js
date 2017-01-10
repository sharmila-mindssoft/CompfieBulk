var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");

var legalEntity = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");

var domain = $("#domain");
var domainId = $("#domain-id");
var acDomain = $("#ac-domain");

var unit = $("#unit");
var unitId = $("#unit-id");
var acUnit = $("#ac-unit");

var act = $("#act");
var actId = $("#act-id");
var acAct = $("#ac-act");

var complianceTask = $("#compliance-task");
var complianceTaskId = $("#compliance-task-id");
var acComplianceTask = $("#ac-compliance-task");

var complianceFrequency = $("#compliance-frequency");
var userType = $("#user-type");
var user = $("#user");
var userId = $("#user-id");
var acUser = $("#ac-user");
var fromDate = $("#from-date");
var toDate = $("#to-date");
var complianceTaskStatus = $("#compliance-task-status");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var clientLogo = $("#client-logo");
var legalEntityName = $("#legal-entity-name");
var countryName = $("#country-name");
var domainName = $("#domain-name");
var reportTableTbody = $("#report-table-tbody");
var template = $("#template");
var reportTable = $("#report-table");
var totalRecord = $("#total-record");
var REPORT = null;

function PageControls() {
    $(".from-date, .to-date").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-M-yy",
        onSelect: function(selectedDate) {
            if ($(this).hasClass("from-date") == true) {
                var dateMin = $('.from-date').datepicker("getDate");
                var rMin = new Date(dateMin.getFullYear(), dateMin.getMonth(), dateMin.getDate()); // +1
                $('.to-date').datepicker("option", "minDate", rMin);
            }
            if ($(this).hasClass("to-date") == true) {
                var dateMin = $('.to-date').datepicker("getDate");
            }
        }
    });

    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._countries;
        if (countryList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        //alert(text_val +' - '+countryList.toSource() +' - '+)
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

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = REPORT._units;
        if (unitList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "u_name", "u_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._acts;
        if (actList.length == 0)
            displayMessage(message.act_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acAct, actId, text_val, actList, "act_name", "act_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        if (complianceTaskList.length == 0)
            displayMessage(message.complianceTask_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acComplianceTask, complianceTaskId, text_val, complianceTaskList, "c_task", "c_id", function(val) {
            onComplianceTaskAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    user.keyup(function(e) {
        var text_val = user.val().trim();
        var userList = REPORT._users;
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acUser, userId, text_val, userList, "u_name", "u_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            reportView.show();
            showAnimation(reportView);
            REPORT.fetchReportValues();
            REPORT.showReportValues();
        }
    });

    exportButton.click(function() {
        if (REPORT.validate()) {
            REPORT.fetchReportValues()
            REPORT.exportReportValues();
        }
    });

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
    clearElement([legalEntity, legalEntityId, domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    legalEntity.val(val[1]);
    legalEntityId.val(val[0]);
    legalEntity.focus();
    clearElement([domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchDomainList(val[0]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([unit, unitId, act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchUnitList(val[0]);
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchActList(val[0]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
    clearElement([complianceTask, complianceTaskId]);
    REPORT.fetchComplianceaskList(val[0]);
}

onComplianceTaskAutoCompleteSuccess = function(REPORT, val) {
    complianceTask.val(val[1]);
    complianceTaskId.val(val[0]);
    complianceTask.focus();
}

onUserAutoCompleteSuccess = function(REPORT, val) {
    user.val(val[1]);
    userId.val(val[0]);
    user.focus();
}

StatusReportConsolidated = function() {
    this._countries = [];
    this._entities = [];
    this._domains = [];
    this._units = [];
    this._acts = [];
    this._compliance_task = [];
    this._frequencies = [];
    this._user_type = [];
    this._users = [];
    this._compliance_task_status = [];
    this._service_providers = [];
    this._report_data = [];
}

StatusReportConsolidated.prototype.loadSearch = function() {
    reportView.hide();
    country.empty();
    legalEntity.empty();
    domain.val('');
    domainId.val('');
    unit.val('');
    unitId.val('');
    act.val('');
    actId.val('');
    complianceTask.val('');
    complianceTaskId.val('');
    complianceFrequency.empty();
    userType.empty();
    user.val('');
    userId.val('');
    fromDate.val('');
    toDate.val('');
    complianceTaskStatus.empty();
    this.fetchSearchList();
};

StatusReportConsolidated.prototype.fetchSearchList = function() {
    t_this = this;
    var jsondata = '{"countries":[{"c_id":1,"c_name":"india","is_active":true},{"c_id":2,"c_name":"srilanka","is_active":true}],"entities":[{"le_id":1,"c_id":1,"le_name":"RG Legal Entity","is_active":true},{"le_id":2,"c_id":1,"le_name":"ABC Legal Entity","is_active":true}],"frequencies":[{"f_id":1,"f_name":"Periodical"},{"f_id":2,"f_name":"Review"},{"f_id":3,"f_name":"Flexi Review"},{"f_id":4,"f_name":"One Time"}],"user_type":[{"user_type_id":1,"user_type_name":"Assignee"},{"user_type_id":2,"user_type_name":"Concurrence"},{"user_type_id":3,"user_type_name":"Approval"}],"compliance_task_status":[{"comp_task_status_id":1,"comp_task_status":"Complied"},{"comp_task_status_id":2,"comp_task_status":"Delayed Compliances"},{"comp_task_status_id":3,"comp_task_status":"Inprogress"},{"comp_task_status_id":4,"comp_task_status":"Not Complied"}],"service_providers":[{"s_p_id":1,"s_p_name":"String","s_p_shrot":"short"}],"users":[{"u_id":1,"u_name":"Siva ","is_active":true},{"u_id":2,"u_name":"Hari","is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._countries = object.countries;
    t_this._entities = object.entities;
    t_this._frequencies = object.frequencies;
    t_this._userType = object.user_type;
    t_this._users = object.users;
    t_this._complianceTaskStatus = object.compliance_task_status;
    t_this._serviceProviders = object.service_providers;

    t_this.renderCountriesList(t_this._countries);
    t_this.renderLegalEntityList(t_this._entities);
    t_this.renderComplianceFrequencyList(t_this._frequencies);
    t_this.renderUserTypeList(t_this._userType);
    t_this.renderComplianceTaskStatusList(t_this._complianceTaskStatus);
};

StatusReportConsolidated.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    var jsondata = '{"domains":[{"d_id":1,"d_name":"Labour Law","le_id":1,"is_active":true},{"d_id":2,"d_name":"Finance Law","le_id":2,"is_active":true},{"d_id":3,"d_name":"Employee Law","le_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._domains = object.domains;
};

StatusReportConsolidated.prototype.fetchUnitList = function(dom_id) {
    t_this = this;
    var jsondata = '{"units":[{"u_id":1,"u_name":"RG Madurai Unit","u_code":"RG1034","address":"12 RJ Complex, Main road, Madurai, 625022","d_id":1,"is_active":true},{"u_id":2,"u_name":"RG Dindugal Unit","u_code":"RG1035","address":"10 RG Complex, Main road, Dindugal, 623020","d_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._units = object.units;
};

StatusReportConsolidated.prototype.fetchActList = function(unit_id) {
    t_this = this;
    var jsondata = '{"acts":[{"act_id":1,"act_name":"The Batteries Act","u_id":1,"is_active":true},{"act_id":2,"act_name":"Indian Partnership Act, 1932","u_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._acts = object.acts;
};

StatusReportConsolidated.prototype.fetchComplianceaskList = function(act_id) {
    t_this = this;
    var jsondata = '{"compliance_task":[{"c_id":1,"c_task":"FORM I - Half yearly returns Submission","act_id":1,"is_active":true},{"c_id":2,"c_task":"FORM II - Registration","act_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._compliance_task = object.compliance_task;
};

StatusReportConsolidated.prototype.renderCountriesList = function(data) {
    t_this = this;
    country.empty();
    var countryName = [];
    $.each(data, function(i, e) {
        //countryName.push(e.c_name+",");
        countryName = e.c_name;
    });
    country.html(countryName);
};

StatusReportConsolidated.prototype.renderLegalEntityList = function(data) {
    t_this = this;
    legalEntity.empty();
    var legalEntityName = [];
    $.each(data, function(i, e) {
        //legalEntityName.push(e.le_name+",");
        legalEntityName = e.le_name;
    });
    legalEntity.html(legalEntityName);
};

StatusReportConsolidated.prototype.renderComplianceFrequencyList = function(data) {
    t_this = this;
    complianceFrequency.empty();
    var complianceFrequencyList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceFrequencyList = complianceFrequencyList + '<option value="' + e.f_id + '"> ' + e.f_name + ' </option>';
    });
    complianceFrequency.html(complianceFrequencyList);
};

StatusReportConsolidated.prototype.renderUserTypeList = function(data) {
    t_this = this;
    userType.empty();
    var userTypeList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        userTypeList = userTypeList + '<option value="' + e.user_type_id + '"> ' + e.user_type_name + ' </option>';
    });
    userType.html(userTypeList);
};

StatusReportConsolidated.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.comp_task_status_id + '"> ' + e.comp_task_status + ' </option>';
    });
    complianceTaskStatus.html(complianceTaskStatusList);
};

StatusReportConsolidated.prototype.validate = function() {
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
        else if (isLengthMinMax(domain, 1, 50, message.domain_max) == false)
            return false;
        else if (isCommonName(domain, message.domain_str) == false)
            return false;
    }
    if (unit) {
        if (isLengthMinMax(unit, 0, 50, message.unit_max) == false)
            return false;
        else if (isCommonName(unit, message.unit_str) == false)
            return false;
    }
    if (act) {
        if (isLengthMinMax(act, 0, 50, message.act_max) == false)
            return false;
        else if (isCommonName(act, message.act_str) == false)
            return false;
    }
    if (complianceTask) {
        if (isLengthMinMax(complianceTask, 0, 50, message.complianceTask_max) == false)
            return false;
        else if (isCommonName(complianceTask, message.complianceTask_str) == false)
            return false;
    }
    if (user) {
        if (isLengthMinMax(user, 0, 50, message.user_max) == false)
            return false;
        else if (isCommonName(user, message.user_str) == false)
            return false;
    }
    if (fromDate) {
        if (isNotEmpty(fromDate, message.fromdate_required) == false)
            return false;
    }
    if (toDate) {
        if (isNotEmpty(toDate, message.todate_required) == false)
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

StatusReportConsolidated.prototype.fetchReportValues = function() {
    t_this = this;
    var jsondata = '{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Test Act","compliance_task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1004 - Suresh","activity_status":"Approved","activity_date":"20-Aug-2016","doc_list":[],"completion_date":"18-Aug-2016","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Test Act","compliance_task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1002 - Rajkumar","activity_status":"Submitted","activity_date":"18-Aug-2016","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/status-report-consolidated"}],"completion_date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1035 - RG Chennai Unit - 23, K.K.Nagar, Chennai-600025","l_name":"PF Act","compliance_task":"FORM VIII - Notice of Opening","frequency":"One Time","due_date":"20-Aug-2016","task_status":"Inprogress","user_name":"EMP1004 - Suresh","activity_status":"Pending","activity_date":"","doc_list":[],"completion_date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1035 - RG Chennai Unit - 23, K.K.Nagar, Chennai-600025","l_name":"PF Act","compliance_task":"FORM VIII - Notice of Opening","frequency":"One Time","due_date":"20-Aug-2016","task_status":"Inprogress","user_name":"EMP1002 - Rajkumar","activity_status":"Submitted","activity_date":"19-Aug-2016","doc_list":[{"doc_name":"Document 2","doc_url":"http://localhost:8083/status-report-consolidated"}],"completion_date":"","com_id":1,"f_id":1}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;
};

StatusReportConsolidated.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    clientLogo.attr("src", "/files/client/common/images/yourlogo.png");
    legalEntityName.html(legalEntity.html());
    countryName.html(country.html());
    domainName.html(domain.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var unitname = "";
    var actname = "";
    var complianceTask = "";
    $.each(data, function(k, v) {
        if (unitname != v.u_name) {
            var cloneone = $('#template #report-table .row-one').clone();
            $('.unit-name', cloneone).text(v.u_name);
            reportTableTbody.append(cloneone);
            unitname = v.u_name;
        }

        if (actname != v.l_name) {
            var clonetwo = $('#template #report-table .row-two').clone();
            $('.act-name', clonetwo).text(v.l_name);
            reportTableTbody.append(clonetwo);
            actname = v.l_name;
        }

        if (complianceTask != v.compliance_task) {
            var clonethree = $('#template #report-table .row-three').clone();
            $('.sno', clonethree).text(j);
            $('.compliance-task', clonethree).text(v.compliance_task);
            $('.frequency', clonethree).text(v.frequency);
            $('.due-date', clonethree).text(v.due_date);
            $('.compliance-task-status', clonethree).text(v.task_status);
            $('.user-name', clonethree).text(v.user_name);
            $('.activity-status', clonethree).text(v.activity_status);
            if (v.activity_date != "")
                $('.activity-date', clonethree).text(v.activity_date);
            else
                $('.activity-date', clonethree).text('-');
            if (v.doc_list.length > 0) {
                $.each(v.doc_list, function(k1, v1) {
                    $('.uploaded-document a', clonethree).text(v1.doc_name).attr("href", v1.doc_url);
                });
            } else {
                $('.uploaded-document', clonethree).text('-');
            }

            if (v.completion_date != "")
                $('.completion-date', clonethree).text(v.completion_date);
            else
                $('.completion-date', clonethree).text('-');
            reportTableTbody.append(clonethree);
            j = j + 1;
            complianceTask = v.compliance_task;
        } else {
            var clonefour = $('#template #report-table .row-four').clone();
            $('.user-name-new', clonefour).text(v.user_name);
            $('.activity-status-new', clonefour).text(v.activity_status);
            if (v.activity_date != "")
                $('.activity-date-new', clonefour).text(v.activity_date);
            else
                $('.activity-date-new', clonefour).text('-');
            if (v.doc_list.length > 0) {
                $.each(v.doc_list, function(k1, v1) {
                    $('.uploaded-document-new a', clonefour).text(v1.doc_name).attr("href", v1.doc_url);
                });
            } else {
                $('.uploaded-document-new', clonefour).text('-');
            }

            if (v.completion_date != "")
                $('.completion-date-new', clonefour).text(v.completion_date);
            else
                $('.completion-date-new', clonefour).text('-');
            reportTableTbody.append(clonefour);
            j = j + 1;
            complianceTask = v.compliance_task;
        }
    });
    totalRecord.html(j);
};

StatusReportConsolidated.prototype.exportReportValues = function() {
    alert('export');
};

StatusReportConsolidated.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        this.displayMessage("Domain name exists");
    } else {
        this.displayMessage(error);
    }
};

REPORT = new StatusReportConsolidated();

$(document).ready(function() {
    PageControls();
    REPORT.loadSearch();
});
