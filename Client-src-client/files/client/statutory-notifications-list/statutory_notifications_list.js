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

var act = $("#act");
var actId = $("#act-id");
var acAct = $("#ac-act");

var fromDate = $("#from_date");
var toDate = $("#to_date");

var showButton = $("#show-button");
var exportButton = $("#export-button");

var reportView = $("#report-view");
var reportTableTbody = $("#report-table-tbody");
var template = $("#template");
var reportTable = $("#report-table");
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
        var condition_fields = ["is_active","le_id"];
        var condition_values = [true, LegalEntityId.val()];
        commonAutoComplete(e, acDomain, domainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(REPORT, val);
        }, condition_fields, condition_values);
    });

    act.keyup(function(e) {
        var text_val = act.val().trim();
        var actList = REPORT._acts;
        var condition_fields = ["domain_id"];
        var condition_values = [domainId.val()];

        if (actList.length == 0)
            displayMessage(message.act_required);
        commonAutoComplete(e, acAct, actId, text_val, actList, "statutory_mapping", "compliance_id", function(val) {
            onActAutoCompleteSuccess(REPORT, val);
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
    clearElement([LegalEntityName, LegalEntityId, domain, domainId, act, actId]);
}

onLegalEntityAutoCompleteSuccess = function(REPORT, val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    clearElement([domain, domainId, act, actId]);
    REPORT.fetchDomainList(countryId.val(), val[0]);
}

onDomainAutoCompleteSuccess = function(REPORT, val) {
    domain.val(val[1]);
    domainId.val(val[0]);
    domain.focus();
    clearElement([act, actId]);
}

onActAutoCompleteSuccess = function(REPORT, val) {
    act.val(val[1]);
    actId.val(val[0]);
    act.focus();
}

StatutoryNotificationsList = function() {
    this._countries = [];
    this._entities = [];
    this._domains = [];
    this._acts = [];
    this._report_data = [];
    this._on_current_page = 1;
    this._sno = 0;
    this._total_record = 0;
    this._csv = false;
    this._StatutoryNotifications = [];
}

StatutoryNotificationsList.prototype.loadSearch = function() {
    reportView.hide();
    country.val('');
    countryId.val('');
    LegalEntityName.val('');
    LegalEntityId.val('');
    domain.val('');
    domainId.val('');
    act.val('');
    actId.val('');
    fromDate.val('');
    toDate.val('');
    this.fetchSearchList();
};

StatutoryNotificationsList.prototype.fetchSearchList = function() {
    t_this = this;
    t_this._countries = client_mirror.getUserCountry();
    t_this._entities = client_mirror.getSelectedLegalEntity();
};

StatutoryNotificationsList.prototype.loadCountryDetails = function(){
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

StatutoryNotificationsList.prototype.fetchDomainList = function(c_id, le_id) {
    t_this = this;
    displayLoader();
    client_mirror.getStatutoryNotificationsListReportFilters(parseInt(c_id), parseInt(le_id), function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._domains = response.domains;
            t_this._acts = response.act_legal_entity;
            hideLoader();
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

StatutoryNotificationsList.prototype.validate = function() {
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
    if (act) {
        if (isLengthMinMax(act, 0, 500, message.act_max) == false)
            return false;
        else if (isCommonName(act, message.act_str) == false)
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

StatutoryNotificationsList.prototype.fetchReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    d_id = domainId.val();
    le_id = LegalEntityId.val();
    stat_map = act.val();
    if (stat_map == "")
        stat_map = null;
    var f_date = null;
    var t_date = null;
    if (fromDate.val() != "")
        f_date = fromDate.val();
    if (toDate.val() != "")
        t_date = toDate.val();
    var check_count = false;
    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        this._sno = 0;
        check_count = true;
    } else {
        this._sno = (this._on_current_page - 1) *  _page_limit;
        check_count = false;
    }
    displayLoader();
    client_mirror.getStatutoryNotificationsListReportData(
        parseInt(c_id), parseInt(le_id), parseInt(d_id), stat_map, f_date, t_date, csv, this._sno, _page_limit,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            t_this._StatutoryNotifications = response.stat_notf_list_report;
            if (check_count == true)
                t_this._total_record = response.total_count;
            if (response.stat_notf_list_report.length == 0) {
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

StatutoryNotificationsList.prototype.showReportValues = function() {
    t_this = this;
    var data = t_this._StatutoryNotifications;
    $('.le-header').text(LegalEntityName.val());
    $('.ctry-header').text(country.val());
    $('.dom-header').text(domain.val());
    var j = 1;
    reportTableTbody.find('tr').remove();
    var is_null = true;
    showFrom = t_this._sno + 1;
    $.each(data, function(k, v) {
        console.log(data.length)
        is_null = false;

        var clonethree = $('#template #report-table .row-three').clone();
        t_this._sno += 1;
        $('.sno', clonethree).text(t_this._sno);
        $('.act-name', clonethree).text(v.statutory_mapping);
        $('.compliance-task', clonethree).text(v.compliance_task);
        var comp_task = '<span class="fa fa-info-circle text-primary c-pointer" data-toggle="tooltip" title="' + v.compliance_description + '"></span>&nbsp';
        $('.compliance-task', clonethree).parent().prepend(comp_task);
        $('[data-toggle="tooltip"]').tooltip();
        //$('.compliance-task', clonethree).html('<i class="fa fa-info-circle text-primary c-pointer" data-toggle="tooltip" title="' + v.compliance_description + '"></i>' + v.compliance_task);
        $('.due-date', clonethree).text(v.created_on);
        $('.notifications-content', clonethree).text(v.notification_text);
        reportTableTbody.append(clonethree);
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
        showPagePan(showFrom, t_this._sno, t_this._total_record);
    }
};

StatutoryNotificationsList.prototype.exportReportValues = function() {
    t_this = this;
    c_id = countryId.val();
    d_id = domainId.val();
    le_id = LegalEntityId.val();
    stat_map = act.val();
    if (stat_map == "")
        stat_map = null;

    f_date = fromDate.val();
    t_date = toDate.val();

    _page_limit = parseInt(ItemsPerPage.val());
    if (this._on_current_page == 1) {
        _sno = 0
    }
    else {
        _sno = (this._on_current_page - 1) *  _page_limit;
    }
    displayLoader();
    client_mirror.getStatutoryNotificationsListReportData(
        parseInt(c_id), parseInt(le_id), parseInt(d_id), stat_map, f_date, t_date, csv, sno, _page_limit,
        function(error, response) {
        console.log(error, response)
        if (error == null) {
            hideLoader();
            if(csv){
                document_url = response.link;
                window.open(document_url, '_blank');
            }
        } else {
            t_this.possibleFailures(error);
            hideLoader();
        }
    });
};

StatutoryNotificationsList.prototype.possibleFailures = function(error) {
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

REPORT = new StatutoryNotificationsList();

$(document).ready(function() {
    PageControls();
    loadItemsPerPage();
    REPORT.loadSearch();
    REPORT.loadCountryDetails();
});
