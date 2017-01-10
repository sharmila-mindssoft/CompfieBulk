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
    this._report_data = [];
}

StatusReportConsolidated.prototype.fetchSearchList = function() {
    t_this = this;
    var jsondata = '{"countries":[{"c_id":1,"c_name":"india","is_active":true},{"c_id":2,"c_name":"srilanka","is_active":true}],"business_group":[{"b_g_id":1,"b_g_name":"RG Business Group","c_id":1,"is_active":true},{"b_g_id":2,"b_g_name":"ABC Business Group","c_id":1,"is_active":true}],"entities":[{"le_id":1,"le_name":"RG Legal Entity","c_id":1,"b_g_id":1,"is_active":true},{"le_id":2,"le_name":"ABC Legal Entity","c_id":1,"b_g_id":null,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);
    t_this._countries = object.countries;
    t_this._business_group = object.business_group;
    t_this._entities = object.entities;
    t_this._divisions = object.divisions;
    t_this._categorys = object.categorys;
    t_this._domains = object.domains;
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
    var jsondata = '{"data_lists":[{"c_id":1,"b_g_id":1,"le_id":1,"div_id":1,"cat_id":1,"dom_id":1,"domain_name":"Labour Law","domain_lists":[{"unit_name":"UN001 - Unit One","inprogress":4,"complied":3,"delayed_complied":2,"not_complied":1,"un_assigned":4,"not_opted":2,"total":16},{"unit_name":"UN002 - Unit Two","inprogress":6,"complied":4,"delayed_complied":0,"not_complied":1,"un_assigned":4,"not_opted":2,"total":17}],"assigned":50,"un_assigned":20,"not_opted":5,"total":85},{"c_id":1,"b_g_id":1,"le_id":1,"div_id":1,"cat_id":1,"dom_id":2,"domain_name":"Finance Law","domain_lists":[{"unit_name":"UN003 - Unit Three","inprogress":5,"complied":4,"delayed_complied":0,"not_complied":0,"un_assigned":4,"not_opted":2,"total":15}],"assigned":43,"un_assigned":15,"not_opted":30,"total":88},{"c_id":1,"b_g_id":1,"le_id":1,"div_id":1,"cat_id":1,"dom_id":3,"domain_name":"Employee Law","domain_lists":[{"unit_name":"UN003 - Unit Four","inprogress":5,"complied":4,"delayed_complied":0,"not_complied":0,"un_assigned":4,"not_opted":2,"total":15},{"unit_name":"UN005 - Unit Five","inprogress":5,"complied":4,"delayed_complied":0,"not_complied":0,"un_assigned":4,"not_opted":2,"total":15}],"assigned":35,"un_assigned":20,"not_opted":15,"total":70}]}';
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
    var assigned_count = 0;
    var un_assigned_count = 0;
    var not_opted_count = 0;
    var row_total_count = 0;
    $.each(data, function(k, v) {
        //sno domain-name assigned un-assigned not-opted row-total
        var cloneone = $('#template #report-table .report-row').clone();
        $('.sno', cloneone).text(j);
        $('.domain-name', cloneone).text(v.domain_name);
        $('.domain-name', cloneone).on('click', function() {
            t_this.showDomainDetails(v.dom_id);
        });
        $('.assigned', cloneone).text(v.assigned);
        $('.un-assigned', cloneone).text(v.un_assigned);
        $('.not-opted', cloneone).text(v.not_opted);
        $('.row-total', cloneone).text(v.total);
        reportTableTbody.append(cloneone);
        j = j + 1;
        assigned_count = assigned_count + v.assigned;
        un_assigned_count = un_assigned_count + v.un_assigned;
        not_opted_count = not_opted_count + v.not_opted;
        row_total_count = row_total_count + v.total;

        var inprogress_new_count = 0;
        var complied_new_count = 0;
        var delayed_new_count = 0;
        var not_complied_new_count = 0;
        var un_assigned_new_count = 0;
        var not_opted_new_count = 0;
        var row_total_new_count = 0;
        var i = 0
        $.each(v.domain_lists, function(k1, v1) {
            var clonetwo = $('#template #report-table .report-new-row').clone();
            clonetwo.addClass("domain-"+v.dom_id);
            $('.unit-name', clonetwo).text(v1.unit_name);
            $('.inprogress', clonetwo).text(v1.inprogress);
            $('.complied', clonetwo).text(v1.complied);
            $('.delayed-complied', clonetwo).text(v1.delayed_complied);
            $('.not-complied', clonetwo).text(v1.not_complied);
            $('.un-assigned', clonetwo).text(v1.un_assigned);
            $('.not-opted', clonetwo).text(v1.not_opted);
            $('.row-total', clonetwo).text(v1.total);
            reportTableTbodyNew.append(clonetwo);
            inprogress_new_count = inprogress_new_count + v1.inprogress;
            complied_new_count = complied_new_count + v1.complied;
            delayed_new_count = delayed_new_count + v1.delayed_complied;
            not_complied_new_count = not_complied_new_count + v1.not_complied;
            un_assigned_new_count = un_assigned_new_count + v1.un_assigned;
            not_opted_new_count = not_opted_new_count + v1.not_opted;
            row_total_new_count = row_total_new_count + v1.total;
            i = i + 1;
        });
        if(i > 1) {
            var clonethree = $('#template #report-table .report-new-total-row').clone();
            clonethree.addClass("domain-"+v.dom_id);
            $('.total-inprogress', clonethree).text(inprogress_new_count);
            $('.total-complied', clonethree).text(complied_new_count);
            $('.total-delayed-complied', clonethree).text(delayed_new_count);
            $('.total-not-complied', clonethree).text(not_complied_new_count);
            $('.total-un-assigned', clonethree).text(un_assigned_new_count);
            $('.total-not-opted', clonethree).text(not_opted_new_count);
            $('.total-count-new', clonethree).text(row_total_new_count);
            reportTableTbodyNew.append(clonethree);
        }
    });
    if(j > 2) {
        var clonefour = $('#template #report-table .report-total-row').clone();
        $('.assigned-total', clonefour).text(assigned_count);
        $('.un-assigned-total', clonefour).text(un_assigned_count);
        $('.not-opted-total', clonefour).text(not_opted_count);
        $('.total-count', clonefour).text(row_total_count);
        reportTableTbody.append(clonefour);
    }
};

StatusReportConsolidated.prototype.showDomainDetails = function(dom_id) {
    $('.domain-table-view').show();
    $('.unit-details').hide();
    $('.domain-'+dom_id).show();
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
