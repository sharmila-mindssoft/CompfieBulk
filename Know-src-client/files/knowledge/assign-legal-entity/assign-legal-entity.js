var assignLegalEntitiesList = '';
var userList = '';
var CLIENT_ID = 0;

// Add screen fields
var AddScreen = $('#assign-le-add');
var ViewScreen = $('#assign-le-view');
var ListScreen = $('#assign-le-list');
var SaveButton = $('#save');
var CancelButton = $('.btn-cancel');

var User_id = $('#userid');
var User_val = $('#userval');
var Group_Label = $('.group-label');
var Country_Label = $('.country-label');

var ListFilterBox = $('.js-filter');
var AddFilterBox = $('.js-filter-add');
var AddFilterCountry = $('#add-filter-country');
var AddFilterBG = $('#add-filter-bg');
var AddFilterLE = $('#add-filter-le');

var AC_User = $('#ac-user');
var AC_Textbox = $('.ac-textbox');

var LE_DOMAINS = {};
var TESelected = [];

function resetValues() {
    ListFilterBox.val('');
    AddFilterBox.val('');
    Group_Label.text('');
    Country_Label.text('');
    User_val.val('');
    User_id.val('');
}

function processCancel() {
    AddScreen.hide();
    ViewScreen.hide();
    ListScreen.show();
    resetValues();
}

function processSave() {
    if (validateMandatory()) {
        displayLoader();
        SaveButton.prop("disabled",true);
        var s_users = [];
        var s_le = [];
        s_users.push(parseInt(User_id.val()));
        $('input[name="le"]:checked').each(function() {
            var splitIds = (this.value).split(',');
            s_le.push(parseInt(splitIds[1]));
        });
        mirror.saveAssignLegalEntity(CLIENT_ID, s_le, s_users, function(error, response) {
            if (error == null) {
                displaySuccessMessage(message.legalentity_assigned_success);
                AddScreen.hide();
                ListScreen.show();
                ViewScreen.hide();
                initialize();
            } else {
                SaveButton.prop("disabled",false);
                displayMessage(error);
                hideLoader();
            }
        });
    }
}

