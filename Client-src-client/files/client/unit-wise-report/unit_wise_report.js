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

    LegalEntityName.keyup(function(e) {
        var text_val = LegalEntityName.val().trim();
        var legalEntityList = REPORT._entities;
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, ACLegalEntity, LegalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = [];
        for(var i=0;i<REPORT._units.length;i++){
            if(REPORT._units[i].legal_entity_id == LegalEntityId.val()){
                unitList.push({
                    "unit_id": REPORT._units[i].unit_id,
                    "unit_name": REPORT._units[i].unit_code+" - "+REPORT._units[i].unit_name
                });
            }
        }
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        });
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var dm_id = null;
        for(var i=0;i<REPORT._units.length;i++){
            if(REPORT._units[i].unit_id == unitId.val()){
                dm_id = REPORT._units[i].domain_id;
                break;
            }
        }
        var domainList = REPORT._domains;
        var condition_fields = ["is_active", "d_id"];
        var condition_values = [true, dm_id];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._compliance_task;

        var condition_fields = ["unit_id"];
        var condition_values = [unitId.val()];
        if (domainId.val() != ""){
            condition_fields.push("domain_id");
            condition_values.push(domainId.val())
        }
        commonAutoComplete(e, acAct, actId, text_val, actList, "statutory_mapping", "compliance_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        var condition_fields = ["unit_id"];
        var condition_values = [unitId.val()];
        if (domainId.val() != ""){
            condition_fields.push("domain_id");
            condition_values.push(domainId.val())
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
        var condition_fields = ["unit_id"];
        var condition_values = [unitId.val()];
        if (domainId.val() != ""){
            condition_fields.push("domain_id");
            condition_values.push(domainId.val())
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
            console.log(userList.length)
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
        }
    });

    exportButton.click(function() {
        if (REPORT.validate()) {
            csv = true;
            REPORT.exportReportValues();
        }
    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        this._on_current_page = 1;
        this._sno = 0;
        createPageView(t_this._total_record);
        csv = false;
        REPORT.fetchReportValues();
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
    clearElement([LegalEntityName, LegalEntityId, unit, unitId, domain, domainId, act, actId, complianceTask, complianceTaskId, users, userId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    clearElement([unit, unitId, domain, domainId, act, actId, complianceTask, complianceTaskId, users, userId]);
    REPORT.fetchUnitList(countryId.val(), val[0]);
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([domain, domainId, act, actId, complianceTask, complianceTaskId, users, userId]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
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
UnitWiseReport = function() {
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
    this._UnitCompliances = [];
}

UnitWiseReport.prototype.loadSearch = function() {
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
    this.fetchSearchList();
};

UnitWiseReport.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

UnitWiseReport.prototype.loadEntityDetails = function(){
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
        REPORT.fetchUnitList(c_id, le_id);
    }

};

UnitWiseReport.prototype.fetchUnitList = function(c_id, le_id) {
    t_this = this;
    client_mirror.getUnitWiseReportFilters(parseInt(c_id), parseInt(le_id), function(error, response) {
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

UnitWiseReport.prototype.renderComplianceFrequencyList = function(data) {
    t_this = this;
    complianceFrequency.empty();
    var complianceFrequencyList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceFrequencyList = complianceFrequencyList + '<option value="' + e.frequency_id + '"> ' + e.frequency_name + ' </option>';
    });
    complianceFrequency.html(complianceFrequencyList);
};

UnitWiseReport.prototype.renderUserTypeList = function(data) {
    t_this = this;
    userType.empty();
    var userTypeList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        userTypeList = userTypeList + '<option value="' + e.user_type_id + '"> ' + e.user_type + ' </option>';
    });
    userType.html(userTypeList);
};

UnitWiseReport.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.task_status_id + '"> ' + e.task_status + ' </option>';
    });
    complianceTaskStatus.html(complianceTaskStatusList);
};

