var BusinessGroupName = $(".business-group-name");
var BusinessGroupSelect = $(".business-group-select");
var LegalEntityName = $(".legal-entity-name");
var LegalEntitySelect = $(".legal-entity-select");
var FType = $(".frequency-type");
var Domain = $(".domain");
var DomainId = $("#domain-id");
var AcDomain = $("#ac-domain");

var ShowUnitButton = $(".show-unit-button");

var SearchUnit = $(".search-unit");
var SearchUnitCheckBox = $(".search-unit-selectall");

var UnitList = $(".unit-list"); 
var UnitList_li = $(".unit-list li"); 
var UNIT_CS_ID = {};
var ACTIVE_UNITS = [];

var TbodyComplianceList = $(".tbody-compliance-list");

var NextButton = $("#next-button");
var PreviousButton = $("#previous-button");
var SubmitButton = $("#submit-button");

var CURRENT_TAB = 1;

var BreadCrumbs = $(".breadcrumbs");
var BreadCrumbImg = '<i class="fa fa-angle-double-right"></i>';

var API_Wizard1 = "wizard_1";
var API_Wizard2 = "wizard_2";
var SAVE_API = "save";
var SUBMIT_API = "submit";
var API_LIST = "list";
var EDIT_API = "edit"

var le_id = null;
var d_id = null;
var sno = 1;
var temp_ftype = "";
var actCount = 1;
var LastAct = "";
var LastSubAct = "";
var count = 1;

var r_s_page = null;


PageControls = function() {
     NextButton.click(function() {
        TbodyComplianceList.empty();
        CURRENT_TAB += 1;
        showTab();
    });

    PreviousButton.click(function() {
        CURRENT_TAB = CURRENT_TAB - 1;
        isShowMore = false;
        showTab();
    });

    Domain.keyup(function(e) {
        var text_val = Domain.val().trim();
        var domainList = r_s_page._DomainList;
        var condition_fields = ["is_active", "le_id"];
        var condition_values = [true, le_id];
        commonAutoComplete(e, AcDomain, DomainId, text_val, domainList, "d_name", "d_id", function(val) {
            onDomainAutoCompleteSuccess(val);
        }, condition_fields, condition_values);
    });

    ShowUnitButton.click(function() {
       r_s_page.getUnitList();
    });
}

onDomainAutoCompleteSuccess = function(val) {
    Domain.val(val[1]);
    DomainId.val(val[0]);
    Domain.focus();
}


ReviewSettingsPage = function () {
    this._TypeList = [];
    this._DomainList = [];
    this._Units = [];
    this._ComplianceList = [];
}

ReviewSettingsPage.prototype.showLegalEntity = function (){    
    var t_this = this;
    NextButton.hide();
    PreviousButton.hide();
    SubmitButton.hide();
    var userLegalentity = user.entity_info;
    if(userLegalentity.length > 1){
        BusinessGroupName.hide();
        BusinessGroupSelect.show();
        LegalEntityName.hide();
        LegalEntitySelect.show();
        var select = '<option value="">Select</option>';
        $.each(user.entity_info, function(k, val){
            select = select + '<option value="' + val["le_id"] + '"> ' + val["le_name"] + ' </option>';
        });        
        LegalEntitySelect.html(select);
        LegalEntitySelect.on("change", function(){
            t_this.showTypeDomainList();
        });
    }else{
        BusinessGroupSelect.hide();
        BusinessGroupName.show();
        LegalEntitySelect.hide();
        LegalEntityName.show();
        LegalEntityName.text(userLegalentity[0]["le_name"]);
        BusinessGroupName.text(userLegalentity[0]["bg_name"]);
        le_id = userLegalentity[0]["le_id"]
        t_this.showTypeDomainList();
    }
}

ReviewSettingsPage.prototype.showTypeDomainList = function(){
    t_this = this;
    client_mirror.getReviewSettingsFilters(le_id, function(error, response) {
        if (error == null) {
            t_this._TypeList = response.compliance_frequency;
            t_this._DomainList = response.domain_list;            
            t_this.renderTypeList(t_this._TypeList);
        } else {
            t_this.possibleFailures(error);
        }
    });
}

