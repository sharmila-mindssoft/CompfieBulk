var UserList;
var DomainList;
var CountryList;
var OrganizationList;
var StatutoryNatureList;
var ApproveMappingList;

var ACCountry = $('#ac-country');
var ACDomain = $('#ac-domain');
var ACStatutoryNature = $('#ac-statutorynature');
var ACUser = $('#ac-user');
var ACOrganization = $('#ac-organization');

var CountryVal = $('#countryval');
var Country = $('#country');
var DomainVal = $('#domainval');
var Domain = $('#domain');
var OrganizationVal = $('#organizationval');
var Organization = $('#organization');
var StatutoryNatureVal = $('#statutorynatureval');
var StatutoryNature = $('#statutorynature');
var UserVal = $('#userval');
var User = $('#user');

var ShowBtn = $(".btn-show");
var SubmitBtn = $(".btn-submit");
var LastMapping;
var approvalList = [];

function initialize(){
    $(".client-group-grid").hide();
    $(".approve-group-div").hide();
    CountryVal.focus();
    function onSuccess(data) {
        UserList = data.knowledgeusers;
        DomainList = data.domains;
        CountryList = data.countries;
        OrganizationList = data.industries;
        StatutoryNatureList = data.statutory_natures;
    }
    function onFailure(error) {
        custom_alert(error);
    }
    mirror.getApproveStatutoryMapingsFilters(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });

}

function getValue(field_name){
   if (field_name == "country") {
        c_id = Country.val().trim();
        if (c_id == '') {
            return null;
        }
        return parseInt(c_id);
    }
    else if (field_name == "organization") {
        org_id = Organization.val().trim();
        if (org_id == '') {
            return null;
        }
        return parseInt(org_id);
    }
    else if (field_name == "statutorynature") {
        sn_id = StatutoryNature.val().trim();
        if (sn_id == '') {
            return null;
        }
        return parseInt(sn_id);
    }
    else if (field_name == "user") {
        u_id = User.val().trim();
        if (u_id == '') {
            return null;
        }
        return parseInt(u_id);
    }
    else if (field_name == "domain") {
        d_id = Domain.val().trim();
        if (d_id == '') {
            return null;
        }
        return parseInt(d_id);
    }

}

function validateMandatory(){
    is_valid = true;
    if (getValue("country") == null) {
      displayMessage(message.country_required);
      is_valid = false;
    }
    else if (getValue("domain") == null) {
      displayMessage(message.domain_required);
      is_valid = false;
    }
    return is_valid;
}

function loadApprovalList() {
    $(".tbody-sm-list").empty();
    $(".sm-grid").show();

    var sno = 0;
    $.each(ApproveMappingList, function(key, value){
        if(LastMapping != value.m_id){
            ++ sno;
            var sm_row = $("#templates .table-sm-list tr");
            var clone = sm_row.clone();
            $(".sno", clone).text(sno);
            $(".organization", clone).text(value.org_names);
            $(".statutorynature", clone).text(value.s_n_name);
            $(".provision", clone).text(value.map_text);
            $('.sm-approve-control', clone).attr('id', 'action-'+value.m_id);
            $('.sm-approve-control', clone).on('change', function () {
                updateMappingStatus(this);
            });
            $(".sm-reason", clone).attr('id', 'reason-'+value.m_id);
            $('.sm-reason', clone).on('change', function () {
                updateMappingReason(this);
            });
            $(".tbody-sm-list").append(clone);
            LastMapping = value.m_id;

            var compliance_head = $("#templates .table-compliance-head thead tr");
            var clone1 = compliance_head.clone();
            $(".tbody-sm-list").append(clone1);
        }

        var compliance_row = $("#templates .table-compliance-list tr");
        var clone2 = compliance_row.clone();
        $(".compliacne_name a", clone2).text(value.c_task);

        $('.compliacne_name', clone2).on('click', function (e) {

            mirror.getComplianceInfo(value.comp_id, function(error, response) {
                if (error == null) {
                    $('.popup-statutory').text(response.s_pro);
                    $('.popup-compliancetask').text(response.c_task);
                    $('.popup-description').text(response.descrip);
                    $('.popup-penalconse').text(response.p_cons);
                    $('.popup-frequency').text(response.freq);
                    $('.popup-occurance').text(response.summary);
                    $('.popup-applicablelocation').text(response.locat);
                    $('.popup-referencelink').text(response.refer);
                    Custombox.open({
                        target: '#custom-modal',
                        effect: 'contentscale',
                    });
                    e.preventDefault();
                }
                else {
                  displayMessage(error);
                }
            });
        });

        var status = "Active";
        if(value.is_active == false){
            status = "Inactive";
        }

        $(".status", clone2).text(status);
        $(".created_by", clone2).text(value.c_by);
        $(".updated_by", clone2).text(value.u_by);
        $('.compliance-approve-control', clone2).attr('id', 'caction-'+value.comp_id);
        $('.compliance-approve-control', clone2).addClass('action-'+value.m_id);
        $('.compliance-approve-control', clone2).on('change', function () {
            updateComplianceStatus(
                "caction-"+value.comp_id,
                "creason-"+value.comp_id
            )
        });
        $(".compliance-reason", clone2).attr('id', 'creason-'+value.comp_id);
        $(".compliance-reason", clone2).addClass("reason-"+value.m_id);
        $(".tbody-sm-list").append(clone2);

        $('.compliance-reason').on('input', function (e) {
            this.value = isCommon($(this));
        });
        $('.sm-reason').on('input', function (e) {
            this.value = isCommon($(this));
        });
    });

    if(sno > 0){
        $(".btn-submit").show();
    }else{
        $(".btn-submit").hide();
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $(".tbody-sm-list").append(clone);
    }
}

