
var TECHNO_MANAGERS = '';
var TECHNO_USERS = '';
var DOMAIN_MANAGERS = '';
var DOMAIN_USERS = '';
var GROUPS = '';
var BUSINESS_GROUPS = '';
var LEGAL_ENTITIES = '';
var DOMAINS = '';
var USER_CATEGORIES = '';

var selected_textbox = '';
var selected_textid = '';
var d_id = '';
var c_id = '';

var TechnoManagerName = $("#techno_manager_name");
var TechnoManagerId = $("#techno_manager_id");
var ACTechnoManager = $("#ac-techno-manager");
var TMShow = $(".tm-show-btn");
var TMSubmit = $(".btn-submit-1");
var TechnoDetailsList = '';
var TMRemarks = $("#tm_remarks");

var TechnoExecutiveName = $("#techno_executive_name");
var TechnoExecutiveId = $("#techno_executive_id");
var ACTechnoExecutive = $("#ac-techno-executive");
var RTechnoExecutiveName = $("#te_techno_executive_name");
var RTechnoExecutiveId = $("#te_techno_executive_id");
var RACTechnoExecutive = $("#te-ac-techno-executive");
var TERemarks = $("#te_remarks");
var TEShow = $(".te-show-btn");
var TESubmit = $(".btn-submit-2");

var DomainManagerName = $("#domain_manager_name");
var DomainManagerId = $("#domain_manager_id");
var ACDomainManager = $("#ac-domain-manager");
var DMGroupName = $("#dm_group_name");
var DMGroupId = $("#dm_group_id");
var DMACGroup = $("#ac-dm-group");
var DMBusinessGroupName = $("#dm_business_group_name");
var DMBusinessGroupId = $("#dm_business_group_id");
var DMACBusinessGroup = $("#ac-dm-business-group");
var DMLegalEntityName = $("#dm_legal_entity_name");
var DMLegalEntityId = $("#dm_legal_entity_id");
var DMACLegalEntity = $("#ac-dm-legal-entity");
var DMDomainName = $("#dm_domain_name");
var DMDomainId = $("#dm_domain_id");
var DMACDomain = $("#ac-dm-domain");
var DMShow = $(".dm-show-btn");
var DMSubmit = $(".btn-submit-3");
var DomainDetailsList = '';
var DMRemarks = $("#dm_remarks");

var DomainExecutiveName = $("#domain_executive_name");
var DomainExecutiveId = $("#domain_executive_id");
var ACDomainExecutive = $("#ac-domain-executive");
var RDomainExecutiveName = $("#de_domain_executive_name");
var RDomainExecutiveId = $("#de_domain_executive_id");
var RACDomainExecutive = $("#de-ac-domain-executive");
var DEGroupName = $("#de_group_name");
var DEGroupId = $("#de_group_id");
var DEACGroup = $("#ac-de-group");
var DEBusinessGroupName = $("#de_business_group_name");
var DEBusinessGroupId = $("#de_business_group_id");
var DEACBusinessGroup = $("#ac-de-business-group");
var DELegalEntityName = $("#de_legal_entity_name");
var DELegalEntityId = $("#de_legal_entity_id");
var DEACLegalEntity = $("#ac-de-legal-entity");
var DEDomainName = $("#de_domain_name");
var DEDomainId = $("#de_domain_id");
var DEACDomain = $("#ac-de-domain");
var DEShow = $(".de-show-btn");
var DESubmit = $(".btn-submit-4");
var DERemarks = $("#de_remarks");


var ReplaceManagerShow = $(".replace-manager-show-btn");
var ReplaceManagerSubmit = $(".btn-submit-5");
var ReplaceManagerRemarks = $("#replace_manager_remarks");
var ManagerCategory = '';
var ManagerId = '';
var ReplaceManagerId = '';

//retrive businessgroup form autocomplete value
function clearData(){
    $('.tbody-tm-view').empty();
    $('.tbody-te-view').empty();
    $('.tbody-dm-view').empty();
    $('.tbody-de-view').empty();
    TMRemarks.val('');
    TERemarks.val('');
    DMRemarks.val('');
    DERemarks.val('');
    ReplaceManagerRemarks.val('');
    d_id = '';
    c_id = '';
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
}

