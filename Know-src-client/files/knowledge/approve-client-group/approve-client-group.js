var COUNTRIES = '';
var GROUPS = '';
var GROUPINFO = '';
var ORGANIZATIONS = '';
var ACCountry = $('#ac-country');
var ACGroup = $('#ac-group');
var CountryVal = $('#countryval');
var Country = $('#country-id');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var ApproveBtn = $(".approve-group");
var ShowBtn = $(".btn-show");
var approvalList = [];

function initialize(){
    displayLoader();
    $(".client-group-grid").hide();
    $(".approve-group-div").hide();
    function onSuccess(data) {
        COUNTRIES = data.countries;
        GROUPS = data.group_approval_list;
        GROUPINFO = data.group_info;
        hideLoader();
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getClientGroupApprovalList(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

function updateComplianceStatus(e, selectbox_id, reason_id){
    var selected_class = $(e).attr('class').split(' ').pop();
    $("#"+selected_class).val('0');

    var selected_option = $("#"+selectbox_id).val();
    if(selected_option == 2){
        $("#"+reason_id).show();
    }else{
        $("#"+reason_id).hide();
    }
}

function updateMappingStatus(e){
    var selected_class = $(e).attr('id');
    var splitId = selected_class.split("-").pop();
    var selected_option = $("#"+selected_class).val();

    $('.action-'+splitId).each(function() {
        $('.action-'+splitId).val(selected_option);
    });
    if(selected_option == 2){
        $("#reason-"+splitId).show();
    }else{
        $("#reason-"+splitId).hide();
        $('.reason-'+splitId).each(function() {
            $('.reason-'+splitId).hide();
        });
    }
}

function updateMappingReason(e){
    var selected_class = $(e).attr('id');
    var splitId = selected_class.split("-").pop();
    var selected_value = $(e).val();
    $('.reason-'+splitId).each(function() {
        $('.reason-'+splitId).val(selected_value);
    });
}

function loadApprovalList() {
    displayLoader();
    var LastGroup = '';
    $(".group-list").empty();
    $(".client-group-grid").hide();
    $(".approve-group-div").hide()
    
    var group_id = Group.val();
    var c_name = CountryVal.val();

    if(Country.val() == ''){
        displayMessage(message.country_required)
        return false;
    }
    $(".client-group-grid").show();

    var sno = 0;
    $.each(GROUPS, function(key, value){
        if(c_name == value.c_name && (group_id == '' || group_id == value.gt_id)){
            if(LastGroup != value.gt_id){
                ++ sno;
                var group_row = $("#templates .table-group-list tr");
                var clone = group_row.clone();
                $(".sno", clone).text(sno);
                $(".group_name", clone).text(value.group_name);
                $(".email_id", clone).text(value.email_id);
                
                $('.sm-approve-control', clone).attr('id', 'action-'+value.gt_id);
                $('.sm-approve-control', clone).on('change', function () {
                    updateMappingStatus(this);
                });
                $(".sm-reason", clone).attr('id', 'reason-'+value.gt_id);
                $('.sm-reason', clone).on('change', function () {
                    updateMappingReason(this);
                });
                $(".group-list").append(clone);
                LastGroup = value.gt_id;
            }

            var le_row = $("#templates .table-le-list tr");
            var clone2 = le_row.clone();
            $(".country_name", clone2).text(value.c_name);
            $(".legal_entity_name a", clone2).text(value.le_name);
            $(".legal_entity_name a", clone2).click(function(){
                displayPopup(
                    value.le_id, value.group_name, value.email_id, value.le_name, value.c_name, value.short_name
                );
            });
        
            $('.compliance-approve-control', clone2).attr('id', 'caction-'+value.le_id);
            $('.compliance-approve-control', clone2).addClass('action-'+value.gt_id);
            $('.compliance-approve-control', clone2).on('change', function () {
                updateComplianceStatus(
                    this,
                    "caction-"+value.le_id,
                    "creason-"+value.le_id
                )
            });
            $(".compliance-reason", clone2).attr('id', 'creason-'+value.le_id);
            $(".compliance-reason", clone2).addClass("reason-"+value.gt_id);
            $(".group-list").append(clone2);

            $('.compliance-reason').on('input', function (e) {
                //this.value = isCommon($(this));
                isCommon(this);
            });
            $('.sm-reason').on('input', function (e) {
                //this.value = isCommon($(this));
                isCommon(this);
            });
        }

    });

    if(sno > 0){
        $(".approve-group-div").show()
    }else{
        $(".approve-group-div").hide()
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $(".group-list").append(clone);
    }
    hideLoader();
}

function validateForm(){
    var result = true;
    approvalList = [];

    $.each(GROUPS, function(key, value){
        if(CountryVal.val() == value.c_name && (Group.val() == '' || Group.val() == value.gt_id)){
            var gt_id = value["gt_id"];
            var le_id = value["le_id"];
            var le_name = value["le_name"];
            
            var action_class = "caction-"+le_id;
            var reason_class = "creason-"+le_id;
            var selected_option = parseInt($("#"+action_class).val());
            var remarks = $("#"+reason_class).val().trim();
            var approval_status = true;

            if(selected_option == 2){
                approval_status = false;
                if(remarks.length == 0){
                    displayMessage(message.reason_required);
                    result = false;
                }
                else if (validateMaxLength("remark", remarks, "Reason") == false) {
                    result = false;
                }
                approvalList.push(
                    mirror.approveClientGroupList(gt_id, le_id, le_name,
                    approval_status, remarks)
                )
            }else if(selected_option == 1){
                remarks = "";
                approvalList.push(
                    mirror.approveClientGroupList(gt_id, le_id, le_name,
                    approval_status, remarks)
                )
            }
        }
    });
    if(result == false){
        return false;
    }else{
        return true;
    } 
}

function submitApprovalForm(){
    validation_result = validateForm();
    if(validation_result){
        if(approvalList.length > 0){
            displayLoader();
            function onSuccess(data) {
                displaySuccessMessage(message.action_success);
                $(".client-group-grid").hide();
                $(".approve-group-div").hide();
                function onSuccess(data) {
                    COUNTRIES = data.countries;
                    GROUPS = data.group_approval_list;
                    GROUPINFO = data.group_info;
                    ShowBtn.trigger( "click" );
                    hideLoader();
                }
                function onFailure(error) {
                    displayMessage(error);
                    hideLoader();
                }
                mirror.getClientGroupApprovalList(function (error, response) {
                    if (error == null) {
                        onSuccess(response);
                    } else {
                        onFailure(error);
                    }
                });

                
            }
            function onFailure(error) {
                displayMessage(error);
                hideLoader();
            }
            mirror.approveClientGroup(approvalList,
                function (error, response) {
                    if (error == null) {
                        onSuccess(response);
                    } else {
                        onFailure(error);
                    }
                });
        }else{
            displayMessage(message.approve_atleast_one_group);
        }
    }    
}

function getOrganizations(dId){
    var returnVal = '';
    var o_returnVal = '';
    $.each(ORGANIZATIONS, function(key, org_val){
        if(dId == org_val.d_id){
            returnVal = returnVal + org_val.org_name + ' - ' + org_val.count + ', ';
            if(org_val.o_count != null && org_val.o_count != org_val.count && org_val.o_count != 0 && org_val.o_count != ''){
                o_returnVal = o_returnVal + org_val.org_name + ' - ' + org_val.o_count + ', ';
            }
        }
    });
    returnVal = returnVal.replace(/,\s*$/, "");
    o_returnVal = o_returnVal.replace(/,\s*$/, "");

    if(o_returnVal != ''){
        o_returnVal = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + o_returnVal + "'></i>";
    }
    return o_returnVal + "<span>"+ returnVal + "</span>";
}

function loadLegalEntities(leDetails){

    var o_view_license = '';
    if(leDetails[18] != null && leDetails[18] != leDetails[10]){
        o_view_license = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + leDetails[18] + "'></i>";
    }

    var o_group_admin_email = '';
    if(leDetails[19] != null && leDetails[19] != leDetails[2]){
        o_group_admin_email = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + leDetails[19] + "'></i>";
    }

    $(".page-title").text("Client Group: "+leDetails[0]);
    $(".client_short_name").text("Short Name: "+leDetails[9]);
    $(".admin_username").html("Group Admin: "  + o_group_admin_email + "<span>"+ leDetails[2] + "</span>");
    $(".view_only_licence").html("View Only Licence(s): " + o_view_license + "<span>"+ leDetails[10] + "</span>");
    $(".remarks").text("Remarks: "+leDetails[11]);

    $(".overlay .tbody-le").empty();
    var le_row = $("#templates .le-row .le");
    var domain_header = $("#templates .domain-header");
    var domain_body = $("#templates .tbody-domain");
    var domain_row = $("#templates .domain-row tr");
    //$.each(LEGAL_ENTITIES, function(key, value){

    var o_bg_name = '';
    if(leDetails[13] != null && leDetails[13] != leDetails[3]){
        o_bg_name = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + leDetails[13] + "'></i>";
    }

    var o_le_name = '';
    if(leDetails[12] != null && leDetails[12] != leDetails[1]){
        o_le_name = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + leDetails[12] + "'></i>";
    }

    var o_file_space = '';
    if(leDetails[16] != null && leDetails[16] != leDetails[6]){
        o_file_space = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + leDetails[16] + " GB'></i>";
    }

    var o_contract_from = '';
    if(leDetails[14] != null && leDetails[14] != leDetails[4]){
        o_contract_from = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + leDetails[14] + "'></i>";
    }

    var o_contract_to = '';
    if(leDetails[15] != null && leDetails[15] != leDetails[5]){
        o_contract_to = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + leDetails[15] + "'></i>";
    }

    var o_total_license = '';
    if(leDetails[17] != null && leDetails[17] != leDetails[7]){
        o_total_license = "<i class='fa fa-info-circle text-primary c-pointer' data-toggle='tooltip' title='Old Data: " + leDetails[17] + "'></i>";
    }

    var clone = le_row.clone();
    var clone1 = domain_header.clone();
    var clone2 = domain_body.clone();
    $(".le_country", clone).text("Country: "+leDetails[8]);
    $(".le_bg", clone).text("Business Group: -");
    if(leDetails[3] != null){
        $(".le_bg", clone).html("Business Group: " + o_bg_name + "<span>"+ leDetails[3] + "</span>");   
    }
    $(".le_name", clone).html("Legal Entity: " + o_le_name + "<span>"+ leDetails[1] + "</span>");
    $(".file_space", clone).html("File space: " + o_file_space + "<span>" + leDetails[6] + " GB");
    $(".contract_from", clone).html("Contract From: " + o_contract_from + "<span>"+ leDetails[4] + "</span>");
    $(".contract_to", clone).html("Contract To: " + o_contract_to + "<span>"+ leDetails[5] + "</span>");
    $(".total_licence", clone).html("Total Licence(s): " + o_total_license + "<span>"+ leDetails[7] + "</span>");
    $("tbody-domain", clone).append(clone2);
    $(".overlay .tbody-le").append(clone);
    $(".overlay .tbody-le").append(clone1);

    var L_DOMAIN = '';
    $.each(ORGANIZATIONS, function(key, org_val){
        if(L_DOMAIN != org_val.d_name){
            var ORGS = getOrganizations(org_val.d_id);
            var clone2 = domain_row.clone();
            $(".domain-name", clone2).text(org_val.d_name);
            $(".org-name", clone2).html(ORGS);
            $(".tbody-domain", clone1).append(clone2);
            L_DOMAIN = org_val.d_name;
        }
    });
    hideLoader();
}

function displayPopup(le_id, g_name_, email_, le_name_, c_name_, s_name_) {
    displayLoader();
    function onSuccess(data) {
        var bg_ = data.bg_name;
        var c_from_ = data.contract_from;
        var c_to_ = data.contract_to;
        var f_space_ = Math.round(data.file_space/(1024*1024*1024)).toFixed(2);
        var no_of_licence_ = data.no_of_licence;
        var no_of_view_licence_ =data.no_of_view_licence;
        var remarks_ = '-';
        if(data.remarks != null){
            remarks_ = data.remarks;
        }
        ORGANIZATIONS = data.org_info;

        var o_le_name_ = data.o_le_name;
        var o_bg_ = data.o_bg_name;
        var o_c_from_ = data.o_contract_from;
        var o_c_to_ = data.o_contract_to;
        var o_f_space_ = null;
        if( data.o_file_space != null){
            o_f_space_ = Math.round(data.o_file_space/(1024*1024*1024)).toFixed(2);
        }
        var o_no_of_licence_ = data.o_no_of_licence;
        var o_no_of_view_licence_ =data.o_no_of_view_licence;
        var o_group_admin_email_ = data.o_group_admin_email_id;

        var leDetails = [g_name_, le_name_, email_, bg_, c_from_, c_to_, f_space_, no_of_licence_, c_name_, s_name_, 
        no_of_view_licence_, remarks_, o_le_name_, o_bg_, o_c_from_, o_c_to_, o_f_space_, o_no_of_licence_, o_no_of_view_licence_,
        o_group_admin_email_];
        loadLegalEntities(leDetails);
        //loadDateConfigurations();
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getLegalEntity(parseInt(le_id),
        function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}
//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();

    var current_id = id_element[0].id;
    if(current_id == 'country-id'){
      GroupVal.val('');
      Group.val('');
    }
}
function pageControls() {
    //load country list in autocomplete text box
    CountryVal.keyup(function(e){
        var text_val = $(this).val();

        var condition_fields = ["is_active"];
        var condition_values = [true];

        commonAutoComplete(
        e, ACCountry, Country, text_val, 
        COUNTRIES, "country_name", "country_id", function (val) {
            onAutoCompleteSuccess(CountryVal, Country, val);
        }, condition_fields, condition_values);
    });

    //load group list in autocomplete text box
    GroupVal.keyup(function(e){
        if(Country.val() != ''){
          var condition_fields = [];
          var condition_values = [];

          condition_fields.push("c_ids");
          condition_values.push(Country.val());

          var text_val = $(this).val();
          commonAutoComplete(
            e, ACGroup, Group, text_val, 
            GROUPINFO, "ct_name", "ct_id", function (val) {
                onAutoCompleteSuccess(GroupVal, Group, val);
            }, condition_fields, condition_values);
        }
    });

    ApproveBtn.click(function(){
        submitApprovalForm();
    });

    ShowBtn.click(function(){
        loadApprovalList();
    });
    
}
//initialization
$(function () {
    initialize();
    pageControls();
});