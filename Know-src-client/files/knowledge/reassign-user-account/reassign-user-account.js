
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

var TE_PARANTS = {};
var DE_PARANTS = {};
var DM_PARANTS = {};
var DE_GROUPS = {};
var DM_GROUPS = {};
var LE_COUNTRIES = {};
var LE_DOMAINS = {};
var DE_LE = {};
var DM_LE = {};

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
var TESelectAll = $(".te-selectall");
var TECheckbox = $(".te-group-checkbox");
var TESelected = [];
var DMSelected = [];
var DESelected = [];
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


var ReplaceManagerShow = $("#category");
var ReplaceManagerSubmit = $(".btn-submit-5");
var ReplaceManagerRemarks = $("#replace_manager_remarks");
var ManagerCategory = '';
var ManagerId = '';
var ReplaceManagerId = '';

var RemarkView1 = $(".remark-view1");
var SubmitView1 = $(".submit-view1");
var RemarkView2 = $(".remark-view2");
var SubmitView2 = $(".submit-view2");
var RemarkView3 = $(".remark-view3");
var SubmitView3 = $(".submit-view3");
var RemarkView4 = $(".remark-view4");
var SubmitView4 = $(".submit-view4");

//retrive businessgroup form autocomplete value
function clearData(){
    TESelectAll.prop("checked", false);
    TMRemarks.val('');
    TERemarks.val('');
    DMRemarks.val('');
    DERemarks.val('');
    ReplaceManagerRemarks.val('');
    RTechnoExecutiveName.val('');
    RTechnoExecutiveId.val('');
    RDomainExecutiveName.val('');
    RDomainExecutiveId.val('');
    d_id = '';
    c_id = '';
    ManagerId = '';
    ReplaceManagerId = '';
}