function loadTMList(){
        var LastGroup = '';
        var group_countries = {};
        var group_domains = {};

        $.each(TechnoDetailsList, function(key, value) {
            if(LastGroup != value.ct_name){
                var grouptableRow = $('#templates .tm-view-row .tm-view-group-row');
                var clone = grouptableRow.clone();

                $('.tm-group-checkbox', clone).val(value.ct_id);
                $('.tm-group', clone).text(value.ct_name);
                $('.tm-ac-view', clone).addClass('tm-ac-'+value.ct_id);

                $('.tm-techno-manager-name', clone).attr('id', 'techno_manager_name_'+value.ct_id);
                $('.techno_manager_id', clone).attr('id', 'techno_manager_id_'+value.ct_id);
                $('.ac-techno-manager', clone).attr('id', 'ac-techno-manager-'+value.ct_id);

                $('.tm-techno-manager-name', clone).keyup(function(e){
                    var condition_fields = ["country_domains"];
                    var condition_values1 = [group_countries[value.ct_id]];
                    var condition_values2 = group_domains[value.ct_id];

                    var text_val = $(this).val();
                    selected_textbox = $(this);
                    selected_textid = $("#techno_manager_id_"+value.ct_id);

                    commonAutoComplete1(
                        e, $("#ac-techno-manager-"+value.ct_id), $("#techno_manager_id_"+value.ct_id), text_val,
                        TECHNO_MANAGERS, "employee_name", "user_id",  function (val) {
                            onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                        }, condition_fields, condition_values1, condition_values2);
                });

                $('.tbody-tm-view').append(clone);
                LastGroup = value.ct_name;

                group_countries[value.ct_id] = [];
                group_domains[value.ct_id] = [];
            }

            group_countries[value.ct_id] = group_countries[value.ct_id].push(value.c_id);
            group_domains[value.ct_id] = $.merge(group_domains[value.ct_id], value.d_ids);

            var letableRow = $('#templates .tm-view-row .tm-view-le-row');
            var clone = letableRow.clone();
            $('.tm-country', clone).text(value.c_name);
            $('.tm-le', clone).text(value.le_name);
            $('.te-ac-view', clone).addClass('te-ac-'+value.ct_id);

            $('.tm-techno-executive-name', clone).attr('id', 'techno_executive_name_'+value.le_id);
            $('.techno_executive_id', clone).attr('id', 'techno_executive_id_'+value.le_id);
            $('.ac-techno-executive', clone).attr('id', 'ac-techno-executive-'+value.le_id);
            $('.techno_executive_id', clone).addClass('group_le_'+value.ct_id);
            $('.old_executive_id', clone).attr('id', 'old_executive_id_'+value.le_id);
            $('.old_executive_id', clone).val(value.executive_id);

            

            $('.tm-techno-executive-name', clone).keyup(function(e){
                var condition_fields = ["country_domains"];
                var condition_values1 = [value.c_id];
                var condition_values2 = value.d_ids;

                var text_val = $(this).val();
                selected_textbox = $(this);
                selected_textid = $("#techno_executive_id_"+value.le_id);

                commonAutoComplete1(
                    e, $("#ac-techno-executive-"+value.le_id), $("#techno_executive_id_"+value.le_id), text_val,
                    TECHNO_USERS, "employee_name", "user_id", function (val) {
                        onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                    }, condition_fields, condition_values1, condition_values2);
            });
        
            $('.tbody-tm-view').append(clone);
        });

        console.log(group_countries)
        console.log(group_domains)
        $('.tm-group-checkbox').on('click', function(e) {
            var tm_view = '.tm-ac-' + $(this).val();
            var te_view = '.te-ac-' + $(this).val();
            if($(this).prop("checked")){
                $(tm_view).show();
                $(te_view).show();
            }else{
                $(tm_view).hide();
                $(te_view).hide();
            }
        });
}

