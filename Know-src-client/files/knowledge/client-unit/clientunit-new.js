//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterDomain = $('#search-domain-name');
var FilterOrgn = $('#search-organization-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');
/**
 * Created by Minds on 24/09/2016.
 */

var groupList;
var countryList;
var domainList;
var businessGroupList;
var legalEntitiesList;
var divisionList;
var countryFulList;
var countc = 1;
var industryList;
var unitList;
var geographyList;
var geographyLevelList;
var unitcodecount = 1001;
var countryByCount = 1;
var lastClassval = 1;
var unitcodeautogenerateids = null;
var get2CharsofGroup = null;
var max = {};
var auto_generate_initial_value = null;
var isUpdate = false;
var checkunitscount = null;
var usercountrycount = null;
var clientdomainList = null;
var division_cnt = 0;
var unit_cnt = 0;
var unit_values = '';
var units_count = [];
var prev_org_id = 0;
var check_org = false;

var clientUnitAdd = $('#clientunit-add');
var clientUnitView = $('#clientunit-view');

//drop down in main search
var groupSelect_option_0 = $('#group-select  option:gt(0)');
var busgrpSelect_option_0 = $('#businessgroup-select  option:gt(0)');
var entitySelect_option_0 = $('#entity-select  option:gt(0)');
var groupSelect_option_no = $('#group-select option:not(:selected)');
var busgrpSelect_option_no = $('#businessgroup-select option:not(:selected)');
var entitySelect_option_no = $('#entity-select option:not(:selected)');

//main search filters
var clientSelect = $('#group-select');
var bgrpSelect = $('#businessgroup-select');
var leSelect = $('#entity-select');
var ctrySelect_name = $('#country-name');
var ctrySelect_id = $('#country-id');
var unitErrMsg = $('.unit-error-msg');

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterGroup = $('#search-group-name');
var FilterBGroup = $('#search-bgroup-name');
var FilterLE = $('#search-le-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

var countryUnitList = $('.add-country-unit-list');

function initialize() {
    function onSuccess(data) {
        clientUnitAdd.hide();
        clientUnitView.show();
        isUpdate = false;
        countryByCount = 1;
        countc = 0;
        usercountrycount = 0;
        groupSelect_option_0.empty();
        busgrpSelect_option_0.empty();
        entitySelect_option_0.empty();
        groupList = data.group_company_list;
        businessGroupList = data.business_group_list;
        legalEntitiesList = data.unit_legal_entity;
        divisionList = data.divisions;
        countryFulList = data.countries_units;
        geographyLevelList = data.unit_geography_level_list;
        geographyList = data.unit_geographies_list;
        industryList = data.domains_organization_list;
        domainList = data.domains_organization_list;
        unitList = data.unit_list;
        //clientdomainList = data.client_domains;
        resetallfilter();
        loadClientsList(unitList);
    }

    function onFailure(error) {
        custom_alert(error);
    }
    mirror.getClients('view', function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

//Load Get Client List -----------------------------------------------------------------------------------------
function loadClientsList(data) {
    $('.tbody-clientunit-list').find('tr').remove();
    var sno = 0;
    var getAllArrayValues = [];

    $.each(data, function(key, value) {
        var unitId = value.unit_id;
        var unitVal = 0;
        var clientId = value.client_id;
        var bgroupId = value.business_group_id;
        var lentitiesId = value.legal_entity_id;
        var divisionId = value.division_id;
        var countryId = value.country_id;
        var tableRow = $('#templates .table-clientunit-list .table-row');
        var clone = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone).text(sno);
        $('.group-name', clone).text(getGroupName(clientId));
        $('.business-group-name', clone).text(getBusinessGroupName(bgroupId));
        $('.country-name', clone).text(getCountryName(countryId));
        $('.legal-entity-name', clone).text(getLegalEntityName(lentitiesId));

        //edit icon
        $('.edit').attr('title', 'Click Here to Edit');
        $('.edit', clone).addClass('fa-pencil text-primary');
        $('.edit', clone).on('click', function() {
            clientunit_edit(clientId, bgroupId, lentitiesId, countryId);
        });

        if (value.is_active == false) {
            $('.status-text', clone).text("In active");
        } else {
            $('.status-text', clone).text("Active");
        }

        $('.tbody-clientunit-list').append(clone);
    });
}

function getGroupName(groupId) {
    var groupName;
    $.each(groupList, function(key, value) {
        if (value.client_id == groupId) {
            groupName = value.group_name;
        }
    });
    return groupName;
}

function getBusinessGroupName(businessGroupId) {
    var businessgroupName;
    $.each(businessGroupList, function(key, value) {
        if (value.business_group_id == businessGroupId) {
            businessgroupName = value.business_group_name;
        }
    });
    return businessgroupName;
}

function getLegalEntityName(legalentityId) {
    var legalEntityName;
    $.each(legalEntitiesList, function(key, value) {
        if (value.legal_entity_id == legalentityId) {
            legalEntityName = value.legal_entity_name;
        }
    });
    return legalEntityName;
}

function getCountryName(countryId) {
    var countryName;
    $.each(countryFulList, function(key, value) {
        if (value.country_id == countryId) {
            countryName = value.country_name;
        }
    });
    return countryName;
}
//Edit client Unit  -----------------------------------------------------------------------------------------------
function clientunit_edit(clientunitId, businessgroupId, legalentityId, countryId) {
    isUpdate = true;
    units_count = [];
    division_cnt = 0;
    $('#clientunit-view').hide();
    $('#clientunit-add').show();
    $('#group-select').hide();
    $('.labelgroup').show();
    $('#businessgroup-select').hide();
    $('.labelbusinessgroup').show();
    $('#entity-select').hide();
    $('.labelentity').show();
    $('#ac-country').hide();
    $('#country-name').hide();
    $('.labelcountry').show();

    //$('#division-text').show();
    $('#division-select').hide();
    $('#division-new').hide();
    $('#division-existing').hide();
    $('.no-of-units').val('');

    var x = document.getElementsByTagName('input');
    for (i = 0; i <= x.length - 1; i++) {
        if (x.item(i).type != 'submit') {
            x.item(i).value = '';
        }
    }
    $('#group-select').find('option').not(':first').remove();
    $('#businessgroup-select').find('option').not(':first').remove();
    $('#entity-select').find('option').not(':first').remove();
    checkunitscount = null;
    clearMessage();

    function onSuccess(data) {
        clientdomainList = data.domains_organization_list;
        unitList = data.unit_list;
        loadFormListUpdate(clientunitId, businessgroupId, legalentityId, countryId);
    }

    function onFailure(error) {
        displayMessage(error);
    }
    mirror.getClientsEdit(clientunitId, businessgroupId, legalentityId, countryId, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}
//Update load form cal------------------------------------------------------------------------------------------
function loadFormListUpdate(clientunitId, businessgroupId, legalEntityId, countryId) {
    $('#businessgroup-update-id').val('');
    $('#legalentity-update-id').val('');
    $('#client-unit-id').val(clientunitId);
    $('.add-country-unit-list').empty();
    //group
    loadClientGroups(groupList);
    $('.labelgroup').text(getGroupName(clientunitId));

    //businessgroup
    if (businessgroupId != '') {
        loadBusinessGroups(clientunitId);
        $('#businessgroup-update-id').val(businessgroupId);
        $(".labelbusinessgroup").text(getBusinessGroupName(businessgroupId));
        //$('#businessgroup-select option[value = '+businessgroupId+']').attr('selected','selected');
    }

    if (businessgroupId == '') {
        $(".labelbusinessgroup").text(" --- ")
    }

    //legalentity
    loadLegalEntity(clientunitId, businessgroupId);
    $('#legalentity-update-id').val(legalEntityId);
    $(".labelentity").text(getLegalEntityName(legalEntityId));
    $(".labelentity").attr("data-id", legalEntityId);
    //$('#entity-text').val(getLegalEntityName(legalEntityId));
    //$('#entity-select option[value = '+legalEntityId+']').attr('selected','selected');

    //country
    if (countryId != '')
        LoadCountry(countryId);

    //load doamin, orgainsiation in array
    load_domain_org();

    //Load Units under division/category
    unitcount = 1;
    unit_start_cnt = 1;
    div_catg_cnt = 1;
    div_start_cnt = 2;
    divisionId = 0;
    categoryName = '';

    $.each(unitList, function(unitkey, unitval) {
        unitval = unitList[unitkey];
        category_name = unitval.category_name;
        if (unitval.client_id == clientunitId && unitval.country_id == countryId && unitval.legal_entity_id == legalEntityId) {
            var tab_len = $('.add-country-unit-list').find('table').length;
            if (tab_len == 0 || tab_len < 0) {
                division_cnt = 0;
                addcountryrownew();
                loadUnitValues(unitval);
            } else {
                var rowcnt = 0;
                var division_name;
                var returnRow = 0;
                if (unitval.division_id != '') {
                    division_name = getDivisionName(unitval.division_id);
                }
                $('.labelcategory-' + parseInt(i + 1) + '-1').show();

                //find the existing row
                if (division_name != "" && category_name != "") {
                    returnRow = findDivisionRow(division_name, category_name);
                } else if (division_name != "" && category_name == "null") {
                    returnRow = findDivisionRow(division_name, "--");
                } else if (division_name == "null" && category_name != "") {
                    returnRow = findDivisionRow("--", category_name);
                } else if (division_name == "null" && category_name == "null") {
                    returnRow = findDivisionRow("--", "--");
                }
                //display in corresponding row
                if (returnRow > 0) {
                    addNewUnitRow_edit('tbody-unit-' + parseInt(returnRow));
                    loadUnitValues_exists(unitval, returnRow);
                } else {
                    addcountryrownew();
                    loadUnitValues(unitval);
                }

            }
        }
    });
}

function findDivisionRow(divisionName, categoryName) {
    var returnRow = 0;
    if (divisionName == null) {
        divisionName = "--"
    }
    if (categoryName == null) {
        categoryName = "--"
    }
    var tab_len = $('.add-country-unit-list').find('table').length;
    for (var i = 1; i <= (tab_len - 1); i++) {
        if ($('.labeldivision-' + parseInt(i) + '-1').text() == divisionName && $('.labelcategory-' + parseInt(i) + '-1').text() == categoryName) {
            returnRow = i;
            break;
        }
    }
    return returnRow;
}

// log edited domain id and organisation id
function load_domain_org() {
    units_count = [];
    domain_ids = [];
    org_ids = [];
    for (var i = 0; i < unitList.length; i++) {
        d_ids = unitList[i].domain_ids;
        if (d_ids.length > 0) {
            for (var j = 0; j < d_ids.length; j++) {
                domain_ids.push(d_ids[j])
            }
        }
        i_ids = unitList[i].i_ids;
        if (i_ids.length > 0) {
            for (var j = 0; j < i_ids.length; j++) {
                org_ids.push(i_ids[j])
            }
        }
    }


    for (var i = 0; i < domain_ids.length; i++) {

        if (i == 0)
        //push 0 index of domain id and org id
            units_count.push(domain_ids[i] + '-' + org_ids[i] + '-' + 1);


        match_count = false;
        for (var j = i + 1; j <= domain_ids.length; ++j) {
            if (domain_ids[j] == domain_ids[i] && org_ids[j] == org_ids[i]) {

                // var unit_count_val = units_count[i].split("-")[2];
                // units_count[i] = domain_ids[i]+'-'+org_ids[i]+'-'+ (parseInt(unit_count_val)+1);
                match_count = true;
            }
        }
        if (match_count == false) {
            units_count[i] = domain_ids[i] + '-' + org_ids[i] + '-' + 1;
        }

    }
}

function getDivisionName(divisionId) {
    var division_name;
    for (var i = 0; i < divisionList.length; i++) {
        if (divisionList[i].division_id == divisionId) {
            division_name = divisionList[i].division_name;
            break;
        }
    }
    return division_name;
}

function loadUnitValues(unitval) {
    var unit_second_cnt = $('.unitcnt-' + division_cnt + '-' + 1).val();
    var firstlist = unitval
    var cid = firstlist.country_id;
    $('.division-id-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.labeldivision-' + division_cnt + '-' + unit_second_cnt).show();
    if (firstlist.division_id > 0) {
        $('.divisionid-' + division_cnt + '-' + unit_second_cnt).val(firstlist.division_id);
        loadDivision('division-id-' + division_cnt + '-' + unit_second_cnt);
        $('.division-id-' + division_cnt + '-' + unit_second_cnt + ' option[value=' + firstlist.division_id + ']').attr('selected', 'selected');
        division_name = getDivisionName(firstlist.division_id);
        $('.labeldivision-' + division_cnt + '-' + unit_second_cnt).text(division_name);
    } else if (firstlist.division_id == 0) {
        $('.labeldivision-' + division_cnt + '-' + unit_second_cnt).show();
        $('.labeldivision-' + division_cnt + '-' + unit_second_cnt).text("--");
    }

    if (firstlist.category_name != null) {
        $('.categoryid-' + division_cnt + '-' + unit_second_cnt).val(firstlist.category_id);
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).val(firstlist.category_name);
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).hide();
        $('.labelcategory-' + division_cnt + '-' + unit_second_cnt).show();
        $('.labelcategory-' + division_cnt + '-' + unit_second_cnt).text(firstlist.category_name);
    } else {
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).val();
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).hide();
        $('.labelcategory-' + division_cnt + '-' + unit_second_cnt).show();
        $('.labelcategory-' + division_cnt + '-' + unit_second_cnt).text("--");
    }

    var gid = firstlist.geography_id;
    var unitlts = loadupdateunitlocation(gid);
    loadglevels('glevel-' + division_cnt + '-' + unit_second_cnt);
    $('.glevel-' + division_cnt + '-' + unit_second_cnt + ' option[value=' + unitlts.level_id + ']').attr('selected', 'selected');
    $('.glevel-' + division_cnt + '-' + unit_second_cnt).hide();
    for (var i = 0; i < geographyLevelList.length; i++) {
        if (geographyLevelList[i].l_id == unitlts.level_id) {
            $('.labelgeolevels-' + division_cnt + '-' + unit_second_cnt).show();
            $('.labelgeolevels-' + division_cnt + '-' + unit_second_cnt).text(geographyLevelList[i].l_name);
        }
    }
    $('.tbody-unit-' + division_cnt + ' i').hide();

    $('.unitlocation-' + division_cnt + '-' + unit_second_cnt).val(unitlts.gname);
    $('.unitlocation-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.unitlocation-ids-' + division_cnt + '-' + unit_second_cnt).val(gid);
    $('.unitlocation-ids-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.full-location-list-' + division_cnt + '-' + unit_second_cnt).text(unitlts.mapping);
    $('.full-location-list-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.labelunitlocation-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labelunitlocation-' + division_cnt + '-' + unit_second_cnt).text(unitlts.gname);

    $('.unit-id-' + division_cnt + '-' + unit_second_cnt).val(firstlist.unit_id);

    $('.unit-code-' + division_cnt + '-' + unit_second_cnt).val(firstlist.unit_code);
    $('.unit-code-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.labelunitcode-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labelunitcode-' + division_cnt + '-' + unit_second_cnt).text(firstlist.unit_code);

    $('.unit-name-' + division_cnt + '-' + unit_second_cnt).val(firstlist.unit_name);
    $('.unit-name-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.labelunitname-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labelunitname-' + division_cnt + '-' + unit_second_cnt).text(firstlist.unit_name);

    $('.unit-address-' + division_cnt + '-' + unit_second_cnt).val(firstlist.address);
    $('.unit-address-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.labelunitaddress-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labelunitaddress-' + division_cnt + '-' + unit_second_cnt).text(firstlist.address);

    $('.postal-code-' + division_cnt + '-' + unit_second_cnt).val(firstlist.postal_code);
    $('.postal-code-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.labelpostcode-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labelpostcode-' + division_cnt + '-' + unit_second_cnt).text(firstlist.postal_code);

    var domainsListArray = firstlist.domain_ids;
    $('.domainselected-' + division_cnt + '-' + unit_second_cnt).hide();
    domain_names = getDomainsName(domainsListArray);
    $('.labeldomain-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labeldomain-' + division_cnt + '-' + unit_second_cnt).text(domain_names);

    var orgtypeArray = firstlist.i_ids;
    $('.orgtypeselected-' + division_cnt + '-' + unit_second_cnt).val(orgtypeArray.length + ' Selected');
    
    $('.orgtypeselected-' + division_cnt + '-' + unit_second_cnt).hide();
    orgn_names = getOrganizationName(orgtypeArray);
    $('.labelorganization-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labelorganization-' + division_cnt + '-' + unit_second_cnt).text(orgn_names);

    if (firstlist.is_active == true) {
        $('.activedclass-' + division_cnt + '-' + unit_second_cnt).text('Active');
        if ($('.active_cnt-' + division_cnt + '-' + unit_second_cnt).text() == "") {
            act_cnt = 1;
            $('.active_cnt-' + division_cnt + '-' + unit_second_cnt).text("Active Unit(s): " + act_cnt);
        } else {
            act_cnt = $('.active_cnt-' + division_cnt + '-' + unit_second_cnt).text().split(":")[1].trim();
            $('.active_cnt-' + division_cnt + '-' + unit_second_cnt).text("Active Unit(s): " + parseInt(act_cnt) + 1);
        }
    } else {
        var classname = 'imgactivedclass-' + division_cnt + '-' + unit_second_cnt;
    }

    if (firstlist.is_approved == "0") {
        $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('Pending');
    } else if (firstlist.is_approved == "1") {
        $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('Approved');
    } else if (firstlist.is_approved == "2") {
        $('.rejected-icon-' + division_cnt + '-' + unit_second_cnt).show();
        $('.rejected-icon-' + division_cnt + '-' + unit_second_cnt).attr('title', firstlist.remarks);
        $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('Rejected');
        rowIndx = unit_second_cnt - 1;
        $('.tbody-unit-' + division_cnt + ' tr').eq(rowIndx).css("color", "rgb(255,0,0)");
    }

    $('.active_cnt-' + division_cnt + '-' + unit_second_cnt).show();

    loadDomains();
    industrytype('industry-' + division_cnt + '-' + unit_second_cnt, orgtypeArray);
    return false;

    $('.domainselected').parent('span').hide();
    $('.orgtypeselected').parent('span').hide();
}

