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

var complianceFrequency = $("#compliance-frequency");
var userType = $("#user-type");
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
var REPORT = null;

var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var f_count = 0;

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
        var condition_values = [true, legalEntityId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = REPORT._units;
        if (unitList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["d_ids"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
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

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        if (complianceTaskList.length == 0)
            displayMessage(message.complianceTask_required);
        var condition_fields = ["d_id"];
        var condition_values = [domainId.val()];
        commonAutoComplete(e, acComplianceTask, complianceTaskId, text_val, complianceTaskList, "c_task", "compliance_id", function(val) {
            onComplianceTaskAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var userList = REPORT._users;
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acUsers, usersId, text_val, userList, "employee_name", "user_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        var csv = false;
        on_current_page = 1;
        processSubmit(csv);
    });

    exportButton.click(function() {
        var csv = true;
        processSubmit(csv);
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        f_count = 0;
        on_current_page = 1;
        createPageView(t_this._total_count);
        var csv = false;
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
    this._total_count = [];
}

StatusReportConsolidated.prototype.loadSearch = function() {
    reportView.hide();
    country.val('');
    legalEntity.val('');
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
    users.val('');
    usersId.val('');
    fromDate.val('');
    toDate.val('');
    complianceTaskStatus.empty();
    this.fetchSearchList();
};

StatusReportConsolidated.prototype.fetchSearchList = function() {
    t_this = this;
    /*var jsondata = '{"countries":[{"c_id":1,"c_name":"india","is_active":true},{"c_id":2,"c_name":"srilanka","is_active":true}],"entities":[{"le_id":1,"c_id":1,"le_name":"RG Legal Entity","is_active":true},{"le_id":2,"c_id":1,"le_name":"ABC Legal Entity","is_active":true}],"frequencies":[{"f_id":1,"f_name":"Periodical"},{"f_id":2,"f_name":"Review"},{"f_id":3,"f_name":"Flexi Review"},{"f_id":4,"f_name":"One Time"}],"user_type":[{"user_type_id":1,"user_type_name":"Assignee"},{"user_type_id":2,"user_type_name":"Concurrence"},{"user_type_id":3,"user_type_name":"Approval"}],"compliance_task_status":[{"comp_task_status_id":1,"comp_task_status":"Complied"},{"comp_task_status_id":2,"comp_task_status":"Delayed Compliances"},{"comp_task_status_id":3,"comp_task_status":"Inprogress"},{"comp_task_status_id":4,"comp_task_status":"Not Complied"}],"service_providers":[{"s_p_id":1,"s_p_name":"String","s_p_shrot":"short"}],"users":[{"u_id":1,"u_name":"Siva ","is_active":true},{"u_id":2,"u_name":"Hari","is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);*/

    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getUserLegalEntity();
    t_this._userType = UserTypes; // common-functions.js
    t_this._complianceTaskStatus = ComplianceTaskStatuses; // common-functions.js
    t_this.renderUserTypeList(t_this._userType);
    t_this.renderComplianceTaskStatusList(t_this._complianceTaskStatus);
};

StatusReportConsolidated.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    client_mirror.getStatusReportConsolidatedFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
            t_this._units = response.units;
            t_this._acts = response.acts;
            t_this._compliance_task = response.compliances;
            t_this._users = response.legal_entity_users;
            t_this._frequencies = response.compliance_frequency;
            t_this.renderComplianceFrequencyList(t_this._frequencies);

        } else {
            t_this.possibleFailures(error);
        }
    });
};

StatusReportConsolidated.prototype.renderComplianceFrequencyList = function(data) {
    t_this = this;
    complianceFrequency.empty();
    var complianceFrequencyList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceFrequencyList = complianceFrequencyList + '<option value="' + e.frequency_id + '"> ' + e.frequency + ' </option>';
    });
    complianceFrequency.html(complianceFrequencyList);
};

StatusReportConsolidated.prototype.renderUserTypeList = function(data) {
    t_this = this;
    userType.empty();
    var userTypeList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        userTypeList = userTypeList + '<option value="' + e.id + '"> ' + e.name + ' </option>';
    });
    userType.html(userTypeList);
};

StatusReportConsolidated.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="All">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.name + '"> ' + e.name + ' </option>';
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

