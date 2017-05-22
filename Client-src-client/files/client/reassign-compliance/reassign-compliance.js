var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();
var CURRENT_TAB = 1;
var DOMAINS = null;
var UNITS = null;
var USERS = null;
var FILTER_USERS = null;
var REASSIGN_UNITS = null;
var ComplianceList = null;

var ASSIGNEE_SU = {};
var APPROVER_SU = {};
var two_level_approve;

var NextButton = $('#btn-next');
var PreviousButton = $('#btn-previous');
var SubmitButton = $("#btn-submit");
var ShowMore = $(".btn-showmore");
var CancelButton = $('#btn-cancel');

var ReassignView = $("#reassigncompliance-view");
var ReassignAdd = $("#reassigncompliance-add");

var ShowButton = $(".btn-show");
var ReassignButton = $(".btn-reassign");

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");

var DomainName = $("#domain_name");
var DomainId = $("#domain_id");
var ACDomain = $("#ac-domain");

var UserName = $("#user_name");
var UserId = $("#user_id");
var ACUser = $("#ac-user");

var UnitName = $("#unit_name");
var UnitId = $("#unit_id");
var ACUnit = $("#ac-unit");

var UserType = $("#user_type");
var Reason = $("#reason");

var UnitList = $("#datatable-responsive .tbody-unit-list");
var UnitRow = $("#templates .table-unit .table-row");
var UserTypeRow = $("#templates .table-unit .table-type-row");

var SelectedUnitCount = $(".selected_checkbox_count");
var SelectedUnitView = $(".selected_checkbox");

var ACTIVE_UNITS = [];
var LastUserType = '';
var UTYPE = 0;

var REASSIGN_FILTER = "reassign_filter";
var GET_COMPLIANCE = "get_compliance";
var SUBMIT_API = 'submit_api';

var LastUnit = '';
var LastAct = '';
var LastType = '';
var SCOUNT = 0;
var ACOUNT = 0;
var UCOUNT = 0;
var totalRecord = 10;
var mUnit = 5;

var SELECTED_COMPLIANCE = {};

var Filter_List = $('.filter-list');
var OLD_USERS_ = [];
var CHECK_USER_CATEGORY = 0;

