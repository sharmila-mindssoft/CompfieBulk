//country countryId businessGroup businessGroupId legalEntity legalEntityId division divisionId category categoryId domain domainId
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

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var clientLogo = $("#client-logo");
var legalEntityName = $("#legal-entity-name");
var countryName = $("#country-name");

var reportTableTbody = $("#report-table-tbody");
var domainName = $("#domain-name");
var reportTableTbodyNew = $("#report-table-tbody-new");
var template = $("#template");
var reportTable = $("#report-table");
var REPORT = null;

StatusReportConsolidated = function() {
    this._countries = [];
    this._business_group = [];
    this._entities = [];
    this._divisions = [];
    this._categorys = [];
    this._domains = [];
}

StatusReportConsolidated.prototype.fetchSearchList = function() {
    t_this = this;
    var jsondata = '{"countries":[{"c_id":1,"c_name":"india","is_active":true},{"c_id":1,"c_name":"srilanka","is_active":true}],"business_group":[{"b_g_id":1,"b_g_name":"RG Business Group","c_id":1,"is_active":true},{"b_g_id":2,"b_g_name":"ABC Business Group","c_id":1,"is_active":true}],"entities":[{"le_id":1,"le_name":"RG Legal Entity","c_id":1,"b_g_id":1,"is_active":true},{"le_id":2,"le_name":"ABC Legal Entity","c_id":1,"b_g_id":null,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._countries = object.countries;
    t_this._business_group = object.business_group;
    t_this._entities = object.entities;
    t_this._divisions = object.divisions;
    t_this._categorys = object.categorys;
    t_this._domains = object.domains;

    t_this.renderCountriesList(t_this._countries);
    t_this.renderBusinessGroupList(t_this._business_group);
    t_this.renderLegalEntityList(t_this._entities);
};

