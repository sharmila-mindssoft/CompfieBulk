var CountryNameLabel = $(".country-name");
var CountryNameAC = $(".country-name-ac");

var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal-entity");
var LegalEntityId = $("#legal-entity-id");
var ACLegalEntity = $("#ac-legal-entity");

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
var users = $("#user");
var userId = $("#user-id");
var acUser = $("#ac-user");
var fromDate = $("#from_date");
var toDate = $("#to_date");
var complianceTaskStatus = $("#compliance-task-status");
var LegalEntityCompliances = [];

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
var le_id = null, le_name = null;
var c_id = null, c_name = null;
var REPORT = null;

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var _page_limit = 25;
var csv = false;


function PageControls() {
    $(".from-date, .to-date").datepicker({
        showButtonPanel: true,
        closeText: 'Clear',
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-M-yy",
        onSelect: function(selectedDate) {
            if ($(this).hasClass("from-date") == true) {
                var dateMin = $('.from-date').datepicker("getDate");
                var rMin = new Date(dateMin.getFullYear(), dateMin.getMonth(), dateMin.getDate()); // +1
                $('.to-date').datepicker("option", "minDate", rMin);
                var event = arguments.callee.caller.caller.arguments[0];
                if ($(event.delegateTarget).hasClass('ui-datepicker-close')) {
                    $(this).val('');
                }
            }
            if ($(this).hasClass("to-date") == true) {
                var dateMin = $('.to-date').datepicker("getDate");
            }
        }
    });

    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._countries;
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            onCountryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    LegalEntityName.keyup(function(e) {
        var text_val = LegalEntityName.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, ACLegalEntity, LegalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, LegalEntityId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = [];
        for(var i=0;i<REPORT._units.length;i++){
            if(REPORT._units[i].domain_id == domainId.val()){
                unitList.push({
                    "unit_id": REPORT._units[i].unit_id,
                    "unit_name": REPORT._units[i].unit_code+" - "+REPORT._units[i].unit_name
                });
            }
        }
        if (unitList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        });
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = [];
        var condition_fields = ["domain_id"];
        var condition_values = [domainId.val()];
        if (unitId.val() != ""){
            actList = REPORT._compliance_task;
            condition_fields.push("unit_id");
            condition_values.push(unitId.val())
        }else{
            actList = REPORT._acts;
        }

        if (actList.length == 0)
            displayMessage(message.act_required);
        commonAutoComplete(e, acAct, actId, text_val, actList, "statutory_mapping", "compliance_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        if (complianceTaskList.length == 0)
            displayMessage(message.complianceTask_required);
        var condition_fields = ["domain_id"];
        var condition_values = [domainId.val()];
        if (unitId.val() != ""){
            condition_fields.push("unit_id");
            condition_values.push(unitId.val())
        }
        if (act.val() != ""){
            condition_fields.push("statutory_mapping");
            condition_values.push(act.val().trim())
        }
        commonAutoComplete(e, acComplianceTask, complianceTaskId, text_val, complianceTaskList, "compliance_task", "compliance_id", function(val) {
            onComplianceTaskAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var condition_fields = ["domain_id"];
        var condition_values = [domainId.val()];
        if (unitId.val() != ""){
            condition_fields.push("unit_id");
            condition_values.push(unitId.val())
        }
        if (complianceTaskId.val() != ""){
            condition_fields.push("compliance_id");
            condition_values.push(complianceTaskId.val());
        }
        if (userType.val() >= 0){
            var userList = REPORT._users;
            if (userType.val() == 0){
                commonAutoComplete(e, acUser, userId, text_val, userList, "assignee_name", "assignee", function(val) {
                    onUserAutoCompleteSuccess(REPORT, val);
                }, condition_fields, condition_values);
            }
            else if (userType.val() == 1){
                commonAutoComplete(e, acUser, userId, text_val, userList, "concurrer_name", "concurrence_person", function(val) {
                    onUserAutoCompleteSuccess(REPORT, val);
                }, condition_fields, condition_values);
            }
            else if (userType.val() == 2){
                commonAutoComplete(e, acUser, userId, text_val, userList, "approver_name", "approval_person", function(val) {
                    onUserAutoCompleteSuccess(REPORT, val);
                }, condition_fields, condition_values);
            }
        }else{
            var userList = [];
            for (var i=0;i<REPORT._users.length;i++){
                j = 0;
                while (j<3){
                    if (j==0){
                        userList.push({
                            "domain_id": REPORT._users[i].domain_id,
                            "unit_id": REPORT._users[i].unit_id,
                            "compliance_id": REPORT._users[i].compliance_id,
                            "u_id": REPORT._users[i].assignee,
                            "u_name": REPORT._users[i].assignee_name
                        });
                    }
                    else if (j==1){
                        userList.push({
                            "domain_id": REPORT._users[i].domain_id,
                            "unit_id": REPORT._users[i].unit_id,
                            "compliance_id": REPORT._users[i].compliance_id,
                            "u_id": REPORT._users[i].concurrence_person,
                            "u_name": REPORT._users[i].concurrer_name
                        });
                    }
                    else if (j==2){
                        userList.push({
                            "domain_id": REPORT._users[i].domain_id,
                            "unit_id": REPORT._users[i].unit_id,
                            "compliance_id": REPORT._users[i].compliance_id,
                            "u_id": REPORT._users[i].approval_person,
                            "u_name": REPORT._users[i].approver_name
                        });
                    }
                    j++;
                }
            }
            commonAutoComplete(e, acUser, userId, text_val, userList, "u_name", "u_id", function(val) {
                onUserAutoCompleteSuccess(REPORT, val);
            }, condition_fields, condition_values);
        }
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            csv = false;
            this._on_current_page = 1;
            this._sno = 0;
            this._total_record = 0;
            reportView.show();
            showAnimation(reportView);
            REPORT.fetchReportValues();
            REPORT.renderPageControls();
        }
    });

    exportButton.click(function() {
        if (REPORT.validate()) {
            csv = true;
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
    clearElement([LegalEntityName, LegalEntityId, domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId, users, userId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    clearElement([domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId, users, userId]);
    REPORT.fetchDomainList(countryId.val(), val[0]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([unit, unitId, act, actId, complianceTask, complianceTaskId, users, userId]);
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([act, actId, complianceTask, complianceTaskId, users, userId]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
    clearElement([complianceTask, complianceTaskId, users, userId]);
}

onComplianceTaskAutoCompleteSuccess = function(REPORT, val) {
    complianceTask.val(val[1]);
    complianceTaskId.val(val[0]);
    complianceTask.focus();
    clearElement([users, userId]);
}

onUserAutoCompleteSuccess = function(REPORT, val) {
    users.val(val[1]);
    userId.val(val[0]);
    users.focus();
}
LegalEntityWiseReport = function() {
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
    this._on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
    this._LegalEntityCompliances = [];
}

LegalEntityWiseReport.prototype.loadSearch = function() {
    reportView.hide();
    country.val('');
    countryId.val('');
    LegalEntityName.val('');
    LegalEntityId.val('');
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
    userId.val('');
    fromDate.val('');
    toDate.val('');
    complianceTaskStatus.empty();
    this.renderPageControls();
    this.fetchSearchList();
};

LegalEntityWiseReport.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

LegalEntityWiseReport.prototype.loadEntityDetails = function(){
    t_this = this;
    if(t_this._entities.length > 1){
        CountryNameAC.show();
        CountryNameLabel.hide();
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
    }else{
        c_name = t_this._entities[0]["c_name"];
        c_id = t_this._entities[0]["c_id"];
        CountryNameLabel.show();
        CountryNameAC.hide();
        CountryNameLabel.text(c_name);
        country.val(c_name);
        countryId.val(c_id);
        le_name = t_this._entities[0]["le_name"];
        le_id = t_this._entities[0]["le_id"];
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(le_name);
        LegalEntityName.val(le_name);
        LegalEntityId.val(le_id);
        REPORT.fetchDomainList(c_id, le_id);
    }

};

LegalEntityWiseReport.prototype.fetchDomainList = function(c_id, le_id) {
    t_this = this;
    client_mirror.getLegalEntityWiseReportFilters(parseInt(c_id), parseInt(le_id), function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._domains = response.domains;
            t_this._units = response.unit_legal_entity;
            t_this._acts = response.act_legal_entity;
            t_this._compliance_task = response.compliance_task_list;
            t_this._compliance_task_status = response.compliance_task_status;
            REPORT.renderComplianceTaskStatusList(t_this._compliance_task_status);
            t_this._frequencies = response.compliance_frequency_list;
            REPORT.renderComplianceFrequencyList(t_this._frequencies);
            t_this._user_type = response.compliance_user_type;
            REPORT.renderUserTypeList(t_this._user_type);
            t_this._users = response.compliance_users;
        } else {
            t_this.possibleFailures(error);
        }
    });
};

LegalEntityWiseReport.prototype.renderCountriesList = function(data) {
    t_this = this;
    country.empty();
    var countryName = [];
    $.each(data, function(i, e) {
        //countryName.push(e.c_name+",");
        countryName = e.c_name;
    });
    country.html(countryName);
};

LegalEntityWiseReport.prototype.renderLegalEntityList = function(data) {
    t_this = this;
    LegalEntityName.empty();
    var legalEntityName = [];
    $.each(data, function(i, e) {
        //legalEntityName.push(e.le_name+",");
        legalEntityName = e.le_name;
    });
    LegalEntityName.html(legalEntityName);
};

LegalEntityWiseReport.prototype.renderComplianceFrequencyList = function(data) {
    t_this = this;
    complianceFrequency.empty();
    var complianceFrequencyList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceFrequencyList = complianceFrequencyList + '<option value="' + e.frequency_id + '"> ' + e.frequency_name + ' </option>';
    });
    complianceFrequency.html(complianceFrequencyList);
};

LegalEntityWiseReport.prototype.renderUserTypeList = function(data) {
    t_this = this;
    userType.empty();
    var userTypeList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        userTypeList = userTypeList + '<option value="' + e.user_type_id + '"> ' + e.user_type + ' </option>';
    });
    userType.html(userTypeList);
};

LegalEntityWiseReport.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.task_status_id + '"> ' + e.task_status + ' </option>';
    });
    complianceTaskStatus.html(complianceTaskStatusList);
};

