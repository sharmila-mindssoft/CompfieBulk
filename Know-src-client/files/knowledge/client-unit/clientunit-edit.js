//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');
/**
 * Created by Minds on 24/09/2016.
 */
var edit = false;
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
var prev_org_id = 0;
var check_org = false;
var del_row=[];
var le_contract_expiry = 0;
var le_approval = 0;

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

//Edit client Unit  -----------------------------------------------------------------------------------------------
function clientunit_edit(clientunitId, businessgroupId, legalentityId, countryId) {
    isUpdate = true;
    units_count = [];
    edit = true;
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
    $('.fa-search').hide();
    $('.labelcountry').show();
    $('.mandatory').hide();
    $('#add-country-row').hide();
    $('.total_created_unit').text('');
    //$('#division-text').show();
    $('#division-select').hide();
    //$('.division-new').hide();
    //$('.division-existing').hide();
    $('.no-of-units').val('');
    check_org = false;
    addUnitsId = [];
    del_row = [];

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

    for(var le=0;le<legalEntitiesList.length;le++) {
        if(legalEntitiesList[le].legal_entity_id == legalentityId) {
            le_contract_expiry = parseInt(legalEntitiesList[le].le_expiry_days);
            le_approval = legalEntitiesList[le].is_approved;
        }
    }
    function onSuccess(data) {
        clientdomainList = data.domains_organization_list;
        unitList = data.unit_list;
        loadFormListUpdate(clientunitId, businessgroupId, legalentityId, countryId);
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getClientsEdit(clientunitId, businessgroupId, legalentityId, countryId, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}
// Get the group name by its client id
function getGroupName(groupId) {
    var groupName;
    $.each(groupList, function(key, value) {
        if (value.client_id == groupId) {
            groupName = value.group_name;
        }
    });
    return groupName;
}
// Get the business group name by its business group id
function getBusinessGroupName(businessGroupId) {
    var businessgroupName;
    $.each(businessGroupList, function(key, value) {
        if (value.business_group_id == businessGroupId) {
            businessgroupName = value.business_group_name;
        }
    });
    return businessgroupName;
}
// To get Country name from its its list by its ID
function getCountryName(countryId) {
    var countryName;
    $.each(countryFulList, function(key, value) {
        if (value.country_id == countryId) {
            countryName = value.country_name;
        }
    });
    return countryName;
}
// To get Legal entity name from its list by its ID
function getLegalEntityName(legalentityId) {
    var legalEntityName;
    $.each(legalEntitiesList, function(key, value) {
        if (value.legal_entity_id == legalentityId) {
            legalEntityName = value.legal_entity_name;
        }
    });
    return legalEntityName;
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
    if (businessgroupId != '' && businessgroupId != null) {
        loadBusinessGroups(clientunitId);
        $('#businessgroup-update-id').val(businessgroupId);
        $(".labelbusinessgroup").text(getBusinessGroupName(businessgroupId));
        //$('#businessgroup-select option[value = '+businessgroupId+']').attr('selected','selected');
    }

    if (businessgroupId == '' || businessgroupId == null) {
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
    //load_domain_org();

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
                edit = true;
                addcountryrownew();
                loadUnitValues(unitval);
                edit = false;
            } else {
                var rowcnt = 0;
                var division_name;
                var returnRow = 0;
                if (unitval.division_id != '') {
                    division_name = getDivisionName(unitval.division_id);
                }
                //$('.labelcategory-' + parseInt(i + 1) + '-1').show();

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
                    edit = true;
                    addNewUnitRow_edit('tbody-unit-' + parseInt(returnRow));
                    loadUnitValues_exists(unitval, returnRow);
                    edit = false;
                } else {
                    edit = true;
                    addcountryrownew();
                    loadUnitValues(unitval);
                    edit = false;
                }

            }
        }
    });
}
//To find whether division row is created
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

        if ($('.division-name-' + parseInt(i) + '-1').val() == divisionName && $('.category-name-' + parseInt(i) + '-1').val() == categoryName) {
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
                domain_ids.push(d_ids[j]);
            }
        }
        i_ids = unitList[i].i_ids;
        if (i_ids.length > 0) {
            for (var j = 0; j < i_ids.length; j++) {
                org_ids.push(i_ids[j]);
            }
        }
    }

    for (var i = 0; i < domain_ids.length; i++) {

        if (i == 0) {
            //push 0 index of domain id and org id
            units_count.push(domain_ids[i] + '-' + org_ids[i] + '-' + 1);
            //break;
        }
        else{
            match_count = false;
            for (var j = 0; j < units_count.length; j++) {
                var unit_count_val = units_count[j].split("-");
                if (unit_count_val[0] == domain_ids[i] && unit_count_val[1] == org_ids[i]) {
                    units_count[j] = domain_ids[i]+'-'+org_ids[i]+'-'+ (parseInt(unit_count_val[2])+1);
                    match_count = true;
                    break;
                }
            }
            if (match_count == false) {
                units_count.push(domain_ids[i] + '-' + org_ids[i] + '-' + 1);
                //break;
            }
        }
    }

}
// Create empty row and bind the unit values
function loadUnitValues(unitval) {
    var unit_second_cnt = $('.unitcnt-' + division_cnt + '-' + 1).val();
    var firstlist = unitval
    var cid = firstlist.country_id;
    $('.table-addunit-' + division_cnt).hide();
    $('.btn-showmore').show();
    $('.division-id-' + division_cnt + '-' + unit_second_cnt).hide();
    //$('.labeldivision-' + division_cnt + '-' + unit_second_cnt).show();
    if (firstlist.division_id > 0) {
        $('.divisionid-' + division_cnt + '-' + unit_second_cnt).val(firstlist.division_id);
        loadDivision('division-id-' + division_cnt + '-' + unit_second_cnt);
        $('.division-id-' + division_cnt + '-' + unit_second_cnt + ' option[value=' + firstlist.division_id + ']').attr('selected', 'selected');
        division_name = getDivisionName(firstlist.division_id);
        //$('.labeldivision-' + division_cnt + '-' + unit_second_cnt).text(division_name);
        $('.input_business_group-' + division_cnt + '-' + unit_second_cnt).show();
        $('.division-name-' + division_cnt + '-' + unit_second_cnt).show();
        $('.division-name-' + division_cnt + '-' + unit_second_cnt).val(division_name);
        $('.division-existing-'+ division_cnt + '-' + unit_second_cnt).hide();
    } else if (firstlist.division_id == 0) {
        $('.input_business_group-' + division_cnt + '-' + unit_second_cnt).show();
        $('.division-name-' + division_cnt + '-' + unit_second_cnt).show();
        $('.division-name-' + division_cnt + '-' + unit_second_cnt).val("--");
        $('.division-existing-'+ division_cnt + '-' + unit_second_cnt).hide();
        $('.division-name-' + division_cnt + '-' + unit_second_cnt).attr("disabled", true);
    }

    if (firstlist.category_name != null) {
        $('.categoryid-' + division_cnt + '-' + unit_second_cnt).val(firstlist.category_id);
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).val(firstlist.category_name);
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).show();
    } else {
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).val("--");
        $('.category-name-' + division_cnt + '-' + unit_second_cnt).attr("disabled", true);
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
    $('.domain-'+division_cnt + '-' + unit_second_cnt).val(domainsListArray);
    $('.assign_cnt-'+division_cnt + '-' + unit_second_cnt).val(firstlist.assign_count);
    domain_names = getDomainsName(domainsListArray);
    $('.labeldomain-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labeldomain-' + division_cnt + '-' + unit_second_cnt).text(domain_names);
    loadDomains(division_cnt + '-' + unit_second_cnt,domainsListArray);

    var orgtypeArray = firstlist.i_ids;
    $('.orgtypeselected-' + division_cnt + '-' + unit_second_cnt).val(orgtypeArray.length + ' Selected');

    $('.orgtypeselected-' + division_cnt + '-' + unit_second_cnt).hide();
    orgn_names = getOrganizationName(orgtypeArray);
    $('.labelorganization-' + division_cnt + '-' + unit_second_cnt).show();
    $('.labelorganization-' + division_cnt + '-' + unit_second_cnt).text(orgn_names);
    industrytype('industry-' + division_cnt + '-' + unit_second_cnt, orgtypeArray);
    push_domain_orgn(division_cnt + '-' + unit_second_cnt, domainsListArray, orgtypeArray);
    if (firstlist.is_active == true) {
        $('.activedclass-' + division_cnt + '-' + unit_second_cnt).text('In Active');

    } else {
        var classname = 'imgactivedclass-' + division_cnt + '-' + unit_second_cnt;
        $('.activedclass-' + division_cnt + '-' + unit_second_cnt).text('Active');
        var actual_text = $('.active_cnt-' + division_cnt + '-' + 1).text();
        var start = 1;

        if(actual_text == ''){
            $('.active_cnt-' + division_cnt + '-' + 1).text("Active Unit(s) : "+start);
        }
        else
        {
            start = actual_text.split(":")[1].trim();
            summate = parseInt(actual_cnt)+parseInt(1);
            $('.active_cnt-' + division_cnt + '-' + 1).text("Active Unit(s) : "+summate);
        }
    }

    $('.edit-icon-' + division_cnt + '-' + unit_second_cnt).attr('title', 'Edit');
    $('.edit-icon-' + division_cnt + '-' + unit_second_cnt).on('click', function() {
        unitrow_edit(this.className, orgtypeArray);
    });
    $('.delete-icon-' + division_cnt + '-' + unit_second_cnt).attr('title', 'Close');
    $('.delete-icon-' + division_cnt + '-' + unit_second_cnt).on('click', function() {
        unitrow_close(this.className);
    });
    $('.edit-icon-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.delete-icon-' + division_cnt + '-' + unit_second_cnt).hide();
    $('.active_cnt-' + division_cnt + '-' + unit_second_cnt).show();
    if ($("#client-unit-id").val() != "") {
        $('.edit-icon').show();
        // $('.edit-icon').on('click', function() {
        //     unitrow_edit(this.className, orgtypeArray);
        // });
        $('.edit-icon-' + division_cnt + '-' + unit_second_cnt).show();
    }
    if ($("#client-unit-id").val() == "") {
        $('.edit-icon').hide();
    }