function PageControls() {

    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._countries;
        if (countryList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            onCountryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    businessGroup.keyup(function(e) {
        var text_val = businessGroup.val().trim();
        var businessGroupList = REPORT._business_group;
        if (businessGroupList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active", "c_id"];
        var condition_values = [true, countryId.val()];
        commonAutoComplete(e, acBusinessGroup, businessGroupId, text_val, businessGroupList, "b_g_name", "b_g_id", function(val) {
            onBusinessGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntity.keyup(function(e) {
        var text_val = legalEntity.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active", "c_id", "b_g_id"];
        var condition_values = [true, countryId.val(), businessGroupId.val()];
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    division.keyup(function(e) {
        var text_val = division.val().trim();
        var divisionList = REPORT._divisions;
        if (divisionList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, 1];
        commonAutoComplete(e, acDivision, divisionId, text_val, divisionList, "div_name", "div_id", function(val) {
            onDivisionAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    category.keyup(function(e) {
        var text_val = category.val().trim();
        var categoryList = REPORT._categorys;
        if (categoryList.length == 0)
            displayMessage(message.category_required);
        var condition_fields = ["is_active", "le_id", "div_id"];
        var condition_values = [true, 1, divisionId.val()];
        commonAutoComplete(e, acCategory, categoryId, text_val, categoryList, "c_name", "c_id", function(val) {
            onCategoryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });
    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = REPORT._domains;
        var condition_fields = ["is_active", "le_id", "div_id", "c_id"];
        var condition_values = [true, 1, divisionId.val(), categoryId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
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
            REPORT.fetchReportValues();
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
    clearElement([businessGroup, businessGroupId, legalEntity, legalEntityId, division, divisionId, category, categoryId, domain, domainId]);
}

onBusinessGroupAutoCompleteSuccess = function(REPORT, val) {
    businessGroup.val(val[1]);
    businessGroupId.val(val[0]);
    businessGroup.focus();
    clearElement([legalEntity, legalEntityId, division, divisionId, category, categoryId, domain, domainId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    legalEntity.val(val[1]);
    legalEntityId.val(val[0]);
    legalEntity.focus();
    clearElement([division, divisionId, category, categoryId, domain, domainId]);
    REPORT.fetchDivisionCategoryDomainList(val[0]);
}

onDivisionAutoCompleteSuccess = function(REPORT, val) {
    division.val(val[1]);
    divisionId.val(val[0]);
    division.focus();
    clearElement([category, categoryId, domain, domainId]);
}

onCategoryAutoCompleteSuccess = function(REPORT, val) {
    category.val(val[1]);
    categoryId.val(val[0]);
    category.focus();
    clearElement([domain, domainId]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
}

StatusReportConsolidated.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, businessGroup, businessGroupId, legalEntity, legalEntityId, division, divisionId, category, categoryId, domain, domainId]);
    this.fetchSearchList();
};

StatusReportConsolidated.prototype.fetchDivisionCategoryDomainList = function(le_id) {
    t_this = this;
    if(le_id != "") {
        var jsondata = '{"divisions":[{"div_id":1,"div_name":"RG Divisions One","le_id":1,"is_active":true},{"div_id":2,"div_name":"RG Divisions Two","le_id":1,"is_active":true}],"categorys":[{"c_id":1,"c_name":"RG Category One","le_id":1,"div_id":1,"is_active":true},{"c_id":2,"c_name":"Rg Category Two","le_id":1,"div_id":null,"is_active":true}],"domains":[{"d_id":1,"d_name":"Labour Law","le_id":1,"div_id":null,"c_id":1,"is_active":true},{"d_id":2,"d_name":"Finance Law","le_id":1,"div_id":1,"c_id":null,"is_active":true},{"d_id":3,"d_name":"Economic Law","le_id":1,"div_id":1,"c_id":1,"is_active":true},{"d_id":3,"d_name":"Industrial Law","le_id":1,"div_id":null,"c_id":null,"is_active":true}]}';
        var object = jQuery.parseJSON(jsondata);
        t_this._divisions = object.divisions;
        t_this._categorys = object.categorys;
        t_this._domains = object.domains;
    } else {
        displayMessage(message.legalentity_required);
    }
};
//country businessGroup legalEntity division category domain
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
    if (domain) {
        if (isLengthMinMax(domain, 0, 50, message.domain_max) == false)
            return false;
        else if (isCommonName(domain, message.domain_str) == false)
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
    var jsondata = '{"data_lists":[{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai division - 142, North Street, Madurai-625001","l_name":"Test Act","compliance_task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1004 - Suresh","activity_status":"Approved","activity_date":"20-Aug-2016","doc_list":[],"completion_date":"18-Aug-2016","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":1,"u_name":"RG1034 - RG Madurai division - 142, North Street, Madurai-625001","l_name":"Test Act","compliance_task":"FORM I - Half yearly returns Submission","frequency":"Periodical","due_date":"24-Aug-2016","task_status":"Complied","user_name":"EMP1002 - Rajkumar","activity_status":"Submitted","activity_date":"18-Aug-2016","doc_list":[{"doc_name":"Document 1","doc_url":"http://localhost:8083/status-report-consolidated"}],"completion_date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1035 - RG Chennai division - 23, K.K.Nagar, Chennai-600025","l_name":"PF Act","compliance_task":"FORM VIII - Notice of Opening","frequency":"One Time","due_date":"20-Aug-2016","task_status":"Inprogress","user_name":"EMP1004 - Suresh","activity_status":"Pending","activity_date":"","doc_list":[],"completion_date":"","com_id":1,"f_id":1},{"le_id":1,"c_id":1,"d_id":1,"u_id":2,"u_name":"RG1035 - RG Chennai division - 23, K.K.Nagar, Chennai-600025","l_name":"PF Act","compliance_task":"FORM VIII - Notice of Opening","frequency":"One Time","due_date":"20-Aug-2016","task_status":"Inprogress","user_name":"EMP1002 - Rajkumar","activity_status":"Submitted","activity_date":"19-Aug-2016","doc_list":[{"doc_name":"Document 2","doc_url":"http://localhost:8083/status-report-consolidated"}],"completion_date":"","com_id":1,"f_id":1}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._report_data = object.data_lists;
};

StatusReportConsolidated.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    clientLogo.attr("src", "/files/client/common/images/yourlogo.png");
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var divisionname = "";
    var actname = "";
    var category = "";
    $.each(data, function(k, v) {
        if (divisionname != v.u_name) {
            var cloneone = $('#template #report-table .row-one').clone();
            $('.division-name', cloneone).text(v.u_name);
            reportTableTbody.append(cloneone);
            divisionname = v.u_name;
        }

        if (actname != v.l_name) {
            var clonetwo = $('#template #report-table .row-two').clone();
            $('.act-name', clonetwo).text(v.l_name);
            reportTableTbody.append(clonetwo);
            actname = v.l_name;
        }

        if (category != v.compliance_task) {
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
            category = v.compliance_task;
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
            category = v.compliance_task;
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
