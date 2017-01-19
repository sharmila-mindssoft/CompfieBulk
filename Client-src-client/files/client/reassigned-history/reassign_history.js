// Declare basic elements to variable 
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

var users = $("#user");
var usersId = $("#user-id");
var acUsers = $("#ac-user");

var fromDate = $("#from-date");
var toDate = $("#to-date");

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
    // To call date picker function. assign to date field 
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

    //when click the country text box to initiate auto complete to display & get values from object 
    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._countries;
        if (countryList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        // to call auto complete common function to required variable to pass
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            // on success to return the ID and value  
            onCountryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntity.keyup(function(e) {
        var text_val = legalEntity.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
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

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var userList = REPORT._users;
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acUsers, usersId, text_val, userList, "u_name", "u_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        //if (REPORT.validate()) {
            reportView.show();
            showAnimation(reportView);
            REPORT.fetchReportValues();
            REPORT.showReportValues();
        //}
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
// on success auto complete to set the value corresponding  
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
    users.val(val[1]);
    usersId.val(val[0]);
    users.focus();
}

ReassignHistory = function() {
    this._countries = []; // To declare empty array object 
    this._entities = [];
    this._domains = [];
    this._units = [];
    this._acts = [];
    this._compliance_task = [];
    this._users = [];
    this._report_data = [];
}

ReassignHistory.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, legalEntity, legalEntityId, domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId, fromDate, toDate]);
    this.fetchSearchList();
};

ReassignHistory.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getUserLegalEntity();
    
    //var jsondata = '{"countries":[{"c_id":1,"c_name":"india","is_active":true},{"c_id":2,"c_name":"srilanka","is_active":true}],"entities":[{"le_id":1,"c_id":1,"le_name":"RG Legal Entity","is_active":true},{"le_id":2,"c_id":1,"le_name":"ABC Legal Entity","is_active":true}],"users":[{"u_id":1,"u_name":"Siva ","is_active":true},{"u_id":2,"u_name":"Hari","is_active":true}]}';
    //var object = jQuery.parseJSON(jsondata);
    client_mirror.getReassignedHistoryReportFilters(function(error, response) {
        if (error == null) {
            t_this._countries = response.countries;
        } else {
            t_this.possibleFailures(error);
        }
    });
};

ReassignHistory.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    var jsondata = '{"domains":[{"d_id":1,"d_name":"Labour Law","le_id":1,"is_active":true},{"d_id":2,"d_name":"Finance Law","le_id":2,"is_active":true},{"d_id":3,"d_name":"Employee Law","le_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._domains = object.domains;
};

ReassignHistory.prototype.fetchUnitList = function(dom_id) {
    t_this = this;
    var jsondata = '{"units":[{"u_id":1,"u_name":"RG Madurai Unit","u_code":"RG1034","address":"12 RJ Complex, Main road, Madurai, 625022","d_id":1,"is_active":true},{"u_id":2,"u_name":"RG Dindugal Unit","u_code":"RG1035","address":"10 RG Complex, Main road, Dindugal, 623020","d_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._units = object.units;
};

ReassignHistory.prototype.fetchActList = function(unit_id) {
    t_this = this;
    var jsondata = '{"acts":[{"act_id":1,"act_name":"The Batteries Act","u_id":1,"is_active":true},{"act_id":2,"act_name":"Indian Partnership Act, 1932","u_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._acts = object.acts;
};

ReassignHistory.prototype.fetchComplianceaskList = function(act_id) {
    t_this = this;
    var jsondata = '{"compliance_task":[{"c_id":1,"c_task":"FORM I - Half yearly returns Submission","act_id":1,"is_active":true},{"c_id":2,"c_task":"FORM II - Registration","act_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._compliance_task = object.compliance_task;
};

ReassignHistory.prototype.validate = function() {
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
    if (users) {
        if (isLengthMinMax(users, 0, 50, message.user_max) == false)
            return false;
        else if (isCommonName(users, message.user_str) == false)
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

ReassignHistory.prototype.fetchReportValues = function() {
    t_this = this;
    var jsondata = '{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Aug-2016","assigned":"EMP0016 - Rajkumar / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Approved"},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Jun-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Assignee Re-deployed"},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Jan-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":""},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form B - Annual Returns Submission","due_date":"01-Sep-2016","assigned_date":"20-Aug-2016","assigned":"EEMP0016 -Rajkumar / EMP0013 - Suresh / EMP0014 -Praveen","reason":"Role Changed"},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form B - Annual Returns Submission","due_date":"01-Sep-2016","assigned_date":"01-Jan-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Assignee Re-deployed"}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;
};

ReassignHistory.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    clientLogo.attr("src", "/files/client/common/images/yourlogo.png");
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    domainName.html(domain.val());
    var j = 0;
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
            j = j + 1;
            var clonethree = $('#template #report-table .row-three').clone();
            $('.sno', clonethree).text(j);
            $('.compliance-task', clonethree).text(v.compliance_task);
            $('.due-date', clonethree).text(v.due_date);
            $('.assigned-date', clonethree).text(v.assigned_date);
            $('.assigned', clonethree).text(v.assigned);
            if (v.reason != "") { $('.reason', clonefour).text(v.reason); } else { $('.reason', clonefour).text('-'); }
            reportTableTbody.append(clonethree);
            complianceTask = v.compliance_task;
        } else {
            var clonefour = $('#template #report-table .row-four').clone();
            $('.assigned-date-new', clonefour).text(v.assigned_date);
            $('.assigned-new', clonefour).text(v.assigned);
            $('.reason-new', clonefour).text(v.reason);
            if (v.reason != "") { $('.reason-new', clonefour).text(v.reason); } else { $('.reason-new', clonefour).text('-'); }
            reportTableTbody.append(clonefour);
            complianceTask = v.compliance_task;
        }
    });
    totalRecord.html(j);
};

ReassignHistory.prototype.exportReportValues = function() {
    alert('export');
};

ReassignHistory.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        this.displayMessage("Domain name exists");
    } else {
        this.displayMessage(error);
    }
};

// call class ReassignHistory to store the REPORT object
REPORT = new ReassignHistory();

$(document).ready(function() {
    // To initially to call the page controller what are the activity to set in page controller
    PageControls();
    // To store values in object & search list element 
    REPORT.loadSearch();
});