function loadUnitValues_exists(unitval, start_cnt) {
    var unit_second_cnt = $('.unitcnt-' + start_cnt + '-' + 1).val();
    var firstlist = unitval

    var cid = firstlist.country_id;
    //load division
    $('.division-id-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.labeldivision-' + start_cnt + '-' + unit_second_cnt).show();
    if (firstlist.division_id > 0) {
        $('.divisionid-' + division_cnt + '-' + unit_second_cnt).val(firstlist.division_id);
        loadDivision('division-id-' + division_cnt + '-' + unit_second_cnt);
        $('.division-id-' + division_cnt + '-' + unit_second_cnt + ' option[value=' + firstlist.division_id + ']').attr('selected', 'selected');
        division_name = getDivisionName(firstlist.division_id);
        $('.labeldivision-' + division_cnt + '-' + unit_second_cnt).text(division_name);
    } else if (firstlist.division_id == 0) {
        $('.labeldivision-' + division_cnt + '-' + unit_second_cnt).show();
        $('.labeldivision-' + division_cnt + '-' + unit_second_cnt).text("--");
    }
    if (firstlist.category_name != null) {
        $('.categoryid-' + division_cnt + '-' + unit_second_cnt).val(firstlist.category_id);
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).val(firstlist.category_name);
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).hide();
        $('.labelcategory-' + division_cnt + '-' + unit_second_cnt).show();
        $('.labelcategory-' + division_cnt + '-' + unit_second_cnt).text(firstlist.category_name);
    } else {
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).val();
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).hide();
        $('.labelcategory-' + division_cnt + '-' + unit_second_cnt).show();
        $('.labelcategory-' + division_cnt + '-' + unit_second_cnt).text("--");
    }

    var gid = firstlist.geography_id;
    var unitlts = loadupdateunitlocation(gid);
    loadglevels('glevel-' + start_cnt + '-' + unit_second_cnt);


    //loadIndustry('industry-'+countryByCount+'-'+1);
    $('.glevel-' + start_cnt + '-' + unit_second_cnt + ' option[value=' + unitlts.level_id + ']').
    attr('selected', 'selected');

    $('.glevel-' + start_cnt + '-' + unit_second_cnt).hide();
    for (var i = 0; i < geographyLevelList.length; i++) {
        if (geographyLevelList[i].l_id == unitlts.level_id) {
            $('.labelgeolevels-' + start_cnt + '-' + unit_second_cnt).show();
            $('.labelgeolevels-' + start_cnt + '-' + unit_second_cnt).text(geographyLevelList[i].l_name);
        }
    }
    $('.tbody-unit-' + start_cnt + ' i').hide();

    $('.unitlocation-' + start_cnt + '-' + unit_second_cnt).val(unitlts.gname);
    $('.unitlocation-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.unitlocation-ids-' + start_cnt + '-' + unit_second_cnt).val(gid);
    $('.unitlocation-ids-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.full-location-list-' + start_cnt + '-' + unit_second_cnt).text(unitlts.mapping);
    $('.full-location-list-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.labelunitlocation-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labelunitlocation-' + start_cnt + '-' + unit_second_cnt).text(unitlts.gname);

    $('.unit-id-' + start_cnt + '-' + unit_second_cnt).val(firstlist.unit_id);

    $('.unit-code-' + start_cnt + '-' + unit_second_cnt).val(firstlist.unit_code);
    $('.unit-code-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.labelunitcode-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labelunitcode-' + start_cnt + '-' + unit_second_cnt).text(firstlist.unit_code);

    $('.unit-name-' + start_cnt + '-' + unit_second_cnt).val(firstlist.unit_name);
    $('.unit-name-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.labelunitname-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labelunitname-' + start_cnt + '-' + unit_second_cnt).text(firstlist.unit_name);

    $('.unit-address-' + start_cnt + '-' + unit_second_cnt).val(firstlist.address);
    $('.unit-address-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.labelunitaddress-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labelunitaddress-' + start_cnt + '-' + unit_second_cnt).text(firstlist.address);

    $('.postal-code-' + start_cnt + '-' + unit_second_cnt).val(firstlist.postal_code);
    $('.postal-code-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.labelpostcode-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labelpostcode-' + start_cnt + '-' + unit_second_cnt).text(firstlist.postal_code);

    var domainsListArray = firstlist.domain_ids;

    //$('.domain-' + division_cnt + '-' + unit_second_cnt).val(domainsListArray);
    $('.domainselected-' + start_cnt + '-' + unit_second_cnt).val(domainsListArray.length + ' Selected');
    //loadDomains('domain-' + division_cnt + '-' + unit_second_cnt);
    $('.domainselected-' + start_cnt + '-' + unit_second_cnt).hide();
    //$('.domain-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.ul-domain-list-' + start_cnt + '-' + unit_second_cnt).hide();
    domain_names = getDomainsName(domainsListArray);
    $('.labeldomain-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labeldomain-' + start_cnt + '-' + unit_second_cnt).text(domain_names);

    var orgtypeArray = firstlist.i_ids;
    //$('.orgtype-' + division_cnt + '-' + unit_second_cnt).val(orgtypeArray);
    $('.orgtypeselected-' + start_cnt + '-' + unit_second_cnt).val(orgtypeArray.length + ' Selected');
    
    $('.orgtypeselected-' + start_cnt + '-' + unit_second_cnt).hide();
    //$('.orgtype-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.ul-orgtype-list-' + start_cnt + '-' + unit_second_cnt).hide();
    orgn_names = getOrganizationName(orgtypeArray);
    $('.labelorganization-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labelorganization-' + start_cnt + '-' + unit_second_cnt).text(orgn_names);



    if (firstlist.is_active == true) {
        $('.activedclass-' + start_cnt + '-' + unit_second_cnt).text('Active');
        if ($('.active_cnt-' + start_cnt + '-' + 1).text() == "") {
            act_cnt = 1;
            $('.active_cnt-' + start_cnt + '-' + 1).text("Active Unit(s): " + act_cnt);
        } else {
            act_cnt = parseInt($('.active_cnt-' + start_cnt + '-' + 1).text().split(":")[1].trim()) + 1;
            $('.active_cnt-' + start_cnt + '-' + 1).text("Active Unit(s): " + act_cnt);
        }
    } else {
        var classname = 'imgactivedclass-' + start_cnt + '-' + unit_second_cnt;
    }

    if (firstlist.is_approved == "0") {
        $('.approveclass-' + start_cnt + '-' + unit_second_cnt).text('Pending');
    } else if (firstlist.is_approved == "1") {
        $('.approveclass-' + start_cnt + '-' + unit_second_cnt).text('Approved');
    } else if (firstlist.is_approved == "2") {
        $('.rejected-icon-' + start_cnt + '-' + unit_second_cnt).show();
        $('.rejected-icon-' + start_cnt + '-' + unit_second_cnt).attr('title', firstlist.remarks);
        $('.approveclass-' + start_cnt + '-' + unit_second_cnt).text('Rejected');
        rowIndx = unit_second_cnt - 1;
        $('.tbody-unit-' + start_cnt + ' tr').eq(rowIndx).css("color", "rgb(255,0,0)");
    }
    $('.edit-icon-' + start_cnt + '-' + unit_second_cnt).attr('title', 'Edit');
    $('.edit-icon-' + start_cnt + '-' + unit_second_cnt).on('click', function() {
        unitrow_edit(this.className, orgtypeArray);
    });
    $('.delete-icon-' + start_cnt + '-' + unit_second_cnt).attr('title', 'Close');
    $('.delete-icon-' + start_cnt + '-' + unit_second_cnt).on('click', function() {
        unitrow_close(this.className, orgtypeArray);
    });
    $('.edit-icon-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.delete-icon-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.active_cnt-' + start_cnt + '-' + unit_second_cnt).show();
    if ($("#client-unit-id").val() != "") {
        $('.edit-icon').show();
        // $('.edit-icon').on('click', function() {
        //     unitrow_edit(this.className, orgtypeArray);
        // });
        $('.edit-icon-' + start_cnt + '-' + unit_second_cnt).show();
    }
    if ($("#client-unit-id").val() == "") {
        $('.edit-icon').hide();
    }

}
//Add Button  -------------------------------------------------------------------------------------------------
$('#btn-clientunit-add').click(function() {
    isUpdate = false;
    units_count = [];
    division_cnt = 0;
    clientUnitAdd.show();
    clientUnitView.hide();
    clientSelect.show();
    bgrpSelect.show();
    leSelect.show();
    //$('#ac-country').show();
    $('#country-name').show();
    $('#division-select').show();
    $('#division-new').show();
    $('#division-existing').show();
    $('.division-id').show();
    $('.labeldivision').hide();

    groupSelect_option_no.attr('disabled', false);
    busgrpSelect_option_no.attr('disabled', false);
    entitySelect_option_no.attr('disabled', false);
    $('.labelgroup').hide();
    $('.labelbusinessgroup').hide();
    $('.labelentity').hide();
    $('.labelcountry').hide();

    unitErrMsg.val('');
    checkunitscount = null;
    countryByCount = 1;
    countc = 0;
    usercountrycount = 0;
    clearMessage();
    var x = document.getElementsByTagName('input');
    for (i = 0; i <= x.length - 1; i++) {
        if (x.item(i).type != 'submit') {
            x.item(i).value = '';
        }
    }
    var y = document.getElementsByTagName('select');
    for (i = 0; i <= y.length - 1; i++) {
        y.item(i).value = '';
    }
    clientSelect.find('option').not(':first').remove();
    bgrpSelect.find('option').not(':first').remove();
    leSelect.find('option').not(':first').remove();

    countryUnitList.empty();
    loadClientGroups(groupList);
});
//Cancel Button  ----------------------------------------------------------------------------------------------
$('#btn-clientunit-cancel').click(function() {

    clientUnitAdd.hide();
    clientUnitView.show();

    /*var msgstatus = message.cancel_operation;

    confirm_alert(msgstatus, function(isConfirm){
      if(isConfirm){
        clientUnitAdd.hide();
        clientUnitView.show();
      }
    });*/

    // $('.warning-confirm').dialog({
    //   title: 'Cancel',
    //   buttons: {
    //     Ok: function () {
    //       $(this).dialog('close');
    //       clientUnitAdd.hide();
    //       clientUnitView.show();
    //       isUpdate = false;
    //       countryByCount = 1;
    //       countc = 0;
    //       usercountrycount = 0;
    //       groupSelect_option_0.empty();
    //       busgrpSelect_option_0.empty();
    //       entitySelect_option_0.empty();
    //     },
    //     Cancel: function () {
    //       $(this).dialog('close');
    //     }
    //   },
    //   open: function () {
    //     $('.warning-message').html(msgstatus);
    //   }
    // });`
});
//Load All Groups  ---------------------------------------------------------------------------------------------
function loadClientGroups(groupsList) {
    $('#group-select').focus();
    var clients = groupsList;

    for (var i = 0; i < clients.length; i++) {
        var obj = $(".client-drop-down option");
        var clone = obj.clone();
        clone.attr("value", clients[i].client_id);
        clone.text(clients[i].group_name);
        clientSelect.append(clone);
    }
}

