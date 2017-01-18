//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterDomain = $('#search-domain-name');
var FilterOrgn = $('#search-organization-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');
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
var del_row=[];
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

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

// Initialized to get the filter records from DB
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
        displayMessage(error);
    }
    displayLoader();
    mirror.getClients('view', function(error, response) {
        if (error == null) {
            onSuccess(response);
            hideLoader();
        } else {
            onFailure(error);
            hideLoader();
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
            $('.status-text', clone).text("Active");
        } else {
            $('.status-text', clone).text("In Active");
        }

        $('.tbody-clientunit-list').append(clone);
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
// To get division name from its list by its ID
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
//Add Button EVent-------------------------------------------------------------------------------------------------
$('#btn-clientunit-add').click(function() {
    isUpdate = false;
    edit = false;
    units_count = [];
    division_cnt = 0;
    clientUnitAdd.show();
    clientUnitView.hide();
    clientSelect.show();
    bgrpSelect.show();
    leSelect.show();
    $('#country-name').show();
    $('.fa-search').show();
    $('#division-select').show();
    $('.division-id').show();
    $('.labeldivision').hide();
    groupSelect_option_no.attr('disabled', false);
    busgrpSelect_option_no.attr('disabled', false);
    entitySelect_option_no.attr('disabled', false);
    $('.labelgroup').hide();
    $('.labelgroup').text('');
    $('.labelbusinessgroup').hide();
    $('.labelentity').hide();
    $('.labelcountry').hide();
    $('.mandatory').show();
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
    initialize();
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
// On change of client group will reset other filters
$("#group-select").on("change", function(){
    if($(this).val() == ""){
        $("#businessgroup-select option:gt(0)").remove();
    }
    else{
        $("#businessgroup-select").empty();
        var obj_bgrp = $(".bgrp-drop-down option");
        var clone_bgrp = obj_bgrp.clone();
        clone_bgrp.attr("value", 0);
        clone_bgrp.text("Select");
        $('#businessgroup-select').append(clone_bgrp);
        $('#country-name').val('');
        $('#entity-select').empty();
        var obj_le = $(".le-drop-down option");
        var clone_le = obj_le.clone();
        clone_le.attr("value", 0);
        clone_le.text("Select");
        leSelect.append(clone_le);
        loadBusinessGroups();
    }
});
//Load Business Groups  ---------------------------------------------------------------------------------------------
function loadBusinessGroups() {
    var groupId = clientSelect.val();
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
// On change of business group will reset the child filters
$("#businessgroup-select").on("change", function(){
    $('#country-name').val('');
    $('#entity-select').empty();
    var obj_le = $(".le-drop-down option");
    var clone_le = obj_le.clone();
    clone_le.attr("value", 0);
    clone_le.text("Select");
    leSelect.append(clone_le);
});
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
    $('#entity-select').empty();
    var obj_le = $(".le-drop-down option");
    var clone_le = obj_le.clone();
    clone_le.attr("value", 0);
    clone_le.text("Select");
    leSelect.append(clone_le);
    loadLegalEntity();
}
// Arrow key functionality
function onArrowKey_Client(e, ac_item, multipleselect, callback) {
    var ccount;
    if(multipleselect.indexOf('unit') >=0){
        ccount = multipleselect.split(",")[1];
    }
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
            var ac_id = $('.' + ac_item + ' li:eq(' + chosen + ')').attr('id');
            var ac_name = $('.' + ac_item + ' li:eq(' + chosen + ')').text();
            for (var geography in geographyList) {
                if (geographyList[geography].geography_id == parseInt(ac_id)) {
                    mappingname = geographyList[geography].mapping;
                    $('.full-location-list' + ccount).html(mappingname);
                }
            }
            var elem = "<li id="+ac_id+">"+ac_name+"</li>";
            $('.auto-complete-unit-location').css('display', 'none');
            activate_unitlocaion(elem,ccount,mappingname);
        }

        return false;
    }
}
// Loads the countries in the list
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
        var ctry_list = [];
        if (textval.length > 0) {
            for (var i in countries) {
                if (~countries[i].country_name.toLowerCase().indexOf(textval.toLowerCase())) {
                    if (bgrpId > 0) {
                        if (countries[i].client_id == groupId && countries[i].business_group_id == bgrpId) {
                            var ul_list = document.getElementById("ac-country");
                            var li_list = ul_list.getElementsByTagName("li");
                            var occur = -1;
                            for(var j=0;j<li_list.length;j++){
                                occur = li_list[j].textContent.indexOf(countries[i].country_name)
                            }
                            if(occur < 0){
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
                    } else {
                        if (countries[i].client_id == groupId) {
                            var ul_list = document.getElementById("ac-country");
                            var li_list = ul_list.getElementsByTagName("li");
                            var occur = -1;
                            for(var j=0;j<li_list.length;j++){
                                occur = li_list[j].textContent.indexOf(countries[i].country_name)
                            }
                            if(occur < 0){
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
    var countryId = $('#country-id').val();
    if (businessGroupId == 0) {
        businessGroupId = null;
    }
    if (businessGroupId != null && clientId != '' && countryId != '') {
        $('#entity-select').find('option:gt(0)').remove();
        $.each(legalEntitiesList, function(key, value) {
            if (value.client_id == clientId && value.business_group_id == businessGroupId &&
                value.country_id == countryId) {
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
    if (businessGroupId == null && clientId != 0 && countryId != '') {
        $('#entity-select').find('option:gt(0)').remove();
        //$('#division-select').find('option:gt(0)').remove();
        $.each(legalEntitiesList, function(key, value) {
            if (value.client_id == clientId && value.country_id == countryId) {
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
// Add new unit under a division/ category
function addcountryrow() {
    clearMessage();
    edit = false;
    var groupId = clientSelect.val();
    var businessgroupid = bgrpSelect.val();
    var lentityId = leSelect.val();
    var countryVal = $('#country-id').val();
    if (groupId == '' && $('#client-unit-id').val() == '') {
        displayMessage(message.group_required);
        return false;
    }
    else if (countryVal == '' && ($('.labelcountry').text() == '')) {
        displayMessage(message.country_required);
        return false;
    }
    else if (lentityId == '' && ($('.labelentity').text() == '')) {
        displayMessage(message.legalentity_required);
        return false;
    }
    else{
        $('.add-country-unit-list').show();
        addcountryrownew();
    }
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
    $('.domain-selectbox-view', clone).addClass('domain-selectbox-view-' + division_cnt + '-' + 1);
    $('.ul-domain-list', clone).addClass('ul-domain-list-' + division_cnt + '-' + 1);
    $('.labeldomain', clone).addClass('labeldomain-' + division_cnt + '-' + 1)
    $('.orgtype-list', clone).addClass('orgtype-list-' + division_cnt + '-' + 1);
    $('.orgtypeselected', clone).addClass('orgtypeselected-' + division_cnt + '-' + 1);
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
    if ($('#client-unit-id').val() > 0) {

        $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).attr('title', 'Edit');
        $('.edit-icon', clone).on('click', function() {
            var orgtypeArray = $('.orgtypeselected-' + division_cnt + '-' + 1, clone).val();
            unitrow_edit(this.className, orgtypeArray);
        });
        $('.division-new-' + division_cnt + '-' + 1, clone).hide();
        $('.division-existing-' + division_cnt + '-' + 1).hide();
        if(edit == false){
            console.log("here")
            $('.domainselected-' + division_cnt + '-' + 1).multiselect('rebuild');
            $('.orgtypeselected-' + division_cnt + '-' + 1).multiselect('rebuild');

            $('.domainselected-' + division_cnt + '-' + 1).parent('span').show();
            $('.orgtypeselected-' + division_cnt + '-' + 1).parent('span').show();
        }
    }
    else
    {
      $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).hide();
      $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).show();
      $('.division-new', clone).show();
        $('.division-existing-' + division_cnt + '-' + 1).hide();
    }
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
    $('.edit-icon-' + division_cnt + '-' + 1).hide();
    $('.divisioncnt-' + division_cnt + '-' + 1).val(division_cnt);
    $('.unitcnt-' + division_cnt + '-' + 1).val(1);
    if ($("#client-unit-id").val() == "") {
        loadDomains(division_cnt + '-' + 1,null);
        $('.orgtypeselected-' + division_cnt + '-' + 1).multiselect('rebuild');
    }

    if ($('.unitcode-checkbox-' + division_cnt).is(':checked')) {
        console.log("code:1-"+get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids))
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
    $('.domainselected',clone).on('change', function(e) {
        industrytype('industry-' + division_cnt + '-' + 1, []);
    });
    $('.orgtypeselected',clone).on('change', function(e) {
        log_units_count(e,division_cnt + '-' + 1);
    });
}
//Add Unit for individual Rows---------------------------------------------------------------------------------
function log_units_count(e,classval) {
    var domain_id = $('.domainselected-' + classval).val();
    var org_id = $('.orgtypeselected-' + classval).val();
    if (units_count.length > 0) {
        for (var i = 0; i < units_count.length; i++) {
            var split_unit = units_count[i].split("-");
            if (domain_id == split_unit[0] && org_id == split_unit[1]) {
                var assignedUnits = getOrgCount(domain_id, org_id);
                if (assignedUnits <= parseInt(split_unit[2])) {
                    var msgstatus = message.unit_remove;
                    confirm_alert(msgstatus, function(isConfirm){
                    if(isConfirm){
                        var index = parseInt(classval.split("-")[1]);
                        if (index == 1) {
                            var rowIndx = index - 1;
                            $('.tbody-unit-' + division_cnt + ' tr').eq(rowIndx).remove();
                        } else {
                            index = parseInt(classval.split("-")[0]);
                            var rowIndx = 0;
                            if (parseInt($('.tbody-unit-' + index + ' tr').length) > 1) {
                            }
                            $('.tbody-unit-' + index + ' tr').eq(rowIndx).remove();
                        }
                        var countval =classval.split("-")[0];
                        $('.unitcnt-' + countval + '-' + 1).val(parseInt($('.unitcnt-' + countval + '-' + 1).val()) -1);
                      e.preventDefault();
                    }
                    else{
                        prev_org_id = org_id;
                        check_org = true;
                    }
                  });
                } else if (parseInt(assignedUnits) > parseInt(split_unit[2])) {
                    units_count[i] = domain_id + '-' + org_id + '-' + (parseInt(split_unit[2]) + 1);
                }
            }
        }
    } else {

        units_count.push(domain_id + '-' + org_id + '-' + 1);
    }
}
// Get the unit count under a domain and organization
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
// Checks the stored unit count under a domain and organization - to prompt user
function check_previous_orgn(evt) {

    if (check_org == true) {
        var org_bool = false;
        var unitno = $('.unitcnt-' + division_cnt + '-' + 1).val();
        var org_id = $('.orgtypeselected-' + division_cnt + '-' + parseInt(unitno - 1)).val();
        for(var i=0;i<org_id.length;i++){
            if(org_id[i] == prev_org_id){
                org_bool = true;
            }
        }
        if (org_bool == true) {
            var msgstatus = message.unit_remove;
            displayMessage(msgstatus);
            var index = parseInt($('.tbody-unit-' + division_cnt + ' tr').parent().index())+1;
            $('.tbody-unit-' + division_cnt + ' tr').eq(0).remove();
            $('.unitcnt-' + division_cnt + '-' + 1).val(parseInt($('.unitcnt-' + division_cnt + '-' + 1).val()) -1);

        } else {
            check_org = false;
            addNewUnitRow(evt);
        }
    } else {
        addNewUnitRow(evt);
    }
}
// To add new unit rows under division category
function addNewUnitRow(str) {
    var lastIndexOf_hyphen = str.lastIndexOf('-');
    var countval = str.substring((lastIndexOf_hyphen + 1), (lastIndexOf_hyphen + 2));
    var table_tr = null;
    var unitval = parseInt($('.unitcnt-' + countval + '-' + 1).val()) + 1;
    $('.unitcnt-' + countval + '-' + 1).val(unitval);

    if(parseInt($('.tbody-unit-' + countval).find('tr').length) > 0){
        var divUnitAddRow = $('#templatesUnitRow').find('tr:eq(0)');
        var clone1 = divUnitAddRow.clone();

        $('.tbody-unit-' + countval).find('tr:eq(0)').before(clone1);
        table_tr = $('.tbody-unit-' + countval).find('tr:eq(0)');
    }
    else{
        var divUnitAddRow = $('#templatesUnitRow').find('tr:eq(0)');
        var clone1 = divUnitAddRow.clone();

        $('.tbody-unit-' + countval).append(clone1);
        table_tr = $('.tbody-unit-' + countval);
    }

    table_tr.find('td').find('input,select,span,div,ul,i').each(function() {
        $(this).attr({
            'class': function(_, lastClass) {
                return $(this).attr('class').split(' ').pop() + ' ' + $(this).attr('class') + '-' + division_cnt + '-' + unitval },
        });
    });
    if(edit == false){
        loadDomains(division_cnt + '-' + unitval,null);
    }

    $('.sno-' + division_cnt + '-' + unitval).text(unitval);
    if ($('.unitcode-checkbox-' + countval).is(':checked')) {
        console.log("code:2-"+get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids))
        console.log("code-cnt:"+countval)
        $('.unit-code-' + division_cnt + '-' + unitval).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
        unitcodeautogenerateids++;
    }
    $('.activedclass-' + division_cnt + '-' + unitval).text('Active');
    $('.approveclass-' + division_cnt + '-' + unitval).text('Pending');

    if ($('#client-unit-id').val() > 0) {
        if($('.unit-id-' + division_cnt + '-' + unitval).val() == ''){
            $('.edit-icon-' + division_cnt + '-' + unitval).hide();
            $('.delete-icon-' + division_cnt + '-' + unitval).attr('title', 'Close');
            $('.delete-icon-' + division_cnt + '-' + unitval).on('click', function() {
                unitrow_close(this.className);
            });
            $('.delete-icon-' + division_cnt + '-' + unitval).show();
        }
        else{
            $('.edit-icon-' + division_cnt + '-' + unitval).show();
        }
        $('.division-new-' + division_cnt+ '-' + unitval).hide();
        $('.division-existing-' + division_cnt+ '-' + unitval).hide();
    }
    else{
        $('.edit-icon').hide();
        $('.delete-icon-' + division_cnt + '-' + unitval).attr('title', 'Close');
        $('.delete-icon-' + division_cnt + '-' + unitval).on('click', function() {
            unitrow_close(this.className);
        });
        $('.delete-icon').show();
        $('.division-new-' + division_cnt+ '-' + unitval).show();
        $('.division-existing-' + division_cnt+ '-' + unitval).hide();
    }
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
    $('.orgtypeselected-' + division_cnt + '-' + unitval).on('change', function(e) {
        log_units_count(e,division_cnt + '-' + unitval);
    });
    $('.domainselected-' + division_cnt + '-' + unitval).on('change', function(e) {
        industrytype('industry-' + division_cnt + '-' + unitval, []);
    });
    $('.orgtypeselected-' + division_cnt + '-' + unitval).multiselect('rebuild');
}
// To pad unit codes
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
// Unit code auto generation
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
// Unit code auto generation
function unitcodeautogenerate(auto_generate_initial_value) {
    //unitcodeautogenerateids = null;
    if (unitcodeautogenerateids == null || unitcodeautogenerateids == ''){
        unitcodeautogenerateids = auto_generate_initial_value;
    }
    if ($('.labelgroup').text().trim() == '') {
        //unitcodeautogenerateids = auto_generate_initial_value;
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
        //unitcodeautogenerateids = auto_generate_initial_value;
        var sno = [];
        if ($('.unitcode-checkbox').is(':checked')) {
            var groupname = $.trim($('.labelgroup').text());
            var groupname = groupname.replace(' ', '');
            get2CharsofGrouplower = groupname.slice(0, 2);
            get2CharsofGroup = get2CharsofGrouplower.toUpperCase();
            var flag = 0;
            $('.add-country-unit-list .unit-code').each(function(i) {
                console.log("prev:"+$(this).val())
                if ($(this).val() == '') {
                    console.log("prev1:"+$(this).val())
                    $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    unitcodeautogenerateids++;
                }
                else {
                    console.log("fhdgf<h")
                    //$(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    //unitcodeautogenerateids++;
                }
            });
        } else {
            $('.add-country-unit-list .unit-code').each(function(i) {
                if ($(this).val() == '') {
                    console.log("dsvvsjh")
                 $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    unitcodeautogenerateids++;
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
        lentityId = $('#legalentity-update-id').val();
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
// To add/ cancel new division
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
        loadDivision('division-id'+countval);
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
            {
                clone.attr("value", level_id);
                clone.text(level_name);
                $('.' + lastClass).append(clone);
            }
        });
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
    var parentname='';
    $('.unitlocation' + ccount).val(checkname);
    $('.unitlocation-ids' + ccount).val(checkval);
    for (var geography in geographyList) {
        if (geographyList[geography].geography_id == parseInt(checkval)) {
            parentname = geographyList[geography].mapping;
        }
    }
    $('.full-location-list' + ccount).html(parentname);
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
        onArrowKey_Client(e, 'ac-textbox', 'unit,'+countval, function(val) {
            activate_unitlocaion(this, countval, val);
        });
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
                if(domain_names.length == 0){
                    domain_names.push(domainList[j].domain_name);
                    break;
                }
                else{
                    var occur = false;
                    for(var k=0;k<domain_names.length;k++){
                        if(domain_names[k] == domainList[j].domain_name){
                            occur = true;
                            break;
                        }
                    }
                    if(occur == false){
                        domain_names.push(domainList[j].domain_name);
                        //break;
                    }
                }
            }
        }
    }
    return domain_names;
}

//load domains
function loadDomains(ccount,selected_arr) {
    var second_cnt = $('.unitcnt-' + division_cnt + '-' + 1).val();
    var d_ctrl = $('.domainselected-' + ccount);
    d_ctrl.empty();
    var editorgtypeval = [];
    var getClientid;
    if (($('#client-unit-id').val() == '') || ($('#client-unit-id').val() == 0)) {
        getClientid = $('#group-select').val();
    } else {
        getClientid = $('#client-unit-id').val();
    }
    if ($('#client-unit-id').val() == 0){// || $('.unit-id-'+division_cnt+'-'+$(".unitcnt-" + division_cnt + "-" + 1).val()).val() == '') {
        var domains = domainList;
        var lentityId = leSelect.val();
        var optText = "";
        var d_arr = [];
        $.each(domains, function(key, value) {
            if (lentityId == domains[key].legal_entity_id) {
                var occur = false;
                if(d_arr.length == 0){
                    d_arr.push(domains[key].domain_id)
                }
                else
                {
                    for(var i=0;i<d_arr.length;i++){
                        if(d_arr[i] == domains[key].domain_id){
                            occur = true;
                        }
                    }
                    if(occur == false){
                        d_arr.push(domains[key].domain_id)
                    }
                }

                if(occur == false){
                    optText = optText + '<option value="'+domains[key].domain_id+'" >'+domains[key].domain_name+'</option>';
                }
            }
        });
        d_ctrl.html(optText);
    } else {
        var domains = domainList;
        var lentityId = $(".labelentity").data('id');
        var optText = "";
        var d_arr = [];
        $.each(domains, function(key, value) {
            editorgtypeval = selected_arr;
            var selectorgtypestatus = '';
            if(editorgtypeval != null && editorgtypeval != "undefined"){
                for (var j = 0; j < editorgtypeval.length; j++) {
                    if (editorgtypeval[j] == domains[key].domain_id) {
                        selectorgtypestatus = 'selected';
                    }
                }
            }

            if (lentityId == domains[key].legal_entity_id) {
                var sel = "selected";
                var occur = false;

                if(d_arr.length == 0){
                    d_arr.push(domains[key].domain_id)
                }
                else
                {
                    for(var i=0;i<d_arr.length;i++){
                        if(d_arr[i] == domains[key].domain_id){
                            occur = true;
                        }
                    }
                    if(occur == false){
                        d_arr.push(domains[key].domain_id)
                    }
                }

                if(occur == false){
                    if(editorgtypeval == null && editorgtypeval == "undefined"){
                        optText = optText + '<option value="'+domains[key].domain_id+'">'+domains[key].domain_name+'</option>';
                    }
                    else
                        optText = optText + '<option value="'+domains[key].domain_id+'" '+selectorgtypestatus+' >'+domains[key].domain_name+'</option>';
                }
            }
        });
        d_ctrl.html(optText);
    }
    d_ctrl.multiselect('rebuild');
}
//load industry under domain
function industrytype(classval, selected_arr) {
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
    var editorgtypeval = [];

    if (lentityId > 0) {
        if ($('#client-unit-id').val() == 0 || $('#client-unit-id').val() == '') {
            var domains = domainList;
            var optText = "";
            for (var i in domains) {
                if (lentityId == domains[i].legal_entity_id && domain_id == domains[i].domain_id) {
                    var orgtypeId = parseInt(domains[i].industry_id);
                    var orgtypeName = domains[i].industry_name;
                    optText = optText + '<option value="'+orgtypeId+'" >'+orgtypeName+'</option>';
                }
            }
            $('.orgtypeselected' + countval).html(optText);
        } else {
            editorgtypeval = selected_arr
            var domains = domainList;
            var optText = "";
            for (var i in domains) {
                var selectorgtypestatus = '';
                if(editorgtypeval != null && editorgtypeval != "undefined"){
                    for (var j = 0; j < editorgtypeval.length; j++) {
                        if (editorgtypeval[j] == domains[i].industry_id) {
                            selectorgtypestatus = 'selected';
                        }
                    }
                }
                if (lentityId == domains[i].legal_entity_id && domain_id == domains[i].domain_id) {

                    var orgtypeId = parseInt(domains[i].industry_id);
                    var orgtypeName = domains[i].industry_name;
                    optText = optText + '<option value="'+orgtypeId+'" '+selectorgtypestatus+'>'+orgtypeName+'</option>';
                }
            }
            $('.orgtypeselected' + countval).html(optText);
        }
    } else {
        if (lentityId == 0 && $('#client-unit-id').val() == '') {
            displayMessage(message.legalentity_required);
            return false;
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
                if(orgn_names.length == 0){
                    orgn_names.push(domainList[j].industry_name);
                    break;
                }
                else{
                    var occur = false;
                    for(var k=0;k<orgn_names.length;k++){
                        if(orgn_names[k]==domainList[j].industry_name){
                            occur = true;
                            break;
                        }
                    }
                    if(occur == false){
                        orgn_names.push(domainList[j].industry_name);
                    }
                }
            }
        }
    }
    return orgn_names;
}
// Arrow key for domain and organization
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
function checkDeletedRow(delval){
    console.log(delval, del_row)
    for(var i=0;i<del_row.length;i++){
        console.log(del_row)
        if(del_row[i]==delval){
            console.log("true")
            return true;
        }
    }
    return false;
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
            console.log("save-1:"+unit_cnt)
            if ($('.category-name-' + i + '-' + 1).val() != '') {
                category = $('.category-name-' + i + '-' + 1).val();
            } else {
                category = null;
            }

            div_arr = mirror.getDivisionDict(divIdValue, divNameValue, category, i, parseInt(unit_cnt));
            division_units.push(div_arr);

            if (unit_cnt > 0) {
                for (var j = 1; j <= unit_cnt; j++) {
                    if(checkDeletedRow(i+"-"+j) == false){
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
                            if (unitCountValue == 1) {
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
                        } else if (unitAddress == '') {
                            displayMessage(message.unitaddress_required);
                            return;
                        } else if (unitPostalCode == '') {
                            displayMessage(message.unitpostal_required);
                            return;
                        } else if (unitdomain == '' || unitdomain == null) {
                            displayMessage(message.domain_required);
                            return;
                        } else if (unitIndustryId == '' || unitIndustryId == null) {
                            displayMessage(message.industryname_required);
                            return;
                        }
                        else
                        {
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
                                for (var ij = 0; ij < unitdomain.length; ij++) {
                                    unitdomains.push(parseInt(unitdomain[ij]));
                                }
                                for(var ij=0;ij<unitdomains.length;ij++){
                                    for(var jk=0;jk<unitIndustryId.length;jk++){
                                        var list = {};
                                        if(unitdomain.length == 1){
                                            list['domain_id'] = parseInt(unitdomain[ij]);
                                            list['industry_id'] = parseInt(unitIndustryId[jk]);
                                            unitIndustryIds.push(list);
                                        }else{
                                            list['domain_id'] = parseInt(unitdomain[ij]);
                                            list['industry_id'] = parseInt(unitIndustryId[jk]);
                                            unitIndustryIds.push(list);
                                            break;
                                        }
                                    }
                                }

                                unit = mirror.getUnitDict(null, unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitdomains, unitIndustryIds);

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
        /*mirror.saveClient(parseInt(groupNameValue), parseInt(bgIdValue), leIdValue, parseInt(countryVal), division_units, units, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.record_added);
                units_count = [];
                unitcodeautogenerateids = null;
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });*/
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
        var unitIndustryIds = [];
        var unitdomains = [];

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
            var catg_span_ctrl = $('.category-name-' + i + '-' + 1).attr('style').trim();
            if (catg_span_ctrl == "display: none;") {

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
                    if(checkDeletedRow(i+"-"+j) == false){
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
                                unitdomain = $('.domainselected-' + i + '-' + j).val();
                                //unitdomains = unitdomain;
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
                            } else if (unitAddress == '') {
                                displayMessage(message.unitaddress_required);
                                return;
                            } else if (unitPostalCode == '') {
                                displayMessage(message.unitpostal_required);
                                return;
                            } else if (unitdomain == '' || unitdomain == null) {
                                displayMessage(message.domain_required);
                                return;
                            } else if (unitIndustryId == '' || unitIndustryId == null) {
                                displayMessage(message.industryname_required);
                                return;
                            }  else {
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
                                    for (var ij = 0; ij < unitdomain.length; ij++) {
                                        unitdomains.push(parseInt(unitdomain[ij]));
                                    }
                                    for(var ij=0;ij<unitdomains.length;ij++){
                                        for(var jk=0;jk<unitIndustryId.length;jk++){
                                            var list = {};
                                            if(unitdomain.length == 1){
                                                list['domain_id'] = parseInt(unitdomain[ij]);
                                                list['industry_id'] = parseInt(unitIndustryId[jk]);
                                                unitIndustryIds.push(list);
                                            }else{
                                                list['domain_id'] = parseInt(unitdomain[ij]);
                                                list['industry_id'] = parseInt(unitIndustryId[jk]);
                                                unitIndustryIds.push(list);
                                                break;
                                            }
                                        }
                                    }

                                    if (total_div != i) {
                                        total_div = total_div + 1;
                                    }
                                    div_arr = mirror.getDivisionDict(parseInt(divIdValue), divNameValue, category, total_div, parseInt(total_units));
                                    division_units.push(div_arr);
                                    unit = mirror.getUnitDict(parseInt(unitId), unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitdomains, unitIndustryIds);

                                    units.push(unit);
                                } else {
                                    displayMessage(duplicates + ' Unit Code Already Exits!!!');
                                    return;
                                }
                            }
                        }
                    }
                }
            } else {
                displayMessage(message.add_one_unit);
                return;
            }
        }
        if(units.length > 0){
            mirror.saveClient(parseInt(client_id), parseInt(bgIdValue), parseInt(leIdValue), parseInt(countryVal), division_units, units, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.unit_updated);
                    units_count = [];
                    onSuccess(response);
                } else {
                    onFailure(error);
                }
            });
        }
        else{
            displayMessage("No Updations in Unit(s)");
        }
    }

    //main loop -- end
});
// Reset all filter in main search area
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
// To process the filter search
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
// Set class for status field
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
// Form Initialization
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
