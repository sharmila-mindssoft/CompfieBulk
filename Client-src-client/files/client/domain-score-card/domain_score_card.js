//country countryId businessGroup businessGroupId legalEntity legalEntityId division divisionId category categoryId domain domainId
var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");
var filterCountryName = $(".filter-country-name");

var businessGroup = $("#business-group");
var businessGroupId = $("#business-group-id");
var acBusinessGroup = $("#ac-business-group");
var filterBusinessGroupName = $(".filter-business-group-name");

var legalEntity = $("#legal-entity");
var legalEntityId = $("#legal-entity-id");
var acLegalEntity = $("#ac-legal-entity");
var filterLegalEntityName = $(".filter-legal-entity-name");

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
var LOGO = null;

DomainScoreCard = function() {
    this._entities = [];
    this._divisions = [];
    this._categorys = [];
    this._domains = [];
    this._report_data = [];
}

DomainScoreCard.prototype.fetchSearchList = function() {
    t_this = this;
    /*var jsondata = '{"countries":[{"c_id":1,"c_name":"india","is_active":true},{"c_id":2,"c_name":"srilanka","is_active":true}],"business_group":[{"b_g_id":1,"b_g_name":"RG Business Group","c_id":1,"is_active":true},{"b_g_id":2,"b_g_name":"ABC Business Group","c_id":1,"is_active":true}],"entities":[{"le_id":1,"le_name":"RG Legal Entity","c_id":1,"b_g_id":1,"is_active":true},{"le_id":2,"le_name":"ABC Legal Entity","c_id":1,"b_g_id":null,"is_active":true}]}';
    var object = jQuery.parseJSON(jsondata);*/
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

function PageControls() {

    country.keyup(function(e) {
        var text_val = country.val().trim();
        var countryList = REPORT._entities;
        // if (countryList.length == 0 && text_val != '')
        //     displayMessage(message.country_required);
        var condition_fields = [];
        var condition_values = [];
        commonAutoComplete(e, acCountry, countryId, text_val, countryList, "c_name", "c_id", function(val) {
            onCountryAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    businessGroup.keyup(function(e) {
        var text_val = businessGroup.val().trim();
        var businessGroupList = REPORT._entities;
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, acBusinessGroup, businessGroupId, text_val, businessGroupList, "bg_name", "bg_id", function(val) {
            onBusinessGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    legalEntity.keyup(function(e) {
        var text_val = legalEntity.val().trim();
        var legalEntityList = REPORT._entities;
        // if (legalEntityList.length == 0 && text_val != '')
        //     displayMessage(message.legalentity_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        if (businessGroupId.val() != '') { condition_fields.push("bg_id"); condition_values.push(businessGroupId.val()); }
        commonAutoComplete(e, acLegalEntity, legalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    division.keyup(function(e) {
        var text_val = division.val().trim();
        var divisionList = REPORT._divisions;
        var condition_fields = [];
        var condition_values = [];
        commonAutoComplete(e, acDivision, divisionId, text_val, divisionList, "div_name", "div_id", function(val) {
            onDivisionAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    category.keyup(function(e) {
        var text_val = category.val().trim();
        var categoryList = REPORT._categorys;
        var condition_fields = ["div_id"];
        var condition_values = [divisionId.val()];
        commonAutoComplete(e, acCategory, categoryId, text_val, categoryList, "cat_name", "cat_id", function(val) {
            onCategoryAutoCompleteSuccess(REPORT, val);
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

    showButton.click(function() {
        var csv = false;
        processSubmit(csv);
    });

    exportButton.click(function() {
        var csv = true;
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

DomainScoreCard.prototype.loadSearch = function() {
    reportView.hide();
    clearElement([country, countryId, businessGroup, businessGroupId, legalEntity, legalEntityId, division, divisionId, category, categoryId, domain, domainId]);
    this.fetchSearchList();
};

DomainScoreCard.prototype.fetchDivisionCategoryDomainList = function(le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getStatutorySettingsUnitWiseFilters(parseInt(le_id), function(error, response) {
        if (error == null) {
            t_this._domains = response.domains;
            t_this._divisions = response.div_infos;
            t_this._categorys = response.cat_infos;
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });
};
//country businessGroup legalEntity division category domain
DomainScoreCard.prototype.validate = function() {
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

DomainScoreCard.prototype.fetchReportValues = function(csv) {
    t_this = this;
    var c_id = parseInt(countryId.val());
    var bg_id = parseInt(businessGroupId.val());
    if (!bg_id) bg_id = null
    var le_id = parseInt(legalEntityId.val());
    var d_id = parseInt(domainId.val());
    if (!d_id) d_id = null
    var div_id = parseInt(divisionId.val());
    if (!div_id) div_id = null
    var cat_id = parseInt(categoryId.val());
    if (!cat_id) cat_id = null
    displayLoader();
    client_mirror.getDomainScoreCard(c_id, bg_id, le_id, d_id, div_id, cat_id, csv, function(error, response) {
        if (error == null) {
            t_this._report_data = response.domain_score_card_list;
            LOGO = response.logo_url;
            if (csv == false) {
                reportView.show();
                showAnimation(reportView);
                REPORT.showReportValues();
            } else {
                REPORT.exportReportValues();
            }
        } else {
            t_this.possibleFailures(error);
        }
        hideLoader();
    });

};

DomainScoreCard.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._report_data;
    if(LOGO != null)
        clientLogo.attr("src", LOGO);
    else
        clientLogo.remove();
    legalEntityName.html(legalEntity.val());
    countryName.html(country.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    reportTableTbodyNew.find('tr').remove();
    $('.domain-table-view').hide();
    var assigned_count = 0;
    var un_assigned_count = 0;
    var not_opted_count = 0;
    var row_total_count = 0;
    if(data.length > 0) {
        $.each(data, function(k, v) {
            var row_total = 0;
            //sno domain-name assigned un-assigned not-opted row-total
            var cloneone = $('#template #report-table .report-row').clone();
            $('.sno', cloneone).text(j);
            $('.domain-name', cloneone).text(v.domain_name);
            $('.domain-name', cloneone).on('click', function() {
                t_this.showDomainDetails(v.domain_id, v.domain_name);
            });
            $('.assigned', cloneone).text(v.assigned_count);
            $('.un-assigned', cloneone).text(v.unassigned_count);
            $('.not-opted', cloneone).text(v.not_opted_count);

            assigned_count = assigned_count + v.assigned_count;
            un_assigned_count = un_assigned_count + v.unassigned_count;
            not_opted_count = not_opted_count + v.not_opted_count;
            row_total = v.assigned_count + v.unassigned_count + v.not_opted_count;
            row_total_count = row_total_count + row_total;
            $('.row-total', cloneone).text(row_total);
            reportTableTbody.append(cloneone);
            j = j + 1;

            var inprogress_new_count = 0;
            var complied_new_count = 0;
            var delayed_new_count = 0;
            var not_complied_new_count = 0;
            var un_assigned_new_count = 0;
            var not_opted_new_count = 0;
            var row_total_new_count = 0;
            var i = 0
            $.each(v.units_wise_count, function(k1, v1) {
                var row_total_new = 0;
                var clonetwo = $('#template #report-table .report-new-row').clone();
                clonetwo.addClass("domain-" + v.domain_id);
                $('.unit-name', clonetwo).text(v1.unit);
                $('.inprogress', clonetwo).text(v1.inprogress_count);
                $('.complied', clonetwo).text(v1.complied_count);
                $('.delayed-complied', clonetwo).text(v1.delayed_count);
                $('.not-complied', clonetwo).text(v1.overdue_count);
                $('.un-assigned', clonetwo).text(v1.unassigned_count);
                $('.not-opted', clonetwo).text(v1.not_opted_count);
                inprogress_new_count = inprogress_new_count + v1.inprogress_count;
                complied_new_count = complied_new_count + v1.complied_count;
                delayed_new_count = delayed_new_count + v1.delayed_count;
                not_complied_new_count = not_complied_new_count + v1.overdue_count;
                un_assigned_new_count = un_assigned_new_count + v1.unassigned_count;
                not_opted_new_count = not_opted_new_count + v1.not_opted_count;
                row_total_new = v1.inprogress_count + v1.complied_count + v1.delayed_count + v1.overdue_count + v1.unassigned_count + v1.not_opted_count;
                row_total_new_count = row_total_new_count + row_total_new;
                $('.row-total', clonetwo).text(row_total_new);
                reportTableTbodyNew.append(clonetwo);
                i = i + 1;
            });
            if (i > 1) {
                var clonethree = $('#template #report-table .report-new-total-row').clone();
                clonethree.addClass("domain-" + v.domain_id);
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
        if (j > 2) {
            var clonefour = $('#template #report-table .report-total-row').clone();
            $('.assigned-total', clonefour).text(assigned_count);
            $('.un-assigned-total', clonefour).text(un_assigned_count);
            $('.not-opted-total', clonefour).text(not_opted_count);
            $('.total-count', clonefour).text(row_total_count);
            reportTableTbody.append(clonefour);
        }
    } else {
        reportTableTbody.html('<tr><td colspan="100%"><br><center>Record Not Found!</center><br></td></tr>');
    }
};

DomainScoreCard.prototype.showDomainDetails = function(dom_id, dom_name) {
    $('.domain-table-view').show();
    $('.unit-details').hide();
    $('#domain-name').text(dom_name);
    $('.domain-' + dom_id).show();
};

DomainScoreCard.prototype.possibleFailures = function(error) {
    if (error == 'DomainNameAlreadyExists') {
        displayMessage("Domain name exists");
    } else {
        displayMessage(error);
    }
};

DomainScoreCard.prototype.loadEntityDetails = function() {
    t_this = this;
    if(t_this._entities.length > 1) {
        country.parent().show();
        filterCountryName.hide();

        legalEntity.parent().show();
        filterLegalEntityName.hide();

        businessGroup.parent().show();
        filterBusinessGroupName.hide();
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
        
        var BG_NAME = '-';
        if(t_this._entities[0]["bg_name"] != null) 
            BG_NAME = t_this._entities[0]["bg_name"];
        
        var BG_ID = '';
        if(t_this._entities[0]["bg_id"] != null)
            BG_ID = t_this._entities[0]["bg_id"];

        filterBusinessGroupName.show();
        filterBusinessGroupName.html(BG_NAME);
        businessGroupId.val(BG_ID);
        businessGroup.parent().hide();
        businessGroup.val(BG_NAME);

        REPORT.fetchDivisionCategoryDomainList(t_this._entities[0]["le_id"]);
    }
    hideLoader();
};

REPORT = new DomainScoreCard();

$(document).ready(function() {
    displayLoader();
    PageControls();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});