//Load Business Groups  ---------------------------------------------------------------------------------------------
function loadBusinessGroups() {
    var groupId = clientSelect.val();
    busgrpSelect_option_0.remove();
    for (var i in businessGroupList) {
        if (businessGroupList[i].client_id == groupId) {
            var bgroupId = businessGroupList[i].business_group_id;
            var bgroupName = businessGroupList[i].business_group_name;
            var obj = $(".bgrp-drop-down option");
            var clone = obj.clone();
            clone.attr("value", bgroupId);
            clone.text(bgroupName);
            $('#businessgroup-select').append(clone);
        }
    }
}

//load country list in autocomplete text box
$('#country-name').keyup(function(e) {
    var textval = $(this).val();
    loadauto_countrytext(e, textval, function(val) {
        onCountrySuccess(val);
    });
});

//store the selected country name and id
function onCountrySuccess(val) {
    ctrySelect_name.val(val[1]);
    ctrySelect_id.val(val[0]);
    ctrySelect_name.focus();
}

function onArrowKey_Client(e, ac_item, multipleselect, callback) {
    if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 13) {
        chosen = '';
    }
    if (e.keyCode == 40) {
        if (chosen === '') {
            chosen = 0;
        } else if (chosen + 1 < $('.' + ac_item + ' li').length) {
            chosen++;
        }
        $('.' + ac_item + ' li').removeClass('auto-selected');
        $('.' + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 38) {
        if (chosen === '') {
            chosen = 0;
        } else if (chosen > 0) {
            chosen--;
        }
        $('.' + ac_item + ' li').removeClass('auto-selected');
        $('.' + ac_item + ' li:eq(' + chosen + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 13) {
        var ac_id = $('.' + ac_item + ' li:eq(' + chosen + ')').attr('id');
        var ac_name = $('.' + ac_item + ' li:eq(' + chosen + ')').text();
        if (multipleselect == 'country') {
            $('#country_name').val(ac_name);
            $('#country_id').val(ac_id);
            $('.glevel-' + ac_id).empty();
            //$('.autocompleteview-' + ccount).css('display', 'none');
            activate_text_arrow(ac_id, ac_name, callback);
        } else {
            $('.unitlocation' + ccount).val(ac_name);
            $('.unitlocation-ids' + ccount).val(ac_id);
            for (var geography in geographyList) {
                if (geographyList[geography].geography_id == parseInt(ac_id)) {
                    mappingname = geographyList[geography].mapping;
                }
            }
            $('.full-location-list' + ccount).html('<br>' + mappingname);
            $('.auto-complete-unit-location').css('display', 'none');
        }

        return false;
    }
}

function loadauto_countrytext(e, textval, callback) {
    $('#country-id').val('');
    $('#ac-country').show();
    $('#ac-country ul').empty();
    var groupId;
    var bgrpId = bgrpSelect.val();
    if ($('#client-unit-id').val() != '') {
        groupId = $('#client-unit-id').val();
    } else if ($('#client-unit-id').val() == '') {
        groupId = clientSelect.val();
    }
    if (groupId == '' || groupId == 0) {
        displayMessage(message.group_required);
    } else {
        var countries = countryFulList;
        if (textval.length > 0) {
            for (var i in countries) {
                if (~countries[i].country_name.toLowerCase().indexOf(textval.toLowerCase())) {
                    if (bgrpId > 0) {
                        if (countries[i].client_id == groupId && countries[i].business_group_id == bgrpId) {
                            var obj = $(".country-list-drop-down li");
                            var clone = obj.clone();
                            clone.attr("id", countries[i].country_id);
                            clone.click(function() {
                                activate_text(this, callback);
                            });
                            clone.text(countries[i].country_name);
                            $('#ac-country ul').append(clone);
                        }
                    } else {
                        if (countries[i].client_id == groupId) {

                            var obj = $(".country-list-drop-down li");

                            var clone = obj.clone();
                            clone.attr("id", countries[i].country_id);
                            clone.click(function() {
                                activate_text(this, callback);
                            });
                            clone.text(countries[i].country_name);
                            $('#ac-country ul').append(clone);
                        }
                    }
                }
            }
        } else {
            $('.ac-textbox').hide();
        }
    }
    onArrowKey_Client(e, 'ac-textbox', 'country', callback);
}

//Load country for edit
function LoadCountry(country_id) {
    for (i in countryFulList) {
        if (countryFulList[i].country_id == country_id) {
            $('#country-id').val(country_id);
            $('#country-name').val(countryFulList[i].country_name);
            $('.labelcountry').text(countryFulList[i].country_name);
            break;
        }
    }
}
//Load LegalEntities  ---------------------------------------------------------------------------------------------
function loadLegalEntity() {
    var clientId = clientSelect.val();
    var businessGroupId = bgrpSelect.val();
    var countryId = ctrySelect_id;
    if (businessGroupId == 0) {
        businessGroupId = null;
    }
    if (businessGroupId != null) {
        $('#entity-select').find('option:gt(0)').remove();
        $.each(legalEntitiesList, function(key, value) {
            if (value.client_id == clientId && value.business_group_id == businessGroupId) {
                var lentityId = value.legal_entity_id;
                var lentityName = value.legal_entity_name;

                var obj = $(".le-drop-down option");
                var clone = obj.clone();
                clone.attr("value", lentityId);
                clone.text(lentityName);
                leSelect.append(clone);
            }
        });
    }
    if (businessGroupId == null) {
        $('#entity-select').find('option:gt(0)').remove();
        //$('#division-select').find('option:gt(0)').remove();
        $.each(legalEntitiesList, function(key, value) {
            if (value.client_id == clientId) {
                var lentityId = value.legal_entity_id;
                var lentityName = value.legal_entity_name;
                var obj = $(".le-drop-down option");
                var clone = obj.clone();
                clone.attr("value", lentityId);
                clone.text(lentityName);
                leSelect.append(clone);
            }
        });
    }
}

function addcountryrow() {
    clearMessage();
    var groupId = clientSelect.val();
    var businessgroupid = bgrpSelect.val();
    var lentityId = leSelect.val();
    var countryVal = $('#country-id').val();
    if (groupId == '' && $('#client-unit-id').val() == '') {
        displayMessage(message.group_required);
        return;
    }
    if (countryVal == '' && ($('.labelcountry').text() == '')) {
        displayMessage(message.country_required);
        return;
    }
    if (lentityId == '' && ($('.labelentity').text() == '')) {
        displayMessage(message.legalentity_required);
        return;
    }
    $('.add-country-unit-list').show();

    addcountryrownew();
}

//Add Country Wise List ----------------------------------------------------------------------------------------
function addcountryrownew() {
    countryUnitList.show();
    division_cnt++;

    unit_cnt = 0;
    var countryIds = [];
    var countryFullListIds = [];
    clearMessage();
    var divCountryAddRow = $('#templates .grid-table');
    var clone = divCountryAddRow.clone();
    $('.btable', clone).addClass('table-' + division_cnt);
    $('.countryval', clone).addClass('countryval-' + division_cnt);
    $('.country', clone).addClass('country-' + division_cnt);
    //$('.autocompleteview', clone).addClass('autocompleteview-' + division_cnt);
    //$('.ulist-text', clone).addClass('ulist-text-' + division_cnt);
    $('.select_business_group', clone).addClass('select_business_group-' + division_cnt + '-' + 1);
    $('.input_business_group', clone).addClass('input_business_group-' + division_cnt + '-' + 1);
    $('.divisioncnt', clone).addClass('divisioncnt-' + division_cnt + '-' + 1);
    $('.division-id', clone).addClass('division-id-' + division_cnt + '-' + 1);
    $('.division-name', clone).addClass('division-name-' + division_cnt + '-' + 1);
    $('#division-new', clone).addClass('division-new-' + division_cnt + '-' + 1);
    $('#division-existing', clone).addClass('division-existing-' + division_cnt + '-' + 1);
    $('.divisionid', clone).addClass('divisionid-' + division_cnt + '-' + 1);
    $('.labeldivision', clone).addClass('labeldivision-' + division_cnt + '-' + 1);
    $('.active_cnt', clone).addClass('active_cnt-' + division_cnt + '-' + 1);

    $('.category-name', clone).addClass('category-name-' + division_cnt + '-' + 1);
    $('.labelcategory', clone).addClass('labelcategory-' + division_cnt + '-' + 1);
    $('.categoryid', clone).addClass('categoryid-' + division_cnt + '-' + 1);

    $('.unitcnt', clone).addClass('unitcnt-' + division_cnt + '-' + 1);
    $('.sno', clone).addClass('sno-' + division_cnt + '-' + 1);

    $('.geography-levels', clone).addClass('glevel-' + division_cnt + '-' + 1);
    $('.labelgeolevels', clone).addClass('labelgeolevels-' + division_cnt + '-' + 1)

    $('.unitlocation', clone).addClass('unitlocation-' + division_cnt + '-' + 1);
    $('.labelunitlocation', clone).addClass('labelunitlocation-' + division_cnt + '-' + 1)
    $('.unitlocation-ids', clone).addClass('unitlocation-ids-' + division_cnt + '-' + 1);
    $('.auto-complete-unit-location', clone).addClass('auto-complete-unit-location-' + division_cnt + '-' + 1);
    $('.unitlocationlist-text', clone).addClass('unitlocationlist-text-' + division_cnt + '-' + 1);
    $('.full-location-list', clone).addClass('full-location-list-' + division_cnt + '-' + 1);

    $('.unit-id', clone).addClass('unit-id-' + division_cnt + '-' + 1);

    $('.unitcode-checkbox', clone).addClass('unitcode-checkbox-' + division_cnt);
    $('.unit-code', clone).addClass('unit-code-' + division_cnt + '-' + 1);
    $('.labelunitcode', clone).addClass('labelunitcode-' + division_cnt + '-' + 1)

    $('.unit-name', clone).addClass('unit-name-' + division_cnt + '-' + 1);
    $('.labelunitname', clone).addClass('labelunitname-' + division_cnt + '-' + 1)

    $('.unit-address', clone).addClass('unit-address-' + division_cnt + '-' + 1);
    $('.labelunitaddress', clone).addClass('labelunitaddress-' + division_cnt + '-' + 1)

    $('.postal-code', clone).addClass('postal-code-' + division_cnt + '-' + 1);
    $('.labelpostcode', clone).addClass('labelpostcode-' + division_cnt + '-' + 1)

    $('.domain-list', clone).addClass('domain-list-' + division_cnt + '-' + 1);
    $('.domainselected', clone).addClass('domainselected-' + division_cnt + '-' + 1);
    //$('.domainselected-' + division_cnt + '-' + 1).parent('td').hide();
    //$('.multiselect-native-select', clone).addClass('multiselect-native-select-' + division_cnt + '-' + 1);
    //$('.multiselect-native-select-' + division_cnt + '-' + 1).hide();
    //$('.domain', clone).addClass('domain-' + division_cnt + '-' + 1);
    //loadDomains('domain-' + division_cnt + '-' + 1);
    //$('#domains', clone).addClass('domains-' + division_cnt + '-' + 1);

    $('.domain-selectbox-view', clone).addClass('domain-selectbox-view-' + division_cnt + '-' + 1);
    $('.ul-domain-list', clone).addClass('ul-domain-list-' + division_cnt + '-' + 1);
    $('.labeldomain', clone).addClass('labeldomain-' + division_cnt + '-' + 1)

    $('.orgtype-list', clone).addClass('orgtype-list-' + division_cnt + '-' + 1);
    $('.orgtypeselected', clone).addClass('orgtypeselected-' + division_cnt + '-' + 1);
    //$('.orgtype', clone).addClass('orgtype-' + division_cnt + '-' + 1);
    
    //$('.orgtype-selectbox-view', clone).addClass('orgtype-selectbox-view-' + division_cnt + '-' + 1);
    $('.ul-orgtype-list', clone).addClass('ul-orgtype-list-' + division_cnt + '-' + 1);
    $('.labelorganization', clone).addClass('labelorganization-' + division_cnt + '-' + 1)

    $('.add-unit-row', clone).addClass('table-addunit-' + division_cnt);
    $('.tbody-unit-list', clone).addClass('tbody-unit-' + division_cnt);
    $('.no-of-units', clone).addClass('no-of-units-' + division_cnt);
    $('.activedclass', clone).addClass('activedclass-' + division_cnt + '-' + 1);
    $('.approveclass', clone).addClass('approveclass-' + division_cnt + '-' + 1);

    $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).attr('title', 'Close');
    $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).on('click', function() {
        unitrow_close(this.className);
    });
    $('.rejected-icon', clone).addClass('rejected-icon-' + division_cnt + '-' + 1);
    $('.rejected-icon', clone).addClass('rejected-icon-' + division_cnt + '-' + 1).hide();
    if ($('#client-unit-id').val() > 0) {

        $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).attr('title', 'Edit');
        $('.edit-icon', clone).on('click', function() {
            var orgtypeArray = $('.orgtypeselected-' + division_cnt + '-' + 1, clone).val(); 
            unitrow_edit(this.className, orgtypeArray);
        });
        //$('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).hide();
    }
    /*else
    {
      $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).hide();
      $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).hide();
    }*/
    //$('#unitcount').val(1);
    //$('#countrycount').val(1);
    $('.unit-error-msg', clone).addClass('unit-error-msg-' + division_cnt);
    var tab_len = $('.add-country-unit-list').find('table:eq(0)').length;
    if (tab_len > 0) {
        $('.add-country-unit-list').find('table:eq(0)').before(clone);
    } else {
        $('.add-country-unit-list').append(clone);
    }
    
    $('.no-of-units-' + division_cnt).val(1);
    $('.sno-' + division_cnt + '-' + 1).text(1);
    $('.activedclass-' + division_cnt + '-' + 1).text('Active');
    $('.approveclass-' + division_cnt + '-' + 1).text('Pending');
    $('.edit-icon-' + division_cnt + '-' + 1).show();
    $('.divisioncnt-' + division_cnt + '-' + 1).val(division_cnt);
    $('.unitcnt-' + division_cnt + '-' + 1).val(1);
    if ($("#client-unit-id").val() == "") {
        loadDomains();
        industrytype('industry-' + division_cnt + '-' + 1, []);
    }
    if ($('.unitcode-checkbox').is(':checked')) {
        $('.unit-code-' + division_cnt + '-' + 1).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
        unitcodeautogenerateids++;
    }
    countc++;
    countryByCount++;
    $('.unit-code', clone).on('input', function(e) {
        this.value = isCommon_Unitcode($(this));
    });
    $('.unit-name', clone).on('input', function(e) {
        this.value = isCommon($(this));
    });
    $('.unit-address', clone).on('input', function(e) {
        this.value = isCommon_Address($(this));
    });
    $('.postal-code', clone).on('input', function(e) {
        this.value = isNumbers($(this));
    });
}
//Add Unit for individual Rows---------------------------------------------------------------------------------
function log_units_count(classval) {
    var domain_id = $('.domainselected' + classval).val();
    var org_id = $('.orgtypeselected' + classval).val();
    if (units_count.length > 0) {
        for (var i = 0; i < units_count.length; i++) {
            var split_unit = units_count[i].split("-");
            if (domain_id == split_unit[0] && org_id == split_unit[1]) {
                var assignedUnits = getOrgCount(domain_id, org_id);
                if (assignedUnits <= parseInt(split_unit[2])) {
                    //if(classval.split("-")[2] == "1")
                    //{
                    var msgstatus = message.unit_remove;
                    $('.warning-confirm').dialog({
                        title: 'Remove Unit',
                        buttons: {
                            Ok: function() {
                                $(this).dialog('close');
                                //var index = parseInt($('.tbody-unit-'+division_cnt+' tr').length)-1;
                                var index = parseInt(classval.split("-")[2]);
                                if (index == 1) {
                                    var rowIndx = index - 1;
                                    $('.tbody-unit-' + division_cnt + ' tr').eq(rowIndx).remove();
                                } else {
                                    index = parseInt(classval.split("-")[1]);
                                    var rowIndx = 0;
                                    if (parseInt($('.tbody-unit-' + index + ' tr').length) > 1) {
                                        rowIndx = parseInt($('.tbody-unit-' + index + ' tr').length) - 1;
                                    }
                                    $('.tbody-unit-' + index + ' tr').eq(rowIndx).remove();
                                }
                            },
                            /*Cancel: function () {
                              $(this).dialog('close');
                              prev_org_id = org_id;
                              check_org = true;
                            }*/
                        },
                        open: function() {
                            $('.warning-message').html(msgstatus);
                        }
                    });
                    //}
                } else if (parseInt(assignedUnits) > parseInt(split_unit[2])) {
                    units_count[i] = domain_id + '-' + org_id + '-' + (parseInt(split_unit[2]) + 1);
                }
            }
        }
    } else {
        units_count.push(domain_id + '-' + org_id + '-' + 1);
    }
}

