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

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var userList = REPORT._users;
        commonAutoComplete(e, acUser, userId, text_val, userList, "username", "user_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        });
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["user_id"];
        var condition_values = [userId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "domain_name", "domain_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = [];
        for(var i=0;i<REPORT._units.length;i++){
            unitList.push({
                "user_id_optional": REPORT._units[i].user_id_optional,
                "domain_id": REPORT._units[i].domain_id,
                "unit_id": REPORT._units[i].unit_id,
                "unit_name": REPORT._units[i].unit_code+" - "+REPORT._units[i].unit_name
            });
        }
        condition_fields = ["user_id_optional"];
        condition_values = [userId.val()];
        if (domainId.val() != ""){
            condition_fields.push("domain_id");
            condition_values.push(domainId.val())
        }
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._compliance_task;
        var newActList = [];
        var u_id = userId.val();
        for(var i=0;i<actList.length;i++){
            if(u_id == actList[i].assignee){
                newActList.push({
                    "user_id_optional": actList[i].assignee,
                    "domain_id": actList[i].domain_id,
                    "unit_id": actList[i].unit_id,
                    "compliance_id": actList[i].compliance_id,
                    "statutory_mapping": actList[i].statutory_mapping
                });
            }
            if(u_id == actList[i].concurrence_person){
                newActList.push({
                    "user_id_optional": actList[i].concurrence_person,
                    "domain_id": actList[i].domain_id,
                    "unit_id": actList[i].unit_id,
                    "compliance_id": actList[i].compliance_id,
                    "statutory_mapping": actList[i].statutory_mapping
                });
            }
            if(u_id == actList[i].approval_person){
                newActList.push({
                    "user_id_optional": actList[i].approval_person,
                    "domain_id": actList[i].domain_id,
                    "unit_id": actList[i].unit_id,
                    "compliance_id": actList[i].compliance_id,
                    "statutory_mapping": actList[i].statutory_mapping
                });
            }
        }
        condition_fields = ["user_id_optional"];
        condition_values = [userId.val()];
        if (domainId.val() != ""){
            condition_fields.push("domain_id");
            condition_values.push(domainId.val())
        }
        if (unitId.val() != ""){
            condition_fields.push("unit_id");
            condition_values.push(unitId.val())
        }
        commonAutoComplete(e, acAct, actId, text_val, newActList, "statutory_mapping", "compliance_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        var newTaskList = [];
        var u_id = userId.val();
        for(var i=0;i<complianceTaskList.length;i++){
            if(u_id == complianceTaskList[i].assignee){
                newTaskList.push({
                    "user_id_optional": complianceTaskList[i].assignee,
                    "domain_id": complianceTaskList[i].domain_id,
                    "unit_id": complianceTaskList[i].unit_id,
                    "compliance_id": complianceTaskList[i].compliance_id,
                    "statutory_mapping": complianceTaskList[i].statutory_mapping,
                    "compliance_task": complianceTaskList[i].compliance_task
                });
            }
            if(u_id == complianceTaskList[i].approval_person){
                newTaskList.push({
                    "user_id_optional": complianceTaskList[i].approval_person,
                    "domain_id": complianceTaskList[i].domain_id,
                    "unit_id": complianceTaskList[i].unit_id,
                    "compliance_id": complianceTaskList[i].compliance_id,
                    "statutory_mapping": complianceTaskList[i].statutory_mapping,
                    "compliance_task": complianceTaskList[i].compliance_task
                });
            }
            if(u_id == complianceTaskList[i].concurrence_person){
                newTaskList.push({
                    "user_id_optional": complianceTaskList[i].concurrence_person,
                    "domain_id": complianceTaskList[i].domain_id,
                    "unit_id": complianceTaskList[i].unit_id,
                    "compliance_id": complianceTaskList[i].compliance_id,
                    "statutory_mapping": complianceTaskList[i].statutory_mapping,
                    "compliance_task": complianceTaskList[i].compliance_task
                });
            }
        }
        condition_fields = ["user_id_optional"];
        condition_values = [userId.val()];
        if (domainId.val() != ""){
            condition_fields.push("domain_id");
            condition_values.push(domainId.val())
        }
        if (unitId.val() != ""){
            condition_fields.push("unit_id");
            condition_values.push(unitId.val())
        }
        if (act.val() != ""){
            condition_fields.push("statutory_mapping");
            condition_values.push(act.val().trim())
        }
        commonAutoComplete(e, acComplianceTask, complianceTaskId, text_val, newTaskList, "compliance_task", "compliance_id", function(val) {
            onComplianceTaskAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
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
    clearElement([LegalEntityName, LegalEntityId, users, userId, domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    clearElement([users, userId, domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchUsersList(countryId.val(), val[0]);
}

onUserAutoCompleteSuccess = function(REPORT, val) {
    users.val(val[1]);
    userId.val(val[0]);
    users.focus();
    clearElement([domain, domainId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
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

UserWiseReport = function() {
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
    this._UserCompliances = [];
}

UserWiseReport.prototype.loadSearch = function() {
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

UserWiseReport.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

UserWiseReport.prototype.loadEntityDetails = function(){
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
        REPORT.fetchUsersList(c_id, le_id);
    }

};

UserWiseReport.prototype.fetchUsersList = function(c_id, le_id) {
    t_this = this;
    client_mirror.getUserWiseReportFilters(parseInt(c_id), parseInt(le_id), function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._domains = response.user_domains_list;
            t_this._units = response.users_units_list;
            t_this._acts = response.user_act_task_list;
            t_this._compliance_task = response.user_act_task_list;
            t_this._compliance_task_status = response.compliance_task_status;
            REPORT.renderComplianceTaskStatusList(t_this._compliance_task_status);
            t_this._frequencies = response.compliance_frequency_list;
            REPORT.renderComplianceFrequencyList(t_this._frequencies);
            t_this._user_type = response.compliance_user_type;
            REPORT.renderUserTypeList(t_this._user_type);
            t_this._users = response.le_users_list;
        } else {
            t_this.possibleFailures(error);
        }
    });
};

UserWiseReport.prototype.renderCountriesList = function(data) {
    t_this = this;
    country.empty();
    var countryName = [];
    $.each(data, function(i, e) {
        //countryName.push(e.c_name+",");
        countryName = e.c_name;
    });
    country.html(countryName);
};

UserWiseReport.prototype.renderLegalEntityList = function(data) {
    t_this = this;
    legalEntity.empty();
    var legalEntityName = [];
    $.each(data, function(i, e) {
        //legalEntityName.push(e.le_name+",");
        legalEntityName = e.le_name;
    });
    legalEntity.html(legalEntityName);
};

UserWiseReport.prototype.renderComplianceFrequencyList = function(data) {
    t_this = this;
    complianceFrequency.empty();
    var complianceFrequencyList = '<option value="0">All</option>';
    $.each(data, function(i, e) {
        complianceFrequencyList = complianceFrequencyList + '<option value="' + e.frequency_id + '"> ' + e.frequency_name + ' </option>';
    });
    complianceFrequency.html(complianceFrequencyList);
};

UserWiseReport.prototype.renderUserTypeList = function(data) {
    t_this = this;
    userType.empty();
    var userTypeList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        userTypeList = userTypeList + '<option value="' + e.user_type_id + '"> ' + e.user_type + ' </option>';
    });
    userType.html(userTypeList);
};

UserWiseReport.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.task_status_id + '"> ' + e.task_status + ' </option>';
    });
    complianceTaskStatus.html(complianceTaskStatusList);
};

UserWiseReport.prototype.validate = function() {
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
    if (users) {
        if (isNotEmpty(users, message.user_required) == false)
            return false;
        else if (isLengthMinMax(users, 0, 70, message.user_max) == false)
            return false;
        else if (isCommonName(users, message.user_str) == false)
            return false;
    }
    if (userId.val() == ""){
        displayMessage(message.user_required);
        users.focus();
        return false;
    }
    if (domain) {
        if (isLengthMinMax(domain, 0, 50, message.domain_max) == false)
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

UserWiseReport.prototype.fetchReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    le_id = LegalEntityId.val();
    user_id = userId.val();
    d_id = domainId.val();
    if (d_id == "")
        d_id = 0;
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
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
    f_date = fromDate.val();
    t_date = toDate.val();
    c_t_s = $('#compliance-task-status option:selected').text().trim();

    client_mirror.getUserWiseReport(
        parseInt(c_id), parseInt(le_id), parseInt(user_id), parseInt(d_id), parseInt(unit_id), stat_map, parseInt(compl_id),
        parseInt(c_f_id), u_t, f_date, t_date, c_t_s, csv, 0, 0,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._UserCompliances = response.user_compliances;
            t_this._total_record = response.total_count;
            t_this.processpaging();
        } else {
            t_this.possibleFailures(error);
        }
    });
};

UserWiseReport.prototype.showReportValues = function(data) {
    t_this = this;
    //var data = t_this._UserCompliances;
    $('.le-header').text(LegalEntityName.val());
    $('.ctry-header').text(country.val());
    $('.usr-header').text(users.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var unitname = "";
    var domainname = ""
    var actname = "";
    var complianceHistoryId = null;
    var fileList = [];
    unit_names = [];
    act_names = [];
    domain_names = [];
    for (var i=0;i<data.length;i++){
        var occur = -1;
        for(var j=0;j<unit_names.length;j++){
            if(data[i].unit_id == unit_names[j]){
                occur = 1;
                break;
            }
        }
        if(occur < 0){
            unit_names.push(data[i].unit_id);
        }
    }
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
    var d_count = 1;
    var sub_cnt = 0;
    for(var i=0;i<unit_names.length;i++){
        u_count = 1;
        domainname = ""
        for(var d=0;d<domain_names.length;d++){
            d_count = 1;
            domainname = domain_names[d];
            var actname = "";
            for (var sm=0;sm<act_names.length;sm++){
                s_count = 1;
                actname = act_names[sm];
                $.each(data, function(k, v) {
                    console.log("A:"+unit_names[i], domainname, actname, complianceHistoryId)
                    is_null = false;
                    $('.client-logo').attr("src", v.logo_url);
                    if(v.unit_id == unit_names[i] && domainname == v.domain_id){
                        if (u_count == 1){
                            var cloneone = $('#template #report-table .row-one').clone();
                            $('.domain-name', cloneone).text("Domain : "+v.domain_name);
                            $('.unit-name', cloneone).text("Unit : "+v.unit_name);
                            reportTableTbody.append(cloneone);
                            unitname = v.unit_id;
                            domainname = v.domain_id;
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
                                console.log("1:"+unit_names[i], domainname, actname, complianceHistoryId)
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
                                if (v.document_name != "" && v.document_name != "-") {
                                    var files = v.document_name.split(",");
                                    $.each(files, function(k1) {
                                        $('.uploaded-document', clonethree).append(
                                            $('<a/>')
                                            .addClass("c-pointer")
                                            .attr("onClick", "downloadFile("+LegalEntityId.val()+", "+countryId.val()+", "+domainId.val()+", "+v.unit_id+", '"+v.start_date+"', '"+files[k1]+"')")
                                            .text(files[k1]),
                                            $('<br/>')
                                        );
                                    });
                                } else {
                                    $('.uploaded-document', clonethree).html("-");
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
                                console.log("2:"+unit_names[i], domainname, actname, complianceHistoryId)
                                var clonefour = $('#template #report-table .row-four').clone();
                                $(clonefour).addClass("tree" + v.compliance_history_id);
                                $('.user-name-new', clonefour).text(v.assignee_name);
                                $('.activity-status-new', clonefour).text(v.activity_status);
                                if (v.activity_date != "")
                                    $('.activity-date-new', clonefour).text(v.activity_date);
                                else
                                    $('.activity-date-new', clonefour).text('-');
                                if (v.document_name != "" && v.document_name != "-") {
                                    var files = v.document_name.split(",");
                                    $.each(files, function(k1) {
                                        console.log(v.compliance_history_id, files[k1])
                                        $('.uploaded-document-new', clonefour).append(
                                            $('<a/>')
                                            .addClass("c-pointer")
                                            .attr("onClick", "downloadFile("+LegalEntityId.val()+", "+countryId.val()+", "+domainId.val()+", "+v.unit_id+", '"+v.start_date+"', '"+files[k1]+"')")
                                            .text(files[k1]),
                                            $('<br/>')
                                        );
                                    });
                                } else {
                                    $('.uploaded-document-new', clonefour).html("-");
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
                        } //act checking
                    } // unit & domain checking
                }); // data loop
            } // act loop
        } // domain loop
    } // unit loop
};

downloadFile = function(le_id, c_id, d_id, u_id, date, file) {
    client_mirror.downloadTaskFile(parseInt(le_id), parseInt(c_id), parseInt(d_id), parseInt(u_id), date, file);
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

UserWiseReport.prototype.exportReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    le_id = LegalEntityId.val();
    user_id = userId.val();
    d_id = domainId.val();
    if (d_id == "")
        d_id = 0;
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
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
    f_date = fromDate.val();
    t_date = toDate.val();
    c_t_s = $('#compliance-task-status option:selected').text().trim();

    client_mirror.getUserWiseReport(
        parseInt(c_id), parseInt(le_id), parseInt(user_id), parseInt(d_id), parseInt(unit_id), stat_map, parseInt(compl_id),
        parseInt(c_f_id), u_t, f_date, t_date, c_t_s, csv, 0, 0,
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

UserWiseReport.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage(message.domainname_exists);
    } else if (error == "ExportToCSVEmpty") {
        displayMessage(message.empty_export);
    } else {
        displayMessage(error);
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

UserWiseReport.prototype.processpaging = function() {
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
        $('.usr-header').text(users.val());
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
        showAnimation(reportView);
        REPORT.showReportValues(ReportData);
    }
};

UserWiseReport.prototype.pageData = function(on_current_page) {
    t_this = this;
    data = [];
    recordData = [];
    _page_limit = parseInt(ItemsPerPage.val());
    recordLength = (parseInt(on_current_page) * _page_limit);
    console.log("1:"+recordLength)
    var showFrom = t_this._sno + 1;
    var is_null = true;
    recordData = t_this._UserCompliances;
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
        is_null = false;
        c_h_id = history_id[i];
        for(var j=0;j<recordData.length;j++){
            if(c_h_id == recordData[j].compliance_history_id){
                data.push(recordData[j]);
            }
        }
        if(i == (recordLength-1))
        {
            console.log("2:"+i)
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

REPORT = new UserWiseReport();

$(document).ready(function() {
    $('.row-three').click(function() {
        $('.row-four').toggle("slow");
    });
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});

