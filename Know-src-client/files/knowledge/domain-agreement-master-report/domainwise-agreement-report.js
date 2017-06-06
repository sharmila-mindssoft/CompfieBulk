//List items variable declaration
var CountryList;
var DomainList;
var GroupList;
var BusinessGroupList;
var LegalEntityList;
var ReportData;

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACGroup = $('#ac-group');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACDomain = $('#ac-domain');

//Input field variable declaration
var CountryVal = $('#countryval');
var Country = $('#country');
var GroupVal = $('#groupval');
var Group = $('#group');
var BusinessGroupVal = $('#businessgroupval');
var BusinessGroup = $('#businessgroup');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentity');
var DomainVal = $('#domainval');
var Domain = $('#domain');
var FromDate = $('#fromdate');
var ToDate = $('#todate');
var SubmitButton = $('#submit');
var ExportButton = $('#export');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;

//Other variable declaration
var LoaderIcon = $('.loading-indicator-spin');
var ReportView = $('.grid-table-rpt');
var lastGroup;
var lastBusinessGroup;


function displayLoader() {
    LoaderIcon.show();
}

function hideLoader() {
    LoaderIcon.hide();
}

function resetValues() {
    displayMessage('');
}

function initialize() {
    //resetValues();
    displayLoader();
    mirror.getClientAgreementReportFilters(function(error, data) {
        if (error == null) {
          CountryList = data.countries;
          DomainList = data.domains;
          GroupList = data.client_group_master;
          BusinessGroupList = data.business_groups;
          LegalEntityList = data.unit_legal_entity;
          hideLoader();
        }else {
            hideLoader();
            displayMessage(error);
        }
    });
}

function getValue(field_name) {
    if (field_name == "country") {
        c_id = Country.val().trim();
        if (c_id == '') {
            return null;
        }
        return parseInt(c_id);
    } else if (field_name == "group") {
        g_id = Group.val().trim();
        if (g_id == '') {
            return null;
        }
        return parseInt(g_id);
    } else if (field_name == "businessgroup") {
        bg_id = BusinessGroup.val().trim();
        if (bg_id == '') {
            return null;
        }
        return parseInt(bg_id);
    } else if (field_name == "legalentity") {
        le_id = LegalEntity.val().trim();
        if (le_id == '') {
            return null;
        }
        return parseInt(le_id);
    } else if (field_name == "domain") {
        d_id = Domain.val().trim();
        if (d_id == '') {
            return null;
        }
        return parseInt(d_id);
    } else if (field_name == "from_date") {
        f_date = FromDate.val().trim();
        if (f_date == '') {
            return null;
        }
        return f_date;
    } else if (field_name == "to_date") {
        t_date = ToDate.val().trim();
        if (t_date == '') {
            return null;
        }
        return t_date;
    }
};

function validateMandatory() {
    is_valid = true;
    if (getValue("country") == null) {
        displayMessage(message.country_required);
        is_valid = false;
    } else if (getValue("domain") == null) {
        displayMessage(message.domain_required);
        is_valid = false;
    }
    return is_valid;
};

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + totalRecord + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
};

function hidePagePan() {
    CompliacneCount.text('');
    PaginationView.hide();
}

function createPageView(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    Pagination.empty();
    Pagination.removeData('twbs-pagination');
    Pagination.unbind('page');

    Pagination.twbsPagination({
        totalPages: Math.ceil(total_records / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                processSubmit(false);
            }
        }
    });
};

$('.close').click(function() {
    $('.overlay').css('visibility', 'hidden');
    $('.overlay').css('opacity', '0');
});

function displayPopup(LE_ID, D_ID) {
    displayLoader();
    mirror.getOrganizationWiseUnitCount(LE_ID, D_ID,
        function(error, response) {
            if (error != null) {
                displayMessage(error);
                hideLoader();
            } else {
                $('.overlay').css('visibility', 'visible');
                $('.overlay').css('opacity', '1');
                $('.popup-list').find('tr').remove();
                var unit_count_list = response.organizationwise_unit_count_list;
                var header_popup = "";
                var data_popup = "";
                $.each(unit_count_list, function(key, value) {
                    $('.popup-heading').text(value.domain_name);
                    header_popup = header_popup + '<td class="header-bg1" align="center" width="200">'+value.organization_name+'</td>';
                    data_popup = data_popup + '<td align="center" width="200">'+value.domain_used_unit+' / '+value.domain_total_unit+'</td>';
                });
                $('.header_tr_popup').html(header_popup);
                $('.data_tr_popup').html(data_popup);

                Custombox.open({
                    target: '#custom-modal',
                    effect: 'contentscale',
                    complete: function() {
                        hideLoader();
                    }
                });
            }
        }
    );
}