function getOrgCount(domain_id, org_id) {
    var entityval;
    if ($('#client-unit-id').val() != '') {
        entityval = $('#legalentity-update-id').val();
    } else {
        entityval = leSelect.val();
    }
    for (var i in domainList) {
        if (domainList[i].legal_entity_id == entityval && domainList[i].domain_id == domain_id && domainList[i].industry_id == org_id) {
            return domainList[i].unit_count;
        }
    }
}

function unitrow_edit(evt, i_ids) {
    console.log("function unitrow_edit(evt, i_ids) --"+i_ids);
    split_evt_spaces = evt.split(' ');
    split_evt_hyphen = split_evt_spaces[5].split('-');
    var countval = split_evt_hyphen[2] + "-" + split_evt_hyphen[3];
    $('.glevel-' + countval).show();
    $('.labelgeolevels-' + countval).hide();

    $('.unitlocation-' + countval).show();
    $('.unitlocation-ids-' + countval).show();
    $('.full-location-list-' + countval).show();
    $('.labelunitlocation-' + countval).hide();

    $('.unit-code-' + countval).show();
    $('.labelunitcode-' + countval).hide();

    $('.unit-name-' + countval).show();
    $('.labelunitname-' + countval).hide();

    $('.unit-address-' + countval).show();
    $('.labelunitaddress-' + countval).hide();

    $('.postal-code-' + countval).show();
    $('.labelpostcode-' + countval).hide();

    $('.domainselected-' + countval).show();
    $('.ul-domain-list-' + countval).show();
    $('.labeldomain-' + countval).hide();

    $('.orgtypeselected-' + countval).show();
    $('.ul-orgtype-list-' + countval).show();
    $('.labelorganization-' + division_cnt + '-' + unit_cnt).hide();
    $('.labelorganization-' + countval).hide();

    $('.delete-icon-' + countval).show();
    $('.edit-icon-' + countval).hide();

    loadDomains();
    industrytype('industry-' + countval, i_ids );

    $('.domainselected-' + countval).multiselect('rebuild');
    $('.orgtypeselected-' + countval).multiselect('rebuild');

    $('.domainselected-' + countval).parent('span').show();
    $('.orgtypeselected-' + countval).parent('span').show();
}