function loadTEList(){
        $.each(TechnoDetailsList, function(key, value) {
            var letableRow = $('#templates .te-view-row .te-view-le-row');
            var clone = letableRow.clone();

            $('.te-group-checkbox', clone).val(value.ct_id + '-' + value.le_id);
            $('.te-group', clone).text(value.ct_name);
            var bg_name = '-';
            if(value.bg_name != null){
                bg_name = value.bg_name;
            }
            $('.te-businessgroup', clone).text(bg_name);
            $('.te-country', clone).text(value.c_name);
            $('.te-le', clone).text(value.le_name);
            $('.tbody-te-view').append(clone);
        });
}

function loadDMList(){
        var LastLE = '';
        var group_countries = {};
        var group_domains = {};

        $.each(DomainDetailsList, function(key, value) {
            if(LastLE != value.le_name){
                var letableRow = $('#templates .dm-view-row .dm-view-le-row');
                var clone = letableRow.clone();

                $('.dm-group-checkbox-main', clone).val(value.le_id);
                $('.dm-le', clone).text(value.le_name);
                //$('.dm-ac-view', clone).addClass('dm-ac-'+value.le_id);

                $('.dm-domain-manager-name', clone).attr('id', 'domain_manager_name_'+value.le_id);
                $('.domain_manager_id', clone).attr('id', 'domain_manager_id_'+value.le_id);
                $('.ac-domain-manager', clone).attr('id', 'ac-domain-manager-'+value.le_id);

                $('.dm-domain-manager-name', clone).keyup(function(e){
                    var condition_fields = ["country_domains"];
                    var condition_values1 = [c_id];
                    var condition_values2 = [d_id];

                    var text_val = $(this).val();
                    selected_textbox = $(this);
                    selected_textid = $("#domain_manager_id_"+value.le_id);

                    commonAutoComplete1(
                        e, $("#ac-domain-manager-"+value.le_id), $("#domain_manager_id_"+value.le_id), text_val,
                        DOMAIN_MANAGERS, "employee_name", "user_id",  function (val) {
                            onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                        }, condition_fields, condition_values1, condition_values2);
                });

                $('.tbody-dm-view').append(clone);
                LastLE = value.le_name;
            }

            var unittableRow = $('#templates .dm-view-row .dm-view-unit-row');
            var clone = unittableRow.clone();

            $('.dm-group-checkbox', clone).val(value.u_id);
            
            $('.dm-unitcode', clone).text(value.u_code);
            $('.dm-unitname', clone).text(value.u_name);
            $('.dm-unitaddress', clone).attr('title', value.address);
            $('.dm-unitlocation', clone).text(value.location);
            $('.de-ac-view', clone).addClass('de-ac-'+value.u_id);
            
            $('.dm-domain-executive-name', clone).attr('id', 'domain_executive_name_'+value.u_id);
            $('.domain_executive_id', clone).attr('id', 'domain_executive_id_'+value.u_id);
            $('.ac-domain-executive', clone).attr('id', 'ac-domain-executive-'+value.u_id);
            $('.domain_executive_id', clone).addClass('group_le_'+value.u_id);
            $('.d_old_executive_id', clone).attr('id', 'd_old_executive_id_'+value.u_id);
            $('.d_old_executive_id', clone).val(value.executive_id);

            $('.dm-domain-executive-name', clone).keyup(function(e){
                var condition_fields = ["country_domains"];
                var condition_values1 = [c_id];
                var condition_values2 = [d_id];

                var text_val = $(this).val();
                selected_textbox = $(this);
                selected_textid = $("#domain_executive_id_"+value.le_id);

                commonAutoComplete1(
                    e, $("#ac-domain-executive-"+value.u_id), $("#domain_executive_id_"+value.u_id), text_val,
                    DOMAIN_USERS, "employee_name", "user_id", function (val) {
                        onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                    }, condition_fields, condition_values1, condition_values2);
            });
        
            $('.tbody-dm-view').append(clone);
        });

        $('.dm-group-checkbox').on('click', function(e) {
            var de_view = '.de-ac-' + $(this).val();
            if($(this).prop("checked")){
                $(de_view).show();
            }else{
                $(de_view).hide();
            }
        });
}