ReviewSettingsPage.prototype.possibleFailures = function(error) {
    if (error == "UserGroupNameAlreadyExists") {
        displayMessage(message.domainname_required);
    } else if (error == 'InvalidUserGroupId') {
        displayMessage(message.invalid_usergroupid);
    } else if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
    } else {
        displayMessage(error);
    }
};   

ReviewSettingsPage.prototype.renderTypeList = function(data) {
    FType.empty()
    var select = '<option value="">Select</option>';
    $.each(data, function(k, val){
        select = select + '<option value="' + val["frequency_id"] + '"> ' + val["frequency"] + ' </option>';
    });
    FType.html(select);
}

ReviewSettingsPage.prototype.getUnitList = function(){
    t_this = this;
    d_id = DomainId.val();
    if(FType.children(':selected').val() == ""){
        displayMessage(message.compliancefrequency_required);
        return false;
    }
    else if(Domain.val() == ""){
        displayMessage(message.domainname_required);
        return false;
    }
    else if(DomainId.val() == ""){
        displayMessage(message.domainname_required);
        return false;    
    }
    else{
        temp_ftype = FType.children(':selected').val();
        client_mirror.getReviewSettingsUnitFilters(le_id, parseInt(d_id), function(error, response) {
            if (error == null) {
                NextButton.show();
                $(".step-1-unit-list").show();
                t_this._Units = response.rs_unit_list;
                t_this.renderUnitList(t_this._Units);
            } else {
                t_this.possibleFailures(error);
            }
        });    
    }
}

ReviewSettingsPage.prototype.renderUnitList = function(_Units) {
    UNIT_CS_ID = {};
    if(UnitList.length == 0){
        var UnitRow = $(".unit-list-ul li");
        var clone = UnitRow.clone();
        clone.text('No Units Found');
        UnitList.append(clone);
    }else{        
        var temp_d_name = "";
        $.each(_Units, function(key, value) {

            unit_idval = value.u_id;
            unit_text = value.u_code + " - " + value.u_name + " - " + value.address;
            var d_name = value.div_name;
            if(temp_d_name != d_name){
                var UnitRowheading = $(".unit-list-ul .heading");
                var cloneHeading = UnitRowheading.clone();    
                cloneHeading.html(d_name);
                UnitList.append(cloneHeading);
                temp_d_name = d_name;
            }
            
            var UnitRow = $(".unit-list-ul .unit-names");
            var clone = UnitRow.clone();
            clone.html(unit_text + '<i></i>');
            clone.attr('id', unit_idval);
            UnitList.append(clone);
            clone.click(function() {
                activateUnit(this);
            });
            UNIT_CS_ID[value.u_id] = value;
        });
    }

}