LegalEntityWiseReport.prototype.validate = function() {
    if (country) {
        if (isNotEmpty(country, message.country_required) == false)
            return false;
        else if (isLengthMinMax(country, 1, 50, message.country_max) == false)
            return false;
        else if (isCommonName(country, message.country_str) == false)
            return false;
    }
    if (LegalEntityName) {
        if (isNotEmpty(LegalEntityName, message.legalentity_required) == false)
            return false;
        else if (isLengthMinMax(LegalEntityName, 1, 50, message.legalentity_max) == false)
            return false;
        else if (isCommonName(LegalEntityName, message.legalentity_str) == false)
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

LegalEntityWiseReport.prototype.fetchReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    le_id = LegalEntityId.val();
    d_id = domainId.val();
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
    stat_map = $('#act option:selected').text();
    if (stat_map == "")
        stat_map = null;
    compl_id = complianceTaskId.val();
    if (compl_id == "")
        compl_id = 0;
    c_f_id = complianceFrequency.val();
    if (c_f_id == "")
        c_f_id = 0;
    u_t = $('#user-type option:selected').text();
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    f_date = fromDate.val();
    t_date = toDate.val();
    c_t_s = $('#compliance-task-status option:selected').text();

    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        this._sno = 0
    }
    else {
        this._sno = (this._on_current_page - 1) *  _page_limit;
    }

    client_mirror.getLegalEntityWiseReport(
        parseInt(c_id), parseInt(le_id), parseInt(d_id), parseInt(unit_id), stat_map, parseInt(compl_id),
        parseInt(c_f_id), u_t, parseInt(user_id), f_date, t_date, c_t_s, csv, this._sno, _page_limit,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._LegalEntityCompliances = response.legal_entities_compliances;
            if (response.legal_entities_compliances.length == 0) {
                t_this.hidePageView();
                t_this.hidePagePan();
                //Export_btn.hide();
                PaginationView.hide();
                t_this.showReportValues();
            }
            else{
                t_this._total_record = response.legal_entities_compliances.length;
                if (t_this._sno == 0) {
                    t_this.createPageView(t_this, t_this._total_record);
                }
                //Export_btn.show();
                PaginationView.show();
                t_this.showReportValues();
            }
        } else {
            t_this.possibleFailures(error);
        }
    });
};