function updateComplianceStatus(selectbox_id, reason_id){
    var selected_option = $("#"+selectbox_id).val();
    if(selected_option == 3 || selected_option == 4){
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
    if(selected_option == 3 || selected_option == 4){
        $("#reason-"+splitId).show();
    }else{
        $("#reason-"+splitId).hide();
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

function getApprovalList (){
  if(validateMandatory()){
    _country = getValue("country");
    _domain = getValue("domain");
    _statutorynature = getValue("statutorynature");
    _organization = getValue("organization");
    _user = getValue("user");

    mirror.getApproveStatutoryMapings(_country, _domain,
    _organization, _statutorynature, _user,
        function(error, response) {
            if (error != null) {
                displayMessage(error);
            }
            else {
                ApproveMappingList = response.approv_mappings;
                loadApprovalList();
            }
        }
    );
  }
}


function validateForm(){
    var result = true;
    approvalList = [];

    var country_name = CountryVal.val();
    var domain_name = DomainVal.val();


    $.each(ApproveMappingList, function(key, value){
        var map_text = value["map_text"];
        var c_task = value["c_task"];
        var m_id = value["m_id"];
        var comp_id = value["comp_id"];
        var u_by = value["u_by"];
        var is_common = false;
        var statutory_nature = value["s_n_name"];

        var action_class = "caction-"+comp_id;
        var reason_class = "creason-"+comp_id;
        var selected_option = parseInt($("#"+action_class).val());
        var remarks = $("#"+reason_class).val().replace(/ /g,'');

        if(selected_option == 3 || selected_option == 4){
            if(remarks.length == 0){
                displayMessage(message.reason_required);
                result = false;
            }
            approvalList.push(
                mirror.approveStatutoryList(country_name, domain_name, statutory_nature,
                map_text, c_task, selected_option, remarks, m_id, comp_id, is_common, u_by)
            )
        }else if(selected_option == 2){
            remarks = "";
            approvalList.push(
                mirror.approveStatutoryList(country_name, domain_name, statutory_nature,
                map_text, c_task, selected_option, remarks, m_id, comp_id, is_common, u_by)
            )
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
            function onSuccess(data) {
                displaySuccessMessage(message.statutory_mapping_approve_success);
                getApprovalList();
            }
            function onFailure(error) {
                custom_alert(error);
            }
            mirror.approveStatutoryMapping(approvalList,
                function (error, response) {
                if (error == null) {
                    onSuccess(response);
                } else {
                    onFailure(error);
                }
            });
        }else{
            displayMessage(message.atleast_one_compliance_select);
        }
    }
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();

    /*var current_id = id_element[0].id;
    if(current_id == 'country-id'){
      GroupVal.val('');
      Group.val('');
    }*/
}

function pageControls() {
    //load country list in autocomplete text box
    CountryVal.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
        e, ACCountry, Country, text_val,
        CountryList, "country_name", "country_id", function (val) {
            onAutoCompleteSuccess(CountryVal, Country, val);
        });
    });

    //load domain list in autocomplete text box
    DomainVal.keyup(function(e){
        var condition_fields = [];
        var condition_values = [];
        if(Country.val() != ''){
          condition_fields.push("country_ids");
          condition_values.push(Country.val());
        }
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomain, Domain, text_val,
            DomainList, "domain_name", "domain_id", function (val) {
                onAutoCompleteSuccess(DomainVal, Domain, val);
            }, condition_fields, condition_values);
    });

    //load organization list in autocomplete text box
    OrganizationVal.keyup(function(e){
        var condition_fields = [];
        var condition_values = [];
        if(Country.val() != '' && Domain.val() != ''){
            condition_fields["country_id", "domain_id"];
            condition_values[Country.val(), Domain.val()];

            var text_val = $(this).val();
            commonAutoComplete(
            e, ACOrganization, Organization, text_val,
            OrganizationList, "industry_name", "industry_id", function (val) {
                onAutoCompleteSuccess(OrganizationVal, Organization, val);
            }, condition_fields, condition_values);
        }
    });

    //load statutory nature list in autocomplete text box
    StatutoryNatureVal.keyup(function(e){
        var condition_fields = [];
        var condition_values = [];
        if(Country.val() != ''){
            condition_fields["country_id"];
            condition_values[Country.val()];

            var text_val = $(this).val();
            commonAutoComplete(
            e, ACStatutoryNature, StatutoryNature, text_val,
            StatutoryNatureList, "statutory_nature_name", "statutory_nature_id", function (val) {
                onAutoCompleteSuccess(StatutoryNatureVal, StatutoryNature, val);
            }, condition_fields, condition_values);
        }
    });

    //load statutory nature list in autocomplete text box
    UserVal.keyup(function(e){
        var text_val = $(this).val();
        commonAutoComplete(
        e, ACUser, User, text_val,
        UserList, "employee_name", "user_id", function (val) {
            onAutoCompleteSuccess(UserVal, User, val);
        });
    });

    SubmitBtn.click(function(){
        submitApprovalForm();
    });

    ShowBtn.click(function(){
        $(".sm-grid").hide();
        getApprovalList();
    });

}
//initialization
$(function () {
    initialize();
    pageControls();
});