callAPI = function(api_type) {
    if(api_type = "API_Wizard2"){
        displayLoader();
        showBreadCrumbText();
        client_mirror.getReviewSettingsComplianceFilters(
            le_id, parseInt(d_id), ACTIVE_UNITS, parseInt(temp_ftype), (sno-1),
            function(error, data) {
                if (error == null) {
                    COMPLIANCES_LIST = data.rs_compliance_list;
                    var timeline = data.timeline;
                    totalRecord = data.total_records;
                    $(".domain-name-static").html(Domain.val());
                    $(".timeline-static").html(timeline);
                    loadCompliances();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            }
        );
    }
}

activateUnit = function (element) {
    if(ACTIVE_UNITS.length >= 10){
        displayMessage(message.maximum_units);
        return false;
    }else{
        var chkstatus = $(element).attr('class');
        var chkid = $(element).attr('id');
        if (chkstatus == 'active') {
            $(element).removeClass('active');
            $(element).find('i').removeClass('fa fa-check pull-right');
            index = ACTIVE_UNITS.indexOf(parseInt(chkid));
            ACTIVE_UNITS.splice(index, 1);
        } else {
            $(element).addClass('active');
            $(element).find('i').addClass('fa fa-check pull-right');
            ACTIVE_UNITS.push(parseInt(chkid));
        }
    }
}



validateFirstTab = function()  {
    if (ACTIVE_UNITS.length <= 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
        TbodyComplianceList.empty();
        callAPI(API_Wizard2);
        isShowMore = true;
        return true;
    }
};


showTab = function(){    
    hideall = function() {
        // $('.setup-panel li').addClass('disabled');
        $('.statutory_mapping_tab li').removeClass('active');
        $('.tab-pane').removeClass('active in');
        $('#tab1').hide();
        $('#tab2').hide();
        SubmitButton.hide();
        NextButton.hide();
        PreviousButton.hide();
    }

    enabletabevent = function(tab) {
        if (tab == 1) {
            $('.tab-step-1 a').attr('href', '#tab1');
        }
        else if (tab == 2) {
            $('.tab-step-2 a').attr('href', '#tab2');
        }
    }
    disabletabevent = function() {
        $('.tab-step-1 a').removeAttr('href');
        $('.tab-step-2 a').removeAttr('href');
    }
    console.log("CURRENT_TAB-"+CURRENT_TAB);
    if (CURRENT_TAB == 1) {
        hideall();
        disabletabevent();
        enabletabevent(1);
        $('.tab-step-1').addClass('active')
        $('#tab1').addClass("active in");
        $('#tab1').show();
        NextButton.show();
    }
    else if (CURRENT_TAB == 2) {
        if(validateFirstTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        }
        hideall();
        enabletabevent(2);
        $('.tab-step-2').addClass('active')
        $('#tab2').addClass('active in');
        $('#tab2').show();
        SubmitButton.show();
        PreviousButton.show();
        showBreadCrumbText();
    }
}

showBreadCrumbText = function() {
    BreadCrumbs.empty();
    var img_clone = BreadCrumbImg;
    // BreadCrumbs.append(GroupName.val());

    if (BusinessGroupName.val()) {
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + BusinessGroupName.val() + " ");
    }

    BreadCrumbs.append(img_clone);
    BreadCrumbs.append(" " + LegalEntityName.html() + " ");

    if (FType.children(':selected').val()) {
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + FType.children(':selected').text() + " ");
    }

    if (Domain.val()) {
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + Domain.val() + " ");
    }
}

loadCompliances = function(){
    if(COMPLIANCES_LIST.length == 0){
        var no_record_row = $("#templates .table-no-record");
        var no_clone = no_record_row.clone();
        $(".tbody-compliance-list").append(no_clone);
        $(".total_count_view").hide();
    }else{
        $.each(COMPLIANCES_LIST, function(key, value) {
            if(LastAct != value.level_1_s_name){
                var acttableRow = $('#templates #headingOne');
                var clone = acttableRow.clone();
                $('.act-name', clone).attr('id', 'heading'+actCount);
                $('.panel-title a span', clone).text(value.level_1_s_name);
                $('.panel-title a', clone).attr('href', '#collapse'+actCount);
                $('.panel-title a', clone).attr('aria-controls', 'collapse'+actCount);

                $('.coll-title', clone).attr('id', 'collapse'+actCount);
                $('.coll-title', clone).attr('aria-labelledb', 'heading'+actCount);
                $('.tbody-compliance-list').append(clone);
                LastAct = value.level_1_s_name;
                actCount = actCount + 1;
            }
            // if(LastSubAct != value.map_text){
            //     var subTitleRow = $('#statutory-value .div-compliance-list .sub-title-row');
            //     var clone3 = subTitleRow.clone();
            //     $('.sub-title', clone3).text(value.map_text);
            //     $(' #collapse'+count+' .tbody-compliance-list').append(clone3);
            //     LastSubAct = value.map_text;
            // }

            var complianceDetailtableRow = $('#templates .div-compliance-list .compliance-details');
            var clone2 = complianceDetailtableRow.clone();
           
            $('.statutory-provision', clone2).text(value.s_provision);
            $('.compliance-task', clone2).text(value.comp_name);
            $('.repeats-by', clone2).text(value.comp_name);

            $('#collapse'+count+' .tbody-compliance-list').append(clone2);

        });
    }
}

r_s_page = new ReviewSettingsPage();

$(document).ready(function() {
    PageControls();    
    r_s_page.showLegalEntity();    
});
    