LegalEntityWiseReport.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._LegalEntityCompliances;
    $('.le-header').text(LegalEntityName.val());
    $('.ctry-header').text(country.val());
    $('.dom-header').text(domain.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var unitname = "";
    var actname = "";
    var complianceTask = "";
    var is_null = true;
    showFrom = t_this._sno + 1;
    t_this._total_record = data.length;
    $.each(data, function(k, v) {
        console.log(data.length)
        is_null = false;
        $('.client-logo').attr("src", v.logo_url);

        if (unitname != v.unit_name) {
            var cloneone = $('#template #report-table .row-one').clone();
            $('.unit-name', cloneone).text(v.unit_name);
            reportTableTbody.append(cloneone);
            unitname = v.unit_name;
        }

        if (actname != v.statutory_mapping) {
            var clonetwo = $('#template #report-table .row-two').clone();
            $('.act-name', clonetwo).text(v.statutory_mapping);
            reportTableTbody.append(clonetwo);
            actname = v.statutory_mapping;
        }

        if (complianceTask != v.compliance_task) {
            var clonethree = $('#template #report-table .tree-open-close').clone();
            t_this._sno += 1;
            $('.sno', clonethree).text(t_this._sno);
            $('.compliance-task', clonethree).text(v.compliance_task);
            $('.frequency', clonethree).text(v.frequency_name);
            $('.due-date', clonethree).text(v.due_date);
            $('.compliance-task-status', clonethree).text(v.task_status);
            $('.user-name', clonethree).html(v.assignee_name);
            $('.user-name', clonethree).addClass("-"+v.compliance_id);
            $('.user-name', clonethree).on('click', function() { tree_open_close(this); });
            $('.activity-status', clonethree).text(v.activity_status);
            if (v.activity_date != "")
                $('.activity-date', clonethree).text(v.activity_date);
            else
                $('.activity-date', clonethree).text('-');
            if (v.document_name.length > 0) {
                //$('.uploaded-document a', clonethree).text(v.documents).attr("href", v.url);
                $('.uploaded-document', clonethree).html(v.document_name);
                $('.uploaded-document', clonethree).addClass("-"+v.compliance_id);
                $('.uploaded-document', clonethree).on('click', function() { download_url(v.url); });

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
            var clonefour = $('#template #report-table .tree-data').clone();
            $('.user-name-new', clonefour).text(v.assignee_name);
            $('.activity-status-new', clonefour).text(v.activity_status);
            if (v.activity_date != "")
                $('.activity-date-new', clonefour).text(v.activity_date);
            else
                $('.activity-date-new', clonefour).text('-');
            if (v.document_name.length > 0) {
                //$('.uploaded-document a', clonethree).text(v.documents).attr("href", v.url);
                $('.uploaded-document', clonethree).html(v.document_name);
                $('.uploaded-document', clonethree).addClass("-"+v.compliance_id);
                $('.uploaded-document', clonethree).on('click', function() { download_url(v.url); });
            } else {
                $('.uploaded-document', clonethree).text('-');
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

    if (is_null == true) {
        //a_page.hidePagePan();
        reportTableTbody.empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        reportTableTbody.append(clone4);
    }
    else {
        t_this.showPagePan(showFrom, t_this._sno, t_this._total_record);
    }
};

function tree_open_close(e) {
    var len = e.className.split("-").length;
    id = e.className.split("-")[len-1];
    $('.tree' + id).toggle("slow");
}

function download_url(doc_url) {
    if(doc_url != null){
        window.open(doc_url, '_blank');
    }
}

LegalEntityWiseReport.prototype.exportReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    le_id = LegalEntityId.val();
    d_id = domainId.val();
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
    stat_map = $('#act option:selected').text();
    if (stat_map == "")
        stat_map = null;
    compl_id = complianceTaskId.val();
    if (compl_id == "")
        compl_id = 0;
    c_f_id = complianceFrequency.val();
    if (c_f_id == "")
        c_f_id = 0;
    u_t = $('#user-type option:selected').text();
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    f_date = fromDate.val();
    t_date = toDate.val();
    c_t_s = $('#compliance-task-status option:selected').text();

    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        _sno = 0
    }
    else {
        _sno = (this._on_current_page - 1) *  _page_limit;
    }

    client_mirror.getLegalEntityWiseReport(
        parseInt(c_id), parseInt(le_id), parseInt(d_id), parseInt(unit_id), stat_map, parseInt(compl_id),
        parseInt(c_f_id), u_t, parseInt(user_id), f_date, t_date, c_t_s, csv, sno, _page_limit,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            if(csv){
                document_url = response.link;
                window.open(document_url, '_blank');
            }
        } else {
            t_this.possibleFailures(error);
        }
    });
};

LegalEntityWiseReport.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
    }
};

// Pagination Functions - begins
LegalEntityWiseReport.prototype.hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

LegalEntityWiseReport.prototype.createPageView = function(a_obj, total_records) {
    perPage = parseInt(ItemsPerPage.val());
    a_obj.hidePageView();

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(a_obj._on_current_page) != cPage) {
                a_obj._on_current_page = cPage;
                a_obj.fetchReportValues();
            }
        }
    });
};
LegalEntityWiseReport.prototype.showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
LegalEntityWiseReport.prototype.hidePagePan = function() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

LegalEntityWiseReport.prototype.renderPageControls = function(e) {
    var t_this = this;
    ItemsPerPage.on('change', function(e) {
        t_this.perPage = parseInt($(this).val());
        t_this._sno = 0;
        t_this._on_current_page = 1;
        t_this.createPageView(t_this, t_this._total_record);
        t_this.fetchReportValues();
    });
    t_this._perPage = parseInt(ItemsPerPage.val());

};
// Pagination Ends

REPORT = new LegalEntityWiseReport();

$(document).ready(function() {
    $('.row-three').click(function() {
        $('.row-four').toggle("slow");
    });
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});