function loadCompliances(data) {
    $('.table-client-agreement-list').empty();
    var showFrom = sno + 1;
    var is_null = true;
    var tableRow_tr = $('#templates .table-agreement-list .heading-list');
    var clonetr = tableRow_tr.clone();
    $('.table-client-agreement-list').append(clonetr);

    $.each(data, function(key, value) {
        is_null = false;
        var domain_units = value.domain_used_unit + ' / ' + value.domain_total_unit;

        if (lastGroup != value.group_name) {
            var tableRowHeading = $('#templates .table-agreement-list .group-list');
            var cloneHeading = tableRowHeading.clone();
            $('.group-name', cloneHeading).text(value.group_name);
            if (lastBusinessGroup != value.business_group_name) {
                $('.business-group-name', cloneHeading).text(value.business_group_name);
            }
            $('.group-admin-email', cloneHeading).text(value.group_admin_email);
            $('.table-client-agreement-list').append(cloneHeading);
            lastGroup = value.group_name;
        }

        /*if (lastBusinessGroup != value.business_group_name) {
          var tableRowHeading = $('#templates .table-agreement-list .business-group-list');
          var cloneHeading = tableRowHeading.clone();
          $('.business-group-name', cloneHeading).text(value.business_group_name);
          $('.table-client-agreement-list').append(cloneHeading);
          lastBusinessGroup = value.business_group_name;
        }*/

        var tableRow = $('#templates .table-agreement-list .tbody-agreement-list');
        var clone = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone).text(sno);
        $('.le', clone).html(value.legal_entity_name);
        $('.le-email', clone).html(value.legal_entity_admin_email);
        $('.le-contactno', clone).html(value.legal_entity_admin_contactno);
        $('.domain-units', clone).html(domain_units);
        $('.domain-units', clone).on('click', function() {
            displayPopup(value.legal_entity_id, value.domain_id);
        });
        $('.activation-date', clone).html(value.activation_date);
        $('.contract-from', clone).html(value.contract_from);
        $('.contract-to', clone).html(value.contract_to);
        $('.table-client-agreement-list').append(clone);
    });
    if (is_null == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, sno, totalRecord);
    }
    hideLoader();
}

function processSubmit (csv){
  if(validateMandatory()){
    displayLoader();
    //displayMessage('');
    _country = getValue("country");
    _domain = getValue("domain");
    _group = getValue("group");
    _businessgroup = getValue("businessgroup");
    _legalentity = getValue("legalentity");
    _from_date = getValue("from_date");
    _to_date = getValue("to_date");
    _page_limit = parseInt($('#items_per_page').val());
    _country_name = CountryVal.val();
    _domain_name = DomainVal.val();
    if (on_current_page == 1) {
      sno = 0
    }
    else {
      sno = (on_current_page - 1) *  _page_limit;
    }

    mirror.getDomainwiseAgreementReport(_country, _group, _businessgroup,
    _legalentity, _domain, _from_date, _to_date, csv, sno, _page_limit,
    _country_name, _domain_name,
        function(error, response) {
            if (error != null) {
                hideLoader();
                displayMessage(error);
            }
            else {
              $('.details').show();
              $('#compliance_animation')
                .removeClass().addClass('bounceInLeft animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
              });
              if (csv) {
                hideLoader();
                var download_url = response.link;
                window.open(download_url, '_blank');
              }else{
                sno  = sno;
                ReportData = response.domainwise_agreement_list;
                totalRecord = response.total_count;
                lastGroup = '';
                lastBusinessGroup = '';

                $('.disp_country').text(CountryVal.val());
                $('.disp_domain').text(DomainVal.val());

                if (totalRecord == 0) {
                  $('.table-client-agreement-list').empty();
                  var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
                  var clone4 = tableRow4.clone();
                  $('.no_records', clone4).text('No Records Found');
                  $('.table-client-agreement-list').append(clone4);
                  PaginationView.hide();
                  hideLoader();
                } else {
                    hideLoader();
                    if (sno == 0) {
                        createPageView(totalRecord);
                    }
                    PaginationView.show();
                    ReportView.show();
                    loadCompliances(ReportData);
                    }
                }
            }
        });
    }
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();

    var current_id = id_element[0].id;
    if (current_id == 'country') {
        GroupVal.val('');
        Group.val('');
        BusinessGroupVal.val('');
        BusinessGroup.val('');
        LegalEntityVal.val('');
        LegalEntity.val('');
        DomainVal.val('');
        Domain.val('');
    } else if (current_id == 'domain') {
        GroupVal.val('');
        Group.val('');
        BusinessGroupVal.val('');
        BusinessGroup.val('');
        LegalEntityVal.val('');
        LegalEntity.val('');
    } else if (current_id == 'group') {
        BusinessGroupVal.val('');
        BusinessGroup.val('');
        LegalEntityVal.val('');
        LegalEntity.val('');
    } else if (current_id == 'businessgroup') {
        LegalEntityVal.val('');
        LegalEntity.val('');
    }
}

