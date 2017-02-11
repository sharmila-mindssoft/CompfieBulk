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
        $(".accordion-div").append(no_clone);
        $(".total_count_view").hide();
    }else{
        $(".accordion-div").empty();
        LastAct = '';
        $.each(COMPLIANCES_LIST, function(key, value) {
            console.log(LastAct +"!="+ value.level_1_s_name)
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
                    if($(this).prop("checked") == true){

                    }else{

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
                console.log("property--"+$(this).prop("checked"));
                if($(this).prop("checked") == true){
                    var sdates = value.s_dates;
                    $(".repeat-every", clone2).show();
                    $(".review", clone2).show();
                    $(".due-date", clone2).show();
                    $(".trigger", clone2).show();
                    $(".repeat-every", clone2).val(value.r_every);
                    $('.repeat-every-type option[value='+sdates[0].repeats_type_id+']', clone2).attr('selected','selected');
                    $(".due-date", clone2).val(value.due_date);
                    $(".trigger", clone2).val(sdates[0].trigger_before_days);
                    $('.due-date', clone2).datepicker({
                      changeMonth: true,
                      changeYear: true,
                      numberOfMonths: 1,
                      dateFormat: 'dd-M-yy',
                      monthNames: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
                    });
                }
                else{
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
            $('.old-repeat-by', clone2).text(value.r_every);
            $('.old-repeat-type-id', clone2).text(value.repeats_type_id);
            $('.old-due-date', clone2).text(value.due_date);
            $('.old-trigger', clone2).text(value.trigger_before_days);
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
        $(".unit-static").text(UNIT_CS_ID[v]);
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
        var selected_compliances_list = [];
        $.each($(".comp-checkbox:checked").closest("td").siblings("td"), function () {
        // $(".comp-checkbox:checked").each(function(e){
            var data = $(this).parents('tr:eq(0)');
            var compid = $(data).find(".compliance-id").val();
            var comtask = $(data).find(".compliance-task").text();
            var repeatevery = $(data).find(".repeat-every").val();
            var repeateverytype = $(data).find(".repeat-every-type").val();
            var duedate = $(data).find(".due-date").val();
            var trigger = $(data).find(".trigger").val();
            var old_repeat_by = $(data).find(".old_repeat_by").val();
            var old_repeat_type_id = $(data).find(".old_repeat_type_id").val();
            var old_due_date = $(data).find(".old_due_date").val();
            var old_trigger_before_days = $(data).find(".old_trigger_before_days").val();


            console.log(repeatevery+"--"+repeateverytype+"--"+ duedate+"--"+ trigger+"--"+compid);
            console.log("----"+old_repeat_by+"--"+old_repeat_type_id+"--"+ old_due_date+"--"+ old_trigger_before_days+"--"+compid);
            if(repeatevery == ""){
                console.log('displayMessage("Repeat Every Required for "+comtask);')
                displayMessage("Repeat Every Required for "+comtask);
                return false;
            }
            else if(duedate == ""){
                console.log('displayMessage("Due Date Required for "+comtask);');
                displayMessage("Due Date Required for "+comtask);
                return false;
            }
            else if(trigger == ""){
                console.log('displayMessage("Trigger Before Days Required for "+comtask);');
                displayMessage("Trigger Before Days Required for "+comtask);
                return false;
            }            
            else{                
                selected_compliances_list.push(
                    client_mirror.saveReviewSettingsComplianceDict(
                        parseInt(le_id), parseInt(d_id), parseInt(temp_ftype), ACTIVE_UNITS, parseInt(compid), parseInt(repeatevery), 
                        parseInt(repeateverytype), duedate, parseInt(trigger), parseInt(old_repeat_by),
                        parseInt(old_repeat_type_id), old_due_date, parseInt(old_trigger_before_days)
                    )
                );
            }
        });
        client_mirror.saveReviewSettingsCompliance(selected_compliances_list, function(error, response) {
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
    }
});

r_s_page = new ReviewSettingsPage();

$(document).ready(function() {
    PageControls();    
    r_s_page.showLegalEntity();    
});
    