function loadDEList(){
    $.each(DomainDetailsList, function(key, value) {
        var unittableRow = $('#templates .de-view-row .de-view-unit-row');
        var clone = unittableRow.clone();

        $('.de-group-checkbox', clone).val(value.u_id);
        
        $('.de-unitcode', clone).text(value.u_code);
        $('.de-unitname', clone).text(value.u_name);
        $('.de-unitaddress', clone).attr('title', value.address);
        $('.de-unitlocation', clone).text(value.location);
        
        $('.tbody-de-view').append(clone);
    });
}

function callTechnoUserInfo(userId, type){
    mirror.getTechnoUSerInfo(userId, function(error, response) {
        if (error == null) {
            TechnoDetailsList = response.t_user_info;
            if(type == 'TM'){
                loadTMList();
            }else{
                loadTEList();
            }
        } else {
            displayMessage(error);
        }
    });

}

function callDomainUserInfo(userId, groupId, legalentityId, domainId, type){
    mirror.getDomainUserInfo(userId, groupId, legalentityId, domainId, function(error, response) {
        if (error == null) {
            DomainDetailsList = response.d_user_info;
            if(type == 'DM'){
                loadDMList();
            }else{
                loadDEList();
            }
        } else {
            displayMessage(error);
        }
    });

}

function getCountryId(l_Id){
    var country_id = '';
    $.each(LEGAL_ENTITIES, function(key, value) {
        if(value.legal_entity_id == parseInt(l_Id)){
            country_id = value.country_id;
        }
    });
    return country_id;
}