StatusReportConsolidated.prototype.fetchReportValues = function(csv) {
    t_this = this;
    /*var jsondata = '{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Test Act","compliance_task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1004 - Suresh","activity_status":"Approved","activity_date":"20-Aug-2016","doc_list":[],"completion_date":"18-Aug-2016","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Test Act","compliance_task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1002 - Rajkumar","activity_status":"Submitted","activity_date":"18-Aug-2016","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/status-report-consolidated"}],"completion_date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Test Act","compliance_task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1002 - Sivakumar","activity_status":"Pending","activity_date":"20-Aug-2016","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/status-report-consolidated"}],"completion_date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1035 - RG Chennai Unit - 23, K.K.Nagar, Chennai-600025","l_name":"PF Act","compliance_task":"FORM VIII - Notice of Opening","frequency":"One Time","due_date":"20-Aug-2016","task_status":"Inprogress","user_name":"EMP1004 - Suresh","activity_status":"Pending","activity_date":"","doc_list":[],"completion_date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1035 - RG Chennai Unit - 23, K.K.Nagar, Chennai-600025","l_name":"PF Act","compliance_task":"FORM VIII - Notice of Opening","frequency":"One Time","due_date":"20-Aug-2016","task_status":"Inprogress","user_name":"EMP1002 - Rajkumar","activity_status":"Submitted","activity_date":"19-Aug-2016","doc_list":[{"doc_name":"Document 2","doc_url":"http://localhost:8083/status-report-consolidated"}],"completion_date":"","com_id":1,"f_id":1}]}';
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
    var comp_fre_id = parseInt(complianceFrequency.val());
    var user_type_id = parseInt(userType.val());
    var comp_task_status_id = complianceTaskStatus.val();

    var t_count = parseInt(ItemsPerPage.val());
    if (on_current_page == 1) { f_count = 0 } else { f_count = (on_current_page - 1) * t_count; }
    
    client_mirror.getStatusReportConsolidated(c_id, le_id, d_id, u_id, act, compliance_task_id, usr_id, comp_fre_id, user_type_id, comp_task_status_id, from_date, to_date, f_count, t_count, csv, function(error, response) {
        if (error == null) {
            t_this._report_data = response.status_report_consolidated_list;
            t_this._total_count = response.total_count;
            if (csv == false) {
                reportView.show();
                showAnimation(reportView);
                REPORT.showReportValues();
                if (f_count == 0)
                    createPageView(t_this._total_count);
            } else {
                REPORT.exportReportValues();
            }
        } else {
            t_this.possibleFailures(error);
        }
    });
};

StatusReportConsolidated.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    clientLogo.attr("src", "/files/client/common/images/yourlogo.png");
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    domainName.html(domain.val());
    var j = 0;
    reportTableTbody.find('tr').remove();
    var unitId = ""; //unit
    var actname = "";
    var complianceId = "";
    $.each(data, function(k, v) {
        if (unitId != v.unit_id) {
            var cloneone = $('#template #report-table .row-one').clone();
            $('.unit-name', cloneone).text(v.unit);
            reportTableTbody.append(cloneone);
            unitId = v.unit_id;
        }

        if (actname != v.act_name) {
            var clonetwo = $('#template #report-table .row-two').clone();
            $('.act-name', clonetwo).text(v.act_name);
            reportTableTbody.append(clonetwo);
            actname = v.act_name;
        }

        if (complianceId != v.compliance_id) {
            j = j + 1;
            var clonethree = $('#template #report-table .row-three').clone();
            $('.sno', clonethree).text(j);
            $('.compliance-task', clonethree).text(v.compliance_name);
            $('.frequency', clonethree).text(v.frequency_name);
            $('.due-date', clonethree).text(v.due_date);
            $('.compliance-task-status', clonethree).text(v.task_status);
            $('.user-name', clonethree).text(v.user_name);
            $('.activity-status', clonethree).text(v.activity_status);
            if (v.activity_on != "")
                $('.activity-date', clonethree).text(v.activity_on);
            else
                $('.activity-date', clonethree).text('-');
            /*if (v.doc_list.length > 0) {
                $.each(v.doc_list, function(k1, v1) {
                    $('.uploaded-document a', clonethree).text(v1.doc_name).attr("href", v1.doc_url);
                });
            } else {
                $('.uploaded-document', clonethree).text('-');
            }*/

            if(v.uploaded_document != "")
                $('.uploaded-document', clonethree).text(v.uploaded_document);
            else
                $('.uploaded-document', clonethree).text('-');

            if (v.completion_date != "")
                $('.completion-date', clonethree).text(v.completion_date);
            else
                $('.completion-date', clonethree).text('-');
            reportTableTbody.append(clonethree);
            complianceId = v.compliance_id;
        } else {
            var clonefour = $('#template #report-table .row-four').clone();
            $('.user-name-new', clonefour).text(v.user_name);
            $('.activity-status-new', clonefour).text(v.activity_status);
            if (v.activity_on != "")
                $('.activity-date-new', clonefour).text(v.activity_on);
            else
                $('.activity-date-new', clonefour).text('-');
            /*if (v.doc_list.length > 0) {
                $.each(v.doc_list, function(k1, v1) {
                    $('.uploaded-document-new a', clonefour).text(v1.doc_name).attr("href", v1.doc_url);
                });
            } else {
                $('.uploaded-document-new', clonefour).text('-');
            }*/

            if(v.uploaded_document != "")
                $('.uploaded-document', clonethree).text(v.uploaded_document);
            else
                $('.uploaded-document', clonethree).text('-');

            if (v.completion_date != "")
                $('.completion-date-new', clonefour).text(v.completion_date);
            else
                $('.completion-date-new', clonefour).text('-');
            reportTableTbody.append(clonefour);

            complianceId = v.compliance_id;
        }
    });
    showPagePan(f_count, j, t_this._total_count);
};

treeShowHide = function(e, tree) {
    if ($('.' + tree)) {
        if ($('.' + tree).is(":visible") == true)
            $('.' + tree).hide();
        else
            $('.' + tree).show();
    }
};

showPagePan = function(start, end, total) {
    var firstCount = parseInt(start) + 1;
    var showText = 'Showing ' + firstCount + ' to ' + end + ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
};

hidePagePan = function() {
    CompliacneCount.text('');
    PaginationView.hide();
}

createPageView = function(total_records) {
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
                processSubmit();
            }
        }
    });
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
    loadItemsPerPage();
});