//$('.active_cnt-' + division_cnt + '-' + unit_second_cnt).text()
    if (firstlist.is_approved == 0) {
        $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('Pending');

    } else if (firstlist.is_approved == 1) {
        $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('Approved');

    } else if (firstlist.is_approved == 2) {
        $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text('');
        $('.approveclass-' + division_cnt + '-' + unit_second_cnt).text("Rejected");
        var unit_ctrl = '<span class="fa fa-info-circle text-primary c-pointer" data-toggle="tooltip" title="' + firstlist.remarks + '"></span>';
        $('.approveclass-' + division_cnt + '-' + unit_second_cnt).parent().prepend(unit_ctrl);
        $('[data-toggle="tooltip"]').tooltip();
        $('.tbody-unit-' + division_cnt + ' tr').eq(0).css("color", "rgb(255,0,0)");
    }

    //industrytype('industry-' + division_cnt + '-' + unit_second_cnt, orgtypeArray);

    $('.domainselected').parent('span').hide();
    $('.orgtypeselected').parent('span').hide();
}
// To bind the unit values in the corresponding row
function loadUnitValues_exists(unitval, start_cnt) {
    var unit_second_cnt = $('.unitcnt-' + start_cnt + '-' + 1).val();
    var firstlist = unitval

    var cid = firstlist.country_id;
    //load division
    $('.table-addunit-' + division_cnt).hide();
    $('.division-id-' + start_cnt + '-' + unit_second_cnt).hide();
    //$('.labeldivision-' + division_cnt + '-' + unit_second_cnt).show();
    if (firstlist.division_id > 0) {
        $('.divisionid-' + start_cnt + '-' + unit_second_cnt).val(firstlist.division_id);
        loadDivision('division-id-' + start_cnt + '-' + unit_second_cnt);
        $('.division-id-' + start_cnt + '-' + unit_second_cnt + ' option[value=' + firstlist.division_id + ']').attr('selected', 'selected');
        division_name = getDivisionName(firstlist.division_id);
        //$('.labeldivision-' + division_cnt + '-' + unit_second_cnt).text(division_name);
        $('.input_business_group-' + start_cnt + '-' + unit_second_cnt).show();
        $('.division-name-' + start_cnt + '-' + unit_second_cnt).show();
        $('.division-name-' + start_cnt + '-' + unit_second_cnt).val(division_name);
        $('.division-existing-'+ start_cnt + '-' + unit_second_cnt).hide();
    } else if (firstlist.division_id == 0) {
        $('.input_business_group-' + start_cnt + '-' + unit_second_cnt).show();
        $('.division-name-' + start_cnt + '-' + unit_second_cnt).show();
        $('.division-name-' + start_cnt + '-' + unit_second_cnt).val("--");
        $('.division-existing-'+ start_cnt + '-' + unit_second_cnt).hide();
        $('.division-name-' + start_cnt + '-' + unit_second_cnt).attr("disabled", true);
    }

    if (firstlist.category_name != null) {
        $('.categoryid-' + start_cnt + '-' + unit_second_cnt).val(firstlist.category_id);
        $('.category-name-' + start_cnt + '-' + unit_second_cnt).val(firstlist.category_name);
        $('.category-name-' + start_cnt + '-' + unit_second_cnt).show();
    } else {
        $('.category-name-' + start_cnt + '-' + unit_second_cnt).val("--");
        $('.category-name-' + start_cnt + '-' + unit_second_cnt).attr("disabled", true);
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
    $('.domain-'+start_cnt + '-' + unit_second_cnt).val(domainsListArray);
    $('.assign_cnt-'+division_cnt + '-' + unit_second_cnt).val(firstlist.assign_count);
    //$('.domain-' + division_cnt + '-' + unit_second_cnt).hide();
    domain_names = getDomainsName(domainsListArray);
    $('.labeldomain-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labeldomain-' + start_cnt + '-' + unit_second_cnt).text(domain_names);
    loadDomains(start_cnt + '-' + unit_second_cnt,domainsListArray);

    var orgtypeArray = firstlist.i_ids;
    //$('.orgtype-' + division_cnt + '-' + unit_second_cnt).val(orgtypeArray);
    $('.orgtypeselected-' + start_cnt + '-' + unit_second_cnt).val(orgtypeArray.length + ' Selected');

    $('.orgtypeselected-' + start_cnt + '-' + unit_second_cnt).hide();
    orgn_names = getOrganizationName(orgtypeArray);
    $('.labelorganization-' + start_cnt + '-' + unit_second_cnt).show();
    $('.labelorganization-' + start_cnt + '-' + unit_second_cnt).text(orgn_names);
    industrytype('industry-' + start_cnt + '-' + unit_second_cnt, orgtypeArray);

    push_domain_orgn(start_cnt + '-' + unit_second_cnt, domainsListArray, orgtypeArray);
    $('.domainselected').parent('span').hide();
    $('.orgtypeselected').parent('span').hide();

    if (firstlist.is_active == true) {
        $('.activedclass-' + start_cnt + '-' + unit_second_cnt).text('In Active');

    } else {
        var classname = 'imgactivedclass-' + start_cnt + '-' + unit_second_cnt;
        $('.activedclass-' + start_cnt + '-' + unit_second_cnt).text('Active');

        var actual_text = $('.active_cnt-' + start_cnt + '-' + 1).text();
        var start = 1;
        if(actual_text == ''){
            $('.active_cnt-' + start_cnt + '-' + 1).text("Active Unit(s) : "+start);
        }
        else
        {
            start = actual_text.split(":")[1].trim();
            summate = parseInt(start)+parseInt(1);
            $('.active_cnt-' + start_cnt + '-' + 1).text("Active Unit(s) : "+summate);
        }
    }

    if (firstlist.is_approved == 0) {
        $('.approveclass-' + start_cnt + '-' + unit_second_cnt).text('Pending');
    } else if (firstlist.is_approved == 1) {
        $('.approveclass-' + start_cnt + '-' + unit_second_cnt).text('Approved');
    } else if (firstlist.is_approved == 2) {
        $('.approveclass-' + start_cnt + '-' + unit_second_cnt).text('');
        $('.approveclass-' + start_cnt + '-' + unit_second_cnt).text("Rejected");
        var unit_ctrl = '<span class="fa fa-info-circle text-primary c-pointer" data-toggle="tooltip" title="' + firstlist.remarks + '"></span>';
        $('.approveclass-' + start_cnt + '-' + unit_second_cnt).parent().prepend(unit_ctrl);
        $('[data-toggle="tooltip"]').tooltip();
        $('.tbody-unit-' + start_cnt + ' tr').eq(0).css("color", "rgb(255,0,0)");
    }

    $('.edit-icon-' + start_cnt + '-' + unit_second_cnt).attr('title', 'Edit');
    $('.edit-icon-' + start_cnt + '-' + unit_second_cnt).on('click', function() {
        unitrow_edit(this.className, orgtypeArray);
    });
    $('.delete-icon-' + start_cnt + '-' + unit_second_cnt).attr('title', 'Close');
    $('.delete-icon-' + start_cnt + '-' + unit_second_cnt).on('click', function() {
        unitrow_close(this.className);
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
// when edit is clicked in unit row
function unitrow_edit(evt, i_ids) {
    split_evt_spaces = evt.split(' ');
    split_evt_hyphen = split_evt_spaces[5].split('-');
    var countval = split_evt_hyphen[2] + "-" + split_evt_hyphen[3];
    if(le_contract_expiry >= 0 && le_approval > 0){
        $('.glevel-' + countval).show();
        $('.labelgeolevels-' + countval).hide();
        $('.glevel-' + countval).attr("disabled", true);

        $('.unitlocation-' + countval).show();
        $('.unitlocation-ids-' + countval).show();
        $('.full-location-list-' + countval).show();
        $('.labelunitlocation-' + countval).hide();
        $('.unitlocation-' + countval).attr("disabled", true);

        $('.unit-code-' + countval).show();
        $('.labelunitcode-' + countval).hide();
        $('.unit-code-' + countval).attr("disabled", true);

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

        //loadDomains();
        //industrytype('industry-' + countval, i_ids );

        $('.domainselected-' + countval).multiselect('rebuild');
        $('.orgtypeselected-' + countval).multiselect('rebuild');

        $('.domainselected-' + countval).parent('span').show();
        $('.orgtypeselected-' + countval).parent('span').show();
    }
    else {
        if(le_contract_expiry < 0) {
            displayMessage(message.legal_entity_expired);
        }
        else if(le_approval == 0){
            displayMessage(message.legal_entity_approval)
        }
    }
}
// When close icon clicked in edit/ add unit row
function unitrow_close(evt) {
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
//to remove rows in add mode
function unitrow_remove(evt) {
    var msgstatus = message.unit_delete;
    confirm_alert(msgstatus, function(isConfirm){
        if(isConfirm){
            split_evt_spaces = evt.split(' ');
            split_evt_hyphen = split_evt_spaces[5].split('-');
            var countval = split_evt_hyphen[2] + "-" + split_evt_hyphen[3];
            if (unitcodeautogenerateids != null){
                if ($('.unit-code-'+countval).val().indexOf(unitcodeautogenerateids) >= 0)
                    unitcodeautogenerateids = unitcodeautogenerateids - 1;
            }

            unitcnt_val = $('.unitcnt-'+split_evt_hyphen[2] +"-1").val();
            delete_row = 0;
            del_row.push(countval);
            //delete_row = parseInt($('.tbody-unit-' + split_evt_hyphen[2] + ' tr').length)-parseInt(unitcnt_val);
            delete_row = $('.remove-icon-'+countval).parent().parent().index();
            if(delete_row < 0)
                delete_row = 0;

            $('.tbody-unit-' + split_evt_hyphen[2] + ' tr').eq(delete_row).remove();
            division_cnt = division_cnt - 1;
            //unitcodeautogenerateids = unitcodeautogenerateids -1;
            if(division_cnt == 0){
                division_cnt = 1;
            }
            $('.divisioncnt-' +split_evt_hyphen[2]+"-"+1).val(division_cnt);

            if((parseInt(unitcnt_val)-1) == 0)
            {
                $('.unitcnt-' + split_evt_hyphen[2] +"-1").val(0);
            }
            else
            {
                $('.unitcnt-' + split_evt_hyphen[2] +"-1").val(parseInt(unitcnt_val));
            }
            if($('.total_created_unit').text() == ""){
                $('.total_created_unit').text("1");
            }else{
                $('.total_created_unit').text(parseInt($('.total_created_unit').text()) - 1);
            }

            for(var i=0;i<units_count.length;i++){
                if(units_count[i].row == countval) {
                    units_count[i].u_count = 0;
                }
            }
        }
    });
}
// Add new unit row during edit mode
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

    /*$('.edit-icon-' + countval + '-' + unitval).attr('title', 'Edit');

    $('.delete-icon-' + countval + '-' + unitval).attr('title', 'Close');
    $('.delete-icon-' + countval + '-' + unitval).on('click', function() {
        unitrow_close(this.className);
    });

    $('.edit-icon-' + countval + '-' + unitval).hide();
    $('.delete-icon-' + countval + '-' + unitval).hide();*/
    //$('.rejected-icon-' + countval + '-' + unitval).hide();

    if ($('#client-unit-id').val() > 0) {
        if($('.unit-id-' + division_cnt + '-' + unitval).val() == ''){
            $('.edit-icon-' + division_cnt + '-' + unitval).hide();
            $('.delete-icon-' + division_cnt + '-' + unitval).attr('title', 'Close');
            $('.delete-icon-' + division_cnt + '-' + unitval).on('click', function() {
                unitrow_close(this.className);
            });
            $('.delete-icon-' + division_cnt + '-' + unitval).hide();
            $('.remove-icon-' + division_cnt + '-' + unitval).show();
            $('.remove-icon-' + division_cnt + '-' + unitval).attr('title', 'Remove');
            $('.remove-icon-' + division_cnt + '-' + unitval).on('click', function() {
                unitrow_remove(this.className);
            });
        }
        else{
            $('.edit-icon-' + division_cnt + '-' + unitval).show();
            $('.delete-icon-' + division_cnt + '-' + unitval).hide();
            $('.remove-icon-' + division_cnt + '-' + unitval).hide();
        }
        $('.division-new-' + division_cnt+ '-' + unitval).hide();
        $('.division-existing-' + division_cnt+ '-' + unitval).hide();
    }
    else{
        $('.edit-icon').hide();
        $('.remove-icon-' + division_cnt + '-' + unitval).attr('title', 'Remove');
        $('.remove-icon-' + division_cnt + '-' + unitval).on('click', function() {
            unitrow_remove(this.className);
        });
        $('.remove-icon-' + division_cnt + '-' + unitval).show();
        $('.division-new-' + division_cnt+ '-' + unitval).show();
        $('.division-existing-' + division_cnt+ '-' + unitval).hide();
    }
    if($('.total_created_unit').text() == ""){
        $('.total_created_unit').text("1");
    }else{
        $('.total_created_unit').text(parseInt($('.total_created_unit').text()) + 1);
    }
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

    $('.orgtypeselected-' + countval + '-' + unitval).on('change', function(e) {
        checkUnassignedOrg(e);
        log_units_count(e);
    });
    $('.domainselected-' + division_cnt + '-' + unitval).on('change', function(e) {
        log_units_count(e);
        checkAssignedUnits(e);
        //industrytype('industry-' + division_cnt + '-' + unitval, []);
    });
    //loadDomains();
    $('.orgtypeselected-' + division_cnt + '-' + 1).multiselect('rebuild');
    //industrytype('industry-' + countval + '-' + unitval, []);

    $('.domainselected').parent('span').hide();
    $('.orgtypeselected').parent('span').hide();
}