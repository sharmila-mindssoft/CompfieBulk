var statutoryMappingDataList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoriesList;
var complianceFrequencyList;
var temp_act = null;
var finalList;
var count = 1;
var compliance_count = 0;
var lastActName = '';
var lastOccuranceid = 0;
var totalRecord;
var filterdata = {};
var mappedStatutory;

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACOrgtype = $('#ac-industry');
var ACDomain = $('#ac-domain');
var ACStatNature = $('#ac-statutorynature');
var ACGeography = $('#ac-geography');
var ACStatutory = $('#ac-statutory');

//Input field variable declaration
var CountryVal = $('#countryval');
var Country = $('#country');
var OrgtypeVal = $('#industryval');
var Orgtype = $('#industry');
var DomainVal = $('#domainval');
var Domain = $('#domain');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var StatutoryNatureVal = $('#statutorynatureval');
var StatutoryNature = $('#statutorynature');
var GeographyVal = $('#geographyval');
var Geography = $('#geography');
var StatutoryVal = $('#statutoryval');
var Statutory = $('#statutory');

var SubmitButton = $('#submit');
var ExportButton = $('#export');

var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var ReportView = $('.grid-table-rpt');

//get statutory mapping filter details from api
function getStatutoryMappings() {
    function onSuccess(data) {
        industriesList = data.industries;
        statutoriesList = data.level_one_statutories;
        countriesList = data.countries;
        domainsList = data.domains;
        statutoryNaturesList = data.statutory_natures;
        geographiesList = data.geographies;
        complianceFrequencyList = data.compliance_frequency;
        //load compliance frequency selectbox
        for (var compliancefrequency in complianceFrequencyList) {
            var option = $('<option></option>');
            option.val(complianceFrequencyList[compliancefrequency].frequency_id);
            option.text(complianceFrequencyList[compliancefrequency].frequency);
            $('#compliance_frequency').append(option);
        }
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getStatutoryMappingsReportFilter(function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' entries ';
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
                processSubmit();
            }
        }
    });
};

//display statutory mapping details accoring to count
function loadCountwiseResult(filterList) {
    $('.tbody-compliance').empty();
    lastActName = '';
    lastOccuranceid = 0;
    var showFrom = sno + 1;
    var is_null = true;
    for (var entity in filterList) {
        is_null = false;
        sno = sno + 1;
        var actname = filterList[entity].act_name;
        var frequency_id = filterList[entity].frequency_id;
        var industry_names = filterList[entity].industry_names;
        var statutory_nature_name = filterList[entity].statutory_nature_name;
        var statutory_provision = filterList[entity].s_pro_map;
        var compliance_name = filterList[entity].c_task;
        var download_url = filterList[entity].url;
        if (actname != lastActName) {
            var tableRow = $('#act-templates .table-act-list .table-row-act-list');
            var clone = tableRow.clone();
            $('.actname', clone).text(actname);
            $('.tbody-compliance').append(clone);

            lastOccuranceid = 0;
            count++;

        }
        var occurance = '';
        var occuranceid;
        if (frequency_id != lastOccuranceid) {
            $.each(complianceFrequencyList, function(index, value) {
                if (value.frequency_id == frequency_id) {
                    occurance = value.frequency;
                    occuranceid = value.frequency_id;
                }
            });
            var tableRow2 = $('#head-templates .table-compliance-frequency-list .table-row-com-frequency');
            var clone2 = tableRow2.clone();
            $('.tbl_heading', clone2).text(occurance);
            $('.tbody-compliance').append(clone2);
        }
        var tableRow1 = $('#compliance-templates .table-compliances-list .table-row');
        var clone1 = tableRow1.clone();
        $('.tbody-compliance').append(clone1);
        $('.tbl_sno', clone1).text(sno);
        $('.tbl_industrytype', clone1).text(industry_names);
        $('.tbl_statutorynature', clone1).text(statutory_nature_name);
        $('.tbl_statutoryprovision', clone1).text(statutory_provision.substring(statutory_provision.indexOf(">>") + 2));
        if (download_url == null) {
            $('.tbl_compliancetask', clone1).html(compliance_name);
        } else {
            $('.tbl_compliancetask', clone1).html('<a href= "' + download_url + '" target="_blank" download>' + compliance_name + '</a>');
        }
        var statutorydate = filterList[entity].summary;
        $('.tbl_description', clone1).text(filterList[entity].description);
        $('.tbl_penalconsequences', clone1).text(filterList[entity].p_consequences);
        $('.tbl_occurance', clone1).text(statutorydate);
        var applicableLocation = '';
        for (var i = 0; i < filterList[entity].geo_maps.length; i++) {
            applicableLocation = applicableLocation + filterList[entity].geo_maps[i] + '<br>';
        }
        $('.tbl_applicablelocation', clone1).html(applicableLocation);
        $('.tbody-compliance').append(clone1);
        compliance_count = compliance_count + 1;
        lastActName = actname;
        lastOccuranceid = frequency_id;
    }

    if (is_null == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, sno, totalRecord);
    }
    hideLoader();
}

