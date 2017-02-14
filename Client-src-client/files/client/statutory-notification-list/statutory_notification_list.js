// Declare basic elements to variable 
var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");

var domain = $("#domain");
var domainId = $("#domain-id");
var acDomain = $("#ac-domain");

var act = $("#act");
var actId = $("#act-id");
var acAct = $("#ac-act");

var fromDate = $("#from-date");
var toDate = $("#to-date");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var countryName = $("#country-name");
var domainName = $("#domain-name");
var reportTableTbody = $("#report-table-tbody");
var template = $("#template");
var reportTable = $("#report-table");
var totalRecord = $("#total-record");
var treeShowHide = $(".row-three");
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

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, legalEntityId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._acts;
        if (actList.length == 0)
            displayMessage(message.act_required);
        var condition_fields = ["d_id"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acAct, actId, text_val, actList, "act", "act", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            reportView.show();
            showAnimation(reportView);
            var c_id = parseInt(countryId.val());
            var d_id = parseInt(domainId.val());
            var act = actId.val();
            if (!act) act = null
            var from_date = fromDate.val();
            var to_date = toDate.val();
            var csv = false;
            REPORT.fetchReportValues(c_id, d_id, act, from_date, to_date, csv);
        }
    });

 exportButton.click(function() {
        if (REPORT.validate()) {
            reportView.show();
            showAnimation(reportView);
            var c_id = parseInt(countryId.val());
            var d_id = parseInt(domainId.val());
            var act = actId.val();
            if (!act) act = null
            var from_date = fromDate.val();
            var to_date = toDate.val();
            var csv = false;
            REPORT.fetchReportValues(c_id, d_id, act, from_date, to_date, csv);
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
    clearElement([domain, domainId, act, actId]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([act, actId]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
}

ReassignHistory = function() {
    this._countries = []; // To declare empty array object 
    this._domains = [];
    this._acts = [];
    this._report_data = [];
    this._total_count = [];
}

ReassignHistory.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, domain, domainId, act, actId, fromDate, toDate]);
    this.fetchSearchList();
};

ReassignHistory.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
};

ReassignHistory.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    client_mirror.getReassignedHistoryReportFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
            t_this._acts = response.acts;
        } else {
            t_this.possibleFailures(error);
        }
    });
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
    if (domain) {
        if (isNotEmpty(domain, message.domain_required) == false)
            return false;
        else if (isLengthMinMax(domain, 1, 50, message.domain_max) == false)
            return false;
        else if (isCommonName(domain, message.domain_str) == false)
            return false;
    }
    if (act) {
        if (isLengthMinMax(act, 0, 50, message.act_max) == false)
            return false;
        else if (isCommonName(act, message.act_str) == false)
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

ReassignHistory.prototype.fetchReportValues = function(c_id, d_id, act, from_date, to_date, csv) {
    t_this = this;
    /*var jsondata = '{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Aug-2016","assigned":"EMP0016 - Rajkumar / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Approved"},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Jun-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Assignee Re-deployed"},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Jan-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":""},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form B - Annual Returns Submission","due_date":"01-Sep-2016","assigned_date":"20-Aug-2016","assigned":"EEMP0016 -Rajkumar / EMP0013 - Suresh / EMP0014 -Praveen","reason":"Role Changed"},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form B - Annual Returns Submission","due_date":"01-Sep-2016","assigned_date":"01-Jan-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Assignee Re-deployed"}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;*/
    client_mirror.getReassignedHistoryReport(c_id, le_id, d_id, u_id, act, compliance_task_id, users_id, from_date, to_date, csv, function(error, response) {
        if (error == null) {
            t_this._report_data = response.reassigned_history_list;
            t_this._total_count = response.total_count;
            if (csv == false)
                REPORT.showReportValues();
            else
                REPORT.exportReportValues();
        } else {
            t_this.possibleFailures(error);
        }
    });
};

ReassignHistory.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    countryName.html(country.val());
    domainName.html(domain.val());
    var j = 0;
    reportTableTbody.find('tr').remove();
    var actname = "";
    var tree = "";
    $.each(data, function(k, v) {
        if (unitid != v.unit_id) {
            var cloneone = $('#template #report-table .row-one').clone();
            $('.unit-name', cloneone).text(v.unit);
            reportTableTbody.append(cloneone);
            unitid = v.unit_id;
        }

        if (actname != v.act_name) {
            var clonetwo = $('#template #report-table .row-two').clone();
            $('.act-name', clonetwo).text(v.act_name);
            reportTableTbody.append(clonetwo);
            actname = v.act_name;
        }

        if (complianceid != v.compliance_id) {
            j = j + 1;
            var clonethree = $('#template #report-table .row-three').clone();
            $('.sno', clonethree).text(j);
            $('.compliance-task', clonethree).text(v.compliance_task);
            $('.due-date', clonethree).text(v.due_date);
            $('.assigned-date', clonethree).text(v.assigned_on);
            $('.assigned', clonethree).text(v.new_user);
            if (v.reason != "") { $('.reason', clonefour).text(v.remarks); } else { $('.reason', clonefour).text('-'); }
            $(clonethree).on('click', function (e) {
              treeShowHide(e, "tree"+v.compliance_id);
            });
            $(clonethree).attr("id","tree"+v.compliance_id);
            reportTableTbody.append(clonethree);
            complianceid = v.compliance_id;
        } else {
            if (tree == v.compliance_id) {
                var clonefive = $('#template #report-table .row-five').clone();
                $('.assigned-date-new', clonefive).text(v.assigned_on);
                $('.assigned-new', clonefive).text(v.new_user);
                $('.reason-new', clonefive).text(v.remarks);
                if (v.reason != "") { $('.reason-new', clonefive).text(v.remarks); } else { $('.reason-new', clonefive).text('-'); }
                $('.tree'+v.compliance_id).append(clonefive);
            } else {
                var clonefour = $('#template #report-table .row-four').clone();
                $(clonefour).addClass("tree"+v.compliance_id);
                $('.assigned-date-new', clonefour).text(v.assigned_on);
                $('.assigned-new', clonefour).text(v.new_user);
                $('.reason-new', clonefour).text(v.remarks);
                if (v.reason != "") { $('.reason-new', clonefour).text(v.remarks); } else { $('.reason-new', clonefour).text('-'); }
                reportTableTbody.append(clonefour);
                complianceid = v.compliance_id;
                tree = v.compliance_id
            }
        }
    });
     var total = t_this._total_count;
    totalRecord.html(total);
};
ReassignHistory.prototype.exportReportValues = function() {
    alert('export');
};
ReassignHistory.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
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

