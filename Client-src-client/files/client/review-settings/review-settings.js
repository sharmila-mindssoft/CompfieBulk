var BusinessGroupName = $(".business-group-name");
var BusinessGroupSelect = $(".business-group-select");
var LegalEntityName = $(".legal-entity-name");
var LegalEntitySelect = $(".legal-entity-select");

var BusinessGroup = $(".business-group");
var BusinessGroupId = $("#business-group-id");
var AcBusinessGroup = $("#ac-business-group");

var LegalEntity = $(".legal-entity");
var LegalEntityId = $("#legal-entity-id");
var AcLegalEntity = $("#ac-legal-entity");

var FType = $(".frequency-type");
var Domain = $(".domain");
var DomainId = $("#domain-id");
var AcDomain = $("#ac-domain");

var ShowUnitButton = $(".show-unit-button");

var SearchUnit = $(".search-unit");
var SelectAll = $(".unit-selectall");

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

var SelectedCount = $(".selected-count");

var le_id = null;
var d_id = null;
var sno = 1;
var temp_ftype = "";
var actCount = 0;
var LastAct = "";
var LastSubAct = "";
var count = 1;
var repeats_type = {1:"Days", 2:"Months", 3:"Years"};
var r_s_page = null;
var selectedcompliance = 0;
var userLegalentity = client_mirror.getSelectedLegalEntity();
var userBusinessGroup = [];
var currentDate = null;
$.each(userLegalentity, function(k, val){
    if(val.bg_id != null){        
        userBusinessGroup.push(val);
    } 
});

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

    BusinessGroup.keyup(function(e) {        
        var text_val = BusinessGroup.val().trim();                
        commonAutoComplete(e, AcBusinessGroup, BusinessGroupId, text_val, userBusinessGroup, "bg_name", "bg_id", function(val) {
            onBusinessGroupAutoCompleteSuccess(val);
        });
    });

    LegalEntity.keyup(function(e) {
        var text_val = LegalEntity.val().trim();
        // var legalentityList = r_s_page._LegalEntityList;
        if(BusinessGroupId.val() != ""){
            var condition_fields = ["bg_id"];
            var condition_values = [bg_id];    
        }        
        commonAutoComplete(e, AcLegalEntity, LegalEntityId, text_val, userLegalentity, "le_name", "le_id", function(val) {
            onLegalEntityAutoCompleteSuccess(val);
        }, condition_fields, condition_values);
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
        SelectAll.prop('checked', false);
        ACTIVE_UNITS = [];
        r_s_page.getUnitList();
    });
}

onBusinessGroupAutoCompleteSuccess = function(val) {
    BusinessGroup.val(val[1]);
    BusinessGroupId.val(val[0]);
    BusinessGroup.focus();
    bg_id = val[0];
}

onLegalEntityAutoCompleteSuccess = function(val) {    
    LegalEntity.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntity.focus();
    le_id = val[0];
    r_s_page.showTypeDomainList();
}

onDomainAutoCompleteSuccess = function(val) {
    Domain.val(val[1]);
    DomainId.val(val[0]);
    Domain.focus();
}


ReviewSettingsPage = function () {
    this._TypeList = [];
    this._BusinessGroupList = [];
    this._LegalEntityList = [];
    this._DomainList = [];
    this._Units = [];
    this._ComplianceList = [];
}

