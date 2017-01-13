var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");

var businessGroup = $("#business-group");
var businessGroupId = $("#business-group-id");
var acBusinessGroup = $("#ac-business-group");

var legalEntity = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");

var division = $("#division");
var divisionId = $("#division-id");
var acDivision = $("#ac-division");

var category = $("#category");
var categoryId = $("#category-id");
var acCategory = $("#ac-category");

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
    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._countries;
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            onCountryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    businessGroup.keyup(function(e) {
        var text_val = businessGroup.val().trim();
        var businessGroupList = REPORT._business_group;
        var condition_fields = ["is_active", "c_id"];
        var condition_values = [true, countryId.val()];
        commonAutoComplete(e, acBusinessGroup, businessGroupId, text_val, businessGroupList, "b_g_name", "b_g_id", function(val) {
            onBusinessGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntity.keyup(function(e) {
        var text_val = legalEntity.val().trim();
        var legalEntityList = REPORT._entities;
        var condition_fields = ["is_active", "c_id", "b_g_id"];
        var condition_values = [true, countryId.val(), businessGroupId.val()];
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, legalEntityId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "dom_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    division.keyup(function(e) {
        var text_val = division.val().trim();
        var divisionList = REPORT._divisions;
        var condition_fields = ["is_active", "d_id"];
        var condition_values = [true, domainId.val()];
        commonAutoComplete(e, acDivision, divisionId, text_val, divisionList, "div_name", "div_id", function(val) {
            onDivisionAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    category.keyup(function(e) {
        var text_val = category.val().trim();
        var categoryList = REPORT._categorys;
        var condition_fields = ["is_active", "div_id", "d_id"];
        var condition_values = [true, divisionId.val(), domainId.val()];
        commonAutoComplete(e, acCategory, categoryId, text_val, categoryList, "cat_name", "cat_id", function(val) {
            onCategoryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = REPORT._units;
        var condition_fields = ["is_active", "div_id", "d_id", "cat_id" ];
        var condition_values = [true, divisionId.val(), domainId.val(), categoryId.val()];
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "u_name", "u_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._acts;
        var condition_fields = ["is_active", "div_id", "d_id", "cat_id", "u_id"];
        var condition_values = [true, divisionId.val(), domainId.val(), categoryId.val(), unitId.val()];
        commonAutoComplete(e, acAct, actId, text_val, actList, "act_name", "act_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    complianceTask.keyup(function(e) {
        var text_val = complianceTask.val().trim();
        var complianceTaskList = REPORT._compliance_task;
        var condition_fields = ["is_active", "div_id", "d_id", "cat_id", "u_id", "act_id"];
        var condition_values = [true, divisionId.val(), domainId.val(), categoryId.val(), unitId.val(), actId.val()];
        commonAutoComplete(e, acComplianceTask, complianceTaskId, text_val, complianceTaskList, "com_task", "com_id", function(val) {
            onComplianceTaskAutoCompleteSuccess(REPORT, val);
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

onCountryAutoCompleteSuccess = function(REPORT, val) {
    country.val(val[1]);
    countryId.val(val[0]);
    country.focus();
    clearElement([businessGroup, businessGroupId, legalEntity, legalEntityId, domain, domainId, division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
}

onBusinessGroupAutoCompleteSuccess = function(REPORT, val) {
    businessGroup.val(val[1]);
    businessGroupId.val(val[0]);
    businessGroup.focus();
    clearElement([legalEntity, legalEntityId, domain, domainId, division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    legalEntity.val(val[1]);
    legalEntityId.val(val[0]);
    legalEntity.focus();
    clearElement([domain, domainId, division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchDomainList(val[0]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchDivisionList(val[0]);
}

onDivisionAutoCompleteSuccess = function(REPORT, val) {
    division.val(val[1]);
    divisionId.val(val[0]);
    division.focus();
    clearElement([category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchCategoryList(val[0], domainId.val());
}

onCategoryAutoCompleteSuccess = function(REPORT, val) {
    category.val(val[1]);
    categoryId.val(val[0]);
    category.focus();
    clearElement([unit, unitId, act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchUnitList(val[0], divisionId.val(), domainId.val());
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([act, actId, complianceTask, complianceTaskId]);
    REPORT.fetchActList(val[0], categoryId.val(), divisionId.val(), domainId.val());
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
    clearElement([complianceTask, complianceTaskId]);
    REPORT.fetchComplianceaskList(val[0], unitId.val(), categoryId.val(), divisionId.val(), domainId.val());
}

onComplianceTaskAutoCompleteSuccess = function(REPORT, val) {
    complianceTask.val(val[1]);
    complianceTaskId.val(val[0]);
    complianceTask.focus();
}

StatusReportConsolidated = function() {
    this._countries = [];
    this._business_group = [];
    this._entities = [];
    this._domains = [];
    this._divisions = [];
    this._categorys = [];
    this._units = [];
    this._acts = [];
    this._compliance_task = [];
    this._frequencies = [];
    this._compliance_task_status = [];
    this._report_data = [];
}

StatusReportConsolidated.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, businessGroup, businessGroupId, legalEntity, legalEntityId, domain, domainId, division, divisionId, category, categoryId, unit, unitId, act, actId, complianceTask, complianceTaskId]);
    complianceFrequency.empty();
    complianceTaskStatus.empty();
    this.fetchSearchList();
};

StatusReportConsolidated.prototype.fetchSearchList = function() {
    t_this = this;
    var jsondata = '{"countries":[{"c_id":1,"c_name":"india","is_active":true},{"c_id":2,"c_name":"srilanka","is_active":true}],"business_group":[{"b_g_id":1,"b_g_name":"RG Business Group","c_id":1,"is_active":true},{"b_g_id":2,"b_g_name":"ABC Business Group","c_id":1,"is_active":true}],"entities":[{"le_id":1,"le_name":"RG Legal Entity","c_id":1,"b_g_id":1,"is_active":true},{"le_id":2,"le_name":"ABC Legal Entity","c_id":1,"b_g_id":1,"is_active":true}],"frequencies":[{"f_id":1,"f_name":"Periodical"},{"f_id":2,"f_name":"Review"},{"f_id":3,"f_name":"Flexi Review"},{"f_id":4,"f_name":"One Time"}],"user_type":[{"user_type_id":1,"user_type_name":"Assignee"},{"user_type_id":2,"user_type_name":"Concurrence"},{"user_type_id":3,"user_type_name":"Approval"}],"compliance_task_status":[{"comp_task_status_id":1,"comp_task_status":"Complied"},{"comp_task_status_id":2,"comp_task_status":"Delayed Compliances"},{"comp_task_status_id":3,"comp_task_status":"Inprogress"},{"comp_task_status_id":4,"comp_task_status":"Not Complied"}],"service_providers":[{"s_p_id":1,"s_p_name":"String","s_p_shrot":"short"}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._countries = object.countries;
    t_this._business_group = object.business_group;
    t_this._entities = object.entities;
    t_this._frequencies = object.frequencies;
    t_this._complianceTaskStatus = object.compliance_task_status;

    t_this.renderComplianceFrequencyList(t_this._frequencies);
    t_this.renderComplianceTaskStatusList(t_this._complianceTaskStatus);
};

StatusReportConsolidated.prototype.fetchDomainList = function(le_id) {
    t_this = this;
    var jsondata = '{"domains":[{"d_id":1,"dom_name":"Labour Law","le_id":1,"is_active":true},{"d_id":2,"dom_name":"Finance Law","le_id":2,"is_active":true},{"d_id":3,"dom_name":"Employee Law","le_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._domains = object.domains;
};

StatusReportConsolidated.prototype.fetchDivisionList = function(d_id) {
    t_this = this;
    var jsondata = '{"divisions":[{"div_id":1,"div_name":"Labour Law","d_id":1,"is_active":true},{"div_id":2,"div_name":"Finance Law","d_id":1,"is_active":true},{"div_id":3,"div_name":"Employee Law","d_id":2,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._divisions = object.divisions;
};

StatusReportConsolidated.prototype.fetchCategoryList = function(div_id, d_id) {
    t_this = this;
    var jsondata = '{"categorys":[{"cat_id":1,"cat_name":"RG Category one","d_id":1,"div_id":1,"is_active":true},{"cat_id":2,"cat_name":"RG Category two","d_id":1,"div_id":1,"is_active":true},{"cat_id":3,"cat_name":"ABC Category","d_id":2,"div_id":2,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._categorys = object.categorys;
};

StatusReportConsolidated.prototype.fetchUnitList = function(cat_id, div_id, d_id) {
    t_this = this;
    var jsondata = '{"units":[{"u_id":1,"u_name":"RG1034 - RG Madurai Unit","u_code":"RG1034","address":"12 RJ Complex, Main road, Madurai, 625022","div_id":1,"d_id":1,"cat_id":1,"is_active":true},{"u_id":2,"u_name":"RG1035 - RG Dindugal Unit","u_code":"RG1035","address":"10 RG Complex, Main road, Dindugal, 623020","div_id":1,"d_id":1,"cat_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._units = object.units;
};

StatusReportConsolidated.prototype.fetchActList = function(unit_id, cat_id, div_id, d_id) {
    t_this = this;
    var jsondata = '{"acts":[{"act_id":1,"act_name":"The Batteries Act","div_id":1,"d_id":1,"cat_id":1,"u_id":1,"is_active":true},{"act_id":2,"act_name":"Indian Partnership Act, 1932","div_id":1,"d_id":1,"cat_id":1,"u_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._acts = object.acts;
};

StatusReportConsolidated.prototype.fetchComplianceaskList = function(act_id, unit_id, cat_id, div_id, d_id) {
    t_this = this;
    var jsondata = '{"compliance_task":[{"com_id":1,"com_task":"FORM I - Half yearly returns Submission","div_id":1,"d_id":1,"cat_id":1,"u_id":1,"act_id":1,"is_active":true},{"com_id":2,"com_task":"FORM II - Registration","div_id":1,"d_id":1,"cat_id":1,"u_id":1,"act_id":1,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._compliance_task = object.compliance_task;
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
    if (businessGroup) {
        if (isLengthMinMax(businessGroup, 0, 50, message.businessgroup_max) == false)
            return false;
        else if (isCommonName(businessGroup, message.businessgroup_str) == false)
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
    if (division) {
        if (isLengthMinMax(division, 0, 50, message.division_max) == false)
            return false;
        else if (isCommonName(division, message.division_str) == false)
            return false;
    }
    if (category) {
        if (isLengthMinMax(category, 0, 50, message.category_max) == false)
            return false;
        else if (isCommonName(category, message.category_str) == false)
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
    var jsondata = '{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"comp_id":1,"u_name":"Unit: RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","comp_task":"Notifications","frequency":"On Occurrence","due_date":"","task_status":"Not Opted","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/statutory-settings-unit-wise-report"}],"upcoming_dates":[{"user_name":"Mr. Praveen","due_date":"30-Jan-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Apr-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Oct-2017"}]},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"comp_id":2,"u_name":"Unit: RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","comp_task":"Annual Returns","frequency":"Periodical","due_date":"","task_status":"Assigned","doc_list":[{"doc_name":"Document 2","doc_url":"http://localhost:8083/statutory-settings-unit-wise-report"}],"upcoming_dates":[{"user_name":"Mr. Ramkumar","due_date":"31-Apr-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Oct-2017"}]},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"comp_id":3,"u_name":"Unit: RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","comp_task":"Notifications","frequency":"On Occurrence","due_date":"","task_status":"Not Opted","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/statutory-settings-unit-wise-report"}],"upcoming_dates":[{"user_name":"Mr. Praveen","due_date":"30-Jan-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Apr-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Oct-2017"}]},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"comp_id":4,"u_name":"Unit: RG1034 - RG Madurai Unit - 142, North Street, Madurai-625001","l_name":"Batteries Act","comp_task":"Notifications","frequency":"On Occurrence","due_date":"","task_status":"Not Opted","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/statutory-settings-unit-wise-report"}],"upcoming_dates":[{"user_name":"Mr. Praveen","due_date":"30-Jan-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Apr-2017"},{"user_name":"Mr. Ramkumar","due_date":"31-Oct-2017"}]}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;
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
    var unitname = "";
    var actname = "";
    $.each(data, function(k, v) {
        j = j + 1;
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

        var clonethree = $('#template #report-table .row-three').clone();
        $('.sno', clonethree).text(j);
        $('.compliance-task', clonethree).text(v.compliance_task);
        $('.frequency', clonethree).text(v.frequency);
        $('.due-date', clonethree).text(v.due_date);
        $('.compliance-task-status', clonethree).text(v.task_status);
        if (v.doc_list.length > 0) {
            $.each(v.doc_list, function(k1, v1) {
                $('.uploaded-document a', clonethree).text(v1.doc_name).attr("href", v1.doc_url);
            });
        } else {
            $('.uploaded-document', clonethree).text('-');
        }
        reportTableTbody.append(clonethree);

        var clonefour = $('#template #report-table .row-four').clone();
        $.each(v.upcoming_dates, function(k2, v2) {

            var clonefive = $('#template #report-table .row-five').clone();
            $('.user-name', clonefive).text(v2.user_name);
            $('.due-date', clonefive).text(v2.due_date);

            $('.tree-row', clonefour).append(clonefive);
        });
        reportTableTbody.append(clonefour);
        
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
