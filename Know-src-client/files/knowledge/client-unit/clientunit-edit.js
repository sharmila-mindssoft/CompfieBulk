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
var edited_ids = [];
var clientUnitAdd = $('#clientunit-add');
var clientUnitView = $('#clientunit-view');
var showMore_Hit = 0;
var edit_client_id = 0;
var edit_le_id = 0;
var edit_bg_id = 0;
var edit_country_id = 0;

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
    edited_ids = [];
    edit_client_id = clientunitId;
    edit_bg_id = businessgroupId;
    edit_le_id = legalentityId;
    edit_country_id = countryId;
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
    mirror.getClientsEdit(clientunitId, businessgroupId, legalentityId, countryId, showMore_Hit, unitsPerPage, function(error, response) {
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
//show more
$('#btn-clientunit-showmore').click(function() {
    showMore_Hit = showMore_Hit + 1;
    function onSuccess(data) {
        clientdomainList = data.domains_organization_list;
        unitList = data.unit_list;
        //loadFormListUpdate(edit_client_id, edit_bg_id, edit_le_id, edit_country_id);
        $.each(unitList, function(unitkey, unitval) {
            unitval = unitList[unitkey];
            category_name = unitval.category_name;
            if (unitval.client_id == edit_client_id && unitval.country_id == edit_country_id && unitval.legal_entity_id == edit_le_id) {
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
                        //addNewUnitRow_edit('tbody-unit-' + parseInt(returnRow));
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
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getClientsEdit(edit_client_id, edit_bg_id, edit_le_id, edit_country_id, showMore_Hit, unitsPerPage, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
            hideLoader();
        }
    });
});
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

    //country
    if (countryId != '')
        LoadCountry(countryId);

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
                    //addNewUnitRow_edit('tbody-unit-' + parseInt(returnRow));
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
    $('.edit_o_ids-'+division_cnt + '-' + unit_second_cnt).val(orgtypeArray);
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
        if (firstlist.is_active == true){
            displayMessage(message.unit_closed);
        }else{
            unitrow_edit(this, orgtypeArray);
        }
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

// when edit is clicked in unit's last row
function unitfirstrow_edit(e, i_ids) {
    evt = e.className;
    split_evt_spaces = evt.split(' ');
    split_evt_hyphen = split_evt_spaces[5].split('-');
    var countval = split_evt_hyphen[2] + "-" + split_evt_hyphen[3];

    if(le_contract_expiry >= 0 && le_approval > 0){
        $('.labelgeolevels-' + countval).show();
        $('.labelunitlocation-' + countval).show();
        $('.labelunitcode-' + countval).show();

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

        $('.domainselected-' + countval).multiselect('rebuild');
        $('.orgtypeselected-' + countval).multiselect('rebuild');

        $('.domainselected-' + countval).parent('span').show();
        $('.orgtypeselected-' + countval).parent('span').show();

        edited_ids.push($('.unit-id-' + countval).val())
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

// when edit is clicked in unit's other rows
function unitrow_edit(e, i_ids) {
    evt = e.className;
    split_evt_spaces = evt.split(' ');
    split_evt_hyphen = split_evt_spaces[5].split('-');
    var countval = split_evt_hyphen[2] + "-" + split_evt_hyphen[3];
    //table_td = $('.tbody-unit-' + split_evt_hyphen[2]).find('tr:eq('+split_evt_hyphen[3]+')');
    $('.division-new-' + countval).hide();
    $('.division-existing-' + countval).hide();

    $('.glevel-' + countval).hide();
    $('.labelgeolevels-' + countval).show();
    $('.labelgeolevels-' + countval).text($('.labelgeolevels-'+countval).text());

    $('.unitlocation-' + countval).hide();
    $('.full-location-list-' + countval).hide();
    $('.labelunitlocation-' + countval).show();
    $('.labelunitlocation-' + countval).text($('.labelunitlocation-'+countval).text());

    $('.unit-code-' + countval).hide();
    $('.labelunitcode-' + countval).text($('.labelunitcode-'+countval).text());
    $('.labelunitcode-' + countval).show();

    var a = $('.labelunitname-' + countval).text();
    $('.unit-name-' + countval).val(a);
    $('.unit-name-' + countval).show();
    $('.labelunitname-' + countval).hide();

    $('.unit-address-' + countval).val($('.labelunitaddress-' + countval).text());
    $('.unit-address-' + countval).show();
    $('.labelunitaddress-' + countval).hide();

    $('.postal-code-' + countval).val($('.labelpostcode-' + countval).text());
    $('.postal-code-' + countval).show();
    $('.labelpostcode-' + countval).hide();

    var domainsListArray = $('.domain-' + countval).val();
    $('.domainselected-' + countval).val(domainsListArray.length + ' Selected');
    loadDomains(countval,domainsListArray);

    var orgtypeArray = $('.edit_o_ids-' + countval).val();
    $('.orgtypeselected-' + countval).val(orgtypeArray.length + ' Selected');
    industrytype('industry-' + countval, orgtypeArray);

    $('.orgtypeselected-' + countval).on('change', function(e) {
        checkUnassignedOrg(e);
        log_units_count(e);
    });
    $('.domainselected-' + countval).on('change', function(e) {
        log_units_count(e);
        checkAssignedUnits(e);
    });
    $('.domainselected-' + countval).show();
    $('.ul-domain-list-' + countval).show();
    $('.labeldomain-' + countval).hide();

    $('.orgtypeselected-' + countval).show();
    $('.ul-orgtype-list-' + countval).show();
    $('.labelorganization-' + countval).hide();

    $('.activedclass-' + countval).text('Active');
    $('.approveclass-' + countval).text('Pending');

    $('.unit-name-' + countval).on('input', function(e) {
        this.value = isCommon($(this));
    });
    $('.unit-address-' + countval).on('input', function(e) {
        this.value = isCommon_Address($(this));
    });
    $('.postal-code-' + countval).on('input', function(e) {
        this.value = isNumbers($(this));
    });

    $('.delete-icon-' + countval).show();
    $('.edit-icon-' + countval).hide();

    //loadDomains();
    //industrytype('industry-' + countval, i_ids );

    $('.domainselected-' + countval).multiselect('rebuild');
    $('.orgtypeselected-' + countval).multiselect('rebuild');

    $('.domainselected-' + countval).parent('span').show();
    $('.orgtypeselected-' + countval).parent('span').show();
    console.log("1:"+edited_ids)
    if(edited_ids.length > 0){
        var occur = -1;
        for(var i=0;i<edited_ids.length;i++)
        {
            if(edited_ids[i] == (countval+"-"+$('.unit-id-' + countval).val())){
                occur = 1;
                break;
            }
        }
        if(occur < 0){
            edited_ids.push(countval+"-"+$('.unit-id-' + countval).val());
        }
    }
    else {
        edited_ids.push(countval+"-"+$('.unit-id-' + countval).val());
    }
    console.log("2:"+edited_ids)
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

    for(var i=0;i<edited_ids.length;i++){
        if(edited_ids[i] == countval + " - "+ $('.unit-id-' + countval).val()){
            edited_ids.remove(i);
        }
    }
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

// To bind the unit values in the corresponding row
function loadUnitValues_exists(unitval, start_cnt) {
    var u_val = parseInt($('.tbody-unit-' + start_cnt).find('tr').length) + 1;
    $('.unitcnt-' + start_cnt + '-' + 1).val(u_val);
    var unit_second_cnt = $('.unitcnt-' + start_cnt + '-' + 1).val();
    console.log("1:"+unit_second_cnt)
    var divUnitAddRow = $('#templatesUnitRow .table-UnitRow-list .table-unit-row');
    var clone1 = divUnitAddRow.clone();
    var firstlist = unitval;
    var gid = firstlist.geography_id;
    var unitlts = loadupdateunitlocation(gid);
    $('.glevel', clone1).hide();
    for (var i = 0; i < geographyLevelList.length; i++) {
        if (geographyLevelList[i].l_id == unitlts.level_id) {
            $('.labelgeolevels', clone1).text(geographyLevelList[i].l_name);
            $('.labelgeolevels', clone1).addClass("labelgeolevels-" + start_cnt + '-' + unit_second_cnt);
        }
    }
    $('.unitlocation', clone1).hide();
    $('.unitlocation-ids', clone1).val(gid);
    $('.unitlocation-ids', clone1).addClass("unitlocation-ids-" + start_cnt + '-' + unit_second_cnt);

    $('.full-location-list', clone1).hide();
    $('.labelunitlocation', clone1).text(unitlts.gname);
    $('.labelunitlocation', clone1).addClass('labelunitlocation-' + start_cnt + '-' + unit_second_cnt);

    $('.unit-id', clone1).val(firstlist.unit_id);
    $('.unit-id', clone1).addClass('unit-id-' + start_cnt + '-' + unit_second_cnt);
    $('.unit-code', clone1).hide();
    $('.unit-code-', clone1).addClass('unit-code-' + start_cnt + '-' + unit_second_cnt);
    $('.labelunitcode', clone1).text(firstlist.unit_code);
    $('.labelunitcode', clone1).addClass('labelunitcode-' + start_cnt + '-' + unit_second_cnt);

    $('.unit-name', clone1).hide();
    $('.unit-name', clone1).addClass("unit-name-" + start_cnt + '-' + unit_second_cnt);
    $('.labelunitname', clone1).text(firstlist.unit_name);
    $('.labelunitname', clone1).addClass('labelunitname-' + start_cnt + '-' + unit_second_cnt);

    $('.unit-address', clone1).hide();
    $('.unit-address', clone1).addClass("unit-address-" + start_cnt + '-' + unit_second_cnt);
    $('.labelunitaddress', clone1).text(firstlist.address);
    $('.labelunitaddress', clone1).addClass('labelunitaddress-' + start_cnt + '-' + unit_second_cnt);

    $('.postal-code', clone1).hide();
    $('.postal-code', clone1).addClass("postal-code-" + start_cnt + '-' + unit_second_cnt);
    $('.labelpostcode', clone1).text(firstlist.postal_code);
    $('.labelpostcode', clone1).addClass('labelpostcode-' + start_cnt + '-' + unit_second_cnt);

    var domainsListArray = firstlist.domain_ids;
    domain_names = getDomainsName(domainsListArray);
    $('.labeldomain', clone1).text(domain_names);
    $('.labeldomain', clone1).addClass('labeldomain-' + start_cnt + '-' + unit_second_cnt);
    $('.domain', clone1).addClass('domain-' + start_cnt + '-' + unit_second_cnt);
    //$('.domain-' + start_cnt + '-' + unit_second_cnt, clone1).val(domainsListArray);
    $('.domain', clone1).val(domainsListArray);
    $('.assign_cnt', clone1).addClass('assign_cnt-' + start_cnt + '-' + unit_second_cnt);
    $('.assign_cnt-' + start_cnt + '-' + unit_second_cnt).val(firstlist.assign_count);
    $('.domainselected', clone1).addClass('domainselected-' + start_cnt + '-' + unit_second_cnt);
    $('.domainselected-' + start_cnt + '-' + unit_second_cnt, clone1).hide();

    var orgtypeArray = firstlist.i_ids;
    orgn_names = getOrganizationName(orgtypeArray);
    console.log(firstlist.unit_id, domainsListArray, orgtypeArray)
    $('.labelorganization', clone1).text(orgn_names);
    $('.labelorganization', clone1).addClass('labelorganization-' + start_cnt + '-' + unit_second_cnt);
    $('.orgtypeselected').hide();
    $('.orgtypeselected', clone1).addClass('orgtypeselected-' + start_cnt + '-' + unit_second_cnt);
    $('.edit_o_ids', clone1).addClass('edit_o_ids-' + start_cnt + '-' + unit_second_cnt);
    $('.edit_o_ids-' + start_cnt + '-' + unit_second_cnt, clone1).val(orgtypeArray);

    push_domain_orgn(start_cnt + '-' + unit_second_cnt, domainsListArray, orgtypeArray);
    if (firstlist.is_active == true) {
        $('.activedclass', clone1).text('In Active');

    } else {
        var classname = 'imgactivedclass-' + start_cnt + '-' + unit_second_cnt;
        $('.activedclass', clone1).text('Active');

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
    $('.activedclass', clone1).addClass('activedclass-' + start_cnt + '-' + unit_second_cnt);

    if (firstlist.is_approved == 0) {
        $('.approveclass', clone1).text('Pending');
    } else if (firstlist.is_approved == 1) {
        $('.approveclass', clone1).text('Approved');
    } else if (firstlist.is_approved == 2) {
        $('.approveclass', clone1).text('');
        $('.approveclass', clone1).text("Rejected");
        var unit_ctrl = '<span class="fa fa-info-circle text-primary c-pointer" data-toggle="tooltip" title="' + firstlist.remarks + '"></span>';
        $('.approveclass').parent().prepend(unit_ctrl);
        $('[data-toggle="tooltip"]').tooltip();
        $('.tbody-unit-' + start_cnt + ' tr').eq(0).css("color", "rgb(255,0,0)");
    }
    $('.approveclass', clone1).addClass('approveclass-' + start_cnt + '-' + unit_second_cnt);

    $('.edit-icon', clone1).attr('title', 'Edit');
    $('.edit-icon', clone1).addClass('edit-icon-' + start_cnt + '-' + unit_second_cnt);
    $('.edit-icon', clone1).on('click', function() {
        if (firstlist.is_active == true){
            displayMessage(message.unit_closed);
        }else{
            unitrow_edit(this, orgtypeArray);
        }
    });

    $('.delete-icon', clone1).attr('title', 'Close');
    $('.delete-icon', clone1).on('click', function() {
        unitrow_close(this.className);
    });
    $('.delete-icon', clone1).addClass('delete-icon-' + start_cnt + '-' + unit_second_cnt);

    $('.edit-icon-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.delete-icon-' + start_cnt + '-' + unit_second_cnt).hide();
    $('.active_cnt-' + start_cnt + '-' + unit_second_cnt).show();
    if ($("#client-unit-id").val() != "") {
        $('.edit-icon').show();
        $('.edit-icon-' + start_cnt + '-' + unit_second_cnt).show();
    }
    if ($("#client-unit-id").val() == "") {
        $('.edit-icon').hide();
    }

    if($('.total_created_unit').text() == ""){
        $('.total_created_unit').text("1");
    }else{
        $('.total_created_unit').text(parseInt($('.total_created_unit').text()) + 1);
    }

    $('.tbody-unit-' + start_cnt).find('tr:eq(0)').before(clone1);
}