function unitrow_close(evt) {
    /*split_evt_spaces = evt.split(' ');
    split_evt_hyphen = split_evt_spaces[5].split('-');
    var countval = split_evt_hyphen[2] + "-" + split_evt_hyphen[3];

    var unit_id = $('.unit-id-' + countval).val();
    for (var i in unitList) {
        if (unitList[i].unit_id == unit_id) {
            loadUnitValues_exists(unitList[i], split_evt_hyphen[2]);
        }
    }
    $('.domainselected-'+countval).parent('span').hide();
    $('.orgtypeselected-'+countval).parent('span').hide();

    $('.edit-icon-' + countval).show();
    $('.delete-icon-' + countval).hide();*/


    split_evt_spaces = evt.split(' ');
    split_evt_hyphen = split_evt_spaces[5].split('-');
    var countval = split_evt_hyphen[2] + "-" + split_evt_hyphen[3];
    $('.glevel-' + countval).hide();
    $('.labelgeolevels-' + countval).show();

    $('.unitlocation-' + countval).hide();
    $('.unitlocation-ids-' + countval).hide();
    $('.full-location-list-' + countval).hide();
    $('.labelunitlocation-' + countval).show();

    $('.unit-code-' + countval).hide();
    $('.labelunitcode-' + countval).show();

    $('.unit-name-' + countval).hide();
    $('.labelunitname-' + countval).show();

    $('.unit-address-' + countval).hide();
    $('.labelunitaddress-' + countval).show();

    $('.postal-code-' + countval).hide();
    $('.labelpostcode-' + countval).show();

    $('.domainselected-' + countval).hide();
    $('.ul-domain-list-' + countval).hide();
    $('.labeldomain-' + countval).show();

    $('.orgtypeselected-' + countval).hide();
    $('.ul-orgtype-list-' + countval).hide();
    $('.labelorganization-' + division_cnt + '-' + unit_cnt).show();
    $('.labelorganization-' + countval).show();

    $('.delete-icon-' + countval).hide();
    $('.edit-icon-' + countval).show();

    /*loadDomains();
    industrytype('industry-' + countval);*/

    $('.domainselected-' + countval).parent('span').hide();
    $('.orgtypeselected-' + countval).parent('span').hide();
}

function check_previous_orgn(evt) {
    /*var tableclassname = $(evt).parents('table').attr('class');

    var tableclass = tableclassname.split(' ');
    var tbodyclassname = $('.' + tableclass[1]).find('tbody:eq(1)').attr('class');
    var tbodyclasses = tbodyclassname.split(' ');*/
    if (check_org == true) {
        var unitno = $('.unitcnt-' + division_cnt + '-' + 1).val();
        var org_id = $('.orgtypeselected-' + division_cnt + '-' + parseInt(unitno - 1)).val();
        if (org_id == prev_org_id) {
            var msgstatus = message.unit_remove;
            $('.warning-confirm').dialog({
                title: 'Remove Unit',
                buttons: {
                    Ok: function() {
                        $(this).dialog('close');
                        var index = parseInt($('.tbody-unit-' + division_cnt + ' tr').parent().index());
                        $('.tbody-unit-' + division_cnt + ' tr').eq(index).remove();
                    },
                    /*Cancel: function () {
                      $(this).dialog('close');
                      prev_org_id = org_id;
                      check_org = true;
                    }*/
                },
                open: function() {
                    $('.warning-message').html(msgstatus);
                }
            });
        } else {
            check_org = false;
            addNewUnitRow(evt);
        }
    } else {
        addNewUnitRow(evt);
    }

}

function addNewUnitRow(str) {
    var lastIndexOf_hyphen = str.lastIndexOf('-');
    var countval = str.substring((lastIndexOf_hyphen + 1), (lastIndexOf_hyphen + 2));
        //var countval = division_cnt;
    var unitval = parseInt($('.unitcnt-' + countval + '-' + 1).val()) + 1;
    $('.unitcnt-' + countval + '-' + 1).val(unitval);

    var divUnitAddRow = $('#templatesUnitRow').find('tr:eq(0)');
    var clone1 = divUnitAddRow.clone();

    $('.tbody-unit-' + countval).find('tr:eq(0)').before(clone1);
    var table_tr = $('.tbody-unit-' + countval).find('tr:eq(0)');
    /*$(this).attr({
        'class': function(_, lastClass) { return $(this).attr('class').substring(0,
          ($(this).attr('class').length - 4)) + '-'+division_cnt+'-'+unitval },
        }); */
    table_tr.find('td').find('input,select,span,div,ul').each(function() {
        $(this).attr({
            'class': function(_, lastClass) {
                return $(this).attr('class').split(' ').pop() + ' ' + $(this).attr('class') + '-' + division_cnt + '-' + unitval },
        });
    });
    $('.sno-' + division_cnt + '-' + unitval).text(unitval);

    $('.rejected-icon-' + division_cnt + '-' + (lastClassval + 1)).hide();

    if ($('.unitcode-checkbox-' + division_cnt).is(':checked')) {
        $('.unit-code-' + division_cnt + '-' + unitval).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
        unitcodeautogenerateids++;
    }
    //$('.sno-'+division_cnt+'-'+unitval).text(unitval);
    $('.activedclass-' + division_cnt + '-' + unitval).text('Active');
    $('.approveclass-' + division_cnt + '-' + unitval).text('Pending');
    
    $('.unit-code-' + division_cnt + '-' + unitval).on('input', function(e) {
        this.value = isCommon_Unitcode($(this));
    });
    $('.unit-name-' + division_cnt + '-' + unitval).on('input', function(e) {
        this.value = isCommon($(this));
    });
    $('.unit-address-' + division_cnt + '-' + unitval).on('input', function(e) {
        this.value = isCommon_Address($(this));
    });
    $('.postal-code-' + division_cnt + '-' + unitval).on('input', function(e) {
        this.value = isNumbers($(this));
    });
    loadDomains();
    industrytype('industry-' + division_cnt + '-' + unitval, []);
}

function addNewUnitRow_edit(str) {
    var countval = str.split("-")[2].trim();

    var unitval = parseInt($('.tbody-unit-' + countval).find('tr').length) + 1;
    $('.unitcnt-' + countval + '-' + 1).val(unitval);

    var divUnitAddRow = $('#templatesUnitRow').find('tr:eq(0)');
    var clone1 = divUnitAddRow.clone();

    $('.tbody-unit-' + countval).find('tr:eq(0)').before(clone1);
    var table_tr = $('.tbody-unit-' + countval).find('tr:eq(0)');
    /*$(this).attr({
        'class': function(_, lastClass) { return $(this).attr('class').substring(0,
          ($(this).attr('class').length - 4)) + '-'+division_cnt+'-'+unitval },
        }); */
    table_tr.find('td').find('input,select,span,div,ul,i').each(function() {
        $(this).attr({
            'class': function(_, lastClass) {
                return $(this).attr('class').split(' ').pop() + ' ' + $(this).attr('class') + '-' + countval + '-' + unitval },
        });
    });
    $('.sno-' + countval + '-' + unitval).text(unitval);


    $('.edit-icon-' + countval + '-' + unitval).attr('title', 'Edit');

    $('.delete-icon-' + countval + '-' + unitval).attr('title', 'Close');
    $('.delete-icon-' + countval + '-' + unitval).on('click', function() {
        unitrow_close(this.className);
    });

    $('.edit-icon-' + countval + '-' + unitval).hide();
    $('.delete-icon-' + countval + '-' + unitval).hide();
    $('.rejected-icon-' + countval + '-' + unitval).hide();

    if ($('.unitcode-checkbox-' + countval).is(':checked')) {
        $('.unit-code-' + division_cnt + '-' + unitval).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
        unitcodeautogenerateids++;
    }
    //$('.sno-'+division_cnt+'-'+unitval).text(unitval);
    $('.activedclass-' + countval + '-' + unitval).text('Active');
    $('.approveclass-' + countval + '-' + unitval).text('Pending');
    
    $('.unit-code-' + countval + '-' + unitval).on('input', function(e) {
        this.value = isCommon_Unitcode($(this));
    });
    $('.unit-name-' + countval + '-' + unitval).on('input', function(e) {
        this.value = isCommon($(this));
    });
    $('.unit-address-' + countval + '-' + unitval).on('input', function(e) {
        this.value = isCommon_Address($(this));
    });
    $('.postal-code-' + countval + '-' + unitval).on('input', function(e) {
        this.value = isNumbers($(this));
    });

    loadDomains();
    industrytype('industry-' + countval + '-' + unitval, []);

    $('.domainselected').parent('span').hide();
    $('.orgtypeselected').parent('span').hide();
}

function intTo5digitsString(nb) {
    if (nb > 0 && nb < 10)
        return '0000' + nb;
    else if (nb >= 10 && nb < 100)
        return '000' + nb;
    else if (nb >= 100 && nb < 1000)
        return '00' + nb;
    else if (nb >= 1000 && nb < 10000)
        return '0' + nb;
}

