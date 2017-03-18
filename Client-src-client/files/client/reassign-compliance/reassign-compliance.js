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
var SCOUNT = 0;
var ACOUNT = 0;
var UCOUNT = 0;
var totalRecord = 10;
var mUnit = 5;

var SELECTED_COMPLIANCE = {};

var Filter_List = $('.filter-list');

function callAPI(api_type) {
    if (api_type == REASSIGN_FILTER) { 
        displayLoader();
        client_mirror.getReassignComplianceFilters(parseInt(LegalEntityId.val()),
            function(error, data) {
                if (error == null) {
                    DOMAINS = data.domains;
                    UNITS = data.units;
                    FILTER_USERS = data.legal_entity_users;
                } else {
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
        var con_Name = null;
        var app_Name = null;

        if ($('.assigneelist.active').attr('id') != undefined) {
            ass_Id = parseInt($('.assigneelist.active').attr('id'));
            ass_Name = $('.assigneelist.active').text().trim();
        }
        if ($('.concurrencelist.active').attr('id') != undefined) {
            con_Id = parseInt($('.concurrencelist.active').attr('id'));
            con_Name = $('.concurrencelist.active').text().trim();
        }
        if ($('.approvallist.active').attr('id') != undefined) {
            app_Id = parseInt($('.approvallist.active').attr('id'));
            app_Name = $('.approvallist.active').text().trim();
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
            /*var C_U_ID = comb_[0] + '-' + comb_[1];
            SELECTED_COMPLIANCE[C_U_ID] = {
                'u_id': parseInt(comb_[1]),
                'comp_id': parseInt(comb_[0]),
                'comp_name': comb_[2],
                'c_h_id': h_id,
                'd_date': d_date,
                'o_assignee': parseInt(old_[0]),
                'o_concurrence_person': parseInt(old_[1]),
                'o_approval_person': parseInt(old_[2])
            } */
            rcData = client_mirror.reassignComplianceDet(parseInt(comb_[1]), parseInt(comb_[0]), comb_[2], 
                h_id, d_date, parseInt(old_[0]), parseInt(old_[1]), parseInt(old_[2]));
            rCompliances.push(rcData);
        });
        /*console.log(SELECTED_COMPLIANCE);*/

        client_mirror.saveReassignCompliance(parseInt(le_id), parseInt(r_from), ass_Id, ass_Name, con_Id, app_Id, rCompliances, reason, 
            function (error, response) {
            if (error == null) {
                //ComplianceList = data.reassign_compliances;
                //ActList = data.level_one_name;
                displaySuccessMessage(message.submit_success);
                ReassignView.show();
                ReassignAdd.hide();
                initialize();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });

/*      assignCompliance = [];
        var totalCompliance = 1;
        var selectedStatus = false;
        var applicableUnitsArray = [];
        for (var i = 1; i <= ACOUNT - 1; i++) {
            var actComplianceCount = $('.a-' + i).length;
            for (var j = 1; j <= actComplianceCount; j++) {
                var complianceApplicable = false;
                if ($('#c-' + totalCompliance).is(':checked')) {
                    complianceApplicable = true;
                    selectedStatus = true;
                }

                if (complianceApplicable) {
                    var combineidVal = $('#combineid' + totalCompliance).val().split('#');
                    var compliance_id = parseInt(combineidVal[0]);
                    var compliance_name = combineidVal[1];
                    var due_date = parseInt(combineidVal[3]);
                    var frequency = combineidVal[2];
                    
                    var appl_units = $('#appl_unit' + totalCompliance).val();
                    if (appl_units != '')
                      appl_units = appl_units.replace(/,\s*$/, '').split(',');
                    var applicable_units = [];
                    for (var u = 0; u < appl_units.length; u++) {
                      applicable_units.push(parseInt(appl_units[u]));
                    }
                    for (var k = 0; k < applicable_units.length; k++) {
                      if ($.inArray(applicable_units[k], applicableUnitsArray) == -1) {
                        applicableUnitsArray.push(parseInt(applicable_units[k]));
                      }
                    }
                    var statutory_dates = [];
                    var current_due_date = '';
                    var current_trigger_day = '';
                    var current_due_dates = [];
                    var validitydate = null;
                    var cvaliditydate = null;
                    var minvaliditydate = false;
                    var maxvaliditydate = false;
                    if ($('#validitydate' + totalCompliance).val() != undefined && $('#validitydate' + totalCompliance).val() != '') {
                      validitydate = $('#validitydate' + totalCompliance).val();
                      cvaliditydate = convert_date(validitydate);
                    }
                    if (frequency != 'On Occurrence') {
                        var dDate = null;
                        var tDay = null;
                        if (due_date > 1) {
                            for (var k = 0; k < due_date; k++) {
                                dDate = $('#duedate' + totalCompliance + '-' + k).val();
                                if (dDate != '') {
                                    tDay = $('#triggerdate' + totalCompliance + '-' + k).val();
                                    current_due_dates.push([
                                      dDate,
                                      tDay
                                    ]);
                                } else {
                                    displayMessage(message.compliance_duedate_required);
                                    hideLoader();
                                    return false;
                                }
                            }
                        } else {
                            dDate = $('#duedate' + totalCompliance).val();
                            if (dDate != '') {
                              tDay = $('#triggerdate' + totalCompliance).val();
                              current_due_dates.push([
                                dDate,
                                tDay
                              ]);
                            } else {
                              displayMessage(message.compliance_duedate_required);
                              hideLoader();
                              return false;
                            }
                        }

                        if (dDate != undefined && dDate != '') {
                            var convertDueDate = convert_date(dDate);
                            if (convertDueDate < currentDate) {
                              displayMessage(message.duedatelessthantoday_compliance + compliance_name);
                              hideLoader();
                              return false;
                            }
                        }
                        var sort_elements = current_due_dates;
                        if (current_due_dates.length > 1) {
                            sort_elements.sort(function (a, b) {
                              a1 = convert_date(a[0]);
                              b1 = convert_date(b[0]);
                              return a1 - b1;
                            });
                            current_due_date = sort_elements[0][0];
                            current_trigger_day = parseInt(sort_elements[0][1]);
                        } else {
                            current_due_date = current_due_dates[0][0];
                            current_trigger_day = parseInt(sort_elements[0][1]);
                        }
                       
                    } else {
                        var statutory_dates = null;
                        var current_due_date = null;
                        var current_trigger_day = null;
                    }
                    assignComplianceData = client_mirror.assignCompliances(compliance_id, compliance_name, statutory_dates, current_due_date, validitydate, current_trigger_day, applicable_units);
                    assignCompliance.push(assignComplianceData);
                }
                totalCompliance++;
            }
        }
        
        if (selectedStatus) {
            var unit_names = '';
            for (var unit in UNITS) {
              if ($.inArray(UNITS[unit].unit_id, ACTIVE_UNITS) >= 0) {
                if (unit_names == '') {
                  unit_names += UNITS[unit].unit_name;
                } else {
                  unit_names += ', ' + UNITS[unit].unit_name;
                }
              }
            }

            function onSuccess(data) {
                displayMessage(message.save_success);
                CURRENT_TAB = 1;
                initialize();
            }
            function onFailure(error, response) {
                displayMessage(error);
                err_message = message.error;
                if (err_message == 'undefined')
                  displayMessage(error);
                else if (error == 'InvalidDueDate') {
                  task = response.compliance_task;
                  displayMessage(message.invalid_duedate + task);
                } else
                displayMessage(err_message);
                hideLoader();
            }
            client_mirror.saveAssignedComplianceFormData(ass_Id, ass_Name, con_Id, con_Name, 
                app_Id, app_Name, assignCompliance, parseInt(le_id), parseInt(d_id),  function (error, response) {
                if (error == null) {
                  onSuccess(response);
                } else {
                  onFailure(error, response);
                }
            });
                
        } else {
            hideLoader();
            displayMessage(message.nocompliance_selected_forassign);
        }*/
    }

    /*else if (api_type == WIZARD_ONE_UNIT_FILTER) { 
        displayLoader();
        var le_id = LEList.find("li.active").attr("id");
        var d_id = DomainList.find("li.active").attr("id");
        client_mirror.getAssignComplianceUnits(parseInt(le_id), parseInt(d_id), function(error, data) {
            if (error == null) {
                UNITS = data.assign_units;
                FREQUENCY = data.comp_frequency;
                loadUnit();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } 
    */
}

//load available user in third wizard
function loadUser(userType) {
    var selectedUnit = null;
    var userClass;
    var sId = 0;
    if (userType == 'assignee') {
        selectedUnit = $('#assignee_unit').val();
        userClass = 'assigneelist';
    } else if (userType == 'concurrence') {
        selectedUnit = $('#concurrence_unit').val();
        userClass = 'concurrencelist';
    } else {
        selectedUnit = $('#approval_unit').val();
        userClass = 'approvallist';
    }
    $('#' + userType).empty();
    var assigneeUserId = null;

    if ($('.assigneelist.active').attr('id') != undefined) {
        var cIds = $('.assigneelist.active').attr('id').split('-');
        assigneeUserId = parseInt(cIds[0]);
        if (parseInt(cIds[1]) != 0)
            sId = cIds[1];
    }
    var concurrenceUserId = null;
    if ($('.concurrencelist.active').attr('id') != undefined) {
        var cIds = $('.concurrencelist.active').attr('id').split('-');
        concurrenceUserId = parseInt(cIds[0]);
        if (parseInt(cIds[1]) != 0)
            sId = cIds[1];
    }
    var approvalUserId = null;
        if ($('.approvallist.active').attr('id') != undefined) {
        var cIds = $('.approvallist.active').attr('id').split('-');
        approvalUserId = parseInt(cIds[0]);
        if (parseInt(cIds[1]) != 0)
            sId = cIds[1];
    }
    var conditionResult = true;
    var conditionResult1 = true;
  
    var str = '';

    for (var user in USERS) {
        var serviceProviderId = 0;
        if (USERS[user].sp_id != null) {
            serviceProviderId = USERS[user].sp_id;
        }
        if (selectedUnit == 'all' || parseInt(selectedUnit) == USERS[user].s_u_id || (serviceProviderId > 0 && selectedUnit != '')) {
            var userId = USERS[user].usr_id;
            var empCode = USERS[user].emp_code;
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
            if (userPermission && (assigneeUserId == null || assigneeUserId != userId) && (approvalUserId == null || approvalUserId != userId) && (concurrenceUserId == null || concurrenceUserId != userId) && (serviceProviderId == 0 || sId == serviceProviderId || sId == 0) && concurrenceStatus && checkOldUser) {
                str += '<li id="' + combine + '" class="' + userClass + '" >' + userName + ' <i></i> </li>';
            }
        }
    }
    $('#' + userType).append(str);
}

$('#assignee_unit').change(function () {
    loadUser('assignee');
});

$('#concurrence_unit').change(function () {
    var assigneeSelectedId = '';
    if ($('.assigneelist.active').attr('id') != undefined) {
        assigneeSelectedId = $('.assigneelist.active').attr('id').split('-')[0];
    }
    loadUser('concurrence');
});

$('#approval_unit').change(function () {
    var assigneeSelectedId = '';
    if ($('.assigneelist.active').attr('id') != undefined) {
        assigneeSelectedId = $('.assigneelist.active').attr('id').split('-')[0];
    }
    loadUser('approval');
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

$('#concurrence').click(function (event) {
    var chkstatus = $(event.target).attr('class');
    if (chkstatus != undefined) {
        if (chkstatus == 'concurrencelist active') {
            $(event.target).removeClass('active');
            $(event.target).find('i').removeClass('fa fa-check pull-right');
        } else {
            $('.concurrencelist').each(function (index, el) {
            $(el).removeClass('active');
            $(el).find('i').removeClass('fa fa-check pull-right');
        });
        $(event.target).addClass('active');
        $(event.target).find('i').addClass('fa fa-check pull-right');
    }
    loadUser('approval');
  }
});

$('#approval').click(function (event) {
    var chkstatus = $(event.target).attr('class');
    if (chkstatus != undefined) {
        if (chkstatus == 'approvallist active') {
            $(event.target).removeClass('active');
            $(event.target).find('i').removeClass('fa fa-check pull-right');
        } else {
            $('.approvallist').each(function (index, el) {
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
    $('#concurrence').empty();
    $('#approval').empty();
    $('#assignee_unit').empty();
    $('#assignee_unit').append('<option value=""> Select </option>');
    $('#assignee_unit').append('<option value="all"> All </option>');
    $.each(ASSIGNEE_SU, function (key, value) {
        var option = $('<option></option>');
        option.val(key);
        option.text(value);
        $('#assignee_unit').append(option);
    });
    $('#concurrence_unit').empty();
    $('#concurrence_unit').append('<option value=""> Select </option>');
    $('#concurrence_unit').append('<option value="all"> All </option>');
    $.each(APPROVER_SU, function (key, value) {
        var option = $('<option></option>');
        option.val(key);
        option.text(value);
        $('#concurrence_unit').append(option);
    });
    $('#approval_unit').empty();
    $('#approval_unit').append('<option value=""> Select </option>');
    $('#approval_unit').append('<option value="all"> All </option>');
    $.each(APPROVER_SU, function (key, value) {
        var option = $('<option></option>');
        option.val(key);
        option.text(value);
        $('#approval_unit').append(option);
    });

    /*if (two_level_approve) {
        $('.c-view').show();
      } else {
        $('.c-view').hide();
    }*/
}

function validateFirstTab() {
    if ($('.comp-checkbox:checked').length <= 0) {
        displayMessage(message.nocompliance_selected_forassign)
        return false;
    } else {
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

    /*$('.a-' + id).each(function() {
        if(cstatus){
            if($('.comp-checkbox:checked').length > mCompliances){
                $(this).prop("checked", false);
                displayMessage(message.maximum_compliance_selection_reached_select_all);
                return false;
            }else{
                $(this).prop("checked", true);
            }
        }else{
            $(this).prop("checked", cstatus);
        }
    });
    $('.selected_count').text('Selected Compliance:' + $('.comp-checkbox:checked').length);*/
}

function getNoRecord(){
    SelectedUnitView.hide();
    var no_record_row = $("#templates .table-no-record tr");
    var clone = no_record_row.clone();
    UnitList.append(clone);
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

        /*$('.comp-checkbox', clone2).on('click', function() {
            get_selected_count(this);
        });*/
        
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
        }else if(UTYPE == 2){
            $('.c_assignee').text('Current Concurrence: ' + UserName.val());
        }else{
            $('.c_assignee').text('Current Approver: ' + UserName.val());
        }

        CURRENT_TAB = 1;
        showTab();
        callAPI(GET_COMPLIANCE);
        /*$(".total_count_view").hide();
        LastAct = '';
        LastSubAct = '';
        statutoriesCount = 1;
        actCount = 1;
        count = 1;
        sno = 1;
        totalRecord = 0;
        AssignStatutoryList.empty();
        SingleAssignStatutoryList.empty();
        SELECTED_COMPLIANCE = {};
        ACT_MAP = {};
        return true;*/
    }
}
function loadUnits() {
    //C_COUNT = 0;
    //UNIT_CS_ID = {};
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
            $('.tbl_reassign', clone).show();
            if(value.user_type_id == 1) {
                $('.tbl_reassign', clone).on('click', function(e) {
                    getCompliance(this, 1);
                });
            }
            else if(value.user_type_id == 2) {
                $('.tbl_reassign', clone).on('click', function(e) {
                    getCompliance(this, 2);
                });
            }
            else if(value.user_type_id == 3) {
                $('.tbl_reassign', clone).on('click', function(e) {
                    getCompliance(this, 3);
                });
            }
        }else{
            $('.tbl_reassign', clone).hide();
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
   
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACUser, UserId, text_val,
            FILTER_USERS, "employee_name", "user_id",
            function(val) {
                onAutoCompleteSuccess(UserName, UserId, val);
            }, condition_fields, condition_values);
          
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
}

//validation on third wizard
function validate_thirdtab() {
    if ($('.assigneelist.active').text() == '' && $('.concurrencelist.active').text() == '' && $('.approvallist.active').text() == '' ) {
        displayMessage(message.atleast_one_user_required_reassign);
        return false;
    } else if (Reason.val() == '') {
        displayMessage(message.reason_required);
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
}

function initialize() {
    reset();
    pageControls();
    loadEntityDetails();
}

$(function() {
    initialize();
});