$(".reassign_tab li").click(function() {
    var cTab = $(this).attr('value');
    clearData();
    if(cTab == 'tm'){
        TechnoManagerName.val('');
        TechnoManagerId.val('');
        $('.tbody-tm-view').empty();
        RemarkView1.hide();
        SubmitView1.hide();
        $(".view-1").hide();
        // var norecord_row = $('#nocompliance-templates .table-nocompliances-list .table-row');
        // var norecord_clone = norecord_row.clone();
        // $('.tbl_norecords', norecord_clone).text('No Records Found');
        // $('.tbody-tm-view').append(norecord_clone);
    }else if(cTab == 'te'){
        TechnoExecutiveName.val('');
        TechnoExecutiveId.val('');
        $('.tbody-te-view').empty();
        RemarkView2.hide();
        SubmitView2.hide();
        $(".view-2").hide();
        // var norecord_row = $('#nocompliance-templates .table-nocompliances-list .table-row');
        // var norecord_clone = norecord_row.clone();
        // $('.tbl_norecords', norecord_clone).text('No Records Found');
        // $('.tbody-te-view').append(norecord_clone);
        // $('.te-selectall').hide();

    }else if(cTab == 'dm'){
        DomainManagerName.val('');
        DomainManagerId.val('');
        DMGroupName.val('');
        DMGroupId.val('');
        DMBusinessGroupName.val('');
        DMBusinessGroupId.val('');
        DMLegalEntityName.val('');
        DMLegalEntityId.val('');
        DMDomainName.val('');
        DMDomainId.val('');
        $('.tbody-dm-view').empty();
        RemarkView3.hide();
        SubmitView3.hide();
        $(".view-3").hide();
        // var norecord_row = $('#nocompliance-templates .table-nocompliances-list .table-row');
        // var norecord_clone = norecord_row.clone();
        // $('.tbl_norecords', norecord_clone).text('No Records Found');
        // $('.tbody-dm-view').append(norecord_clone);

    }else if(cTab == 'de'){
        DomainExecutiveName.val('');
        DomainExecutiveId.val('');
        DEGroupName.val('');
        DEGroupId.val('');
        DEBusinessGroupName.val('');
        DEBusinessGroupId.val('');
        DELegalEntityName.val('');
        DELegalEntityId.val('');
        DEDomainName.val('');
        DEDomainId.val('');
        $('.tbody-de-view').empty();
        RemarkView4.hide();
        SubmitView4.hide();
        $(".view-4").hide();
        // var norecord_row = $('#nocompliance-templates .table-nocompliances-list .table-row');
        // var norecord_clone = norecord_row.clone();
        // $('.tbl_norecords', norecord_clone).text('No Records Found');
        // $('.tbody-de-view').append(norecord_clone);

    }else{
        clearData();
        $('#category').val('');    
        $(".manager-list").empty();
        $(".replace-manager-list").empty();
        $(".replace-view").hide();
    }
});

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;

    if (current_id == 'domain_manager_id') {
        DMGroupName.val('');
        DMGroupId.val('');
        DMBusinessGroupName.val('');
        DMBusinessGroupId.val('');
        DMLegalEntityName.val('');
        DMLegalEntityId.val('');
        DMDomainName.val('');
        DMDomainId.val('');
    }else if (current_id == 'dm_group_id') {
        DMBusinessGroupName.val('');
        DMBusinessGroupId.val('');
        DMLegalEntityName.val('');
        DMLegalEntityId.val('');
        DMDomainName.val('');
        DMDomainId.val('');
    } else if (current_id == 'dm_business_group_id') {
        DMLegalEntityName.val('');
        DMLegalEntityId.val('');
        DMDomainName.val('');
        DMDomainId.val('');
    } else if (current_id == 'dm_legal_entity_id') {
        DMDomainName.val('');
        DMDomainId.val('');
    }else if (current_id == 'domain_executive_id') {
        DEGroupName.val('');
        DEGroupId.val('');
        DEBusinessGroupName.val('');
        DEBusinessGroupId.val('');
        DELegalEntityName.val('');
        DELegalEntityId.val('');
        DEDomainName.val('');
        DEDomainId.val('');
    }else if (current_id == 'de_group_id') {
        DEBusinessGroupName.val('');
        DEBusinessGroupId.val('');
        DELegalEntityName.val('');
        DELegalEntityId.val('');
        DEDomainName.val('');
        DEDomainId.val('');
    } else if (current_id == 'de_business_group_id') {
        DELegalEntityName.val('');
        DELegalEntityId.val('');
        DEDomainName.val('');
        DEDomainId.val('');
    } else if (current_id == 'de_legal_entity_id') {
        DEDomainName.val('');
        DEDomainId.val('');
    }else if (current_id == 'techno_manager_id') {
        clearData();
        $('.tbody-tm-view').empty();
        callTechnoUserInfo(parseInt(TechnoManagerId.val()), 'TM');
    }else if (current_id == 'techno_executive_id') {
        clearData();
        $('.tbody-te-view').empty();
        callTechnoUserInfo(parseInt(TechnoExecutiveId.val()), 'TE');
    }else{
        var sub_id = current_id.substr(0, current_id.lastIndexOf('_'));
        if (sub_id == 'domain_manager_id') {
            $('.domain_executive_id').val('');
            $('.dm-domain-executive-name').val('');
        }
    }
}

