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

var ServiceProvider = $("#service-provider");
var ServiceProviderId = $("#service-provider-id");
var ACServiceProvider = $("#ac-service-provider");

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

var users = $("#user");
var userId = $("#user-id");
var acUser = $("#ac-user");
var fromDate = $("#from_date");
var toDate = $("#to_date");
var complianceTaskStatus = $("#compliance-task-status");
var ServiceProviderCompliances = [];

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

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

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

    ServiceProvider.keyup(function(e) {
        var text_val = ServiceProvider.val().trim();
        var spList = REPORT._sp_list;
        commonAutoComplete(e, ACServiceProvider, ServiceProviderId, text_val, spList, "sp_name", "sp_id", function(val) {
            onServiceProviderAutoCompleteSuccess(REPORT, val);
        });
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["sp_id_optional"];
        var condition_values = [ServiceProviderId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "domain_name", "domain_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = [];
        for(var i=0;i<REPORT._units.length;i++){
            if(REPORT._units[i].sp_id_optional == ServiceProviderId.val() && REPORT._units[i].domain_id == domainId.val()){
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

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._acts;
        var newActList = [];
        var sp_id = ServiceProviderId.val();
        for(var i=0;i<actList.length;i++){
            if(sp_id == actList[i].sp_ass_id_optional || sp_id == actList[i].sp_app_id_optional || sp_id == actList[i].sp_cc_id_optional){
                newActList.push({
                    "domain_id": actList[i].domain_id,
                    "unit_id": actList[i].unit_id,
                    "compliance_id": actList[i].compliance_id,
                    "statutory_mapping": actList[i].statutory_mapping
                });
            }
        }
        var condition_fields = ["domain_id"];
        var condition_values = [domainId.val()];
        if (unitId.val() != ""){
            condition_fields.push("unit_id");
            condition_values.push(unitId.val())
        }
        commonAutoComplete(e, acAct, actId, text_val, newActList, "statutory_mapping", "compliance_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        clearElement([users, userId]);
    });

    users.keyup(function(e) {
        var text_val = users.val().trim();
        var userList = REPORT._users;
        var condition_fields = ["sp_id_optional","domain_id"];
        var condition_values = [ServiceProviderId.val(), domainId.val()];
        if (unitId.val() != ""){
            condition_fields.push("unit_id");
            condition_values.push(unitId.val())
        }
        if (actId.val() != ""){
            condition_fields.push("compliance_id");
            condition_values.push(actId.val());
        }
        commonAutoComplete(e, acUser, userId, text_val, userList, "user_name", "user_id", function(val) {
            onUserAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    showButton.click(function() {
        if (REPORT.validate()) {
            csv = false;
            on_current_page = 1;
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
        on_current_page = 1;
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
    clearElement([LegalEntityName, LegalEntityId, ServiceProvider, ServiceProviderId, domain, domainId, unit, unitId, act, actId, complianceTask, users, userId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    clearElement([ServiceProvider, ServiceProviderId, domain, domainId, unit, unitId, act, actId, complianceTask, users, userId]);
    REPORT.fetchServiceProviderList(countryId.val(), val[0]);
}

onServiceProviderAutoCompleteSuccess = function(REPORT, val) {
    ServiceProvider.val(val[1]);
    ServiceProviderId.val(val[0]);
    ServiceProvider.focus();
    clearElement([domain, domainId, unit, unitId, act, actId, complianceTask, users, userId]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([unit, unitId, act, actId, complianceTask, users, userId]);
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([act, actId, complianceTask, users, userId]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
    clearElement([complianceTask, users, userId]);
}

onUserAutoCompleteSuccess = function(REPORT, val) {
    users.val(val[1]);
    userId.val(val[0]);
    users.focus();
}
ServiceProviderWiseReport = function() {
    this._countries = [];
    this._entities = [];
    this._sp_list = [];
    this._domains = [];
    this._units = [];
    this._acts = [];
    //this._compliance_task = [];
    this._users = [];
    this._compliance_task_status = [];
    this._report_data = [];
    on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
    this._ServiceProviderCompliances = [];
}

ServiceProviderWiseReport.prototype.loadSearch = function() {
    reportView.hide();
    country.val('');
    countryId.val('');
    LegalEntityName.val('');
    LegalEntityId.val('');
    ServiceProvider.val('');
    ServiceProviderId.val('');
    domain.val('');
    domainId.val('');
    unit.val('');
    unitId.val('');
    act.val('');
    actId.val('');
    complianceTask.val('');
    users.val('');
    userId.val('');
    fromDate.val('');
    toDate.val('');
    complianceTaskStatus.empty();
    this.fetchSearchList();
};

ServiceProviderWiseReport.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

ServiceProviderWiseReport.prototype.loadEntityDetails = function(){
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
        REPORT.fetchServiceProviderList(c_id, le_id);
    }
    hideLoader();
};

ServiceProviderWiseReport.prototype.fetchServiceProviderList = function(c_id, le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getServiceProviderWiseReportFilters(parseInt(c_id), parseInt(le_id), function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._sp_list = response.sp_list;
            t_this._domains = response.sp_domains_list;
            t_this._units = response.sp_unit_list;
            t_this._acts = response.sp_act_task_list;
            t_this._compliance_task_status = response.compliance_task_status;
            REPORT.renderComplianceTaskStatusList(t_this._compliance_task_status);
            t_this._users = response.sp_users_list;
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

ServiceProviderWiseReport.prototype.renderComplianceTaskStatusList = function(data) {
    t_this = this;
    complianceTaskStatus.empty();
    var complianceTaskStatusList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        complianceTaskStatusList = complianceTaskStatusList + '<option value="' + e.task_status_id + '"> ' + e.task_status + ' </option>';
    });
    complianceTaskStatus.html(complianceTaskStatusList);
};

ServiceProviderWiseReport.prototype.validate = function() {
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
    if (ServiceProvider) {
        if (isNotEmpty(ServiceProvider, message.spname_required) == false)
            return false;
        else if (isLengthMinMax(ServiceProvider, 1, 100, message.legalentity_max) == false)
            return false;
        else if (isCommonName(ServiceProvider, message.legalentity_str) == false)
            return false;
    }
    if (ServiceProviderId.val() == "") {
        displayMessage(message.spname_required);
        ServiceProvider.focus();
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
    if (domainId.val() == "") {
        displayMessage(message.domain_required);
        domain.focus();
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

ServiceProviderWiseReport.prototype.fetchReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    le_id = LegalEntityId.val();
    sp_id = ServiceProviderId.val();
    d_id = domainId.val();
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
    stat_map = act.val();
    if (stat_map == "")
        stat_map = null;
    compliance_task = complianceTask.val().trim();
    if (compliance_task == "")
        compliance_task = null;
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    f_date = fromDate.val();
    t_date = toDate.val();
    c_t_s = $('#compliance-task-status option:selected').text().trim();
    displayLoader();
    client_mirror.getServiceProviderWiseReport(
        parseInt(c_id), parseInt(le_id), parseInt(sp_id), parseInt(d_id), parseInt(unit_id), stat_map, compliance_task,
        parseInt(user_id), f_date, t_date, c_t_s, csv, 0, 0,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._ServiceProviderCompliances = response.sp_compliances;
            t_this._total_record = response.total_count;
            t_this.processpaging();
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

ServiceProviderWiseReport.prototype.showReportValues = function(data) {
    t_this = this;
    //var data = t_this._ServiceProviderCompliances;
    $('.le-header').text(LegalEntityName.val());
    $('.ctry-header').text(country.val());
    $('.dom-header').text(domain.val());
    $('.sp-name').text(ServiceProvider.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var unitname = "";
    var actname = "";
    var complianceHistoryId = null;
    var fileList = [];

    unit_names = [];
    act_names = [];
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
    //t_this._total_record = data.length;
    var u_count = 1;
    var sub_cnt = 0;
    for(var i=0;i<unit_names.length;i++){
        u_count = 1;
        var actname = "";
        for (var sm=0;sm<act_names.length;sm++){
            s_count = 1;
            actname = act_names[sm];
            $.each(data, function(k, v) {
                is_null = false;
                if (v.logo_url != null)
                    clientLogo.attr("src", v.logo_url);
                else
                    clientLogo.remove();
                if(v.unit_id == unit_names[i]){
                    // unit name cloning
                    if(u_count == 1){
                        var cloneone = $('#template #report-table .row-one').clone();
                        $('.unit-name', cloneone).text(v.unit_name);
                        reportTableTbody.append(cloneone);
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
                    }
                }
            });
        }
    }
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

ServiceProviderWiseReport.prototype.exportReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    le_id = LegalEntityId.val();
    sp_id = ServiceProviderId.val();
    d_id = domainId.val();
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
    stat_map = act.val();
    if (stat_map == "")
        stat_map = null;
    compliance_task = complianceTask.val().trim();
    if (compliance_task == "")
        compliance_task = null;
    user_id = userId.val();
    if (user_id == "")
        user_id = 0;
    f_date = fromDate.val();
    t_date = toDate.val();
    c_t_s = $('#compliance-task-status option:selected').text().trim();
    displayLoader();
    client_mirror.getServiceProviderWiseReport(
        parseInt(c_id), parseInt(le_id), parseInt(sp_id), parseInt(d_id), parseInt(unit_id), stat_map, compliance_task,
        parseInt(user_id), f_date, t_date, c_t_s, csv, 0, 0,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            hideLoader();
            if(csv){
                document_url = response.link;
                $(location).attr('href', document_url);
            }
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

ServiceProviderWiseReport.prototype.possibleFailures = function(error) {
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
            console.log(cPage, on_current_page)
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                REPORT.fetchReportValues();
            }
        }
    });
};

ServiceProviderWiseReport.prototype.processpaging = function() {
    t_this = this;
    _page_limit = parseInt(ItemsPerPage.val());
    if (on_current_page == 1) {
        this._sno = 0;
    }
    else {
        this._sno = (on_current_page - 1) *  _page_limit;
    }

    sno  = t_this._sno;
    //totalRecord = industriesList.length;
    ReportData = REPORT.pageData(on_current_page);
    if (t_this._total_record == 0) {
        $('.le-header').text(LegalEntityName.val());
        $('.ctry-header').text(country.val());
        $('.dom-header').text(domain.val());
        $('.sp-name').text(ServiceProvider.val());
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

ServiceProviderWiseReport.prototype.pageData = function(on_current_page) {
    t_this = this;
    data = [];
    recordData = [];
    _page_limit = parseInt(ItemsPerPage.val());
    recordLength = (parseInt(on_current_page) * _page_limit);
    var showFrom = t_this._sno + 1;
    var is_null = true;
    recordData = t_this._ServiceProviderCompliances;
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

REPORT = new ServiceProviderWiseReport();

$(document).ready(function() {
    displayLoader();
    $('.row-three').click(function() {
        $('.row-four').toggle("slow");
    });
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});
