var CountryNameLabel = $(".country-name");
var CountryNameAC = $(".country-name-ac");

var country = $("#country");
var countryId = $("#country-id");
var acCountry = $("#ac-country");

var BusinessGroupNameLabel = $(".business-group-name");
var BusinessGroupNameAC = $(".business-group-name-ac");

var BusinessGroupName = $("#business_group_name");
var BusinessGroupId = $("#business_group_id");
var ACBusinessGroup = $("#ac-business-group");

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");

var domain = $("#domain");
var domainId = $("#domain-id");
var acDomain = $("#ac-domain");

var unit = $("#unit");
var unitId = $("#unit-id");
var acUnit = $("#ac-unit");

var DivisionName = $("#division");
var DivisionId = $("#division-id");
var ACDivision = $("#ac-division");

var CategoryName = $("#category");
var CategoryId = $("#category-id");
var ACCategory = $("#ac-category");

var OrgTypeName = $("#orgtype");
var OrgTypeId = $("#organization-type-id");
var ACOrgType = $("#ac-organization-type");

var UnitStatus = $("#unit-status");
var UnitList = [];

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var clientLogo = $("#client-logo");
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

    BusinessGroupName.keyup(function(e) {
        var text_val = BusinessGroupName.val().trim();
        var bgList = REPORT._entities;
        if (bgList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        commonAutoComplete(e, ACBusinessGroup, BusinessGroupId, text_val, bgList, "bg_name", "bg_id", function(val) {
            onBusinessGroupAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    LegalEntityName.keyup(function(e) {
        var text_val = LegalEntityName.val().trim();
        var legalEntityList = REPORT._entities;
        if (legalEntityList.length == 0 && text_val != '')
            displayMessage(message.domainname_required);
        var condition_fields = ["c_id"];
        var condition_values = [countryId.val()];
        if (BusinessGroupId.val() != '') {
            condition_fields.push("bg_id");
            condition_values.push(BusinessGroupId.val());
        }
        commonAutoComplete(e, ACLegalEntity, LegalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    DivisionName.keyup(function(e) {
        var text_val = DivisionName.val().trim();
        var divisionList = REPORT._divisions;
        commonAutoComplete(e, ACDivision, DivisionId, text_val, divisionList, "division_name", "division_id", function(val) {
            onDivisionAutoCompleteSuccess(REPORT, val);
        });
    });

    CategoryName.keyup(function(e) {
        var text_val = CategoryName.val().trim();
        var categoryList = REPORT._categories;
        if (DivisionId.val() != '') {
            condition_fields = ["division_id"];
            condition_values = [DivisionId.val()];
        }
        commonAutoComplete(e, ACCategory, CategoryId, text_val, categoryList, "category_name", "category_id", function(val) {
            onCategoryAutoCompleteSuccess(REPORT, val);
        });
    });

    unit.keyup(function(e) {
        var text_val = unit.val().trim();
        var unitList = [];
        condition_fields = [];
        condition_values = [];
        if (DivisionId.val() != '') {
            condition_fields = ["division_id"];
            condition_values = [DivisionId.val()];
        }
        if (CategoryId.val() != '') {
            if(condition_fields.length > 0){
                condition_fields.push("category_id");
                condition_values.push(CategoryId.val());
            }
            else
            {
                condition_fields = ["category_id"];
                condition_values = [CategoryId.val()];
            }

        }
        for(var i=0;i<REPORT._units.length;i++){
            unitList.push({
                "division_id": REPORT._units[i].division_id,
                "category_id": REPORT._units[i].category_id,
                "unit_id": REPORT._units[i].unit_id,
                "unit_name": REPORT._units[i].unit_code+" - "+REPORT._units[i].unit_name
            });
        }
        commonAutoComplete(e, acUnit, unitId, text_val, unitList, "unit_name", "unit_id", function(val) {
            onUnitAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    domain.keyup(function(e) {
        var text_val = domain.val().trim();
        var domainList = [];
        if (unitId.val() != '') {
            d_List = REPORT._units;
            d_ids = [];
            for(var i=0;i<d_List.length;i++){
                if(d_List[i].unit_id == unitId.val()){
                    d_ids = d_List[i].d_ids;
                }
            }
            d_List = REPORT._domains;
            for(var i=0;i<d_ids.length;i++){
                for(var j=0;j<d_List.length;j++){
                    if(d_ids[i] == d_List[j].domain_id){
                        domainList.push({
                            "domain_id": d_List[j].domain_id,
                            "domain_name": d_List[j].domain_name,
                        });
                    }
                }
            }
        }
        else{
            domainList = REPORT._domains;
        }
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "domain_name", "domain_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        });
    });

    OrgTypeName.keyup(function(e) {
        var text_val = OrgTypeName.val().trim();
        var orgtypeList = [];
        if (unitId.val() != '') {
            d_List = REPORT._units;
            i_ids = [];
            for(var i=0;i<d_List.length;i++){
                if(d_List[i].unit_id == unitId.val()){
                    if(domainId.val() != ""){
                        if($.inArray(parseInt(domainId.val()), d_List[i].d_ids) >= 0){
                            i_ids = d_List[i].i_ids;
                        }
                    }
                    else
                    {
                        i_ids = d_List[i].i_ids;
                    }
                }
            }
            d_List = REPORT._domains;
            for(var i=0;i<i_ids.length;i++){
                for(var j=0;j<d_List.length;j++){
                    if(i_ids[i] == d_List[j].organisation_id){
                        orgtypeList.push({
                            "organisation_id": d_List[j].organisation_id,
                            "organisation_name": d_List[j].organisation_name,
                        });
                    }
                }
            }
        }
        else{
            if(domainId.val() != ""){
                for(var i=0;i<REPORT._domains.length;i++){
                    if(domainId.val() == REPORT._domains[i].domain_id){
                        orgtypeList.push({
                            "organisation_id": REPORT._domains[i].organisation_id,
                            "organisation_name": REPORT._domains[i].organisation_name,
                        })
                    }
                }
            }
            else{
                orgtypeList = REPORT._domains;
            }
        }
        commonAutoComplete(e, ACOrgType, domainId, text_val, orgtypeList, "organisation_name", "organisation_id", function(val) {
            onOrgTypeAutoCompleteSuccess(REPORT, val);
        });
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
    clearElement([BusinessGroupName, BusinessGroupId, LegalEntityName, LegalEntityId, DivisionId, DivisionName, CategoryId, CategoryName, unit, unitId, domain, domainId, OrgTypeName, OrgTypeId]);
}

onBusinessGroupAutoCompleteSuccess = function(REPORT, val) {
    BusinessGroupName.val(val[1]);
    BusinessGroupId.val(val[0]);
    BusinessGroupName.focus();
    clearElement([LegalEntityName, LegalEntityId, DivisionId, DivisionName, CategoryId, CategoryName, unit, unitId, domain, domainId, OrgTypeName, OrgTypeId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    clearElement([DivisionId, DivisionName, CategoryId, CategoryName, unit, unitId, domain, domainId, OrgTypeName, OrgTypeId]);
    REPORT.fetchDivisionList(countryId.val(), BusinessGroupId.val(), val[0]);
}

onDivisionAutoCompleteSuccess = function(REPORT, val) {
    DivisionName.val(val[1]);
    DivisionId.val(val[0]);
    DivisionName.focus();
    clearElement([CategoryId, CategoryName, unit, unitId, domain, domainId, OrgTypeName, OrgTypeId]);
}

onCategoryAutoCompleteSuccess = function(REPORT, val) {
    CategoryName.val(val[1]);
    CategoryId.val(val[0]);
    CategoryName.focus();
    clearElement([unit, unitId, domain, domainId, OrgTypeName, OrgTypeId]);
}

onUnitAutoCompleteSuccess = function(REPORT, val) {
    unit.val(val[1]);
    unitId.val(val[0]);
    unit.focus();
    clearElement([domain, domainId, OrgTypeName, OrgTypeId]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([OrgTypeName, OrgTypeId]);
}

onOrgTypeAutoCompleteSuccess = function(REPORT, val) {
    OrgTypeName.val(val[1]);
    OrgTypeId.val(val[0]);
    OrgTypeName.focus();
}

UnitListReport = function() {
    this._countries = [];
    this._entities = [];
    this._divisions = [];
    this._categories = [];
    this._domains = [];
    this._units = [];
    this._orgtypes = [];
    this._unit_status = [];
    this._report_data = [];
    this._on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
    this._UnitList = [];
}

UnitListReport.prototype.loadSearch = function() {
    reportView.hide();
    country.val('');
    countryId.val('')
    LegalEntityId.val('');
    LegalEntityName.val('');
    BusinessGroupName.val('');
    BusinessGroupId.val('');
    DivisionName.val('');
    DivisionId.val('');
    CategoryId.val('');
    CategoryName.val('');
    domain.val('');
    domainId.val('');
    unit.val('');
    unitId.val('');
    OrgTypeId.val('');
    OrgTypeName.val('');
    UnitStatus.empty();
    this.fetchSearchList();
};

UnitListReport.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

UnitListReport.prototype.loadEntityDetails = function(){
    t_this = this;
    if(t_this._entities.length > 1){
        CountryNameAC.show();
        CountryNameLabel.hide();
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
        BusinessGroupNameLabel.hide();
        BusinessGroupNameAC.show();
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
        var BG_NAME = '-';
        if(t_this._entities[0]["bg_name"] != null){
            BG_NAME = t_this._entities[0]["bg_name"];
        }
        var BG_ID = '';
        if(t_this._entities[0]["bg_id"] != null){
            BG_ID = t_this._entities[0]["bg_id"];
        }
        BusinessGroupNameLabel.show();
        BusinessGroupNameAC.hide();
        BusinessGroupNameLabel.text(BG_NAME);
        BusinessGroupName.val(BG_NAME);
        BusinessGroupId.val(BG_ID);
        REPORT.fetchDivisionList(c_id, BG_ID, le_id);
    }
    hideLoader();
};

UnitListReport.prototype.fetchDivisionList = function(c_id, bg_id, le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getUnitListReportFilters(parseInt(c_id), parseInt(bg_id), parseInt(le_id), function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._divisions = response.divisions;
            t_this._categories = response.categories;
            t_this._domains = response.domains_organisations_list;
            t_this._units = response.units_list;
            t_this._unit_status = response.unit_status_list;
            REPORT.renderUnitStatusList(t_this._unit_status);
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};
UnitListReport.prototype.renderCountriesList = function(data) {
    t_this = this;
    country.empty();
    var countryName = [];
    $.each(data, function(i, e) {
        //countryName.push(e.c_name+",");
        countryName = e.c_name;
    });
    country.html(countryName);
};

UnitListReport.prototype.renderLegalEntityList = function(data) {
    t_this = this;
    legalEntity.empty();
    var legalEntityName = [];
    $.each(data, function(i, e) {
        //legalEntityName.push(e.le_name+",");
        legalEntityName = e.le_name;
    });
    legalEntity.html(legalEntityName);
};

UnitListReport.prototype.renderUnitStatusList = function(data) {
    t_this = this;
    UnitStatus.empty();
    var UnitList = '<option value="-1">All</option>';
    $.each(data, function(i, e) {
        UnitList = UnitList + '<option value="' + e.unit_status_id + '"> ' + e.unit_status + ' </option>';
    });
    UnitStatus.html(UnitList);
};

UnitListReport.prototype.validate = function() {
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
    if (BusinessGroupName) {
        if (isLengthMinMax(BusinessGroupName, 0, 50, message.businessgroup_max) == false)
            return false;
        else if (isCommonName(BusinessGroupName, message.businessgroup_str) == false)
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
    if (DivisionName) {
        if (isLengthMinMax(DivisionName, 0, 50, message.division_max) == false)
            return false;
        else if (isCommonName(DivisionName, message.division_str) == false)
            return false;
    }
    if (CategoryName) {
        if (isLengthMinMax(CategoryName, 0, 50, message.category_max) == false)
            return false;
        else if (isCommonName(CategoryName, message.category_str) == false)
            return false;
    }
    if (unit) {
        if (isLengthMinMax(unit, 0, 50, message.unit_max) == false)
            return false;
        else if (isCommonName(unit, message.unit_str) == false)
            return false;
    }
    if (domain) {
        if (isLengthMinMax(domain, 0, 50, message.domain_max) == false)
            return false;
        else if (isCommonName(domain, message.domain_str) == false)
            return false;
    }

    if (OrgTypeName) {
        if (isLengthMinMax(OrgTypeName, 0, 50, message.orgtype_max) == false)
            return false;
        else if (isCommonName(OrgTypeName, message.orgtype_str) == false)
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

UnitListReport.prototype.fetchReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    bg_id = BusinessGroupId.val();
    if (bg_id == "")
        bg_id = 0;
    le_id = LegalEntityId.val();
    div_id = DivisionId.val();
    if (div_id == "")
        div_id = 0;
    cg_id = CategoryId.val();
    if (cg_id == "")
        cg_id = 0;
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
    d_id = domainId.val();
    if (d_id == "")
        d_id = 0;
    org_id = OrgTypeId.val();
    if (org_id == "")
        org_id = 0;
    check_count = false;
    u_s = $('#unit-status option:selected').text().trim();

    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        this._sno = 0;
        check_count = true;
    }
    else {
        this._sno = (this._on_current_page - 1) *  _page_limit;
        check_count = false;
    }
    displayLoader();
    client_mirror.getUnitListReport(
        parseInt(c_id), parseInt(bg_id), parseInt(le_id), parseInt(div_id), parseInt(cg_id), parseInt(unit_id),
        parseInt(d_id), parseInt(org_id), u_s, csv, this._sno, _page_limit,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._UnitList = response.unit_list_report;
            if (check_count == true)
                t_this._total_record = response.total_count;
            if (response.unit_list_report.length == 0) {
                hidePageView();
                hidePagePan();
                //Export_btn.hide();
                PaginationView.hide();
                t_this.showReportValues();
            }
            else{
                if (t_this._sno == 0) {
                    createPageView(t_this._total_record);
                }
                //Export_btn.show();
                PaginationView.show();
                t_this.showReportValues();
            }
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

UnitListReport.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._UnitList;
    $('.le-header').text(LegalEntityName.val());
    $('.ctry-header').text(country.val());
    $('.dom-header').text(domain.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var divisionname = "";
    var is_null = true;
    showFrom = t_this._sno + 1;
    divi_names = [];
    for (var i=0;i<data.length;i++){
        var occur = -1;
        for(var j=0;j<divi_names.length;j++){
            if(data[i].division_name == divi_names[j]){
                occur = 1;
                break;
            }
        }
        if(occur < 0){
            divi_names.push(data[i].division_name);
        }
    }
    console.log(divi_names)
    for(var i=0;i<divi_names.length;i++){
        u_count = 1;
        $.each(data, function(k, v) {
            console.log(data.length)
            is_null = false;
            $('.client-logo').attr("src", v.logo_url);
            if (divi_names[i] == v.division_name) {
                if(u_count == 1){
                    if(divi_names[i] == "---"){
                        var cloneone = $('#template #report-table .row-two').clone();
                        $('.division-name', cloneone).text("Division : -Nil-");
                        reportTableTbody.append(cloneone);
                        u_count = u_count + 1;
                    }else{
                        var cloneone = $('#template #report-table .row-two').clone();
                        $('.division-name', cloneone).text("Division : "+v.division_name);
                        reportTableTbody.append(cloneone);
                        u_count = u_count + 1;
                    }
                }

                var clonethree = $('#template #report-table .row-three').clone();
                t_this._sno += 1;
                $('.sno', clonethree).text(t_this._sno);
                $('.unit-code', clonethree).text(v.unit_code);
                $('.unit-name', clonethree).text(v.unit_name);
                $('.domain-org-type', clonethree).text(v.d_i_names);
                $('.location', clonethree).text(v.geography_name);
                var addr = v.address + " , "+v.postal_code;
                $('.address', clonethree).text(addr);
                $('.status', clonethree).text(v.unit_status);
                console.log(v.unit_status)
                $('.unit-date', clonethree).text(v.closed_on);
                reportTableTbody.append(clonethree);
                j = j + 1;
            }
        });
    }

    if (is_null == true) {
        //a_page.hidePagePan();
        reportTableTbody.empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        reportTableTbody.append(clone4);
    }
    else {
        showPagePan(showFrom, t_this._sno, t_this._total_record);
    }
};

UnitListReport.prototype.exportReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    bg_id = BusinessGroupId.val();
    le_id = LegalEntityId.val();
    div_id = DivisionId.val();
    if (div_id == "")
        div_id = 0;
    cg_id = CategoryId.val();
    if (cg_id == "")
        cg_id = 0;
    unit_id = unitId.val();
    if (unit_id == "")
        unit_id = 0;
    d_id = domainId.val();
    if (d_id == "")
        d_id = 0;
    org_id = OrgTypeId.val();
    if (org_id == "")
        org_id = 0;

    u_s = $('#unit-status option:selected').text().trim();

    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        this._sno = 0
    }
    else {
        this._sno = (this._on_current_page - 1) *  _page_limit;
    }
    displayLoader();
    client_mirror.getUnitListReport(
        parseInt(c_id), parseInt(bg_id), parseInt(le_id), parseInt(div_id), parseInt(cg_id), parseInt(unit_id),
        parseInt(d_id), parseInt(org_id), u_s, csv, sno, _page_limit,
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

UnitListReport.prototype.possibleFailures = function(error) {
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

REPORT = new UnitListReport();

$(document).ready(function() {
    displayLoader();
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadEntityDetails();
});
