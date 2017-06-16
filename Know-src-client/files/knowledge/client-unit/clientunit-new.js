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
var addedUnitList;
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
var prev_unit_cnt = null;
var prev_org_id = [];
var check_org = false;
var del_row = [];
var initTabIndex = 7;
var clientUnitAdd = $('#clientunit-add');
var clientUnitView = $('#clientunit-view');
var addUnitsId = [];
var le_contract_expiry = 0;
var le_approval = 0;
var unitcode_err = false;
var showMore_Hit = 0;

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
        showMore_Hit = 0;
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
        unitList = data.client_unit_list;
        //clientdomainList = data.client_domains;
        resetallfilter();
        loadClientsList(unitList);
        hideLoader();
    }

    function onFailure(error) {
        //displayMessage(error);
        if (error == "UserIsNotResponsibleForAnyClient") {
            $('.tbody-clientunit-list').empty();
            var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
            var clone4 = tableRow4.clone();
            $('.no_records', clone4).text('No Records Found');
            $('.tbody-clientunit-list').append(clone4);
        }
    }
    displayLoader();
    mirror.getClients('view', function(error, response) {
        if (error == null) {
            onSuccess(response);
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
    if (data.length == 0) {
        $('.tbody-clientunit-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-clientunit-list').append(clone4);
    } else {
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
            $('.group-name', clone).text(value.client_name);
            $('.business-group-name', clone).text(value.business_group_name);
            $('.country-name', clone).text(value.country_name);
            $('.legal-entity-name', clone).text(value.legal_entity_name);

            //edit icon
            if (value.is_approved == 0) {
                $('.edit', clone).hide();
            } else {
                $('.edit').attr('title', 'Click Here to Edit');
                $('.edit', clone).addClass('fa-pencil text-primary');
                $('.edit', clone).on('click', function() {
                    $('.total_created_unit').text("0");
                    $('#btn-clientunit-showmore').show();
                    clientunit_edit(clientId, bgroupId, lentitiesId, countryId, value.total_units);
                });
            }


            $('.tbody-clientunit-list').append(clone);
        });
    }

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
    initTabIndex = 7;
    clientUnitAdd.show();
    clientUnitView.hide();
    clientSelect.show();
    bgrpSelect.show();
    leSelect.show();
    $('#btn-clientunit-showmore').hide();
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
    $('#add-country-row').show();
    $(".checkbox-single").show();
    $(".unit-code-label").hide();
    unitErrMsg.val('');
    checkunitscount = null;
    countryByCount = 1;
    countc = 0;
    showMore_Hit = 0;
    usercountrycount = 0;
    $('.total_created_unit').text("0");
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
    unitcodeautogenerateids = null;
    initialize();
    initTabIndex = 7;
    showMore_Hit = 0;
});
//Load All Groups  ---------------------------------------------------------------------------------------------
function loadClientGroups(groupsList) {
    $('#group-select').focus();
    var clients = groupsList;
    for (var i = 0; i < clients.length; i++) {
        var ul_list = document.getElementById("group-select");
        var li_list = ul_list.getElementsByTagName("option");
        var occur = -1;
        for (var j = 0; j < li_list.length; j++) {
            occur = li_list[j].textContent.indexOf(clients[i].group_name)
        }
        if (occur < 0) {
            var obj = $(".client-drop-down option");
            var clone = obj.clone();
            clone.attr("value", clients[i].client_id);
            clone.text(clients[i].group_name);
            clientSelect.append(clone);
        }
    }
}
// On change of client group will reset other filters
$("#group-select").on("change", function() {
    if ($(this).val() == "") {
        $("#businessgroup-select option:gt(0)").remove();
    } else {
        $("#businessgroup-select").empty();
        var obj_bgrp = $(".bgrp-drop-down option");
        var clone_bgrp = obj_bgrp.clone();
        clone_bgrp.attr("value", 0);
        clone_bgrp.text("Select");
        $('#businessgroup-select').append(clone_bgrp);
        $('#country-name').val('');
        $('#country-id').val('');
        $('#entity-select').empty();
        var obj_le = $(".le-drop-down option");
        var clone_le = obj_le.clone();
        clone_le.attr("value", 0);
        clone_le.text("Select");
        leSelect.append(clone_le);
        loadBusinessGroups();
    }
    division_cnt = 0;
    $('.total_created_unit').text("0");
    unitcodeautogenerateids = null;
});
//Load Business Groups  ---------------------------------------------------------------------------------------------
function loadBusinessGroups() {
    var groupId = clientSelect.val();
    for (var i in businessGroupList) {
        if (businessGroupList[i].client_id == groupId) {
            var bgroupId = businessGroupList[i].business_group_id;
            var bgroupName = businessGroupList[i].business_group_name;
            var ul_list = document.getElementById("businessgroup-select");
            var li_list = ul_list.getElementsByTagName("option");
            var occur = -1;
            for (var j = 0; j < li_list.length; j++) {
                occur = li_list[j].textContent.indexOf(bgroupName)
            }
            if (occur < 0) {
                var obj = $(".bgrp-drop-down option");
                var clone = obj.clone();
                clone.attr("value", bgroupId);
                clone.text(bgroupName);
                $('#businessgroup-select').append(clone);
            }
        }
    }
}
// On change of business group will reset the child filters
$("#businessgroup-select").on("change", function() {
    $('#country-name').val('');
    $('#entity-select').empty();
    var obj_le = $(".le-drop-down option");
    var clone_le = obj_le.clone();
    clone_le.attr("value", 0);
    clone_le.text("Select");
    $('#country-name').val('');
    $('#country-id').val('');
    leSelect.append(clone_le);
    division_cnt = 0;
    $('.total_created_unit').text("0");
    unitcodeautogenerateids = null;
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
    division_cnt = 0;
    $('.total_created_unit').text("0");
    unitcodeautogenerateids = null;
}
// Arrow key functionality
function onArrowKey_Client(e, ac_item, multipleselect, callback) {
    var ccount;
    if (multipleselect.indexOf('unit') >= 0) {
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
            var elem = "<li id=" + ac_id + ">" + ac_name + "</li>";
            $('.auto-complete-unit-location').css('display', 'none');
            activate_unitlocaion(elem, ccount, mappingname);
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
                            for (var j = 0; j < li_list.length; j++) {
                                //occur = li_list[j].textContent.indexOf(countries[i].country_name)
                                if (li_list[j].textContent == countries[i].country_name)
                                    occur = 1;
                            }
                            if (occur < 0) {
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
                            for (var j = 0; j < li_list.length; j++) {
                                //occur = li_list[j].textContent.indexOf(countries[i].country_name)
                                if (li_list[j].textContent == countries[i].country_name)
                                    occur = 1;
                            }
                            if (occur < 0) {
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
    unitcodeautogenerateids = null;
    division_cnt = 0;
    units_count = [];
    var clientId = clientSelect.val();
    var businessGroupId = bgrpSelect.val();
    var countryId = $('#country-id').val();
    if (businessGroupId == 0) {
        businessGroupId = null;
    }
    if (businessGroupId != null && clientId != '' && countryId != '') {
        $('#entity-select').find('option:gt(0)').remove();
        $.each(legalEntitiesList, function(key, value) {
            var expiry_days = parseInt(value.le_expiry_days);
            if (value.client_id == clientId && value.business_group_id == businessGroupId &&
                value.country_id == countryId && expiry_days > 0 && value.is_approved == 1) {
                var lentityId = value.legal_entity_id;
                var lentityName = value.legal_entity_name;
                var ul_list = document.getElementById("entity-select");
                var li_list = ul_list.getElementsByTagName("option");
                var occur = -1;
                for (var j = 0; j < li_list.length; j++) {
                    occur = li_list[j].textContent.indexOf(lentityName)
                }
                if (occur < 0) {
                    var obj = $(".le-drop-down option");
                    var clone = obj.clone();
                    clone.attr("value", lentityId);
                    clone.text(lentityName);
                    leSelect.append(clone);
                }

            }
        });
    }
    if (businessGroupId == null && clientId != 0 && countryId != '') {
        $('#entity-select').find('option:gt(0)').remove();
        //$('#division-select').find('option:gt(0)').remove();
        $.each(legalEntitiesList, function(key, value) {
            var expiry_days = parseInt(value.le_expiry_days);
            if (value.client_id == clientId && value.country_id == countryId && expiry_days > 0 && value.is_approved == 1) {
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

function getLEDetails() {
    $('.total_created_unit').text("0");
    var lentityId = leSelect.val();
    for (var le = 0; le < legalEntitiesList.length; le++) {
        if (legalEntitiesList[le].legal_entity_id == lentityId) {
            le_contract_expiry = parseInt(legalEntitiesList[le].le_expiry_days);
            le_approval = legalEntitiesList[le].is_approved;
        }
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
    } else if (countryVal == '' && ($('.labelcountry').text() == '')) {
        displayMessage(message.country_required);
        return false;
    } else if (lentityId == 0 && ($('.labelentity').text() == '')) {
        displayMessage(message.legalentity_required);
        return false;
    } else {
        //unitcodeautogenerateids = null;
        function onSuccess(data) {
            addedUnitList = data.unit_list;
            for (var i = 0; i < addedUnitList.length; i++) {
                push_added_domain_org(addedUnitList);
            }
            hideLoader();
            if (le_contract_expiry >= 0 && le_approval > 0) {
                $('.add-country-unit-list').show();
                addcountryrownew();
            } else {
                if (le_contract_expiry < 0) {
                    displayMessage(message.legal_entity_expired);
                } else if (le_approval == 0) {
                    displayMessage(message.legal_entity_approval);
                }
            }

        }

        function onFailure(error) {
            displayMessage(error);
        }
        displayLoader();
        mirror.getClientsEdit(parseInt(clientSelect.val()), parseInt(bgrpSelect.val()), parseInt(leSelect.val()), parseInt(ctrySelect_id.val()), 0, 0, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
                hideLoader();
            }
        });

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
    var divCountryAddRow = null;
    divCountryAddRow = $('#templates .grid-table');

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
    $('.labeldomain', clone).addClass('labeldomain-' + division_cnt + '-' + 1);
    $('.domain', clone).addClass('domain-' + division_cnt + '-' + 1);
    $('.assign_cnt', clone).addClass('assign_cnt-' + division_cnt + '-' + 1);
    $('.orgtype-list', clone).addClass('orgtype-list-' + division_cnt + '-' + 1);
    $('.edit_o_ids', clone).addClass('edit_o_ids-' + division_cnt + '-' + 1);
    $('.orgtypeselected', clone).addClass('orgtypeselected-' + division_cnt + '-' + 1);
    $('.ul-orgtype-list', clone).addClass('ul-orgtype-list-' + division_cnt + '-' + 1);
    $('.labelorganization', clone).addClass('labelorganization-' + division_cnt + '-' + 1);
    $('.add-unit-row', clone).addClass('table-addunit-' + division_cnt);
    $('.tbody-unit-list', clone).addClass('tbody-unit-' + division_cnt);
    $('.no-of-units', clone).addClass('no-of-units-' + division_cnt);
    $('.activedclass', clone).addClass('activedclass-' + division_cnt + '-' + 1);
    $('.approveclass', clone).addClass('approveclass-' + division_cnt + '-' + 1);
    $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).attr('title', 'Close');
    $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).on('click', function() {
        unitrow_close(this.className);
    });
    $('.remove-icon', clone).addClass('remove-icon-' + division_cnt + '-' + 1).attr('title', 'Remove');
    $('.remove-icon', clone).addClass('remove-icon-' + division_cnt + '-' + 1).on('click', function() {
        unitrow_remove(this.className);
    });
    if ($('#client-unit-id').val() > 0) {
        $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).attr('title', 'Edit');
        $('.edit-icon', clone).on('click', function() {
            var orgtypeArray = $('.orgtypeselected-' + division_cnt + '-' + 1, clone).val();
            unitrow_edit(this, orgtypeArray);
        });
        $('.division-new-' + division_cnt + '-' + 1, clone).hide();
        $('.division-existing-' + division_cnt + '-' + 1).hide();
        $('.remove-icon-' + division_cnt + '-' + 1).hide();
        if (edit == false) {
            $('.domainselected-' + division_cnt + '-' + 1).multiselect('rebuild');
            $('.orgtypeselected-' + division_cnt + '-' + 1).multiselect('rebuild');

            //$('.domainselected-' + division_cnt + '-' + 1).parent('span').show();
            //$('.orgtypeselected-' + division_cnt + '-' + 1).parent('span').show();
        }
    } else {
        $('.edit-icon', clone).addClass('edit-icon-' + division_cnt + '-' + 1).hide();
        $('.delete-icon', clone).addClass('delete-icon-' + division_cnt + '-' + 1).hide();
        $('.remove-icon-' + division_cnt + '-' + 1, clone).show();
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
    if ($('#client-unit-id').val() == "") {
        if ($('.total_created_unit').text() == "") {
            $('.total_created_unit').text("1");
        } else {
            $('.total_created_unit').text(parseInt($('.total_created_unit').text()) + 1);
        }
    }
    $('.unitcnt-' + division_cnt + '-' + 1).val(1);
    if ($("#client-unit-id").val() == "") {
        loadDomains(division_cnt + '-' + 1, null);
        $('.orgtypeselected-' + division_cnt + '-' + 1).multiselect('rebuild');
    } else {
        $('.domainselected-' + division_cnt + '-' + 1).multiselect('rebuild');
        $('.orgtypeselected-' + division_cnt + '-' + 1).multiselect('rebuild');
    }

    if ($('.unitcode-checkbox-' + division_cnt).is(':checked')) {
        $('.unit-code-' + division_cnt + '-' + 1).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
        unitcodeautogenerateids++;
    }
    countc++;
    countryByCount++;
    $('.unit-code', clone).on('input', function(e) {
        this.value = isCommon_Unitcode($(this));
    });
    $('.unit-code', clone).on('change', function(e) {
        if ($(this).val() == "") {
            unitcodeautogenerateids = unitcodeautogenerateids - 1;
        }
    });
    $('.unit-name', clone).on('input', function(e) {
        this.value = isCommon($(this));
    });
    $('.category-name', clone).on('input', function(e) {
        this.value = isCommon_input($(this));
    });
    $('.division-name', clone).on('input', function(e) {
        this.value = isCommon_input($(this));
    });
    $('.unit-address', clone).on('input', function(e) {
        this.value = isCommon_Address($(this));
    });
    $('.postal-code', clone).on('input', function(e) {
        this.value = isNumbers($(this));
    });

    $('.domainselected-' + division_cnt + '-' + 1, clone).on('change', function(e) {
        checkAssignedUnits(e);
        log_units_count(e);
    });
    $('.orgtypeselected-' + division_cnt + '-' + 1, clone).on('change', function(e) {
        checkUnassignedOrg(e);
        log_units_count(e);
    });
    setTabIndex(division_cnt);
}
//Add Unit for individual Rows---------------------------------------------------------------------------------
function log_units_count(e) {
    var classattr = e.target.className.split(" ").pop().split("-");
    var classval = classattr[1] + "-" + classattr[2];
    var domain_id = $('.domainselected-' + classval).val();
    var org_id = $('.orgtypeselected-' + classval).val();
    var chk_count = 0;
    var assigned_count = 0;
    var assignedUnits = 0;
    var unitIndx = -1;
    var ind_count = 0;
    var entityval;
    if ($('#client-unit-id').val() != '') {
        entityval = $('#legalentity-update-id').val();
    } else {
        entityval = leSelect.val();
    }
    if (domain_id != null && (org_id != null && org_id != '')) {
        if (units_count.length > 0) {
            for (var d = 0; d < domain_id.length; d++) {
                for (var o = 0; o < org_id.length; o++) {
                    ind_count = 0;
                    for (var il = 0; il < industryList.length; il++) {
                        assignedUnits = 0;
                        assigned_count = 0;
                        unitIndx = -1;
                        chk_count = 0;
                        if (industryList[il].legal_entity_id == entityval && industryList[il].domain_id == domain_id[d] && industryList[il].industry_id == org_id[o]) {
                            ind_count++;
                            assignedUnits = industryList[il].unit_count;
                            for (var i = 0; i < units_count.length; i++) {
                                if (domain_id[d] == units_count[i].d_id && org_id[o] == units_count[i].o_id) {
                                    prev_unit_cnt = domain_id[d] + "-" + org_id[o];
                                    chk_count++;
                                    if (classval == units_count[i].row) {
                                        unitIndx = i;
                                    }
                                    assigned_count = parseInt(units_count[i].u_count) + assigned_count;
                                }
                            }
                            if (assigned_count < assignedUnits || assigned_count == 0) {
                                if (chk_count == 0 || unitIndx < 0) {
                                    units_count.push({
                                        "row": classval,
                                        "d_id": domain_id[d],
                                        "o_id": org_id[o],
                                        "a_count": assignedUnits,
                                        "u_count": 1
                                    });
                                    //console.log("pushed-2:"+classval, domain_id[d], org_id[o], assignedUnits, 1);
                                } else if (unitIndx >= 0) {
                                    if (units_count[unitIndx].u_count == 0) {
                                        units_count[unitIndx].u_count = 1;
                                    }
                                }
                            } else {
                                if (unitIndx >= 0) {
                                    if (units_count[unitIndx].u_count == 0) {
                                        units_count[unitIndx].u_count = 1;
                                    }
                                } else {
                                    alertrow(e, classval, org_id[o]);
                                }
                            }
                        }
                    }
                    if (ind_count == 0) {
                        var exist_d_id = -1;
                        for (var ind = 0; ind < units_count.length; ind++) {
                            if (domain_id[d] == units_count[ind].d_id) {
                                exist_d_id = 1;
                                break;
                            }
                        }
                        if (exist_d_id < 0) {
                            prev_org_id = org_id;
                            industrytype('industry-' + classval, prev_org_id);
                        }
                    }
                }
            }
        } else {
            push_domain_orgn(classval, domain_id, org_id);
        }
    } else if (domain_id != null) {
        var edit_icon = $('.delete-icon-' + classval).attr('style').split(";")[0].trim();
        var chk_count = 0;
        var i_ids = null;
        if (units_count.length > 0) {
            for (var d = 0; d < domain_id.length; d++) {
                for (var i = 0; i < units_count.length; i++) {
                    if (domain_id[d] == units_count[i].d_id && classval == units_count[i].row) {
                        chk_count++;
                        if ($('.unit-id-' + classval).val() != "") {
                            i_ids = $('.edit_o_ids-' + classval).val();
                            /*for (var u = 0; u < unitList.length; u++) {
                                if (unitList[u].unit_id == $('.unit-id-' + classval).val()) {
                                    i_ids = unitList[u].i_ids;
                                    break;
                                }
                            }*/
                            if (units_count[i].u_count == 1 && i_ids.indexOf(units_count[i].o_id) < 0) {
                                //displayMessage(message.org_remove);
                                units_count[i].u_count = 0;
                            } else if (i_ids.indexOf(units_count[i].o_id) < 0) {
                                if ($('.orgtypeselected-' + classval).val() != null) {
                                    prev_org_id = $('.orgtypeselected-' + classval).val();
                                } else {
                                    prev_org_id = i_ids;
                                }
                                industrytype('industry-' + classval, prev_org_id);
                            }
                        } else {
                            if (units_count[i].u_count > 0) {
                                units_count[i].u_count = 0;
                            } else {
                                prev_org_id = null;
                                industrytype('industry-' + classval, prev_org_id);
                            }
                        }
                    }
                }
                if (chk_count == 0) {
                    i_ids = null;
                    if ($('.unit-id-' + classval).val() != "") {
                        i_ids = $('.edit_o_ids-' + classval).val();
                    }
                    prev_org_id = i_ids;
                    industrytype('industry-' + classval, prev_org_id);
                }
            }
        } else {
            prev_org_id = null;
            industrytype('industry-' + classval, prev_org_id);
        }
    } else if (domain_id == null) {
        if (units_count.length > 0) {
            for (var i = 0; i < units_count.length; i++) {
                if (classval == units_count[i].row) {
                    if (units_count[i].u_count > 0) {
                        units_count[i].u_count = 0;
                    }
                    $('.orgtypeselected-' + classval).empty();
                    prev_org_id = null;
                    industrytype('industry-' + classval, prev_org_id);
                }
            }
        }
    }
}

function alertrow(e, classval, org_id) {
    var org_name = null;
    for (var dl = 0; dl < domainList.length; dl++) {
        if (org_id == domainList[dl].industry_id) {
            org_name = domainList[dl].industry_name;
        }
    }
    var msgstatus = message.unit_remove + "(" + org_name + ")";
    check_org = false;
    displayMessage(msgstatus);
    if ($('.unit-id-' + classval).val() == "") {
        var index = parseInt(classval.split("-")[1]);
        if (index == 1) {
            var rowIndx = index - 1;
            $('.tbody-unit-' + division_cnt + ' tr').eq(rowIndx).remove();
            if ($('.tbody-unit-' + division_cnt + ' tr').length == 0)
            {
                division_cnt = division_cnt - 1;
            }
        } else {
            index = parseInt(classval.split("-")[0]);
            var rowIndx = 0;
            if (parseInt($('.tbody-unit-' + index + ' tr').length) > 1) {}
            $('.tbody-unit-' + index + ' tr').eq(rowIndx).remove();
        }
        var countval = classval.split("-")[0];
        $('.unitcnt-' + countval + '-' + 1).val(parseInt($('.unitcnt-' + countval + '-' + 1).val()) - 1);
        $('.total_created_unit').text(parseInt($('.total_created_unit').text()) - 1);
        for (var i = 0; i < units_count.length; i++) {
            if (units_count[i].row == classval) {
                units_count[i].u_count = 0;
            }
        }

        if (unitcodeautogenerateids != null)
            unitcodeautogenerateids = unitcodeautogenerateids - 1;
    } else {
        i_ids = null;
        for (var i = 0; i < unitList.length; i++) {
            if (unitList[i].unit_id == $('.unit-id-' + classval).val()) {
                i_ids = unitList[i].i_ids;
                break;
            }
        }
        industrytype('industry-' + classval, i_ids);
        //$('.orgtypeselected-'+classval+" option").filter("[value = " + org_id + "]").removeAttr("checked");
    }
    e.preventDefault();
}

function push_added_domain_org(data) {
    var entityval;
    if ($('#client-unit-id').val() != '') {
        entityval = $('#legalentity-update-id').val();
    } else {
        entityval = leSelect.val();
    }
    var rowNo = 0;
    var add_occur = -1;
    for (var j = 0; j < data.length; j++) {
        d_id = data[j].domain_ids;
        o_id = data[j].i_ids;
        for (var d = 0; d < d_id.length; d++) {
            add_occur = -1;
            for (var o = 0; o < o_id.length; o++) {
                for (var il = 0; il < industryList.length; il++) {
                    if (industryList[il].legal_entity_id == entityval && industryList[il].domain_id == d_id[d] && industryList[il].industry_id == o_id[o]) {
                        var assignedUnits = industryList[il].unit_count;
                        var assigned_count = 0;
                        for (var i = 0; i < units_count.length; i++) {
                            if (units_count[i].d_id == d_id[d] && units_count[i].o_id == o_id[o] && units_count[i].row == "0-" + j) {
                                add_occur = 1;
                            }
                        }
                        if (add_occur < 0) {
                            units_count.push({
                                "row": "0-" + j,
                                "d_id": d_id[d],
                                "o_id": o_id[o],
                                "a_count": assignedUnits,
                                "u_count": 1
                            });
                            //console.log("pushed-0:"+"0-"+j, d_id[d], o_id[o], assignedUnits, 1, j);
                        }
                    }
                }
            }
        }
    }
}

function push_domain_orgn(classval, d_id, o_id) {
    var entityval;
    if ($('#client-unit-id').val() != '') {
        entityval = $('#legalentity-update-id').val();
    } else {
        entityval = leSelect.val();
    }
    if ($('#client-unit-id').val() == '' || $('.unit-id-' + classval).val() == '') {
        var add_occur = 0;
        for (var d = 0; d < d_id.length; d++) {
            for (var o = 0; o < o_id.length; o++) {
                for (var il = 0; il < industryList.length; il++) {
                    if (industryList[il].legal_entity_id == entityval && industryList[il].domain_id == d_id[d] && industryList[il].industry_id == o_id[o]) {
                        var assignedUnits = industryList[il].unit_count;
                        for (var i = 0; i < units_count.length; i++) {
                            if (units_count[i].d_id == d_id[d] && units_count[i].o_id == o_id[o] && units_count[i].row == classval) {
                                add_occur++;
                            }
                        }
                        if (add_occur == 0) {
                            units_count.push({
                                "row": classval,
                                "d_id": d_id[d],
                                "o_id": o_id[o],
                                "a_count": assignedUnits,
                                "u_count": 1
                            });
                            //console.log("pushed-1:"+classval, d_id[d], o_id[o], assignedUnits, 1);
                        }
                    }
                }
            }
        }
    } else {
        var occur = -1;
        var unitIndx = -1;
        for (var d = 0; d < d_id.length; d++) {
            for (var o = 0; o < o_id.length; o++) {
                for (var i = 0; i < units_count.length; i++) {
                    for (var il = 0; il < industryList.length; il++) {
                        if (industryList[il].legal_entity_id == entityval && industryList[il].domain_id == d_id[d] && industryList[il].industry_id == o_id[o]) {
                            var assignedUnits = industryList[il].unit_count;
                            if (d_id[d] == units_count[i].d_id && o_id[o] == units_count[i].o_id) {
                                occur = 1;
                                if (classval != units_count[i].row) {
                                    occur = -1;
                                }
                            }
                        }
                    }
                }
            }
        }

        if (occur < 0) {
            row_occur = -1;
            for (var d = 0; d < d_id.length; d++) {
                row_occur = -1;
                for (var o = 0; o < o_id.length; o++) {
                    for (var il = 0; il < industryList.length; il++) {
                        if (industryList[il].legal_entity_id == entityval && industryList[il].domain_id == d_id[d] && industryList[il].industry_id == o_id[o]) {
                            var assignedUnits = industryList[il].unit_count;
                            for (var i = 0; i < units_count.length; i++) {
                                if (units_count[i].d_id == d_id[d] && units_count[i].o_id == o_id[o] && units_count[i].row == classval) {
                                    row_occur = 1;
                                }
                            }
                            if (row_occur < 0) {
                                units_count.push({
                                    "row": classval,
                                    "d_id": d_id[d],
                                    "o_id": o_id[o],
                                    "a_count": assignedUnits,
                                    "u_count": 1
                                });
                                //console.log("pushed-3:"+classval, d_id[d], o_id[o], assignedUnits, 1);
                            }
                        }
                    }
                }
            }
        }
    }
}

//check assigned units under domain while removing a domain from unit
function checkAssignedUnits(e) {
    classattr = e.target.className.split(" ").pop().split("-");
    classval = classattr[1] + "-" + classattr[2];
    d_sel = $('.domainselected-' + classval).val();
    domain_saved = $('.domain-' + classval).val();
    a_cnt = $('.assign_cnt-' + classval).val();
    var d_ids = null;
    var d_name = null;
    var checkAssigned = false;
    if ($('.unit-id-' + classval).val() != '') {
        if (d_sel != null) {
            for (var i = 0; i < domain_saved.length; i++) {
                if (jQuery.inArray(domain_saved[i], d_sel) < 0) {
                    if (a_cnt[i] > 0) {
                        checkAssigned = true;
                        d_ids = parseInt(domain_saved[i]);
                        for (var j = 0; j < domainList.length; j++) {
                            if (d_ids == domainList[j].domain_id) {
                                d_name = domainList[j].domain_name;
                                break;
                            }
                        }
                        domain_alert = message.unit_unassign_confirm.replace('d_name', d_name);
                        confirm_alert(domain_alert, function(isConfirm) {
                            if (isConfirm) {
                                displayLoader();
                                mirror.checkAssignedDomainUnits(parseInt($('.unit-id-' + classval).val()), d_ids, function(error, response) {
                                    if (error == null) {
                                        displaySuccessMessage(message.unit_assigned('d_name', d_name));
                                        i_ids = null;
                                        for (var i = 0; i < unitList.length; i++) {
                                            if (unitList[i].unit_id == $('.unit-id-' + classval).val()) {
                                                i_ids = unitList[i].i_ids;
                                                break;
                                            }
                                        }
                                        industrytype('industry-' + classval, i_ids);
                                        hideLoader();
                                    } else {
                                        displayMessage(error);
                                        hideLoader();
                                    }
                                });
                            } else {
                                d_ids = [];
                                loadDomains(classval, domain_saved);
                            }
                            e.preventDefault();
                        });
                    }
                    for (var u = 0; u < units_count.length; u++) {
                        if (classval == units_count[u].row && units_count[u].d_id == domain_saved[i]) {
                            if (units_count[u].u_count > 0) {
                                units_count[u].u_count = 0;
                            }
                        }
                    }
                }
            }
            if (checkAssigned == false) {
                i_ids = $('.edit_o_ids-' + classval).val();
                industrytype('industry-' + classval, i_ids);
            }
        } else {
            displayMessage(message.domain_required);
        }
    } else {
        var d_nodes = e.target.childNodes;
        for (var i = 0; i < d_nodes.length; i++) {
            for (var j = 0; j < units_count.length; j++) {
                if (units_count[j].row == classval) {
                    if (units_count[j].d_id == d_nodes[i].value && d_nodes[i].selected == false) {
                        if (units_count[j].u_count > 0) {
                            units_count[j].u_count = 0;
                        }
                        //industrytype('industry-' + classval, prev_org_id);
                    }
                }
            }
            industrytype('industry-' + classval, $('.orgtypeselected-' + classval).val());
        }
    }
}

// To enroll unchecked organizations
function checkUnassignedOrg(e) {
    classattr = e.target.className.split(" ").pop().split("-");
    classval = classattr[1] + "-" + classattr[2];
    var o_nodes = e.target.childNodes;
    for (var i = 0; i < o_nodes.length; i++) {
        var o_list = o_nodes[i].childNodes;
        for (var j = 0; j < o_list.length; j++) {
            for (var k = 0; k < units_count.length; k++) {
                if (units_count[k].row == classval) {
                    if (units_count[k].o_id == o_list[j].value && o_list[j].selected == false) {
                        if (units_count[k].u_count > 0) {
                            units_count[k].u_count = 0;
                        }
                    }
                }
            }
        }
    }
}

// Checks the stored unit count under a domain and organization - to prompt user
var x = 0;

function check_previous_orgn(evt) {
    if (x == 0) {
        x = 1;
        //$('.add-unit-row').hide();
        if (check_org == true) {
            var dom_id = null;
            var org_id = null;
            var org_bool = true;
            var unitno = $('.unitcnt-' + division_cnt + '-' + 1).val();
            dom_id = $('.domainselected-' + division_cnt + '-' + unitno).val();
            org_id = $('.orgtypeselected-' + division_cnt + '-' + unitno).val();

            if (org_bool == true) {
                var msgstatus = message.unit_remove;
                displayMessage(msgstatus);
                var index = parseInt($('.tbody-unit-' + division_cnt + ' tr').parent().index()) + 1;
                $('.tbody-unit-' + division_cnt + ' tr').eq(0).remove();
                $('.unitcnt-' + division_cnt + '-' + 1).val(parseInt($('.unitcnt-' + division_cnt + '-' + 1).val()) - 1);
                $('.total_created_unit').text(parseInt($('.total_created_unit').text()) - 1);
                if (unitcodeautogenerateids != null)
                    unitcodeautogenerateids = unitcodeautogenerateids - 1;
                check_org = false;
            } else {
                check_org = false;
                addNewUnitRow(evt);
            }
        } else {
            if (le_contract_expiry >= 0 && le_approval > 0) {
                addNewUnitRow(evt);
            } else {
                if (le_contract_expiry < 0) {
                    displayMessage(message.legal_entity_expired);
                } else if (le_approval == 0) {
                    displayMessage(message.legal_entity_approval);
                }
            }
        }
        setTimeout(function() { x = 0; }, 500);
    }
}
// To add new unit rows under division category
function addNewUnitRow(str) {
    var lastIndexOf_hyphen = str.lastIndexOf('-');
    var countval = str.substring((lastIndexOf_hyphen + 1), (lastIndexOf_hyphen + 2));
    var table_tr = null;
    var unitval = parseInt($('.unitcnt-' + countval + '-' + 1).val()) + 1;
    $('.unitcnt-' + countval + '-' + 1).val(unitval);
    addUnitsId.push(countval + "-" + unitval);
    if (parseInt($('.tbody-unit-' + countval).find('tr').length) > 0) {
        var divUnitAddRow = $('#templatesUnitRow').find('tr:eq(0)');
        var clone1 = divUnitAddRow.clone();

        $('.tbody-unit-' + countval).find('tr:eq(0)').before(clone1);
        table_tr = $('.tbody-unit-' + countval).find('tr:eq(0)');
    } else {
        var divUnitAddRow = $('#templatesUnitRow').find('tr:eq(0)');
        var clone1 = divUnitAddRow.clone();

        $('.tbody-unit-' + countval).append(clone1);
        table_tr = $('.tbody-unit-' + countval);
    }

    table_tr.find('td').find('input,select,span,div,ul,i').each(function() {
        $(this).attr({
            'class': function(_, lastClass) {
                return $(this).attr('class').split(' ').pop() + ' ' + $(this).attr('class') + '-' + countval + '-' + unitval
            },
        });
    });

    if (edit == false) {
        loadDomains(countval + '-' + unitval, null);
    }

    $('.sno-' + countval + '-' + unitval).text(unitval);
    if ($('.unitcode-checkbox-' + countval).is(':checked')) {
        $('.unit-code-' + countval + '-' + unitval).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
        unitcodeautogenerateids++;
    }
    $('.activedclass-' + countval + '-' + unitval).text('Active');
    $('.approveclass-' + countval + '-' + unitval).text('Pending');

    if ($('#client-unit-id').val() > 0) {
        if ($('.unit-id-' + countval + '-' + unitval).val() == '') {
            $('.edit-icon-' + countval + '-' + unitval).hide();
            $('.delete-icon-' + countval + '-' + unitval).attr('title', 'Close');
            $('.delete-icon-' + countval + '-' + unitval).on('click', function() {
                unitrow_close(this.className);
            });
            $('.delete-icon-' + countval + '-' + unitval).hide();
            $('.remove-icon-' + countval + '-' + unitval).show();
            $('.remove-icon-' + countval + '-' + unitval).attr('title', 'Remove');
            $('.remove-icon-' + countval + '-' + unitval).on('click', function() {
                unitrow_remove(this.className);
            });
        } else {
            $('.edit-icon-' + countval + '-' + unitval).show();
            $('.delete-icon-' + countval + '-' + unitval).hide();
            $('.remove-icon-' + countval + '-' + unitval).hide();
        }
        $('.division-new-' + countval + '-' + unitval).hide();
        $('.division-existing-' + countval + '-' + unitval).hide();
    } else {
        $('.edit-icon-' + countval + '-' + unitval).hide();
        $('.remove-icon-' + countval + '-' + unitval).attr('title', 'Remove');
        $('.remove-icon-' + countval + '-' + unitval).on('click', function() {
            unitrow_remove(this.className);
        });
        $('.remove-icon-' + countval + '-' + unitval).show();
        $('.division-new-' + countval + '-' + unitval).show();
        $('.division-existing-' + countval + '-' + unitval).hide();
    }
    if ($('#client-unit-id').val() == ""){
        if ($('.total_created_unit').text() == "") {
            $('.total_created_unit').text("1");
        } else {
            $('.total_created_unit').text(parseInt($('.total_created_unit').text()) + 1);
        }
    }

    $('.unit-code-' + countval + '-' + unitval).on('input', function(e) {
        this.value = isCommon_Unitcode($(this));
    });
    $('.unit-code-' + countval + '-' + unitval).on('change', function(e) {
        if ($(this).val() == "") {
            unitcodeautogenerateids = unitcodeautogenerateids - 1;
        }
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
    $('.category-name-' + countval + '-' + 1).on('input', function(e) {
        this.value = isCommon_input($(this));
    });
    $('.division-name-' + countval + '-' + 1).on('input', function(e) {
        this.value = isCommon_input($(this));
    });
    $('.orgtypeselected-' + countval + '-' + unitval).on('change', function(e) {
        //log_units_count(e,countval + '-' + unitval);
        checkUnassignedOrg(e);
        log_units_count(e);
    });
    $('.domainselected-' + countval + '-' + unitval).on('change', function(e) {
        checkAssignedUnits(e);
        log_units_count(e);
    });
    $('.orgtypeselected-' + countval + '-' + unitval).multiselect('rebuild');
    setTabIndex(countval);
}

function setTabIndex(countval) {
    var unit_second_cnt = parseInt($('.unitcnt-' + countval + '-' + 1).val())
    var table_tr = $('.tbody-unit-' + countval).find('tr:eq(0)');
    table_tr.find('td').find('input, button, select').each(function() {
        var c_name = $(this).attr('class');
        if (c_name != "undefined" && c_name != null && (c_name.indexOf("domainselected") >= 0 || c_name.indexOf("orgtypeselected") >= 0)) {
            //initTabIndex--;
        } else {
            initTabIndex++;
            $(this).attr({
                'tabindex': initTabIndex,
            });
        }
    });
    $('.glevel-' + countval + '-' + unit_second_cnt).focus();
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
function autoGenerateUnitCode(cls) {
    var client_id = $('#group-select').val();

    if (client_id == '' || client_id == null || client_id == "Select") {
        client_id = $('#client-unit-id').val();
    }

    function onSuccess(data) {
        unitcodeautogenerate(data.next_unit_code, cls);
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getNextUnitCode(parseInt(client_id), function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}
// Unit code auto generation
function unitcodeautogenerate(auto_generate_initial_value, cls) {
    countval = cls.split(" ")[1].split("-")[2].trim();
    //unitcodeautogenerateids = null;
    if (unitcodeautogenerateids == null || unitcodeautogenerateids == '') {
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
            $('.add-country-unit-list .tbody-unit-' +countval + ' .unit-code').each(function(i) {
                if ($(this).prev('.unit-id').val() == '') {
                    $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    unitcodeautogenerateids++;
                } else {
                    if ($(this).val() == '') {
                        $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                        unitcodeautogenerateids++;
                    } else {
                        if (unitcode_err == true) {
                            $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                            unitcodeautogenerateids++;
                        }
                    }
                }
            });
            unitcode_err = false;
        } else {
            $('.add-country-unit-list .unit-code').each(function(i) {
                if ($(this).prev('.unit-id').val() == '') {
                    $(this).val(''); //$(this).removeAttr("readonly");
                } else if ($(this).val() != '') {
                    if (unitcode_err == true) {
                        var groupname = $.trim($('#group-select :Selected').text());
                        var groupname = groupname.replace(' ', '');
                        get2CharsofGrouplower = groupname.slice(0, 2);
                        get2CharsofGroup = get2CharsofGrouplower.toUpperCase();
                        $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                        unitcodeautogenerateids++;
                    }
                }
            });
            unitcode_err = false;
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
                if ($(this).val() == '') {
                    $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    unitcodeautogenerateids++;
                } else {
                    //$(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    //unitcodeautogenerateids++;
                    if (unitcode_err == true) {
                        $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                        unitcodeautogenerateids++;
                    }
                }
            });
            unitcode_err = false;
        } else {
            $('.add-country-unit-list .unit-code').each(function(i) {
                if ($(this).val() == '') {
                    $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                    unitcodeautogenerateids++;
                } else if ($(this).val() != '') {
                    if (unitcode_err == true) {
                        var groupname = $.trim($('.labelgroup').text());
                        var groupname = groupname.replace(' ', '');
                        get2CharsofGrouplower = groupname.slice(0, 2);
                        get2CharsofGroup = get2CharsofGrouplower.toUpperCase();
                        $(this).val(get2CharsofGroup + intTo5digitsString(unitcodeautogenerateids));
                        unitcodeautogenerateids++;
                    }
                }
            });
            unitcode_err = false;
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
function divisionExistingChecking(cls, str) {
    if (str == 'New') {
        split_space = cls.split(" ")[3].split("-")
        var countval = '-' + split_space[2] + '-' + 1;
        $('.input_business_group' + countval).show();
        $('.division-name' + countval).show();
        $('.division-name' + countval).focus();
        $('.division-id' + countval).hide();
        $('.division-new' + countval).hide();
        $('.division-existing' + countval).show();
        $('.division-name' + countval).val('');
        $('.division-id' + countval).val('');
        $('.select_business_group' + countval).hide();
    }
    if (str == 'Cancel') {
        split_space = cls.split(" ")[4].split("-")
        var countval = '-' + split_space[2] + '-' + 1;
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
        loadDivision('division-id' + countval);
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
            if (countryid == value.c_id) {
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
    var parentname = '';
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
                        console.log("1:"+countval, geographyList[glist].mapping);
                        activate_unitlocaion(this, countval, geographyList[glist].mapping);
                    });
                    clone.text(geographyList[glist].geography_name);
                    $('.unitlocationlist-text' + countval).append(clone);
                }
            }
        }
        onArrowKey_Client(e, 'auto-complete-unit-location', 'unit,' + countval, function(val) {
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
                if (domain_names.length == 0) {
                    domain_names.push(domainList[j].domain_name);
                    break;
                } else {
                    var occur = false;
                    for (var k = 0; k < domain_names.length; k++) {
                        if (domain_names[k] == domainList[j].domain_name) {
                            occur = true;
                            break;
                        }
                    }
                    if (occur == false) {
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
function loadDomains(ccount, selected_arr) {
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
    if ($('#client-unit-id').val() == 0) { // || $('.unit-id-'+division_cnt+'-'+$(".unitcnt-" + division_cnt + "-" + 1).val()).val() == '') {
        var domains = domainList;
        var lentityId = leSelect.val();
        var optText = "";
        var d_arr = [];
        $.each(domains, function(key, value) {
            if (lentityId == domains[key].legal_entity_id) {
                var occur = false;
                if (d_arr.length == 0) {
                    d_arr.push(domains[key].domain_id)
                } else {
                    for (var i = 0; i < d_arr.length; i++) {
                        if (d_arr[i] == domains[key].domain_id) {
                            occur = true;
                        }
                    }
                    if (occur == false) {
                        d_arr.push(domains[key].domain_id)
                    }
                }

                if (occur == false) {
                    optText = optText + '<option value="' + domains[key].domain_id + '" >' + domains[key].domain_name + '</option>';
                }
            }
        });
        d_ctrl.html(optText);
    } else {
        var domains = domainList;
        var lentityId = $('#legalentity-update-id').val();
        var optText = "";
        var d_arr = [];
        $.each(domains, function(key, value) {
            if(ccount.split("-")[1] == 1)
                editorgtypeval = selected_arr;
            else
                editorgtypeval = selected_arr.trim().split(",");
            //editorgtypeval = selected_arr;
            var selectorgtypestatus = '';
            if (editorgtypeval != null && editorgtypeval != "undefined") {
                for (var j = 0; j < editorgtypeval.length; j++) {
                    if (editorgtypeval[j] == domains[key].domain_id) {
                        selectorgtypestatus = 'selected';
                    }
                }
            }

            if (lentityId == domains[key].legal_entity_id) {
                var sel = "selected";
                var occur = false;

                if (d_arr.length == 0) {
                    d_arr.push(domains[key].domain_id)
                } else {
                    for (var i = 0; i < d_arr.length; i++) {
                        if (d_arr[i] == domains[key].domain_id) {
                            occur = true;
                        }
                    }
                    if (occur == false) {
                        d_arr.push(domains[key].domain_id)
                    }
                }

                if (occur == false) {
                    if (editorgtypeval == null && editorgtypeval == "undefined") {
                        optText = optText + '<option value="' + domains[key].domain_id + '">' + domains[key].domain_name + '</option>';
                    } else
                        optText = optText + '<option value="' + domains[key].domain_id + '" ' + selectorgtypestatus + ' >' + domains[key].domain_name + '</option>';
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
    unitid = $('.unit-id-' + ccount[1] + '-' + ccount[2]);

    if ($('#client-unit-id').val() == '') {
        domain_id = $('.domainselected' + countval).val();
        lentityId = leSelect.val();
    } else {
        domain_id = $('.domainselected' + countval).val();
        lentityId = $(".labelentity").data('id');
    }
    var editorgtypeval = [];

    if (lentityId > 0) {
        if ($('#client-unit-id').val() == 0 || $('#client-unit-id').val() == '') {
            var domains = domainList;
            var optText = "";

            for (var domain in domain_id) {
                var flag = true;
                for (var i in domains) {
                    var selectorgtypestatus = '';

                    if (selected_arr != null && selected_arr != "undefined") {
                        for (var j = 0; j < selected_arr.length; j++) {
                            if (selected_arr[j] == domains[i].industry_id && domain_id[domain] == domains[i].domain_id) {
                                selectorgtypestatus = 'selected';
                            }
                        }
                    }
                    if (lentityId == domains[i].legal_entity_id && domain_id[domain] == domains[i].domain_id) {
                        if (flag) {
                            optText += '<optgroup label="' + domains[i].domain_name + '">';
                        }
                        var orgtypeId = parseInt(domains[i].industry_id);
                        var orgtypeName = domains[i].industry_name;
                        optText = optText + '<option value="' + orgtypeId + '" ' + selectorgtypestatus + '>' + orgtypeName + '</option>';
                        flag = false;
                    }
                }
                if (flag == false) optText += '</optgroup>'
                $('.orgtypeselected' + countval).html(optText);
            }

        } else {
            if(ccount[2] == 1)
                editorgtypeval = selected_arr;
            else
                editorgtypeval = selected_arr.trim().split(",");
            var domains = domainList;
            var optText = "";
            for (var domain in domain_id) {
                var flag = true;
                for (var i in domains) {
                    var selectorgtypestatus = '';
                    var readonlystatus = '';
                    if (editorgtypeval != null && editorgtypeval != "undefined") {
                        for (var j = 0; j < editorgtypeval.length; j++) {
                            if (editorgtypeval[j] == domains[i].industry_id && domain_id[domain] == domains[i].domain_id) {
                                selectorgtypestatus = 'selected';
                                if ($('.unit-id' + countval).val() != '') {
                                    readonlystatus = 'disabled';
                                }
                            }
                        }
                    }

                    if (lentityId == domains[i].legal_entity_id && domain_id[domain] == domains[i].domain_id) {
                        if (flag) {
                            optText += '<optgroup label="' + domains[i].domain_name + '">';
                        }
                        var orgtypeId = parseInt(domains[i].industry_id);
                        var orgtypeName = domains[i].industry_name;
                        optText = optText + '<option value="' + orgtypeId + '" ' + selectorgtypestatus + ' ' + readonlystatus + '>' + orgtypeName + '</option>';
                        flag = false;

                    }
                }
                if (flag == false) optText += '</optgroup>'
                $('.orgtypeselected' + countval).html(optText);
            }

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
                if (orgn_names.length == 0) {
                    orgn_names.push(domainList[j].industry_name);
                    break;
                } else {
                    var occur = false;
                    for (var k = 0; k < orgn_names.length; k++) {
                        if (orgn_names[k] == domainList[j].industry_name) {
                            occur = true;
                            break;
                        }
                    }
                    if (occur == false) {
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

function checkEditedRow(val) {
    var checkVal = false;
    for (var i = 0; i < edited_ids.length; i++) {
        if (edited_ids[i].split("-")[0] == val) {
            checkVal = true;
        }
    }
    return checkVal;
}

function checkNewAddRow(addval) {
    var checkVal = false;
    for (var i = 0; i < addUnitsId.length; i++) {
        if (addUnitsId[i] == addval) {
            checkVal = true;
        }
    }
    return checkVal;
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
    var editDiv = false;
    var editCatg = false;
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
        if (le_contract_expiry < 0) {
            displayMessage(message.legal_entity_expired)
        } else if (le_approval == 0) {
            displayMessage(legal_entity_approval)
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
                unitcode_err = true;
            } else if (error == 'CategoryNameAlreadyExists') {
                displayMessage(message.category_exists);
            } else if (error == 'SaveUnitFailure') {
                displayMessage(message.unit_failed);
            } else if (error == 'LegalEntityClosed') {
                displayMessage(message.le_closed);
            } else {
                displayMessage(error);
            }
        }
        var businessGroup;
        var bgIdValue;
        var bgNameValue;
        //bgIdValue = parseInt(businessgroupValue);
        if (businessgroupValue != 0 && businessgroupValue != "0") {
            bgIdValue = businessgroupValue;
            bgNameValue = businessgroupName;
        } else {
            for (var le = 0; le < legalEntitiesList.length; le++) {
                if (legalEntitiesList[le].legal_entity_id == legalEntityValue) {
                    bgIdValue = legalEntitiesList[le].business_group_id;
                    break;
                }
            }
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
        var division_dict = [];
        var units = [];
        var division_units = [];
        var unitarr = [];
        for (var i = 1; i <= division_cnt; i++) {
            var div_arr;
            divisionValue = $('.division-id-' + i + '-' + 1).val();
            divisiontextValue = $('.division-name-' + i + '-' + 1).val().trim();
            if (divisiontextValue == '') {
                if (divisionValue == "") {
                    divIdValue = null;
                    divNameValue = null;
                } else {
                    divIdValue = parseInt(divisionValue);
                    divNameValue = $('#division-select option:selected').text();
                }
            } else {
                divIdValue = null;
                if (validateMaxLength("division_name", divisiontextValue, "Division Name") == false) {
                    displayMessage(message.division_max);
                    return;
                } else
                    divNameValue = divisiontextValue;
            }
            unit_cnt = $('.unitcnt-' + i + '-1').val();
            if ($('.category-name-' + i + '-' + 1).val() != '') {
                if (validateMaxLength("category_name", $('.category-name-' + i + '-' + 1).val(), "Category Name") == false) {
                    displayMessage(message.category_max50);
                    return;
                } else
                    category = $('.category-name-' + i + '-' + 1).val();
            } else {
                category = null;
            }
            div_arr = mirror.getDivisionDict(divIdValue, divNameValue, category, i, parseInt(unit_cnt));
            division_units.push(div_arr);
            if (unit_cnt > 0) {
                for (var j = 1; j <= unit_cnt; j++) {
                    //if(checkDeletedRow(i+"-"+j) == false){
                    var unit;
                    var unitIndustryIds = [];
                    var unitdomains = [];
                    unitId = null;
                    glevel_item = $('.glevel-' + i + '-' + j).val();
                    unitCode = $('.unit-code-' + i + '-' + j).val();

                    unitName = $('.unit-name-' + i + '-' + j).val().trim();
                    unitAddress = $('.unit-address-' + i + '-' + j).val().trim();
                    unitPostalCode = $('.postal-code-' + i + '-' + j).val().trim();
                    unitGeographyId = $('.unitlocation-ids-' + i + '-' + j).val().trim();
                    unitLocation = $('.unitlocation-' + i + '-' + j).val().trim();


                    unitIndustryId = $('.orgtypeselected-' + i + '-' + j).val();

                    //unitIndustryName = $('.industry-' + i + '-' + j + ' option:selected').text();

                    unitdomain = $('.domainselected-' + i + '-' + j).val();

                    if (glevel_item == 0 && unitLocation == '' && unitGeographyId == '' && unitCode == '' && unitName == '' && unitAddress == '' && unitPostalCode == '' && unitdomains.length == 0 && unitIndustryIds.length == 0) {
                        if (unitCountValue == 1) {
                            displayMessage(message.add_one_unit);
                            return;
                        }
                        continue;
                    }
                    if (glevel_item == 0) {
                        displayMessage(message.geographylevel_required);
                        return;
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
                    } else if (validateMaxLength("unit_code", unitCode, "Unit Code") == false) {
                        return;
                    } else if (unitName == '') {
                        displayMessage(message.unitname_required);
                        return;
                    } else if (validateMaxLength("unit_name", unitName, "Unit Name") == false) {
                        return;
                    } else if (unitAddress == '') {
                        displayMessage(message.unitaddress_required);
                        return;
                    } else if (validateMaxLength("unit_address", unitAddress, "Unit Address") == false) {
                        return;
                    } else if (unitPostalCode == '') {
                        displayMessage(message.unitpostal_required);
                        return;
                    } else if (validateMaxLength("unit_post_code", unitPostalCode, "Unit Postal Code") == false) {
                        return;
                    } else if (parseFloat(unitPostalCode) <= 0 || isNaN(parseFloat(unitPostalCode))) {
                        displayMessage(message.postal_invalid);
                        return;
                    } else if (unitdomain == '' || unitdomain == null) {
                        displayMessage(message.domain_required);
                        return;
                    } else if (unitIndustryId == '' || unitIndustryId == null) {
                        displayMessage(message.industryname_required);
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
                            for (var ij = 0; ij < unitdomain.length; ij++) {
                                unitdomains.push(parseInt(unitdomain[ij]));
                            }
                            for (var ij = 0; ij < unitdomains.length; ij++) {
                                for (var jk = 0; jk < unitIndustryId.length; jk++) {
                                    var list = {};
                                    for (var ind = 0; ind < industryList.length; ind++) {
                                        if (industryList[ind].industry_id == unitIndustryId[jk] && industryList[ind].domain_id == unitdomain[ij]) {
                                            list['domain_id'] = parseInt(unitdomain[ij]);
                                            list['industry_id'] = parseInt(unitIndustryId[jk]);
                                            var occ = -1;
                                            for(var oc=0;oc<unitIndustryIds.length;oc++){
                                                if(unitIndustryIds[oc].domain_id == parseInt(unitdomain[ij]) && unitIndustryIds[oc].industry_id == parseInt(unitIndustryId[jk])) {
                                                    occ = 1;
                                                    break;
                                                }
                                            }
                                            if (occ < 0){
                                                unitIndustryIds.push(list);
                                                break;
                                            }
                                        }
                                    }
                                }
                            }

                            unit = mirror.getUnitDict(null, unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitdomains, unitIndustryIds, 0);

                            units.push(unit);
                        } else {
                            displayMessage(message.unit_code_exists.replace('duplicates', duplicates));
                            return;
                        }
                    }
                    //}
                }
            } else {
                displayMessage(message.add_one_unit);
                return;
            }
        }
        displayLoader();
        mirror.saveClient(parseInt(groupNameValue), parseInt(bgIdValue), leIdValue, parseInt(countryVal), division_units, units, division_dict, function(error, response) {
            console.log(error, response)
            if (error == null) {
                displaySuccessMessage(message.unit_added);
                units_count = [];
                unitcodeautogenerateids = null;
                onSuccess(response);
                hideLoader();
            } else {
                onFailure(error);
                hideLoader();
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
                unitcode_err = true;
            } else if (error == 'CategoryNameAlreadyExists') {
                displayMessage(message.category_exists);
            } else if (error == 'SaveUnitFailure') {
                displayMessage(message.unit_failed);
            } else if (error == 'LegalEntityClosed') {
                displayMessage(message.le_closed);
            } else {
                displayMessage(error);
            }
        }

        client_id = $('#client-unit-id').val();
        bgIdValue = $('#businessgroup-update-id').val();
        leIdValue = $('#legalentity-update-id').val();
        countryVal = $('#country-id').val();

        if (le_contract_expiry < 0) {
            displayMessage(message.legal_entity_expired);
        } else if (le_approval == 0) {
            displayMessage(message.legal_entity_approval);
        }
        var division;
        var divIdValue;
        var divNameValue;

        var category = "null";

        var units = [];
        var division_units = [];
        var division_dict = [];
        var unitarr = [];
        var total_div = 0;
        var total_units = 0;
        var unitIndustryIds = [];
        var unitdomains = [];

        //check only for division, category updation
        for (var i = 1; i <= division_cnt; i++) {
            if (checkEditedRow(i) == false) {
                var divi_span_ctrl = $('.division-id-' + i + '-' + 1).attr('style');
                divisionValue = $('.divisionid-' + i + '-' + 1).val();
                divisiontextValue = $('.division-name-' + i + '-' + 1).val().trim();
                if (divisiontextValue == '' || divisiontextValue == "--") {
                    divIdValue = null;
                    divNameValue = null;
                    if (divisionValue != "") {
                        displayMessage(message.division_required);
                        return;
                    }
                } else {
                    divIdValue = parseInt(divisionValue);
                    divNameValue = divisiontextValue;
                    if (getDivisionName(divIdValue) != divNameValue) {
                        editDiv = true;
                    }
                }

                //get category values
                if ($('.category-name-' + i + '-' + 1).val() != '') {
                    category = $('.category-name-' + i + '-' + 1).val() + "|" + $('.categoryid-' + i + '-' + 1).val();
                    if ($('.category-name-' + i + '-' + 1).val() != '--') {
                        for (var ul = 0; ul < unitList.length; ul++) {
                            if (unitList[ul].category_id == $('.categoryid-' + i + '-' + 1).val()) {
                                if ($('.category-name-' + i + '-' + 1).val() != unitList[ul].category_name) {
                                    editCatg = true;
                                    break;
                                }
                            }
                        }
                    }
                } else {
                    if ($('.categoryid-' + i + '-' + 1).val() == "") {
                        displayMessage(message.catgname_required);
                        return;
                    } else {
                        category = null;
                    }
                }

                if (editDiv == true || editCatg == true) {
                    if (editDiv == true) {
                        if (validateMaxLength("division_name", divNameValue, "Division Name") == false) {
                            displayMessage(message.division_max);
                            return;
                        }
                    } else if (editCatg == true) {
                        if (validateMaxLength("category_name", category.split("|")[0], "Category Name") == false) {
                            displayMessage(message.category_max50);
                            return;
                        }
                    }
                    console.log(parseInt(client_id), parseInt(bgIdValue), parseInt(leIdValue), divIdValue, divNameValue, category)
                    div_arr = mirror.getDiviCatgDict(parseInt(client_id), parseInt(bgIdValue), parseInt(leIdValue), divIdValue, divNameValue, category)
                    division_dict.push(div_arr)
                    editDiv = false;
                    editCatg = false;
                }
            }
        }



        if (edited_ids.length > 0) {
            for (var i = 0; i < edited_ids.length; i++) {
                total_units = 0;
                index_i = edited_ids[i].split("-")[0];
                index_j = edited_ids[i].split("-")[1];
                unit_id = edited_ids[i].split("-")[2];
                //get division ctrl value
                var divi_span_ctrl = $('.division-id-' + index_i + '-' + 1).attr('style');

                divisionValue = $('.divisionid-' + index_i + '-' + 1).val();
                divisiontextValue = $('.division-name-' + index_i + '-' + 1).val().trim();
                if (divisiontextValue == '' || divisiontextValue == "--") {
                    divIdValue = null;
                    divNameValue = null;
                    if (divisionValue != "") {
                        displayMessage(message.division_required);
                        return;
                    }
                } else {
                    divIdValue = parseInt(divisionValue);
                    divNameValue = divisiontextValue;
                    if (getDivisionName(divIdValue) != divNameValue) {
                        editDiv = true;
                    }
                }

                //get category values
                if ($('.category-name-' + index_i + '-' + 1).val() != '') {
                    category = $('.category-name-' + index_i + '-' + 1).val() + "|" + $('.categoryid-' + index_i + '-' + 1).val();
                    if ($('.category-name-' + index_i + '-' + 1).val() != '--') {
                        for (var ul = 0; ul < unitList.length; ul++) {
                            if (unitList[ul].category_id == $('.categoryid-' + i + '-' + 1).val()) {
                                if ($('.category-name-' + index_i + '-' + 1).val() != unitList[ul].category_name) {
                                    editCatg = true;
                                    break;
                                }
                            }
                        }
                    }
                } else {
                    if ($('.categoryid-' + index_i + '-' + 1).val() == "") {
                        displayMessage(message.catgname_required);
                        return;
                    } else {
                        category = null;
                    }
                }
                var unitIndustryIds = [];
                var unitdomains = [];
                var unit;
                var unitId, unitCode, unitName, unitAddress, unitPostalCode, unitGeographyId;
                var unitLocation, unitIndustryId, unitdomain;

                edited = true;
                unitId = $('.unit-id-' + index_i + '-' + index_j).val();

                unitCode = $('.labelunitcode-' + index_i + '-' + index_j).text();
                unitName = $('.unit-name-' + index_i + '-' + index_j).val();
                unitAddress = $('.unit-address-' + index_i + '-' + index_j).val();
                unitPostalCode = $('.postal-code-' + index_i + '-' + index_j).val();
                unitGeographyId = $('.unitlocation-ids-' + index_i + '-' + index_j).val().trim();

                //i_ids = $('.edit_o_ids-' + index_i + '-' + index_j).val();

                //i_ids.push($('.orgtypeselected-' + index_i + '-' + index_j).val());
                /*var cu_ids = $('.orgtypeselected-' + index_i + '-' + index_j).val();
                jQuery.each(cu_ids, function(index, item) {
                    i_ids.push(item);
                });*/
                i_ids = [];
                var o_ctrl = $('.orgtypeselected-' + index_i + '-' + index_j)[0].options;
                for(var f=0;f<o_ctrl.length;f++){
                    if(o_ctrl[f].selected == true){
                        i_ids.push(o_ctrl[f].value);
                    }
                }
                unitIndustryId = i_ids;
                console.log(unitId, unitIndustryId)

                unitdomain = $('.domainselected-' + index_i + '-' + index_j).val();
                total_units = total_units + 1;
                if (unitGeographyId == '' && unitCode == '' && unitName == '' && unitAddress == '' && unitPostalCode == '' && unitdomain == '' && unitIndustryId == '') {
                    if (unitcount == 1) {
                        displayMessage(message.add_one_unit);
                        return;
                    }
                    continue;
                }
                if (unitName == '') {
                    displayMessage(message.unitname_required);
                    return;
                } else if (validateMaxLength("unit_name", unitName, "Unit Name") == false) {
                    return;
                } else if (unitAddress == '') {
                    displayMessage(message.unitaddress_required);
                    return;
                } else if (validateMaxLength("unit_address", unitAddress, "Unit Address") == false) {
                    return;
                } else if (unitPostalCode == '') {
                    displayMessage(message.unitpostal_required);
                    return;
                } else if (validateMaxLength("unit_post_code", unitPostalCode, "Unit Postal Code") == false) {
                    return;
                } else if (parseFloat(unitPostalCode) <= 0 || isNaN(parseFloat(unitPostalCode))) {
                    displayMessage(message.postal_invalid);
                    return;
                } else if (unitdomain == '' || unitdomain == null) {
                    displayMessage(message.domain_required);
                    return;
                } else if (unitIndustryId == '' || unitIndustryId == null) {
                    displayMessage(message.industryname_required);
                    return;
                } else {
                    var occur = -1;
                    for (var n = 0; n < unitarr.length; n++) {
                        if (unitarr[n] == unitCode) {
                            occur = 1;
                        }
                    }

                    if (occur < 0) {
                        unitarr.push(unitCode);
                    }
                    if (occur < 0) {
                        for (var ij = 0; ij < unitdomain.length; ij++) {
                            unitdomains.push(parseInt(unitdomain[ij]));
                        }
                        for (var ij = 0; ij < unitdomains.length; ij++) {
                            for (var jk = 0; jk < unitIndustryId.length; jk++) {
                                var list = {};
                                for (var ind = 0; ind < industryList.length; ind++) {
                                    if (industryList[ind].industry_id == unitIndustryId[jk] && industryList[ind].domain_id == unitdomain[ij]) {
                                        list['domain_id'] = parseInt(unitdomain[ij]);
                                        list['industry_id'] = parseInt(unitIndustryId[jk]);
                                        var occ = -1;
                                        for(var oc=0;oc<unitIndustryIds.length;oc++){
                                            if(unitIndustryIds[oc].domain_id == parseInt(unitdomain[ij]) && unitIndustryIds[oc].industry_id == parseInt(unitIndustryId[jk])) {
                                                occ = 1;
                                                break;
                                            }
                                        }
                                        if (occ < 0){
                                            unitIndustryIds.push(list);
                                            break;
                                        }
                                    }
                                }
                            }
                        }

                        if (total_div != i) {
                            total_div = total_div + 1;
                        }
                        console.log(parseInt(unitId), unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitdomains, unitIndustryIds, 0)
                        div_arr = mirror.getDivisionDict(parseInt(divIdValue), divNameValue, category, total_div, parseInt(total_units));
                        division_units.push(div_arr);
                        unit = mirror.getUnitDict(parseInt(unitId), unitName, unitCode, unitAddress, parseInt(unitPostalCode), parseInt(unitGeographyId), unitdomains, unitIndustryIds, 0);

                        units.push(unit);
                    } else {
                        displayMessage(message.unit_code_exists.replace('duplicates', duplicates));
                        return;
                    }
                }
            }
        }

        if (units.length > 0) {
            displayLoader();
            mirror.saveClient(parseInt(client_id), parseInt(bgIdValue), parseInt(leIdValue), parseInt(countryVal), division_units, units, division_dict, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.unit_updated);
                    units_count = [];
                    onSuccess(response);
                    hideLoader();
                } else {
                    onFailure(error);
                    hideLoader();
                }
            });
        } else if (division_dict.length > 0) {
            displayLoader();
            mirror.saveDivisionCategory(division_dict, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.div_catag_update);
                    division_dict = [];
                    onSuccess(response);
                    hideLoader();
                } else {
                    onFailure(error);
                    hideLoader();
                }
            });
        } else {
            displayMessage(message.no_updation);
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
// Form Initialization
$(function() {
    initialize();
    $(".table-fixed").stickyTableHeaders();
    //renderControls();
});
$(document).find('.js-filtertable-view').each(function() {
    $(this).filtertable().addFilter('.js-filter-view');
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
