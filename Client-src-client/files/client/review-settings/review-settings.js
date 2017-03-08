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
var actCount = 1;
var LastAct = "";
var LastSubAct = "";
var count = 1;
var repeats_type = {1:"Days", 2:"Months", 3:"Years"};
var r_s_page = null;
var selectedcompliance = 0;
var userLegalentity = client_mirror.getSelectedLegalEntity();


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
    
    if(userLegalentity.length > 1){
        BusinessGroupName.hide();
        BusinessGroupSelect.show();
        LegalEntityName.hide();
        LegalEntitySelect.show();
        loadBusinessGroups();

       
        LegalEntitySelect.on("change", function(){
            var getle_id = $(".legal-entity-select option:selected").val()
            if(getle_id > 0 ){
                le_id = parseInt(getle_id);
                t_this.showTypeDomainList();
            }
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

function loadBusinessGroups(){
    var bgselect = '<option value="">Select</option>';
    $.each(user.entity_info, function(k, val){
        if(val["bg_name"] != null){
            bgselect = bgselect + '<option value="' + val["bg_id"] + '"> ' + val["bg_name"] + ' </option>';    
        }            
    });        
    BusinessGroupSelect.html(bgselect);
}

function loadLegalEntity(){
    LegalEntitySelect.html("");    
    var getbg_id = $(".business-group-select option:selected").val();        
    if(getbg_id == ""){
        getbg_id = null;
    }
    var select = '<option value="">Select</option>';
    $.each(user.entity_info, function(k, val){
        if(getbg_id == val['bg_id'])
            select = select + '<option value="' + val["le_id"] + '"> ' + val["le_name"] + ' </option>';
    });        
    LegalEntitySelect.html(select);
    
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
    $(".UnitList").empty();
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

SearchUnit.keyup(function () {
    var filter = jQuery(this).val();
    jQuery(".unit-list .unit-names").each(function () {
        if (jQuery(this).text().search(new RegExp(filter, "i")) < 0) {
            jQuery(this).hide();
        } else {
            jQuery(this).show()
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
                    console.log(el);
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
        $(".UnitList").empty();
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
    else if(BusinessGroupSelect.find("option:selected").val()){
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + BusinessGroupSelect.find("option:selected").text()+ " ");
    }

    if(LegalEntityName.val() > 1){
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + LegalEntityName.html() + " ");
    }
    else if(LegalEntitySelect.find("option:selected").val()){
        BreadCrumbs.append(img_clone);
        BreadCrumbs.append(" " + LegalEntitySelect.find("option:selected").text() + " ");
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
    }else{
        $(".accordion-div").empty();
        LastAct = '';
        $.each(COMPLIANCES_LIST, function(key, value) {
            if(LastAct != value.level_1_s_name){
                console.log("actCount--"+actCount);
                var acttableRow = $('#templates .p-head');
                var clone = acttableRow.clone();
                $('.act-name', clone).attr('id', 'heading'+actCount);
                $('.panel-title a span', clone).text(value.level_1_s_name);
                $('.panel-title a', clone).attr('href', '#collapse'+actCount);
                $('.panel-title a', clone).attr('aria-controls', 'collapse'+actCount);

                $('.coll-title', clone).attr('id', 'collapse'+actCount);
                $('.coll-title', clone).attr('aria-labelledb', 'heading'+actCount);
                $('.all-comp-checkbox', clone).on("click", function(){
                    var tableelement = $(this).closest(".table").find("tbody");
                    //var tabletbody = tableelement;
                    console.log(tableelement);
                    if($(this).prop("checked") == true){
                        console.log("welcomet 1")
                        console.log(tableelement.find("td .checkbox .comp_checkbox"));
                        var tdchecklist = tableelement.find(".comp_checkbox").prop("selected", true);
                    }else{
                        console.log("welcomet 2")
                        var tdchecklist = tableelement.find(".comp_checkbox").prop("selected", false);
                    }
                });
                $('.accordion-div').append(clone);
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
            $('.comp-checkbox').addClass("comp-checkbox-"+actCount);
            $('.comp-checkbox', clone2).on("click", function(){
                if($(this).prop("checked") == true){
                    selectedcompliance += 1;
                    var sdates = value.s_dates;
                    $(".repeat-every", clone2).show();
                    $(".review", clone2).show();
                    $(".due-date", clone2).show();
                    $(".trigger", clone2).show();
                    $(".repeat-every", clone2).val(value.r_every);
                    $('.repeat-every-type option[value='+value.repeats_type_id+']', clone2).attr('selected','selected');
                    var sdates= value.s_dates;
                    for(var i = 0; i<sdates.length; i++ ){
                        // $(".due-date", clone2).val(value.due_date);
                        // $(".trigger", clone2).val(sdates[0].trigger_before_days);    
                        var ddRow = $('#templates .due-date-templates .col-sm-12');
                        var ddclone = ddRow.clone();
                        
                        $(".due-date-div", clone2).append(ddclone);

                        var trigRow = $('#templates .trigger-templates .col-sm-8');
                        var trigclone = trigRow.clone();
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
                    SelectedCount.html(selectedcompliance);
                }
                else{
                    selectedcompliance -= 1;
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
            $('.repeats-by', clone2).text("Every "+value.r_every+" "+ repeats_type[value.repeats_type_id]);
            $('.old-repeat-by', clone2).val(value.r_every);
            $('.old-repeat-type-id', clone2).val(value.repeats_type_id);
            $('.old-due-date', clone2).val(value.due_date);
            $('.old-trigger', clone2).val(value.trigger_before_days);
            $('.old-statu', clone2).val(JSON.stringify(value.s_dates));
            $('.applicable-count', clone2).text(value.u_ids.length+" / "+ACTIVE_UNITS.length);
            $('.applicable-count', clone2).on('click', function() {
                displayPopup(value.u_ids);
            });

            $('#collapse'+count+' .tbody-compliance-list').append(clone2);

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

SubmitButton.on("click", function(){
    var checkedcount = $(".comp-checkbox:checked").length;
    console.log("checkedcount--"+checkedcount);
    if(checkedcount == 0){
        console.log('displayMessage("Select any one compliance")');
        displayMessage("Select any one compliance");
        return false;
    }else{
        var flag_status = 0;
        var selected_compliances_list = [];        
        $.each($(".comp-checkbox:checked").closest(".compliance-details"), function () {
            console.log(this);
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

            console.log("old_statu--"+old_statu);
           
            if(repeatevery == ""){
                console.log('displayMessage("Repeat Every Required for "+comtask);')
                displayMessage("Repeat Every Required for "+comtask);
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
                    console.log(duedate+">>>>"+trigger);

                    if(duedate == ""){
                        console.log('displayMessage("Due Date Required for "+comtask);');
                        displayMessage("Due Date Required for "+comtask);
                        return false;
                    }
                    if(trigger == ""){
                        console.log('displayMessage("Trigger Before Days Required for "+comtask);');
                        displayMessage("Trigger Before Days Required for "+comtask);
                        return false;
                    }            

                    var statu = {};                                      
                    statu['statutory_date'] = null;
                    statu['statutory_month'] = null;
                    statu['trigger_before_days'] = null;
                    statu['repeat_by'] = null;
                    console.log("**"+duedate);
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
                    console.log(repeatevery+"--"+repeateverytype+"--"+ duedate+"--"+ trigger+"--"+compid);
                    console.log("----"+old_repeat_by+"--"+old_repeat_type_id+"--"+ old_due_date+"--"+ old_trigger_before_days+"--"+compid);
                });
                old_due_date = null;
               
                // var old_statu = {};       
                // var old_statu_dates =[];
                // old_statu['statutory_date'] = null;
                // old_statu['statutory_month'] = null;
                // old_statu['trigger_before_days'] = old_trigger_before_days;
                // old_statu['repeats_by'] = null;
                // if(old_due_date != ''){
                //     var old_split_date = old_due_date.split("-");
                //     console.log("months.old_split_date[1]---"+months.old_split_date[1]);
                //     old_statu['statutory_date'] = old_split_date[0];
                //     old_statu['statutory_month'] = months.old_split_date[1];
                // }
                // if(trigger != ''){
                //     old_statu['trigger_before_days'] = old_trigger_before_days;   
                // }
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
        });
        if(flag_status > 0){
            client_mirror.saveReviewSettingsCompliance(parseInt(le_id), selected_compliances_list, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.save_success);
                    CURRENT_TAB = 1;
                    showTab();
                    r_s_page.showLegalEntity();
                    hideLoader();
                } else {
                    displayMessage(error);
                }
            });    
        }else{
            displayMessage(message.nocompliance_selected);
        }
        
    }
});

checkDateEndOfTheMonth = function(){

}

r_s_page = new ReviewSettingsPage();

$(document).ready(function() {
    PageControls();    
    loadBusinessGroups();
    loadLegalEntity();
    r_s_page.showLegalEntity();    
});
    