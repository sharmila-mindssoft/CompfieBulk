// Declare basic elements to variable
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

var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var f_count = 1;
var REPORT = null;
var LOGO = null;

function PageControls() {
    // To call date picker function. assign to date field
    // $(".from-date, .to-date").datepicker({
    //     changeMonth: true,
    //     changeYear: true,
    //     dateFormat: "dd-M-yy",
    //     onSelect: function(selectedDate) {
    //         if ($(this).hasClass("from-date") == true) {
    //             var dateMax = $('.from-date').datepicker('getDate');
    //             var dateMax = new Date(dateMax.getFullYear(), dateMax.getMonth()+3, dateMax.getDate()-1);
    //             $('.to-date').datepicker('setDate', dateMax);
    //         }
    //         if ($(this).hasClass("to-date") == true) {
    //             var dateMin = $('.to-date').datepicker('getDate');
    //             var dateMin = new Date(dateMin.getFullYear(), dateMin.getMonth()-3, dateMin.getDate()+1);
    //             $('.from-date').datepicker('setDate', dateMin);
    //         }
    //     }
    // });

    $(".from-date, .to-date").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-M-yy",
        onSelect: function(selectedDate) {
            if ($(this).hasClass("from-date") == true) {
                var fromDate = $('.from-date').datepicker('getDate');
                var dateMax = new Date(fromDate.getFullYear(), fromDate.getMonth() + 3, fromDate.getDate() - 1);
                var dateMin = new Date(fromDate.getFullYear(), fromDate.getMonth(), fromDate.getDate());
                $('.to-date').datepicker('setDate', dateMax);
                $('.to-date').datepicker("option", "minDate", dateMin);
                $('.to-date').datepicker("option", "maxDate", dateMax);
            }
            if ($(this).hasClass("to-date") == true) {
                var dateMin = $('.to-date').datepicker('getDate');
            }
        }
    });

    //when click the country text box to initiate auto complete to display & get values from object
    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._entities;
        if (countryList.length == 0 && text_val != '')
            displayMessage(message.country_required);
        var condition_fields = [];
        var condition_values = [];
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

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = REPORT._units;
        if (unitList.length == 0 && text_val != '')
            displayMessage(message.unit_required);
        var condition_fields = ["d_ids"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._acts;
        var condition_fields = ["d_id"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acAct, actId, text_val, actList, "act", "act", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        var condition_fields = ["d_id"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acComplianceTask, complianceTaskId, text_val, complianceTaskList, "c_task", "compliance_id", function(val) {
            onComplianceTaskAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var userList = REPORT._users;
        var le_users = {};
        le_users['employee_code'] = '';
        le_users['employee_name'] = 'Administrator';
        le_users['is_active'] = true;
        le_users['le_id'] = legalEntityId.val();
        le_users['user_id'] = 1;
        userList.unshift(le_users);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acUsers, usersId, text_val, userList, "employee_name", "user_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        on_current_page = 1;
        processSubmit(false, true);
    });

    exportButton.click(function() {
        processSubmit(true, false);
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        f_count = 1;
        on_current_page = 1;
        createPageView(t_this._total_count);
        processSubmit(false, false);
    });
}

processSubmit = function(csv, count_qry) {
    if (REPORT.validate()) {
        REPORT.fetchReportValues(csv, count_qry);
    }
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
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([act, actId, complianceTask, complianceTaskId]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
    clearElement([complianceTask, complianceTaskId]);
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
    this._entities = [];
    this._domains = [];
    this._units = [];
    this._acts = [];
    this._compliance_task = [];
    this._users = [];
    this._report_data = [];
    this._total_count = [];
}

ReassignHistory.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, legalEntity, legalEntityId, domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId, fromDate, toDate]);
    this.fetchSearchList();
};