UnitWiseReport.prototype.validate = function() {
    if (country) {
        if (isNotEmpty(country, message.country_required) == false)
            return false;
        else if (isLengthMinMax(country, 1, 50, message.country_max) == false)
            return false;
        else if (isCommonName(country, message.country_str) == false)
            return false;
    }
    if (countryId.val() == ""){
        displayMessage(message.country_required);
        country.focus();
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
    if (LegalEntityId.val() == "") {
        displayMessage(message.legalentity_required);
        LegalEntityName.focus();
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
    if (unitId.val() == ""){
        displayMessage(message.unit_required);
        unit.focus();
        return false;
    }
    if (domain) {
        if (isLengthMinMax(domain, 0, 50, message.domain_max) == false)
            return false;
        else if (isCommonName(domain, message.domain_str) == false)
            return false;
    }

    if (act) {
        if (isLengthMinMax(act, 0, 500, message.act_max) == false)
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

UnitWiseReport.prototype.fetchReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    le_id = LegalEntityId.val();
    d_id = domainId.val();
    if (d_id == "")
        d_id = 0;
    unit_id = unitId.val();
    stat_map = act.val();
    if (stat_map == "")
        stat_map = null;
    compl_id = complianceTaskId.val();
    if (compl_id == "")
        compl_id = 0;
    c_f_id = complianceFrequency.val();
    if (c_f_id == "")
        c_f_id = 0;
    u_t = $('#user-type option:selected').text().trim();
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    f_date = fromDate.val();
    t_date = toDate.val();
    c_t_s = $('#compliance-task-status option:selected').text().trim();

    client_mirror.getUnitWiseReport(
        parseInt(c_id), parseInt(le_id), parseInt(unit_id), parseInt(d_id), stat_map, parseInt(compl_id),
        parseInt(c_f_id), u_t, parseInt(user_id), f_date, t_date, c_t_s, csv, 0, 0,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._UnitCompliances = response.unit_compliances;
            t_this._total_record = response.total_count;
            t_this.processpaging();
        } else {
            t_this.possibleFailures(error);
        }
    });
};

UnitWiseReport.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._UnitCompliances;
    $('.le-header').text(LegalEntityName.val());
    $('.ctry-header').text(country.val());
    $('.unit-header').text(unit.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var domainname = "";
    var actname = "";
    var complianceHistoryId = null;
    var fileList = [];

    domain_names = [];
    act_names = [];
    for (var i=0;i<data.length;i++){
        var occur = -1;
        for(var j=0;j<domain_names.length;j++){
            if(data[i].domain_id == domain_names[j]){
                occur = 1;
                break;
            }
        }
        if(occur < 0){
            domain_names.push(data[i].domain_id);
        }
    }
    for (var i=0;i<data.length;i++){
        var occur = -1;
        for(var j=0;j<act_names.length;j++){
            if(data[i].statutory_mapping == act_names[j]){
                occur = 1;
                break;
            }
        }
        if(occur < 0){
            act_names.push(data[i].statutory_mapping);
        }
    }

    var u_count = 1;
    var sub_cnt = 0;
    for(var i=0;i<domain_names.length;i++){
        u_count = 1;
        var actname = "";
        for (var sm=0;sm<act_names.length;sm++){
            s_count = 1;
            actname = act_names[sm];
            $.each(data, function(k, v) {
                $('.unit-header').text(v.unit_name);
                is_null = false;
                $('.client-logo').attr("src", v.logo_url);
                if(v.domain_id == domain_names[i]){
                    // unit name cloning
                    if(u_count == 1){
                        var cloneone = $('#template #report-table .row-one').clone();
                        $('.domain-name', cloneone).text(v.domain_name);
                        reportTableTbody.append(cloneone);
                        domainname = v.domain_name;
                        u_count = u_count + 1;
                    }

                    if (actname == v.statutory_mapping) {
                        if(s_count == 1){
                            var clonetwo = $('#template #report-table .row-two').clone();
                            $('.act-name', clonetwo).text(v.statutory_mapping);
                            reportTableTbody.append(clonetwo);
                            actname = v.statutory_mapping;
                            s_count = s_count + 1;
                        }

                        if (complianceHistoryId != v.compliance_history_id){
                            var clonethree = $('#template #report-table .row-three').clone();
                            t_this._sno += 1;
                            $('.sno', clonethree).text(t_this._sno);
                            $('.compliance-task', clonethree).text(v.compliance_task);
                            $('.frequency', clonethree).text(v.frequency_name);
                            $('.due-date', clonethree).text(v.due_date);
                            $('.compliance-task-status', clonethree).text(v.task_status);
                            // $('.user-name', clonethree).addClass("-"+v.compliance_id);
                            // $('.user-name', clonethree).on('click', function() { tree_open_close(this); });
                            $('.activity-status', clonethree).text(v.activity_status);
                            if (v.activity_date != "")
                                $('.activity-date', clonethree).text(v.activity_date);
                            else
                                $('.activity-date', clonethree).text('-');
                            fileList = [];
                            if(v.document_name != null && v.document_name != "")
                            {
                                if (v.document_name.indexOf("|") >= 0)
                                    for(var f=0;f<v.document_name.split("|").length;f++) {
                                        fileList.push(v.document_name.split("|")[f]);
                                    }
                                else
                                    fileList.push(v.document_name);
                            }
                            if (fileList.length > 0) {
                                for(var doc=0;doc<fileList.length;doc++) {
                                    if(fileList[doc]!=''){
                                        var tableDocs = $('#template .temp-download');
                                        var cloneDocs = tableDocs.clone();
                                        $(".download-file", cloneDocs).text(fileList[doc]);
                                        $('.download-file', cloneDocs).on('click', function() {
                                            //download_url(v.url);
                                            f_name = $(this).text();
                                            c_id = countryId.val();
                                            le_id = LegalEntityId.val();
                                            d_id = domainId.val();
                                            client_mirror.downloadTaskFile(le_id, c_id, d_id, v.unit_id, v.start_date, f_name); //data.file_names[i]);
                                        });
                                        $('.uploaded-document', clonethree).append(cloneDocs);
                                    }
                                }
                            }
                            else {
                                $('.uploaded-document', clonethree).text('-');
                            }

                            if (v.completion_date != "")
                                $('.completion-date', clonethree).text(v.completion_date);
                            else
                                $('.completion-date', clonethree).text('-');
                            if (v.history_count > 1) {
                                $('#user_rows', clonethree).show();
                                $('#no_rows', clonethree).hide();
                                $('.user-name', clonethree).html(v.assignee_name);
                                $(clonethree).on('click', function(e) {
                                    treeShowHide(e, "tree" + v.compliance_history_id);
                                });
                                $(clonethree).attr("id", "tree" + v.compliance_history_id);
                            } else {
                                $('#user_rows', clonethree).hide();
                                $('#no_rows', clonethree).show();
                                $('.user-name', clonethree).html(v.assignee_name);
                            }
                            reportTableTbody.append(clonethree);
                            j = j + 1;
                            complianceHistoryId = v.compliance_history_id;
                        }
                        else {
                            var clonefour = $('#template #report-table .row-four').clone();
                            $(clonefour).addClass("tree" + v.compliance_history_id);
                            $('.user-name-new', clonefour).text(v.assignee_name);
                            $('.activity-status-new', clonefour).text(v.activity_status);
                            if (v.activity_date != "")
                                $('.activity-date-new', clonefour).text(v.activity_date);
                            else
                                $('.activity-date-new', clonefour).text('-');
                            fileList = [];
                            if(v.document_name != null && v.document_name != "")
                            {
                                if (v.document_name.indexOf("|") >= 0)
                                    for(var f=0;f<v.document_name.split("|").length;f++) {
                                        fileList.push(v.document_name.split("|")[f]);
                                    }
                                else
                                    fileList.push(v.document_name);
                            }
                            if (fileList.length > 0) {
                                for(var doc=0;doc<fileList.length;doc++) {
                                    if(fileList[doc]!=''){
                                        var tableDocs = $('#template .temp-download');
                                        var cloneDocs = tableDocs.clone();
                                        $(".download-file", cloneDocs).text(fileList[doc]);
                                        $('.download-file', cloneDocs).on('click', function() {
                                            //download_url(v.url);
                                            f_name = $(this).text();
                                            c_id = countryId.val();
                                            le_id = LegalEntityId.val();
                                            d_id = domainId.val();
                                            client_mirror.downloadTaskFile(le_id, c_id, d_id, v.unit_id, v.start_date, f_name); //data.file_names[i]);
                                        });
                                        $('.uploaded-document-new', clonefour).append(cloneDocs);
                                    }
                                }
                            }
                            else {
                                $('.uploaded-document-new', clonefour).text('-');
                            }

                            if (v.completion_date != "")
                                $('.completion-date-new', clonefour).text(v.completion_date);
                            else
                                $('.completion-date-new', clonefour).text('-');
                            reportTableTbody.append(clonefour);
                            j = j + 1;
                            sub_cnt = sub_cnt + 1;
                            complianceHistoryId = v.compliance_history_id;
                        }
                    }
                }
            });
        }
    }
};

treeShowHide = function(e, tree) {
    if ($('.' + tree)) {
        if ($('.' + tree).is(":visible") == true)
            $('.' + tree).hide();
        else
            $('.' + tree).show();
    }
};

function download_url(doc_url) {
    if(doc_url != null){
        window.open(doc_url, '_blank');
    }
}

UnitWiseReport.prototype.exportReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    le_id = LegalEntityId.val();
    d_id = domainId.val();
    if (d_id == "")
        d_id = 0;
    unit_id = unitId.val();
    stat_map = act.val();
    if (stat_map == "")
        stat_map = null;
    compl_id = complianceTaskId.val();
    if (compl_id == "")
        compl_id = 0;
    c_f_id = complianceFrequency.val();
    if (c_f_id == "")
        c_f_id = 0;
    u_t = $('#user-type option:selected').text().trim();
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    f_date = fromDate.val();
    t_date = toDate.val();
    c_t_s = $('#compliance-task-status option:selected').text().trim();

    client_mirror.getUnitWiseReport(
        parseInt(c_id), parseInt(le_id), parseInt(unit_id), parseInt(d_id), stat_map, parseInt(compl_id),
        parseInt(c_f_id), u_t, parseInt(user_id), f_date, t_date, c_t_s, csv, 0, 0,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            if(csv){
                document_url = response.link;
                $(location).attr('href', document_url);
            }
        } else {
            t_this.possibleFailures(error);
        }
    });
};