// get statutory mapping report data from api
function processSubmit() {
    var country = $('#country').val();
    var domain = $('#domain').val();
    var industry = null;
    var statutorynature = null;
    var geography = null;
    var act = null;
    var c_frequency = null;
    if ($('#industry').val() != '')
        industry = $('#industry').val();
    if ($('#statutorynature').val() != '')
        statutorynature = $('#statutorynature').val();
    if ($('#geography').val() != '')
        geography = $('#geography').val();
    if ($('#statutory').val() != '')
        act = $('#statutory').val();
    if ($('#compliance_frequency').val() != '')
        c_frequency = $('#compliance_frequency').val();
    if (country.length == 0) {
        CountryVal.focus();
        displayMessage(message.country_required);
    } else if (domain.length == 0) {
        DomainVal.focus();
        displayMessage(message.domain_required);
    } else {
        displayLoader();
        _page_limit = parseInt(ItemsPerPage.val());

        if (on_current_page == 1) {
            sno = 0
        } else {
            sno = (on_current_page - 1) * _page_limit;
        }

        filterdata = {};
        filterdata.c_id = parseInt(country);
        filterdata.d_id = parseInt(domain);
        filterdata.a_i_id = parseInt(industry);
        filterdata.a_s_n_id = parseInt(statutorynature);
        filterdata.a_g_id = parseInt(geography);
        filterdata.statutory_id_optional = parseInt(act);
        filterdata.frequency_id = parseInt(c_frequency);
        filterdata.r_count = parseInt(sno);
        filterdata.page_count = parseInt(_page_limit);

        function onSuccess(data) {
            $('.details').show();
            $('#compliance_animation')
                .removeClass().addClass('bounceInLeft animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
                    $(this).removeClass();
                });
            sno = sno;
            statutoryMappingDataList = data.statutory_mappings;
            totalRecord = data.total_count;
            hideLoader();

            if (totalRecord == 0) {
                $('.tbody-compliance').empty();
                var tableRow4 = $('#nocompliance-templates .table-nocompliances-list .table-row');
                var clone4 = tableRow4.clone();
                $('.tbl_norecords', clone4).text('No Records Found');
                $('.tbody-compliance').append(clone4);
                PaginationView.hide();
                ReportView.show();
                hideLoader();
            } else {
                hideLoader();
                if (sno == 0) {
                    createPageView(totalRecord);
                }
                PaginationView.show();
                ReportView.show();
                loadCountwiseResult(statutoryMappingDataList);
            }

        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }
        mirror.getStatutoryMappingsReportData(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
        temp_act = act;
    }
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();

    var current_id = id_element[0].id;
    if (current_id == 'country') {
        DomainVal.val('');
        Domain.val('');
        OrgtypeVal.val('');
        Orgtype.val('');
        StatutoryNatureVal.val('');
        StatutoryNature.val('');
        GeographyVal.val('');
        Geography.val('');
        StatutoryVal.val('');
        Statutory.val('');
    } else if (current_id == 'domain') {
        OrgtypeVal.val('');
        Orgtype.val('');
        StatutoryNatureVal.val('');
        StatutoryNature.val('');
        GeographyVal.val('');
        Geography.val('');
        StatutoryVal.val('');
        Statutory.val('');
    } else if (current_id == 'industry') {
        StatutoryNatureVal.val('');
        StatutoryNature.val('');
        GeographyVal.val('');
        Geography.val('');
        StatutoryVal.val('');
        Statutory.val('');
    } else if (current_id == 'statutorynature') {
        GeographyVal.val('');
        Geography.val('');
        StatutoryVal.val('');
        Statutory.val('');
    } else if (current_id == 'geography') {
        StatutoryVal.val('');
        Statutory.val('');
    }
}