function loadTMList(){
        $(".view-1").show();
        var LastGroup = '';
        var group_countries = {};
        var le_countries = {};
        var isCount = false;
        var DuplicateTMData = [];
        $.each(TechnoDetailsList, function(key, value) {
            isCount = true;
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
                    var condition_fields = ["country_domains_parent", "user_id"];
                    var condition_values = [group_countries[value.ct_id], TechnoManagerId.val()];
                    //alert(JSON.stringify(group_countries[value.ct_id]))
                    var text_val = $(this).val();
                    selected_textbox = $(this);
                    selected_textid = $("#techno_manager_id_"+value.ct_id);

                    commonAutoComplete1(
                        e, $("#ac-techno-manager-"+value.ct_id), $("#techno_manager_id_"+value.ct_id), text_val,
                        TECHNO_MANAGERS, "employee_name", "user_id",  function (val) {
                            onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                        }, condition_fields, condition_values);
                });

                $('.tbody-tm-view').append(clone);
                LastGroup = value.ct_name;

                group_countries[value.ct_id] = [];
                DuplicateTMData = [];
            }
            /*console.log(value.ct_id)
            console.log(group_countries)
            console.log(value.c_id)
            console.log(group_countries[value.ct_id])*/
            var d_ids = value.d_ids;
            var c_id = value.c_id;
            for(var i=0; i<d_ids.length; i++){
                var tm =  c_id +'-'+ d_ids[i] ;
                if ($.inArray(tm, DuplicateTMData) == -1) {
                    DuplicateTMData.push(tm);                    
                    var TMData = {
                        'c_id': c_id,
                        'd_id': d_ids[i],
                    }
                    group_countries[value.ct_id].push(TMData);
                }
                //alert(JSON.stringify(TE_PARANTS[te]))
            }

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

            le_countries[value.le_id] = [];
            for(var i=0; i<d_ids.length; i++){
                var tm =  c_id +'-'+ d_ids[i] ;
                var TMLeData = {
                    'c_id': c_id,
                    'd_id': d_ids[i],
                    'p_user_ids': [],
                }
                le_countries[value.le_id].push(TMLeData);
                //alert(JSON.stringify(TE_PARANTS[te]))
            }

            $('.tm-techno-executive-name', clone).keyup(function(e){
                for(var i=0; i<le_countries[value.le_id].length; i++){
                    //alert(le_countries[value.le_id][i].p_user_ids)
                    le_countries[value.le_id][i].p_user_ids = [parseInt($("#techno_manager_id_"+value.ct_id).val())];
                }
                var condition_fields = ["country_domains_parent"];
                var condition_values = [le_countries[value.le_id]];
                //alert(JSON.stringify(le_countries[value.le_id]))
                var text_val = $(this).val();
                selected_textbox = $(this);
                selected_textid = $("#techno_executive_id_"+value.le_id);

                commonAutoComplete1(
                    e, $("#ac-techno-executive-"+value.le_id), $("#techno_executive_id_"+value.le_id), text_val,
                    TECHNO_USERS, "employee_name", "user_id", function (val) {
                        onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                    }, condition_fields, condition_values);
            });
        
            $('.tbody-tm-view').append(clone);
        });

        if(isCount == false){
            RemarkView1.hide();
            SubmitView1.hide();
            var norecord_row = $('#nocompliance-templates .table-nocompliances-list .table-row');
            var norecord_clone = norecord_row.clone();
            $('.tbl_norecords', norecord_clone).text('No Records Found');
            $('.tbody-tm-view').append(norecord_clone);
        }else{
            RemarkView1.show();
            SubmitView1.show();
        }
        //console.log(group_countries)
        //console.log(group_domains)
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
        hideLoader();
}

function loadTEList(){
        $(".view-2").show();
        var isCount = false;
        $.each(TechnoDetailsList, function(key, value) {
            isCount = true;
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

        $('.te-group-checkbox').click(function() {
            getTEValidCountries();
        });
        if(isCount == false){
            RemarkView2.hide();
            SubmitView2.hide();
            var norecord_row = $('#nocompliance-templates .table-nocompliances-list .table-row');
            var norecord_clone = norecord_row.clone();
            $('.tbl_norecords', norecord_clone).text('No Records Found');
            $('.tbody-te-view').append(norecord_clone);
            $('.te-selectall').hide();
        }else{
            $('.te-selectall').show();
            RemarkView2.show();
            SubmitView2.show();
        }
        hideLoader();

}

function loadDMList(){
        $(".view-3").show();
        var LastLE = '';
        var group_countries = {};
        var group_domains = {};
        var isCount = false;
        $.each(DomainDetailsList, function(key, value) {
            isCount = true;
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
                    DMSelected = [];
                    var dm = DomainManagerId.val() +'-'+ c_id +'-'+ d_id ;
                    DMSelected.push(DM_PARANTS[dm])
                    var condition_fields = ["country_domains_parent", "user_id"];
                    var condition_values = [DMSelected, DomainManagerId.val()];
                    //alert(JSON.stringify(DMSelected))
                    var text_val = $(this).val();
                    selected_textbox = $(this);
                    selected_textid = $("#domain_manager_id_"+value.le_id);

                    commonAutoComplete2(
                        e, $("#ac-domain-manager-"+value.le_id), $("#domain_manager_id_"+value.le_id), text_val,
                        DOMAIN_MANAGERS, "employee_name", "user_id",  function (val) {
                            onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                        }, condition_fields, condition_values);
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
                de_parent = [];
                if($("#domain_manager_id_"+value.le_id).val() != ''){
                    de_parent.push(parseInt($("#domain_manager_id_"+value.le_id).val()))
                }
                var DEData = {
                    'c_id': c_id,
                    'd_id': d_id,
                    'p_user_ids': de_parent,
                }

                var condition_fields = ["country_domains_parent"];
                var condition_values = [[DEData]];
                
                var text_val = $(this).val();
                selected_textbox = $(this);
                selected_textid = $("#domain_executive_id_"+value.u_id);
                if(de_parent.length > 0){
                    commonAutoComplete1(
                        e, $("#ac-domain-executive-"+value.u_id), $("#domain_executive_id_"+value.u_id), text_val,
                        DOMAIN_USERS, "employee_name", "user_id", function (val) {
                            onAutoCompleteSuccess(selected_textbox, selected_textid, val);
                        }, condition_fields, condition_values);
                }
                
            });
        
            $('.tbody-dm-view').append(clone);
        });

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

        $(".dm-group-checkbox-main").change(function() {
            $(".tbody-dm-view .dm-group-checkbox").prop('checked', $(this).prop("checked"));
            if($(this).prop("checked")){
                $(".de-ac-view").show();
            }else{
                $(".de-ac-view").hide();
            }

        });

        $('.dm-group-checkbox').on('click', function(e) {
            var de_view = '.de-ac-' + $(this).val();
            if($(this).prop("checked")){
                $(de_view).show();
            }else{
                $(de_view).hide();
            }
        });

        if(isCount == false){
            RemarkView3.hide();
            SubmitView3.hide();
            var norecord_row = $('#nocompliance-templates .table-nocompliances-list .table-row');
            var norecord_clone = norecord_row.clone();
            $('.tbl_norecords', norecord_clone).text('No Records Found');
            $('.tbody-dm-view').append(norecord_clone);
        }else{
            RemarkView3.show();
            SubmitView3.show();
        }
        hideLoader();
}