ReviewSettingsPage.prototype.showLegalEntity = function (){    
    var t_this = this;
    NextButton.hide();
    PreviousButton.hide();
    SubmitButton.hide();
    
    if(userLegalentity.length > 1){
        BusinessGroupName.hide();
        BusinessGroupSelect.show();
        LegalEntityName.hide();
        LegalEntitySelect.show();
        // loadBusinessGroups();
       
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
    client_mirror.getReviewSettingsFilters(parseInt(le_id), function(error, response) {
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
    UnitList.empty();
    t_this = this;
    d_id = DomainId.val();
    if(le_id == null){
        displayMessage(message.legalentity_required);
        return false;
    }    
    if(FType.find('option:selected').val() == ""){
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
        client_mirror.getReviewSettingsUnitFilters(parseInt(le_id), parseInt(d_id), function(error, response) {
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

SearchUnit.keyup(function () {
    var filter = jQuery(this).val();
    jQuery(".unit-list .unit-names").each(function () {        
        if (jQuery(this).text().search(new RegExp(filter, "i")) < 0) {
            jQuery(this).hide();
            jQuery(".unit-list .heading").hide();
        } else {
            jQuery(this).show();
            jQuery(".unit-list .heading").hide();
        }
        if(filter == ""){
            jQuery(".unit-list .heading").show();
        }
    });
});

ReviewSettingsPage.prototype.renderUnitList = function(_Units) {
    UNIT_CS_ID = {};
    if(UnitList.length == 0){
        var UnitRow = $(".unit-list-ul li");
        var clone = UnitRow.clone();
        clone.text('No Units Found');
        UnitList.append(clone);
        $(".reviewcheck").hide();
    }else{        
        $(".reviewcheck").show();
        var temp_d_name = "";
        $.each(_Units, function(key, value) {

            unit_idval = value.u_id;
            unit_text = value.u_code + " - " + value.u_name + " - " + value.address;
            var d_name = value.div_name;
            if(temp_d_name != d_name){
                if(d_name != null){
                    var UnitRowheading = $(".unit-list-ul .heading");
                    var cloneHeading = UnitRowheading.clone();    
                    cloneHeading.html(d_name);
                    UnitList.append(cloneHeading);
                }else{
                    var UnitRowheading = $(".unit-list-ul .heading");
                    var cloneHeading = UnitRowheading.clone();    
                    cloneHeading.html("Others");
                    UnitList.append(cloneHeading);
                }
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

SelectAll.click(function() {
    ACTIVE_UNITS = [];
    //UNIT_CS_ID = {};
    if (UnitList.length > 0) {
        $('.unit-list .unit-names').each(function(index, el) {
            if (ACTIVE_UNITS.length >= 20) {
                displayMessage(message.maximum_units);
                return false;
            } else {
                if (SelectAll.prop('checked')) {
                    $(el).addClass('active');
                    $(el).find('i').addClass('fa fa-check pull-right');
                    var chkid = $(el).attr('id');
                    ACTIVE_UNITS.push(parseInt(chkid));
                } else {
                    $(el).removeClass('active');
                    $(el).find('i').removeClass('fa fa-check pull-right');
                }
            }
        });
    }

});

callAPI = function(api_type) {
    if(api_type = "API_Wizard2"){
        displayLoader();
        showBreadCrumbText();
        client_mirror.getReviewSettingsComplianceFilters(
            parseInt(le_id), parseInt(d_id), ACTIVE_UNITS, parseInt(temp_ftype), (sno-1),
            function(error, data) {
                if (error == null) {
                    COMPLIANCES_LIST = data.rs_compliance_list;
                    var timeline = data.timeline;
                    totalRecord = data.total_records;
                    $(".domain-name-static").html(Domain.val());
                    $(".timeline-static").html(timeline);
                    loadCompliances();
                    hideLoader();
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
        var chkstatus = $(element).hasClass("active");        
        var chkid = $(element).attr('id');
        if (chkstatus == true) {
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
        actCount = 1;
        callAPI(API_Wizard2);
        isShowMore = true;
        return true;
    }
};

// clearElement = function(arr) {
//     if (arr.length > 0) {
//         $.each(arr, function(i, element) {
//             element.val('');
//         });
//     }
// }


showTab = function(){    
    hideall = function() {
        // $('.setup-panel li').addClass('disabled');
        $('.statutory_mapping_tab li').removeClass('active');
        $('.tab-pane').removeClass('active in');
        $('#tab1').hide();
        $('#tab2').hide();
        //UnitList.empty();
        //clearElement(Domain, DomainId);
        // Domain.val('');
        // DomainId.val('');
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
        $(".accordion-div").empty();
        SubmitButton.show();
        PreviousButton.show();
        showBreadCrumbText();
    }
}

showBreadCrumbText = function() {
    BreadCrumbs.empty();
    var img_clone = BreadCrumbImg;
    // BreadCrumbs.append(GroupName.val());

    if (BusinessGroupName.text()) {        
        BreadCrumbs.append(" " + BusinessGroupName.val() + " ");
        BreadCrumbs.append(img_clone);
    }
    else if(BusinessGroupId.val()){
        BreadCrumbs.append(" " + BusinessGroup.val()+ " ");
        BreadCrumbs.append(img_clone);
    }

    if(LegalEntityName.text()){        
        BreadCrumbs.append(" " + LegalEntityName.html() + " ");
    }
    else if(LegalEntity.val()){
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + LegalEntity.val() + " ");
    }

    if (FType.find("option:selected").val()) {
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + FType.find("option:selected").text() + " ");
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
        $(".accordion-div").append(no_clone);
        $(".total_count_view").hide();
         SubmitButton.hide();
    }else{
        $(".accordion-div").empty();
        LastAct = '';
        $.each(COMPLIANCES_LIST, function(key, value) {
            if(LastAct != value.level_1_s_name){
                actCount = actCount + 1;
                var acttableRow = $('#templates .p-head');
                var clone = acttableRow.clone();
                $('.act-name', clone).attr('id', 'heading'+actCount);
                $('.panel-title a span', clone).text(value.level_1_s_name);
                $('.panel-title a', clone).attr('href', '#collapse'+actCount);
                $('.panel-title a', clone).attr('aria-controls', 'collapse'+actCount);

                $('.coll-title', clone).attr('id', 'collapse'+actCount);
                $('.coll-title', clone).attr('aria-labelledb', 'heading'+actCount);
                // $('#collapse'+actCount+' tbody', clone).addClass("welcome");
                $('#checkbox1', clone).on("click", function(){
                    var tableelement = $(this).closest(".table").find("tbody");
                    if($(this).prop("checked") == true){
                        $.each(tableelement.find('input:checkbox.comp-checkbox'), function(){
                            var tdcheckbox = $(this).prop("checked", true).triggerHandler('click');
                            //tdcheckbox.trigger('click');
                            // $('.comp-checkbox', clone2);
                        });                        
                    }else{
                        //var tdcheckbox = $(this).prop("checked", false).triggerHandler('click');
                        $.each(tableelement.find('input:checkbox.comp-checkbox'), function(){

                            var tdchecklist = tableelement.find("input:checkbox.comp-checkbox").prop("checked", false);
                            $(this).prop("checked", false).triggerHandler('click');
                        });
                    }
                });
                $('.accordion-div').append(clone);
                LastAct = value.level_1_s_name;
                

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
            $('.comp-checkbox').addClass("comp-checkbox-"+actCount);
            $('#checkbox2', clone2).click(function(){
                if($(this).prop("checked") == true){
                    $(".due-date-div", clone2).empty();
                    $(".trigger-div", clone2).empty();                    
                    var sdates = value.s_dates;
                    $(".repeat-every", clone2).show();
                    $(".review", clone2).show();
                    $(".due-date", clone2).show();
                    $(".trigger", clone2).show();
                    $(".repeat-every", clone2).val(value.r_every);
                    $('.repeat-every-type option[value='+value.repeats_type_id+']', clone2).attr('selected','selected');
                    var sdates= value.s_dates;
                    if(FType.find("option:selected").val() == 3){
                        if(value.repeats_type_id == 1){
                            $('.repeat-every-type option[value="2"]', clone2).remove();
                            $('.repeat-every-type option[value="3"]', clone2).remove();                        
                            $(".repeat-every", clone2).keyup(function(){                                
                                if($(this).val() > value.r_every){
                                    $(this).val(value.r_every);
                                    displayMessage(message.repeats_type_not_exceed_actual_value);
                                    return false;
                                }                                
                            });
                        }
                        if(value.repeats_type_id == 2){           
                            $('.repeat-every-type option[value="3"]', clone2).remove();
                            $(".repeat-every", clone2).keyup(function(){             
                                // option[value='+value.repeats_type_id+']
                                if($(this).val() > value.r_every && $('.repeat-every-type', clone2).val() == 2){
                                     $(this).val(value.r_every);
                                     displayMessage(message.repeats_type_not_exceed_actual_value);
                                     return false;
                                }                                
                                if (12 % parseInt($(this).val()) == 0 ) {
                                    if(sdates.length > 1){
                                        var val_repevery = 12 / $(this).val();
                                        console.log(val_repevery);
                                        $(".due-date-div", clone2).html("");
                                        $(".trigger-div", clone2).html("");
                                        for(var j = 0; j < val_repevery; j++){
                                            var ddRow = $('#templates .due-date-templates .col-sm-12');
                                            var ddclone = ddRow.clone();    
                                            $('.due-date', ddclone).datepicker({
                                                changeMonth: true,
                                                changeYear: true,
                                                numberOfMonths: 1,
                                                dateFormat: 'dd-M-yy',
                                                monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                                            });                                     
                                            $(".due-date-div", clone2).append(ddclone);   

                                            var trigRow = $('#templates .trigger-templates .col-sm-8');
                                            var trigclone = trigRow.clone();                                    
                                            $('.trigger', trigclone).on('input', function(e) {
                                                this.value = isNumbers($(this));
                                            });
                                            $(".trigger-div", clone2).append(trigclone); 
                                        }
                                    }else{
                                        $(".due-date-div", clone2).html("");
                                        $(".trigger-div", clone2).html("");
                                        var ddRow = $('#templates .due-date-templates .col-sm-12');
                                        var ddclone = ddRow.clone();        
                                        $('.due-date', ddclone).datepicker({
                                            changeMonth: true,
                                            changeYear: true,
                                            numberOfMonths: 1,
                                            dateFormat: 'dd-M-yy',
                                            monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                                        });                                 
                                        $(".due-date-div", clone2).append(ddclone);   

                                        var trigRow = $('#templates .trigger-templates .col-sm-8');
                                        var trigclone = trigRow.clone();                                    
                                        $('.trigger', trigclone).on('input', function(e) {
                                            this.value = isNumbers($(this));
                                        });
                                        $(".trigger-div", clone2).append(trigclone); 

                                    }
                                }else{  
                                    $(".due-date-div", clone2).html("");
                                    $(".trigger-div", clone2).html("");
                                    var ddRow = $('#templates .due-date-templates .col-sm-12');
                                    var ddclone = ddRow.clone();        
                                    $('.due-date', ddclone).datepicker({
                                        changeMonth: true,
                                        changeYear: true,
                                        numberOfMonths: 1,
                                        dateFormat: 'dd-M-yy',
                                        monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                                    });                                 
                                    $(".due-date-div", clone2).append(ddclone);   

                                    var trigRow = $('#templates .trigger-templates .col-sm-8');
                                    var trigclone = trigRow.clone();                                    
                                    $('.trigger', trigclone).on('input', function(e) {
                                        this.value = isNumbers($(this));
                                    });
                                    $(".trigger-div", clone2).append(trigclone); 
                                }
                                
                            });
                            
                        }    
                    }
                    if(FType.find("option:selected").val() == 4){
                        $(".repeat-every", clone2).keyup(function(){                                       
                            if (12 % parseInt($(this).val()) == 0 ) {
                                if(sdates.length > 1){
                                    var val_repevery = 12 / $(this).val();                                
                                    $(".due-date-div", clone2).html("");
                                    $(".trigger-div", clone2).html("");
                                    for(var j = 0; j < val_repevery; j++){
                                        var ddRow = $('#templates .due-date-templates .col-sm-12');
                                        var ddclone = ddRow.clone();    
                                        $('.due-date', ddclone).datepicker({
                                            changeMonth: true,
                                            changeYear: true,
                                            numberOfMonths: 1,
                                            dateFormat: 'dd-M-yy',
                                            monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                                        });                                     
                                        $(".due-date-div", clone2).append(ddclone);   

                                        var trigRow = $('#templates .trigger-templates .col-sm-8');
                                        var trigclone = trigRow.clone();                                    
                                        $('.trigger', trigclone).on('input', function(e) {
                                            this.value = isNumbers($(this));
                                        });
                                        $(".trigger-div", clone2).append(trigclone); 
                                    }
                                }
                                else{
                                    $(".due-date-div", clone2).html("");
                                    $(".trigger-div", clone2).html("");
                                    var ddRow = $('#templates .due-date-templates .col-sm-12');
                                    var ddclone = ddRow.clone();        
                                    $('.due-date', ddclone).datepicker({
                                        changeMonth: true,
                                        changeYear: true,
                                        numberOfMonths: 1,
                                        dateFormat: 'dd-M-yy',
                                        monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                                    });                                 
                                    $(".due-date-div", clone2).append(ddclone);   

                                    var trigRow = $('#templates .trigger-templates .col-sm-8');
                                    var trigclone = trigRow.clone();                                    
                                    $('.trigger', trigclone).on('input', function(e) {
                                        this.value = isNumbers($(this));
                                    });
                                    $(".trigger-div", clone2).append(trigclone); 
                                }
                            }else{  
                                $(".due-date-div", clone2).html("");
                                $(".trigger-div", clone2).html("");
                                var ddRow = $('#templates .due-date-templates .col-sm-12');
                                var ddclone = ddRow.clone();        
                                $('.due-date', ddclone).datepicker({
                                    changeMonth: true,
                                    changeYear: true,
                                    numberOfMonths: 1,
                                    dateFormat: 'dd-M-yy',
                                    monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                                });                                 
                                $(".due-date-div", clone2).append(ddclone);   

                                var trigRow = $('#templates .trigger-templates .col-sm-8');
                                var trigclone = trigRow.clone();                                    
                                $('.trigger', trigclone).on('input', function(e) {
                                    this.value = isNumbers($(this));
                                });
                                $(".trigger-div", clone2).append(trigclone); 
                            }
                            
                        });
                    }
                    
                    
                    var due_date_list= value.due_date_list;                    
                    for(var i = 0; i<sdates.length; i++ ){
                        var ddRow = $('#templates .due-date-templates .col-sm-12');
                        var ddclone = ddRow.clone();      
                        $(".due-date", ddclone).val(due_date_list[i]);
                        $('.due-date', ddclone).datepicker({
                            changeMonth: true,
                            changeYear: true,
                            numberOfMonths: 1,
                            dateFormat: 'dd-M-yy',
                            monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                        });   
                        $(".due-date-div", clone2).append(ddclone);

                        var trigRow = $('#templates .trigger-templates .col-sm-8');
                        var trigclone = trigRow.clone();
                        $(".trigger", trigclone).val(sdates[i].trigger_before_days);    
                        $('.trigger', trigclone).on('input', function(e) {
                            this.value = isNumbers($(this));
                        });
                        $(".trigger-div", clone2).append(trigclone);
                    }  
                    $('.due-date', clone2).datepicker({
                        changeMonth: true,
                        changeYear: true,
                        numberOfMonths: 1,
                        dateFormat: 'dd-M-yy',
                        monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                    });     

                    selectedcompliance += 1;
                    SelectedCount.html(selectedcompliance);
                }
                else{
                    selectedcompliance = selectedcompliance - 1;
                    SelectedCount.html(selectedcompliance);
                    $(".repeat-every", clone2).hide();
                    $(".review", clone2).hide();
                    $(".due-date", clone2).hide();
                    $(".trigger", clone2).hide();
                }
            });
            $('.compliance-id', clone2).val(value.comp_id)
            $('.statutory-provision', clone2).text(value.s_prov);
            $('.compliance-task', clone2).text(value.comp_name);
            if(value.r_every != null || value.r_every != undefined){
                $('.repeats-by', clone2).text("Every "+value.r_every+" "+ repeats_type[value.repeats_type_id]);    
            }else{
                $('.repeats-by', clone2).text("-");    
            }            
            $('.old-repeat-by', clone2).val(value.r_every);
            $('.old-repeat-type-id', clone2).val(value.repeats_type_id);
            $('.old-due-date', clone2).val(value.due_date);
            $('.old-trigger', clone2).val(value.trigger_before_days);
            $('.old-statu', clone2).val(JSON.stringify(value.s_dates));
            $('.applicable-count', clone2).text(value.u_ids.length+" / "+ACTIVE_UNITS.length);
            $('.applicable-count', clone2).on('click', function() {
                displayPopup(value.u_ids);
            });
            $('#collapse'+actCount+' .tbody-compliance-list').append(clone2);

        });
    }
}

displayPopup = function(unit_ids){
    $('.model-unit-list').find('p').remove();
    $.each(unit_ids, function(k, v) {
        var UnitsRow = $('#templates p');
        var cloneUnit = UnitsRow.clone();        
        var units = UNIT_CS_ID[v];
        cloneUnit.text(units.u_code+" - "+units.u_name+" - "+units.address);
        $('.model-unit-list').append(cloneUnit);        
    });
    Custombox.open({
        target: '#custom-modal',
        effect: 'contentscale',
        complete: function() {
            isAuthenticate = false;
        }
    });
}


function convert_date(data) {
  var date = data.split('-');
  var months = [
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
  ];
  for (var j = 0; j < months.length; j++) {
    if (date[1] == months[j]) {
      date[1] = months.indexOf(months[j]) + 1;
    }
  }
  if (date[1] < 10) {
    date[1] = '0' + date[1];
  }
  return new Date(date[2], date[1] - 1, date[0]);
}



SubmitButton.on("click", function(){
    var checkedcount = $(".comp-checkbox:checked").length;
    if(checkedcount == 0){
        displayMessage("Select any one compliance");
        return false;
    }else{
        var flag_status = 0;
        var selected_compliances_list = [];  
        var dt = 0;
        $.each($(".comp-checkbox:checked").closest(".compliance-details"), function () {
            flag_status = 0;
            dt = 0;   
            // $(".comp-checkbox:checked").each(function(e){
            var data = this;
            var compid = $(data).find(".compliance-id").val();
            var comtask = $(data).find(".compliance-task").text();
            var repeatevery = $(data).find(".repeat-every").val();
            var repeateverytype = $(data).find(".repeat-every-type").val();
            var old_repeat_by = $(data).find(".old-repeat-by").val();
            var old_repeat_type_id = $(data).find(".old-repeat-type-id").val();
            var old_due_date = $(data).find(".old-due-date").val();
            var old_trigger_before_days = $(data).find(".old-trigger").val();
            var old_statu = $(data).find(".old-statu").val();
            
            if(repeatevery == ""){
                displayMessage("Repeat Every Required for "+comtask);
                return false;
            }
            else if(repeatevery.length > 3){
                displayMessage("Repeat Every: Maximum 3 Digits are allowed for "+comtask);
                return false;
            }
            else{ 
                var eachloop = $(data).find(".due-date-div .col-sm-12");
                var duedate_first, trigger_first;
                var months = {Jan:1, Feb:2, Mar:3, Apr:4, May:5, Jun:6, Jul:7, Aug:8, Sep:9, Oct:10, Nov:11, Dec:12 };
                var statu_dates =[];                
                var c = 1;
               
                $.each(eachloop, function(k, val){
                    var duedate_input = $(data).find(".due-date-div .col-sm-12:nth-child("+c+") input");
                    var trigger_input = $(data).find(".trigger-div .col-sm-8:nth-child("+c+") input");
                    var duedate = duedate_input.val();
                    var trigger = trigger_input.val();
                    if(c == 1){
                        duedate_first = duedate;
                        trigger_first = parseInt(trigger);    
                    }                                        
                    
                    if(duedate == ""){                        
                        displayMessage("Due Date Required for "+comtask);
                        dt = 1;
                        return false;
                    }           
                    else if(trigger == ""){                    
                        displayMessage("Trigger Before Days Required for "+comtask);
                        dt = 1;
                        return false;
                    }    
                    else{
                        dt = 0;
                        var max_triggerbefore = 0;
                        var max_repeatevery = 0;
                        if (repeateverytype != null) {
                          if (repeateverytype == 1) {                            
                            max_triggerbefore = repeatevery;
                          } else if (repeateverytype == 2) {                            
                            max_triggerbefore = repeatevery * 30;
                          } else {
                            max_triggerbefore = repeatevery * 365;
                          }
                        }
                        if(old_repeat_type_id != null){
                          if (old_repeat_type_id == 1) {                            
                            max_repeatevery = old_repeat_by;
                          } else if (old_repeat_type_id == 2) {                            
                            max_repeatevery = old_repeat_by * 30;
                          } else {
                            max_repeatevery = old_repeat_by * 365;
                          }

                        }
                        if(repeatevery != ''){

                            repeatevery = parseInt(repeatevery);
                             if (repeatevery == 0) {
                                displayMessage(message.repeatevery_iszero + comtask);
                                dt = 1;
                                return false;
                            }
                            if (max_repeatevery > 0 && repeatevery > max_repeatevery) {
                                displayMessage(message.repeats_every_less_equal_old_repeats_every + comtask);
                                dt = 1;
                                return false;
                            }
                        }
                        if (trigger != '') {                            
                            trigger = parseInt(trigger);
                            if (trigger > 100) {
                                displayMessage(message.triggerbefore_exceed + comtask);
                                dt = 1;
                                return false;
                            }
                            if (trigger == 0) {
                                displayMessage(message.triggerbefore_iszero + comtask);
                                dt = 1;
                                return false;
                            }
                            if (max_triggerbefore > 0 && trigger > max_triggerbefore) {
                                displayMessage(message.triggerdays_exceeding_repeatsevery + comtask);
                                dt = 1;
                                return false;
                            }
                        }

                        var convertDueDate = convert_date(duedate);
                        var convertCDate = convert_date(currentDate);
                        if (convertDueDate < convertCDate) {
                            displayMessage(message.duedatelessthantoday_compliance + comtask);
                            dt = 1;
                            return false;
                        }

                        var statu = {};                                      
                        statu['statutory_date'] = null;
                        statu['statutory_month'] = null;
                        statu['trigger_before_days'] = null;
                        statu['repeat_by'] = null;

                        if(duedate != ''){
                            var split_date = duedate.split("-");
                            statu['statutory_date'] = parseInt(split_date[0]);
                            statu['statutory_month'] = months[split_date[1]];
                        }
                        if(trigger != ""){
                            statu['trigger_before_days'] = parseInt(trigger);   
                        }
                        statu_dates.push(statu);
                        c++;                        
                        
                    }
                });
                old_due_date = null;
                if(dt == 0){
                    old_statu_dates = jQuery.parseJSON(old_statu);                
                    selected_compliances_list.push(
                        client_mirror.saveReviewSettingsComplianceDict(
                            parseInt(compid), parseInt(le_id), parseInt(d_id), parseInt(temp_ftype), ACTIVE_UNITS, parseInt(repeatevery), 
                            parseInt(repeateverytype), duedate_first, trigger_first, statu_dates, parseInt(old_repeat_by),
                            parseInt(old_repeat_type_id), old_due_date, old_statu_dates
                        )
                    );
                    flag_status = 1;
                }
                
            }
        });
        if(flag_status > 0){
            client_mirror.saveReviewSettingsCompliance(parseInt(le_id), selected_compliances_list, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.review_settings_submit_success);
                    le_id = null;
                    FType.find("option:gt(0)").remove();
                    BusinessGroup.val('');
                    BusinessGroupId.val('');
                    LegalEntity.val('');
                    LegalEntityId.val('');
                    Domain.val('');
                    DomainId.val('');
                    ACTIVE_UNITS = [];
                    UnitList.empty();
                    $(".step-1-unit-list").hide();
                    CURRENT_TAB = 1;
                    showTab();
                    SelectAll.prop("checked", false);
                    r_s_page.showLegalEntity();
                    hideLoader();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            });    
        }
        else if(dt == 1){                
        }
        else{
            displayMessage(message.nocompliance_selected);
        }
        
    }
});

checkDateEndOfTheMonth = function(){

}

r_s_page = new ReviewSettingsPage();

$(document).ready(function() {
    current_date(function (c_date){
        currentDate = c_date;
        PageControls();    
        r_s_page.showLegalEntity();
    });  
});
    