ReassignHistory.prototype.fetchSearchList = function() {
    t_this = this;
    /*var jsondata = '[{"c_id":1,"le_name":"LG Legal Entity","le_id":1,"bg_name":"LG Business Group","bg_id":1,"c_name":"India"},{"c_id":1,"le_name":"LG Legal Entity","le_id":1,"bg_name":"LG Business Group","bg_id":1,"c_name":"India"}]';
    var object = jQuery.parseJSON(jsondata);
    t_this._entities = object;*/
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

ReassignHistory.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getReassignedHistoryReportFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
            t_this._units = response.units;
            t_this._acts = response.acts;
            t_this._compliance_task = response.compliances;
            t_this._users = response.legal_entity_users;
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
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
        if (isNotEmpty(unit, message.unit_required) == false)
            return false;
        else if (isLengthMinMax(unit, 0, 50, message.unit_max) == false)
            return false;
        else if (isCommonName(unit, message.unit_str) == false)
            return false;
    }
    if (act) {
        if (isLengthMinMax(act, 0, 100, message.act_max) == false)
            return false;
        else if (isCommonName(act, message.act_str) == false)
            return false;
    }
    if (complianceTask) {
        if (isLengthMinMax(complianceTask, 0, 150, message.complianceTask_max) == false)
            return false;
        else if (isCommonName(complianceTask, message.complianceTask_str) == false)
            return false;
    }
    if (users) {
        if (isLengthMinMax(users, 0, 70, message.user_max) == false)
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

ReassignHistory.prototype.fetchReportValues = function(csv, count_qry) {
    t_this = this;
    /*var jsondata = '{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Aug-2016","assigned":"EMP0016 - Rajkumar / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Approved"},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Jun-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Assignee Re-deployed"},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form A - Registration","due_date":"28-Aug-2016","assigned_date":"01-Jan-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":""},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form B - Annual Returns Submission","due_date":"01-Sep-2016","assigned_date":"20-Aug-2016","assigned":"EEMP0016 -Rajkumar / EMP0013 - Suresh / EMP0014 -Praveen","reason":"Role Changed"},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","compliance_task":"Form B - Annual Returns Submission","due_date":"01-Sep-2016","assigned_date":"01-Jan-2016","assigned":"EMP0011 - Murali / EMP0013 - Suresh / EMP0014 - Praveen","reason":"Assignee Re-deployed"}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;*/
    var c_id = parseInt(countryId.val());
    var le_id = parseInt(legalEntityId.val());
    var d_id = parseInt(domainId.val());
    var u_id = parseInt(unitId.val());
    if (!u_id) u_id = null
    var act = actId.val();
    if (!act) act = null
    var compliance_task_id = parseInt(complianceTaskId.val());
    if (!compliance_task_id) compliance_task_id = null
    var usr_id = parseInt(usersId.val());
    if (!usr_id) usr_id = null
    var from_date = fromDate.val();
    var to_date = toDate.val();

    var t_count = parseInt(on_current_page) * parseInt(ItemsPerPage.val());
    if (on_current_page == 1) { f_count = 1 } else { f_count = ((parseInt(on_current_page) - 1) * parseInt(ItemsPerPage.val())) + 1; }
    displayLoader();
    client_mirror.getReassignedHistoryReport(c_id, le_id, d_id, u_id, act, compliance_task_id, usr_id, from_date, to_date, f_count, t_count, csv, count_qry, function(error, response) {
        if (error == null) {
            t_this._report_data = response.reassigned_history_list;
            if(response.total_count != 0)
                t_this._total_count = response.total_count;
            LOGO = response.logo_url;
            if (csv == false) {
                reportView.show();
                showAnimation(reportView);
                REPORT.showReportValues();
                if (f_count == 1)
                    createPageView(t_this._total_count);
            }
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};

ReassignHistory.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    if(LOGO != null)
        clientLogo.attr("src", LOGO);
    else
        clientLogo.remove();
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    domainName.html(domain.val());
    reportTableTbody.find('tr').remove();
    var unitid = "";
    var actname = "";
    var complianceid = "";
    var tree = "";
    var j = f_count;
    var i = 0;
    if(data.length > 0) {
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

            // if (complianceid != v.compliance_id) {
            //     i = i + 1;
            //     var clonethree = $('#template #report-table .row-three').clone();
            //     $('.sno', clonethree).text(j);
            //     $('.compliance-task', clonethree).text(v.compliance_task);
            //     $('.due-date', clonethree).text(v.due_date);
            //     $('.assigned-date', clonethree).text(v.assigned_on);
            //     $('.assigned', clonethree).text(v.new_user);
            //     if (v.reason != "") { $('.reason', clonethree).text(v.remarks); } else { $('.reason', clonethree).text('-'); }
            //     $(clonethree).attr("onClick", "treeShowHide('tree" + i + "')");
            //     $(clonethree).attr("id", "tree" + i);
            //     reportTableTbody.append(clonethree);
            //     complianceid = v.compliance_id;
            //     j = j + 1;
            // } else {
            //     if (tree == v.compliance_id) {
            //         var clonefive = $('#template #report-table .row-five').clone();
            //         $('.assigned-date-new', clonefive).text(v.assigned_on);
            //         $('.assigned-new', clonefive).text(v.new_user);
            //         $('.reason-new', clonefive).text(v.remarks);
            //         if (v.reason != "") { $('.reason-new', clonefive).text(v.remarks); } else { $('.reason-new', clonefive).text('-'); }
            //         $('.tree' + i + ' .tree-body').append(clonefive);
            //     } else {
            //         var clonefour = $('#template #report-table .row-four').clone();
            //         $(clonefour).addClass("tree" + i);
            //         $('.assigned-date-new', clonefour).text(v.assigned_on);
            //         $('.assigned-new', clonefour).text(v.new_user);
            //         $('.reason-new', clonefour).text(v.remarks);
            //         if (v.reason != "") { $('.reason-new', clonefour).text(v.remarks); } else { $('.reason-new', clonefour).text('-'); }
            //         reportTableTbody.append(clonefour);
            //         tree = v.compliance_id
            //     }
            //     complianceid = v.compliance_id;
            // }

            if (complianceid != v.compliance_id) {
                i = i + 1;
                var clonethree = $('#template #report-table .row-three').clone();
                $('.sno', clonethree).text(j);
                $('.compliance-task', clonethree).text(v.compliance_task);
                $('.due-date', clonethree).text(v.due_date);
                $('.assigned-date', clonethree).text(v.assigned_on);
                $('.assigned', clonethree).text(v.new_user);
                if (v.reason != "") { $('.reason', clonethree).text(v.remarks); } else { $('.reason', clonethree).text('-'); }
                $(clonethree).attr("onClick", "treeShowHide('tree" + i + "')");
                $(clonethree).attr("id", "tree" + i);
                reportTableTbody.append(clonethree);
                complianceid = v.compliance_id;

                var clonefour = $('#template #report-table .row-four').clone();
                $(clonefour).addClass("tree" + i);
                $('.assigned-date-new', clonefour).text(v.assigned_on);
                $('.assigned-new', clonefour).text(v.old_user);
                reportTableTbody.append(clonefour);

                j = j + 1;
            } 

        });
        showPagePan(f_count, j, t_this._total_count);
    } else {
        reportTableTbody.html('<tr><td colspan="100%"><br><center>Record Not Found!</center><br></td></tr>');
        hidePagePan();
    }
};

treeShowHide = function(tree) {
    if ($('.' + tree)) {
        if ($('.' + tree).is(":visible") == true)
            $('.' + tree).hide();
        else
            $('.' + tree).show();
    }
};

showPagePan = function(start, end, total) {
    var showText = 'Showing ' + start + ' to ' + (end - 1) + ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
};

hidePagePan = function() {
    CompliacneCount.text('');
    PaginationView.hide();
}

createPageView = function(total_records) {
    if(parseInt(total_records) > 0) {
        perPage = parseInt(ItemsPerPage.val());
        Pagination.empty();
        Pagination.removeData('twbs-pagination');
        Pagination.unbind('page');

        Pagination.twbsPagination({
            totalPages: Math.ceil(total_records / perPage),
            visiblePages: visiblePageCount,
            onPageClick: function(event, page) {
                cPage = parseInt(page);
                if (parseInt(on_current_page) != cPage) {
                    on_current_page = cPage;
                    processSubmit(false, false);
                }
            }
        });
    }
};

ReassignHistory.prototype.exportReportValues = function() {
    // alert('export');
};

ReassignHistory.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
    }
};

ReassignHistory.prototype.loadEntityDetails = function() {
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
};

// call class ReassignHistory to store the REPORT object
REPORT = new ReassignHistory();

$(document).ready(function() {
    // To initially to call the page controller what are the activity to set in page controller
    PageControls();
    // To store values in object & search list element
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
    loadItemsPerPage();
});