function loadDEList(){
    $(".view-4").show();
    $('.tbody-de-view').empty();
    var isCount = false;
    $.each(DomainDetailsList, function(key, value) {
        isCount = true;
        var unittableRow = $('#templates .de-view-row .de-view-unit-row');
        var clone = unittableRow.clone();

        $('.de-group-checkbox', clone).val(value.u_id);
        
        $('.de-unitcode', clone).text(value.u_code);
        $('.de-unitname', clone).text(value.u_name);
        $('.de-unitaddress', clone).attr('title', value.address);
        $('.de-unitlocation', clone).text(value.location);
        
        $('.tbody-de-view').append(clone);
    });

    if(isCount == false){
        RemarkView4.hide();
        SubmitView4.hide();
        var norecord_row = $('#nocompliance-templates .table-nocompliances-list .table-row');
        var norecord_clone = norecord_row.clone();
        $('.tbl_norecords', norecord_clone).text('No Records Found');
        $('.tbody-de-view').append(norecord_clone);
    }else{
        RemarkView4.show();
        SubmitView4.show();
    }
    hideLoader();
}

function callTechnoUserInfo(userId, type){
    displayLoader();
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
            hideLoader();
        }
    });

}

function callDomainUserInfo(userId, groupId, legalentityId, domainId, type){
    displayLoader();
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
            hideLoader();
        }
    });

}

/*function getCountryId(l_Id){
    var country_id = '';
    $.each(LEGAL_ENTITIES, function(key, value) {
        if(value.legal_entity_id == parseInt(l_Id)){
            country_id = value.country_id;
        }
    });
    return country_id;
}*/