function autoGenerateUnitCode() {
    var client_id = $('#group-select').val();
    if (client_id == '' || client_id == null || client_id == "Select") {
        client_id = $('#client-unit-id').val();
    }
    function onSuccess(data) {
        unitcodeautogenerate(data.next_unit_code);
    }

    function onFailure(error) {
        displayMessage(error);
    }
    mirror.getNextUnitCode(parseInt(client_id), function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

function unitcodeautogenerate(auto_generate_initial_value) {
    unitcodeautogenerateids = null;
    if ($('.labelgroup').text().trim() == '') {
        unitcodeautogenerateids = auto_generate_initial_value;
        var sno = [];
        if ($('.unitcode-checkbox').is(':checked')) {
            var groupname = $.trim($('#group-select :Selected').text());
            var groupname = groupname.replace(' ', '');
            get2CharsofGrouplower = groupname.slice(0, 2);
            get2CharsofGroup = get2CharsofGrouplower.toUpperCase();

            var flag = 0;
            $('.add-country-unit-list .unit-code').each(function(i) {
                if ($(this).prev('.unit-id').val() == '') {

                    $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    unitcodeautogenerateids++;
                } else {
                    $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    unitcodeautogenerateids++;
                }
            });
        } else {
            $('.add-country-unit-list .unit-code').each(function(i) {
                if ($(this).prev('.unit-id').val() == '') {
                    $(this).val(''); //$(this).removeAttr("readonly");
                }
            });
        }
    }
    if ($('.labelgroup').text().trim() != '') {
        // client_id = $("#client-unit-id").val();
        // $.each(groupList, function(key, value){
        //     if(value['client_id'] == client_id){
        //         auto_generate_initial_value = value["next_unit_code"];
        //     }
        // });
        unitcodeautogenerateids = auto_generate_initial_value;
        var sno = [];
        if ($('.unitcode-checkbox').is(':checked')) {
            var groupname = $.trim($('.labelgroup').text());
            var groupname = groupname.replace(' ', '');
            get2CharsofGrouplower = groupname.slice(0, 2);
            get2CharsofGroup = get2CharsofGrouplower.toUpperCase();
            var flag = 0;
            $('.add-country-unit-list .unit-code').each(function(i) {
                if ($(this).prev('.unit-id').val() == '') {
                    $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    unitcodeautogenerateids++;
                } //$(this).attr("readonly", "readonly");
            });
        } else {
            $('.add-country-unit-list .unit-code').each(function(i) {
                if ($(this).prev('.unit-id').val() == '') {
                    $(this).val(''); //$(this).removeAttr("readonly");
                }
            });
        }
    }
}

//load division
function loadDivision(classval) {
    var lastClass = classval.split(' ').pop();
    var clientId, businessGroupId, lentityId;
    if ($('#client-unit-id').val() != '') {
        clientId = $('#client-unit-id').val();
        businessGroupId = $('#businessgroup-update-id').val();
        lentityId = $('legalentity-update-id').val();
    } else {
        clientId = clientSelect.val();
        businessGroupId = bgrpSelect.val();
        lentityId = leSelect.val();
    }

    $('.' + lastClass).find('option:gt(0)').remove();
    $.each(divisionList, function(key, value) {
        if (businessGroupId > 0) {
            if (value.client_id == clientId && value.business_group_id == businessGroupId && value.legal_entity_id == lentityId) {
                var divisionId = value.division_id;
                var divisionName = value.division_name;
                var obj = $('.divi-drop-down option');
                var clone = obj.clone();
                clone.attr("value", divisionId);
                clone.text(divisionName);
                $('.' + lastClass).append(clone);
            }
        } else {
            if (value.client_id == clientId && value.legal_entity_id == lentityId) {
                var divisionId = value.division_id;
                var divisionName = value.division_name;
                var obj = $('.divi-drop-down option');
                var clone = obj.clone();
                clone.attr("value", divisionId);
                clone.text(divisionName);
                $('.' + lastClass).append(clone);
            }
        }
    });
}

function divisionExistingChecking(str) {
    var countval = '-' + division_cnt + '-' + 1;
    if (str == 'New') {
        $('.input_business_group' + countval).show();
        $('.division-name' + countval).show();
        $('.division-id' + countval).hide();
        $('.division-new' + countval).hide();
        $('.division-existing' + countval).show();
        $('.division-name' + countval).val('');
        $('.division-id' + countval).val('');
        $('.select_business_group' + countval).hide();
    }
    if (str == 'Cancel') {
        if ($('#client-unit-id').val() == '') {
            $('.select_business_group' + countval).show();
        } else {
            $('.select_business_group' + countval).hide();
        }
        $('.input_business_group' + countval).hide();
        $('.division-name' + countval).hide();
        $('.division-id' + countval).show();
        $('.division-new' + countval).show();
        $('.division-existing' + countval).hide();
        $('.division-name' + countval).val('');
        $('.division-id' + countval).val('');
        $('.division-id' + countval).find('option').not(':first').remove();
        loadDivision(classval);
    }
}

//Load Geography Levels -------------------------------------------------------------------------------------------
function loadglevels(classval) {
    //input-box geography-levels glevel-1-1
    var lastClass = classval.split(' ').pop();
    var checkval = lastClass.split('-');
    var countryvalue = $('#country-name').val();
    var countryid = $('#country-id').val();
    if (countryvalue == '') {
        displayMessage(message.country_required);
    } else {
        $('.' + lastClass).empty();
        var obj = $('.glevel-drop-down option');
        var clone = obj.clone();
        clone.attr("value", 0);
        clone.text("Select");
        $('.' + lastClass).append(clone);
        $.each(geographyLevelList, function(key, value) {
            obj = $('.glevel-drop-down option');
            clone = obj.clone();
            var level_id = value.l_id;
            var level_name = value.l_name;
            if (countryid == value.c_id)
                clone.attr("value", level_id);
            clone.text(level_name);
            $('.' + lastClass).append(clone);
        });
        //$('.'+lastClass +'option:gt(0)').remove();
    }
}

//set selected autocomplte value to textbox and geographylevel list
function hideunitlocation(classname) {
    var lastClass = classname.split(' ').pop();
    $('.' + lastClass).css('display', 'none');
}

function activate_unitlocaion(element, ccount, mappingname) {

    var checkname = $(element).text();
    var checkval = $(element).attr('id');
    $('.unitlocation' + ccount).val(checkname);
    $('.unitlocation-ids' + ccount).val(checkval);
    $('.full-location-list' + ccount).html(mappingname);
}
//autocomplete location
function loadlocation(textval, classval, e) {

    var lastClass = classval.split(' ').pop();
    var ccount = lastClass.split('-');
    var countval = '-' + ccount[1] + '-' + ccount[2];

    var glevelval = $('.glevel' + countval).val();

    $('.auto-complete-unit-location' + countval).css('display', 'block');
    var suggestions = [];
    $('.unitlocationlist-text' + countval).empty();
    if (textval.length > 0) {
        for (var glist in geographyList) {

            if (geographyList[glist].level_id == glevelval) {
                if (~geographyList[glist].geography_name.toLowerCase().indexOf(textval.toLowerCase()) && geographyList[glist].is_active == 1) {

                    var obj = $(".location-list-drop-down li");
                    var clone = obj.clone();
                    clone.attr("id", geographyList[glist].geography_id);
                    clone.click(function() {
                        activate_unitlocaion(this, countval, geographyList[glist].mapping);
                    });
                    clone.text(geographyList[glist].geography_name);
                    $('.unitlocationlist-text' + countval).append(clone);
                }
            }
        }
        //$('.unitlocationlist-text' + countval).append(str);
        //$('.unitlocation-ids'+countval).val('');
        onArrowKey_Client(e, 'unitlocationlist-text' + countval, countval, 'unit');
    }
}

function loadupdateunitlocation(gid) {
    var units = {};
    for (var i in geographyList) {
        var v = geographyList[i];
        if (v.geography_id == gid) {
            units.gname = v.geography_name;
            units.mapping = v.mapping;
            units.level_id = v.level_id;
        }
    }

    return units;
}

function changelocation(classval) {
    var lastClass = classval.split(' ').pop();
    var checkval = lastClass.split('-');
    $('.unitlocation-' + checkval[1] + '-' + checkval[2]).val('');
    $('.unitlocation-ids-' + checkval[1] + '-' + checkval[2]).val('');
    $('.full-location-list-' + checkval[1] + '-' + checkval[2]).html('');
}

//get domain for edit section
function getDomainsName(domain_ids) {
    domain_names = [];

    for (var i = 0; i < domain_ids.length; i++) {
        for (var j = 0; j < domainList.length; j++) {
            if (domain_ids[i] == domainList[j].domain_id) {
                domain_names.push(domainList[j].domain_name);
                break;
            }
        }
    }
    return domain_names;
}

//load domains
function loadDomains() {
    var d_ctrl = $('.domainselected-' + division_cnt + '-' + $(".unitcnt-" + division_cnt + "-" + 1).val());
    d_ctrl.empty();
    var getClientid;
    if (($('#client-unit-id').val() == '') || ($('#client-unit-id').val() == 0)) {
        getClientid = $('#group-select').val();
    } else {
        getClientid = $('#client-unit-id').val();
    }
    if ($('#client-unit-id').val() == 0) {
        var domains = domainList;
        var lentityId = leSelect.val();
        var optText = "";
        $.each(domains, function(key, value) {
            if (lentityId == domains[key].legal_entity_id) {
                optText = optText + '<option value="'+domains[key].domain_id+'" >'+domains[key].domain_name+'</option>';
            }
        });
        d_ctrl.html(optText);
    } else {
        var domains = domainList;
        var lentityId = $(".labelentity").data('id');
        var optText = "";
        $.each(domains, function(key, value) {
            if (lentityId == domains[key].legal_entity_id) {
                var sel = "selected";
                optText = optText + '<option value="'+domains[key].domain_id+'" selected="'+sel+'" >'+domains[key].domain_name+'</option>';
            }
        });
        d_ctrl.html(optText);
    }
    d_ctrl.multiselect('rebuild'); 
}


//industry
function industrytype(classval, selected_arr) {
    //alert(selected_arr);
    //selected_arr
    var lastClass = classval.split(' ').pop();
    var ccount = lastClass.split('-');
    var countval = '-' + ccount[1] + '-' + ccount[2];
    var domain_id, lentityId, unitid;
    if ($('#client-unit-id').val() == '') {
        domain_id = $('.domainselected' + countval).val();
        lentityId = leSelect.val();
    } else {
        domain_id = $('.domainselected' + countval).val();
        lentityId = $(".labelentity").data('id');
        unitid = $('.unit-id-' + ccount[1] + '-' + ccount[2]);
    }
    //alert(domainList.toSource());

    var editorgtypeval = [];

    if (lentityId > 0) {
        //alert(lentityId);
        if ($('#client-unit-id').val() == 0 || $('#client-unit-id').val() == '') {
            var domains = domainList;
            var optText = "";
            for (var i in domains) {
                if (lentityId == domains[i].legal_entity_id) {
                    var orgtypeId = parseInt(domains[i].industry_id);
                    var orgtypeName = domains[i].industry_name;
                    optText = optText + '<option value="'+orgtypeId+'" >'+orgtypeName+'</option>';
                }
            }
            $('.orgtypeselected' + countval).html(optText);
        } else {
            console.log(selected_arr);
            editorgtypeval = selected_arr
            var domains = domainList;
            var optText = "";
            for (var i in domains) {
                var selectorgtypestatus = '';
                for (var j = 0; j < editorgtypeval.length; j++) {
                    console.log(editorgtypeval[j] +"=="+domains[i].industry_id);
                    if (editorgtypeval[j] == domains[i].industry_id) {
                        selectorgtypestatus = 'selected';
                    }
                }
                console.log("le----"+lentityId +' - '+domains[i].legal_entity_id);
                if (lentityId == domains[i].legal_entity_id) {

                    var orgtypeId = parseInt(domains[i].industry_id);
                    var orgtypeName = domains[i].industry_name;
                    //alert(orgtypeName+' - '+orgtypeId);
                    //var sel = "selected";
                    optText = optText + '<option value="'+orgtypeId+'" '+selectorgtypestatus+'>'+orgtypeName+'</option>';
                }
            }
            $('.orgtypeselected' + countval).html(optText);
        }
    } else {
        if (lentityId == 0 && $('#client-unit-id').val() == '') {
            displayMessage(message.legalentity_required);
        }
        if (domain_id == 0) {
            displayMessage(message.domain_required);
        }
    }
    $('.orgtypeselected' + countval).multiselect('rebuild');
}


//get organization for edit section
function getOrganizationName(org_ids) {
    orgn_names = [];

    for (var i = 0; i < org_ids.length; i++) {
        for (var j = 0; j < domainList.length; j++) {
            if (org_ids[i] == domainList[j].industry_id) {
                orgn_names.push(domainList[j].industry_name);
                break;
            }
        }
    }
    return orgn_names;
}

function onArrowKeyUnit(e, ac_item, count) {
    if (e.keyCode == 13) {
        chosen_unit = '';
        $('.domain-selectbox-view').hide();
    }
    if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 32) {
        chosen_unit = '';
    }
    if (e.keyCode == 40) {
        if (chosen_unit === '') {
            chosen_unit = 0;
        } else if (chosen_unit + 1 < $('.' + ac_item + ' li').length) {
            chosen_unit++;
        }
        $('.' + ac_item + ' li').removeClass('auto-selected');
        $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 38) {
        if (chosen_unit === '') {
            chosen_unit = 0;
        } else if (chosen_unit > 0) {
            chosen_unit--;
        }
        $('.' + ac_item + ' li').removeClass('auto-selected');
        $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('auto-selected');
        return false;
    }
    if (e.keyCode == 32) {
        $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('auto-selected');
        var ms_id = $('.' + ac_item + ' li:eq(' + chosen_unit + ')').attr('id');
        var chkstatus = $('.' + ac_item + ' li:eq(' + chosen_unit + ')').attr('class');
        if (ac_item.indexOf('domains') != -1) {
            if (chkstatus == 'active_selectbox' + count + ' active') {
                $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active_selectbox' + count);
                $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active');
            } else {
                $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active_selectbox' + count);
                $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active');
            }
        } else if (ac_item.indexOf('orgtype') != -1) {
            if (chkstatus == 'active_org_selectbox' + count + ' active') {
                $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active_org_selectbox' + count);
                $('.' + ac_item + ' li:eq(' + chosen_unit + ')').removeClass('active');
            } else {
                $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active_org_selectbox' + count);
                $('.' + ac_item + ' li:eq(' + chosen_unit + ')').addClass('active');
            }
        }



        if (ac_item.indexOf('domains') != -1) {
            activate_domain(count);
        } else if (ac_item.indexOf('orgtype') != -1) {
            activate_orgtype(count);
        }

        return false;
    }
}

//Submit Record -----------------------------------------------------------------------------------------

$('#btn-clientunit-submit').click(function() {
    clearMessage();
    var clientunitIdValue = $('#client-unit-id').val();
    var groupNameValue = $('#group-select option:selected').val();
    var businessgroupValue = $('#businessgroup-select option:selected').val();
    var businessgroupName = $('#businessgroup-select option:selected').text();
    var legalEntityValue = $('#entity-select option:selected').val();
    var legalEntityName = $('#entity-select option:selected').text();
    var countryValue = $('#country-name');
    //var divisiontextValue = $('#division-text').val();
    //var divisionValue = $('#division-select').val();
    //var divisionName = $('#division-select :selected').text();
    var unitCountValue = $('#unitcount').val();
    var countryVal = $('#country-id').val();
    var countryName = $('#country-name').val();
    if (clientunitIdValue == '') {
        if (groupNameValue == '') {
            displayMessage(message.group_required);
            return false;
        }
        if (countryName.length == 0) {
            if (countryVal == '') {
                displayMessage(message.country_required);
                return false;
            }
        }

        if (countryVal.length == '') {
            displayMessage(message.country_required);
            return false;
        }
        if (legalEntityValue == "" || legalEntityValue == 0) {
            displayMessage(message.legalentity_required);
            return false;
        }
        if (unitCountValue.length == 0) {
            displayMessage(message.add_one_unit);
            return false;
        }

        function onSuccess(data) {
            $('#clientunit-add').hide();
            $('#clientunit-view').show();
            initialize();
        }

        function onFailure(error) {
            if (error == 'BusinessGroupNameAlreadyExists') {
                displayMessage(message.bgroup_exists);
            } else if (error == 'LegalEntityNameAlreadyExists') {
                displayMessage(message.lentity_exists);
            } else if (error == 'DivisionNameAlreadyExists') {
                displayMessage(message.division_exists);
            } else if (error == 'UnitCodeAlreadyExists') {
                displayMessage(message.unitcode_exists);
            } else {
                displayMessage(error);
            }
        }
        var businessGroup;
        var bgIdValue;
        var bgNameValue;
        bgIdValue = parseInt(businessgroupValue);
        if (businessgroupValue != '') {
            bgNameValue = businessgroupName;
        } else {
            bgNameValue = null;
        }
        var legalEntity;
        var leIdValue;
        var leNameValue;
        leIdValue = parseInt(legalEntityValue);
        if (legalEntityValue != '') {
            leNameValue = legalEntityName;
        } else {
            leNameValue = null;
        }

        var division;
        var divIdValue;
        var divNameValue;

        var category = null;

        var units = [];
        var division_units = [];
        var unitarr = [];
        for (var i = 1; i <= division_cnt; i++) {
            var div_arr;
            divisionValue = $('.division-id-' + i + '-' + 1).val();
            divisiontextValue = $('.division-name-' + i + '-' + 1).val();
            if (divisiontextValue == '') {
                divIdValue = parseInt(divisionValue);
                divNameValue = null;
            } else {
                divIdValue = null;
                divNameValue = divisiontextValue;
            }
            unit_cnt = $('.unitcnt-' + i + '-1').val();

            if ($('.category-name-' + i + '-' + 1).val() != '') {
                category = $('.category-name-' + i + '-' + 1).val();
            } else {
                category = null;
            }

            div_arr = mirror.getDivisionDict(divIdValue, divNameValue, category, i, parseInt(unit_cnt));
            division_units.push(div_arr);


            if (unit_cnt > 0) {
                for (var j = 1; j <= unit_cnt; j++) {
                    var unit;
                    var unitIndustryIds = [];
                    var unitdomains = [];
                    unitId = null;
                    unitCode = $('.unit-code-' + i + '-' + j).val();

                    unitName = $('.unit-name-' + i + '-' + j).val().trim();
                    unitAddress = $('.unit-address-' + i + '-' + j).val().trim();
                    unitPostalCode = $('.postal-code-' + i + '-' + j).val().trim();
                    unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
                    unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();


                    unitIndustryId = $('.orgtypeselected-' + i + '-' + j).val();

                    //unitIndustryName = $('.industry-' + i + '-' + j + ' option:selected').text();

                    unitdomain = $('.domainselected-' + i + '-' + j).val();

                    if (unitLocation == '' && unitGeographyId == '' && unitCode == '' && unitName == '' && unitAddress == '' && unitPostalCode == '' && unitdomains.length == 0 && unitIndustryIds.length == 0) {
                        if (unitcount == 1) {
                            displayMessage(message.add_one_unit);
                            return;
                        }
                        continue;
                    }
                    if (unitLocation == '') {
                        displayMessage(message.unitlocation_required);
                        return;
                    } else if (unitGeographyId == '') {
                        displayMessage(message.unitlocation_invalid);
                        return;
                    } else if (unitCode == '') {
                        displayMessage(message.unitcode_required);
                        return;
                    } else if (unitName == '') {
                        displayMessage(message.unitname_required);
                        return;
                    } else if (unitIndustryId == '' || unitIndustryId == null) {
                        displayMessage(message.industryname_required);
                        return;
                    } else if (unitAddress == '') {
                        displayMessage(message.unitaddress_required);
                        return;
                    } else if (unitPostalCode == '') {
                        displayMessage(message.unitpostal_required);
                        return;
                    } else if (unitdomain == '' || unitdomain == null) {
                        displayMessage(message.domain_required);
                        return;
                    } else {
                        unitarr.push(unitCode);
                        var hash = [];
                        for (var n = unitarr.length; n--;) {
                            if (typeof hash[unitarr[n]] === 'undefined')
                                hash[unitarr[n]] = [];
                            hash[unitarr[n]].push(n);
                        }
                        var duplicates = [];
                        for (var key in hash) {
                            if (hash.hasOwnProperty(key) && hash[key].length > 1) {
                                duplicates.push(key);
                            }
                        }
                        if (duplicates == '') {
                            for (var ij = 0; ij < unitIndustryId.length; ij++) {
                                $.each(industryList, function(k, val) {
                                    var list = {};
                                    if (val["industry_id"] == unitIndustryId[ij] && val["legal_entity_id"] == leIdValue) {
                                        list['domain_id'] = val['domain_id'];
                                        list['industry_id'] = val['industry_id'];
                                        unitIndustryIds.push(list);
                                    }
                                });

                            }
                            for (var ij = 0; ij < unitdomain.length; ij++) {
                                unitdomains.push(parseInt(unitdomain[ij]));
                            }
                            //domains multi select
                            // var arrayDomainsVal = "";
                            // if(unitdomain.indexOf(',')!=-1)
                            // {
                            //   arrayDomainsVal = unitdomain.split(',');
                            // }
                            // else
                            // {
                            //   arrayDomainsVal = unitdomain;
                            // }
                            // var arrayDomains = [];
                            // for (var m = 0; m < arrayDomainsVal.length; m++) {
                            //   arrayDomains[m] = parseInt(arrayDomainsVal[m]);
                            // }
                            // var domainsVal = arrayDomains;

                            // //Organization Multiselect
                            // var arrayOrgtypeVal = "";
                            // if(unitIndustryId.indexOf(',')!=-1)
                            // {
                            //   arrayOrgtypeVal = unitIndustryId.split(',');
                            // }
                            // else
                            // {
                            //   arrayOrgtypeVal = unitIndustryId;
                            // }
                            // var arrayOrgtype = [];
                            // for (var m = 0; m < arrayOrgtypeVal.length; m++) {
                            //   arrayOrgtype[m] = parseInt(arrayOrgtypeVal[m]);
                            // }
                            // var OrgtypeVal = arrayOrgtype;


                            unit = mirror.getUnitDict(null, unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitdomains, unitIndustryIds);

                            units.push(unit);
                        } else {
                            displayMessage(duplicates + ' Unit Code Already Exits!!!');
                            return;
                        }
                    }
                }
            } else {
                displayMessage(message.add_one_unit);
                return;
            }
        }
        mirror.saveClient(parseInt(groupNameValue), parseInt(bgIdValue), leIdValue, parseInt(countryVal), division_units, units, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.record_added);
                units_count = [];
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
        //client id null -- end
    } else if (clientunitIdValue != '') {
        clearMessage();

        function onSuccess(data) {
            $('#clientunit-add').hide();
            $('#clientunit-view').show();
            initialize();
        }

        function onFailure(error) {
            if (error == 'BusinessGroupNameAlreadyExists') {
                displayMessage(message.bgroup_exists);
            } else if (error == 'LegalEntityNameAlreadyExists') {
                displayMessage(message.lentity_exists);
            } else if (error == 'DivisionNameAlreadyExists') {
                displayMessage(message.division_exists);
            } else if (error == 'UnitCodeAlreadyExists') {
                displayMessage(message.unitcode_exists);
            } else {
                displayMessage(error);
            }
        }

        client_id = $('#client-unit-id').val();
        bgIdValue = $('#businessgroup-update-id').val();
        leIdValue = $('#legalentity-update-id').val();
        countryVal = $('#country-id').val();

        var division;
        var divIdValue;
        var divNameValue;

        var category = "null";

        var units = [];
        var division_units = [];
        var unitarr = [];
        var total_div = 0;
        var total_units = 0;

        for (var i = 1; i <= division_cnt; i++) {
            //get division ctrl value
            var divi_span_ctrl = $('.division-id-' + i + '-' + 1).attr('style');
            if (divi_span_ctrl == "display: none;") {
                divIdValue = $('.divisionid-' + i + '-' + 1).val();
                divNameValue = null;
            } else {
                divisionValue = $('.division-id-' + i + '-' + 1).val();
                divisiontextValue = $('.division-name-' + i + '-' + 1).val();
                if (divisiontextValue == '') {
                    divIdValue = parseInt(divisionValue);
                    divNameValue = null;
                } else {
                    divIdValue = null;
                    divNameValue = divisiontextValue;
                }
            }

            //get category values
            var catg_span_ctrl = $('.category-name-' + i + '-' + 1).attr('style').split(";")[1].trim();
            if (catg_span_ctrl == "display: none") {

                category = $('.labelcategory-' + i + '-' + 1).text() + "-" + $('.categoryid-' + i + '-' + 1).val();

                //category = null;
            } else {
                if ($('.category-name-' + i + '-' + 1).val() != '') {
                    category = $('.category-name-' + i + '-' + 1).val();
                } else {
                    category = null;
                }
            }
            unit_cnt = $('.unitcnt-' + i + '-1').val();


            if (unit_cnt > 0) {
                for (var j = 1; j <= unit_cnt; j++) {
                    var unit;
                    var edit_icon = $('.edit-icon-' + i + '-' + j).attr('style').split(";")[0].trim();
                    var unitId, unitCode, unitName, unitAddress, unitPostalCode, unitGeographyId;
                    var unitLocation, unitIndustryId, unitdomain;

                    if (($('.unit-id-' + i + '-' + j).val() != "" && (edit_icon.indexOf("display: none") >= 0))) {
                        unitId = $('.unit-id-' + i + '-' + j).val();

                        if ($('.unit-code-' + i + '-' + j).attr('style') == "display: none;") {
                            unitCode = $('.labelunitcode-' + i + '-' + j).text();
                        } else {
                            unitCode = $('.unit-code-' + i + '-' + j).val();
                        }

                        if ($('.unit-name-' + i + '-' + j).attr('style') == "display: none;") {
                            unitName = $('.labelunitname-' + i + '-' + j).text();
                        } else {
                            unitName = $('.unit-name-' + i + '-' + j).val();
                        }

                        if ($('.unit-address-' + i + '-' + j).attr('style') == "display: none;") {
                            unitAddress = $('.labelunitaddress-' + i + '-' + j).text();
                        } else {
                            unitAddress = $('.unit-address-' + i + '-' + j).val();
                        }

                        if ($('.postal-code-' + i + '-' + j).attr('style') == "display: none;") {
                            unitPostalCode = $('.labelpostcode-' + i + '-' + j).text();
                        } else {
                            unitPostalCode = $('.postal-code-' + i + '-' + j).val();
                        }

                        if ($('.unitlocation-ids-' + i + '-' + j).attr('style') == "display: none;") {
                            unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
                        } else {
                            unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
                        }

                        if ($('.unitlocation-' + i + '-' + j).attr('style') == "display: none;") {
                            unitLocation = $('.labelunitlocation-' + i + '-' + j).text();
                        } else {
                            unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();
                        }

                        if ($('.orgtypeselected-' + i + '-' + j).attr('style') == "display: none;") {
                            unitIndustryId = $('.labelorganization-' + i + '-' + j).text();
                        } else {
                            unitIndustryId = $('.orgtypeselected-' + i + '-' + j).val();
                        }

                        if ($('.domainselected-' + i + '-' + j).attr('style') == "display: none;") {
                            unitdomain = $('.labeldomain-' + i + '-' + j).text();
                        } else {
                            unitdomain = $('.domainselected-' + i + '-' + j).val().map(Number);
                            unitdomains = unitdomain;
                        }
                    } else if ($('.unit-id-' + i + '-' + j).val() == "") {
                        unitId = null;
                        unitCode = $('.unit-code-' + i + '-' + j).val();

                        unitName = $('.unit-name-' + i + '-' + j).val().trim();
                        unitAddress = $('.unit-address-' + i + '-' + j).val().trim();
                        unitPostalCode = $('.postal-code-' + i + '-' + j).val().trim();
                        unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
                        unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();

                        unitIndustryId = $('.orgtypeselected-' + i + '-' + j).val();

                        //unitIndustryName = $('.industry-' + i + '-' + j + ' option:selected').text();
                        unitdomain = $('.domainselected-' + i + '-' + j).val();

                    }
                    if (($('.unit-id-' + i + '-' + j).val() != "" && (edit_icon.indexOf("display: none") >= 0)) ||
                        ($('.unit-id-' + i + '-' + j).val() == "")) {
                        total_units = total_units + 1;
                        console.log(i, j)
                        if (unitLocation == '' && unitGeographyId == '' && unitCode == '' && unitName == '' && unitAddress == '' && unitPostalCode == '' && unitdomain == '' && unitIndustryId == '') {
                            if (unitcount == 1) {
                                displayMessage(message.add_one_unit);
                                return;
                            }
                            continue;
                        }
                        if (unitLocation == '') {
                            displayMessage(message.unitlocation_required);
                            return;
                        } else if (unitGeographyId == '') {
                            displayMessage(message.unitlocation_invalid);
                            return;
                        } else if (unitCode == '') {
                            displayMessage(message.unitcode_required);
                            return;
                        } else if (unitName == '') {
                            displayMessage(message.unitname_required);
                            return;
                        } else if (unitIndustryId == '' || unitIndustryId == null) {
                            console.log(unitIndustryId)
                            displayMessage(message.industryname_required);
                            return;
                        } else if (unitAddress == '') {
                            displayMessage(message.unitaddress_required);
                            return;
                        } else if (unitPostalCode == '') {
                            displayMessage(message.unitpostal_required);
                            return;
                        } else if (unitdomain == '' || unitdomain == null) {
                            displayMessage(message.domain_required);
                            return;
                        } else {
                            unitarr.push(unitCode);
                            var hash = [];
                            for (var n = unitarr.length; n--;) {
                                if (typeof hash[unitarr[n]] === 'undefined')
                                    hash[unitarr[n]] = [];
                                hash[unitarr[n]].push(n);
                            }
                            var duplicates = [];
                            for (var key in hash) {
                                if (hash.hasOwnProperty(key) && hash[key].length > 1) {
                                    duplicates.push(key);
                                }
                            }

                            if (duplicates == '') {

                                /*for(var ij=0; ij<unitIndustryId.length; ij++){
                                  $.each(industryList, function(k ,val){
                                    var list = {};
                                    if(val["industry_id"] == unitIndustryId[ij] && val["legal_entity_id"] == leIdValue){
                                      list['domain_id'] = val['domain_id'];
                                      list['industry_id'] = val['industry_id'];
                                      unitIndustryIds.push(list);
                                    }
                                  });

                                }
                                console.log("i:"+unitIndustryIds)*/

                                //domains multi select
                                /*var arrayDomainsVal = "";
                                if(unitdomain.indexOf(',')!=-1)
                                {
                                  arrayDomainsVal = unitdomain.split(',');
                                }
                                else
                                {
                                  arrayDomainsVal = unitdomain;
                                }
                                var unitdomains = [];
                                for (var m = 0; m < arrayDomainsVal.length; m++) {
                                  unitdomains.push(parseInt(arrayDomainsVal[m]));
                                }
                                console.log("domains:"+unitdomains)*/
                                if (total_div != i) {
                                    total_div = total_div + 1;
                                }
                                div_arr = mirror.getDivisionDict(parseInt(divIdValue), divNameValue, category, total_div, parseInt(total_units));
                                division_units.push(div_arr);
                                unit = mirror.getUnitDict(parseInt(unitId), unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitdomains, unitIndustryId);

                                units.push(unit);
                            } else {
                                displayMessage(duplicates + ' Unit Code Already Exits!!!');
                                return;
                            }
                        }
                    }
                }
            } else {
                displayMessage(message.add_one_unit);
                return;
            }
        }
        mirror.saveClient(parseInt(client_id), parseInt(bgIdValue), parseInt(leIdValue), parseInt(countryVal), division_units, units, function(error, response) {
            if (error == null) {
                //alert(message.unit_save);
                units_count = [];
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }

    //main loop -- end
});

function resetallfilter() {
    var obj_client = $(".client-drop-down option");
    var clone_client = obj_client.clone();
    clone_client.attr("value", 0);
    clone_client.text("Select");
    clientSelect.append(clone_client);

    busgrpSelect_option_0.remove();
    var obj_bgrp = $(".bgrp-drop-down option");
    var clone_bgrp = obj_bgrp.clone();
    clone_bgrp.attr("value", 0);
    clone_bgrp.text("Select");
    $('#businessgroup-select').append(clone_bgrp);

    var obj_le = $(".le-drop-down option");
    var clone_le = obj_le.clone();
    clone_le.attr("value", 0);
    clone_le.text("Select");
    leSelect.append(clone_le);

    var obj_divi = $(".divi-drop-down option");
    var clone_divi = obj_divi.clone();
    clone_divi.attr("value", 0);
    clone_divi.text("Select");
    $('#division-select').append(clone_divi);
}

function processSearch() {
    c_name = FilterCountry.val().toLowerCase();
    g_name = FilterGroup.val().toLowerCase();
    bg_name = FilterBGroup.val().toLowerCase();
    le_name = FilterLE.val().toLowerCase();
    unit_status = $('.search-status-li.active').attr('value');
    searchList = []
    table = $('.tbody-clientunit-list').find('tr');
    for (var i = 0; i < unitList.length; i++) {
        data = table[i];
        unit_data = unitList[i];
        if (table.length > 0) {
            data_c_name = data.cells[3].innerHTML.toLowerCase();
            data_g_name = data.cells[1].innerHTML.toLowerCase();
            data_bg_name = data.cells[2].innerHTML.toLowerCase();
            data_le_name = data.cells[4].innerHTML.toLowerCase();
            data_is_active = unit_data.is_active;
            if (
                (~data_c_name.indexOf(c_name)) && (~data_g_name.indexOf(g_name)) &&
                (~data_bg_name.indexOf(bg_name)) && (~data_le_name.indexOf(le_name))
            ) {
                if ((unit_status == 'all' || Boolean(parseInt(unit_status)) == data_is_active)) {
                    searchList.push(unit_data);
                }
            }
        } else {
            if ((unit_status == 'all' || Boolean(parseInt(unit_status)) == data_is_active)) {
                searchList.push(unit_data);
            }
        }
    }

    loadClientsList(searchList);
}

function renderControls() {
    //status of the list
    Search_status_ul.click(function(event) {
        Search_status_li.each(function(index, el) {
            $(el).removeClass('active');
        });
        $(event.target).parent().addClass('active');

        var currentClass = $(event.target).find('i').attr('class');
        Search_status.removeClass();
        if (currentClass != undefined) {
            Search_status.addClass(currentClass);
            Search_status.text('');
        } else {
            Search_status.addClass('fa');
            Search_status.text('All');
        }
        processSearch();
    });
}

$(function() {
    initialize();
    renderControls();
});

$('#division-text').on('input', function(e) {
    this.value = isCommon($(this));
});
clientSelect.on('change', function() {
    $('.add-country-unit-list').empty();
    countc = null;
});
bgrpSelect.on('change', function() {
    $('.add-country-unit-list').empty();
    countc = null;
});
leSelect.on('change', function() {
    $('.add-country-unit-list').empty();
    countc = null;
});
Search_status.change(function() {
    processSearch();
});
FilterBox.keyup(function() {
    processSearch();
});