function pageControls(){
    TechnoManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACTechnoManager, TechnoManagerId, text_val,
            TECHNO_MANAGERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(TechnoManagerName, TechnoManagerId, val);
            });
    });

    TechnoExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACTechnoExecutive, TechnoExecutiveId, text_val,
            TECHNO_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(TechnoExecutiveName, TechnoExecutiveId, val);
            });
    });

    RTechnoExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, RACTechnoExecutive, RTechnoExecutiveId, text_val,
            TECHNO_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(RTechnoExecutiveName, RTechnoExecutiveId, val);
            });
    });

    DomainManagerName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomainManager, DomainManagerId, text_val,
            DOMAIN_MANAGERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(DomainManagerName, DomainManagerId, val);
            });
    });

    DMGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_closed"];
        var condition_values = [false];
        commonAutoComplete(
            e, DMACGroup, DMGroupId, text_val,
            GROUPS, "group_name", "group_id", function (val) {
                onAutoCompleteSuccess(DMGroupName, DMGroupId, val);
            }, condition_fields, condition_values);
    });

    DMBusinessGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if(DMGroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(DMGroupId.val());
        }
        commonAutoComplete(
            e, DMACBusinessGroup, DMBusinessGroupId, text_val,
            BUSINESS_GROUPS, "business_group_name", "business_group_id",
            function (val) {
                onAutoCompleteSuccess(DMBusinessGroupName, DMBusinessGroupId, val);
            }, condition_fields, condition_values);
    });

    DMLegalEntityName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if(DMGroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(DMGroupId.val());
        }
        if(DMBusinessGroupId.val() != ''){
            condition_fields.push("business_group_id");
            condition_values.push(DMBusinessGroupId.val());
        }
        commonAutoComplete(
            e, DMACLegalEntity, DMLegalEntityId, text_val,
            LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
            function (val) {
                onAutoCompleteSuccess(DMLegalEntityName, DMLegalEntityId, val)
            }, condition_fields, condition_values);
    })

    DMDomainName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, DMACDomain, DMDomainId, text_val,
            DOMAINS, "domain_name", "domain_id",
            function (val) {
                onAutoCompleteSuccess(DMDomainName, DMDomainId, val)
            }, condition_fields, condition_values);
    });

    DomainExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomainExecutive, DomainExecutiveId, text_val,
            DOMAIN_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(DomainExecutiveName, DomainExecutiveId, val);
            });
    });

    RDomainExecutiveName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["country_domains"];
        var condition_values1 = [1];
        var condition_values2 = [1];

        commonAutoComplete1(
            e, RACDomainExecutive, RDomainExecutiveId, text_val,
            DOMAIN_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(RDomainExecutiveName, RDomainExecutiveId, val);
            }, condition_fields, condition_values1, condition_values2);
    });


    DEGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_closed"];
        var condition_values = [false];
        commonAutoComplete(
            e, DEACGroup, DEGroupId, text_val,
            GROUPS, "group_name", "group_id", function (val) {
                onAutoCompleteSuccess(DEGroupName, DEGroupId, val);
            }, condition_fields, condition_values);
    });

    DEBusinessGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if(DEGroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(DEGroupId.val());
        }
        commonAutoComplete(
            e, DEACBusinessGroup, DEBusinessGroupId, text_val,
            BUSINESS_GROUPS, "business_group_name", "business_group_id",
            function (val) {
                onAutoCompleteSuccess(DEBusinessGroupName, DEBusinessGroupId, val);
            }, condition_fields, condition_values);
    });

    DELegalEntityName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = [];
        var condition_values = [];
        if(DEGroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(DEGroupId.val());
        }
        if(DEBusinessGroupId.val() != ''){
            condition_fields.push("business_group_id");
            condition_values.push(DEBusinessGroupId.val());
        }
        commonAutoComplete(
            e, DEACLegalEntity, DELegalEntityId, text_val,
            LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
            function (val) {
                onAutoCompleteSuccess(DELegalEntityName, DELegalEntityId, val)
            }, condition_fields, condition_values);
    })

    DEDomainName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
            e, DEACDomain, DEDomainId, text_val,
            DOMAINS, "domain_name", "domain_id",
            function (val) {
                onAutoCompleteSuccess(DEDomainName, DEDomainId, val)
            }, condition_fields, condition_values);
    });

    TMShow.click(function(){
        clearData();
        if(TechnoManagerId.val() == ''){
            displayMessage(message.reassign_from_required)
        }else{
            callTechnoUserInfo(parseInt(TechnoManagerId.val()), 'TM');
        }
    });

    TEShow.click(function(){
        clearData();
        if(TechnoExecutiveId.val() == ''){
            displayMessage(message.reassign_from_required)
        }else{
            callTechnoUserInfo(parseInt(TechnoExecutiveId.val()), 'TE');
        }
    });

    DMShow.click(function(){
        clearData();
        var dm_id = DomainManagerId.val();
        var group_id = DMGroupId.val();
        var le_id = DMLegalEntityId.val();
        var domain_id = DMDomainId.val();

        d_id = parseInt(domain_id);
        c_id = getCountryId(le_id)

        if(dm_id == ''){
            displayMessage(message.reassign_from_required);
        }else if(group_id == ''){
            displayMessage(message.group_required);
        }else if(le_id == ''){
            displayMessage(message.legalentity_required);
        }else if(domain_id == ''){
            displayMessage(message.domain_required);
        }else{
            callDomainUserInfo(parseInt(dm_id), parseInt(group_id), parseInt(le_id), parseInt(domain_id), 'DM');
        }
    });

    DEShow.click(function(){
        clearData();
        var de_id = DomainExecutiveId.val();
        var group_id = DEGroupId.val();
        var le_id = DELegalEntityId.val();
        var domain_id = DEDomainId.val();

        if(de_id == ''){
            displayMessage(message.reassign_from_required);
        }else if(group_id == ''){
            displayMessage(message.group_required);
        }else if(le_id == ''){
            displayMessage(message.legalentity_required);
        }else if(domain_id == ''){
            displayMessage(message.domain_required);
        }else{
            callDomainUserInfo(parseInt(de_id), parseInt(group_id), parseInt(le_id), parseInt(domain_id), 'DE');
        }
    });

    ReplaceManagerShow.click(function(){
        clearData();
        var category = $('#category').val();
        if(category == '1'){
            loadManagerList(TECHNO_MANAGERS);
            $('.user-title').text('Techno Manager');
        }else{
            loadManagerList(DOMAIN_MANAGERS);
            $('.user-title').text('Domain Manager');
        }
    });

    TMSubmit.click(function(){
        var reassignDetails = [];
        var reassign_from = TechnoManagerId.val();
        var tm_remarks = TMRemarks.val();
        var isValidate = false;

        if(reassign_from == ''){
            displayMessage(message.reassign_from_required);
            return false;
        }else{
            if($('.tm-group-checkbox:checkbox:checked').length > 0){
                $('.tm-group-checkbox:checkbox:checked').each(function (index, el) {
                    var group_id = $(this).val();
                    var reassign_to = $("#techno_manager_id_"+group_id).val();
                    if(reassign_to == ''){
                        displayMessage(message.reassign_to_tm_required)
                        return false;
                    }else{
                        $('.group_le_'+group_id).each(function (i, element) {
                            var selected_id = $(element).attr('id');
                            var legal_entity_id = selected_id.substr(selected_id.lastIndexOf('_') + 1);
                            var te_id = $(element).val();
                            var old_executive_id = $('#old_executive_id_'+legal_entity_id).val();

                            if(te_id == ''){
                                displayMessage(message.reassign_to_te_required);
                                return false;
                            }else{
                                if(tm_remarks == ''){
                                    displayMessage(message.remarks_required);
                                    return false;
                                }else{
                                    if(reassign_from == reassign_to){
                                        displayMessage(message.reassign_from_reassign_to_both_are_same);
                                        return false;
                                    }else{
                                        reassignDetailsData = mirror.technoManagerInfo(parseInt(reassign_to), parseInt(group_id),
                                            parseInt(legal_entity_id), parseInt(te_id), parseInt(old_executive_id));
                                        reassignDetails.push(reassignDetailsData);
                                        isValidate = true;
                                    }
                                }
                            }
                        });
                    }
                });
                if(isValidate){
                    mirror.ReassignTechnoManager(parseInt(reassign_from), reassignDetails, tm_remarks, 
                        function(error, response) {
                        if (error == null) {
                            displaySuccessMessage(message.reassign_users_account_success);
                            TMShow.trigger( "click" );
                        } else {
                            displayMessage(error);
                        }
                    });
                }
                
            }else{
                displayMessage(message.no_records_selected_for_reassign);
            }
            
        }
    });

    TESubmit.click(function(){
        var reassignDetails = [];
        var reassign_from = TechnoExecutiveId.val();
        var reassign_to = RTechnoExecutiveId.val();
        var te_remarks = TERemarks.val();
        var isValidate = false;

        if(reassign_from == ''){
            displayMessage(message.reassign_from_required);
            return false;
        }else{
            if($('.te-group-checkbox:checkbox:checked').length > 0){
                $('.te-group-checkbox:checkbox:checked').each(function (index, el) {
                    var combile_id = $(this).val().split('-');
                    var group_id = combile_id[0];
                    var le_id = combile_id[1];
                    
                    if(reassign_to == ''){
                        displayMessage(message.reassign_to_te_required)
                        return false;
                    }else{
                        if(te_remarks == ''){
                            displayMessage(message.remarks_required);
                            return false;
                        }else{
                            reassignDetailsData = mirror.technoExecutiveInfo(parseInt(group_id),
                                parseInt(le_id));
                            reassignDetails.push(reassignDetailsData);
                            isValidate = true;
                        }
                    }
                });
                if(isValidate){
                    if(reassign_from == reassign_to){
                        displayMessage(message.reassign_from_reassign_to_both_are_same);
                        return false;
                    }else{

                        mirror.ReassignTechnoExecutive(parseInt(reassign_from), parseInt(reassign_to), 
                            reassignDetails, te_remarks, 
                            function(error, response) {
                            if (error == null) {
                                displaySuccessMessage(message.reassign_users_account_success);
                                TEShow.trigger( "click" );
                            } else {
                                displayMessage(error);
                            }
                        });
                    }
                }
                
            }else{
                displayMessage(message.no_records_selected_for_reassign);
            }
            
        }
    });

    DMSubmit.click(function(){
        var reassignDetails = [];
    
        var reassign_from = DomainManagerId.val();
        var group_id = DMGroupId.val();
        var le_id = DMLegalEntityId.val();
        var domain_id = DMDomainId.val();
        var dm_remarks = DMRemarks.val();
        var isValidate = false;

        if(reassign_from == ''){
            displayMessage(message.reassign_from_required);
        }else if(group_id == ''){
            displayMessage(message.group_required);
        }else if(le_id == ''){
            displayMessage(message.legalentity_required);
        }else if(domain_id == ''){
            displayMessage(message.domain_required);
        }else if(dm_remarks == ''){
            displayMessage(message.remarks_required);
        }else{
            if($('.dm-group-checkbox:checkbox:checked').length > 0){
                var reassign_to = $('#domain_manager_id_'+le_id).val();
                if(reassign_to == ''){
                    displayMessage(message.reassign_to_dm_required);
                    return false;
                }else{
                    $('.dm-group-checkbox:checkbox:checked').each(function (index, el) {
                        var u_id = $(this).val();
                        var de_id = $('#domain_executive_id_'+u_id).val();
                        var old_executive_id = $('#d_old_executive_id_'+u_id).val();

                        if(de_id == ''){
                            displayMessage(message.reassign_to_de_required);
                            return false;
                        }else{
                            reassignDetailsData = mirror.domainManagerInfo(parseInt(u_id), parseInt(de_id), parseInt(old_executive_id));
                            reassignDetails.push(reassignDetailsData);
                            isValidate = true;
                        }
                    });
                }

                if(isValidate){
                    if(reassign_from == reassign_to){
                        displayMessage(message.reassign_from_reassign_to_both_are_same);
                        return false;
                    }else{
                        mirror.ReassignDomainManager(parseInt(reassign_from), parseInt(reassign_to), parseInt(group_id),
                            parseInt(le_id), parseInt(domain_id), reassignDetails, dm_remarks, function(error, response) {
                            if (error == null) {
                                displaySuccessMessage(message.reassign_users_account_success);
                                DMShow.trigger( "click" );
                            } else {
                                displayMessage(error);
                            }
                        });
                    }
                }
                
            }else{
                displayMessage(message.no_records_selected_for_reassign);
            }
        }
    });

    DESubmit.click(function(){
    
        var reassign_from = DomainExecutiveId.val();
        var reassign_to = RDomainExecutiveId.val();
        var group_id = DEGroupId.val();
        var le_id = DELegalEntityId.val();
        var domain_id = DEDomainId.val();
        var de_remarks = DERemarks.val();

        if(reassign_from == ''){
            displayMessage(message.reassign_from_required);
        }else if(group_id == ''){
            displayMessage(message.group_required);
        }else if(le_id == ''){
            displayMessage(message.legalentity_required);
        }else if(domain_id == ''){
            displayMessage(message.domain_required);
        }else if(reassign_to == ''){
            displayMessage(message.reassign_to_required);
        }else if(de_remarks == ''){
            displayMessage(message.remarks_required);
        }else{
            if($('.de-group-checkbox:checkbox:checked').length > 0){
                var u_ids = [];
                $('.de-group-checkbox:checkbox:checked').each(function (index, el) {
                    var u_id = $(this).val();
                    u_ids.push(parseInt(u_id))
                });
                
                if(reassign_from == reassign_to){
                    displayMessage(message.reassign_from_reassign_to_both_are_same);
                    return false;
                }else{
                    mirror.ReassignDomainExecutive(parseInt(reassign_from), parseInt(reassign_to), parseInt(group_id),
                        parseInt(le_id), parseInt(domain_id), u_ids, de_remarks, function(error, response) {
                        if (error == null) {
                            displaySuccessMessage(message.reassign_users_account_success);
                            DEShow.trigger( "click" );
                        } else {
                            displayMessage(error);
                        }
                    });
                }
                
            }else{
                displayMessage(message.no_records_selected_for_reassign);
            }
        }
    });

    ReplaceManagerSubmit.click(function(){
        var replace_remarks = ReplaceManagerRemarks.val();

        if(ManagerId == ''){
            displayMessage(message.reassign_from_required);
        }else if(ReplaceManagerId == ''){
            displayMessage(message.reassign_to_required);
        }else if(replace_remarks == ''){
            displayMessage(message.remarks_required);
        }else{
            mirror.SaveUserReplacement(5, parseInt(ManagerId), parseInt(ReplaceManagerId), replace_remarks, 
                function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.reassign_users_account_success);
                    ReplaceManagerShow.trigger( "click" );
                } else {
                    displayMessage(error);
                }
            });
        }
    });
}