function pageControls() {

    //Autocomplete Script Starts
    //retrive country autocomplete value
    //load country list in autocomplete text box
    CountryVal.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACCountry, Country, text_val,
            countriesList, "country_name", "country_id",
            function(val) {
                onAutoCompleteSuccess(CountryVal, Country, val);
            });
    });

    //load domain list in autocomplete textbox
    DomainVal.keyup(function(e) {
        var condition_fields = [];
        var condition_values = [];
        if (Country.val() != '') {
            condition_fields.push("country_ids");
            condition_values.push(Country.val());

            var text_val = $(this).val();
            commonAutoComplete(
                e, ACDomain, Domain, text_val,
                domainsList, "domain_name", "domain_id",
                function(val) {
                    onAutoCompleteSuccess(DomainVal, Domain, val);
                }, condition_fields, condition_values);

        }

    });

    ItemsPerPage.on('change', function(e) {
        perPage = parseInt($(this).val());
        sno = 0;
        on_current_page = 1;
        createPageView(totalRecord);
        processSubmit();
    });

    SubmitButton.click(function() {
        $('#mapping_animation')
            .removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
            });

        on_current_page = 1;
        $('.country').text("Country: " + CountryVal.val());
        $('.domain').text("Domain: " + DomainVal.val());
        processSubmit();
    });

    //load industry list in autocomplete textbox
    OrgtypeVal.keyup(function(e) {
        var condition_fields = [];
        var condition_values = [];
        if (Country.val() != '' && Domain.val() != '') {
            condition_fields.push("country_id");
            condition_values.push(Country.val());
            condition_fields.push("domain_id");
            condition_values.push(Domain.val());
        }
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACOrgtype, Orgtype, text_val,
            industriesList, "industry_name", "industry_id",
            function(val) {
                onAutoCompleteSuccess(OrgtypeVal, Orgtype, val);
            }, condition_fields, condition_values);
    });

    //load statutorynature list in autocomplete textbox
    StatutoryNatureVal.keyup(function(e) {
        var textval = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if (Country.val() != '') {
            condition_fields.push("country_id");
            condition_values.push(Country.val());
        }
        commonAutoComplete(
            e, ACStatNature, StatutoryNature, textval,
            statutoryNaturesList, "statutory_nature_name", "statutory_nature_id",
            function(val) {
                onAutoCompleteSuccess(StatutoryNatureVal, StatutoryNature, val);
            }, condition_fields, condition_values);
    });

    //load geography list in autocomplete textbox
    GeographyVal.keyup(function(e) {
        var textval = $(this).val();
        if (Country.val() != '') {
            commonAutoComplete(
                e, ACGeography, Geography, textval,
                geographiesList[$('#country').val()], "geography_name", "geography_id",
                function(val) {
                    onAutoCompleteSuccess(GeographyVal, Geography, val);
                });
        }
    });

    //load statutory list in autocomplete textbox
    StatutoryVal.keyup(function(e) {
        var textval = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if (Country.val() != '' && Domain.val() != '') {
            condition_fields.push("country_id");
            condition_values.push(Country.val());
            condition_fields.push("domain_id");
            condition_values.push(Domain.val());

            commonAutoComplete(
                e, ACStatutory, Statutory, textval,
                //statutoriesList[$('#country').val()][$('#domain').val()], "statutory_name", "statutory_id", function (val) {
                statutoriesList, "level_1_statutory_name", "level_1_statutory_id",
                function(val) {
                    onAutoCompleteSuccess(StatutoryVal, Statutory, val);
                }, condition_fields, condition_values);
        }
    });
    //Autocomplete Script ends

}

//initialization
$(function() {
    displayLoader();
    $('.grid-table-rpt').hide();
    pageControls();
    loadItemsPerPage();
    getStatutoryMappings();
    $('#countryval').focus();
});