function getTEValidCountries(){
    TESelected = [];
    var TEDuplicate = [];
    $('.te-group-checkbox:checkbox:checked').each(function (index, el) {
        var combile_id = $(this).val().split('-');
        var le_id = combile_id[1];
        var cn_id = LE_COUNTRIES[le_id];
        var d_ids = LE_DOMAINS[le_id];

        for(var i=0; i<d_ids.length; i++){
            var te = TechnoExecutiveId.val() +'-'+ cn_id +'-'+ d_ids[i] ;
            if ($.inArray(te, TEDuplicate) == -1) {
                TEDuplicate.push(te);
                TESelected.push(TE_PARANTS[te]);
            }
            //alert(JSON.stringify(TE_PARANTS[te]))
        }
        
        /*if ($.inArray(cn_id, TECountries) == -1) {
            TECountries.push(cn_id);
        }

        for(var i=0; i<d_ids.length; i++){
            if ($.inArray(d_ids[i], TEDomains) == -1) {
                TEDomains.push(d_ids[i]);
            }
        }*/
    });
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
        
        var condition_fields = ["country_domains_parent", "user_id", ];
        var condition_values = [TESelected, TechnoExecutiveId.val()];
        //alert(containsAll(TESelected))
        commonAutoComplete1(
            e, RACTechnoExecutive, RTechnoExecutiveId, text_val,
            TECHNO_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(RTechnoExecutiveName, RTechnoExecutiveId, val);
            }, condition_fields, condition_values);
    });

    TESelectAll.change(function() {
        $(".tbody-te-view .te-group-checkbox").prop('checked', $(this).prop("checked"));
        getTEValidCountries();
    });

    DomainManagerName.keyup(function(e){
        var condition_fields = ["p_user_ids"];
        var condition_values = [];

        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomainManager, DomainManagerId, text_val,
            DOMAIN_MANAGERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(DomainManagerName, DomainManagerId, val);
            });
    });

    DMGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["group_id"];
        var condition_values = [DM_GROUPS[DomainManagerId.val()]];
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

            commonAutoComplete(
                e, DMACBusinessGroup, DMBusinessGroupId, text_val,
                BUSINESS_GROUPS, "business_group_name", "business_group_id",
                function (val) {
                    onAutoCompleteSuccess(DMBusinessGroupName, DMBusinessGroupId, val);
                }, condition_fields, condition_values);
        }
    });

    DMLegalEntityName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["legal_entity_id"];
        var condition_values = [DM_LE[DomainManagerId.val()]];
        if(DMBusinessGroupId.val() != ''){
            condition_fields.push("business_group_id");
            condition_values.push(DMBusinessGroupId.val());
        }
        if(DMGroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(DMGroupId.val());

            commonAutoComplete(
                e, DMACLegalEntity, DMLegalEntityId, text_val,
                LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
                function (val) {
                    onAutoCompleteSuccess(DMLegalEntityName, DMLegalEntityId, val)
                }, condition_fields, condition_values);
        }
    })

    DMDomainName.keyup(function(e){
        var text_val = $(this).val();
        var cn_id = LE_COUNTRIES[DMLegalEntityId.val()];
        var d_ids = LE_DOMAINS[DMLegalEntityId.val()];
        var condition_fields = ["is_active", "country_ids", "domain_id"];
        var condition_values = [true, cn_id, d_ids];

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

        var de = DomainExecutiveId.val() +'-'+ c_id +'-'+ d_id ;
        var text_val = $(this).val();
        var condition_fields = ["country_domains_parent", "user_id"];
        var condition_values = [[DE_PARANTS[de]], DomainExecutiveId.val()];
        commonAutoComplete1(
            e, RACDomainExecutive, RDomainExecutiveId, text_val,
            DOMAIN_USERS, "employee_name", "user_id", function (val) {
                onAutoCompleteSuccess(RDomainExecutiveName, RDomainExecutiveId, val);
            }, condition_fields, condition_values);
    });

    DEGroupName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["group_id"];
        var condition_values = [DE_GROUPS[DomainExecutiveId.val()]];
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

            commonAutoComplete(
                e, DEACBusinessGroup, DEBusinessGroupId, text_val,
                BUSINESS_GROUPS, "business_group_name", "business_group_id",
                function (val) {
                    onAutoCompleteSuccess(DEBusinessGroupName, DEBusinessGroupId, val);
                }, condition_fields, condition_values);
        }
    });

    DELegalEntityName.keyup(function(e){
        var text_val = $(this).val();
        var condition_fields = ["legal_entity_id"];
        var condition_values = [DE_LE[DomainExecutiveId.val()]];

        if(DEBusinessGroupId.val() != ''){
            condition_fields.push("business_group_id");
            condition_values.push(DEBusinessGroupId.val());
        }

        if(DEGroupId.val() != ''){
            condition_fields.push("client_id");
            condition_values.push(DEGroupId.val());
            commonAutoComplete(
                e, DEACLegalEntity, DELegalEntityId, text_val,
                LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
                function (val) {
                    onAutoCompleteSuccess(DELegalEntityName, DELegalEntityId, val)
                }, condition_fields, condition_values);
        }
    })

    DEDomainName.keyup(function(e){
        var text_val = $(this).val();
        var cn_id = LE_COUNTRIES[DELegalEntityId.val()];
        var d_ids = LE_DOMAINS[DELegalEntityId.val()];
        var condition_fields = ["is_active", "country_ids", "domain_id"];
        var condition_values = [true, cn_id, d_ids];
    
        commonAutoComplete(
            e, DEACDomain, DEDomainId, text_val,
            DOMAINS, "domain_name", "domain_id",
            function (val) {
                onAutoCompleteSuccess(DEDomainName, DEDomainId, val)
            }, condition_fields, condition_values);
    });

    DMShow.click(function(){
        var dm_id = DomainManagerId.val();
        var group_id = DMGroupId.val();
        var le_id = DMLegalEntityId.val();
        var domain_id = DMDomainId.val();

        if(dm_id == ''){
            displayMessage(message.reassign_from_dm_required);
        }else if(group_id == ''){
            displayMessage(message.group_required);
        }else if(le_id == ''){
            displayMessage(message.legalentity_required);
        }else if(domain_id == ''){
            displayMessage(message.domain_required);
        }else{
            clearData();
            $('.tbody-dm-view').empty();
            d_id = parseInt(domain_id);
            c_id = LE_COUNTRIES[le_id];
            callDomainUserInfo(parseInt(dm_id), parseInt(group_id), parseInt(le_id), parseInt(domain_id), 'DM');
        }
    });

    DEShow.click(function(){
        var de_id = DomainExecutiveId.val();
        var group_id = DEGroupId.val();
        var le_id = DELegalEntityId.val();
        var domain_id = DEDomainId.val();

        if(de_id == ''){
            displayMessage(message.reassign_from_de_required);
        }else if(group_id == ''){
            displayMessage(message.group_required);
        }else if(le_id == ''){
            displayMessage(message.legalentity_required);
        }else if(domain_id == ''){
            displayMessage(message.domain_required);
        }else{
            clearData();
            $('.tbody-de-view').empty();
            d_id = parseInt(domain_id);
            c_id = LE_COUNTRIES[le_id];
            callDomainUserInfo(parseInt(de_id), parseInt(group_id), parseInt(le_id), parseInt(domain_id), 'DE');
        }
    });

    ReplaceManagerShow.change(function(){
        clearData();
        var category = $('#category').val();
        if(category == ''){
            displayMessage(message.user_category_required);
            $(".manager-list").empty();
            $(".replace-manager-list").empty();
            $(".replace-view").hide();
            return false;
        }
        else if(category == '1'){
            $(".replace-view").show();
            loadManagerList(TECHNO_MANAGERS);
            $('.user-title').text('Techno Manager');
        }else{
            $(".replace-view").show();
            loadManagerList(DOMAIN_MANAGERS);
            $('.user-title').text('Domain Manager');
        }
    });

    TMSubmit.click(function(){
        var reassignDetails = [];
        var reassign_from = TechnoManagerId.val();
        var tm_remarks = TMRemarks.val().trim();
        var isValidate = false;
        var res = 0;
        if(reassign_from == ''){
            displayMessage(message.reassign_from_tm_required);
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
                                res = 1;
                                return false;
                            }else{
                                reassignDetailsData = mirror.technoManagerInfo(parseInt(reassign_to), parseInt(group_id),
                                    parseInt(legal_entity_id), parseInt(te_id), parseInt(old_executive_id));
                                reassignDetails.push(reassignDetailsData);
                                isValidate = true;
                            }
                        });

                        if(res == 1){
                            return false;
                        }

                        if(tm_remarks == ''){
                            displayMessage(message.remarks_required);
                            res = 1;
                            return false;
                        }
                        else if (validateMaxLength("remark", tm_remarks, "Remark") == false) {
                            res = 1;
                            return false;
                        }
                    }
                });
                if(isValidate && res == 0){
                    displayLoader();
                    mirror.ReassignTechnoManager(parseInt(reassign_from), reassignDetails, tm_remarks, 
                        function(error, response) {
                        if (error == null) {
                            displaySuccessMessage(message.tm_reassign_success);
                            clearData();
                            $('.tbody-tm-view').empty();
                            callTechnoUserInfo(parseInt(TechnoManagerId.val()), 'TM');
                        } else {
                            displayMessage(error);
                            hideLoader();
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
        var te_remarks = TERemarks.val().trim();
        var isValidate = false;

        if(reassign_from == ''){
            displayMessage(message.reassign_from_te_required);
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
                        }else if (validateMaxLength("remark", te_remarks, "Remark") == false) {
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
                        displayLoader();
                        mirror.ReassignTechnoExecutive(parseInt(reassign_from), parseInt(reassign_to), 
                            reassignDetails, te_remarks, 
                            function(error, response) {
                            if (error == null) {
                                displaySuccessMessage(message.te_reassign_success);
                                clearData();
                                $('.tbody-te-view').empty();
                                callTechnoUserInfo(parseInt(TechnoExecutiveId.val()), 'TE');
                            } else {
                                displayMessage(error);
                                hideLoader();
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
        }else{
            if($('.dm-group-checkbox:checkbox:checked').length > 0){
                var reassign_to = $('#domain_manager_id_'+le_id).val();
                if(reassign_to == ''){
                    displayMessage(message.reassign_to_dm_required);
                    return false;
                }else{
                    var res = 0;
                    $('.dm-group-checkbox:checkbox:checked').each(function (index, el) {
                        var u_id = $(this).val();
                        var de_id = $('#domain_executive_id_'+u_id).val();
                        var old_executive_id = $('#d_old_executive_id_'+u_id).val();
                        if(de_id == ''){
                            res = 1;
                            displayMessage(message.reassign_to_de_required);
                            return false;
                        }else{
                            reassignDetailsData = mirror.domainManagerInfo(parseInt(u_id), parseInt(de_id), parseInt(old_executive_id));
                            reassignDetails.push(reassignDetailsData);
                            isValidate = true;
                        }
                    });

                    if(res == 1){
                        return false;
                    }

                    if(dm_remarks == ''){
                        displayMessage(message.remarks_required);
                        res = 1;
                        return false;
                    }else if (validateMaxLength("remark", dm_remarks, "Remark") == false) {
                        res = 1;
                        return false;
                    }
                }

                if(isValidate && res == 0){
                    if(reassign_from == reassign_to){
                        displayMessage(message.reassign_from_reassign_to_both_are_same);
                        return false;
                    }else{
                        displayLoader();
                        mirror.ReassignDomainManager(parseInt(reassign_from), parseInt(reassign_to), parseInt(group_id),
                            parseInt(le_id), parseInt(domain_id), reassignDetails, dm_remarks, function(error, response) {
                            if (error == null) {
                                displaySuccessMessage(message.dm_reassign_success);
                                DMShow.trigger( "click" );
                            } else {
                                displayMessage(error);
                                hideLoader();
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
        }else{
            if($('.de-group-checkbox:checkbox:checked').length > 0){

                if(reassign_to == ''){
                    displayMessage(message.reassign_to_de_required);
                }else if(de_remarks == ''){
                    displayMessage(message.remarks_required);
                }else if (validateMaxLength("remark", de_remarks, "Remark") == false) {
                    return false;
                }else{
                    var u_ids = [];
                    $('.de-group-checkbox:checkbox:checked').each(function (index, el) {
                        var u_id = $(this).val();
                        u_ids.push(parseInt(u_id))
                    });
                    displayLoader();
                    mirror.ReassignDomainExecutive(parseInt(reassign_from), parseInt(reassign_to), parseInt(group_id),
                        parseInt(le_id), parseInt(domain_id), u_ids, de_remarks, function(error, response) {
                        if (error == null) {
                            displaySuccessMessage(message.de_reassign_success);
                            DEShow.trigger( "click" );
                        } else {
                            displayMessage(error);
                            hideLoader();
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
            displayMessage(message.manager_required);
        }else if(ReplaceManagerId == ''){
            displayMessage(message.replace_manager_required);
        }else if(replace_remarks == ''){
            displayMessage(message.remarks_required);
        }else if (validateMaxLength("remark", replace_remarks, "Remark") == false) {
            return false;
        }else{
            displayLoader();
            mirror.SaveUserReplacement(parseInt(ManagerCategory), parseInt(ManagerId), parseInt(ReplaceManagerId), replace_remarks, 
                function(error, response) {
                if (error == null) {
                    getFormData();
                    displaySuccessMessage(message.manager_replacement_success);
                    ReplaceManagerShow.trigger( "change" );
                    hideLoader();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            });
        }
    });

    TMRemarks.on('input', function (e) {
      //this.value = isCommon($(this));
      isCommon(this);
    });

    DMRemarks.on('input', function (e) {
      //this.value = isCommon($(this));
      isCommon(this);
    });

    TERemarks.on('input', function (e) {
      //this.value = isCommon($(this));
      isCommon(this);
    });

    DERemarks.on('input', function (e) {
      //this.value = isCommon($(this));
      isCommon(this);
    });

    ReplaceManagerRemarks.on('input', function (e) {
      //this.value = isCommon($(this));
      isCommon(this);
    });
}

function activateManager(element, country_domains_parent) {
    displayLoader();
    ReplaceManagerId = '';
    $(".replace-manager-list").empty();

    $('.manager-list li').each(function () {
        $(this).removeClass('active');
        $(this).find('i').removeClass('fa fa-check pull-right');
    });

    var chkstatus = $(element).attr('class');
    var chkid = $(element).attr('id').split('-');

    mirror.checkUserReplacement(parseInt(chkid[1]), parseInt(chkid[0]),
        function (error, response) {
            if (error == null) {
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
                    loadReplaceManagerList(ManagerId, TECHNO_MANAGERS, country_domains_parent);
                }else{
                    loadReplaceManagerList(ManagerId, DOMAIN_MANAGERS, country_domains_parent);
                }
                hideLoader();
            } else {
                if(error == "NoTransactionExists"){
                    displayMessage(message.no_trransaction_available);
                }else{
                    displayMessage(error);
                }
                hideLoader();
            }
    });

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
            activateManager(this, value.country_domains_parent);
        });
    });
}

function loadReplaceManagerList(selected_id, USER_LIST, country_domains_parent){
    var selectedMgr = selected_id;
    $(".replace-manager-list").empty();
    $.each(USER_LIST, function(key, value) {
        if(value.user_id != selectedMgr){
            var pass_count = 0;
            for(var j=0; j<country_domains_parent.length; j++){
                var cresult = false;
                var dresult = false;

                for(var i=0; i<value.country_domains_parent.length; i++)  {
                    if(value.country_domains_parent[i]["c_id"] == country_domains_parent[j]["c_id"]){
                        cresult = true;
                    }
                    if(value.country_domains_parent[i]["d_id"] == country_domains_parent[j]["d_id"]){
                        dresult = true;
                    }
                }    
                if(cresult && dresult){
                    pass_count++;
                }
            }
            if(country_domains_parent.length == pass_count){
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
            
        }
    });
}

function generateMap(){
    TE_PARANTS = {};
    DE_PARANTS = {};
    DM_PARANTS = {};
    DE_GROUPS = {};
    DM_GROUPS = {};
    LE_COUNTRIES = {};
    LE_DOMAINS = {};
    DE_LE = {};
    DM_LE = {};

    $.each(TECHNO_USERS, function(key, value) {
        $.each(value.country_domains_parent, function(key1, value1) {
            var te = value.user_id +'-'+ value1.c_id +'-'+ value1.d_id ;
            //alert(JSON.stringify(value1))
            TE_PARANTS[te] = value1;
        });
        //alert(JSON.stringify(TE_PARANTS))
        //TE_PARANTS[value.user_id] = value.p_user_ids;
    });

    $.each(DOMAIN_USERS, function(key, value) {
        $.each(value.country_domains_parent, function(key1, value1) {
            var de = value.user_id +'-'+ value1.c_id +'-'+ value1.d_id ;
            DE_PARANTS[de] = value1;
        });

        //DE_PARANTS[value.user_id] = value.p_user_ids;
        DE_GROUPS[value.user_id] = value.grp_ids;
        DE_LE[value.user_id] = value.le_ids;
    });

    $.each(DOMAIN_MANAGERS, function(key, value) {
        $.each(value.country_domains_parent, function(key1, value1) {
            var dm = value.user_id +'-'+ value1.c_id +'-'+ value1.d_id ;
            DM_PARANTS[dm] = value1;
        });

        //DM_PARANTS[value.user_id] = value.p_user_ids;
        DM_GROUPS[value.user_id] = value.grp_ids;
        DM_LE[value.user_id] = value.le_ids;
    });

    $.each(LEGAL_ENTITIES, function(key, value) {
        LE_COUNTRIES[value.legal_entity_id] = value.country_id;
        LE_DOMAINS[value.legal_entity_id] = value.domain_ids;
    });

}

function getFormData(){
    function onSuccess(data) {
        TECHNO_MANAGERS = data.t_m_reassign;
        TECHNO_USERS = data.t_e_reassign;
        DOMAIN_MANAGERS = data.d_m_reassign;
        DOMAIN_USERS = data.d_e_reassign;
        GROUPS = data.re_assign_groups;
        BUSINESS_GROUPS = data.business_groups;
        LEGAL_ENTITIES = data.admin_legal_entity;
        DOMAINS = data.domains;
        USER_CATEGORIES = data.user_categories;
        generateMap();
        hideLoader();
        //loadManagerList(TECHNO_MANAGERS);
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
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
    displayLoader();
    $(document).ready(function () {
        pageControls();
        getFormData();
    });
}