function pageControls() {

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        sno = 0;
        on_current_page = 1;
        createPageView(totalRecord);
        processSubmit(false);
    });

    SubmitButton.click(function() {
        on_current_page = 1;
        processSubmit(false);
    });

    ExportButton.click(function() {
        processSubmit(true);
    });

    //load country list in autocomplete text box
    CountryVal.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACCountry, Country, text_val,
            CountryList, "country_name", "country_id",
            function(val) {
                onAutoCompleteSuccess(CountryVal, Country, val);
            });
    });

    //load domain list in autocomplete text box
    DomainVal.keyup(function(e) {
        var condition_fields = [];
        var condition_values = [];
        if (Country.val() != '') {
            condition_fields.push("country_ids");
            condition_values.push(Country.val());

            var text_val = $(this).val();
            commonAutoComplete(
                e, ACDomain, Domain, text_val,
                DomainList, "domain_name", "domain_id",
                function(val) {
                    onAutoCompleteSuccess(DomainVal, Domain, val);
                }, condition_fields, condition_values);
            }
    });

    //load group list in autocomplete text box
    GroupVal.keyup(function(e) {
        if (Country.val() != '' && Domain.val() != '') {
            var condition_fields = [];
            var condition_values = [];

            condition_fields.push("country_ids");
            condition_values.push(Country.val());
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACGroup, Group, text_val,
                GroupList, "group_name", "group_id",
                function(val) {
                    onAutoCompleteSuccess(GroupVal, Group, val);
                }, condition_fields, condition_values);
        }
    });

    //load businessgroup list in autocomplete text box
    BusinessGroupVal.keyup(function(e) {
        if (Country.val() != '' && Domain.val() != '') {
            var condition_fields = [];
            var condition_values = [];
            if (Group.val() != '') {
                condition_fields.push("client_id");
                condition_values.push(Group.val());
            }
            var text_val = $(this).val();
            console.log(BusinessGroupList)
            commonAutoComplete(
                e, ACBusinessGroup, BusinessGroup, text_val,
                BusinessGroupList, "business_group_name", "business_group_id",
                function(val) {
                    onAutoCompleteSuccess(BusinessGroupVal, BusinessGroup, val);
                }, condition_fields, condition_values);
        }
    });

    //load legalentity list in autocomplete text box
    LegalEntityVal.keyup(function(e) {
        if (Country.val() != '' && Domain.val() != '') {
            var condition_fields = ["country_id"];
            var condition_values = [Country.val()];
            if (Group.val() != '') {
                condition_fields.push("client_id");
                condition_values.push(Group.val());
            }
            if (BusinessGroup.val() != '') {
                condition_fields.push("business_group_id");
                condition_values.push(BusinessGroup.val());
            }
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACLegalEntity, LegalEntity, text_val,
                LegalEntityList, "legal_entity_name", "legal_entity_id",
                function(val) {
                    onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
                }, condition_fields, condition_values);
        }
    });
}

$(document).ready(function() {
    initialize();
    pageControls();
    loadItemsPerPage();
});