function activateManager(element) {
    $('.manager-list li').each(function () {
        $(this).removeClass('active');
        $(this).find('i').removeClass('fa fa-check pull-right');
    });

    var chkstatus = $(element).attr('class');
    var chkid = $(element).attr('id').split('-');

    if (chkstatus == 'active') {
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
    } else {
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');
        ManagerId = chkid[0];
        ManagerCategory = chkid[1];
    }

    if(ManagerCategory == '5'){
        loadReplaceManagerList(ManagerId, TECHNO_MANAGERS);
    }else{
        loadReplaceManagerList(ManagerId, DOMAIN_MANAGERS);
    }

}

function activateReplaceManager(element) {
    $('.replace-manager-list li').each(function () {
        $(this).removeClass('active');
        $(this).find('i').removeClass('fa fa-check pull-right');
    });

    var chkstatus = $(element).attr('class');
    var chkid = $(element).attr('id');
    
    if (chkstatus == 'active') {
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
    } else {
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');
        ReplaceManagerId = chkid;
    }
}

function loadManagerList(USER_LIST){
    $(".manager-list").empty();
    $(".replace-manager-list").empty();
    $.each(USER_LIST, function(key, value) {
        user_idval = value.user_id + '-' + value.user_category_id;
        user_text = value.employee_name;
        var clone = $("#templates .drop-down-option li").clone();
        clone.html(user_text + '<i></i>');
        clone.attr('id', user_idval);
        $('.manager-list').append(clone);
        clone.click(function() {
            activateManager(this);
        });
    });
}

