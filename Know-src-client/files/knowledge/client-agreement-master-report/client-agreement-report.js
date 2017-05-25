var CountryList;
var DomainList;
var GroupList;
var BusinessGroupList;
var LegalEntityList;
var ReportData;

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;

var ACCountry = $('#ac-country');
var ACGroup = $('#ac-group');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACDomain = $('#ac-domain');

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

var LoaderIcon = $('.loading-indicator-spin');

var lastGroup = '';
var lastBusinessGroup = '';
var lastLE = '';
var acc_count = 1;

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
    ItemsPerPage.on('change', function (e) {
        perPage = parseInt($(this).val());
          sno = 0;
          on_current_page = 1;
          createPageView(totalRecord);
          //processPaging();
      });
    mirror.getClientAgreementReportFilters(function(error, data) {
        if (error == null) {
            console.log(data)
            CountryList = data.countries;
            DomainList = data.domains;
            GroupList = data.client_group_master;
            BusinessGroupList = data.business_groups;
            LegalEntityList = data.unit_legal_entity;
        } else {
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
    }
    return is_valid;
};

function displayPopup(LE_ID, D_ID) {
    mirror.getOrganizationWiseUnitCount(LE_ID, D_ID,
        function(error, response) {
            if (error != null) {
                displayMessage(error);
            } else {
                $('.popup-list').find('tr').remove();
                var unit_count_list = response.organizationwise_unit_count_list;
                $.each(unit_count_list, function(key, value) {
                    $('.table-popup-list').show();
                    var domain_units = value.domain_used_unit + ' / ' + value.domain_total_unit;
                    $('.popup-heading').text(value.domain_name);
                    var clone = $('#templates .table-popup-list .table-row').clone();
                    $('.popup_organization_name', clone).text(value.organization_name);
                    $('.popup_unit_count', clone).text(domain_units);
                    $('.popup-list').append(clone);
                });

                Custombox.open({
                    target: '#custom-modal',
                    effect: 'contentscale',
                    complete: function() {
                        isAuthenticate = false;
                    }
                });
            }
        }
    );
}

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + totalRecord + ' entries ';
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
        totalPages: Math.ceil(total_records/perPage),
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

function loadCompliances(data) {
    $('.table-client-agreement-list').empty();
    $('.table-agreement-list').show();
    var showFrom = sno + 1;
    var is_null = true;
    var tableRow_tr = $('#templates .table-agreement-list .heading-list');
    var clonetr = tableRow_tr.clone();
    $('.table-client-agreement-list').append(clonetr);
    $.each(data, function(key, value) {
        is_null = false;
        var domain_units = value.domain_used_unit + ' / ' + value.domain_total_unit;
        var license_details = value.used_licence + ' / ' + value.total_licence;
        var u_file_space = Math.round(value.used_file_space/(1024*1024*1024)).toFixed(2);
        var file_space = Math.round(value.file_space/(1024*1024*1024)).toFixed(2);
        var file_space_details = u_file_space + ' / ' + file_space;

        if (lastGroup != value.group_name) {
            var tableRowHeading = $('#templates .group-list');
            var cloneHeading = tableRowHeading.clone();
            $('.group-name', cloneHeading).text(value.group_name);
            $('.group-name', cloneHeading).text(value.group_name);
            if (lastBusinessGroup != value.business_group_name) {
                if(value.business_group_name != "" && value.business_group_name != null) {
                    $('.business-group-name', cloneHeading).text(value.business_group_name);
                    lastBusinessGroup = value.business_group_name;
                } else {
                    $('.business-group-name', cloneHeading).remove();
                }
            }
            $('.group-admin-email', cloneHeading).text(value.group_admin_email);
            $('.le-contactno', cloneHeading).text(value.legal_entity_admin_contactno);
            $('.table-client-agreement-list').append(cloneHeading);
            lastGroup = value.group_name;
        }

        if (lastLE != value.legal_entity_name) {
            var tableRow = $('#templates .agreement-row-list');
            var clone = tableRow.clone();
            sno = sno + 1;
            var status = 'Active';
            if (value.is_closed == true) {
                status = 'Closed';
            }
            $('.sno', clone).text(sno);
            $('.le', clone).html(value.legal_entity_name);
            $('.user-license', clone).html(license_details);
            $('.file-space', clone).html(file_space_details);
            $('.le-email', clone).html(value.legal_entity_admin_email);
            $('.le-contactno', clone).html(value.legal_entity_admin_contactno);
            $('.domain-count', clone).html(value.domain_count).on('click', function() { tree_open_close(value.legal_entity_id); });
            $('.contract-from', clone).html(value.contract_from);
            $('.contract-to', clone).html(value.contract_to);
            $('.status', clone).html(status);
            $('.table-client-agreement-list').append(clone);

            lastLE = value.legal_entity_name;
            acc_count++;

            var tableRowvalues_ul = $('#templates .agreement-inner-list');
            var cloneval_ul =  tableRowvalues_ul.clone().addClass('tree' + value.legal_entity_id);;
            $('.inner-domain-name', cloneval_ul).html(value.d_name);
            $('.inner-domain-units', cloneval_ul).text(domain_units);
            $('.inner-domain-units', cloneval_ul).on('click', function() {
                displayPopup(value.legal_entity_id, value.domain_id);
            });
            $('.inner-activation-date', cloneval_ul).html(value.activation_date);
            $('.table-client-agreement-list').append(cloneval_ul);
        } else {
            var tableRowvalues_ul = $('#templates .agreement-inner-list');
            var cloneval_ul = tableRowvalues_ul.clone().addClass('tree' + value.legal_entity_id);;
            $('.inner-domain-name', cloneval_ul).html(value.d_name);
            $('.inner-domain-units', cloneval_ul).text(domain_units);
            $('.inner-domain-units', cloneval_ul).on('click', function() {
                displayPopup(value.legal_entity_id, value.domain_id);
            });
            $('.inner-activation-date', cloneval_ul).html(value.activation_date);
            $('.table-client-agreement-list').append(cloneval_ul);
        }
    });

    $('#accordion').find('.tree-data').click(function() {
        $(this).next().slideToggle('fast');
        $('.accordion-content').not($(this).next()).slideUp('fast');
    });
    if (is_null == true) {
      hidePagePan();
    }
    else {
      showPagePan(showFrom, sno, totalRecord);
    }
    hideLoader();
}

function tree_open_close(id) {
    $('.tree' + id).toggle("slow");
}

function processSubmit(csv) {
    if (validateMandatory()) {
        displayLoader();
        _country = getValue("country");
        _domain = getValue("domain");
        _group = getValue("group");
        _businessgroup = getValue("businessgroup");
        _legalentity = getValue("legalentity");
        _from_date = getValue("from_date");
        _to_date = getValue("to_date");

        _page_limit = parseInt($('#items_per_page').val());
        _country_name = CountryVal.val();

        if (on_current_page == 1) {
            sno = 0
        } else {
            sno = (on_current_page - 1) * _page_limit;
        }

        mirror.getClientAgreementReport(_country, _group, _businessgroup,
            _legalentity, _domain, _from_date, _to_date, csv, (sno + 1), (sno + _page_limit),
            _country_name,
            function(error, response) {
                if (error != null) {
                    hideLoader();
                    displayMessage(error);
                } else {
                    $('.details').show();
                    $('#compliance_animation')
                        .removeClass().addClass('bounceInLeft animated')
                        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
                            $(this).removeClass();
                        });
                    if (csv) {
                        hideLoader();
                        var download_url = response.link;
                        window.open(download_url, '_blank');
                    } else {
                        $('.disp-country').text(CountryVal.val());
                        sno = sno;
                        ReportData = response.client_agreement_list;
                        totalRecord = response.total_count;
                        lastGroup = '';
                        lastBusinessGroup = '';
                        lastLE = '';
                        if (totalRecord == 0) {
                            $('.grid-table-rpt').show();
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
                            $('.grid-table-rpt').show();
                            loadCompliances(ReportData);
                        }
                    }
                }
            }
        );
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
        if (Country.val() != '') {
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
        if (Country.val() != '') {
            var condition_fields = [];
            var condition_values = [];
            if (Group.val() != '') {
                condition_fields.push("client_id");
                condition_values.push(Group.val());
            }
            var text_val = $(this).val();
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
        if (Country.val() != '') {
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
    loadItemsPerPage();

    initialize();
    pageControls();

    $('.tree-open-close').click(function() {
        $('.tree-data').toggle("slow");
    });
});