function callAPI(api_type) {
    if (api_type == REASSIGN_FILTER) { 
        displayLoader();
        client_mirror.getReassignComplianceFilters(parseInt(LegalEntityId.val()),
            function(error, data) {
                if (error == null) {
                    DOMAINS = data.domains;
                    UNITS = data.units;
                    FILTER_USERS = data.legal_entity_users;
                    hideLoader();
                } else {
                    hideLoader();
                    displayMessage(error);
                }
        });
    }

    else if (api_type == GET_COMPLIANCE) { 
        displayLoader();
        var val_legal_entity_id = LegalEntityId.val();
        var val_domain_id = DomainId.val();
        var val_user_id = UserId.val();
        client_mirror.getReAssignComplianceForUnits(int(val_legal_entity_id), 
            int(val_domain_id), int(val_user_id), UTYPE, ACTIVE_UNITS, SCOUNT,
            function(error, data) {
            if (error == null) {
                ComplianceList = data.reassign_compliances;
                //ActList = data.level_one_name;
                loadCompliances();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    }

    else if (api_type == SUBMIT_API) { 
        //displayLoader();
        var ass_Id = null;
        var con_Id = null;
        var app_Id = null;
        var ass_Name = null;
        
        if ($('.assigneelist.active').attr('id') != undefined) {
            if(UTYPE == 1){
                ass_Id = parseInt($('.assigneelist.active').attr('id'));
            }
            else if(UTYPE == 2){
                con_Id = parseInt($('.assigneelist.active').attr('id'));
            }
            else if(UTYPE == 3){
                app_Id = parseInt($('.assigneelist.active').attr('id'));
            }
            ass_Name = $('.assigneelist.active').text().trim();
        }

        
        var reason = null;
        var le_id = LegalEntityId.val();
        var r_from = UserId.val();
        var reason = Reason.val();

        var rCompliances = [];
        $('.comp-checkbox:checkbox:checked').each(function (index, el) {
            var id = $(this).attr("id").split('-');
            var c_no = id[1];

            var old_ = $('#combineid'+c_no).attr("data-old").split('#');
            var comb_ = $('#combineid' + c_no).val().split('#');

            var h_id = null;
            if(comb_[3] != null) h_id = parseInt(comb_[3]);

            var d_date = null;
            if ($('#duedate' + c_no).val() != '' && $('#duedate' + c_no).val() != undefined) {
                d_date = $('#duedate' + c_no).val();
            }
            
            rcData = client_mirror.reassignComplianceDet(parseInt(comb_[1]), parseInt(comb_[0]), comb_[2], 
                h_id, d_date, parseInt(old_[0]), parseInt(old_[1]), parseInt(old_[2]));
            rCompliances.push(rcData);
        });
        /*console.log(SELECTED_COMPLIANCE);*/

        client_mirror.saveReassignCompliance(parseInt(le_id), parseInt(r_from), ass_Id, ass_Name, con_Id, app_Id, rCompliances, reason, 
            function (error, response) {
            if (error == null) {
                displaySuccessMessage(message.compliance_reassign_success);
                ReassignView.show();
                ReassignAdd.hide();
                initialize();
                hideLoader();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    }
}

function getUserLevel(selectedUserId) {
  var getuserLevel = null;
  for (var user in USERS) {
    var userId = USERS[user].usr_id;
    if (userId == selectedUserId) {
      getuserLevel = USERS[user].usr_cat_id;
    }
  }
  return getuserLevel;
}

//load available user in third wizard
function loadUser(userType) {
    var selectedUnit = $('#assignee_unit').val();
    var userClass = 'assigneelist';
    var sId = 0;
    $('#assignee').empty();
    var conditionResult = true;
    var str = '';
    for (var user in USERS) {
        var serviceProviderId = 0;
        if (USERS[user].sp_id != null) {
            serviceProviderId = USERS[user].sp_id;
        }
        //if (selectedUnit == 'all' || parseInt(selectedUnit) == USERS[user].s_u_id || (serviceProviderId > 0 && selectedUnit != '')) {
        if (selectedUnit == 'all' || parseInt(selectedUnit) == USERS[user].s_u_id) {
            var userId = USERS[user].usr_id;
            var empCode = USERS[user].emp_code;
            var userCategoryId = USERS[user].usr_cat_id;
            var userName = '';
            if(empCode != null && empCode != ''){
                userName = USERS[user].emp_code + ' - ' +USERS[user].emp_name;
            }else{
                userName = USERS[user].emp_name;
            }
            var combine = userId + '-' + serviceProviderId;
            var isAssignee = USERS[user].is_assignee;
            var isConcurrence = USERS[user].is_approver;
            var isApprover = USERS[user].is_approver;
            var userPermission;
            
            var checkOldUser = true;
            if (userType == 'assignee') {
                userPermission = isAssignee;
                if(UTYPE == 1 && userId == UserId.val()){
                    checkOldUser = false;
                }
            } else if (userType == 'concurrence') {
                userPermission = isConcurrence;
                if(UTYPE == 2 && userId == UserId.val()){
                    checkOldUser = false;
                }
            } else if (userType == 'approval') {
                userPermission = isApprover;
                if(UTYPE == 3 && userId == UserId.val()){
                    checkOldUser = false;
                }
            }

            var concurrenceStatus = true;
            if(userType == 'concurrence' && USERS[user].usr_cat_id == 1){
                concurrenceStatus = false;
            }

            var checkProcess = true;
            if ($.inArray(userId, OLD_USERS_) != -1) {
                checkProcess = false;
            }

            if (CHECK_USER_CATEGORY != 0) {
                if (userType == 'concurrence') {
                  conditionResult = userCategoryId >= CHECK_USER_CATEGORY;
                } else if (userType == 'approval') {
                  conditionResult = userCategoryId <= CHECK_USER_CATEGORY;
                }
            }

            if (userPermission && conditionResult && (serviceProviderId == 0 || sId == serviceProviderId || sId == 0) && concurrenceStatus && checkOldUser && checkProcess) {
                str += '<li id="' + combine + '" class="' + userClass + '" >' + userName + ' <i></i> </li>';
            }
        }
    }
    $('#assignee').append(str);
}

$('#assignee_unit').change(function () {
    if(UTYPE == 1){
        loadUser('assignee');
    }else if(UTYPE == 2){
        loadUser('concurrence');
    }else{
        loadUser('approval');
    }
    
});

$('#assignee').click(function (event) {
    var chkstatus = $(event.target).attr('class');
    if (chkstatus != undefined) {
        if (chkstatus == 'assigneelist active') {
            $(event.target).removeClass('active');
            $(event.target).find('i').removeClass('fa fa-check pull-right');
        } else {
            $('.assigneelist').each(function (index, el) {
                $(el).removeClass('active');
                $(el).find('i').removeClass('fa fa-check pull-right');
            });
            $(event.target).addClass('active');
            $(event.target).find('i').addClass('fa fa-check pull-right');
        }
    }
});

function loadSeatingUnits(){
    $('#assignee').empty();
    $('#assignee_unit').empty();
    $('#assignee_unit').append('<option value=""> Select </option>');
    $('#assignee_unit').append('<option value="all"> All </option>');
    $.each(ASSIGNEE_SU, function (key, value) {
        var option = $('<option></option>');
        option.val(key);
        option.text(value);
        $('#assignee_unit').append(option);
    });
}

function validateFirstTab() {
    if ($('.comp-checkbox:checked').length <= 0) {
        displayMessage(message.nocompliance_selected_forreassign)
        return false;
    } else {
        CHECK_USER_CATEGORY = 0;
        OLD_USERS_ = [];
        if(UTYPE != 1){
            var o_user = 0;
            $('.comp-checkbox:checkbox:checked').each(function (index, el) {
                var id = $(this).attr("id").split('-');
                var c_no = id[1];
                var old_ = $('#combineid'+c_no).attr("data-old").split('#');
                o_user = 0;
                if(UTYPE == 2){
                    o_user = parseInt(old_[2])
                }else if(UTYPE == 3 && old_[1] != null){
                    o_user = parseInt(old_[1])
                }
                if ($.inArray(o_user, OLD_USERS_) == -1 && o_user != 0) {
                    OLD_USERS_.push(o_user);
                    if(CHECK_USER_CATEGORY < getUserLevel(o_user)){
                        CHECK_USER_CATEGORY = getUserLevel(o_user);
                    }
                }
            });
        }
        return true;
    }
};

function showTab() {
    hideall = function() {
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
        } else if (tab == 2) {
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
    } else if (CURRENT_TAB == 2) {
        if (validateFirstTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        } else {
            displayLoader();
            var val_legal_entity_id = LegalEntityId.val();
            var val_domain_id = DomainId.val();
            client_mirror.getUserToAssignCompliance(
                parseInt(val_domain_id), ACTIVE_UNITS, parseInt(val_legal_entity_id), 
                function(error, data) {
                    if (error == null) {
                        two_level_approve = data.t_l_approve;
                        USERS = data.assign_users;
                        $.each(USERS, function(key, value) {
                            id = value.s_u_id;
                            text = value.s_u_name;
                            assignee_flag = value.is_assignee;
                            approver_flag = value.is_approver;
                            if (id != null && assignee_flag) ASSIGNEE_SU[id] = text;
                            if (id != null && approver_flag) APPROVER_SU[id] = text;
                        });
                        loadSeatingUnits();

                        hideall();
                        enabletabevent(2);
                        $('.tab-step-2').addClass('active')
                        $('#tab2').addClass('active in');
                        $('#tab2').show();
                        PreviousButton.show();
                        NextButton.hide();
                        SubmitButton.show();
                        hideLoader();
                    } else {
                        displayMessage(error);
                        hideLoader();
                        CURRENT_TAB -= 1;
                        return false;
                    }
                }
            );
        }
    }
};

function actstatus(element) {
    var id = $(element).attr("id");
    var cstatus = $(element).prop("checked");
    $('.a-' + id).prop("checked", cstatus);
    $('.selected_count').text('Selected Compliance:' + $('.comp-checkbox:checked').length);
}

function getNoRecord(){
    SelectedUnitView.hide();
    var no_record_row = $("#templates .table-no-record tr");
    var clone = no_record_row.clone();
    UnitList.append(clone);
}

function get_selected_count(element){
    $('.selected_count').text('Selected Compliance:' + $('.comp-checkbox:checked').length);
}

function reset(){
    LegalEntityId.val('');
    LegalEntityName.val('');
    DomainId.val('');
    DomainName.val('');
    UserName.val('');
    UserId.val('');
    UnitId.val('');
    UnitName.val('');
    UserType.val('0');
    UnitList.empty();
    SelectedUnitCount.text('0');
    Reason.val('');
}

function loadCompliances(){
    if (SCOUNT == 0) {
        $('.tbody-reassign-compliance').empty();
    }
         
    $.each(ComplianceList, function(key, value) {
        if(LastUnit != value.u_name){
            UCOUNT++;
            var unitRow = $('#templates #accordion-templates');
            var accordion_clone = unitRow.clone();
            $('.unit_name', accordion_clone).text(value.u_name);
            $('.tbody-accordion-list', accordion_clone).attr('id', 'accordion'+UCOUNT);
            $('.tbody-reassign-compliance').append(accordion_clone);
            LastUnit = value.u_name;
            LastAct = '';
            LastType = '';
        }

        if(LastAct != value.act_name){
            ACOUNT++;
            var countrytableRow = $('#templates #act-templates .p-head');
            var clone = countrytableRow.clone();

            $('.act-checkbox', clone).attr('id', ACOUNT);
            $('.act-checkbox', clone).on('click', function() {
                actstatus(this);
            });
            $('.coll-title', clone).attr('id', 'collapse'+ACOUNT);
            $('.acc-title', clone).attr('id', 'heading'+ACOUNT);
            $('.panel-title a span', clone).text(value.act_name);
            $('.panel-title a', clone).attr('href', '#collapse'+ACOUNT);
            $('.panel-title a', clone).attr('aria-controls', 'collapse'+ACOUNT);
            $('.coll-title', clone).attr('id', 'collapse'+ACOUNT);
            $('.coll-title', clone).attr('aria-labelledb', 'heading'+ACOUNT);
            $('#accordion'+ UCOUNT).append(clone);

            /*$('#'+ACOUNT).click(function() {
                actstatus(this);
            });*/
            LastAct = value.act_name;
            LastType = '';
        }

        if(LastType != value.task_type){
            var categoryRow = $('#templates .table-category tr');
            var category_clone = categoryRow.clone();
            $('.category', category_clone).text(value.task_type);
            $('#collapse' + ACOUNT + ' .tbody-compliance-list').append(category_clone);
            LastType = value.task_type;
        }

        SCOUNT++;
        var compliance_id = value.comp_id;
        var compliance_name = value.compliance_name;
        var compliance_description = value.compliance_description;
        var frequency = value.frequency;
        var due_date = value.d_date;
        var validity_date = value.v_date;
        var summary = value.summary;
        var triggerdate = value.trigger_before_days;
        var history_id = value.c_h_id;
        var assignee = value.assignee_name;
        var concur = value.concurrer_name;
        var approver = value.approver_name;
        var unit_id = value.u_id; 

        if(frequency == 'On Occurrence'){
            triggerdate = '-';
        }

        var combineId = compliance_id + '#' + unit_id + '#' + compliance_name + '#' + history_id;
        var COMPRow = $('#templates #compliances .table-compliances .row-compliances');
        var clone2 = COMPRow.clone();
        $('.comp-checkbox', clone2).attr('id', 'c-' + SCOUNT);
        $('.comp-checkbox', clone2).val(compliance_id);
        $('.comp-checkbox', clone2).addClass('a-' + ACOUNT);

        $('.comp-checkbox', clone2).on('click', function() {
            get_selected_count(this);
        });
        
        $('.combineid-class', clone2).attr('id', 'combineid' + SCOUNT);
        $('.combineid-class', clone2).val(combineId);
        $('.combineid-class', clone2).attr("data-old", value.assignee + '#' + value.concurrence_person + '#' + value.approval_person );

        $('.tbl_compliancetask', clone2).text(compliance_name);
        $('.tbl_desc', clone2).attr('title', compliance_description);
        $('.tbl_frequency', clone2).text(frequency);
        $('.tbl_summary', clone2).text(summary);
        $('.tbl_trigger', clone2).text(triggerdate);
        $('.tbl_assignee', clone2).text(assignee);
        $('.tbl_concur', clone2).text(concur);
        $('.tbl_approver', clone2).text(approver);

        if (frequency != 'On Occurrence') {
            if (history_id == null) {
                $('.ddate', clone2).attr('id', 'duedate' + SCOUNT);
                $('.ddate', clone2).val(due_date);
            } else {
                $('.ddate_hidden', clone2).attr('id', 'duedate' + SCOUNT);
                $('.ddate_hidden', clone2).val(due_date);
                $('.tbl_duedate', clone2).text(due_date);
            }
        } else {
            $('.tbl_duedate', clone2).text(due_date);
        }

        $('.tbl_validitydate', clone2).text(validity_date);

        $('#collapse' + ACOUNT + ' .tbody-compliance-list').append(clone2);
        $('#duedate' + SCOUNT).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: 'dd-M-yy',
            monthNames: [
              'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
            ]
        });
        $('.trigger').on('input', function (e) {
            this.value = isNumbers($(this));
        });
    });
        
    if (SCOUNT == 0) {
        $(".total_count_view").hide();
    } else {
        if (totalRecord == SCOUNT) {
            ShowMore.hide();
        } else {
            ShowMore.show();
        }
        $(".total_count").text('Showing 1 to ' + SCOUNT + ' of ' + totalRecord + ' entries');
        $(".total_count_view").show();
    }

    $('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
    hideLoader();
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'legal_entity_id') {
        DomainName.val('');
        DomainId.val('');
        UserName.val('');
        UserId.val('');
        UnitName.val('');
        UnitId.val('');

        callAPI(REASSIGN_FILTER);
    } else if (current_id == 'domain_id') {
        UserName.val('');
        UserId.val('');
        UnitName.val('');
        UnitId.val('');
    } else if (current_id == 'user_id') {
        UnitName.val('');
        UnitId.val('');
    }
    UnitList.empty();
    getNoRecord();
    ACTIVE_UNITS = [];
}

function int(val) {
    try {
        value = val.trim();
        value = parseInt(value);
        return value;
    } catch (e) {
        return null;
    }
}

function activateUnit(element) {
    var cName = $(element).attr("class").split(' ').pop();
    if ($(element).prop("checked")) {
        if(cName == 'type1'){
            $('.type2').prop("checked", false);
            $('.type3').prop("checked", false);
        }
        else if(cName == 'type2'){
            $('.type1').prop("checked", false);
            $('.type3').prop("checked", false);
        }
        else if(cName == 'type3'){
            $('.type1').prop("checked", false);
            $('.type2').prop("checked", false);
        }
        $(this).prop("checked", true);
    }
    //alert($('.unit-checkbox:checked').length)
    SelectedUnitCount.text($('.unit-checkbox:checked').length);
}

function getCompliance(e, type){
    ACTIVE_UNITS = [];
    totalRecord = 0;
    SCOUNT = 0;
    LastAct = '';
    LastUnit = '';
    ACOUNT = 0;
    UCOUNT = 0;
    $('.selected_count').text('Selected Compliance: 0');

    $('.unit-checkbox:checkbox:checked').each(function (index, el) {
        var id = $(this).val().split(',');
        ACTIVE_UNITS.push(parseInt(id[0]));
        totalRecord = totalRecord + parseInt(id[1]);
    });

    if (ACTIVE_UNITS.length == 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
        ShowMore.hide();
        SubmitButton.hide();
        PreviousButton.hide();
        ReassignView.hide();
        ReassignAdd.show();
        UTYPE = type;

        if(UTYPE == 1){
            $('.c_assignee').text('Current Assignee: ' + UserName.val());
            $('.n_assignee').text('New Assignee');
        }else if(UTYPE == 2){
            $('.c_assignee').text('Current Concurrence: ' + UserName.val());
            $('.n_assignee').text('New Concurrence');
        }else{
            $('.c_assignee').text('Current Approver: ' + UserName.val());
            $('.n_assignee').text('New Approver');
        }

        CURRENT_TAB = 1;
        showTab();
        callAPI(GET_COMPLIANCE);
    }
}
function loadUnits() {
    var t1_count = 0;
    var t2_count = 0;
    var t3_count = 0;
    $.each(REASSIGN_UNITS, function(key, value) {
        if(value.user_type_id == 1) {
            t1_count++;
        }
        else if(value.user_type_id == 2) {
            t2_count++;
        }
        else if(value.user_type_id == 3) {
            t3_count++;
        }
    });

    
    UnitList.empty();
    $.each(REASSIGN_UNITS, function(key, value) {
        var rbutton = false;
        if(LastUserType != value.user_type_id){
            var u_type = '';
            if(value.user_type_id == 1) {
                u_type = 'Assignee';
            }
            else if(value.user_type_id == 2) {
                u_type = 'Concurrence';
            }
            else if(value.user_type_id == 3) {
                u_type = 'Approver';
            }
            var type_clone = UserTypeRow.clone();
            $('.tbl_user_type', type_clone).text(u_type);
            UnitList.append(type_clone);

            LastUserType = value.user_type_id;
            rbutton = true;
        }
        var clone = UnitRow.clone();
        $('.unit-checkbox', clone).attr('id', 'unit' + key);
        $('.unit-checkbox', clone).val(value.u_id + ',' + value.no_of_compliances);
        
        if(value.user_type_id == 1) {
            $('.unit-checkbox', clone).addClass('type1');
        }
        else if(value.user_type_id == 2) {
            $('.unit-checkbox', clone).addClass('type2');
        }
        else if(value.user_type_id == 3) {
            $('.unit-checkbox', clone).addClass('type3');
        }

        $('.tbl_unit', clone).text(value.u_name);
        $('.tbl_address', clone).attr('title', value.address + ', ' + value.postal_code);
        $('.tbl_no_of_compliance', clone).text(value.no_of_compliances);
        $('.unit-checkbox', clone).on('click', function(e) {
            activateUnit(this);
        });
        if(rbutton){
            if(value.user_type_id == 1) {
                $('.tbl_reassign', clone).on('click', function(e) {
                    getCompliance(this, 1);
                });
                $('.tbl_reassign', clone).attr('rowspan', t1_count);
            }
            else if(value.user_type_id == 2) {
                $('.tbl_reassign', clone).on('click', function(e) {
                    getCompliance(this, 2);
                });
                $('.tbl_reassign', clone).attr('rowspan', t2_count)
            }
            else if(value.user_type_id == 3) {
                $('.tbl_reassign', clone).on('click', function(e) {
                    getCompliance(this, 3);
                });
                $('.tbl_reassign', clone).attr('rowspan', t3_count);
            }
            $('.tbl_reassign', clone).show();
        }else{
            $('.tbl_reassign', clone).remove();
        }
        //UNIT_CS_ID[value.u_id] = value.u_name;
        UnitList.append(clone);
    });

    if(REASSIGN_UNITS.length == 0){
        getNoRecord();
    }else{
        SelectedUnitView.show();
    }
}

function validateAndShow() {
    val_legal_entity_id = LegalEntityId.val();
    val_domain_id = DomainId.val();
    val_user_id = UserId.val();
    val_user_type = UserType.val();
    val_unit_id = UnitId.val();


    if (val_legal_entity_id.trim().length <= 0) {
        displayMessage(message.legalentity_required);
        return false;
    } else if (val_domain_id.trim().length <= 0) {
        displayMessage(message.domain_required);
        return false;
    } else if (val_user_id.trim().length <= 0) {
        displayMessage(message.user_required);
        return false;
    } else {
        displayLoader();
        client_mirror.getReAssignComplianceUnits(int(val_legal_entity_id), 
            int(val_domain_id), int(val_user_id), int(val_user_type), int(val_unit_id), 
            function(error, data) {
                if (error == null) {
                    REASSIGN_UNITS = data.reassign_units;
                    loadUnits();
                    hideLoader();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            });
    }
}

function pageControls(){
    ShowButton.click(function() {
        LastUserType = '';
        validateAndShow();
    });

    CancelButton.click(function() {
        ReassignView.show();
        ReassignAdd.hide();
    });

    NextButton.click(function() {
        //$('.tbody-compliance-list').empty();
        CURRENT_TAB += 1;
        showTab();
    });

    PreviousButton.click(function() {
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
    });

    ShowMore.click(function() {
        callAPI(GET_COMPLIANCE);
    });

    SubmitButton.click(function() {
        if (validate_thirdtab()) {
            displayLoader();
            setTimeout(function() {
                callAPI(SUBMIT_API)
            }, 500);
        }
    });

    LegalEntityName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACLegalEntity, LegalEntityId, text_val,
            LEGAL_ENTITIES, "le_name", "le_id",
            function(val) {
                onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
            });
    });

    DomainName.keyup(function(e) {
        var condition_fields = ['is_active'];
        var condition_values = [true];
   
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomain, DomainId, text_val,
            DOMAINS, "d_name", "d_id",
            function(val) {
                onAutoCompleteSuccess(DomainName, DomainId, val);
            }, condition_fields, condition_values);
          
    });

    UserName.keyup(function(e) {
        var condition_fields = ['is_active'];
        var condition_values = [true];
    
        if(UserType.val() != '0'){
            condition_fields.push("user_category_id");
            if(UserType.val() == '1'){
                condition_values.push([5,6])
            }else{
                condition_values.push([1,3,4])
            }
        }
        if(LegalEntityId.val() != ''){
            condition_fields.push("le_id");
            condition_values.push(LegalEntityId.val());
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACUser, UserId, text_val,
                FILTER_USERS, "employee_name", "user_id",
                function(val) {
                    onAutoCompleteSuccess(UserName, UserId, val);
                }, condition_fields, condition_values);

        }
    });

    UnitName.keyup(function(e) {
        var condition_fields = ['is_closed'];
        var condition_values = [false];
        
        if(DomainId.val() != ''){
            condition_fields.push("d_ids");
            condition_values.push(DomainId.val())
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACUnit, UnitId, text_val,
                UNITS, "unit_name", "unit_id",
                function(val) {
                    onAutoCompleteSuccess(UnitName, UnitId, val);
                }, condition_fields, condition_values);
        }
        
    });

    Filter_List.keyup(function() {
        var currentFilter = '#' + $(this).attr("class").split(' ').pop() + ' > li';
        var searchText = $(this).val().toLowerCase();
        $(currentFilter).each(function() {
            var currentLiText = $(this).text().toLowerCase();
            showCurrentLi = currentLiText.indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });

    UserType.change(function() {
        UserName.val('');
        UserId.val('');
    });
}

//validation on third wizard
function validate_thirdtab() {
    if ($('.assigneelist.active').text() == '') {
        if(UTYPE == 1){
            displayMessage(message.new_assignee_required);
        }else if(UTYPE == 2){
            displayMessage(message.new_concurrence_required);
        }else{
            displayMessage(message.new_approval_required);
        }
        
        return false;
   /* } else if ($('.concurrencelist.active').text() == '' && two_level_approve) {
        displayMessage(message.concurrence_required);
        return false;
    } else if ($('.approvallist.active').text() == '') {
        displayMessage(message.approval_required);
        return false;*/
    } else if (Reason.val() == '') {
        displayMessage(message.reason_required);
        return false;
    }else if(Reason.val().length > 500) {
        displayMessage(message.reason_should_not_exceed_500)
        return false;
    } else {
        return true;
    }
}

function loadEntityDetails(){
    if(LEGAL_ENTITIES.length > 1){
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
    }else{
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];
     
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(LE_NAME);
        LegalEntityId.val(LE_ID);
        callAPI(REASSIGN_FILTER);
    }
    getNoRecord();
    hideLoader();
}

function initialize() {
    reset();
    loadEntityDetails();
}

$(function() {
    initialize();
    pageControls();
    
});