function assignLE(cId, cName, gName) {
    SaveButton.prop("disabled",false);
    CLIENT_ID = cId
    displayLoader();
    mirror.getEditAssignLegalEntity(cId, function(error, data) {
        if (error == null) {
            ListScreen.hide();
            AddScreen.show();
            Group_Label.text(gName);
            //Country_Label.text(cName);
            assignLegalEntitiesList = data.unassign_legal_entities;
            userList = data.mapped_techno_users;
            $(".select_all").prop('checked', false);
            $(".form_checkbox").prop('checked', false);
            $('.selected_checkbox_count').html('0');
            loadLegalEntityList(assignLegalEntitiesList);
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
}

function viewLE(cId, cName, gName) {
    CLIENT_ID = cId;
    displayLoader();
    mirror.viewAssignLegalEntity(cId, function(error, data) {
        if (error == null) {
            ListScreen.hide();
            AddScreen.hide();
            ViewScreen.show();
            Group_Label.text(gName);
            Country_Label.text(cName);
            console.log(data);
            assignLegalEntitiesList = data.view_assigned_legal_entities;
            loadUserList(assignLegalEntitiesList);
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
}

function loadGroupList(assignLegalEntitiesList) {
    var j = 1;
    $('.tbody-list').find('tr').remove();
    $.each(assignLegalEntitiesList, function(key, value) {
        var assignedLE = 0;
        var client_id = value.client_id;
        var groupName = value.group_name;
        var countryName = value.country_names;
        var legalEntityCount = value.no_of_legal_entities;
        if (value.no_of_assigned_legal_entities != null) assignedLE = value.no_of_assigned_legal_entities;
        var unAssignedLE = (legalEntityCount - assignedLE);

        var tableRow = $('#templates .table-assign-le-list .table-row');
        var clone = tableRow.clone();
        $('.sno', clone).text(j);
        $('.country', clone).text(countryName);
        $('.group', clone).text(groupName);
        $('.unassigned-le', clone).text(unAssignedLE + ' / ' + legalEntityCount);
        if (unAssignedLE > 0) {
            $('.assign', clone).on('click', function() {
                assignLE(client_id, countryName, groupName);
            });
        }else{
            $('.assign', clone).hide();
        }
        if (unAssignedLE != legalEntityCount) {
            $('.view', clone).on('click', function() {
                viewLE(client_id, countryName, groupName);
            });
        }else{
            $('.view', clone).hide();
        }
        $('.tbody-list').append(clone);
        j = j + 1;
    });

    if(j == 1){
        var no_record_row = $("#templates .table-no-record tr");
        var no_clone = no_record_row.clone();
        $('.tbody-list').append(no_clone);
    }
    hideLoader();
}

$(".select_all").change(function() {
    $(".tbody-add-list .form_checkbox").prop('checked', $(this).prop("checked"));
    $('.selected_checkbox_count').html($('.form_checkbox:checked').length);
    getValidCountries();
});

function loadLegalEntityList(assignLegalEntitiesList) {
    LE_DOMAINS = {};
    var j = 1;
    $('.tbody-add-list').find('tr').remove();
    $.each(assignLegalEntitiesList, function(key, value) {
        var assignedLE = 0;
        var leId = value.legal_entity_id;
        var leName = value.legal_entity_name;
        var bgName = '-';
        if (value.business_group_name != null) bgName = value.business_group_name;
        var cName = value.c_name;
        var cId = value.c_id;
        var combileId = cId + ',' + leId;

        var tableRow = $('#templates .table-assign-le-add .table-row');
        var clone = tableRow.clone();
        $('.ck-box', clone).attr('id', 'legalentity' + j);
        $('.ck-box', clone).val(combileId);
        $('.add-country', clone).text(cName);
        $('.add-bgroup', clone).text(bgName);
        $('.add-le', clone).text(leName);

        $('.tbody-add-list').append(clone);
        j = j + 1;
        $('.form_checkbox').on('click', function(e) {
            $('#usersSelected').val('');
            var che = $('.form_checkbox:checked');
            $('.selected_checkbox_count').html(che.length);
            $('.form_checkbox').closest('tr').removeClass('checked_row');
            che.closest('tr').addClass('checked_row');
            getValidCountries();
        });
        LE_DOMAINS[value.legal_entity_id] = value.domain_ids;
    });
    
    if($('.select_all').prop('checked')){
        $(".tbody-add-list .form_checkbox").prop('checked', true);
        $('.selected_checkbox_count').html($('.form_checkbox:checked').length);
        getValidCountries();
    }else{
        $('.selected_checkbox_count').html('0');
    }
    hideLoader();
}

function loadUserList(assignLegalEntitiesList) {
    var LastName = '';
    var j = 1;
    $('.tbody-view-list').find('tr').remove();
    $.each(assignLegalEntitiesList, function(key, value) {
        var leName = value.legal_entity_name;
        var bgName = '-';
        if (value.business_group_name != null) bgName = value.business_group_name;
        var cName = value.c_name;

        if(LastName != value.employee_name){
            var tableRow = $('#templates .table-assign-le-view .table-row-name');
            var clone1 = tableRow.clone();
            $('.emp-name', clone1).text(value.employee_name);
            $('.tbody-view-list').append(clone1);
            LastName = value.employee_name;
        }

        var tableRow = $('#templates .table-assign-le-view .table-row');
        var clone = tableRow.clone();
        $('.view-country', clone).text(cName);
        $('.view-bgroup', clone).text(bgName);
        $('.view-le', clone).text(leName);
        $('.tbody-view-list').append(clone);
        j = j + 1;
    });
    hideLoader();
}

function getValidCountries() {
    TESelected = [];
    var TEDuplicate = [];
    $('input[name="le"]:checked').each(function() {
        var splitIds = (this.value).split(',');
        var c_id = parseInt(splitIds[0]);
        var le_id = parseInt(splitIds[1]);
        var d_ids = LE_DOMAINS[le_id];

        for(var i=0; i<d_ids.length; i++){
            var te = c_id +'-'+ d_ids[i] ;
            if ($.inArray(te, TEDuplicate) == -1) {
                var LEData = {
                    'c_id': c_id,
                    'd_id': d_ids[i],
                }
                TEDuplicate.push(te);
                TESelected.push(LEData);
            }
            
        }
        //alert(TESelected.length)
    });
}

function validateMandatory() {
    if ($('.form_checkbox:checked').length == 0) {
        displayMessage(message.no_legal_entity_selected);
        return false;
    } else if (User_id.val().length == 0) {
        displayMessage(message.techno_executive_required);
        return false;
    } else {
        return true;
    }
}

//filter process
/*function processListFilter() {
    var countryfilter = ListFilterCountry.val().toLowerCase();
    var groupfilter = ListFilterGroup.val().toLowerCase();
    var filteredList = [];
    for (var entity in assignLegalEntitiesList) {
        var countryName = assignLegalEntitiesList[entity].country_name;
        var groupName = assignLegalEntitiesList[entity].group_name;
        if (~countryName.toLowerCase().indexOf(countryfilter) && ~groupName.toLowerCase().indexOf(groupfilter)) {
            filteredList.push(assignLegalEntitiesList[entity]);
        }
    }
    loadGroupList(filteredList);
}*/

function processAddFilter() {
    var addcountryfilter = AddFilterCountry.val().toLowerCase();
    var bgfilter = AddFilterBG.val().toLowerCase();
    var lefilter = AddFilterLE.val().toLowerCase();

    var filteredList = [];
    for (var entity in assignLegalEntitiesList) {
        var countryName = assignLegalEntitiesList[entity].c_name;
        var bgName = '-';
        if(assignLegalEntitiesList[entity].business_group_name != null){
            bgName = assignLegalEntitiesList[entity].business_group_name;
        }
        var leName = assignLegalEntitiesList[entity].legal_entity_name;
        if (~countryName.toLowerCase().indexOf(addcountryfilter) && ~bgName.toLowerCase().indexOf(bgfilter) && ~leName.toLowerCase().indexOf(lefilter)) {
            filteredList.push(assignLegalEntitiesList[entity]);
        }
    }
    loadLegalEntityList(filteredList);
}

function initialize() {
    displayLoader();
    resetValues();
    mirror.getAssignLegalEntityList(function(error, data) {
        if (error == null) {
            assignLegalEntitiesList = data.assign_le_list;
            loadGroupList(assignLegalEntitiesList);
        } else {
            custom_alert(error);
            hideLoader();
        }
    });
}

function activate_technouser(element) {
    AC_Textbox.hide();
    var ac_id = $(element).attr('id');
    var ac_name = $(element).text();
    User_val.val(ac_name);
    User_id.val(ac_id);
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();    
}

function pageControls() {

    CancelButton.click(function() {
        processCancel();
    });

    SaveButton.click(function() {
        processSave();
    });

    /*ListFilterBox.keyup(function() {
        processListFilter();
    });*/

    AddFilterBox.keyup(function() {
        processAddFilter();
    });

    User_val.keyup(function(e) {
        var text_val = $(this).val();
        var condition_fields = ["mapped_country_domains"];
        var condition_values = [TESelected];
        commonAutoComplete1(
            e, AC_User, User_id, text_val,
            userList, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(User_val, User_id, val);
            }, condition_fields, condition_values);
    });
}
$(document).ready(function() {
    initialize();
    pageControls();
});
$(document).find('.js-filtertable').each(function() {
    $(this).filtertable().addFilter('.js-filter');
});
/*$(document).find('.js-filtertable-add').each(function() {
    $(this).filtertable().addFilter('.js-filter-add');
});*/