UnitWiseReport.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        this.displayMessage("Domain name exists");
    } else {
        this.displayMessage(error);
    }
};

// Pagination Functions - begins
hidePageView = function() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
};

createPageView = function(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    hidePageView();

    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            console.log(cPage, REPORT._on_current_page)
            if (parseInt(REPORT._on_current_page) != cPage) {
                REPORT._on_current_page = cPage;
                REPORT.fetchReportValues();
            }
        }
    });
};

UnitWiseReport.prototype.processpaging = function() {
    t_this = this;
    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        this._sno = 0;
    }
    else {
        this._sno = (this._on_current_page - 1) *  _page_limit;
    }

    sno  = t_this._sno;
    //totalRecord = industriesList.length;
    ReportData = REPORT.pageData(on_current_page);
    if (t_this._total_record == 0) {
        $('.le-header').text(LegalEntityName.val());
        $('.ctry-header').text(country.val());
        $('.unit-header').text(unit.val());
        reportTableTbody.empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        reportTableTbody.append(clone4);
        hidePageView();
        hidePagePan();
    } else {
        if(sno==0){
            createPageView(t_this._total_record);
        }
        $('.pagination-view').show();
        //ReportView.show();
        REPORT.showReportValues(ReportData);
    }
};

UnitWiseReport.prototype.pageData = function(on_current_page) {
    t_this = this;
    data = [];
    recordData = [];
    _page_limit = parseInt(ItemsPerPage.val());
    recordLength = (parseInt(on_current_page) * _page_limit);
    var showFrom = t_this._sno + 1;
    var is_null = true;
    recordData = t_this._UnitCompliances;
    totalRecord = t_this._total_record;
    var c_h_id = null;
    var history_id = [];
    for (var i=0;i<recordData.length;i++){
        var occur = -1;
        for(var j=0;j<history_id.length;j++){
            if(recordData[i].compliance_history_id == history_id[j]){
                occur = 1;
                break;
            }
        }
        if(occur < 0){
            history_id.push(recordData[i].compliance_history_id);
        }
    }

    for(i=t_this._sno;i<history_id.length;i++)
    {
        console.log("1:"+i);
        is_null = false;
        c_h_id = history_id[i];
        console.log("2:"+c_h_id)
        for(var j=0;j<recordData.length;j++){
            if(c_h_id == recordData[j].compliance_history_id){
                console.log("3:"+recordData[j].compliance_history_id)
                data.push(recordData[j]);
            }
        }
        if(i == (recordLength-1))
        {
            break;
        }
    }
    //totalRecord = data.length;
    if (is_null == true) {
        hidePagePan();
    }
    else {
        if(recordLength < totalRecord)
            showPagePan(showFrom, recordLength, totalRecord);
        else
            showPagePan(showFrom, totalRecord, totalRecord);
    }
    return data;
}

showPagePan = function(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};
hidePagePan = function() {
    $('.compliance_count').text('');
    $('.pagination-view').hide();
}

// Pagination Ends

REPORT = new UnitWiseReport();

$(document).ready(function() {
    $('.row-three').click(function() {
        $('.row-four').toggle("slow");
    });
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});