function loadReplaceManagerList(selected_id, USER_LIST){
    var selectedMgr = selected_id;
    $(".replace-manager-list").empty();
    $.each(USER_LIST, function(key, value) {
        if(value.user_id != selectedMgr){
            user_idval = value.user_id;
            user_text = value.employee_name;
            var clone = $("#templates .drop-down-option li").clone();
            clone.html(user_text + '<i></i>');
            clone.attr('id', user_idval);
            $('.replace-manager-list').append(clone);
            clone.click(function() {
                activateReplaceManager(this);
            });
        }
    });
}

function getFormData(){
    function onSuccess(data) {
        TECHNO_MANAGERS = data.t_m_reassign;
        TECHNO_USERS = data.t_e_reassign;
        DOMAIN_MANAGERS = data.d_m_reassign;
        DOMAIN_USERS = data.d_e_reassign;
        GROUPS = data.groups;
        BUSINESS_GROUPS = data.business_groups;
        LEGAL_ENTITIES = data.admin_legal_entity;
        DOMAINS = data.domains;
        USER_CATEGORIES = data.user_categories;
        loadManagerList(TECHNO_MANAGERS);
    }
    function onFailure(error) {
        displayMessage(error);
    }
    mirror.getReassignUserAccountFormdata(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

$(function(){
    initialize();
});

function initialize(){
    $(document).ready(function () {
        pageControls();
        getFormData();
    });
}




